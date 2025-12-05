#!/usr/bin/env python3
"""Ryan Day Complete Profile - Comprehensive Analysis with Advanced Metrics"""
import json, requests
from collections import defaultdict
from datetime import datetime

GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

def query_gql(q):
    """Execute GraphQL query with error handling"""
    try:
        r = requests.post(GRAPHQL_URL, json={'query': q}, headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'})
        return r.json().get('data', {})
    except Exception as e:
        print(f"  ⚠️  Query error: {e}")
        return {}

print("🏈 Ryan Day Complete Profile Generator - Enhanced Edition")
print("=" * 70)

# ============================================================================
# SECTION 1: Fetch 2018 Acting HC Games (Weeks 1-3)
# ============================================================================
print("\n📅 Fetching 2018 Acting HC games (Weeks 1-3)...")
q_2018 = '''{ game(where: {season: {_eq: 2018}, seasonType: {_eq: "regular"}, week: {_lte: 3}, _or: [{homeTeam: {_eq: "Ohio State"}}, {awayTeam: {_eq: "Ohio State"}}]}, orderBy: {week: ASC}) { 
  id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite 
} }'''
games_2018 = query_gql(q_2018).get('game', [])
print(f"  ✓ 2018 Acting HC: {len(games_2018)} games")

# ============================================================================
# SECTION 2: Fetch All Regular Season Games 2019-2025
# ============================================================================
print("\n📅 Fetching regular season games (2019-2025)...")
all_games = []
for year in range(2019, 2026):
    q = f'''{{ game(where: {{season: {{_eq: {year}}}, seasonType: {{_eq: "regular"}}, _or: [{{homeTeam: {{_eq: "Ohio State"}}}}, {{awayTeam: {{_eq: "Ohio State"}}}}]}}, orderBy: {{week: ASC}}) {{ 
      id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite 
    }} }}'''
    games = query_gql(q).get('game', [])
    all_games.extend(games)
    print(f"  ✓ {year}: {len(games)} games")

# ============================================================================
# SECTION 3: Fetch Postseason Games (Bowls + CFP)
# ============================================================================
print("\n📅 Fetching postseason games (2019-2025)...")
q_postseason = '''{ game(where: {season: {_gte: 2019}, seasonType: {_eq: "postseason"}, _or: [{homeTeam: {_eq: "Ohio State"}}, {awayTeam: {_eq: "Ohio State"}}]}, orderBy: {season: ASC}) { 
  id season week seasonType homeTeam awayTeam homePoints awayPoints neutralSite 
} }'''
games_postseason = query_gql(q_postseason).get('game', [])
print(f"  ✓ Postseason: {len(games_postseason)} games")

# Combine all games
all_games_combined = games_2018 + all_games + games_postseason
print(f"\n📊 Total games fetched: {len(all_games_combined)}")

# ============================================================================
# SECTION 4: Fetch Ohio State Rankings (2018-2025)
# ============================================================================
print("\n📊 Fetching Ohio State AP Rankings (2018-2025)...")
q_rankings = '''{ pollRank(where: {poll: {season: {_gte: 2018}, pollType: {name: {_eq: "AP Top 25"}}}, team: {school: {_eq: "Ohio State"}}}, orderBy: {poll: {season: ASC, week: ASC}}) { 
  rank points poll { season week } team { school } 
} }'''
osu_rankings = query_gql(q_rankings).get('pollRank', [])
print(f"  ✓ Total weeks ranked: {len(osu_rankings)}")

# ============================================================================
# SECTION 5: Fetch Betting Lines for 2025 (for ATS calculation)
# ============================================================================
print("\n💰 Fetching betting lines (2025)...")
q_lines = '''{ game(where: {season: {_eq: 2025}, seasonType: {_eq: "regular"}, _or: [{homeTeam: {_eq: "Ohio State"}}, {awayTeam: {_eq: "Ohio State"}}]}, orderBy: {week: ASC}) { 
  id season week homeTeam awayTeam homePoints awayPoints 
  lines { provider { name } spread overUnder } 
} }'''
games_with_lines = query_gql(q_lines).get('game', [])
print(f"  ✓ Games with betting lines: {len(games_with_lines)}")

# ============================================================================
# SECTION 6: Fetch NFL Draft Picks (2019-2025)
# ============================================================================
print("\n🏈 Fetching NFL Draft Picks (2019-2025)...")
q_draft = '''{ draftPicks(where: {collegeTeam: {school: {_eq: "Ohio State"}}, year: {_gte: 2019}}, orderBy: [{year: ASC}, {overall: ASC}]) { 
  year round overall name position { abbreviation } draftTeam { displayName } height weight 
} }'''
draft_picks = query_gql(q_draft).get('draftPicks', [])
print(f"  ✓ Total draft picks: {len(draft_picks)}")

# ============================================================================
# SECTION 7: Fetch Opponent Rankings (for all games)
# ============================================================================
print("\n🎯 Fetching opponent rankings (this may take a moment)...")
opponent_rankings = {}
games_to_check = all_games + games_postseason  # Skip 2018 for now

for game in games_to_check:
    opponent = game['awayTeam'] if game['homeTeam'] == 'Ohio State' else game['homeTeam']
    season = game['season']
    week = game['week']
    season_type = game.get('seasonType', 'regular')
    
    # For postseason games, use CFP Committee Rankings; for regular season use AP Poll
    poll_type = "Playoff Committee Rankings" if season_type == 'postseason' else "AP Top 25"
    
    # For postseason games, use final rankings (week 15) instead of game week
    ranking_week = 15 if season_type == 'postseason' else week
    
    # Query this opponent's rank in that specific week
    q_opp = f'''{{ pollRank(where: {{poll: {{season: {{_eq: {season}}}, week: {{_eq: {ranking_week}}}, pollType: {{name: {{_eq: "{poll_type}"}}}}}}, team: {{school: {{_eq: "{opponent}"}}}}}}) {{
        rank team {{ school conference }}
    }} }}'''
    
    result = query_gql(q_opp).get('pollRank', [])
    if result:
        key = f"{season}-W{week}-{opponent}"
        opponent_rankings[key] = result[0]

print(f"  ✓ Found {len(opponent_rankings)} ranked opponents")# ============================================================================
# NEW SECTION 6A: Fetch Coach Season Records (Year-by-Year)
# ============================================================================
print("\n📅 Fetching coach season records...")
q_coach_seasons = '''{ coachSeason(where: {coach: {firstName: {_eq: "Ryan"}, lastName: {_eq: "Day"}}}, orderBy: {year: ASC}) { 
  year wins losses ties games 
  preseasonRank postseasonRank 
  team { school conference } 
} }'''
coach_seasons = query_gql(q_coach_seasons).get('coachSeason', [])
print(f"  ✓ Coach seasons: {len(coach_seasons)} years")

# ============================================================================
# NEW SECTION 6B: Fetch Talent Composite Ratings
# ============================================================================
print("\n🎓 Fetching talent composite ratings...")
q_talent = '''{ teamTalent(where: {team: {school: {_eq: "Ohio State"}}, year: {_gte: 2018}}, orderBy: {year: ASC}) { 
  year talent 
  team { school conference } 
} }'''
talent_data = query_gql(q_talent).get('teamTalent', [])
print(f"  ✓ Talent data: {len(talent_data)} years")

# ============================================================================
# ============================================================================
# SECTION 7: Calculate All Stats (EXISTING CODE - keeping as is)
# ============================================================================
print("\n🔢 Calculating comprehensive statistics...")

# Basic stats
total_w = total_l = 0
acting_hc_w = acting_hc_l = 0
regular_w = regular_l = 0
postseason_w = postseason_l = 0
y2025_w = y2025_l = 0
home_w = home_l = away_w = away_l = neut_w = neut_l = 0
blow_w = close_w = close_l = 0
margins = []
recent = []

# vs Ranked stats
vs_ranked_w = vs_ranked_l = 0
vs_top5_w = vs_top5_l = 0
vs_top10_w = vs_top10_l = 0
vs_ranked_by_conf = defaultdict(lambda: {'w': 0, 'l': 0})

# Rivalry stats
rivalries = defaultdict(lambda: {'w': 0, 'l': 0, 'games': []})

# Process 2018 Acting HC games
for g in games_2018:
    if g['homePoints'] is None or g['awayPoints'] is None:
        continue  # Skip games not yet played
    
    is_home = g['homeTeam'] == 'Ohio State'
    osu_pts = g['homePoints'] if is_home else g['awayPoints']
    opp_pts = g['awayPoints'] if is_home else g['homePoints']
    margin = osu_pts - opp_pts
    
    if osu_pts > opp_pts:
        acting_hc_w += 1
        total_w += 1
    else:
        acting_hc_l += 1
        total_l += 1

# Process all other games
for g in all_games_combined[len(games_2018):]:
    if g['homePoints'] is None or g['awayPoints'] is None:
        continue  # Skip games not yet played
    
    is_home = g['homeTeam'] == 'Ohio State'
    osu_pts = g['homePoints'] if is_home else g['awayPoints']
    opp_pts = g['awayPoints'] if is_home else g['homePoints']
    opponent = g['awayTeam'] if is_home else g['homeTeam']
    margin = osu_pts - opp_pts
    
    # Win/Loss
    won = osu_pts > opp_pts
    if won:
        total_w += 1
    else:
        total_l += 1
    
    # Regular vs Postseason
    if g['seasonType'] == 'postseason':
        if won: postseason_w += 1
        else: postseason_l += 1
    else:
        if won: regular_w += 1
        else: regular_l += 1
    
    # 2025 season
    if g['season'] == 2025:
        if won: y2025_w += 1
        else: y2025_l += 1
    
    # Home/Away/Neutral
    if g.get('neutralSite'):
        if won: neut_w += 1
        else: neut_l += 1
    elif is_home:
        if won: home_w += 1
        else: home_l += 1
    else:
        if won: away_w += 1
        else: away_l += 1
    
    # Margin categories
    if won and margin >= 20:
        blow_w += 1
    if abs(margin) <= 7:
        if won: close_w += 1
        else: close_l += 1
    
    margins.append(margin)
    recent.append(won)
    
    # vs Ranked opponents
    key = f"{g['season']}-W{g['week']}-{opponent}"
    if key in opponent_rankings:
        opp_rank = opponent_rankings[key]['rank']
        opp_conf = opponent_rankings[key]['team']['conference']
        
        if won:
            vs_ranked_w += 1
            vs_ranked_by_conf[opp_conf]['w'] += 1
        else:
            vs_ranked_l += 1
            vs_ranked_by_conf[opp_conf]['l'] += 1
        
        if opp_rank <= 5:
            if won: vs_top5_w += 1
            else: vs_top5_l += 1
        if opp_rank <= 10:
            if won: vs_top10_w += 1
            else: vs_top10_l += 1
    
    # Rivalry tracking
    if opponent in ['Michigan', 'Penn State', 'Michigan State', 'Wisconsin']:
        if won:
            rivalries[opponent]['w'] += 1
        else:
            rivalries[opponent]['l'] += 1
        rivalries[opponent]['games'].append({'season': g['season'], 'score': f"{osu_pts}-{opp_pts}"})

# ============================================================================
# NEW SECTION 7A: Enhanced Game Metadata & Monthly/Phase Analysis
# ============================================================================
print("\n📊 Analyzing game patterns and trends...")

# Monthly performance
monthly_stats = defaultdict(lambda: {'w': 0, 'l': 0, 'margins': []})
phase_stats = {'Early': {'w': 0, 'l': 0, 'margins': []}, 
               'Mid': {'w': 0, 'l': 0, 'margins': []}, 
               'Late': {'w': 0, 'l': 0, 'margins': []}}
conf_vs_nonconf = {'conference': {'w': 0, 'l': 0, 'margins': []}, 
                   'non_conference': {'w': 0, 'l': 0, 'margins': []}}

# Enhanced game-by-game data
enhanced_games = []
prev_game_date = None
win_streak = 0
loss_streak = 0
max_win_streak = 0
max_loss_streak = 0
current_win_streak = 0
post_loss_record = {'w': 0, 'l': 0}
last_result_was_loss = False

# Rolling metrics
rolling_window = []

for g in all_games_combined:
    if g['homePoints'] is None or g['awayPoints'] is None:
        continue
    
    is_home = g['homeTeam'] == 'Ohio State'
    osu_pts = g['homePoints'] if is_home else g['awayPoints']
    opp_pts = g['awayPoints'] if is_home else g['homePoints']
    opponent = g['awayTeam'] if is_home else g['homeTeam']
    margin = osu_pts - opp_pts
    won = osu_pts > opp_pts
    
    # Month extraction (approximate from week number)
    week = g.get('week', 0)
    if week <= 4:
        month = 'September'
    elif week <= 8:
        month = 'October'
    elif week <= 13:
        month = 'November'
    else:
        month = 'December'
    
    # Season phase
    if week <= 4:
        phase = 'Early'
    elif week <= 9:
        phase = 'Mid'
    else:
        phase = 'Late'
    
    # Conference determination (simplified - Big Ten opponents)
    big_ten_teams = ['Michigan', 'Penn State', 'Michigan State', 'Wisconsin', 
                     'Iowa', 'Nebraska', 'Minnesota', 'Illinois', 'Northwestern',
                     'Purdue', 'Indiana', 'Maryland', 'Rutgers']
    is_conference = opponent in big_ten_teams
    
    # Update monthly stats
    if won:
        monthly_stats[month]['w'] += 1
    else:
        monthly_stats[month]['l'] += 1
    monthly_stats[month]['margins'].append(margin)
    
    # Update phase stats
    if won:
        phase_stats[phase]['w'] += 1
    else:
        phase_stats[phase]['l'] += 1
    phase_stats[phase]['margins'].append(margin)
    
    # Conference vs non-conference
    conf_key = 'conference' if is_conference else 'non_conference'
    if won:
        conf_vs_nonconf[conf_key]['w'] += 1
    else:
        conf_vs_nonconf[conf_key]['l'] += 1
    conf_vs_nonconf[conf_key]['margins'].append(margin)
    
    # Streak tracking
    if won:
        current_win_streak += 1
        max_win_streak = max(max_win_streak, current_win_streak)
        loss_streak = 0
    else:
        loss_streak += 1
        max_loss_streak = max(max_loss_streak, loss_streak)
        current_win_streak = 0
    
    # Post-loss bounce
    if last_result_was_loss:
        if won:
            post_loss_record['w'] += 1
        else:
            post_loss_record['l'] += 1
    last_result_was_loss = not won
    
    # Rolling metrics (last 5 games)
    rolling_window.append({'won': won, 'margin': margin})
    if len(rolling_window) > 5:
        rolling_window.pop(0)
    
    rolling_wins = sum(1 for g in rolling_window if g['won'])
    rolling_win_pct = rolling_wins / len(rolling_window) if rolling_window else 0
    rolling_avg_margin = sum(g['margin'] for g in rolling_window) / len(rolling_window) if rolling_window else 0
    
    # Get opponent rank
    key = f"{g['season']}-W{g['week']}-{opponent}"
    opp_rank = opponent_rankings[key]['rank'] if key in opponent_rankings else None
    
    # Enhanced game data
    enhanced_game = {
        'season': g['season'],
        'week': g['week'],
        'opponent': opponent,
        'score': f"{osu_pts}-{opp_pts}",
        'result': 'W' if won else 'L',
        'margin': margin,
        'location': 'Neutral' if g.get('neutralSite') else ('Home' if is_home else 'Away'),
        'month': month,
        'phase': phase,
        'is_conference': is_conference,
        'opponent_ranked': opp_rank is not None,
        'opponent_rank': opp_rank,
        'rolling_win_pct': round(rolling_win_pct * 100, 1),
        'rolling_avg_margin': round(rolling_avg_margin, 1),
        'current_win_streak': current_win_streak,
        'season_type': g.get('seasonType', 'regular')
    }
    enhanced_games.append(enhanced_game)

# ============================================================================
# NEW SECTION 7B: Clutch Performance Analysis
# ============================================================================
print("\n🔥 Analyzing clutch performance...")

one_score_w = one_score_l = 0
overtime_w = overtime_l = 0
comeback_wins = 0

for g in all_games_combined:
    if g['homePoints'] is None or g['awayPoints'] is None:
        continue
    
    is_home = g['homeTeam'] == 'Ohio State'
    osu_pts = g['homePoints'] if is_home else g['awayPoints']
    opp_pts = g['awayPoints'] if is_home else g['homePoints']
    margin = abs(osu_pts - opp_pts)
    won = osu_pts > opp_pts
    
    # One-score games (≤8 points)
    if margin <= 8:
        if won:
            one_score_w += 1
        else:
            one_score_l += 1

# ============================================================================
# SECTION 8: Calculate ATS (Against the Spread) for 2025 (EXISTING - keeping as is)
# ============================================================================
ats_w = ats_l = ats_push = 0
ats_details = []

for g in games_with_lines:
    if g['homePoints'] is None or g['awayPoints'] is None:
        continue  # Skip games not yet played
    if not g['lines']:
        continue
    
    is_home = g['homeTeam'] == 'Ohio State'
    osu_pts = g['homePoints'] if is_home else g['awayPoints']
    opp_pts = g['awayPoints'] if is_home else g['homePoints']
    margin = osu_pts - opp_pts
    
    # Calculate consensus spread (average of all providers)
    spreads = [line['spread'] for line in g['lines'] if line['spread'] is not None]
    if not spreads:
        continue
    
    consensus_spread = sum(spreads) / len(spreads)
    
    # For home games, spread is already in OSU's perspective
    # For away games, flip the spread
    if not is_home:
        consensus_spread = -consensus_spread
    
    # ATS logic: Did OSU cover the spread?
    ats_margin = margin + consensus_spread  # positive = covered
    
    if abs(ats_margin) < 0.5:
        ats_push += 1
        ats_result = "PUSH"
    elif ats_margin > 0:
        ats_w += 1
        ats_result = "✅ COVERED"
    else:
        ats_l += 1
        ats_result = "❌ MISSED"
    
    ats_details.append({
        'week': g['week'],
        'opponent': g['awayTeam'] if is_home else g['homeTeam'],
        'score': f"{osu_pts}-{opp_pts}",
        'margin': margin,
        'spread': consensus_spread,
        'ats_margin': ats_margin,
        'result': ats_result
    })

# ============================================================================
# SECTION 9: Calculate Team Ranking Stats
# ============================================================================
if osu_rankings:
    ranks = [r['rank'] for r in osu_rankings]
    avg_rank = sum(ranks) / len(ranks)
    lowest_rank = max(ranks)
    weeks_top5 = len([r for r in ranks if r <= 5])
    weeks_top10 = len([r for r in ranks if r <= 10])
    weeks_top25 = len(ranks)
    
    # Find longest Top 5 streak
    max_streak = 0
    current_streak = 0
    for r in ranks:
        if r <= 5:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    # Find the week/year of lowest rank
    lowest_rank_entry = max(osu_rankings, key=lambda x: x['rank'])
    lowest_rank_week = lowest_rank_entry['poll']['week']
    lowest_rank_season = lowest_rank_entry['poll']['season']

# ============================================================================
# NEW SECTION 9A: Year-by-Year Performance Analysis
# ============================================================================
print("\n📈 Calculating year-by-year trends...")

yearly_records = []
prev_win_pct = None

# Process coach seasons if available
if coach_seasons:
    for cs in coach_seasons:
        w = cs.get('wins', 0)
        l = cs.get('losses', 0)
        total = w + l
        win_pct = (w / total * 100) if total > 0 else 0
        trend = (win_pct - prev_win_pct) if prev_win_pct is not None else None
        
        yearly_records.append({
            'year': cs['year'],
            'wins': w,
            'losses': l,
            'ties': cs.get('ties', 0),
            'games': cs.get('games', total),
            'win_pct': round(win_pct, 1),
            'trend': round(trend, 1) if trend is not None else None,
            'preseason_rank': cs.get('preseasonRank'),
            'postseason_rank': cs.get('postseasonRank'),
            'conference': cs['team']['conference'] if 'team' in cs else 'Big Ten'
        })
        prev_win_pct = win_pct
else:
    # Reconstruct from game data
    games_by_year = defaultdict(lambda: {'w': 0, 'l': 0})
    for g in all_games_combined:
        if g['homePoints'] is None or g['awayPoints'] is None:
            continue
        is_home = g['homeTeam'] == 'Ohio State'
        osu_pts = g['homePoints'] if is_home else g['awayPoints']
        opp_pts = g['awayPoints'] if is_home else g['homePoints']
        won = osu_pts > opp_pts
        
        if won:
            games_by_year[g['season']]['w'] += 1
        else:
            games_by_year[g['season']]['l'] += 1
    
    for year in sorted(games_by_year.keys()):
        w = games_by_year[year]['w']
        l = games_by_year[year]['l']
        total = w + l
        win_pct = (w / total * 100) if total > 0 else 0
        trend = (win_pct - prev_win_pct) if prev_win_pct is not None else None
        
        yearly_records.append({
            'year': year,
            'wins': w,
            'losses': l,
            'ties': 0,
            'games': total,
            'win_pct': round(win_pct, 1),
            'trend': round(trend, 1) if trend is not None else None,
            'preseason_rank': None,
            'postseason_rank': None,
            'conference': 'Big Ten'
        })
        prev_win_pct = win_pct

# ============================================================================
# NEW SECTION 9B: Talent Composite Analysis
# ============================================================================
print("\n🎓 Analyzing talent composite data...")

talent_analysis = []
if talent_data:
    for i, td in enumerate(talent_data):
        talent_rating = td.get('talent', 0)
        year = td['year']
        
        # Calculate trend from previous year
        trend_from_prev = None
        if i > 0:
            prev_talent = talent_data[i-1].get('talent', 0)
            if prev_talent > 0:
                trend_from_prev = round(talent_rating - prev_talent, 1)
        
        talent_analysis.append({
            'year': year,
            'talent_rating': round(talent_rating, 1) if talent_rating else None,
            'trend_from_prev_year': trend_from_prev,
            'team': td['team']['school']
        })
    
    # Calculate averages
    avg_talent = sum(td.get('talent', 0) for td in talent_data) / len(talent_data)
else:
    avg_talent = None

# ============================================================================
# NEW SECTION 9C: NFL Draft Analysis
# ============================================================================
print("\n🏈 Analyzing NFL Draft success...")

draft_analysis = {
    'total_picks': len(draft_picks),
    'by_year': defaultdict(int),
    'by_round': defaultdict(int),
    'by_position': defaultdict(int),
    'first_round_picks': 0,
    'top_10_picks': 0,
    'picks_detail': []
}

for pick in draft_picks:
    year = pick.get('year')
    round_num = pick.get('round')
    overall = pick.get('overall')
    position = pick.get('position', {}).get('abbreviation', 'Unknown') if isinstance(pick.get('position'), dict) else pick.get('position', 'Unknown')
    
    draft_analysis['by_year'][year] += 1
    draft_analysis['by_round'][round_num] += 1
    draft_analysis['by_position'][position] += 1
    
    if round_num == 1:
        draft_analysis['first_round_picks'] += 1
    if overall and overall <= 10:
        draft_analysis['top_10_picks'] += 1
    
    draft_analysis['picks_detail'].append({
        'year': year,
        'round': round_num,
        'pick': pick.get('pick'),
        'overall': overall,
        'name': pick.get('name', 'Unknown'),
        'position': position,
        'nfl_team': pick.get('nflTeam', 'Unknown')
    })

# Calculate average draft position
valid_picks = [p['overall'] for p in draft_analysis['picks_detail'] if p['overall']]
avg_draft_pos = sum(valid_picks) / len(valid_picks) if valid_picks else None

# Picks per year
years_with_picks = len(draft_analysis['by_year'])
picks_per_year = draft_analysis['total_picks'] / years_with_picks if years_with_picks > 0 else 0

# ============================================================================
# NEW SECTION 9D: Regression Pattern Analysis
# ============================================================================
print("\n🔍 Analyzing regression patterns...")

regression_analysis = {
    'monthly_performance': {},
    'phase_performance': {},
    'conference_splits': {},
    'post_loss_bounce': {},
    'streaks': {
        'longest_win_streak': max_win_streak,
        'longest_loss_streak': max_loss_streak
    },
    'clutch_performance': {
        'one_score_games': f"{one_score_w}-{one_score_l}",
        'one_score_win_pct': round(one_score_w / (one_score_w + one_score_l) * 100, 1) if one_score_w + one_score_l > 0 else 0
    }
}

# Monthly performance
for month, stats in monthly_stats.items():
    total = stats['w'] + stats['l']
    win_pct = (stats['w'] / total * 100) if total > 0 else 0
    avg_margin = sum(stats['margins']) / len(stats['margins']) if stats['margins'] else 0
    
    regression_analysis['monthly_performance'][month] = {
        'record': f"{stats['w']}-{stats['l']}",
        'win_pct': round(win_pct, 1),
        'avg_margin': round(avg_margin, 1),
        'games': total
    }

# Phase performance
for phase, stats in phase_stats.items():
    total = stats['w'] + stats['l']
    win_pct = (stats['w'] / total * 100) if total > 0 else 0
    avg_margin = sum(stats['margins']) / len(stats['margins']) if stats['margins'] else 0
    
    regression_analysis['phase_performance'][phase] = {
        'record': f"{stats['w']}-{stats['l']}",
        'win_pct': round(win_pct, 1),
        'avg_margin': round(avg_margin, 1),
        'games': total,
        'red_flag': win_pct < 80 and phase == 'Late'
    }

# Conference splits
for conf_type, stats in conf_vs_nonconf.items():
    total = stats['w'] + stats['l']
    win_pct = (stats['w'] / total * 100) if total > 0 else 0
    avg_margin = sum(stats['margins']) / len(stats['margins']) if stats['margins'] else 0
    
    regression_analysis['conference_splits'][conf_type] = {
        'record': f"{stats['w']}-{stats['l']}",
        'win_pct': round(win_pct, 1),
        'avg_margin': round(avg_margin, 1),
        'games': total
    }

# Post-loss bounce
total_post_loss = post_loss_record['w'] + post_loss_record['l']
post_loss_pct = (post_loss_record['w'] / total_post_loss * 100) if total_post_loss > 0 else 0
regression_analysis['post_loss_bounce'] = {
    'record': f"{post_loss_record['w']}-{post_loss_record['l']}",
    'win_pct': round(post_loss_pct, 1),
    'bounces_back_well': post_loss_pct >= 75
}

# ============================================================================
# SECTION 10: Print Results (EXISTING - keeping as is)
# ============================================================================
print("\n" + "=" * 70)
print("📊 COMPREHENSIVE RYAN DAY PROFILE")
print("=" * 70)

print("\n🎯 CAREER RECORD")
print(f"  Acting HC (2018):    {acting_hc_w}-{acting_hc_l} ({acting_hc_w/(acting_hc_w+acting_hc_l)*100:.1f}%)")
print(f"  Regular Season:      {regular_w}-{regular_l} ({regular_w/(regular_w+regular_l)*100:.1f}%)")
print(f"  Postseason:          {postseason_w}-{postseason_l} ({postseason_w/(postseason_w+postseason_l)*100:.1f}%)" if postseason_w+postseason_l > 0 else "  Postseason:          0-0 (no games)")
print(f"  2025 Season:         {y2025_w}-{y2025_l} ({y2025_w/(y2025_w+y2025_l)*100:.1f}%)" if y2025_w+y2025_l > 0 else "  2025 Season:         0-0")
print(f"  TOTAL:               {total_w}-{total_l} ({total_w/(total_w+total_l)*100:.1f}%)")

print("\n🏟️  LOCATION SPLITS")
print(f"  Home:   {home_w}-{home_l} ({home_w/(home_w+home_l)*100:.1f}%)" if home_w+home_l > 0 else "  Home:   0-0")
print(f"  Away:   {away_w}-{away_l} ({away_w/(away_w+away_l)*100:.1f}%)" if away_w+away_l > 0 else "  Away:   0-0")
print(f"  Neutral: {neut_w}-{neut_l} ({neut_w/(neut_w+neut_l)*100:.1f}%)" if neut_w+neut_l > 0 else "  Neutral: 0-0")

print("\n🎖️  VS RANKED OPPONENTS")
if vs_ranked_w + vs_ranked_l > 0:
    print(f"  Overall:    {vs_ranked_w}-{vs_ranked_l} ({vs_ranked_w/(vs_ranked_w+vs_ranked_l)*100:.1f}%)")
    print(f"  vs Top 5:   {vs_top5_w}-{vs_top5_l}" + (f" ({vs_top5_w/(vs_top5_w+vs_top5_l)*100:.1f}%)" if vs_top5_w+vs_top5_l > 0 else ""))
    print(f"  vs Top 10:  {vs_top10_w}-{vs_top10_l}" + (f" ({vs_top10_w/(vs_top10_w+vs_top10_l)*100:.1f}%)" if vs_top10_w+vs_top10_l > 0 else ""))
    print(f"\n  By Conference:")
    for conf in sorted(vs_ranked_by_conf.keys()):
        w = vs_ranked_by_conf[conf]['w']
        l = vs_ranked_by_conf[conf]['l']
        print(f"    {conf:15s} {w}-{l}")
else:
    print("  No ranked opponents found")

print("\n💰 AGAINST THE SPREAD (2025)")
if ats_w + ats_l + ats_push > 0:
    print(f"  ATS Record: {ats_w}-{ats_l}-{ats_push} ({ats_w/(ats_w+ats_l)*100:.1f}%)" if ats_w+ats_l > 0 else f"  ATS Record: {ats_w}-{ats_l}-{ats_push}")
    print(f"\n  Week-by-Week:")
    for detail in ats_details:
        print(f"    Week {detail['week']:2d} vs {detail['opponent']:20s} {detail['score']:8s} | Spread: {detail['spread']:+5.1f} | {detail['result']}")
else:
    print("  No betting lines available")

print("\n📈 OHIO STATE TEAM RANKINGS (Ryan Day Era)")
if osu_rankings:
    print(f"  Average Rank:        #{avg_rank:.1f}")
    print(f"  Lowest Rank Ever:    #{lowest_rank} (Week {lowest_rank_week}, {lowest_rank_season})")
    print(f"  Weeks in Top 5:      {weeks_top5}")
    print(f"  Weeks in Top 10:     {weeks_top10}")
    print(f"  Weeks in Top 25:     {weeks_top25}")
    print(f"  Longest Top 5 Streak: {max_streak} weeks")

print("\n🏆 RIVALRY RECORDS")
for rival in ['Michigan', 'Penn State', 'Michigan State', 'Wisconsin']:
    if rival in rivalries:
        w = rivalries[rival]['w']
        l = rivalries[rival]['l']
        print(f"  vs {rival:20s} {w}-{l}")

print("\n📊 PERFORMANCE METRICS")
print(f"  Blowout Wins (20+):  {blow_w}")
print(f"  Close Games (≤7):    {close_w}-{close_l}")
if margins:
    print(f"  Avg Margin:          {sum(margins)/len(margins):+.1f}")
if recent:
    last_10 = recent[-10:]
    print(f"  Last 10 Games:       {sum(last_10)}-{len(last_10)-sum(last_10)}")

print("\n" + "=" * 70)

# ============================================================================
# SECTION 11: Save All JSON Files
# ============================================================================
print("\n💾 Saving comprehensive analysis to JSON files...")

# FILE 1: Complete Profile (Enhanced)
profile = {
    'generated': str(datetime.now()),
    'coach': 'Ryan Day',
    'career': {
        'acting_hc_2018': f"{acting_hc_w}-{acting_hc_l}",
        'regular_season': f"{regular_w}-{regular_l}",
        'postseason': f"{postseason_w}-{postseason_l}",
        'total': f"{total_w}-{total_l}",
        'win_pct': round(total_w / (total_w + total_l) * 100, 1)
    },
    'splits': {
        'home': f"{home_w}-{home_l}",
        'away': f"{away_w}-{away_l}",
        'neutral': f"{neut_w}-{neut_l}"
    },
    'vs_ranked': {
        'overall': f"{vs_ranked_w}-{vs_ranked_l}",
        'vs_top5': f"{vs_top5_w}-{vs_top5_l}",
        'vs_top10': f"{vs_top10_w}-{vs_top10_l}",
        'by_conference': {conf: f"{stats['w']}-{stats['l']}" for conf, stats in vs_ranked_by_conf.items()}
    },
    'ats_2025': {
        'record': f"{ats_w}-{ats_l}-{ats_push}",
        'win_pct': round(ats_w/(ats_w+ats_l)*100, 1) if ats_w+ats_l > 0 else 0,
        'details': ats_details
    },
    'team_rankings': {
        'avg_rank': round(avg_rank, 1) if osu_rankings else None,
        'lowest_rank': lowest_rank if osu_rankings else None,
        'weeks_top5': weeks_top5 if osu_rankings else 0,
        'weeks_top10': weeks_top10 if osu_rankings else 0,
        'longest_top5_streak': max_streak if osu_rankings else 0
    },
    'rivalries': {rival: f"{stats['w']}-{stats['l']}" for rival, stats in rivalries.items()},
    'metrics': {
        'blowout_wins': blow_w,
        'close_games': f"{close_w}-{close_l}",
        'avg_margin': round(sum(margins)/len(margins), 1) if margins else 0,
        'one_score_games': f"{one_score_w}-{one_score_l}"
    }
}

with open('ryan_day_complete_profile.json', 'w') as f:
    json.dump(profile, f, indent=2)
print("  ✓ ryan_day_complete_profile.json")

# FILE 2: Yearly Performance
yearly_performance = {
    'generated': str(datetime.now()),
    'summary': {
        'total_seasons': len(yearly_records),
        'date_range': f"{yearly_records[0]['year']}-{yearly_records[-1]['year']}" if yearly_records else "N/A",
        'avg_win_pct': round(sum(yr['win_pct'] for yr in yearly_records) / len(yearly_records), 1) if yearly_records else 0
    },
    'yearly_records': yearly_records
}

with open('yearly_performance.json', 'w') as f:
    json.dump(yearly_performance, f, indent=2)
print("  ✓ yearly_performance.json")

# FILE 3: Regression Analysis
with open('regression_analysis.json', 'w') as f:
    json.dump(regression_analysis, f, indent=2)
print("  ✓ regression_analysis.json")

# FILE 4: Talent and Development
talent_and_development = {
    'generated': str(datetime.now()),
    'talent_composite': {
        'by_year': talent_analysis,
        'avg_talent': round(avg_talent, 1) if avg_talent else None,
        'years_tracked': len(talent_data)
    },
    'nfl_draft': {
        'total_picks': draft_analysis['total_picks'],
        'first_round_picks': draft_analysis['first_round_picks'],
        'top_10_picks': draft_analysis['top_10_picks'],
        'avg_draft_position': round(avg_draft_pos, 1) if avg_draft_pos else None,
        'picks_per_year': round(picks_per_year, 1),
        'by_year': dict(draft_analysis['by_year']),
        'by_round': dict(draft_analysis['by_round']),
        'by_position': dict(draft_analysis['by_position']),
        'all_picks': draft_analysis['picks_detail']
    }
}

with open('talent_and_development.json', 'w') as f:
    json.dump(talent_and_development, f, indent=2)
print("  ✓ talent_and_development.json")

# FILE 5: Game-by-Game Enhanced
game_by_game = {
    'generated': str(datetime.now()),
    'total_games': len(enhanced_games),
    'games': enhanced_games
}

with open('game_by_game_enhanced.json', 'w') as f:
    json.dump(game_by_game, f, indent=2)
print("  ✓ game_by_game_enhanced.json")

# FILE 6: Summary Statistics
summary_stats = {
    'generated': str(datetime.now()),
    'overview': {
        'coach': 'Ryan Day',
        'era': '2018-2025',
        'total_record': f"{total_w}-{total_l}",
        'win_pct': round(total_w / (total_w + total_l) * 100, 1),
        'total_games': total_w + total_l
    },
    'key_performance_indicators': {
        'vs_ranked': f"{vs_ranked_w}-{vs_ranked_l} ({round(vs_ranked_w/(vs_ranked_w+vs_ranked_l)*100,1)}%)" if vs_ranked_w+vs_ranked_l > 0 else "0-0",
        'vs_top_10': f"{vs_top10_w}-{vs_top10_l}",
        'ats_2025': f"{ats_w}-{ats_l}-{ats_push}",
        'postseason': f"{postseason_w}-{postseason_l}",
        'home_record': f"{home_w}-{home_l}",
        'avg_margin': round(sum(margins)/len(margins), 1) if margins else 0
    },
    'notable_achievements': {
        'longest_win_streak': max_win_streak,
        'blowout_wins_20plus': blow_w,
        'perfect_seasons': sum(1 for yr in yearly_records if yr['losses'] == 0),
        'nfl_draft_picks': draft_analysis['total_picks'],
        'first_rounders': draft_analysis['first_round_picks']
    },
    'areas_of_concern': {
        'vs_michigan': f"{rivalries['Michigan']['w']}-{rivalries['Michigan']['l']}" if 'Michigan' in rivalries else "N/A",
        'postseason_win_pct': round(postseason_w/(postseason_w+postseason_l)*100, 1) if postseason_w+postseason_l > 0 else 0,
        'close_game_record': f"{close_w}-{close_l}",
        'late_season_dropoff': regression_analysis['phase_performance']['Late']['win_pct'] < regression_analysis['phase_performance']['Early']['win_pct'] if 'Late' in regression_analysis['phase_performance'] and 'Early' in regression_analysis['phase_performance'] else False
    },
    'trend_analysis': {
        'yearly_records': yearly_records,
        'talent_trend': 'increasing' if talent_data and len(talent_data) > 1 and talent_data[-1].get('talent', 0) > talent_data[0].get('talent', 0) else 'stable',
        'draft_picks_trend': draft_analysis['by_year']
    }
}

with open('summary_statistics.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)
print("  ✓ summary_statistics.json")

# ============================================================================
# SECTION 11B: Create Master File with Everything
# ============================================================================
print("\n📦 Creating master file with all data combined...")
master_file = {
    'metadata': {
        'generated': str(datetime.now()),
        'coach': 'Ryan Day',
        'school': 'Ohio State',
        'era': '2018-2025',
        'description': 'Comprehensive Ryan Day coaching profile with all statistics, games, and analysis'
    },
    'summary': summary_stats,
    'career_stats': profile,
    'yearly_performance': yearly_performance,
    'regression_analysis': regression_analysis,
    'talent_and_development': talent_and_development,
    'games': game_by_game,
    'roster_integrity': {
        'total_draft_picks': draft_analysis['total_picks'],
        'years_covered': len(talent_data),
        'coach_seasons_tracked': len(coach_seasons) if coach_seasons else len(yearly_records),
        'data_quality': 'complete' if len(talent_data) > 0 and len(draft_picks) > 0 else 'partial'
    }
}

with open('ryan_day_master.json', 'w') as f:
    json.dump(master_file, f, indent=2)
print("  ✓ ryan_day_master.json (MASTER FILE - Contains everything)")

# ============================================================================
# SECTION 12: Final Summary & Validation
# ============================================================================
print("\n" + "=" * 70)
print("📊 DATA GENERATION COMPLETE")
print("=" * 70)
print(f"\n✅ Total JSON files created: 7 (including master)")
print(f"✅ Total games analyzed: {len(enhanced_games)}")
print(f"✅ Date range: {yearly_records[0]['year'] if yearly_records else 'N/A'} - {yearly_records[-1]['year'] if yearly_records else 'N/A'}")
print(f"✅ Seasons tracked: {len(yearly_records)}")
print(f"✅ NFL Draft picks: {draft_analysis['total_picks']}")
print(f"✅ Talent data points: {len(talent_data)}")
print(f"✅ Ranked opponents faced: {len(opponent_rankings)}")

print("\n📁 Files Generated:")
print("  1. ryan_day_complete_profile.json - Core stats and records")
print("  2. yearly_performance.json - Year-by-year breakdown")
print("  3. regression_analysis.json - Pattern detection & trends")
print("  4. talent_and_development.json - Recruiting & NFL draft")
print("  5. game_by_game_enhanced.json - Detailed game metadata")
print("  6. summary_statistics.json - Executive summary")

if len(talent_data) == 0:
    print("\n⚠️  Warning: No talent composite data available")
if len(draft_picks) == 0:
    print("⚠️  Warning: No NFL draft data available")
if len(coach_seasons) == 0:
    print("⚠️  Warning: Coach season records reconstructed from game data")

print("\n" + "=" * 70)
