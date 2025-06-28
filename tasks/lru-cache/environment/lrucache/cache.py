"""A fixed-capacity Least-Recently-Used (LRU) cache.

get() and put() both count as "using" a key. When a put would exceed capacity,
the least-recently-used entry is evicted.
"""
from __future__ import annotations

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data: "OrderedDict" = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        return self._data[key]

    def put(self, key, value) -> None:
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=True)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key) -> bool:
        return key in self._data
