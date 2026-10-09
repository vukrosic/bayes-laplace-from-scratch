#!/bin/sh
# Runs the seven steps in order. Plain Python 3, no libraries. About 40 seconds.
PY="${PYTHON:-python3}"
cd "$(dirname "$0")" || exit 1
for f in step1_table step2_test step3_succession step4_births step5_start step6_mail step7_buttons; do
  echo "--- $f"
  "$PY" "$f.py" || exit 1
done
