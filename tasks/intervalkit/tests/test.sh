#!/bin/bash
# Verifier entrypoint: put the agent's package on the path and run the hidden
# suite against it. Writes the binary reward to /logs/verifier/reward.txt.
set -uo pipefail
mkdir -p /logs/verifier
WORK=$(mktemp -d)
cp -r /app/intervalkit "$WORK/intervalkit"
cp /tests/test_*.py "$WORK/"

cd "$WORK"
python3 -m unittest discover -s "$WORK" -v
rc=$?

if [ "$rc" -eq 0 ]; then echo -n 1 > /logs/verifier/reward.txt; else echo -n 0 > /logs/verifier/reward.txt; fi
exit 0
