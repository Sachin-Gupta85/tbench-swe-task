"""A sorted set of disjoint half-open integer intervals [start, end).

Invariants maintained at all times:
  * every stored interval has start < end (no empty intervals);
  * intervals are sorted by start;
  * no two stored intervals overlap OR touch (adjacent intervals are merged,
    so [1, 3) and [3, 5) are stored as the single interval [1, 5)).
"""
from __future__ import annotations

from typing import Iterator


class IntervalSet:
    def __init__(self, intervals: list[tuple[int, int]] | None = None) -> None:
        self._ivals: list[tuple[int, int]] = []
        for start, end in intervals or []:
            self.add(start, end)

    # -- mutation ---------------------------------------------------------------

    def add(self, start: int, end: int) -> None:
        """Add [start, end), merging any overlapping or touching intervals."""
        if end <= start:
            return
        res: list[tuple[int, int]] = []
        i, n = 0, len(self._ivals)
        # Keep intervals that end strictly before `start` (b < start => no touch).
        while i < n and self._ivals[i][1] < start:
            res.append(self._ivals[i])
            i += 1
        # Merge every interval that overlaps or touches [start, end) (a <= end).
        while i < n and self._ivals[i][0] <= end:
            start = min(start, self._ivals[i][0])
            end = max(end, self._ivals[i][1])
            i += 1
        res.append((start, end))
        while i < n:
            res.append(self._ivals[i])
            i += 1
        self._ivals = res

    def remove(self, start: int, end: int) -> None:
        """Remove [start, end), splitting intervals that straddle the range."""
        if end <= start:
            return
        res: list[tuple[int, int]] = []
        for a, b in self._ivals:
            if b <= start or a >= end:  # no overlap (touching does not remove)
                res.append((a, b))
                continue
            if a < start:               # left remainder survives
                res.append((a, start))
            if end < b:                 # right remainder survives
                res.append((end, b))
        self._ivals = res

    # -- queries ----------------------------------------------------------------

    def contains(self, point: int) -> bool:
        return any(a <= point < b for a, b in self._ivals)

    def overlaps(self, start: int, end: int) -> bool:
        """True if [start, end) shares any point with the set (half-open)."""
        if end <= start:
            return False
        return any(a < end and start < b for a, b in self._ivals)

    def total_length(self) -> int:
        return sum(b - a for a, b in self._ivals)

    # -- set algebra ------------------------------------------------------------

    def union(self, other: "IntervalSet") -> "IntervalSet":
        result = IntervalSet(self._ivals)
        for a, b in other._ivals:
            result.add(a, b)
        return result

    def intersection(self, other: "IntervalSet") -> "IntervalSet":
        res: list[tuple[int, int]] = []
        i = j = 0
        a, b = self._ivals, other._ivals
        while i < len(a) and j < len(b):
            lo = max(a[i][0], b[j][0])
            hi = min(a[i][1], b[j][1])
            if lo < hi:                 # strict: touching intervals do not intersect
                res.append((lo, hi))
            if a[i][1] < b[j][1]:
                i += 1
            else:
                j += 1
        return IntervalSet(res)

    # -- dunders ----------------------------------------------------------------

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter(self._ivals)

    def __len__(self) -> int:
        return len(self._ivals)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, IntervalSet) and self._ivals == other._ivals

    def __repr__(self) -> str:
        inner = ", ".join(f"[{a}, {b})" for a, b in self._ivals)
        return f"IntervalSet({inner})"
