# Fix the `lrucache` LRU cache

`lrucache.LRUCache(capacity)` is a fixed-size Least-Recently-Used cache. Both
`get(key)` and `put(key, value)` count as *using* a key. When a `put` pushes the
size past `capacity`, the **least-recently-used** entry must be evicted.

The implementation in `/app/lrucache/` has bugs:

1. **`get` doesn't refresh recency** — reading a key doesn't mark it most-recently
   used, so the wrong entry is evicted later.
2. **Updating a key doesn't refresh recency** — `put` on an existing key changes
   the value but not its position.
3. **Eviction removes the wrong entry** — it evicts the most-recently-used item
   instead of the least-recently-used one.

Fix `/app/lrucache/` so eviction follows true LRU order. Keep the public API
(`LRUCache(capacity)`, `get`, `put`, `len()`, `in`) unchanged.
