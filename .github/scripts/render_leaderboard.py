#!/usr/bin/env python3
"""Render OPS Challenge leaderboard data as repository Markdown."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXCLUDED_USERS = {"github-classroom[bot]"}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_entries(task_id: str, leaderboard_dir: Path) -> list[dict[str, Any]]:
    users_dir = leaderboard_dir / "tasks" / task_id / "users"
    if not users_dir.exists():
        return []

    entries: list[dict[str, Any]] = []
    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir() or user_dir.name in EXCLUDED_USERS:
            continue

        stats = load_json(user_dir / "stats.json", {})
        best_time = stats.get("best_time")
        if best_time is None:
            continue

        entries.append(
            {
                "username": user_dir.name,
                "best_time": float(best_time),
                "total_submissions": int(stats.get("total_submissions", 0)),
                "passed_submissions": int(stats.get("passed_submissions", 0)),
                "failed_submissions": int(stats.get("failed_submissions", 0)),
            }
        )

    entries.sort(key=lambda item: (item["best_time"], item["username"].lower()))
    return entries


def render_leaderboard(
    task_json: Path,
    leaderboard_dir: Path,
    generated_at: str | None = None,
) -> str:
    task = load_json(task_json, {})
    task_id = task.get("task_id", "unknown")
    title = task.get("title", task_id)
    generated_at = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entries = load_entries(task_id, leaderboard_dir)

    lines = [
        "# OPS Challenge Leaderboard",
        "",
        f"**Task:** `{task_id}` - {title}",
        f"**Updated:** {generated_at}",
        "",
        "Rankings are sorted by **Best Time** ascending. Only passing submissions are ranked.",
        "",
    ]

    if entries:
        lines.extend(
            [
                "| Rank | User | Best Time (s) | Submissions | Passed | Failed |",
                "| ---: | :--- | ------------: | ----------: | -----: | -----: |",
            ]
        )
        for rank, entry in enumerate(entries, start=1):
            lines.append(
                f"| {rank} | `{entry['username']}` | {entry['best_time']:.3f} | "
                f"{entry['total_submissions']} | {entry['passed_submissions']} | "
                f"{entry['failed_submissions']} |"
            )
    else:
        lines.append("No passing submissions yet.")

    lines.extend(
        [
            "",
            "---",
            "",
            "_This file is generated automatically by the grading workflow. Do not edit it manually._",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-json", required=True, type=Path)
    parser.add_argument("--leaderboard-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rendered = render_leaderboard(args.task_json, args.leaderboard_dir)
    args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
