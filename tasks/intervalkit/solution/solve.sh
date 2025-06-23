#!/bin/bash
# Reference solution: install the corrected package into /app.
# (The verifier then runs the hidden suite against /app/intervalkit.)
set -euo pipefail
mkdir -p /app/intervalkit
cp /solution/intervalkit/*.py /app/intervalkit/
