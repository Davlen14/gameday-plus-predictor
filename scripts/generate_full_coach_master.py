#!/usr/bin/env python3
"""
Generate a fresh full-career master profile for a coach across multiple schools.
Fetches games, rankings, draft picks, talent, ratings (SRS, SP+), betting lines,
pre-arrival context, headshots, and computed analytics.

Example (Matt Campbell):
  python scripts/generate_full_coach_master.py \
    --coach "Matt Campbell" \
    --stint "Toledo:2011-2015" \
    --stint "Iowa State:2016-2025" \
    --output enhanced_coaches_v2/matt_campbell_master_fresh.json
    --context-years 3
"""
import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Path to headshots JSON (relative to project root)
HEADSHOTS_PATH = Path(__file__).parent.parent / "power5_coaches_headshots.json"

GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# Conference name to abbreviation/short name mapping
CONFERENCE_MAP = {
    "ACC": {"abbr": "ACC", "shortName": "ACC"},
    "American Athletic": {"abbr": "AAC", "shortName": "American"},
    "Big 12": {"abbr": "B12", "shortName": "Big 12"},
    "Big Ten": {"abbr": "B1G", "shortName": "Big Ten"},
    "Conference USA": {"abbr": "CUSA", "shortName": "C-USA"},
    "FBS Independents": {"abbr": "Ind", "shortName": "FBS Independents"},
    "Mid-American": {"abbr": "MAC", "shortName": "MAC"},
    "Mountain West": {"abbr": "MWC", "shortName": "Mountain West"},
    "Pac-12": {"abbr": "P12", "shortName": "Pac-12"},
    "SEC": {"abbr": "SEC", "shortName": "SEC"},
    "Sun Belt": {"abbr": "SBC", "shortName": "Sun Belt"},
}


def query_gql(q: str, variables: Dict = None) -> Dict:
    """Minimal GraphQL POST using urllib to avoid external deps."""
    import json as _json
    from urllib import request, error

    payload = {"query": q}
    if variables:
        payload["variables"] = variables
    data = _json.dumps(payload).encode("utf-8")
    req = request.Request(
        GRAPHQL_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return _json.loads(body).get("data", {}) or {}
    except error.HTTPError as exc:
        print(f"⚠️  HTTP error: {exc}")
    except Exception as exc:
        print(f"⚠️  Query error: {exc}")
    return {}


def fetch_games(school: str, start_year: int, end_year: int) -> List[Dict]:
    print(f"📅 Games: {school} {start_year}-{end_year}")
    all_games: List[Dict] = []
    for year in range(start_year, end_year + 1):
        q = f'''{{
            game(where: {{
                season: {{_eq: {year}}},
                _or: [
                    {{homeTeam: {{_eq: "{school}"}}}},
                    {{awayTeam: {{_eq: "{school}"}}}}
                ]
            }}, orderBy: {{week: ASC}}) {{
                id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite
                excitement conferenceGame
            }}
        }}'''
        games = query_gql(q).get("game", [])
        all_games.extend(games)
    # Postseason
    q_post = f'''{{
        game(where: {{
            season: {{_gte: {start_year}, _lte: {end_year}}},
            seasonType: {{_eq: "postseason"}},
            _or: [
                {{homeTeam: {{_eq: "{school}"}}}},
                {{awayTeam: {{_eq: "{school}"}}}}
            ]
        }}) {{
            id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite
            excitement conferenceGame
        }}
    }}'''
    post = query_gql(q_post).get("game", [])
    all_games.extend(post)
    print(f"  → {len(all_games)} games")
    return all_games


def fetch_rankings(school: str, start_year: int, end_year: int) -> List[Dict]:
    """Fetch AP + CFP rankings for school during tenure"""
    q = f'''{{
        pollRank(where: {{
            poll: {{
                season: {{_gte: {start_year}, _lte: {end_year}}},
                pollType: {{name: {{_in: ["AP Top 25", "Playoff Committee Rankings"]}}}}
            }},
            team: {{school: {{_eq: "{school}"}}}}
        }}, orderBy: {{poll: {{season: ASC, week: ASC}}}}) {{
            rank
            points
            poll {{ season week pollType {{ name }} }}
            team {{ school }}
        }}
    }}'''
    rankings = query_gql(q).get("pollRank", [])
    print(f"📊 Rankings ({school}): {len(rankings)}")
    return rankings


def fetch_draft_picks(school: str, start_year: int, end_year: int) -> List[Dict]:
    draft_start = start_year + 1
    draft_end = end_year + 1
    q = f'''{{
        draftPicks(where: {{
            collegeTeam: {{school: {{_eq: "{school}"}}}},
            year: {{_gte: {draft_start}, _lte: {draft_end}}}
        }}, orderBy: [{{year: ASC}}, {{overall: ASC}}]) {{
            year round overall name position {{ abbreviation }} draftTeam {{ displayName }} height weight
        }}
    }}'''
    picks = query_gql(q).get("draftPicks", [])
    print(f"🏈 Draft picks ({school}): {len(picks)}")
    return picks


def fetch_talent_ratings(school: str, start_year: int, end_year: int) -> List[Dict]:
    q = f'''{{
        teamTalent(where:{{
            year:{{_gte:{start_year},_lte:{end_year}}},
            team:{{school:{{_eq:"{school}"}}}}
        }}, orderBy:{{year:ASC}}){{
            year
            talent
            team {{ school }}
        }}
    }}'''
    talent = query_gql(q).get("teamTalent", [])
    print(f"⭐ Talent ({school}): {len(talent)}")
    return talent


def fetch_ratings(school: str, start_year: int, end_year: int) -> List[Dict]:
    q = f'''{{
        ratings(where:{{
            team:{{_eq:"{school}"}},
            year:{{_gte:{start_year},_lte:{end_year}}}
        }}) {{
            year
            team
            srs
            spOverall
            spOffense
            spDefense
            spSpecialTeams
            fpi
        }}
    }}'''
    ratings = query_gql(q).get("ratings", [])
    print(f"📈 Ratings ({school}): {len(ratings)}")
    return ratings


def fetch_historical_team_meta(school: str) -> Dict:
    """Fetch team metadata (colors, images, mascot, historical conference)."""
    q = f'''{{
        historicalTeam(where: {{
            school: {{_eq: "{school}"}}
        }}, limit: 1) {{
            school
            conference
            conferenceAbbreviation
            conferenceShortName
            color
            altColor
            mascot
            abbreviation
            images
        }}
    }}'''
    res = query_gql(q).get("historicalTeam", [])
    return res[0] if res else {}


def fetch_current_team_meta(school: str) -> Dict:
    """Fetch current conference info from currentTeams."""
    q = f'''{{
        currentTeams(where: {{
            school: {{_eq: "{school}"}}
        }}, limit: 1) {{
            school
            conference
            conferenceId
            division
            classification
            abbreviation
        }}
    }}'''
    res = query_gql(q).get("currentTeams", [])
    return res[0] if res else {}


def compose_team_meta(school: str) -> Dict:
    """Combine current conference with historical colors/logos."""
    hist = fetch_historical_team_meta(school)
    curr = fetch_current_team_meta(school)
    meta = {"school": school}

    # Get current conference name first
    conference = curr.get("conference") or hist.get("conference")
    meta["conference"] = conference
    
    # Derive conferenceAbbreviation and conferenceShortName from conference name
    conf_info = CONFERENCE_MAP.get(conference, {"abbr": conference, "shortName": conference})
    meta["conferenceAbbreviation"] = conf_info["abbr"]
    meta["conferenceShortName"] = conf_info["shortName"]
    
    # Other conference-related fields from current data
    for key in ["conferenceId", "division", "classification"]:
        if curr.get(key) is not None:
            meta[key] = curr.get(key)
        elif hist.get(key) is not None:
            meta[key] = hist.get(key)

    # Visuals and mascot from historical (logos/colors)
    for key in ["color", "altColor", "mascot", "abbreviation", "images"]:
        if hist.get(key) is not None:
            meta[key] = hist.get(key)
        elif curr.get(key) is not None:
            meta[key] = curr.get(key)

    return meta


def fetch_weather(game_ids: List[int]) -> Dict[int, Dict]:
    """Fetch weather by gameId in chunks."""
    if not game_ids:
        return {}
    out: Dict[int, Dict] = {}
    chunk = 50
    for i in range(0, len(game_ids), chunk):
        ids = game_ids[i : i + chunk]
        id_list = ",".join(str(x) for x in ids)
        q = f'''{{
            gameWeather(where: {{gameId: {{_in: [{id_list}]}}}}) {{
                gameId
                temperature
                humidity
                precipitation
                windSpeed
                windDirection
            }}
        }}'''
        res = query_gql(q).get("gameWeather", [])
        for item in res:
            out[item.get("gameId")] = item
    return out


def fetch_betting_lines(school: str, year: int) -> List[Dict]:
    q = f'''{{
        game(where: {{
            season: {{_eq: {year}}},
            _or: [{{homeTeam: {{_eq: "{school}"}}}}, {{awayTeam: {{_eq: "{school}"}}}}]
        }}, orderBy: {{week: ASC}}) {{
            id season week homeTeam awayTeam homePoints awayPoints lines {{ provider {{ name }} spread overUnder }}
        }}
    }}'''
    games = query_gql(q).get("game", [])
    print(f"💰 Betting lines ({school} {year}): {len(games)}")
    return games


def calc_record(games: List[Dict], school: str) -> Tuple[int, int, int]:
    w = l = t = 0
    for g in games:
        home, away = g.get("homeTeam"), g.get("awayTeam")
        if home is None or away is None or school not in (home, away):
            continue
        hp, ap = g.get("homePoints"), g.get("awayPoints")
        if hp is None or ap is None:
            continue
        team_score = hp if home == school else ap
        opp_score = ap if home == school else hp
        if team_score > opp_score:
            w += 1
        elif team_score < opp_score:
            l += 1
        else:
            t += 1
    return w, l, t


def load_headshots() -> Dict[str, str]:
    """Load headshots JSON and return coach name -> URL mapping."""
    if not HEADSHOTS_PATH.exists():
        print(f"⚠️  Headshots file not found: {HEADSHOTS_PATH}")
        return {}
    try:
        with open(HEADSHOTS_PATH) as f:
            data = json.load(f)
        # Flatten conference-grouped structure
        headshots = {}
        for conf, coaches in data.items():
            for coach in coaches:
                name = coach.get("coach")
                url = coach.get("headshot_url")
                if name and url:
                    headshots[name] = url
        return headshots
    except Exception as e:
        print(f"⚠️  Error loading headshots: {e}")
        return {}


def fetch_pre_arrival_games(school: str, start_year: int, context_years: int) -> List[Dict]:
    """Fetch games from years before coach arrived (for context)."""
    if context_years <= 0:
        return []
    pre_start = start_year - context_years
    pre_end = start_year - 1
    print(f"📜 Pre-arrival ({school} {pre_start}-{pre_end})")
    all_games: List[Dict] = []
    for year in range(pre_start, pre_end + 1):
        q = f'''{{
            game(where: {{
                season: {{_eq: {year}}},
                _or: [
                    {{homeTeam: {{_eq: "{school}"}}}},
                    {{awayTeam: {{_eq: "{school}"}}}}
                ]
            }}, orderBy: {{week: ASC}}) {{
                id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite
                excitement conferenceGame
            }}
        }}'''
        games = query_gql(q).get("game", [])
        all_games.extend(games)
    print(f"  → {len(all_games)} pre-arrival games")
    return all_games


def compute_analytics(games: List[Dict], school: str, betting_games: List[Dict]) -> Dict:
    """Compute advanced analytics from game data."""
    analytics = {
        "home_record": {"wins": 0, "losses": 0, "ties": 0},
        "away_record": {"wins": 0, "losses": 0, "ties": 0},
        "neutral_record": {"wins": 0, "losses": 0, "ties": 0},
        "by_month": {},
        "signature_wins": [],
        "bad_losses": [],
        "ats_record": {"wins": 0, "losses": 0, "pushes": 0, "no_line": 0},
        "over_under_record": {"overs": 0, "unders": 0, "pushes": 0, "no_line": 0},
        "conference_record": {"wins": 0, "losses": 0},
        "bowl_record": {"wins": 0, "losses": 0},
        "vs_ranked": {"wins": 0, "losses": 0},
        "as_ranked": {"wins": 0, "losses": 0},
    }
    
    # Build betting lookup by game id
    betting_lookup = {}
    for bg in betting_games:
        gid = bg.get("id")
        lines = bg.get("lines", [])
        if gid and lines:
            # Use first available line (usually consensus)
            betting_lookup[gid] = lines[0] if lines else {}
    
    # Month mapping from week numbers (approximate)
    def week_to_month(week: int, season_type: str) -> str:
        if season_type == "postseason":
            return "Bowl"
        if week <= 1:
            return "Aug"
        elif week <= 5:
            return "Sep"
        elif week <= 9:
            return "Oct"
        elif week <= 14:
            return "Nov"
        else:
            return "Dec"
    
    for g in games:
        home = g.get("homeTeam")
        away = g.get("awayTeam")
        hp = g.get("homePoints")
        ap = g.get("awayPoints")
        neutral = g.get("neutralSite", False)
        conf_game = g.get("conferenceGame", False)
        season_type = g.get("seasonType", "regular")
        week = g.get("week", 1)
        season = g.get("season")
        gid = g.get("id")
        
        if hp is None or ap is None or school not in (home, away):
            continue
        
        is_home = home == school
        team_score = hp if is_home else ap
        opp_score = ap if is_home else hp
        opponent = away if is_home else home
        
        won = team_score > opp_score
        lost = team_score < opp_score
        
        # Home/Away/Neutral splits
        if neutral:
            if won:
                analytics["neutral_record"]["wins"] += 1
            elif lost:
                analytics["neutral_record"]["losses"] += 1
            else:
                analytics["neutral_record"]["ties"] += 1
        elif is_home:
            if won:
                analytics["home_record"]["wins"] += 1
            elif lost:
                analytics["home_record"]["losses"] += 1
            else:
                analytics["home_record"]["ties"] += 1
        else:
            if won:
                analytics["away_record"]["wins"] += 1
            elif lost:
                analytics["away_record"]["losses"] += 1
            else:
                analytics["away_record"]["ties"] += 1
        
        # By month
        month = week_to_month(week, season_type)
        if month not in analytics["by_month"]:
            analytics["by_month"][month] = {"wins": 0, "losses": 0, "ties": 0}
        if won:
            analytics["by_month"][month]["wins"] += 1
        elif lost:
            analytics["by_month"][month]["losses"] += 1
        else:
            analytics["by_month"][month]["ties"] += 1
        
        # Conference record
        if conf_game:
            if won:
                analytics["conference_record"]["wins"] += 1
            else:
                analytics["conference_record"]["losses"] += 1
        
        # Bowl record
        if season_type == "postseason":
            if won:
                analytics["bowl_record"]["wins"] += 1
            else:
                analytics["bowl_record"]["losses"] += 1
        
        # Signature wins / bad losses (based on opponent SP+)
        opp_sp = g.get("awaySPOverall") if is_home else g.get("homeSPOverall")
        if opp_sp is not None:
            if won and opp_sp >= 15:
                analytics["signature_wins"].append({
                    "season": season,
                    "week": week,
                    "opponent": opponent,
                    "score": f"{team_score}-{opp_score}",
                    "opp_sp": round(opp_sp, 1)
                })
            elif lost and opp_sp <= 0:
                analytics["bad_losses"].append({
                    "season": season,
                    "week": week,
                    "opponent": opponent,
                    "score": f"{team_score}-{opp_score}",
                    "opp_sp": round(opp_sp, 1)
                })
        
        # ATS record
        if gid in betting_lookup:
            line = betting_lookup[gid]
            spread = line.get("spread")
            over_under = line.get("overUnder")
            
            if spread is not None:
                # Spread is from home team perspective
                # If we're home, negative spread means we're favored
                # If we're away, we need to flip
                actual_margin = team_score - opp_score
                if is_home:
                    cover_margin = actual_margin + spread  # spread is typically negative for favorites
                else:
                    cover_margin = actual_margin - spread  # flip for away team
                
                if cover_margin > 0:
                    analytics["ats_record"]["wins"] += 1
                elif cover_margin < 0:
                    analytics["ats_record"]["losses"] += 1
                else:
                    analytics["ats_record"]["pushes"] += 1
            else:
                analytics["ats_record"]["no_line"] += 1
            
            if over_under is not None:
                total_points = hp + ap
                if total_points > over_under:
                    analytics["over_under_record"]["overs"] += 1
                elif total_points < over_under:
                    analytics["over_under_record"]["unders"] += 1
                else:
                    analytics["over_under_record"]["pushes"] += 1
            else:
                analytics["over_under_record"]["no_line"] += 1
        else:
            analytics["ats_record"]["no_line"] += 1
            analytics["over_under_record"]["no_line"] += 1
    
    # Sort signature wins by opponent strength
    analytics["signature_wins"].sort(key=lambda x: x["opp_sp"], reverse=True)
    analytics["bad_losses"].sort(key=lambda x: x["opp_sp"])
    
    return analytics


def build_master(coach: str, stints: List[Tuple[str, int, int]], context_years: int = 3) -> Dict:
    all_games = []
    all_rankings = []
    all_draft = []
    all_talent = []
    all_betting = []
    all_ratings = []
    pre_arrival_data = {}  # school -> {games, record}
    opponent_ratings: Dict[str, List[Dict]] = {}
    team_meta: Dict[str, Dict] = {}
    stint_summaries = []
    
    # Load headshots
    headshots = load_headshots()
    coach_headshot = headshots.get(coach)
    if coach_headshot:
        print(f"📸 Found headshot for {coach}")
    else:
        print(f"⚠️  No headshot found for {coach}")

    for school, start_year, end_year in stints:
        team_meta[school] = compose_team_meta(school)
        games = fetch_games(school, start_year, end_year)
        rankings = fetch_rankings(school, start_year, end_year)
        draft = fetch_draft_picks(school, start_year, end_year)
        talent = fetch_talent_ratings(school, start_year, end_year)
        ratings = fetch_ratings(school, start_year, end_year)
        betting_2025 = fetch_betting_lines(school, 2025) if end_year >= 2025 else []
        
        # Fetch pre-arrival context
        pre_games = fetch_pre_arrival_games(school, start_year, context_years)
        if pre_games:
            pre_w, pre_l, pre_t = calc_record(pre_games, school)
            pre_total = pre_w + pre_l + pre_t
            pre_arrival_data[school] = {
                "years": f"{start_year - context_years}-{start_year - 1}",
                "games": pre_games,
                "record": f"{pre_w}-{pre_l}" + (f"-{pre_t}" if pre_t else ""),
                "win_pct": round(pre_w / pre_total * 100, 1) if pre_total else 0.0,
                "total_games": pre_total,
            }

        for g in games:
            g["school"] = school
        for r in rankings:
            r["school"] = school
        for d in draft:
            d["school"] = school
        for t in talent:
            t["school"] = school
        for rt in ratings:
            rt["school"] = school
        for b in betting_2025:
            b["school"] = school

        all_games.extend(games)
        all_rankings.extend(rankings)
        all_draft.extend(draft)
        all_talent.extend(talent)
        all_ratings.extend(ratings)
        all_betting.extend(betting_2025)

        # Collect opponent list for ratings enrichment
        opponents = set()
        for g in games:
            if g.get("homeTeam") == school:
                opponents.add(g.get("awayTeam"))
            elif g.get("awayTeam") == school:
                opponents.add(g.get("homeTeam"))

        # Fetch opponent ratings once per school list to avoid duplicate calls
        for opp in opponents:
            if not opp:
                continue
            if opp in opponent_ratings:
                continue
            # Use full stint span as a proxy; opponents may have fewer games, but the span is fine
            opp_r = fetch_ratings(opp, start_year, end_year)
            for item in opp_r:
                item["school"] = opp
            opponent_ratings[opp] = opp_r
            if opp not in team_meta:
                team_meta[opp] = compose_team_meta(opp)

        wins, losses, ties = calc_record(games, school)
        total_games = wins + losses + ties
        win_pct = round(wins / total_games * 100, 1) if total_games else 0.0
        stint_summaries.append(
            {
                "school": school,
                "start_year": start_year,
                "end_year": end_year,
                "record": f"{wins}-{losses}" + (f"-{ties}" if ties else ""),
                "win_pct": win_pct,
                "games": total_games,
            }
        )

    total_w = sum(int(s["record"].split("-")[0]) for s in stint_summaries)
    total_l = sum(int(s["record"].split("-")[1]) for s in stint_summaries)
    total_t = sum(int(s["record"].split("-")[2]) for s in stint_summaries if len(s["record"].split("-")) == 3)
    total_games = total_w + total_l + total_t
    career_win_pct = round(total_w / total_games * 100, 1) if total_games else 0.0

    weather_map = fetch_weather([g["id"] for g in all_games if g.get("id")])

    # Build rating lookup keyed by (team, year)
    rating_lookup: Dict[Tuple[str, int], Dict] = {}
    for r in all_ratings:
        team = r.get("team") or r.get("school")
        year = r.get("year")
        if team and year is not None:
            rating_lookup[(team, int(year))] = r
    for opp, vals in opponent_ratings.items():
        for r in vals:
            team = r.get("team") or r.get("school") or opp
            year = r.get("year")
            if team and year is not None:
                rating_lookup[(team, int(year))] = r

    # Enrich games inline with weather, team meta, and season ratings (flattened structure)
    for g in all_games:
        gid = g.get("id")
        if gid in weather_map:
            g["weather"] = weather_map[gid]
        home = g.get("homeTeam")
        away = g.get("awayTeam")
        season = g.get("season")
        
        # Flatten home team meta
        if home and home in team_meta:
            home_meta = team_meta[home]
            g["homeConference"] = home_meta.get("conference")
            g["homeConferenceAbbr"] = home_meta.get("conferenceAbbreviation")
            g["homeConferenceShortName"] = home_meta.get("conferenceShortName")
            g["homeColor"] = home_meta.get("color")
            g["homeAltColor"] = home_meta.get("altColor")
            g["homeMascot"] = home_meta.get("mascot")
            g["homeLogo"] = home_meta.get("images")
            g["homeAbbreviation"] = home_meta.get("abbreviation")
        
        # Flatten away team meta
        if away and away in team_meta:
            away_meta = team_meta[away]
            g["awayConference"] = away_meta.get("conference")
            g["awayConferenceAbbr"] = away_meta.get("conferenceAbbreviation")
            g["awayConferenceShortName"] = away_meta.get("conferenceShortName")
            g["awayColor"] = away_meta.get("color")
            g["awayAltColor"] = away_meta.get("altColor")
            g["awayMascot"] = away_meta.get("mascot")
            g["awayLogo"] = away_meta.get("images")
            g["awayAbbreviation"] = away_meta.get("abbreviation")
        
        # Flatten home team ratings
        if home and season is not None:
            home_rating = rating_lookup.get((home, int(season)))
            if home_rating:
                g["homeSRS"] = home_rating.get("srs")
                g["homeSPOverall"] = home_rating.get("spOverall")
                g["homeSPOffense"] = home_rating.get("spOffense")
                g["homeSPDefense"] = home_rating.get("spDefense")
                g["homeSPSpecialTeams"] = home_rating.get("spSpecialTeams")
                g["homeFPI"] = home_rating.get("fpi")
        
        # Flatten away team ratings
        if away and season is not None:
            away_rating = rating_lookup.get((away, int(season)))
            if away_rating:
                g["awaySRS"] = away_rating.get("srs")
                g["awaySPOverall"] = away_rating.get("spOverall")
                g["awaySPOffense"] = away_rating.get("spOffense")
                g["awaySPDefense"] = away_rating.get("spDefense")
                g["awaySPSpecialTeams"] = away_rating.get("spSpecialTeams")
                g["awayFPI"] = away_rating.get("fpi")

    # Compute analytics for the coach
    print("📊 Computing analytics...")
    
    # Compute per-stint analytics first
    stint_analytics = {}
    for school, start_year, end_year in stints:
        stint_games = [g for g in all_games if g.get("school") == school]
        stint_betting = [b for b in all_betting if b.get("school") == school]
        stint_analytics[school] = compute_analytics(stint_games, school, stint_betting)
    
    # Aggregate analytics across all stints
    combined_analytics = {
        "home_record": {"wins": 0, "losses": 0, "ties": 0},
        "away_record": {"wins": 0, "losses": 0, "ties": 0},
        "neutral_record": {"wins": 0, "losses": 0, "ties": 0},
        "by_month": {},
        "signature_wins": [],
        "bad_losses": [],
        "ats_record": {"wins": 0, "losses": 0, "pushes": 0, "no_line": 0},
        "over_under_record": {"overs": 0, "unders": 0, "pushes": 0, "no_line": 0},
        "conference_record": {"wins": 0, "losses": 0},
        "bowl_record": {"wins": 0, "losses": 0},
    }
    
    for school_analytics in stint_analytics.values():
        for key in ["home_record", "away_record", "neutral_record"]:
            for stat in ["wins", "losses", "ties"]:
                combined_analytics[key][stat] += school_analytics[key][stat]
        for key in ["conference_record", "bowl_record"]:
            combined_analytics[key]["wins"] += school_analytics[key]["wins"]
            combined_analytics[key]["losses"] += school_analytics[key]["losses"]
        for key in ["ats_record"]:
            for stat in ["wins", "losses", "pushes", "no_line"]:
                combined_analytics[key][stat] += school_analytics[key][stat]
        for key in ["over_under_record"]:
            for stat in ["overs", "unders", "pushes", "no_line"]:
                combined_analytics[key][stat] += school_analytics[key][stat]
        # Merge by_month
        for month, stats in school_analytics["by_month"].items():
            if month not in combined_analytics["by_month"]:
                combined_analytics["by_month"][month] = {"wins": 0, "losses": 0, "ties": 0}
            for stat in ["wins", "losses", "ties"]:
                combined_analytics["by_month"][month][stat] += stats[stat]
        # Merge signature wins and bad losses
        combined_analytics["signature_wins"].extend(school_analytics["signature_wins"])
        combined_analytics["bad_losses"].extend(school_analytics["bad_losses"])
    
    # Sort combined lists
    combined_analytics["signature_wins"].sort(key=lambda x: x["opp_sp"], reverse=True)
    combined_analytics["bad_losses"].sort(key=lambda x: x["opp_sp"])

    master = {
        "metadata": {
            "generated": datetime.utcnow().isoformat(),
            "coach": coach,
            "headshot": coach_headshot,
            "schools": [s[0] for s in stints],
            "description": f"Full career profile for {coach} across {len(stints)} stints",
        },
        "career_summary": {
            "record": f"{total_w}-{total_l}" + (f"-{total_t}" if total_t else ""),
            "win_pct": career_win_pct,
            "games": total_games,
        },
        "analytics": combined_analytics,
        "stint_analytics": stint_analytics,
        "pre_arrival": pre_arrival_data,
        "stints": stint_summaries,
        "games": all_games,
        "rankings": all_rankings,
        "draft_picks": all_draft,
        "talent_ratings": all_talent,
        "ratings": all_ratings,
        "opponent_ratings": opponent_ratings,
        "teams": team_meta,
        "betting_lines": all_betting,
    }
    return master


def parse_stint(arg: str) -> Tuple[str, int, int]:
    try:
        school_part, years = arg.split(":", 1)
        start_s, end_s = years.split("-", 1)
        return school_part, int(start_s), int(end_s)
    except Exception:
        raise ValueError(f"Invalid stint format: {arg}. Expected School:YYYY-YYYY")


def main():
    parser = argparse.ArgumentParser(description="Generate a full-career master profile for a coach.")
    parser.add_argument("--coach", required=True, help="Coach full name, e.g. 'Matt Campbell'")
    parser.add_argument("--stint", action="append", required=True, help="Stint spec: School:YYYY-YYYY")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--context-years", type=int, default=3, help="Years of pre-arrival context (default: 3)")
    args = parser.parse_args()

    stints = [parse_stint(s) for s in args.stint]
    master = build_master(args.coach, stints, context_years=args.context_years)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(master, indent=2))
    print(f"✅ Wrote master: {out_path}")
    print(f"   Stints: {len(master['stints'])}, Games: {len(master['games'])}, Rankings: {len(master['rankings'])}")
    if master.get("analytics"):
        sig_wins = len(master["analytics"].get("signature_wins", []))
        ats = master["analytics"].get("ats_record", {})
        print(f"   Signature wins: {sig_wins}, ATS: {ats.get('wins', 0)}-{ats.get('losses', 0)}-{ats.get('pushes', 0)}")


if __name__ == "__main__":
    main()
