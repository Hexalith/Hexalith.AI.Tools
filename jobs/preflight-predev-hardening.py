#!/usr/bin/env python3
"""Pre-flight checks for the recurring story-predev-hardening job.

Runs deterministic repository checks and writes a structured JSON result file.
The LLM-driven job MUST read that file verbatim rather than re-perform the
checks itself; this keeps aborts auditable and avoids fabricated evidence.

Usage:
    python Hexalith.AI.Tools/jobs/preflight-predev-hardening.py [--repo PATH] [--out PATH] [--latest]

Exit code:
    0  all hard checks passed
    1  at least one hard check failed
    2  script error (uncaught exception)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


SPRINT_STATUS_REL = Path("_bmad-output/implementation-artifacts/sprint-status.yaml")
ARTIFACTS_ROOT_REL = Path("_bmad-output/implementation-artifacts")
LESSONS_LEDGER_REL = Path("_bmad-output/process-notes/story-creation-lessons.md")
RESULT_DIR_REL = Path("_bmad-output/process-notes")
LATEST_RESULT_REL = RESULT_DIR_REL / "predev-preflight-latest.json"

DEFAULT_LESSONS_LEDGER_TEXT = """# Story Creation Lessons

This ledger was bootstrapped automatically by `jobs/preflight-predev-hardening.py`
because this repository had no existing story-creation lessons file.

Use this file to record durable lessons for recurring BMAD story creation,
party-mode review, advanced elicitation, and code-review automation.

## L08 - Party Review vs. Elicitation

- Party-mode review is the cross-role critique and triage pass before
  development; it should produce dated trace evidence when completed.
- Advanced elicitation is a separate hardening pass after a completed
  party-mode trace exists; a recommendation to run elicitation is not itself
  completed elicitation evidence.
"""

PREFLIGHT_AUDIT_EXCLUDES = [
    ":(exclude)_bmad-output/process-notes/predev-preflight-*.json",
    ":(exclude)_bmad-output/process-notes/predev-preflight-latest.json",
    ":(exclude)_bmad-output/process-notes/code-review-preflight-*.json",
    ":(exclude)_bmad-output/process-notes/code-review-preflight-latest.json",
    ":(exclude)_bmad-output/process-notes/preflight-*.json",
    ":(exclude)_bmad-output/process-notes/preflight-latest.json",
]

OUTPUT_TRUNCATE_BYTES = 4000


def detect_default_repo() -> Path:
    """Find the application repo when this tools repo is used as a submodule."""
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / SPRINT_STATUS_REL).is_file():
            return candidate
    return cwd


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def truncate(s: str, limit: int = OUTPUT_TRUNCATE_BYTES) -> str:
    if len(s) <= limit:
        return s
    return s[:limit] + f"\n... [truncated, original length {len(s)} chars]"


def run_command(cmd: list[str], cwd: Path) -> dict[str, Any]:
    """Run a command and capture its real output. Never paraphrases."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "command": cmd,
            "exit_code": proc.returncode,
            "stdout": truncate(proc.stdout),
            "stderr": truncate(proc.stderr),
        }
    except FileNotFoundError as e:
        return {"command": cmd, "exit_code": -1, "stdout": "", "stderr": f"FileNotFoundError: {e}"}
    except subprocess.TimeoutExpired as e:
        return {"command": cmd, "exit_code": -1, "stdout": "", "stderr": f"TimeoutExpired after 60s: {e}"}


def check_yaml_parse(repo: Path) -> dict[str, Any]:
    """#1 sprint-status.yaml exists and parses as YAML."""
    path = repo / SPRINT_STATUS_REL
    info: dict[str, Any] = {"id": 1, "name": "sprint-status.yaml parses as YAML", "path": str(path)}
    if not path.is_file():
        info["result"] = "fail"
        info["details"] = f"file does not exist: {path}"
        return info
    try:
        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        info["result"] = "pass"
        info["details"] = "PARSE OK"
        info["file_size_bytes"] = path.stat().st_size
        info["line_count"] = raw.count("\n") + (0 if raw.endswith("\n") else 1)
        if isinstance(data, dict):
            info["top_level_keys"] = sorted(data.keys())
            ds = data.get("development_status")
            info["development_status_count"] = len(ds) if isinstance(ds, dict) else 0
    except yaml.YAMLError as e:
        info["result"] = "fail"
        info["details"] = f"yaml.YAMLError: {type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001
        info["result"] = "fail"
        info["details"] = f"{type(e).__name__}: {e}"
    return info


def check_dir_exists(repo: Path, rel: Path, check_id: int, name: str) -> dict[str, Any]:
    path = repo / rel
    info: dict[str, Any] = {"id": check_id, "name": name, "path": str(path)}
    if path.is_dir():
        info["result"] = "pass"
        info["details"] = "directory exists"
    else:
        info["result"] = "fail"
        info["details"] = "directory does not exist"
    return info


def check_file_readable(repo: Path, rel: Path, check_id: int, name: str) -> dict[str, Any]:
    path = repo / rel
    info: dict[str, Any] = {"id": check_id, "name": name, "path": str(path)}
    if not path.exists():
        info["result"] = "fail"
        info["details"] = "file does not exist"
        return info
    if not path.is_file():
        info["result"] = "fail"
        info["details"] = "path exists but is not a regular file"
        return info
    try:
        with path.open("r", encoding="utf-8") as f:
            f.read(1)
        info["result"] = "pass"
        info["details"] = "file readable"
    except Exception as e:  # noqa: BLE001
        info["result"] = "fail"
        info["details"] = f"file not readable: {type(e).__name__}: {e}"
    return info


def ensure_lessons_ledger(repo: Path) -> tuple[dict[str, Any], list[Path]]:
    """#3 lessons ledger exists, creating the first-run template if absent."""
    path = repo / LESSONS_LEDGER_REL
    created: list[Path] = []
    if not path.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(DEFAULT_LESSONS_LEDGER_TEXT, encoding="utf-8", newline="\n")
            created.append(LESSONS_LEDGER_REL)
        except Exception as e:  # noqa: BLE001
            info: dict[str, Any] = {
                "id": 3,
                "name": "lessons ledger readable",
                "path": str(path),
                "result": "fail",
                "details": f"could not create first-run lessons ledger: {type(e).__name__}: {e}",
            }
            return info, created
    info = check_file_readable(repo, LESSONS_LEDGER_REL, 3, "lessons ledger readable")
    if created and info["result"] == "pass":
        info["details"] = "file created from first-run template and readable"
        info["created"] = True
    return info, created


def resolve_story_artifact(repo: Path, story_key: str) -> tuple[bool, list[str]]:
    """Implements the Story Artifact Resolution rule from the job spec."""
    root = repo / ARTIFACTS_ROOT_REL
    candidates: list[Path] = []
    flat = root / f"{story_key}.md"
    if flat.is_file():
        candidates.append(flat)
    folder = root / story_key
    if folder.is_dir():
        index = folder / "index.md"
        if index.is_file():
            candidates.append(index)
        for child in sorted(folder.glob("*.md")):
            if child not in candidates:
                candidates.append(child)
    return (len(candidates) > 0, [str(p) for p in candidates])


def check_status_artifact_consistency(repo: Path, yaml_check: dict[str, Any]) -> dict[str, Any]:
    """#4 status-artifact consistency."""
    info: dict[str, Any] = {"id": 4, "name": "status-artifact consistency"}
    if yaml_check["result"] != "pass":
        info["result"] = "skipped"
        info["details"] = "skipped because check #1 (yaml parse) did not pass"
        return info
    try:
        data = yaml.safe_load((repo / SPRINT_STATUS_REL).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        info["result"] = "skipped"
        info["details"] = f"could not re-parse yaml: {type(e).__name__}: {e}"
        return info
    statuses: dict[str, Any] = (data or {}).get("development_status") or {}
    drifts: list[dict[str, str]] = []
    artifact_required = {"ready-for-dev", "in-progress", "review", "done"}
    checked = 0
    for key, status in statuses.items():
        if key.startswith("epic-") or key.endswith("-retrospective"):
            continue
        if status == "blocked":
            continue
        checked += 1
        exists, _ = resolve_story_artifact(repo, key)
        if status == "backlog" and exists:
            drifts.append({"key": key, "status": str(status), "artifact": "present", "expected": "absent"})
        elif status in artifact_required and not exists:
            drifts.append({"key": key, "status": str(status), "artifact": "absent", "expected": "present"})
    info["story_keys_checked"] = checked
    if drifts:
        info["result"] = "fail"
        info["details"] = f"{len(drifts)} status-artifact drift(s) found"
        info["drifts"] = drifts
    else:
        info["result"] = "pass"
        info["details"] = f"no drift across {checked} story keys"
    return info


def check_working_tree(repo: Path, extra_excludes: list[Path] | None = None) -> dict[str, Any]:
    """#5 working tree cleanliness, excluding audit files and same-run bootstraps."""
    info: dict[str, Any] = {"id": 5, "name": "working tree cleanliness"}
    excludes = list(PREFLIGHT_AUDIT_EXCLUDES)
    for rel in extra_excludes or []:
        excludes.append(f":(exclude){rel.as_posix()}")
    cmd_info = run_command(["git", "status", "--porcelain", "--", ".", *excludes], cwd=repo)
    info.update(cmd_info)
    if cmd_info["exit_code"] != 0:
        info["result"] = "fail"
        info["details"] = f"git status --porcelain exited {cmd_info['exit_code']}"
        return info
    lines = [line for line in cmd_info["stdout"].splitlines() if line.strip()]
    info["dirty_path_count"] = len(lines)
    if lines:
        info["result"] = "fail"
        info["details"] = f"{len(lines)} dirty path(s)"
    else:
        info["result"] = "pass"
        info["details"] = "0 dirty paths"
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-flight checks for story-predev-hardening job.")
    parser.add_argument("--repo", type=Path, default=detect_default_repo(),
                        help=("Path to application repo root (default: nearest ancestor containing "
                              "_bmad-output/implementation-artifacts/sprint-status.yaml, otherwise cwd)"))
    parser.add_argument("--out", type=Path, default=None,
                        help="JSON result path (default: _bmad-output/process-notes/predev-preflight-{ISO}.json)")
    parser.add_argument("--latest", action="store_true",
                        help="Also write _bmad-output/process-notes/predev-preflight-latest.json")
    args = parser.parse_args()

    repo = args.repo.resolve()
    timestamp = now_iso()

    yaml_check = check_yaml_parse(repo)
    lessons_check, bootstrapped_paths = ensure_lessons_ledger(repo)
    checks: list[dict[str, Any]] = [
        yaml_check,
        check_dir_exists(repo, ARTIFACTS_ROOT_REL, 2, "artifacts root exists"),
        lessons_check,
        check_status_artifact_consistency(repo, yaml_check),
        check_working_tree(repo, bootstrapped_paths),
    ]
    overall = "fail" if any(c["result"] == "fail" for c in checks) else "pass"

    result = {
        "schema_version": 1,
        "produced_by": "jobs/preflight-predev-hardening.py",
        "timestamp": timestamp,
        "repo": str(repo),
        "result": overall,
        "bootstrap_actions": [
            {
                "action": "created",
                "path": str(repo / rel),
                "reason": "first-run lessons ledger was missing",
            }
            for rel in bootstrapped_paths
        ],
        "checks": checks,
        "note_to_llm": (
            "This file was produced by jobs/preflight-predev-hardening.py. The "
            "recurring pre-dev hardening job MUST quote the contents of this file "
            "verbatim when reporting pre-flight results; do NOT re-run the checks "
            "yourself, paraphrase them, or summarize them in your own words."
        ),
    }

    out_path = args.out or (repo / RESULT_DIR_REL / f"predev-preflight-{timestamp.replace(':', '')}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.latest:
        latest = repo / LATEST_RESULT_REL
        latest.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"PREFLIGHT {overall.upper()} at {timestamp}")
    print(f"  result file: {out_path}")
    for c in checks:
        marker = {"pass": "OK", "fail": "FAIL", "skipped": "SKIP", "info": "INFO"}.get(c["result"], "?")
        print(f"  [{marker:4}] #{c['id']} {c['name']}: {c.get('details', '')}")

    return 0 if overall == "pass" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"PREFLIGHT SCRIPT ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        raise SystemExit(2)
