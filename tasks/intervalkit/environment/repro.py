"""Reproduce the reported bugs. Run: python3 /app/repro.py"""
from intervalkit import IntervalSet

print("1. add(1,3) then add(3,5) — expect [(1, 5)]")
s = IntervalSet()
s.add(1, 3)
s.add(3, 5)
print("   got:", list(s))

print("2. [0,10) remove(3,6) — expect [(0, 3), (6, 10)]")
s = IntervalSet([(0, 10)])
s.remove(3, 6)
print("   got:", list(s))

print("3. intersection of [0,3) and [3,6) — expect []")
print("   got:", list(IntervalSet([(0, 3)]).intersection(IntervalSet([(3, 6)]))))

print("4. [0,5).overlaps(5,10) — expect False")
print("   got:", IntervalSet([(0, 5)]).overlaps(5, 10))
