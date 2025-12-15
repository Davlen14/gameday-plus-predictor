#!/usr/bin/env python3
"""
Generate timeline data for ALL coaches and store directly in database
Creates coach_timeline_data table with JSON columns for weekly, monthly, yearly data
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def get_season_start_date(season):
    """Approximate start date for a college football season"""
    return datetime(season, 9, 1)

def get_week_date(season, week):
    """Approximate date for a given week in a season"""
    start = get_season_start_date(season)
    return start + timedelta(weeks=week-1)

def generate_coach_timeline(coach_id, conn):
    """Generate timeline data for a single coach"""
    cursor = conn.cursor()
    
    # Get coach info
    cursor.execute("SELECT * FROM coaches WHERE id = ?", (coach_id,))
    coach_row = cursor.fetchone()
    if not coach_row:
        return None
    coach = dict(coach_row)
    
    # Get all stints
    cursor.execute("""
        SELECT s.*, t.id as team_id, t.color, t.abbreviation
        FROM stints s
        JOIN teams t ON s.school = t.school
        WHERE s.coach_id = ?
        ORDER BY s.start_year
    """, (coach_id,))
    stints = [dict(row) for row in cursor.fetchall()]
    
    if not stints:
        return None
    
    start_year = stints[0]['start_year']
    end_year = stints[-1]['end_year']
    
    # Initialize timeline data structures
    weekly_data = []
    monthly_data = defaultdict(lambda: {
        'games': 0, 'wins': 0, 'total_rank': 0, 'rank_count': 0,
        'ranked_wins': 0, 'home_wins': 0, 'home_games': 0
    })
    yearly_data = []
    
    # Get all games with enhanced data
    cursor.execute("""
        SELECT season, week, result, opponent_rank, is_conference, is_home, is_signature,
               coach_score, opponent_score, opponent, season_type
        FROM games
        WHERE coach_id = ?
        ORDER BY season, week
    """, (coach_id,))
    games = [dict(row) for row in cursor.fetchall()]
    
    if not games:
        return None
    
    # Get all rankings by week
    cursor.execute("""
        SELECT season, week, rank
        FROM rankings
        WHERE coach_id = ?
        ORDER BY season, week
    """, (coach_id,))
    rankings = [dict(row) for row in cursor.fetchall()]
    
    # Build weekly timeline with enhanced metrics
    running_wins = 0
    running_games = 0
    running_ranked_wins = 0
    running_home_wins = 0
    running_home_games = 0
    running_conf_wins = 0
    running_conf_games = 0
    running_points_for = 0
    running_points_against = 0
    current_win_streak = 0
    max_win_streak = 0
    
    for season in range(start_year, end_year + 1):
        season_games = [g for g in games if g['season'] == season]
        
        for week in range(0, 20):
            week_games = [g for g in season_games if g['week'] == week]
            week_rankings = [r for r in rankings if r['season'] == season and r['week'] == week]
            
            if not week_games and not week_rankings:
                continue
            
            # Calculate stats
            week_wins = sum(1 for g in week_games if g['result'] == 'W')
            week_total = len(week_games)
            week_ranked_wins = sum(1 for g in week_games if g['result'] == 'W' and g['opponent_rank'])
            week_home_wins = sum(1 for g in week_games if g['result'] == 'W' and g['is_home'])
            week_home_games = sum(1 for g in week_games if g['is_home'])
            week_conf_wins = sum(1 for g in week_games if g['result'] == 'W' and g['is_conference'])
            week_conf_games = sum(1 for g in week_games if g['is_conference'])
            week_points_for = sum(g['coach_score'] or 0 for g in week_games)
            week_points_against = sum(g['opponent_score'] or 0 for g in week_games)
            
            running_wins += week_wins
            running_games += week_total
            running_ranked_wins += week_ranked_wins
            running_home_wins += week_home_wins
            running_home_games += week_home_games
            running_conf_wins += week_conf_wins
            running_conf_games += week_conf_games
            running_points_for += week_points_for
            running_points_against += week_points_against
            
            # Track win streaks
            if week_wins > 0 and week_total == week_wins:
                current_win_streak += week_wins
                max_win_streak = max(max_win_streak, current_win_streak)
            elif week_total > 0:
                current_win_streak = 0
            
            win_pct = (running_wins / running_games * 100) if running_games > 0 else 0
            home_win_pct = (running_home_wins / running_home_games * 100) if running_home_games > 0 else 0
            conf_win_pct = (running_conf_wins / running_conf_games * 100) if running_conf_games > 0 else 0
            avg_margin = ((running_points_for - running_points_against) / running_games) if running_games > 0 else 0
            
            # Get AP ranking
            ap_rank = week_rankings[0]['rank'] if week_rankings else None
            ap_rank_inverted = (26 - ap_rank) * 4 if ap_rank else 0
            
            # Approximate date
            date = get_week_date(season, week if week > 0 else 1)
            timestamp = int(date.timestamp() * 1000)
            
            weekly_data.append({
                'x': timestamp,
                'date': date.strftime('%Y-%m-%d'),
                'season': season,
                'week': week,
                'win_pct': round(win_pct, 1),
                'home_win_pct': round(home_win_pct, 1),
                'conf_win_pct': round(conf_win_pct, 1),
                'ap_rank': ap_rank,
                'ap_rank_score': round(ap_rank_inverted, 1),
                'wins': running_wins,
                'games': running_games,
                'ranked_wins': running_ranked_wins,
                'avg_margin': round(avg_margin, 1),
                'win_streak': current_win_streak
            })
            
            # Add to monthly aggregation
            month_key = f"{season}-{date.month:02d}"
            monthly_data[month_key]['games'] += week_total
            monthly_data[month_key]['wins'] += week_wins
            monthly_data[month_key]['ranked_wins'] = monthly_data[month_key].get('ranked_wins', 0) + week_ranked_wins
            if ap_rank:
                monthly_data[month_key]['total_rank'] += ap_rank
                monthly_data[month_key]['rank_count'] += 1
    
    # Monthly data
    monthly_list = []
    for month_key in sorted(monthly_data.keys()):
        year, month = map(int, month_key.split('-'))
        data = monthly_data[month_key]
        
        date = datetime(year, month, 15)
        timestamp = int(date.timestamp() * 1000)
        
        win_pct = (data['wins'] / data['games'] * 100) if data['games'] > 0 else 0
        avg_rank = (data['total_rank'] / data['rank_count']) if data['rank_count'] > 0 else None
        
        monthly_list.append({
            'x': timestamp,
            'date': date.strftime('%Y-%m'),
            'win_pct': round(win_pct, 1),
            'avg_ap_rank': round(avg_rank, 1) if avg_rank else None,
            'games': data['games'],
            'wins': data['wins'],
            'ranked_wins': data['ranked_wins']
        })
    
    # Yearly data
    cursor.execute("""
        SELECT year, class_rank, total_rating, five_stars, four_stars
        FROM recruiting_classes
        WHERE coach_id = ?
        ORDER BY year
    """, (coach_id,))
    recruiting = {row['year']: dict(row) for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT year, COUNT(*) as total, 
               SUM(CASE WHEN round = 1 THEN 1 ELSE 0 END) as first_rounders
        FROM draft_picks
        WHERE coach_id = ?
        GROUP BY year
        ORDER BY year
    """, (coach_id,))
    draft_picks = {row['year']: dict(row) for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT year, talent_rank, talent_rating
        FROM talent_composite
        WHERE coach_id = ?
        ORDER BY year
    """, (coach_id,))
    talent = {row['year']: dict(row) for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT season, points_per_game, points_allowed_pg, sp_overall, sp_offense, sp_defense
        FROM season_analytics
        WHERE coach_id = ?
        ORDER BY season
    """, (coach_id,))
    analytics = {row['season']: dict(row) for row in cursor.fetchall()}
    
    for season in range(start_year, end_year + 1):
        season_games = [g for g in games if g['season'] == season]
        season_wins = sum(1 for g in season_games if g['result'] == 'W')
        season_total = len(season_games)
        season_ranked_wins = sum(1 for g in season_games if g['result'] == 'W' and g['opponent_rank'])
        season_home_wins = sum(1 for g in season_games if g['result'] == 'W' and g['is_home'])
        season_home_games = sum(1 for g in season_games if g['is_home'])
        season_conf_wins = sum(1 for g in season_games if g['result'] == 'W' and g['is_conference'])
        season_conf_games = sum(1 for g in season_games if g['is_conference'])
        season_points_for = sum(g['coach_score'] or 0 for g in season_games)
        season_points_against = sum(g['opponent_score'] or 0 for g in season_games)
        
        win_pct = (season_wins / season_total * 100) if season_total > 0 else 0
        home_win_pct = (season_home_wins / season_home_games * 100) if season_home_games > 0 else 0
        conf_win_pct = (season_conf_wins / season_conf_games * 100) if season_conf_games > 0 else 0
        avg_margin = ((season_points_for - season_points_against) / season_total) if season_total > 0 else 0
        
        season_rankings = [r['rank'] for r in rankings if r['season'] == season and r['rank']]
        best_rank = min(season_rankings) if season_rankings else None
        
        # Calculate elite score
        elite_score = 0
        elite_score += (win_pct * 0.3)
        
        if season in talent and talent[season]['talent_rank']:
            talent_score = max(0, 100 - (talent[season]['talent_rank'] * 4))
            elite_score += (talent_score * 0.25)
        
        if season in recruiting and recruiting[season]['class_rank']:
            recruit_score = max(0, 100 - (recruiting[season]['class_rank'] * 4))
            elite_score += (recruit_score * 0.20)
        
        if season in draft_picks:
            draft_score = min(100, draft_picks[season]['total'] * 5)
            elite_score += (draft_score * 0.15)
        
        if best_rank:
            rank_score = max(0, 100 - (best_rank * 4))
            elite_score += (rank_score * 0.10)
        
        date = datetime(season, 12, 31)
        timestamp = int(date.timestamp() * 1000)
        
        yearly_entry = {
            'x': timestamp,
            'date': str(season),
            'season': season,
            'win_pct': round(win_pct, 1),
            'home_win_pct': round(home_win_pct, 1),
            'conf_win_pct': round(conf_win_pct, 1),
            'record': f"{season_wins}-{season_total - season_wins}",
            'ranked_wins': season_ranked_wins,
            'avg_margin': round(avg_margin, 1),
            'best_ap_rank': best_rank,
            'recruiting_rank': recruiting.get(season, {}).get('class_rank'),
            'talent_rank': talent.get(season, {}).get('talent_rank'),
            'draft_picks': draft_picks.get(season, {}).get('total', 0),
            'first_rounders': draft_picks.get(season, {}).get('first_rounders', 0),
            'elite_score': round(elite_score, 1)
        }
        
        if season in analytics:
            yearly_entry['ppg'] = round(analytics[season]['points_per_game'], 1) if analytics[season]['points_per_game'] else None
            yearly_entry['ppg_allowed'] = round(analytics[season]['points_allowed_pg'], 1) if analytics[season]['points_allowed_pg'] else None
            yearly_entry['sp_overall'] = round(analytics[season]['sp_overall'], 1) if analytics[season]['sp_overall'] else None
            yearly_entry['sp_offense'] = round(analytics[season]['sp_offense'], 1) if analytics[season]['sp_offense'] else None
            yearly_entry['sp_defense'] = round(analytics[season]['sp_defense'], 1) if analytics[season]['sp_defense'] else None
        
        yearly_data.append(yearly_entry)
    
    # Plot bands
    plot_bands = []
    for stint in stints:
        start_date = get_season_start_date(stint['start_year'])
        end_date = datetime(stint['end_year'], 12, 31)
        
        plot_bands.append({
            'from': int(start_date.timestamp() * 1000),
            'to': int(end_date.timestamp() * 1000),
            'color': f"{stint['color']}22" if stint.get('color') else '#cccccc22',
            'school': stint['school'],
            'record': stint['record']
        })
    
    # Flags (milestones)
    flags = []
    
    # Bowl wins
    cursor.execute("""
        SELECT season, week, opponent, coach_score, opponent_score
        FROM games
        WHERE coach_id = ? AND season_type = 'postseason' AND result = 'W'
        ORDER BY season, week
    """, (coach_id,))
    bowl_wins = [dict(row) for row in cursor.fetchall()]
    
    for bowl in bowl_wins:
        date = get_week_date(bowl['season'], bowl['week'])
        flags.append({
            'x': int(date.timestamp() * 1000),
            'title': '🏆',
            'text': f"Bowl Win vs {bowl['opponent']} ({bowl['coach_score']}-{bowl['opponent_score']})",
            'type': 'bowl_win'
        })
    
    # Signature wins
    cursor.execute("""
        SELECT season, week, opponent, opponent_rank, coach_score, opponent_score
        FROM games
        WHERE coach_id = ? AND is_signature = 1 AND result = 'W'
        ORDER BY season, week
    """, (coach_id,))
    signature_wins = [dict(row) for row in cursor.fetchall()]
    
    for sig in signature_wins:
        date = get_week_date(sig['season'], sig['week'])
        rank_text = f" (#{sig['opponent_rank']})" if sig['opponent_rank'] else ""
        flags.append({
            'x': int(date.timestamp() * 1000),
            'title': '🌟',
            'text': f"Signature Win vs {sig['opponent']}{rank_text}",
            'type': 'signature_win'
        })
    
    # Win streaks
    win_streak_count = 0
    for game in games:
        if game['result'] == 'W':
            win_streak_count += 1
            if win_streak_count in [5, 10, 15, 20]:
                date = get_week_date(game['season'], game['week'])
                flags.append({
                    'x': int(date.timestamp() * 1000),
                    'title': '🔥',
                    'text': f"{win_streak_count} Game Win Streak",
                    'type': 'win_streak'
                })
        else:
            win_streak_count = 0
    
    # Undefeated seasons
    for season in range(start_year, end_year + 1):
        season_games = [g for g in games if g['season'] == season]
        season_wins = sum(1 for g in season_games if g['result'] == 'W')
        season_total = len(season_games)
        
        if season_total > 0 and season_wins == season_total:
            date = datetime(season, 12, 31)
            flags.append({
                'x': int(date.timestamp() * 1000),
                'title': '💎',
                'text': f"Undefeated Season ({season_wins}-0)",
                'type': 'undefeated'
            })
    
    # First round draft picks
    for year, data in draft_picks.items():
        if data['first_rounders'] > 0:
            date = datetime(year, 4, 28)
            flags.append({
                'x': int(date.timestamp() * 1000),
                'title': '⭐',
                'text': f"{data['first_rounders']} First Round Pick{'s' if data['first_rounders'] > 1 else ''}",
                'type': 'draft_pick'
            })
    
    return {
        'coach_id': coach_id,
        'coach_name': coach['name'],
        'generated_at': datetime.now().isoformat(),
        'career_record': f"{running_wins}-{running_games - running_wins}",
        'career_win_pct': round((running_wins / running_games * 100) if running_games > 0 else 0, 1),
        'max_win_streak': max_win_streak,
        'total_ranked_wins': running_ranked_wins,
        'weekly': weekly_data,
        'monthly': monthly_list,
        'yearly': yearly_data,
        'plot_bands': plot_bands,
        'flags': flags
    }

def create_timeline_table(conn):
    """Create the coach_timeline_data table if it doesn't exist"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coach_timeline_data (
            coach_id INTEGER PRIMARY KEY,
            coach_name TEXT NOT NULL,
            career_record TEXT,
            career_win_pct REAL,
            max_win_streak INTEGER,
            total_ranked_wins INTEGER,
            weekly_data TEXT,
            monthly_data TEXT,
            yearly_data TEXT,
            plot_bands TEXT,
            flags TEXT,
            generated_at TEXT,
            FOREIGN KEY (coach_id) REFERENCES coaches(id)
        )
    """)
    conn.commit()
    print("✅ Created/verified coach_timeline_data table")

def insert_timeline_data(conn, timeline_data):
    """Insert or update timeline data for a coach"""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO coach_timeline_data (
            coach_id, coach_name, career_record, career_win_pct, max_win_streak,
            total_ranked_wins, weekly_data, monthly_data, yearly_data, 
            plot_bands, flags, generated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timeline_data['coach_id'],
        timeline_data['coach_name'],
        timeline_data['career_record'],
        timeline_data['career_win_pct'],
        timeline_data['max_win_streak'],
        timeline_data['total_ranked_wins'],
        json.dumps(timeline_data['weekly']),
        json.dumps(timeline_data['monthly']),
        json.dumps(timeline_data['yearly']),
        json.dumps(timeline_data['plot_bands']),
        json.dumps(timeline_data['flags']),
        timeline_data['generated_at']
    ))
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('instance/coaches_master.db')
    conn.row_factory = sqlite3.Row
    
    print("🏈 GENERATING TIMELINE DATA FOR ALL COACHES")
    print("=" * 80)
    
    # Create table
    create_timeline_table(conn)
    
    # Get all coaches with games
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c.id, c.name
        FROM coaches c
        JOIN games g ON c.id = g.coach_id
        ORDER BY c.name
    """)
    coaches = cursor.fetchall()
    
    print(f"\n📊 Found {len(coaches)} coaches with game data\n")
    
    success_count = 0
    error_count = 0
    
    for i, coach_row in enumerate(coaches, 1):
        coach_id = coach_row['id']
        coach_name = coach_row['name']
        
        try:
            print(f"[{i}/{len(coaches)}] Processing {coach_name} (ID: {coach_id})...", end=" ")
            
            timeline_data = generate_coach_timeline(coach_id, conn)
            
            if timeline_data:
                insert_timeline_data(conn, timeline_data)
                print(f"✅ {len(timeline_data['weekly'])} weeks, {len(timeline_data['yearly'])} years, {len(timeline_data['flags'])} flags")
                success_count += 1
            else:
                print("⚠️  No data")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            error_count += 1
    
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"✅ Successfully processed: {success_count} coaches")
    print(f"❌ Errors: {error_count} coaches")
    print(f"💾 Data stored in: coach_timeline_data table")
    print("\n🔍 Query timeline data:")
    print("   SELECT coach_name, career_record FROM coach_timeline_data;")
