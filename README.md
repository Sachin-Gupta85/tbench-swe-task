# 🧪 tbench-swe-task — SWE-bench-style bug-fix tasks

> A collection of self-contained **AI-agent evaluation tasks** in the **Terminal-Bench 3** format. Each task gives an agent a small library with planted bugs; the agent must fix it so a hidden test suite passes — without changing the public API.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Format](https://img.shields.io/badge/format-Terminal--Bench%203-6f42c1)
![Tasks](https://img.shields.io/badge/tasks-4-informational)
![Deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Each task is a realistic **SWE-bench-shaped** bug-fix: a bug report, a buggy
starting package, a reference fix, and an independent hidden grader (including
randomized fuzzing) that can't be gamed by special-casing examples.

---

## 📦 Tasks

| Task | Library | Bugs to fix |
|---|---|---|
| [`intervalkit`](tasks/intervalkit) | disjoint half-open interval set | adjacency merge, interior removal, touch-point intersection, half-open overlap |
| [`ratelimit`](tasks/ratelimit) | token-bucket rate limiter | uncapped refill, availability boundary, consumption amount |
| [`lru-cache`](tasks/lru-cache) | fixed-capacity LRU cache | recency on read, recency on update, wrong eviction target |
| [`csv-parser`](tasks/csv-parser) | RFC-4180 CSV parser | escaped quotes, CRLF line endings |

Each task folder contains `instruction.md` (the "issue"), `task.toml` (metadata),
`environment/` (the buggy package), `solution/` (the reference fix), and `tests/`
(the hidden grader).

## ✅ Verify every task (no dependencies)

```bash
python3 run_checks.py
```

```
csv-parser    Oracle=1  Nop=0  ✅
intervalkit   Oracle=1  Nop=0  ✅
lru-cache     Oracle=1  Nop=0  ✅
ratelimit     Oracle=1  Nop=0  ✅
ALL 4 TASKS GOOD ✅
```

- **Oracle = 1** — the reference `solution/` passes every hidden test.
- **Nop = 0** — the untouched buggy `environment/` fails, so the task is non-trivial.

## 📎 Note on the format

These follow the **task-authoring** structure of Terminal-Bench 3 (instruction +
environment + reference solution + independent tests) with a lightweight local
runner, published as **portfolio examples of agent-task design** — not drop-in
submissions to any specific benchmark program.

## 📝 License

MIT — see [LICENSE](LICENSE).
