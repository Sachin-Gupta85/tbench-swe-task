"""Multi-task local verifier (Terminal-Bench style).

Discovers every task under tasks/*/ (each has a meta.json) and checks the two
invariants per task:
    * ORACLE — the reference solution passes the hidden suite.
    * NOP    — the unfixed/stub starting point fails it.

meta.json is one of:
    {"kind": "program", "program": "maze.py"}     # tests read $TASK_BIN
    {"kind": "package", "package": "intervalkit"} # package put on sys.path

Usage: python run_checks.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"


def _run_unittest(tests_dir: Path, env=None, cwd=None) -> bool:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir), "-v"],
        capture_output=True, text=True, env=env, cwd=cwd,
    )
    return proc.returncode == 0


def verify_program(task: Path, meta: dict, which: str) -> bool:
    binpath = task / which / meta["program"]
    env = dict(os.environ, TASK_BIN=str(binpath))
    return _run_unittest(task / "tests", env=env)


def verify_package(task: Path, meta: dict, which: str) -> bool:
    pkg = meta["package"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(task / which / pkg, tmp / pkg)
        for t in (task / "tests").glob("test_*.py"):
            shutil.copy(t, tmp / t.name)
        return _run_unittest(tmp, cwd=tmp)


def verify(task: Path):
    meta = json.loads((task / "meta.json").read_text())
    fn = verify_package if meta["kind"] == "package" else verify_program
    return fn(task, meta, "solution"), fn(task, meta, "environment")


def main() -> int:
    tasks = sorted(d for d in TASKS.iterdir() if (d / "meta.json").exists())
    all_ok = True
    for task in tasks:
        oracle, nop = verify(task)
        ok = oracle and not nop
        all_ok &= ok
        print(f"{task.name:26} Oracle={'1' if oracle else '0'}  "
              f"Nop={'0' if not nop else '1'}  {'✅' if ok else '❌'}")
    print("\n" + (f"ALL {len(tasks)} TASKS GOOD ✅" if all_ok else "CHECK FAILED ❌"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
