#!/usr/bin/env python3
"""Call Workflow AI's checks for a child ID without changing the shared workflow."""
import importlib.util
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("workflow", root/"workflow-ai/scripts/workflow.py")
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)
workflow.TASK_ID = re.compile(r"^(FEAT|CONN|UI|ARCH)-[0-9]{3,6}(?:-[0-9]{2})?$")
assert workflow.TASK_ID.fullmatch("UI-004-01")
assert workflow.TASK_ID.fullmatch("UI-004")
assert not workflow.TASK_ID.fullmatch("../UI-004-01")
if __name__ == "__main__":
    raise SystemExit(workflow.main(sys.argv[1:]))
