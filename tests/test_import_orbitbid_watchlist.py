import json
import tempfile
import unittest
from pathlib import Path
import importlib.util


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "import_orbitbid_watchlist.py"
SPEC = importlib.util.spec_from_file_location("import_orbitbid_watchlist", MODULE_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class ImportOrbitBidWatchlistTests(unittest.TestCase):
    def capture(self, ids):
        return {
            "schema": mod.SCHEMA,
            "captured_at": "2026-09-28T15:00:00Z",
            "source_host": mod.SOURCE_HOST,
            "lot_ids": ids,
        }

    def test_validates_and_deduplicates_ids(self):
        captured_at, ids = mod.validate_capture(self.capture([22, "11", 22]))
        self.assertEqual(captured_at, "2026-09-28T15:00:00Z")
        self.assertEqual(ids, [11, 22])

    def test_rejects_wrong_host(self):
        payload = self.capture([11])
        payload["source_host"] = "example.com"
        with self.assertRaises(ValueError):
            mod.validate_capture(payload)

    def test_matches_saved_public_lots_without_copying_bid_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auction_dir = root / "auctions" / "1879"
            auction_dir.mkdir(parents=True)
            (auction_dir / "lots.json").write_text(
                json.dumps(
                    {
                        "lots": [
                            {
                                "internal_id": 1705100,
                                "requested_lot_number": "18100",
                                "title": "Scaffolding",
                                "amount": 125,
                                "bid_count": 8,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            output = root / "watchlists" / "orbitbid.json"
            data = mod.build_import(
                self.capture([1705100, 9999999]),
                root=root,
                output=output,
                imported_at="2026-09-28T15:01:00Z",
            )

            self.assertEqual(data["matched_saved_lots"], 1)
            self.assertEqual(data["unmatched_lots"], 1)
            saved = data["lots"][0]["saved_lots"][0]
            self.assertEqual(saved["auction_id"], "1879")
            self.assertEqual(saved["lot"], "18100")
            self.assertEqual(saved["title"], "Scaffolding")
            self.assertNotIn("amount", saved)
            self.assertNotIn("bid_count", saved)

    def test_preserves_first_seen_for_still_watched_lot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "watchlists" / "orbitbid.json"
            output.parent.mkdir(parents=True)
            output.write_text(
                json.dumps(
                    {
                        "lots": [
                            {
                                "internal_id": 42,
                                "first_seen_at": "2026-09-20T12:00:00Z",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            data = mod.build_import(
                self.capture([42]),
                root=root,
                output=output,
                imported_at="2026-09-28T15:01:00Z",
            )
            self.assertEqual(data["lots"][0]["first_seen_at"], "2026-09-20T12:00:00Z")
            self.assertEqual(data["lots"][0]["last_seen_at"], "2026-09-28T15:00:00Z")


if __name__ == "__main__":
    unittest.main()
