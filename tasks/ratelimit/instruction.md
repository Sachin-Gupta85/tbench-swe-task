# Fix the `ratelimit` token-bucket limiter

`ratelimit.TokenBucket` is a rate limiter with an injectable clock. A bucket holds
up to `capacity` tokens, starts full, and refills at `refill_rate` tokens per unit
time. `allow(now, amount=1)` grants and consumes `amount` tokens if enough are
available, else denies without consuming.

The implementation in `/app/ratelimit/` has bugs:

1. **Refill isn't capped.** After a long idle period the bucket accumulates more
   than `capacity` tokens.
2. **The boundary is wrong.** A request for exactly the number of tokens available
   is denied; it should be granted.
3. **Consumption ignores `amount`.** A granted request always removes one token
   instead of `amount`.

Fix `/app/ratelimit/` so the limiter is correct. Keep the public API
(`TokenBucket(capacity, refill_rate)`, `allow(now, amount=1)`) unchanged.
