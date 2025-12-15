#!/usr/bin/env python3
"""
Reads target JSON files and reports parse errors or structural oddities.
This script DOES NOT write to any database. It only inspects and prints findings.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parent.parent
SAMPLE_LIMIT = 200
NUMERIC_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
SKIP_SUFFIXES = (" 2.json",)

# Explicit targets from the migration blueprint
CORE_JSONS: List[str] = [
    "weekly_updates/week_15/fbs_teams_stats_only.json",
    "weekly_updates/week_15/fbs_offensive_stats.json",
    "weekly_updates/week_15/fbs_defensive_stats.json",
    "weekly_updates/week_15/react_power5_efficiency.json",
    "weekly_updates/week_15/react_power5_teams.json",
    "weekly_updates/week_15/react_fbs_team_rankings.json",
    "weekly_updates/week_15/team_season_summaries_clean.json",
    "weekly_updates/week_15/power5_drives_only.json",
    "weekly_updates/week_15/complete_win_probabilities.json",
    "weekly_updates/week_15/comprehensive_power_rankings_20251203_053934.json",
    "weekly_updates/week_15/all_fbs_ratings_comprehensive_2025_20251203_054653.json",
    "weekly_updates/week_15/ap.json",
    "weekly_updates/week_15/coaches_simplified_ranked.json",
    "weekly_updates/week_15/react_fbs_conferences.json",
    "weekly_updates/week_15/comprehensive_qb_analysis_2025_20251201_110305.json",
]

REFERENCE_JSONS: List[str] = [
    "fbs.json",
    "data/coaches_advanced_rankings.json",
    "power5_coaches_headshots.json",
    "Currentweekgames.json",
    "frontend/public/ats_data_2025.json",
]

FRONTEND_REFERENCE_JSONS: List[str] = [
    "frontend/src/data/lane_kiffin_master.json",
    "frontend/src/data/james_franklin_master.json",
]

# Pattern-based targets so new drops are picked up automatically.
GLOB_TARGETS: Dict[str, List[str]] = {
    # All player metric comprehensive files across positions and timestamps.
    "player_metrics": [
        "player_metrics/*/comprehensive_*_analysis*.json",
        "weekly_updates/week_15/comprehensive_qb_analysis_*.json",
    ],
    # All coach timelines (frontend). Kept as a glob because there are ~80 files.
    "coach_timelines": [
        "frontend/src/data/coach_timelines/*.json",
    ],
}


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return type(value).__name__


def format_counter(counter: Counter) -> str:
    return ", ".join(f"{k}={counter[k]}" for k in sorted(counter))


def should_skip(path: Path) -> bool:
    return any(path.name.endswith(suffix) for suffix in SKIP_SUFFIXES)


def iter_targets() -> Iterable[Tuple[str, Path]]:
    seen: set[Path] = set()

    def add(label: str, rel_path: str) -> Iterable[Tuple[str, Path]]:
        path = ROOT / rel_path
        if should_skip(path):
            return []
        if path in seen:
            return []
        seen.add(path)
        return [(label, path)]

    targets: List[Tuple[str, Path]] = []

    for rel in CORE_JSONS:
        targets.extend(add("core", rel))
    for rel in REFERENCE_JSONS:
        targets.extend(add("reference", rel))
    for rel in FRONTEND_REFERENCE_JSONS:
        targets.extend(add("frontend_ref", rel))

    for label, patterns in GLOB_TARGETS.items():
        for pattern in patterns:
            for path in ROOT.glob(pattern):
                targets.extend(add(label, str(path.relative_to(ROOT))))

    return sorted(targets, key=lambda item: (item[0], str(item[1])))


def analyze_list_rows(rows: List[Any]) -> List[str]:
    warnings: List[str] = []
    element_types = Counter(type_name(el) for el in rows)
    if len(element_types) > 1:
        warnings.append(f"mixed list element types: {format_counter(element_types)}")

    if element_types.keys() == {"dict"}:
        key_types: Dict[str, Counter] = defaultdict(Counter)
        numeric_strings: Counter = Counter()
        non_dict = 0

        for row in rows[:SAMPLE_LIMIT]:
            if not isinstance(row, dict):
                non_dict += 1
                continue
            for k, v in row.items():
                key_types[k][type_name(v)] += 1
                if isinstance(v, str) and NUMERIC_RE.match(v.strip()):
                    numeric_strings[k] += 1

        if non_dict:
            warnings.append(f"{non_dict} non-dict rows in first {SAMPLE_LIMIT}")

        mixed_keys = {
            key: counts for key, counts in key_types.items() if len(counts) > 1
        }
        if mixed_keys:
            parts = [
                f"{key} ({format_counter(counts)})"
                for key, counts in sorted(mixed_keys.items())
            ]
            warnings.append("keys with mixed value types: " + "; ".join(parts))

        numeric_hits = {
            key: count for key, count in numeric_strings.items() if count > 0
        }
        if numeric_hits:
            parts = [f"{key}={count}" for key, count in sorted(numeric_hits.items())]
            warnings.append(
                "numeric-looking strings detected (consider casting): " + ", ".join(parts)
            )

    return warnings


def analyze_dict(obj: Dict[Any, Any]) -> List[str]:
    warnings: List[str] = []
    if not obj:
        warnings.append("empty object")

    key_types: Dict[str, Counter] = defaultdict(Counter)
    numeric_strings: Counter = Counter()
    for k, v in list(obj.items())[:SAMPLE_LIMIT]:
        key_types[str(k)][type_name(v)] += 1
        if isinstance(v, str) and NUMERIC_RE.match(v.strip()):
            numeric_strings[str(k)] += 1

    mixed_keys = {key: counts for key, counts in key_types.items() if len(counts) > 1}
    if mixed_keys:
        parts = [f"{key} ({format_counter(counts)})" for key, counts in sorted(mixed_keys.items())]
        warnings.append("keys with mixed value types: " + "; ".join(parts))

    if numeric_strings:
        parts = [f"{key}={count}" for key, count in sorted(numeric_strings.items())]
        warnings.append(
            "numeric-looking strings detected (consider casting): " + ", ".join(parts)
        )

    return warnings


def analyze_data(data: Any) -> Tuple[Dict[str, Any], List[str]]:
    meta: Dict[str, Any] = {"root_type": type_name(data)}
    warnings: List[str] = []

    if isinstance(data, list):
        meta["items"] = len(data)
        if not data:
            warnings.append("empty list")
        warnings.extend(analyze_list_rows(data))
    elif isinstance(data, dict):
        meta["keys"] = len(data)
        warnings.extend(analyze_dict(data))
    else:
        warnings.append(f"root is {type_name(data)} (expected list or object)")

    return meta, warnings


def summarize_meta(meta: Dict[str, Any]) -> str:
    parts = []
    if "root_type" in meta:
        parts.append(f"type={meta['root_type']}")
    if "items" in meta:
        parts.append(f"items={meta['items']}")
    if "keys" in meta:
        parts.append(f"keys={meta['keys']}")
    return ", ".join(parts)


def check_file(label: str, path: Path) -> Tuple[str, str]:
    if not path.exists():
        return "SKIP", "missing file"

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        return "ERROR", f"JSON decode error: {exc}"
    except Exception as exc:
        return "ERROR", f"read error: {exc}"

    meta, warnings = analyze_data(data)
    meta_desc = summarize_meta(meta)

    if warnings:
        status = "WARN"
        detail = "; ".join(warnings)
    else:
        status = "OK"
        detail = ""

    msg_parts = [meta_desc] if meta_desc else []
    if detail:
        msg_parts.append(detail)
    return status, " | ".join(msg_parts)


def main() -> int:
    targets = list(iter_targets())
    for label, path in targets:
        status, message = check_file(label, path)
        rel = path.relative_to(ROOT)
        suffix = f" ({label})" if label else ""
        if message:
            print(f"[{status}] {rel}{suffix} -> {message}")
        else:
            print(f"[{status}] {rel}{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
