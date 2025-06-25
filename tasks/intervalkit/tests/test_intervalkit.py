"""Hidden acceptance suite for intervalkit.

The agent never sees this file in its working environment; the verifier runs it
against whatever implementation the agent produced. It tests behaviour only
(never private attributes), so any correct implementation passes.
"""
import random
import unittest

from intervalkit import IntervalSet


def ivals(s):
    return list(s)


class TestAdd(unittest.TestCase):
    def test_add_merges_overlapping(self):
        s = IntervalSet()
        s.add(1, 5)
        s.add(3, 8)
        self.assertEqual(ivals(s), [(1, 8)])

    def test_add_merges_adjacent(self):
        # [1, 3) and [3, 5) touch and must merge into [1, 5).
        s = IntervalSet()
        s.add(1, 3)
        s.add(3, 5)
        self.assertEqual(ivals(s), [(1, 5)])

    def test_add_adjacent_from_left(self):
        s = IntervalSet()
        s.add(5, 10)
        s.add(0, 5)
        self.assertEqual(ivals(s), [(0, 10)])

    def test_add_disjoint_stays_separate(self):
        s = IntervalSet()
        s.add(1, 3)
        s.add(5, 7)
        self.assertEqual(ivals(s), [(1, 3), (5, 7)])

    def test_add_keeps_sorted(self):
        s = IntervalSet()
        for a, b in [(10, 12), (0, 2), (5, 6)]:
            s.add(a, b)
        self.assertEqual(ivals(s), [(0, 2), (5, 6), (10, 12)])

    def test_add_empty_is_noop(self):
        s = IntervalSet()
        s.add(5, 5)
        s.add(8, 2)
        self.assertEqual(ivals(s), [])

    def test_add_swallows_multiple(self):
        s = IntervalSet([(1, 2), (3, 4), (5, 6)])
        s.add(0, 10)
        self.assertEqual(ivals(s), [(0, 10)])


class TestRemove(unittest.TestCase):
    def test_remove_interior_splits_and_keeps_both_sides(self):
        s = IntervalSet([(0, 10)])
        s.remove(3, 6)
        self.assertEqual(ivals(s), [(0, 3), (6, 10)])

    def test_remove_prefix(self):
        s = IntervalSet([(0, 10)])
        s.remove(0, 4)
        self.assertEqual(ivals(s), [(4, 10)])

    def test_remove_suffix(self):
        s = IntervalSet([(0, 10)])
        s.remove(7, 10)
        self.assertEqual(ivals(s), [(0, 7)])

    def test_remove_touching_is_noop(self):
        s = IntervalSet([(0, 5)])
        s.remove(5, 9)   # touches at 5 but shares no point
        self.assertEqual(ivals(s), [(0, 5)])

    def test_remove_spanning_multiple(self):
        s = IntervalSet([(0, 3), (5, 8), (10, 13)])
        s.remove(2, 11)
        self.assertEqual(ivals(s), [(0, 2), (11, 13)])

    def test_remove_entire(self):
        s = IntervalSet([(0, 5)])
        s.remove(-10, 100)
        self.assertEqual(ivals(s), [])


class TestQueries(unittest.TestCase):
    def test_contains(self):
        s = IntervalSet([(0, 5)])
        self.assertTrue(s.contains(0))
        self.assertTrue(s.contains(4))
        self.assertFalse(s.contains(5))   # half-open
        self.assertFalse(s.contains(-1))

    def test_overlaps_touching_is_false(self):
        s = IntervalSet([(0, 5)])
        self.assertFalse(s.overlaps(5, 10))   # touch only
        self.assertFalse(s.overlaps(-5, 0))

    def test_overlaps_true(self):
        s = IntervalSet([(0, 5)])
        self.assertTrue(s.overlaps(4, 10))
        self.assertTrue(s.overlaps(-1, 1))

    def test_total_length(self):
        s = IntervalSet([(0, 5), (10, 13)])
        self.assertEqual(s.total_length(), 8)


class TestSetAlgebra(unittest.TestCase):
    def test_union(self):
        a = IntervalSet([(0, 3)])
        b = IntervalSet([(2, 6), (10, 11)])
        self.assertEqual(ivals(a.union(b)), [(0, 6), (10, 11)])

    def test_intersection_overlap(self):
        a = IntervalSet([(0, 5), (8, 12)])
        b = IntervalSet([(3, 9)])
        self.assertEqual(ivals(a.intersection(b)), [(3, 5), (8, 9)])

    def test_intersection_touching_is_empty(self):
        a = IntervalSet([(0, 3)])
        b = IntervalSet([(3, 6)])
        self.assertEqual(ivals(a.intersection(b)), [])

    def test_intersection_disjoint_is_empty(self):
        a = IntervalSet([(0, 2)])
        b = IntervalSet([(5, 9)])
        self.assertEqual(ivals(a.intersection(b)), [])


class TestDunders(unittest.TestCase):
    def test_len_counts_intervals(self):
        self.assertEqual(len(IntervalSet([(0, 1), (3, 4)])), 2)

    def test_equality(self):
        self.assertEqual(IntervalSet([(0, 5)]), IntervalSet([(0, 2), (2, 5)]))
        self.assertNotEqual(IntervalSet([(0, 5)]), IntervalSet([(0, 4)]))


class TestRandomizedAgainstModel(unittest.TestCase):
    """Fuzz the structure against a brute-force set-of-points reference."""

    DOMAIN = 40

    def test_random_ops(self):
        rng = random.Random(12345)
        for _ in range(300):
            s = IntervalSet()
            model = set()
            for _ in range(40):
                a = rng.randint(0, self.DOMAIN)
                b = rng.randint(0, self.DOMAIN)
                lo, hi = min(a, b), max(a, b)
                if rng.random() < 0.6:
                    s.add(lo, hi)
                    model |= set(range(lo, hi))
                else:
                    s.remove(lo, hi)
                    model -= set(range(lo, hi))

            # Membership must match the model exactly.
            for p in range(-2, self.DOMAIN + 2):
                self.assertEqual(
                    s.contains(p), p in model, f"contains({p}) mismatch"
                )
            # Measure must match.
            self.assertEqual(s.total_length(), len(model))
            # Stored intervals must be sorted, non-empty, and non-touching.
            prev_end = None
            for lo, hi in s:
                self.assertLess(lo, hi, "empty interval stored")
                if prev_end is not None:
                    self.assertLess(prev_end, lo, "touching/overlapping stored")
                prev_end = hi


if __name__ == "__main__":
    unittest.main()
