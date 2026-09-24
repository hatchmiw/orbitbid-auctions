"""Regression tests for mixed numeric and alphanumeric OrbitBid lot IDs."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from mirror_photos import lot_sort_key
from build_contact_sheets import lot_directory_sort_key


class LotSortTests(unittest.TestCase):
    def test_mixed_lot_numbers_do_not_raise(self):
        values = ["12", "2", "12-A", "A12", "12-B", "1", "9", "A2"]
        self.assertEqual(
            sorted(values, key=lot_sort_key),
            ["1", "2", "9", "12", "12-A", "12-B", "A2", "A12"],
        )

    def test_same_prefix_numeric_fragments_sort_naturally(self):
        values = ["10B", "2B", "2A", "10A"]
        self.assertEqual(sorted(values, key=lot_sort_key), ["2A", "2B", "10A", "10B"])

    def test_mixed_case_is_comparable(self):
        values = ["B2", "a10", "A2", "b10"]
        self.assertEqual(sorted(values, key=lot_sort_key), ["A2", "a10", "B2", "b10"])


class ContactSheetSortTests(unittest.TestCase):
    def test_mixed_numeric_and_alphanumeric_lot_folders(self):
        dirs = [Path(n) for n in ("12-A", "2", "A10", "12", "A2", "1", "10")]
        self.assertEqual(
            [d.name for d in sorted(dirs, key=lot_directory_sort_key)],
            ["1", "2", "10", "12", "12-A", "A2", "A10"],
        )


if __name__ == "__main__":
    unittest.main()
