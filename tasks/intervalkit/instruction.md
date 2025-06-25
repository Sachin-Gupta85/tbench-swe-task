# Fix the `intervalkit` interval-set library

`intervalkit` is a small Python library that maintains a set of disjoint,
half-open integer intervals `[start, end)`. Several bug reports have come in and
the test suite is failing. Your job is to fix the library so it behaves
correctly, without changing its public API.

## The library

The package lives at `/app/intervalkit/`:

- `IntervalSet.add(start, end)` — add an interval, merging anything it overlaps **or touches**.
- `IntervalSet.remove(start, end)` — remove a range, splitting intervals that straddle it.
- `IntervalSet.contains(point)` — membership (half-open: `end` is excluded).
- `IntervalSet.overlaps(start, end)` — does `[start, end)` share any point with the set?
- `IntervalSet.total_length()` — total covered length.
- `IntervalSet.union(other)` / `IntervalSet.intersection(other)`.

Intervals are half-open, so `[1, 3)` covers `1, 2` but **not** `3`. Adjacent
intervals touch but share no point: `[1, 3)` and `[3, 5)` must be stored merged
as `[1, 5)`, yet they do **not** overlap.

## Reported bugs

1. **Adjacent intervals are not merged.** After `add(1, 3)` then `add(3, 5)` the
   set stores two intervals instead of one `[1, 5)`.
2. **Removing an interior range loses the left side.** From `[0, 10)`,
   `remove(3, 6)` should leave `[0, 3)` and `[6, 10)`, but the `[0, 3)` piece
   disappears.
3. **Intersection invents empty intervals at touch points.** The intersection of
   `[0, 3)` and `[3, 6)` should be empty, but a zero-length interval appears.
4. **`overlaps` reports touching ranges as overlapping.** For a set holding
   `[0, 5)`, `overlaps(5, 10)` returns `True` even though they only touch.

## What to do

Edit the files under `/app/intervalkit/` so the library is correct. Keep the
public API, class name, and method signatures unchanged. Do not change the
half-open semantics. When you are done, every hidden acceptance test must pass.

You may inspect behaviour by running `python3 /app/repro.py`, which prints a few
of the failing cases.
