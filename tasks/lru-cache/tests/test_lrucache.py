"""Hidden acceptance suite for the LRU cache."""
import unittest

from lrucache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_basic_get_put(self):
        c = LRUCache(2)
        c.put("a", 1)
        self.assertEqual(c.get("a"), 1)
        self.assertIsNone(c.get("missing"))

    def test_evicts_least_recently_used(self):
        c = LRUCache(3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        self.assertEqual(c.get("a"), 1)   # 'a' is now most-recently-used
        c.put("d", 4)                     # over capacity -> evict LRU, which is 'b'
        self.assertNotIn("b", c)
        for k in ("a", "c", "d"):
            self.assertIn(k, c)

    def test_get_refreshes_recency(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.get("a"), 1)   # refresh 'a'
        c.put("c", 3)                     # evict LRU 'b'
        self.assertNotIn("b", c)
        self.assertIn("a", c)
        self.assertIn("c", c)

    def test_update_refreshes_recency(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("a", 10)                    # update 'a' -> now most-recent
        c.put("c", 3)                     # evict LRU 'b'
        self.assertNotIn("b", c)
        self.assertEqual(c.get("a"), 10)
        self.assertIn("c", c)

    def test_new_item_survives_eviction(self):
        c = LRUCache(1)
        c.put("a", 1)
        c.put("b", 2)                     # evicts 'a', keeps the new 'b'
        self.assertIn("b", c)
        self.assertNotIn("a", c)

    def test_len_and_capacity_guard(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        self.assertEqual(len(c), 2)
        with self.assertRaises(ValueError):
            LRUCache(0)


if __name__ == "__main__":
    unittest.main()
