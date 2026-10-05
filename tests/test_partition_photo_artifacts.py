"""Tests for OrbitBid photo artifact sharding."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from partition_photo_artifacts import plan_shards


class PhotoShardPlanTests(unittest.TestCase):
    def test_keeps_each_lot_whole(self):
        shards = plan_shards(
            [("100", 40), ("101", 40), ("102", 40)],
            target_bytes=75,
            hard_max_bytes=100,
        )
        self.assertEqual(shards, [[("100", 40)], [("101", 40)], [("102", 40)]])

    def test_fills_shards_greedily_without_exceeding_target_when_possible(self):
        shards = plan_shards(
            [("1", 30), ("2", 35), ("3", 20), ("4", 10)],
            target_bytes=70,
            hard_max_bytes=100,
        )
        self.assertEqual(
            shards,
            [[("1", 30), ("2", 35)], [("3", 20), ("4", 10)]],
        )

    def test_single_lot_may_exceed_target_but_not_hard_max(self):
        shards = plan_shards(
            [("1", 80), ("2", 10)],
            target_bytes=70,
            hard_max_bytes=100,
        )
        self.assertEqual(shards, [[("1", 80)], [("2", 10)]])

    def test_single_lot_over_hard_max_fails(self):
        with self.assertRaises(ValueError):
            plan_shards(
                [("1", 101)],
                target_bytes=70,
                hard_max_bytes=100,
            )

    def test_invalid_size_limits_fail(self):
        with self.assertRaises(ValueError):
            plan_shards([("1", 1)], target_bytes=101, hard_max_bytes=100)


if __name__ == "__main__":
    unittest.main()
