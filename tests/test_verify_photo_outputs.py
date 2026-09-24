"""Regression tests for snapshot-pure OrbitBid photo verification."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_photo_outputs import main as verify_main


class PhotoArtifactValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.original_cwd = Path.cwd()
        os.chdir(self.temp.name)
        self.addCleanup(os.chdir, self.original_cwd)

        self.auction = Path("auctions/1879")
        self.photos = self.auction / "photos"
        folder = self.photos / "11"
        folder.mkdir(parents=True)
        self.image_path = folder / "01.jpg"
        self.image_path.write_bytes(b"test-image")
        (folder / "review.jpg").write_bytes(b"test-sheet")

        data = {
            "lots": [
                {
                    "requested_lot_number": "11",
                    "images": [{"large_path": "https://example.test/current-image.jpg"}],
                },
                {"requested_lot_number": "12", "images": []},
            ]
        }
        (self.auction / "lots.json").write_text(json.dumps(data), encoding="utf-8")
        manifest = {
            "lot_count": 2,
            "photo_count": 1,
            "error_count": 0,
            "photos": [
                {
                    "lot": "11",
                    "index": 1,
                    "source_url": "https://example.test/current-image.jpg",
                }
            ],
        }
        (self.photos / "manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def verify(self):
        with patch.object(sys, "argv", ["verify_photo_outputs.py", "1879"]):
            with contextlib.redirect_stdout(io.StringIO()):
                return verify_main()

    def test_valid_snapshot_with_photo_free_lot(self):
        self.assertEqual(self.verify(), 0)

    def test_stale_lot_folder_rejected(self):
        stale = self.photos / "old-lot"
        stale.mkdir()
        (stale / "01.jpg").write_bytes(b"old")
        with self.assertRaisesRegex(SystemExit, "stale/extra"):
            self.verify()

    def test_stale_image_in_current_lot_rejected(self):
        (self.photos / "11" / "02.jpg").write_bytes(b"old")
        with self.assertRaisesRegex(SystemExit, "stale/extra image"):
            self.verify()

    def test_wrong_source_url_rejected(self):
        manifest_path = self.photos / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["photos"][0]["source_url"] = "https://example.test/old-image.jpg"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "mapping mismatch"):
            self.verify()

    def test_missing_image_rejected(self):
        self.image_path.unlink()
        with self.assertRaisesRegex(SystemExit, "missing/empty"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
