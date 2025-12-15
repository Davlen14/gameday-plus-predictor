#!/usr/bin/env python3
"""
Merge multiple single-school coach profiles into one master career file.

Usage:
  python scripts/merge_coach_profiles.py --coach "Matt Campbell" \
      --output enhanced_coaches_v2/matt_campbell_master.json \
      campbell_toledo.json campbell_iowa_state.json

Assumptions:
  - Input files follow the shape produced by universal_coach_analyzer.py
    (metadata.school, games array, rankings, draft_picks, talent_ratings, betting_lines_2025).
  - No network calls are made; this just merges local JSON.
"""
import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def type_safe_get(dct, *keys, default=None):
    cur = dct
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def calculate_record(games: List[dict], school: str) -> Tuple[int, int, int]:
    wins = losses = ties = 0
    for game in games:
        home = game.get("homeTeam")
        away = game.get("awayTeam")
        if home is None or away is None:
            continue
        if school not in (home, away):
            continue
        home_points = game.get("homePoints")
        away_points = game.get("awayPoints")
        if home_points is None or away_points is None:
            continue
        team_score = home_points if home == school else away_points
        opp_score = away_points if home == school else home_points
        if team_score > opp_score:
            wins += 1
        elif team_score < opp_score:
            losses += 1
        else:
            ties += 1
    return wins, losses, ties


def load_profiles(files: List[Path]) -> List[dict]:
    profiles = []
    for path in files:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            profiles.append((path, data))
    return profiles


def normalize_school_name(profile: dict, fallback: str) -> str:
    # Prefer explicit metadata.school, otherwise current_team.name, otherwise fallback
    return (
        type_safe_get(profile, "metadata", "school")
        or type_safe_get(profile, "current_team", "name")
        or fallback
    )


def merge_profiles(coach_name: str, profiles: List[Tuple[Path, dict]]) -> dict:
    stints = []
    all_games = []
    all_rankings = []
    all_draft_picks = []
    all_talent = []
    all_betting = []

    schools_seen = []

    for path, prof in profiles:
        school = normalize_school_name(prof, path.stem.split("_")[-1].replace("_", " ").title())
        games = prof.get("games", [])
        rankings = prof.get("rankings", [])
        draft = prof.get("draft_picks", [])
        talent = prof.get("talent_ratings", [])
        betting = prof.get("betting_lines_2025", [])

        # Tag entries with school for downstream filtering
        for g in games:
            g = dict(g)
            g["school"] = school
            all_games.append(g)
        for r in rankings:
            r = dict(r)
            r["school"] = school
            all_rankings.append(r)
        for d in draft:
            d = dict(d)
            d["school"] = school
            all_draft_picks.append(d)
        for t in talent:
            t = dict(t)
            t["school"] = school
            all_talent.append(t)
        for b in betting:
            b = dict(b)
            b["school"] = school
            all_betting.append(b)

        # Stint summary
        years = [g.get("season") for g in games if isinstance(g.get("season"), int)]
        start_year = min(years) if years else None
        end_year = max(years) if years else None
        wins, losses, ties = calculate_record(games, school)
        total_games = wins + losses + ties
        win_pct = round(wins / total_games * 100, 1) if total_games else 0.0

        stints.append(
            {
                "school": school,
                "start_year": start_year,
                "end_year": end_year,
                "record": f"{wins}-{losses}" + (f"-{ties}" if ties else ""),
                "win_pct": win_pct,
                "games": total_games,
                "source_file": str(path),
            }
        )
        schools_seen.append(school)

    # Career totals
    total_wins = total_losses = total_ties = 0
    for stint in stints:
        rec = stint["record"].split("-")
        if len(rec) >= 2:
            total_wins += int(rec[0] or 0)
            total_losses += int(rec[1] or 0)
        if len(rec) == 3:
            total_ties += int(rec[2] or 0)

    career_games = total_wins + total_losses + total_ties
    career_win_pct = round(total_wins / career_games * 100, 1) if career_games else 0.0

    master = {
        "metadata": {
            "generated": datetime.utcnow().isoformat(),
            "coach": coach_name,
            "schools": schools_seen,
            "description": f"Full career profile for {coach_name} merged from {len(profiles)} files",
        },
        "career_summary": {
            "record": f"{total_wins}-{total_losses}" + (f"-{total_ties}" if total_ties else ""),
            "win_pct": career_win_pct,
            "games": career_games,
        },
        "stints": stints,
        "games": all_games,
        "rankings": all_rankings,
        "draft_picks": all_draft_picks,
        "talent_ratings": all_talent,
        "betting_lines": all_betting,
    }
    return master


def main():
    parser = argparse.ArgumentParser(description="Merge single-school coach profiles into a master career file.")
    parser.add_argument("--coach", required=True, help="Coach full name, e.g. 'Matt Campbell'")
    parser.add_argument("--output", required=True, help="Output path for merged master JSON")
    parser.add_argument("files", nargs="+", help="Input JSON files (single-school profiles)")
    args = parser.parse_args()

    input_paths = [Path(f) for f in args.files]
    profiles = load_profiles(input_paths)
    master = merge_profiles(args.coach, profiles)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(master, indent=2))
    print(f"✅ Wrote merged master: {out_path}")
    print(f"   Stints: {len(master['stints'])}, Games: {len(master['games'])}, Rankings: {len(master['rankings'])}")


if __name__ == "__main__":
    main()
