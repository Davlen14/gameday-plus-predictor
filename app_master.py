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
import math
from pathlib import Path
from typing import Dict, List, Optional

# Try to import ESPN service, but don't fail if it's not available
try:
    from espn_game_service import ESPNGameService
    espn_service = ESPNGameService()
    print("✅ ESPN Game Service loaded")
except Exception as e:
    print(f"⚠️  ESPN Game Service not available: {e}")
    espn_service = None

app = Flask(__name__)
CORS(app)

# Database path - check multiple locations
DB_PATH = None
possible_paths = [
    'instance/coaches_master.db',
    '/opt/render/project/src/instance/coaches_master.db',  # Render
    '/app/instance/coaches_master.db',  # Railway/Docker
    'coaches_master.db',  # Root directory
]

for path in possible_paths:
    if os.path.exists(path):
        DB_PATH = path
        break

if not DB_PATH:
    # Fallback - will create error message on routes
    DB_PATH = 'instance/coaches_master.db'
    print("⚠️  WARNING: Database not found at any expected location")
    print(f"⚠️  Checked: {', '.join(possible_paths)}")


def get_db_connection():
    """Get database connection with row factory"""
    if not os.path.exists(DB_PATH):
        error_msg = f"Database not found at: {DB_PATH}"
        print(f"❌ {error_msg}")
        print(f"❌ Current working directory: {os.getcwd()}")
        print(f"❌ Directory contents: {os.listdir('.')}")
        if os.path.exists('instance'):
            print(f"❌ Instance directory contents: {os.listdir('instance')}")
        raise FileNotFoundError(error_msg)
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
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(FileNotFoundError)
def handle_db_not_found(e):
    """Handle database not found errors"""
    return jsonify({
        'error': 'Database not available',
        'message': str(e),
        'status': 'service_unavailable'
    }), 503

@app.errorhandler(500)
def handle_server_error(e):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(e),
        'status': 'error'
    }), 500

@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found',
        'status': 'not_found'
    }), 404


# =============================================================================
# HTML ROUTES
# =============================================================================

@app.route('/health')
def health_check():
    """Health check endpoint with database status"""
    db_exists = os.path.exists(DB_PATH)
    cwd = os.getcwd()
    
    status = {
        'status': 'healthy' if db_exists else 'degraded',
        'database': {
            'path': DB_PATH,
            'exists': db_exists,
            'size': os.path.getsize(DB_PATH) if db_exists else None
        },
        'environment': {
            'cwd': cwd,
            'port': os.environ.get('PORT', 'not set'),
            'python_version': os.sys.version
        }
    }
    
    if db_exists:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM coaches")
            coach_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as count FROM teams")
            team_count = cursor.fetchone()[0]
            conn.close()
            status['database']['coaches'] = coach_count
            status['database']['teams'] = team_count
            status['database']['accessible'] = True
        except Exception as e:
            status['database']['accessible'] = False
            status['database']['error'] = str(e)
    
    return jsonify(status), 200 if db_exists else 503

@app.route('/')
def index():
    """Homepage - Main landing page"""
    return jsonify({
        'message': 'Gameday+ Coach Database API',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check with database status',
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

@app.route('/api/map-data')
def map_data():
    """Get team data for the map with latest season stats"""
    # Coordinates for major programs
    TEAM_COORDINATES = {
        'Georgia': [33.9519, -83.3576], 'Florida State': [30.4383, -84.2807], 'Alabama': [33.2098, -87.5692],
        'Ohio State': [40.0142, -83.0305], 'Michigan': [42.2808, -83.7430], 'USC': [34.0522, -118.2437],
        'Texas A&M': [30.6280, -96.3344], 'Texas': [30.2849, -97.7341], 'Oklahoma': [35.2058, -97.4459],
        'Texas Tech': [33.2164, -97.1292], 'Notre Dame': [41.7001, -86.2379], 'UCLA': [34.0224, -118.2851],
        'California': [37.8716, -122.2585], 'Oregon': [45.5051, -122.6750], 'LSU': [30.4133, -91.1800],
        'Clemson': [34.6781, -82.8374], 'Penn State': [40.7982, -77.8599], 'Florida': [29.6496, -82.3486],
        'Miami': [25.7195, -80.2781], 'Tennessee': [35.9544, -83.9295], 'Auburn': [32.6010, -85.4911],
        'Washington': [47.6553, -122.3035], 'Wisconsin': [43.0702, -89.4125], 'Nebraska': [40.8202, -96.7005],
        'Iowa': [41.6586, -91.5425], 'Utah': [40.7649, -111.8421], 'TCU': [32.7097, -97.3681],
        'Baylor': [31.5493, -97.1143], 'Ole Miss': [34.3647, -89.5384], 'Mississippi State': [33.4552, -88.7944],
        'Arkansas': [36.0687, -94.1748], 'Kentucky': [38.0307, -84.5040], 'South Carolina': [33.9905, -81.0296],
        'Missouri': [38.9358, -92.3332], 'North Carolina': [35.9049, -79.0469], 'NC State': [35.7847, -78.6821],
        'Virginia Tech': [37.2284, -80.4234], 'Louisville': [38.2157, -85.7585], 'Pittsburgh': [40.4446, -79.9609],
        'Georgia Tech': [33.7756, -84.3963], 'Colorado': [40.0076, -105.2659], 'Arizona': [32.2287, -110.9488],
        'Arizona State': [33.4242, -111.9281], 'Stanford': [37.4275, -122.1697], 'Oregon State': [44.5595, -123.2813],
        'Washington State': [46.7313, -117.1617], 'Boise State': [43.6029, -116.1959], 'UCF': [28.6024, -81.2001],
        'Cincinnati': [39.1339, -84.5150], 'Houston': [29.7222, -95.3422], 'BYU': [40.2518, -111.6493],
        'Kansas State': [39.1974, -96.5847], 'Kansas': [38.9543, -95.2558], 'Oklahoma State': [36.1264, -97.0665],
        'West Virginia': [39.6358, -79.9559], 'Iowa State': [42.0266, -93.6465]
    }

    conn = get_db_connection()
    
    # Get latest season
    latest_season = conn.execute('SELECT MAX(season) FROM team_seasons').fetchone()[0]
    
    # Join teams and team_seasons
    query = """
        SELECT 
            t.school, t.logo_url, t.color, t.conference,
            ts.wins, ts.losses, ts.off_ppa, ts.def_ppa, ts.sp_rating, ts.fpi
        FROM teams t
        JOIN team_seasons ts ON t.id = ts.team_id
        WHERE ts.season = ?
    """
    rows = conn.execute(query, (latest_season,)).fetchall()
    conn.close()
    
    teams_data = []
    for row in rows:
        team = dict(row)
        school = team['school']
        if school in TEAM_COORDINATES:
            team['coords'] = TEAM_COORDINATES[school]
            team['name'] = school
            team['logo'] = team['logo_url']
            team['rank'] = "NR" 
            team['record'] = f"{team['wins']}-{team['losses']}"
            team['sp_plus'] = round(team['sp_rating'], 1) if team['sp_rating'] else None
            team['ppa'] = round(team['off_ppa'], 2) if team['off_ppa'] else None
            team['fpi'] = round(team['fpi'], 1) if team['fpi'] else None
            teams_data.append(team)
            
    return jsonify(teams_data)

@app.route('/api/predictions/game/<int:game_id>')
def game_prediction(game_id):
    """Get prediction data for a specific game"""
    try:
        conn = sqlite3.connect('instance/predictions.db')
        conn.row_factory = sqlite3.Row
        
        # Get game details
        game = conn.execute('SELECT * FROM upcoming_games WHERE id = ?', (game_id,)).fetchone()
        if not game:
            return jsonify({'error': 'Game not found'}), 404
            
        game = dict(game)
        
        # Calculate win probability based on FPI if available
        home_fpi = game.get('home_fpi')
        away_fpi = game.get('away_fpi')
        home_win_prob = 0.5
        
        if home_fpi is not None and away_fpi is not None:
            # Simple logistic function for win prob based on FPI diff
            diff = home_fpi - away_fpi + 2.5 # +2.5 for home field
            home_win_prob = 1 / (1 + 10**(-diff/15))
            
        # Construct response
        response = {
            'home_win_prob': home_win_prob,
            'context': {
                'homeColor': game.get('home_color'),
                'awayColor': game.get('away_color'),
                'homeLogo': game.get('home_logo'),
                'awayLogo': game.get('away_logo'),
                'marketHomeSpread': game.get('spread'),
                'marketTotal': game.get('over_under'),
                'book': game.get('line_provider'),
                'formattedSpread': game.get('formatted_spread')
            },
            'key_factors': [
                f"{game.get('home_team')} FPI: {game.get('home_fpi')}",
                f"{game.get('away_team')} FPI: {game.get('away_fpi')}",
                f"Venue: {game.get('venue')}"
            ]
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/network-graph')
def network_graph():
    """CFB Network Graph - Interactive team and conference visualization"""
    return render_template('cfb_network_graph.html')

@app.route('/network-graph-minimal')
def network_graph_minimal():
    """CFB Network Graph - Minimal version for embedding"""
    return render_template('cfb_network_graph_minimal.html')

@app.route('/team-showcase')
def team_showcase():
    """Team Showcase - Modern team explorer"""
    return render_template('team_showcase.html')

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


@app.route('/game-preview')
def game_preview():
    """Game preview page - Modern UI with team colors and wordmarks"""
    return render_template('game_detail_upcoming.html')


@app.route('/game-preview/<int:game_id>')
def game_preview_by_id(game_id):
    """Game preview page by ID - Modern UI with team colors and wordmarks"""
    try:
        # Get comprehensive game preview data
        preview_data = get_game_preview_data(game_id)
        
        if not preview_data:
            return jsonify({
                'error': 'Game not found',
                'message': f'No game found with ID {game_id}'
            }), 404
        
        # Pass data to template
        return render_template('game_detail_upcoming.html', 
                             game_data=preview_data,
                             game_id=game_id)
    except Exception as e:
        return jsonify({
            'error': 'Error loading game preview',
            'message': str(e)
        }), 500


@app.route('/game-recap/<game_id>')
def game_recap(game_id):
    """Game recap page - Full play-by-play visualization for completed games"""
    return render_template('game_recap.html', game_id=game_id)


@app.route('/api/espn/game/<game_id>')
def api_espn_game(game_id):
    """Get ESPN game data for field visualization"""
    if not espn_service:
        return jsonify({'success': False, 'error': 'ESPN service not available'}), 503
    
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    try:
        data = espn_service.get_game_for_field(game_id)
        
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Game not found or failed to fetch'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/espn/game/<game_id>/playbyplay')
def api_espn_playbyplay(game_id):
    """Get full play-by-play data from ESPN"""
    if not espn_service:
        return jsonify({'success': False, 'error': 'ESPN service not available'}), 503
    
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    try:
        data = espn_service.get_playbyplay(game_id, force_refresh)
        
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Play-by-play data not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/espn/game/<game_id>/summary')
def api_espn_summary(game_id):
    """Get raw ESPN game summary"""
    if not espn_service:
        return jsonify({'success': False, 'error': 'ESPN service not available'}), 503
    
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    try:
        data = espn_service.get_game_summary(game_id, force_refresh)
        
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Game summary not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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

@app.route('/ats_data_2025.json')
def serve_ats_data():
    """Serve ATS dataset used by the predictor"""
    frontend_dist = os.path.join('frontend', 'dist')
    if os.path.exists(os.path.join(frontend_dist, 'ats_data_2025.json')):
        return send_from_directory(frontend_dist, 'ats_data_2025.json')
    return jsonify({'error': 'ats_data_2025.json not found'}), 404

@app.route('/CFP.png')
def serve_cfp_logo():
    """Serve CFP logo used by the predictor"""
    frontend_dist = os.path.join('frontend', 'dist')
    if os.path.exists(os.path.join(frontend_dist, 'CFP.png')):
        return send_from_directory(frontend_dist, 'CFP.png')
    return jsonify({'error': 'CFP.png not found'}), 404


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
    try:
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
                COUNT(DISTINCT s.id) as total_seasons,
                ts.wins as latest_wins,
                ts.losses as latest_losses,
                ts.sp_rating as latest_sp,
                ts.talent_composite as latest_talent
            FROM teams t
            LEFT JOIN team_rankings r ON t.id = r.team_id
            LEFT JOIN team_seasons s ON t.id = s.team_id
            LEFT JOIN team_seasons ts ON t.id = ts.team_id AND ts.season = (SELECT MAX(season) FROM team_seasons)
            GROUP BY t.id
            ORDER BY t.school
        """)
        
        teams = rows_to_list(cursor.fetchall())
        conn.close()
        
        return jsonify({
            'teams': teams,
            'count': len(teams)
        })
    except FileNotFoundError as e:
        return jsonify({'error': 'Database not available', 'message': str(e)}), 503
    except Exception as e:
        return jsonify({'error': 'Failed to load teams', 'message': str(e)}), 500


@app.route('/api/stats/conference-wins')
def api_get_conference_wins():
    """Get aggregated conference wins for charts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest season
    cursor.execute("SELECT MAX(season) FROM team_seasons")
    latest_season = cursor.fetchone()[0] or 2024
    
    query = """
        SELECT 
            t.conference,
            AVG(ts.wins) as avg_wins,
            SUM(ts.wins) as total_wins,
            COUNT(t.id) as team_count,
            AVG(ts.sp_rating) as avg_sp,
            AVG(ts.talent_composite) as avg_talent,
            AVG(ts.sp_offense) as avg_offense,
            AVG(ts.sp_defense) as avg_defense,
            AVG(ts.fpi_strength_of_schedule) as avg_sos,
            AVG(ts.turnover_margin) as avg_turnover
        FROM teams t
        JOIN team_seasons ts ON t.id = ts.team_id
        WHERE ts.season = ? AND LOWER(t.classification) = 'fbs'
        GROUP BY t.conference
        ORDER BY avg_wins DESC
    """
    
    cursor.execute(query, (latest_season,))
    rows = cursor.fetchall()
    conn.close()
    
    p5_confs = ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Pac-12']
    g5_confs = ['American Athletic', 'Mid-American', 'Mountain West', 'Sun Belt', 'Conference USA']
    
    data = {
        'p5': [],
        'g5': []
    }
    
    for row in rows:
        conf = row['conference']
        stats = {
            'conference': conf,
            'avg_wins': round(row['avg_wins'], 1),
            'total_wins': row['total_wins'],
            'team_count': row['team_count'],
            'avg_sp': round(row['avg_sp'] or 0, 1),
            'avg_talent': round(row['avg_talent'] or 0, 0),
            'avg_offense': round(row['avg_offense'] or 0, 1),
            'avg_defense': round(row['avg_defense'] or 0, 1),
            'avg_sos': round(row['avg_sos'] or 0, 1),
            'avg_turnover': round(row['avg_turnover'] or 0, 1)
        }
        
        if conf in p5_confs:
            data['p5'].append(stats)
        elif conf in g5_confs:
            data['g5'].append(stats)
            
    return jsonify(data)

@app.route('/frontend/public/photos/<path:filename>')
def serve_conference_logos(filename):
    return send_from_directory('frontend/public/photos', filename)



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
                id, start_date, week, season_type, completed,
                home_team, home_abbreviation, home_logo, home_color, home_alt_color, home_record, home_rank, home_points,
                away_team, away_abbreviation, away_logo, away_color, away_alt_color, away_record, away_rank, away_points,
                line_provider, formatted_spread, spread, over_under, home_moneyline, away_moneyline,
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
                'status': 'Final' if row['completed'] else 'Scheduled',
                'statusDetail': 'Final' if row['completed'] else 'TBD',
                'home': {
                    'team': row['home_team'],
                    'abbr': row['home_abbreviation'],
                    'logo': row['home_logo'],
                    'color': row['home_color'],
                    'altColor': row['home_alt_color'],
                    'record': row['home_record'],
                    'rank': row['home_rank'],
                    'fpi': row['home_fpi'],
                    'score': row['home_points'] if row['home_points'] is not None else 0
                },
                'away': {
                    'team': row['away_team'],
                    'abbr': row['away_abbreviation'],
                    'logo': row['away_logo'],
                    'color': row['away_color'],
                    'altColor': row['away_alt_color'],
                    'record': row['away_record'],
                    'rank': row['away_rank'],
                    'fpi': row['away_fpi'],
                    'score': row['away_points'] if row['away_points'] is not None else 0
                },
                'betting': {
                    'provider': row['line_provider'],
                    'formattedSpread': row['formatted_spread'],
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


@app.route('/api/game/<game_id>', methods=['GET'])
def get_game_by_id(game_id):
    """Get detailed game information for game preview page"""
    try:
        # First check predictions.db for upcoming games
        conn = sqlite3.connect('instance/predictions.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, start_date, week, season_type, completed,
                home_team, home_abbreviation, home_logo, home_color, home_alt_color, home_record, home_rank, home_points,
                away_team, away_abbreviation, away_logo, away_color, away_alt_color, away_record, away_rank, away_points,
                spread, over_under, home_moneyline, away_moneyline,
                venue, neutral_site,
                home_fpi, away_fpi
            FROM upcoming_games
            WHERE id = ?
        """, (str(game_id),))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Game not found'}), 404
        
        # Get team wordmarks from coaches_master.db
        conn_master = sqlite3.connect('instance/coaches_master.db')
        conn_master.row_factory = sqlite3.Row
        cursor_master = conn_master.cursor()
        
        # Get home team wordmark
        cursor_master.execute("SELECT wordmark_url, mascot, conference FROM teams WHERE school = ?", (row['home_team'],))
        home_team_data = cursor_master.fetchone()
        
        # Get away team wordmark
        cursor_master.execute("SELECT wordmark_url, mascot, conference FROM teams WHERE school = ?", (row['away_team'],))
        away_team_data = cursor_master.fetchone()
        
        conn_master.close()
        
        # Build response with all data needed for game preview
        game_data = {
            'id': row['id'],
            'home': {
                'name': row['home_team'],
                'mascot': home_team_data['mascot'] if home_team_data else '',
                'conference': home_team_data['conference'] if home_team_data else '',
                'record': row['home_record'] or '0-0',
                'logo': row['home_logo'],
                'wordmark': home_team_data['wordmark_url'] if home_team_data else '',
                'primaryColor': row['home_color'] or '#333333',
                'altColor': row['home_alt_color'] or '#666666',
                'rank': row['home_rank'],
                'fpi': row['home_fpi']
            },
            'away': {
                'name': row['away_team'],
                'mascot': away_team_data['mascot'] if away_team_data else '',
                'conference': away_team_data['conference'] if away_team_data else '',
                'record': row['away_record'] or '0-0',
                'logo': row['away_logo'],
                'wordmark': away_team_data['wordmark_url'] if away_team_data else '',
                'primaryColor': row['away_color'] or '#333333',
                'altColor': row['away_alt_color'] or '#666666',
                'rank': row['away_rank'],
                'fpi': row['away_fpi']
            },
            'venue': row['venue'] or 'TBD',
            'location': '',  # Could be populated from venue lookup
            'datetime': row['start_date'],
            'broadcast': 'TBD',  # Could be populated from media info
            'spread': row['spread'],
            'overUnder': row['over_under'],
            'prediction': {
                'homeWinPct': 50,  # Could be calculated from FPI
                'homeScore': None,
                'awayScore': None
            }
        }
        
        # Calculate win probability from FPI if available
        if row['home_fpi'] and row['away_fpi']:
            fpi_diff = row['home_fpi'] - row['away_fpi']
            # Simple logistic conversion
            import math
            home_win_pct = 100 / (1 + math.exp(-fpi_diff / 10))
            game_data['prediction']['homeWinPct'] = round(home_win_pct, 1)
        
        return jsonify(game_data)
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


# =============================================================================
# GAME PREVIEW API - Comprehensive game preview data
# =============================================================================

def build_preview_from_upcoming_game(game_row, conn) -> Dict:
    """Build game preview data structure from upcoming_games table"""
    game = dict(game_row)
    
    preview_data = {
        'game': game,
        'opponent_game': {},
        'matchup': {
            'home_team': game['home_team'],
            'away_team': game['away_team'],
            'is_neutral': bool(game.get('neutral_site', 0)),
            'is_conference': bool(game.get('conference_game', 0)),
            'is_signature': False,
            'excitement_index': None,
            'season': game.get('season'),
            'week': game.get('week'),
            'venue': game.get('venue'),
            'start_date': game.get('start_date')
        },
        'teams': {
            'home': {
                'school': game['home_team'],
                'logo': game.get('home_logo'),
                'color': game.get('home_color'),
                'alt_color': game.get('home_alt_color'),
                'mascot': None,
                'record': game.get('home_record'),
                'rank': game.get('home_rank'),
                'fpi': game.get('home_fpi'),
                'wordmark': None
            },
            'away': {
                'school': game['away_team'],
                'logo': game.get('away_logo'),
                'color': game.get('away_color'),
                'alt_color': game.get('away_alt_color'),
                'mascot': None,
                'record': game.get('away_record'),
                'rank': game.get('away_rank'),
                'fpi': game.get('away_fpi'),
                'wordmark': None
            }
        },
        'betting': {
            'spread': game.get('spread'),
            'over_under': game.get('over_under'),
            'home_moneyline': game.get('home_moneyline'),
            'away_moneyline': game.get('away_moneyline')
        },
        'coaches': {},
        'head_to_head': None,
        'form': {},
        'season_analytics': {},
        'situational_stats': {},
        'rankings': {},
        'talent': {},
        'recruiting': {},
        'portal': {},
        'signature_wins': []
    }
    
    # Fetch team data (wordmarks, colors, mascots) from teams table
    cursor = conn.cursor()
    cursor.execute("SELECT wordmark_url, color, alt_color, mascot FROM teams WHERE school = ? LIMIT 1", (game['home_team'],))
    home_team_data = cursor.fetchone()
    if home_team_data:
        preview_data['teams']['home']['wordmark'] = home_team_data[0]
        # Override with teams table data if not already set
        if not preview_data['teams']['home']['color']:
            preview_data['teams']['home']['color'] = home_team_data[1]
        if not preview_data['teams']['home']['alt_color']:
            preview_data['teams']['home']['alt_color'] = home_team_data[2]
        if not preview_data['teams']['home']['mascot']:
            preview_data['teams']['home']['mascot'] = home_team_data[3]
    
    cursor.execute("SELECT wordmark_url, color, alt_color, mascot FROM teams WHERE school = ? LIMIT 1", (game['away_team'],))
    away_team_data = cursor.fetchone()
    if away_team_data:
        preview_data['teams']['away']['wordmark'] = away_team_data[0]
        # Override with teams table data if not already set
        if not preview_data['teams']['away']['color']:
            preview_data['teams']['away']['color'] = away_team_data[1]
        if not preview_data['teams']['away']['alt_color']:
            preview_data['teams']['away']['alt_color'] = away_team_data[2]
        if not preview_data['teams']['away']['mascot']:
            preview_data['teams']['away']['mascot'] = away_team_data[3]
    
    # Get current coaches for both teams
    season = game.get('season', 2024)
    
    # Find home team coach
    cursor.execute("""
        SELECT c.*, s.record, s.win_pct, s.games_coached
        FROM coaches c
        JOIN stints s ON c.id = s.coach_id
        WHERE c.current_school = ? AND s.end_year >= ?
        ORDER BY s.end_year DESC
        LIMIT 1
    """, (game['home_team'], season))
    home_coach_row = cursor.fetchone()
    if home_coach_row:
        home_coach = dict(home_coach_row)
        preview_data['coaches']['home_coach'] = home_coach
        home_coach_id = home_coach['id']
        
        # Get season analytics for home coach
        cursor.execute("SELECT * FROM season_analytics WHERE coach_id = ? AND season = ?", (home_coach_id, season))
        sa_row = cursor.fetchone()
        if sa_row:
            preview_data['season_analytics']['opponent'] = dict(sa_row)
        
        # Get situational stats for home coach
        cursor.execute("SELECT * FROM situational_stats WHERE coach_id = ? LIMIT 1", (home_coach_id,))
        sit_row = cursor.fetchone()
        if sit_row:
            preview_data['situational_stats']['opponent'] = dict(sit_row)
        
        # Get recruiting for home coach
        cursor.execute("""
            SELECT * FROM recruiting_classes 
            WHERE coach_id = ? 
            ORDER BY year DESC 
            LIMIT 2
        """, (home_coach_id,))
        preview_data['recruiting']['opponent'] = [dict(r) for r in cursor.fetchall()]
        
        # Get talent for home coach
        cursor.execute("SELECT * FROM talent_composite WHERE coach_id = ? AND year = ?", (home_coach_id, season))
        talent_row = cursor.fetchone()
        if talent_row:
            preview_data['talent']['opponent'] = dict(talent_row)
    
    # Find away team coach
    cursor.execute("""
        SELECT c.*, s.record, s.win_pct, s.games_coached
        FROM coaches c
        JOIN stints s ON c.id = s.coach_id
        WHERE c.current_school = ? AND s.end_year >= ?
        ORDER BY s.end_year DESC
        LIMIT 1
    """, (game['away_team'], season))
    away_coach_row = cursor.fetchone()
    if away_coach_row:
        away_coach = dict(away_coach_row)
        preview_data['coaches']['away_coach'] = away_coach
        away_coach_id = away_coach['id']
        
        # Get season analytics for away coach
        cursor.execute("SELECT * FROM season_analytics WHERE coach_id = ? AND season = ?", (away_coach_id, season))
        sa_row = cursor.fetchone()
        if sa_row:
            preview_data['season_analytics']['primary'] = dict(sa_row)
        
        # Get situational stats for away coach
        cursor.execute("SELECT * FROM situational_stats WHERE coach_id = ? LIMIT 1", (away_coach_id,))
        sit_row = cursor.fetchone()
        if sit_row:
            preview_data['situational_stats']['primary'] = dict(sit_row)
        
        # Get recruiting for away coach
        cursor.execute("""
            SELECT * FROM recruiting_classes 
            WHERE coach_id = ? 
            ORDER BY year DESC 
            LIMIT 2
        """, (away_coach_id,))
        preview_data['recruiting']['primary'] = [dict(r) for r in cursor.fetchall()]
        
        # Get talent for away coach
        cursor.execute("SELECT * FROM talent_composite WHERE coach_id = ? AND year = ?", (away_coach_id, season))
        talent_row = cursor.fetchone()
        if talent_row:
            preview_data['talent']['primary'] = dict(talent_row)
    
    # Get head-to-head if both coaches found
    if home_coach_row and away_coach_row:
        home_coach_name = home_coach['name']
        away_coach_name = away_coach['name']
        
        cursor.execute("""
            SELECT * FROM vs_coaches 
            WHERE (coach_id = ? AND opponent_coach = ?)
               OR (coach_id = ? AND opponent_coach = ?)
            LIMIT 1
        """, (home_coach_id, away_coach_name, away_coach_id, home_coach_name))
        h2h_row = cursor.fetchone()
        if h2h_row:
            h2h = dict(h2h_row)
            # Normalize to away vs home perspective
            if h2h['coach_id'] == home_coach_id:
                # Home coach's record vs away coach
                preview_data['head_to_head'] = {
                    'away_wins': h2h['losses'],
                    'home_wins': h2h['wins'],
                    'total_games': h2h['wins'] + h2h['losses']
                }
            else:
                # Away coach's record vs home coach
                preview_data['head_to_head'] = {
                    'away_wins': h2h['wins'],
                    'home_wins': h2h['losses'],
                    'total_games': h2h['wins'] + h2h['losses']
                }
    
    return preview_data


def get_game_preview_data(game_id: int) -> Dict:
    """
    Get comprehensive game preview data from coaches_master.db
    Returns all data needed for a full game preview experience
    Supports both internal IDs and ESPN game IDs
    Also checks upcoming_games table in predictions.db for game slider games
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Attach predictions.db to access upcoming_games
    predictions_db_path = 'instance/predictions.db'
    if os.path.exists(predictions_db_path):
        conn.execute(f"ATTACH DATABASE '{predictions_db_path}' AS predictions")
    
    try:
        # Try to find game by internal ID first
        cursor.execute("""
            SELECT g.*, 
                   c1.name as coach_name, c1.id as coach_id,
                   t1.logo_url as team_logo, t1.color as team_color, t1.alt_color as team_alt_color,
                   t1.mascot as team_mascot
            FROM games g
            LEFT JOIN coaches c1 ON g.coach_id = c1.id
            LEFT JOIN teams t1 ON g.school = t1.school
            WHERE g.id = ?
        """, (game_id,))
        
        game_row = cursor.fetchone()
        
        # If not found, try ESPN game ID in games table
        if not game_row:
            cursor.execute("""
                SELECT g.*, 
                       c1.name as coach_name, c1.id as coach_id,
                       t1.logo_url as team_logo, t1.color as team_color, t1.alt_color as team_alt_color,
                       t1.mascot as team_mascot
                FROM games g
                LEFT JOIN coaches c1 ON g.coach_id = c1.id
                LEFT JOIN teams t1 ON g.school = t1.school
                WHERE g.espn_game_id = ?
                LIMIT 1
            """, (str(game_id),))
            game_row = cursor.fetchone()
        
        # If still not found, check upcoming_games table in predictions.db
        if not game_row:
            cursor.execute("""
                SELECT * FROM predictions.upcoming_games WHERE id = ?
            """, (game_id,))
            upcoming_game = cursor.fetchone()
            
            if upcoming_game:
                # Build preview data from upcoming_games table
                preview_data = build_preview_from_upcoming_game(upcoming_game, conn)
                conn.close()
                return preview_data
        
        if not game_row:
            return None
        
        game = dict(game_row)
        
        # Get opponent coach info (find matching game)
        cursor.execute("""
            SELECT g2.*, 
                   c2.name as opponent_coach_name, c2.id as opponent_coach_id,
                   t2.logo_url as opponent_team_logo, t2.color as opponent_color, 
                   t2.alt_color as opponent_alt_color, t2.mascot as opponent_mascot
            FROM games g2
            LEFT JOIN coaches c2 ON g2.coach_id = c2.id
            LEFT JOIN teams t2 ON g2.school = t2.school
            WHERE g2.season = ? AND g2.week = ? 
              AND g2.school = ? AND g2.opponent = ?
            LIMIT 1
        """, (game['season'], game['week'], game['opponent'], game['school']))
        
        opponent_game_row = cursor.fetchone()
        opponent_game = dict(opponent_game_row) if opponent_game_row else {}
        
        coach_id = game['coach_id']
        opponent_coach_id = opponent_game.get('opponent_coach_id')
        season = game['season']
        
        # Build comprehensive payload
        preview_data = {
            'game': game,
            'opponent_game': opponent_game,
            'matchup': {
                'home_team': game['school'] if game['is_home'] else game['opponent'],
                'away_team': game['opponent'] if game['is_home'] else game['school'],
                'is_neutral': bool(game['is_neutral']),
                'is_conference': bool(game['is_conference']),
                'is_signature': bool(game['is_signature']),
                'excitement_index': game.get('excitement_index'),
                'season': season,
                'week': game['week']
            },
            'teams': {
                'home': {
                    'school': game['school'] if game['is_home'] else game['opponent'],
                    'logo': game['team_logo'] if game['is_home'] else game.get('opponent_logo'),
                    'color': game['team_color'] if game['is_home'] else opponent_game.get('opponent_color'),
                    'alt_color': game['team_alt_color'] if game['is_home'] else opponent_game.get('opponent_alt_color'),
                    'mascot': game['team_mascot'] if game['is_home'] else opponent_game.get('opponent_mascot'),
                    'wordmark': None
                },
                'away': {
                    'school': game['opponent'] if game['is_home'] else game['school'],
                    'logo': game.get('opponent_logo') if game['is_home'] else game['team_logo'],
                    'color': opponent_game.get('opponent_color') if game['is_home'] else game['team_color'],
                    'alt_color': opponent_game.get('opponent_alt_color') if game['is_home'] else game['team_alt_color'],
                    'mascot': opponent_game.get('opponent_mascot') if game['is_home'] else game['team_mascot'],
                    'wordmark': None
                }
            },
            'coaches': {},
            'head_to_head': None,
            'form': {},
            'season_analytics': {},
            'situational_stats': {},
            'rankings': {},
            'talent': {},
            'recruiting': {},
            'portal': {},
            'signature_wins': []
        }
        
        # Get coach details for both coaches
        for coach_key, cid in [('home_coach', coach_id if game['is_home'] else opponent_coach_id), 
                                ('away_coach', opponent_coach_id if game['is_home'] else coach_id)]:
            if cid:
                cursor.execute("SELECT * FROM coaches WHERE id = ?", (cid,))
                coach_row = cursor.fetchone()
                if coach_row:
                    preview_data['coaches'][coach_key] = dict(coach_row)
                    
                    # Get current stint record
                    cursor.execute("""
                        SELECT record, win_pct, games_coached, start_year, end_year
                        FROM stints 
                        WHERE coach_id = ? 
                        ORDER BY end_year DESC
                        LIMIT 1
                    """, (cid,))
                    stint_row = cursor.fetchone()
                    if stint_row:
                        preview_data['coaches'][coach_key]['current_stint'] = dict(stint_row)
                    
                    # Get last 10 games
                    cursor.execute("""
                        SELECT result, season, week, opponent, coach_score, opponent_score
                        FROM games 
                        WHERE coach_id = ? 
                        ORDER BY season DESC, week DESC 
                        LIMIT 10
                    """, (cid,))
                    preview_data['coaches'][coach_key]['last_10_games'] = [dict(r) for r in cursor.fetchall()]
        
        # Head-to-head record (if both coaches available)
        if coach_id and opponent_coach_id:
            cursor.execute("""
                SELECT * FROM vs_coaches 
                WHERE coach_id = ? AND opponent_coach IN (
                    SELECT name FROM coaches WHERE id = ?
                )
                LIMIT 1
            """, (coach_id, opponent_coach_id))
            h2h_row = cursor.fetchone()
            if h2h_row:
                preview_data['head_to_head'] = dict(h2h_row)
        
        # Form - Last 5 games overall and vs this opponent (for primary coach)
        if coach_id:
            cursor.execute("""
                SELECT result, season, week, opponent, coach_score, opponent_score, 
                       opponent_sp_overall, excitement_index
                FROM games 
                WHERE coach_id = ? 
                ORDER BY season DESC, week DESC 
                LIMIT 5
            """, (coach_id,))
            preview_data['form']['last_5_overall'] = [dict(r) for r in cursor.fetchall()]
            
            cursor.execute("""
                SELECT result, season, week, opponent, coach_score, opponent_score,
                       opponent_sp_overall, excitement_index
                FROM games 
                WHERE coach_id = ? AND opponent = ?
                ORDER BY season DESC, week DESC 
                LIMIT 5
            """, (coach_id, game['opponent']))
            preview_data['form']['last_5_vs_opponent'] = [dict(r) for r in cursor.fetchall()]
        
        # Season analytics (for primary coach's season)
        if coach_id:
            cursor.execute("""
                SELECT * FROM season_analytics 
                WHERE coach_id = ? AND season = ?
            """, (coach_id, season))
            analytics_row = cursor.fetchone()
            preview_data['season_analytics']['primary'] = dict(analytics_row) if analytics_row else None
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM season_analytics 
                WHERE coach_id = ? AND season = ?
            """, (opponent_coach_id, season))
            analytics_row = cursor.fetchone()
            preview_data['season_analytics']['opponent'] = dict(analytics_row) if analytics_row else None
        
        # Situational stats (per coach, not per season)
        if coach_id:
            cursor.execute("""
                SELECT * FROM situational_stats 
                WHERE coach_id = ?
                ORDER BY id DESC
                LIMIT 1
            """, (coach_id,))
            sit_row = cursor.fetchone()
            preview_data['situational_stats']['primary'] = dict(sit_row) if sit_row else None
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM situational_stats 
                WHERE coach_id = ?
                ORDER BY id DESC
                LIMIT 1
            """, (opponent_coach_id,))
            sit_row = cursor.fetchone()
            preview_data['situational_stats']['opponent'] = dict(sit_row) if sit_row else None
        
        # Rankings trends (last 4 weeks)
        cursor.execute("""
            SELECT * FROM rankings 
            WHERE coach_id = ? AND season = ? AND week >= ?
            ORDER BY week DESC
            LIMIT 4
        """, (coach_id, season, max(1, game['week'] - 3)))
        preview_data['rankings']['primary_trend'] = [dict(r) for r in cursor.fetchall()]
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM rankings 
                WHERE coach_id = ? AND season = ? AND week >= ?
                ORDER BY week DESC
                LIMIT 4
            """, (opponent_coach_id, season, max(1, game['week'] - 3)))
            preview_data['rankings']['opponent_trend'] = [dict(r) for r in cursor.fetchall()]
        
        # Talent composite
        if coach_id:
            cursor.execute("""
                SELECT * FROM talent_composite 
                WHERE coach_id = ? AND year = ?
            """, (coach_id, season))
            talent_row = cursor.fetchone()
            preview_data['talent']['primary'] = dict(talent_row) if talent_row else None
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM talent_composite 
                WHERE coach_id = ? AND year = ?
            """, (opponent_coach_id, season))
            talent_row = cursor.fetchone()
            preview_data['talent']['opponent'] = dict(talent_row) if talent_row else None
        
        # Recruiting classes (last 2 years)
        if coach_id:
            cursor.execute("""
                SELECT * FROM recruiting_classes 
                WHERE coach_id = ? AND year >= ?
                ORDER BY year DESC
                LIMIT 2
            """, (coach_id, season - 1))
            preview_data['recruiting']['primary'] = [dict(r) for r in cursor.fetchall()]
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM recruiting_classes 
                WHERE coach_id = ? AND year >= ?
                ORDER BY year DESC
                LIMIT 2
            """, (opponent_coach_id, season - 1))
            preview_data['recruiting']['opponent'] = [dict(r) for r in cursor.fetchall()]
        
        # Transfer portal
        if coach_id:
            cursor.execute("""
                SELECT * FROM transfer_portal 
                WHERE coach_id = ? AND season = ?
            """, (coach_id, season))
            portal_row = cursor.fetchone()
            preview_data['portal']['primary'] = dict(portal_row) if portal_row else None
        
        if opponent_coach_id:
            cursor.execute("""
                SELECT * FROM transfer_portal 
                WHERE coach_id = ? AND season = ?
            """, (opponent_coach_id, season))
            portal_row = cursor.fetchone()
            preview_data['portal']['opponent'] = dict(portal_row) if portal_row else None
        
        # Signature wins (from this season)
        if coach_id:
            cursor.execute("""
                SELECT * FROM games 
                WHERE coach_id = ? AND season = ? AND is_signature = 1
                ORDER BY week DESC
                LIMIT 3
            """, (coach_id, season))
            preview_data['signature_wins'] = [dict(r) for r in cursor.fetchall()]
        
        # Fetch wordmarks from teams table for both home and away
        home_school = preview_data['teams']['home']['school']
        away_school = preview_data['teams']['away']['school']
        
        cursor.execute("SELECT wordmark_url FROM teams WHERE school = ? LIMIT 1", (home_school,))
        home_wordmark = cursor.fetchone()
        if home_wordmark:
            preview_data['teams']['home']['wordmark'] = home_wordmark[0]
        
        cursor.execute("SELECT wordmark_url FROM teams WHERE school = ? LIMIT 1", (away_school,))
        away_wordmark = cursor.fetchone()
        if away_wordmark:
            preview_data['teams']['away']['wordmark'] = away_wordmark[0]
        
        conn.close()
        return preview_data
        
    except Exception as e:
        conn.close()
        raise e


@app.route('/api/game-preview/<int:game_id>')
def api_game_preview(game_id):
    """
    API endpoint for comprehensive game preview data
    Returns all data needed for game preview template
    """
    try:
        data = get_game_preview_data(game_id)
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Game not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check database exists - but don't exit, just warn
    if not Path(DB_PATH).exists():
        print("❌ Database not found at:", DB_PATH)
        print("⚠️  App will start but database routes may not work")
        print("Run setup_master_db.py first to create the database")
    else:
        print(f"✅ Database found: {DB_PATH}")
    
    print("\n" + "=" * 80)
    print("🌐 UNIVERSAL COACH DATABASE API")
    print("=" * 80)
    print(f"📁 Database: {DB_PATH}")
    port = int(os.environ.get('PORT', 5555))
    print(f"🌍 Server: http://localhost:{port}")
    print(f"📊 API Docs: http://localhost:{port}/api/stats")
    print("=" * 80 + "\n")
    
    app.run(debug=os.environ.get('FLASK_ENV') != 'production', host='0.0.0.0', port=port)
