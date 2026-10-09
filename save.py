"""Keep each step's numbers in runs/<name>.json so the film reads the same numbers the program printed."""
import json
import sys
from pathlib import Path

RUNS = Path(__file__).parent / "runs"


def save(name, data):
    RUNS.mkdir(exist_ok=True)
    tag = f"py{sys.version_info[0]}{sys.version_info[1]}"
    (RUNS / f"{name}.{tag}.json").write_text(json.dumps(data, indent=1))
    (RUNS / f"{name}.json").write_text(json.dumps(data, indent=1))
