"""Hidden acceptance suite for the token-bucket rate limiter."""
import unittest

from ratelimit import TokenBucket


class TestTokenBucket(unittest.TestCase):
    def test_full_bucket_allows_exactly_capacity(self):
        b = TokenBucket(capacity=3, refill_rate=0)
        self.assertTrue(b.allow(0))
        self.assertTrue(b.allow(0))
        self.assertTrue(b.allow(0))       # 3rd uses the last token
        self.assertFalse(b.allow(0))      # now empty

    def test_exact_boundary_is_allowed(self):
        # Exactly `amount` tokens available -> must be granted (>=, not >).
        b = TokenBucket(capacity=2, refill_rate=0)
        self.assertTrue(b.allow(0, amount=2))
        self.assertFalse(b.allow(0, amount=1))

    def test_amount_is_consumed(self):
        b = TokenBucket(capacity=5, refill_rate=0)
        self.assertTrue(b.allow(0, amount=3))   # 5 -> 2
        self.assertFalse(b.allow(0, amount=3))  # only 2 left
        self.assertTrue(b.allow(0, amount=2))   # 2 -> 0

    def test_refill_over_time(self):
        b = TokenBucket(capacity=10, refill_rate=2)   # 2 tokens / unit time
        self.assertTrue(b.allow(0, amount=10))        # drain
        self.assertFalse(b.allow(0, amount=1))        # empty
        self.assertTrue(b.allow(2, amount=4))         # 2s * 2 = 4 refilled
        self.assertFalse(b.allow(2, amount=1))        # drained again

    def test_refill_capped_at_capacity(self):
        # After a long idle, tokens must not exceed capacity.
        b = TokenBucket(capacity=5, refill_rate=1)
        self.assertTrue(b.allow(0, amount=5))         # drain
        # idle for 100 units: would be 100 tokens uncapped, but cap is 5.
        for _ in range(5):
            self.assertTrue(b.allow(100))
        self.assertFalse(b.allow(100))                # only 5 were available

    def test_no_time_travel_refill(self):
        b = TokenBucket(capacity=4, refill_rate=1)
        self.assertTrue(b.allow(0, amount=4))
        self.assertFalse(b.allow(-5, amount=1))       # earlier time -> no refill


if __name__ == "__main__":
    unittest.main()
