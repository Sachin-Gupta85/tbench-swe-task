"""A token-bucket rate limiter with an injectable clock.

A bucket holds up to `capacity` tokens and refills at `refill_rate` tokens per
unit time. `allow(now, amount)` grants the request if enough tokens are present,
consuming them; otherwise it denies without consuming. Time is passed in, so the
limiter is deterministic and testable.
"""
from __future__ import annotations


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float) -> None:
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)   # starts full
        self.last = 0.0

    def _refill(self, now: float) -> None:
        if now > self.last:
            gained = (now - self.last) * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + gained)
            self.last = now

    def allow(self, now: float, amount: float = 1) -> bool:
        self._refill(now)
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False
