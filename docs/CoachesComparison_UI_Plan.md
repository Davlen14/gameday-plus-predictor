# CoachesComparison UI Breakdown (UltraDashboard mock → live data plan)

Use this checklist to implement the modern UI without mock data. Follow the order below to keep changes safe and incremental.

## 0) Inputs & data contracts
- API: `GET /api/coaches/comparison?home_team=<>&away_team=<>` returning `{ coach1, coach2, comparative_analysis, hypothetical_matchup }`.
- Coach shape (live): `profile`, `career_summary`, `season_2025_detail`, `schedule?`, `situational_by_school`, `coaching_archetype_analysis`, `recruiting_classes`, `talent_composite`, `transfer_portal`, `advanced_performance_metrics`.
- Trend data: prefer `coach.schedule` if present; fallback to `season_2025_detail.schedule` with fields `{week,res/score,opponent,point_differential}`.

## 1) Core shell
- Keep existing fetch/useEffect/early returns (no mock DATA in code).
- Header: COACHWAR.ROOM, Target Alpha/Beta labels from `profile`.
- Tabs: `overview`, `career`, `season2025`, `archetype`, `recruiting`, `performance`, `matchup`.

## 2) Overview tab
- Two profile panels:
  - Headshot, record, win%, seasons, total games.
  - Scoring trajectory chart using schedule (pf/pa/diff by week).
- Situational radar:
  - Build from `situational_by_school[0]` or career_summary: vs_ranked, home, away, one_score, blowouts.
- Philosophy clash:
  - Use `comparative_analysis.philosophy_clash` if present; otherwise omit/empty state.

## 3) Career tab
- Stints list: school, years, record, win%.
- Situational stats by school: vs ranked/top10/home/away/one-score/blowouts.
- (Optional) Timeline chart of win% per season using `seasons` data.

## 4) Season 2025 tab
- Season readouts: record, PPG/PAPG, SP+ overall/off/def, FPI, YPP, 3rd/4th down.
- Key players: from `season_2025_detail.key_players_2025`.
- Trend chart: season 2025 schedule if available.

## 5) Archetype tab
- For each coach, pick the archetype entry from `coaching_archetype_analysis` keyed by coach+school.
- Show offensive_identity, defensive_philosophy, game_management, archetype_summary.
- NIL strategy readout: totals, players, avg per player.
- NIL pies: build from `nil_strategy.allocation_by_position` (no mock colors).

## 6) Recruiting tab
- Recruiting classes: year, class_rank (top ~5).
- Talent composite: year, talent_rating (top ~5).
- Transfer portal: season, in/out, net, avg ratings.

## 7) Performance tab
- Advanced performance: `advanced_performance_metrics` → signature_wins (top 3), clutch_performance_metrics (close_game_wins, close_games).

## 8) Matchup tab
- Use `hypothetical_matchup.prediction_framework`:
  - Advantages (home/away keys, not hardcoded to teams).
  - Scenarios list (name/prob/desc/score).
  - Final prediction: winner, confidence, reasoning, upset path.
  - Head-to-head notice if `head_to_head_never_met`.
- Efficiency scatter: plot SP+ offense/defense from `season_2025_detail` for both coaches.

## 9) Styling checklist
- TechPanel, DataReadout, ComparisonRow kept; ensure no duplicate exports/components.
- Remove unused imports; keep charts actually used.
- Defensive null checks on every optional field; show lightweight empty states.
- Avoid hardcoded labels like OMS-25/ILL-25; derive from current schools.

## 10) Regression guardrails
- Preserve fetch/404 hide behavior and loading UI.
- No mock/static DATA objects in final code.
- No conditional hooks; all hooks at top-level.
- Keep tabs wired to real content (no placeholder “DATA MODULE” screens).
