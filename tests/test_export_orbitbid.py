"""Regression tests for direct OrbitBid catalog discovery safety."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from export_orbitbid import catalog_lot_ids_from_html, validate_lot_set


class CatalogParserTests(unittest.TestCase):
    def test_only_collects_lot_links_inside_main(self):
        html = """
        <html><body>
          <a href="/lot/999999/unrelated">outside</a>
          <main>
            <a href="/lot/101/first">first</a>
            <a href="https://bid.orbitbid.com/lot/102/second?x=1">second</a>
            <a href="/lot/101/duplicate">duplicate</a>
          </main>
          <footer><a href="/lot/888888/unrelated">outside</a></footer>
        </body></html>
        """
        self.assertEqual(catalog_lot_ids_from_html(html), [101, 102])

    def test_empty_main_returns_no_lots(self):
        html = '<main><a href="/auction/1920">auction</a></main>'
        self.assertEqual(catalog_lot_ids_from_html(html), [])


class AuctionSafetyTests(unittest.TestCase):
    def test_close_times_within_two_days_pass(self):
        validate_lot_set([
            {"end_time": 1_800_000_000},
            {"end_time": 1_800_086_400},
        ])

    def test_close_times_spanning_more_than_two_days_fail(self):
        with self.assertRaises(RuntimeError):
            validate_lot_set([
                {"end_time": 1_800_000_000},
                {"end_time": 1_800_259_201},
            ])

    def test_missing_close_times_fail(self):
        with self.assertRaises(RuntimeError):
            validate_lot_set([{"end_time": None}, {"end_time": ""}])


if __name__ == "__main__":
    unittest.main()
