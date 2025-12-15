"""
🌐 UNIVERSAL COACH DATABASE API
================================
Flask application serving coach data from coaches_master.db

Dynamic endpoints that work for ANY coach in the database.

Endpoints:
    GET  /api/coaches                    - List all coaches
    GET  /api/coach/<id>                 - Get coach details
    GET  /api/coach/<id>/stints          - Coaching history
    GET  /api/coach/<id>/games           - Game history
    GET  /api/coach/<id>/rankings        - AP Poll history
    GET  /api/coach/<id>/draft_picks     - NFL draft picks
    GET  /api/coach/<id>/situational     - Situational stats
    GET  /api/coach/<id>/vs_coaches      - Head-to-head records
    GET  /api/coach/<id>/season_analytics - Season analytics
    GET  /api/coach/<id>/recruiting      - Recruiting classes
    GET  /api/coach/<id>/talent          - Talent composite
    GET  /api/coach/<id>/portal          - Transfer portal

Usage:
    python app_master.py
    
    Then visit: http://localhost:5555
"""

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path
from typing import Dict, List, Optional

app = Flask(__name__)
CORS(app)
DB_PATH = 'instance/coaches_master.db'


def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row) -> Dict:
    """Convert sqlite Row to dict"""
    return dict(row) if row else None


def rows_to_list(rows) -> List[Dict]:
    """Convert list of rows to list of dicts"""
    return [dict(row) for row in rows]


# =============================================================================
# HTML ROUTES
# =============================================================================

@app.route('/')
def index():
    """Homepage - Main landing page"""
    return jsonify({
        'message': 'Gameday+ Coach Database API',
        'version': '1.0.0',
        'endpoints': {
            '/api/coaches': 'List all coaches',
            '/api/coach/<id>': 'Get coach details',
            '/api/coach/<id>/stints': 'Coaching history',
            '/api/coach/<id>/games': 'Game history',
            '/api/coach/<id>/rankings': 'AP Poll history',
            '/api/coach/<id>/draft_picks': 'NFL draft picks',
            '/api/coach/<id>/situational': 'Situational stats',
            '/api/coach/<id>/vs_coaches': 'Head-to-head records',
            '/api/coach/<id>/season_analytics': 'Season analytics',
            '/api/coach/<id>/recruiting': 'Recruiting classes',
            '/api/coach/<id>/talent': 'Talent composite',
            '/api/coach/<id>/portal': 'Transfer portal'
        }
    })

@app.route('/gamedaylive')
def gamedaylive():
    """GAMEDAY+ Live - Real-time game and analytics showcase"""
    return render_template('gamedaylive.html')

@app.route('/master-dashboard')
def master_dashboard():
    """Master Dashboard - Comprehensive visualization of all data"""
    return render_template('master_dashboard.html')

@app.route('/drives-explorer')
def drives_explorer():
    """Drives Explorer Dashboard"""
    return render_template('drives_explorer.html')


@app.route('/coaches')
def coaches_list():
    """Coaches database page"""
    return render_template('coaches_list.html')


@app.route('/coach/<int:coach_id>')
def coach_detail(coach_id: int):
    """Individual coach profile page"""
    return render_template('coach_detail.html')


@app.route('/teams')
def teams_list():
    """Teams database page"""
    return render_template('teams_list.html')


@app.route('/team/<int:team_id>')
def team_detail(team_id: int):
    """Individual team profile page"""
    return render_template('team_detail.html')


@app.route('/nil')
def nil_index():
    """NIL valuations index page"""
    return render_template('nil_index.html')


@app.route('/nil/team/<int:team_id>')
def nil_team_detail(team_id: int):
    """NIL team detail page"""
    return render_template('nil_team_detail.html')


@app.route('/game/<int:game_id>')
def game_detail_dynamic(game_id: int):
    """Game detail page - Coming Soon (Dynamic)"""
    return render_template('game_detail.html')


@app.route('/game-detail')
def game_detail():
    """Game detail page - Coming Soon (Static for development)"""
    return render_template('game_detail.html')


# =============================================================================
# REACT PREDICTOR APP ROUTES
# =============================================================================

@app.route('/predictor')
@app.route('/predictor/')
def serve_predictor_root():
    """Serve the React predictor app index"""
    try:
        frontend_dist = os.path.join('frontend', 'dist')
        if os.path.exists(frontend_dist):
            return send_from_directory(frontend_dist, 'index.html')
        else:
            return jsonify({
                'error': 'Predictor frontend not built',
                'message': 'Run `cd frontend && npm run build` to build the React app'
            }), 404
    except Exception as e:
        return jsonify({'error': 'Error serving predictor', 'details': str(e)}), 500

@app.route('/predictor/<path:path>')
def serve_predictor_assets(path):
    """Serve React predictor app assets and handle client-side routing"""
    try:
        frontend_dist = os.path.join('frontend', 'dist')
        if os.path.exists(frontend_dist):
            # Try to serve the requested file
            file_path = os.path.join(frontend_dist, path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(frontend_dist, path)
            else:
                # Fall back to index.html for React Router
                return send_from_directory(frontend_dist, 'index.html')
        else:
            return jsonify({
                'error': 'Predictor frontend not built',
                'message': 'Run `cd frontend && npm run build` to build the React app'
            }), 404
    except Exception as e:
        return jsonify({'error': 'Error serving predictor assets', 'details': str(e)}), 500


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/fbs.json')
def serve_fbs_json():
    """Serve FBS teams data for frontend"""
    import json
    try:
        with open('fbs.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([]), 404

@app.route('/api/coaches')
def api_get_coaches():
    """Get list of all coaches"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.id, c.name, c.current_school, c.headshot_url,
            c.career_record, c.career_win_pct, c.total_games, c.created_at,
            COUNT(DISTINCT r.id) as weeks_ranked
        FROM coaches c
        LEFT JOIN rankings r ON c.id = r.coach_id
        GROUP BY c.id
        ORDER BY c.name
    """)
    
    coaches = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coaches': coaches,
        'count': len(coaches)
    })


@app.route('/api/teams')
def api_get_teams():
    """Get list of all FBS teams"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            t.id,
            t.school,
            t.mascot,
            t.abbreviation,
            t.conference,
            t.division,
            t.classification,
            t.color,
            t.alt_color,
            t.logo_url,
            t.location_name,
            t.city,
            t.state,
            t.capacity,
            COUNT(DISTINCT r.id) as total_rankings,
            COUNT(DISTINCT s.id) as total_seasons
        FROM teams t
        LEFT JOIN team_rankings r ON t.id = r.team_id
        LEFT JOIN team_seasons s ON t.id = s.team_id
        GROUP BY t.id
        ORDER BY t.school
    """)
    
    teams = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'teams': teams,
        'count': len(teams)
    })


@app.route('/api/team/<int:team_id>')
def api_get_team(team_id: int):
    """Get detailed information for a single team"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get team basic info
    cursor.execute("""
        SELECT * FROM teams WHERE id = ?
    """, (team_id,))
    
    team = row_to_dict(cursor.fetchone())
    if not team:
        conn.close()
        return jsonify({'error': 'Team not found'}), 404
    
    # Get all rankings for this team
    cursor.execute("""
        SELECT 
            season,
            week,
            ap_rank,
            coaches_rank,
            playoff_rank
        FROM team_rankings
        WHERE team_id = ?
        ORDER BY season DESC, week DESC
    """, (team_id,))
    
    team['rankings'] = rows_to_list(cursor.fetchall())
    
    # Get ALL season records with EVERY metric (113 columns total)
    cursor.execute("""
        SELECT *
        FROM team_seasons
        WHERE team_id = ?
        ORDER BY season DESC
    """, (team_id,))
    
    team['seasons'] = rows_to_list(cursor.fetchall())
    
    conn.close()
    
    return jsonify(team)


@app.route('/api/team/<int:team_id>/roster')
def api_get_team_roster(team_id: int):
    """Get team roster with player stats"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all players for this team with their stats
    cursor.execute("""
        SELECT 
            p.*,
            ps.season,
            ps.games_played,
            ps.passing_yards,
            ps.passing_tds,
            ps.rushing_yards,
            ps.rushing_tds,
            ps.receiving_yards,
            ps.receiving_tds,
            ps.total_tackles,
            ps.sacks
        FROM players p
        LEFT JOIN player_stats ps ON p.id = ps.player_id
        WHERE p.team_id = ?
        ORDER BY 
            CASE p.position_abbr 
                WHEN 'QB' THEN 1
                WHEN 'RB' THEN 2
                WHEN 'WR' THEN 3
                WHEN 'TE' THEN 4
                WHEN 'OL' THEN 5
                WHEN 'DL' THEN 6
                WHEN 'LB' THEN 7
                WHEN 'DB' THEN 8
                WHEN 'CB' THEN 9
                WHEN 'S' THEN 10
                ELSE 11
            END,
            CASE p.class_year
                WHEN 'SR' THEN 4
                WHEN 'JR' THEN 3
                WHEN 'SO' THEN 2
                WHEN 'FR' THEN 1
                ELSE 0
            END DESC,
            p.name
    """, (team_id,))
    
    roster = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify(roster)


@app.route('/api/coach/<int:coach_id>')
def api_get_coach(coach_id: int):
    """Get detailed coach information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM coaches WHERE id = ?", (coach_id,))
    coach = row_to_dict(cursor.fetchone())
    
    if not coach:
        conn.close()
        return jsonify({'error': 'Coach not found'}), 404
    
    # Get stint count
    cursor.execute("SELECT COUNT(*) as count FROM stints WHERE coach_id = ?", (coach_id,))
    coach['stint_count'] = cursor.fetchone()['count']
    
    # Get games count
    cursor.execute("SELECT COUNT(*) as count FROM games WHERE coach_id = ?", (coach_id,))
    coach['games_count'] = cursor.fetchone()['count']
    
    conn.close()
    return jsonify(coach)


@app.route('/api/coach/<int:coach_id>/stints')
def api_get_stints(coach_id: int):
    """Get coaching stints for a coach"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM stints 
        WHERE coach_id = ? 
        ORDER BY start_year DESC
    """, (coach_id,))
    
    stints = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'stints': stints,
        'count': len(stints)
    })


@app.route('/api/coach/<int:coach_id>/games')
def api_get_games(coach_id: int):
    """Get game history for a coach"""
    # Optional filters
    season = request.args.get('season', type=int)
    school = request.args.get('school')
    limit = request.args.get('limit', type=int, default=100)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM games WHERE coach_id = ?"
    params = [coach_id]
    
    if season:
        query += " AND season = ?"
        params.append(season)
    
    if school:
        query += " AND school = ?"
        params.append(school)
    
    query += " ORDER BY season DESC, week DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    games = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'games': games,
        'count': len(games)
    })


@app.route('/api/coach/<int:coach_id>/rankings')
def api_get_rankings(coach_id: int):
    """Get AP Poll rankings history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM rankings 
        WHERE coach_id = ? 
        ORDER BY season DESC, week DESC
    """, (coach_id,))
    
    rankings = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'rankings': rankings,
        'count': len(rankings)
    })


@app.route('/api/coach/<int:coach_id>/draft_picks')
def api_get_draft_picks(coach_id: int):
    """Get NFL draft picks produced"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM draft_picks 
        WHERE coach_id = ? 
        ORDER BY year DESC, round, pick
    """, (coach_id,))
    
    picks = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'draft_picks': picks,
        'count': len(picks)
    })


@app.route('/api/coach/<int:coach_id>/situational')
@app.route('/api/coach/<int:coach_id>/situational_stats')
def api_get_situational_stats(coach_id: int):
    """Get situational statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM situational_stats 
        WHERE coach_id = ? 
        ORDER BY stint_id
    """, (coach_id,))
    
    stats = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'situational_stats': stats,
        'count': len(stats)
    })


@app.route('/api/coach/<int:coach_id>/vs_coaches')
def api_get_vs_coaches(coach_id: int):
    """Get head-to-head records vs other coaches"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM vs_coaches 
        WHERE coach_id = ? 
        ORDER BY wins DESC, losses ASC
    """, (coach_id,))
    
    records = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'vs_coaches': records,
        'count': len(records)
    })


@app.route('/api/coach/<int:coach_id>/season_analytics')
def api_get_season_analytics(coach_id: int):
    """Get season-level analytics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM season_analytics 
        WHERE coach_id = ? 
        ORDER BY season DESC
    """, (coach_id,))
    
    analytics = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'season_analytics': analytics,
        'count': len(analytics)
    })


@app.route('/api/coach/<int:coach_id>/recruiting')
@app.route('/api/coach/<int:coach_id>/recruiting')
@app.route('/api/coach/<int:coach_id>/recruiting_classes')
def api_get_recruiting(coach_id: int):
    """Get recruiting class data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM recruiting_classes 
        WHERE coach_id = ? 
        ORDER BY year DESC
    """, (coach_id,))
    
    classes = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'recruiting_classes': classes,
        'count': len(classes)
    })


@app.route('/api/coach/<int:coach_id>/talent')
@app.route('/api/coach/<int:coach_id>/talent_composite')
def api_get_talent(coach_id: int):
    """Get talent composite data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM talent_composite 
        WHERE coach_id = ? 
        ORDER BY year DESC
    """, (coach_id,))
    
    talent = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'talent_composite': talent,
        'count': len(talent)
    })


@app.route('/api/coach/<int:coach_id>/portal')
@app.route('/api/coach/<int:coach_id>/transfer_portal')
def api_get_portal(coach_id: int):
    """Get transfer portal data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM transfer_portal 
        WHERE coach_id = ? 
        ORDER BY season DESC
    """, (coach_id,))
    
    portal = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'coach_id': coach_id,
        'transfer_portal': portal,
        'count': len(portal)
    })


@app.route('/api/coach/<int:coach_id>/timeline')
def api_get_timeline(coach_id: int):
    """Get career timeline data for Highcharts visualization"""
    import json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            coach_id,
            coach_name,
            career_record,
            career_win_pct,
            max_win_streak,
            total_ranked_wins,
            weekly_data,
            monthly_data,
            yearly_data,
            plot_bands,
            flags,
            generated_at
        FROM coach_timeline_data 
        WHERE coach_id = ?
    """, (coach_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Timeline data not found for this coach'}), 404
    
    # Parse JSON strings to objects
    timeline_data = {
        'coach_id': row['coach_id'],
        'coach_name': row['coach_name'],
        'career_record': row['career_record'],
        'career_win_pct': row['career_win_pct'],
        'max_win_streak': row['max_win_streak'],
        'total_ranked_wins': row['total_ranked_wins'],
        'weekly': json.loads(row['weekly_data']) if row['weekly_data'] else [],
        'monthly': json.loads(row['monthly_data']) if row['monthly_data'] else [],
        'yearly': json.loads(row['yearly_data']) if row['yearly_data'] else [],
        'plot_bands': json.loads(row['plot_bands']) if row['plot_bands'] else [],
        'flags': json.loads(row['flags']) if row['flags'] else [],
        'generated_at': row['generated_at']
    }
    
    return jsonify(timeline_data)


@app.route('/api/search')
def api_search():
    """Search for coaches by name or school"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Query parameter q required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            id, name, current_school, headshot_url,
            career_record, career_win_pct, total_games
        FROM coaches
        WHERE name LIKE ? OR current_school LIKE ?
        ORDER BY name
        LIMIT 20
    """, (f'%{query}%', f'%{query}%'))
    
    results = rows_to_list(cursor.fetchall())
    conn.close()
    
    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    })


@app.route('/api/nil/teams')
def api_nil_teams():
    """API endpoint for all NIL team summaries"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all teams
        cursor.execute('''
            SELECT 
                team_id, team_name, total_valuation, avg_valuation, total_players,
                qb_valuation, rb_valuation, wr_valuation, te_valuation, ol_valuation,
                dl_valuation, lb_valuation, db_valuation, k_valuation, p_valuation
            FROM nil_team_summary
            ORDER BY total_valuation DESC
        ''')
        teams = []
        for row in cursor.fetchall():
            teams.append({
                'team_id': row[0],
                'team_name': row[1],
                'total_valuation': row[2],
                'avg_valuation': row[3],
                'total_players': row[4],
                'qb_valuation': row[5],
                'rb_valuation': row[6],
                'wr_valuation': row[7],
                'te_valuation': row[8],
                'ol_valuation': row[9],
                'dl_valuation': row[10],
                'lb_valuation': row[11],
                'db_valuation': row[12],
                'k_valuation': row[13],
                'p_valuation': row[14]
            })
        
        # Get global stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_players,
                SUM(valuation) as total_valuation,
                AVG(valuation) as avg_valuation
            FROM nil_players
        ''')
        stats_row = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(DISTINCT team_id) FROM nil_team_summary')
        total_teams = cursor.fetchone()[0]
        
        return jsonify({
            'teams': teams,
            'stats': {
                'total_players': stats_row[0],
                'total_valuation': stats_row[1],
                'avg_valuation': stats_row[2],
                'total_teams': total_teams
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/nil/team/<int:team_id>')
def api_nil_team(team_id: int):
    """API endpoint for single team NIL summary"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                team_id, team_name, total_valuation, avg_valuation, total_players,
                qb_valuation, rb_valuation, wr_valuation, te_valuation, ol_valuation,
                dl_valuation, lb_valuation, db_valuation, k_valuation, p_valuation
            FROM nil_team_summary
            WHERE team_id = ?
        ''', (team_id,))
        
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Team not found'}), 404
        
        return jsonify({
            'team_id': row[0],
            'team_name': row[1],
            'total_valuation': row[2],
            'avg_valuation': row[3],
            'total_players': row[4],
            'qb_valuation': row[5],
            'rb_valuation': row[6],
            'wr_valuation': row[7],
            'te_valuation': row[8],
            'ol_valuation': row[9],
            'dl_valuation': row[10],
            'lb_valuation': row[11],
            'db_valuation': row[12],
            'k_valuation': row[13],
            'p_valuation': row[14]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/nil/team/<int:team_id>/players')
def api_nil_team_players(team_id: int):
    """API endpoint for team's NIL player list"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id, player_name, position, position_order, valuation,
                eff1, sigma1, eff2, sigma2, weight_2025, is_backup
            FROM nil_players
            WHERE team_id = ?
            ORDER BY valuation DESC
        ''', (team_id,))
        
        players = []
        for row in cursor.fetchall():
            players.append({
                'id': row[0],
                'player_name': row[1],
                'position': row[2],
                'position_order': row[3],
                'valuation': row[4],
                'eff1': row[5],
                'sigma1': row[6],
                'eff2': row[7],
                'sigma2': row[8],
                'weight_2025': row[9],
                'is_backup': row[10]
            })
        
        return jsonify({'players': players})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/nil/team/<int:team_id>/positions')
def api_nil_team_positions(team_id: int):
    """API endpoint for team's position group analytics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                position, total_players, total_valuation, avg_valuation,
                avg_eff1, avg_eff2, avg_sigma1, avg_sigma2,
                starter_valuation, backup_valuation
            FROM nil_position_groups
            WHERE team_id = ?
            ORDER BY total_valuation DESC
        ''', (team_id,))
        
        positions = []
        for row in cursor.fetchall():
            positions.append({
                'position': row[0],
                'total_players': row[1],
                'total_valuation': row[2],
                'avg_valuation': row[3],
                'avg_eff1': row[4],
                'avg_eff2': row[5],
                'avg_sigma1': row[6],
                'avg_sigma2': row[7],
                'starter_valuation': row[8],
                'backup_valuation': row[9]
            })
        
        return jsonify({'positions': positions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_get_stats():
    """Get database statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Count each table
    tables = ['coaches', 'stints', 'games', 'rankings', 'draft_picks',
              'situational_stats', 'vs_coaches', 'season_analytics',
              'recruiting_classes', 'talent_composite', 'transfer_portal', 'player_season_stats']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        stats[table] = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify(stats)


@app.route('/api/players')
def api_get_players():
    """Get all player season stats"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            id, season, player_id, player_name, position, team, conference, position_type,
            passing_yards, passing_tds, pass_attempts, completions, completion_pct,
            interceptions, yards_per_attempt, rushing_yards, rushing_tds, carries,
            yards_per_carry, receiving_yards, receiving_tds, receptions,
            yards_per_reception, longest_reception, headshot_url, team_logo_url
        FROM player_season_stats
        ORDER BY 
            CASE 
                WHEN passing_yards IS NOT NULL AND passing_yards > 0 THEN passing_yards
                WHEN rushing_yards IS NOT NULL AND rushing_yards > 0 THEN rushing_yards
                WHEN receiving_yards IS NOT NULL AND receiving_yards > 0 THEN receiving_yards
                ELSE 0
            END DESC
        LIMIT 1000
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    players = [dict(row) for row in rows]
    
    return jsonify({'players': players, 'count': len(players)})


# =============================================================================
# PREDICTIONS DATABASE EXPLORER
# =============================================================================

PREDICTIONS_DB = 'instance/predictions.db'

@app.route('/predictions')
def predictions_explorer():
    """Predictions database explorer UI"""
    return render_template('predictions_explorer.html')

@app.route('/api/predictions/table/<table_name>')
def get_predictions_table(table_name):
    """Get data from a specific table in predictions.db"""
    try:
        conn = sqlite3.connect(PREDICTIONS_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get data (limit to 100 rows for performance)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        rows = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'columns': columns,
            'rows': rows,
            'total': len(rows)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upcoming-games', methods=['GET'])
def get_upcoming_games():
    """Get upcoming games from predictions database"""
    try:
        conn = sqlite3.connect('instance/predictions.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, start_date, week, season_type,
                home_team, home_abbreviation, home_logo, home_color, home_alt_color, home_record, home_rank,
                away_team, away_abbreviation, away_logo, away_color, away_alt_color, away_record, away_rank,
                spread, over_under, home_moneyline, away_moneyline,
                venue, neutral_site,
                home_fpi, away_fpi
            FROM upcoming_games
            ORDER BY start_date ASC
        """)
        
        games = []
        for row in cursor.fetchall():
            games.append({
                'id': row['id'],
                'date': row['start_date'],
                'week': row['week'],
                'seasonType': row['season_type'],
                'home': {
                    'team': row['home_team'],
                    'abbr': row['home_abbreviation'],
                    'logo': row['home_logo'],
                    'color': row['home_color'],
                    'altColor': row['home_alt_color'],
                    'record': row['home_record'],
                    'rank': row['home_rank'],
                    'fpi': row['home_fpi']
                },
                'away': {
                    'team': row['away_team'],
                    'abbr': row['away_abbreviation'],
                    'logo': row['away_logo'],
                    'color': row['away_color'],
                    'altColor': row['away_alt_color'],
                    'record': row['away_record'],
                    'rank': row['away_rank'],
                    'fpi': row['away_fpi']
                },
                'betting': {
                    'spread': row['spread'],
                    'overUnder': row['over_under'],
                    'homeMoneyline': row['home_moneyline'],
                    'awayMoneyline': row['away_moneyline']
                },
                'venue': row['venue'],
                'neutralSite': row['neutral_site']
            })
        
        conn.close()
        return jsonify({'games': games})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


# ===== DRIVES DATABASE API ENDPOINTS =====

@app.route('/api/drives/teams', methods=['GET'])
def get_drives_teams():
    """Get all teams from gameday_analytics.db"""
    try:
        conn = sqlite3.connect('gameday_analytics.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT team_name, conference 
            FROM teams 
            ORDER BY team_name
        """)
        
        teams = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(teams)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/drives/team/<team_name>/drives', methods=['GET'])
def get_team_drives(team_name):
    """Get all drives for a specific team"""
    try:
        conn = sqlite3.connect('gameday_analytics.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                d.*,
                def_team.team_name as defense_team
            FROM drives d
            JOIN teams offense_team ON d.offense_team_id = offense_team.id
            LEFT JOIN teams def_team ON d.defense_team_id = def_team.id
            WHERE offense_team.team_name = ?
            ORDER BY d.drive_id
        """, (team_name,))
        
        drives = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(drives)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/drives/team/<team_name>/stats', methods=['GET'])
def get_team_drive_stats(team_name):
    """Get drive statistics for a team"""
    try:
        conn = sqlite3.connect('gameday_analytics.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get total drives and basic stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_drives,
                AVG(d.yards) as avg_yards_per_drive,
                SUM(d.plays) as total_plays,
                SUM(CASE WHEN d.scoring = 1 THEN 1 ELSE 0 END) as scoring_drives,
                SUM(CASE WHEN d.drive_result LIKE '%TD%' THEN 1 ELSE 0 END) as td_drives,
                SUM(CASE WHEN d.drive_result LIKE '%FG%' OR d.drive_result LIKE '%FGA%' THEN 1 ELSE 0 END) as fg_drives,
                SUM(CASE WHEN d.drive_result LIKE '%PUNT%' THEN 1 ELSE 0 END) as punt_drives,
                SUM(CASE WHEN d.drive_result LIKE '%INT%' OR d.drive_result LIKE '%FUMBLE%' THEN 1 ELSE 0 END) as turnover_drives
            FROM drives d
            JOIN teams t ON d.offense_team_id = t.id
            WHERE t.team_name = ?
        """, (team_name,))
        
        stats = dict(cursor.fetchone())
        
        # Calculate percentages
        total = stats['total_drives'] or 1  # Avoid division by zero
        stats['td_rate'] = (stats['td_drives'] / total) * 100
        stats['scoring_rate'] = (stats['scoring_drives'] / total) * 100
        
        # Calculate "other" drives
        accounted = (stats['td_drives'] or 0) + (stats['fg_drives'] or 0) + (stats['punt_drives'] or 0) + (stats['turnover_drives'] or 0)
        stats['other_drives'] = stats['total_drives'] - accounted
        
        conn.close()
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/drives/drive/<int:drive_id>/plays', methods=['GET'])
def get_drive_plays(drive_id):
    """Get all plays for a specific drive"""
    try:
        conn = sqlite3.connect('gameday_analytics.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM plays
            WHERE drive_id = ?
            ORDER BY play_id
        """, (drive_id,))
        
        plays = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(plays)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check database exists
    if not Path(DB_PATH).exists():
        print("❌ Database not found!")
        print("Run setup_master_db.py first to create the database")
        exit(1)
    
    print("\n" + "=" * 80)
    print("🌐 UNIVERSAL COACH DATABASE API")
    print("=" * 80)
    print(f"📁 Database: {DB_PATH}")
    print(f"🌍 Server: http://localhost:5555")
    print(f"📊 API Docs: http://localhost:5555/api/stats")
    print("=" * 80 + "\n")
    
    app.run(debug=True, port=5555)
