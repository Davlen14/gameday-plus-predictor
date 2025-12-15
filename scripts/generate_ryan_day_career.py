#!/usr/bin/env python3
"""
Generate comprehensive coach career timeline JSON
Includes: coaching stints, games, recruiting, draft picks, rankings, events
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

# Connect to database
conn = sqlite3.connect('instance/coaches_master.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get coach_id from command line argument or default to Ryan Day
coach_id = int(sys.argv[1]) if len(sys.argv) > 1 else 82
cursor.execute("SELECT * FROM coaches WHERE id = ?", (coach_id,))
ryan_day_row = cursor.fetchone()

# Build comprehensive career data
ryan_day = dict(ryan_day_row)
career_data = {
    "coach_id": coach_id,
    "name": ryan_day['name'],
    "current_school": ryan_day.get('current_school'),
    "career_record": ryan_day.get('career_record'),
    "career_win_pct": ryan_day.get('career_win_pct'),
    "headshot_url": ryan_day.get('headshot_url'),
    "generated_at": datetime.now().isoformat(),
    "career_timeline": []
}

print(f"🎯 Building comprehensive career data for {career_data['name']}")
print("=" * 80)

# Get all coaching stints
cursor.execute("""
    SELECT s.*, t.id as team_id, t.color, t.alt_color, t.logo_url, t.abbreviation, t.mascot
    FROM stints s
    JOIN teams t ON s.school = t.school
    WHERE s.coach_id = ?
    ORDER BY s.start_year
""", (coach_id,))
stints = [dict(row) for row in cursor.fetchall()]

print(f"\n📋 Processing {len(stints)} Coaching Stints...")

# For each stint, gather all related data
for stint in stints:
    stint_data = {
        "type": "coaching_stint",
        "start_year": stint['start_year'],
        "end_year": stint['end_year'],
        "school": stint['school'],
        "record": stint.get('record'),
        "win_pct": stint.get('win_pct'),
        "games_coached": stint.get('games_coached'),
        "team_id": stint['team_id'],
        "team_info": {
            "abbreviation": stint.get('abbreviation'),
            "mascot": stint.get('mascot'),
            "color": stint.get('color'),
            "alt_color": stint.get('alt_color'),
            "logo": stint.get('logo_url')
        },
        "seasons": [],
        "major_events": []
    }
    
    print(f"\n   {stint['start_year']}-{stint['end_year']}: {stint['school']} - {stint.get('record', 'N/A')}")
    
    # Get games for this stint
    cursor.execute("""
        SELECT *
        FROM games
        WHERE coach_id = ? 
        AND season >= ? 
        AND season <= ?
        ORDER BY season, week
    """, (coach_id, stint['start_year'], stint['end_year']))
    games = [dict(row) for row in cursor.fetchall()]
    
    print(f"      🏈 {len(games)} games")
    
    # Group games by season
    seasons_dict = {}
    for game in games:
        season = game['season']
        if season not in seasons_dict:
            seasons_dict[season] = {
                "season": season,
                "games": [],
                "notable_games": [],
                "record": {"wins": 0, "losses": 0}
            }
        
        is_win = game['result'] == 'W'
        is_postseason = game.get('season_type') == 'postseason'
        
        game_data = {
            "week": game['week'],
            "opponent": game['opponent'],
            "opponent_logo": game.get('opponent_logo'),
            "is_home": bool(game.get('is_home')),
            "is_neutral": bool(game.get('is_neutral')),
            "is_conference": bool(game.get('is_conference')),
            "coach_score": game.get('coach_score'),
            "opponent_score": game.get('opponent_score'),
            "result": game['result'],
            "win": is_win,
            "post_season": is_postseason,
            "opponent_rank": game.get('opponent_rank'),
            "is_signature": bool(game.get('is_signature'))
        }
        
        seasons_dict[season]["games"].append(game_data)
        
        # Update season record
        if is_win:
            seasons_dict[season]["record"]["wins"] += 1
        else:
            seasons_dict[season]["record"]["losses"] += 1
        
        # Identify notable games
        if is_postseason:
            seasons_dict[season]["notable_games"].append({
                "type": "bowl_game",
                "description": f"{'Won' if is_win else 'Lost'} vs {game['opponent']} {game.get('coach_score', 0)}-{game.get('opponent_score', 0)}",
                "week": game['week'],
                "win": is_win
            })
        
        # Check if rivalry game
        rival_keywords = ['Michigan', 'Penn State', 'Michigan State', 'Wisconsin']
        opponent_name = game['opponent']
        if any(rival in opponent_name for rival in rival_keywords):
            if is_win:
                seasons_dict[season]["notable_games"].append({
                    "type": "rivalry_win",
                    "description": f"Defeated {opponent_name} {game.get('coach_score', 0)}-{game.get('opponent_score', 0)}",
                    "week": game['week'],
                    "opponent": opponent_name
                })
    
    stint_data["seasons"] = list(seasons_dict.values())
    
    # Get recruiting classes for this stint
    cursor.execute("""
        SELECT * FROM recruiting_classes
        WHERE coach_id = ? 
        AND year >= ? 
        AND year <= ?
        ORDER BY year
    """, (coach_id, stint['start_year'], stint['end_year']))
    recruiting_classes = [dict(row) for row in cursor.fetchall()]
    
    print(f"      🎓 {len(recruiting_classes)} recruiting classes")
    
    for rc in recruiting_classes:
        stint_data["major_events"].append({
            "type": "recruiting_class",
            "year": rc['year'],
            "rank": rc.get('rank'),
            "points": rc.get('points'),
            "description": f"#{rc.get('rank', 'N/A')} Recruiting Class ({rc.get('points', 0)} pts)"
        })
    
    # Get draft picks for this stint
    cursor.execute("""
        SELECT *
        FROM draft_picks
        WHERE coach_id = ?
        AND year >= ?
        AND year <= ?
        ORDER BY year, round, pick
    """, (coach_id, stint['start_year'], stint['end_year'] + 3))
    draft_picks = [dict(row) for row in cursor.fetchall()]
    
    print(f"      🏆 {len(draft_picks)} NFL draft picks")
    
    # Group draft picks by year
    draft_by_year = {}
    for pick in draft_picks:
        year = pick['year']
        if year not in draft_by_year:
            draft_by_year[year] = []
        draft_by_year[year].append({
            "player": pick['player_name'],
            "position": pick.get('position'),
            "round": pick['round'],
            "pick": pick.get('pick'),
            "team": pick['nfl_team']
        })
    
    for year, picks in draft_by_year.items():
        first_rounders = [p for p in picks if p['round'] == 1]
        if first_rounders:
            stint_data["major_events"].append({
                "type": "first_round_picks",
                "year": year,
                "count": len(first_rounders),
                "players": first_rounders,
                "description": f"{len(first_rounders)} First Round Pick{'s' if len(first_rounders) > 1 else ''}"
            })
    
    # Get AP Poll rankings for this stint
    cursor.execute("""
        SELECT * FROM rankings
        WHERE coach_id = ?
        AND season >= ?
        AND season <= ?
        ORDER BY season, week
    """, (coach_id, stint['start_year'], stint['end_year']))
    rankings = [dict(row) for row in cursor.fetchall()]
    
    print(f"      📈 {len(rankings)} AP Poll weeks")
    
    # Find highest rankings per season
    rank_by_season = {}
    for rank in rankings:
        season = rank['season']
        poll_rank = rank.get('rank', 999)
        if season not in rank_by_season or poll_rank < rank_by_season[season]:
            rank_by_season[season] = poll_rank
    
    for season, best_rank in rank_by_season.items():
        if best_rank <= 5:
            stint_data["major_events"].append({
                "type": "top_5_ranking",
                "season": season,
                "rank": best_rank,
                "description": f"Reached #{best_rank} in AP Poll"
            })
    
    # Get talent composite for this stint
    cursor.execute("""
        SELECT * FROM talent_composite
        WHERE coach_id = ?
        AND year >= ?
        AND year <= ?
        ORDER BY year
    """, (coach_id, stint['start_year'], stint['end_year']))
    talent_data = [dict(row) for row in cursor.fetchall()]
    
    print(f"      ⭐ {len(talent_data)} talent rankings")
    
    for talent in talent_data:
        if talent.get('rank') and talent['rank'] <= 5:
            stint_data["major_events"].append({
                "type": "top_talent",
                "year": talent['year'],
                "rank": talent['rank'],
                "talent": talent.get('talent'),
                "description": f"#{talent['rank']} Talent Composite"
            })
    
    # Get transfer portal data
    cursor.execute("""
        SELECT * FROM transfer_portal
        WHERE coach_id = ?
        AND season >= ?
        AND season <= ?
        ORDER BY season
    """, (coach_id, stint['start_year'], stint['end_year']))
    portal_data = [dict(row) for row in cursor.fetchall()]
    
    print(f"      🔄 {len(portal_data)} transfer portal records")
    
    # Sort major events by year
    stint_data["major_events"].sort(key=lambda x: x.get('year', x.get('season', 0)))
    
    career_data["career_timeline"].append(stint_data)

conn.close()

# Save to JSON file
coach_name_slug = career_data['name'].lower().replace(' ', '_')
output_file = Path(f'frontend/src/data/{coach_name_slug}_career.json')
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(career_data, f, indent=2)

print(f"\n{'=' * 80}")
print(f"✅ Created comprehensive career file: {output_file}")
print(f"👤 Coach: {career_data['name']} (ID: {coach_id})")
print(f"📊 Total Coaching Stints: {len(career_data['career_timeline'])}")
print(f"🎯 Total Events Tracked: {sum(len(stint['major_events']) for stint in career_data['career_timeline'])}")
print(f"🏈 Total Seasons: {sum(len(stint['seasons']) for stint in career_data['career_timeline'])}")
print(f"📁 File size: {output_file.stat().st_size / 1024:.1f} KB")
