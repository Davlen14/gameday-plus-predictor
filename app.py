from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import asyncio
import os
import json
from graphqlpredictor import LightningPredictor
from run import format_prediction_output

app = Flask(__name__)
CORS(app)  # Enable CORS for iOS app

def get_team_id(team_name):
    """Convert team name to team ID using fbs.json data"""
    if isinstance(team_name, int):
        return team_name  # Already an ID
    
    team_name_lower = team_name.lower().strip()
    
    # Load teams from fbs.json
    try:
        with open('fbs.json', 'r') as f:
            teams_data = json.load(f)
        
        # First pass: Look for exact matches
        for team in teams_data:
            # Check exact school name match
            if team['school'].lower() == team_name_lower:
                return team['id']
            # Check exact mascot name match
            if team['mascot'].lower() == team_name_lower:
                return team['id']
        
        # Second pass: Look for exact word matches
        for team in teams_data:
            school_words = team['school'].lower().split()
            if team_name_lower in school_words:
                return team['id']
        
        # Third pass: Look for partial matches (most permissive)
        for team in teams_data:
            if team_name_lower in team['school'].lower():
                return team['id']
            
    except Exception as e:
        print(f"Error loading fbs.json: {e}")
        raise ValueError(f"Could not load team data from fbs.json: {e}")
    
    # Generate helpful error message with available teams
    try:
        available_teams = [team['school'] for team in sorted(teams_data, key=lambda x: x['school'])]
        raise ValueError(f"Team '{team_name}' not found. Try using the full school name like 'Washington State' or 'Ole Miss'. Available teams: {', '.join(available_teams[:20])}... (see /teams endpoint for full list)")
    except:
        raise ValueError(f"Team '{team_name}' not found. Please use the /teams endpoint to see all available teams.")

def extract_team_season_games(details, games_key, team_id_key, team_name, team_data):
    """Extract and format season game records for a team"""
    season_games = details.get(games_key, []) if details else []
    team_id = details.get(team_id_key) if details else None
    
    if not season_games or not team_id:
        return None
    
    wins = 0
    losses = 0
    games = []
    
    for game in season_games:
        home_points = game.get('homePoints')
        away_points = game.get('awayPoints')
        
        if home_points is not None and away_points is not None:
            if game.get('homeTeamId') == team_id:
                result = "W" if home_points > away_points else "L"
                if home_points > away_points:
                    wins += 1
                else:
                    losses += 1
                games.append({
                    "week": game['week'],
                    "opponent": game.get('awayTeam', 'Unknown'),
                    "result": result,
                    "score": f"{home_points}-{away_points}",
                    "isAway": False,
                    "opponentLogo": f"http://a.espncdn.com/i/teamlogos/ncaa/500/{game.get('awayTeamId', 0)}.png"
                })
            elif game.get('awayTeamId') == team_id:
                result = "W" if away_points > home_points else "L"
                if away_points > home_points:
                    wins += 1
                else:
                    losses += 1
                games.append({
                    "week": game['week'],
                    "opponent": game.get('homeTeam', 'Unknown'),
                    "result": result,
                    "score": f"{away_points}-{home_points}",
                    "isAway": True,
                    "opponentLogo": f"http://a.espncdn.com/i/teamlogos/ncaa/500/{game.get('homeTeamId', 0)}.png"
                })
    
    # Return last 6 games
    return {
        "team": team_name,
        "record": f"{wins}-{losses}",
        "logo": team_data.get('logo_url', 'N/A'),
        "primary_color": team_data.get('primary_color', '#000000'),
        "games": games[-6:]  # Last 6 games
    }

def calculate_base_data_quality(prediction, details):
    """
    Calculate base data quality score (70-95 range) based on available data completeness
    Factors: market lines availability, player data completeness, recent game data
    """
    score = 70  # Base score
    
    # Market data availability (+8 points max)
    market_spread = getattr(prediction, 'market_spread', None)
    market_total = getattr(prediction, 'market_total', None)
    market_lines = details.get('market_lines', [])
    
    if market_spread and market_total:
        score += 4  # Both spread and total available
    elif market_spread or market_total:
        score += 2  # One market line available
        
    if len(market_lines) >= 3:
        score += 4  # Multiple sportsbooks
    elif len(market_lines) >= 1:
        score += 2  # At least one sportsbook
    
    # Player data completeness (+7 points max)
    player_analysis = details.get('enhanced_player_analysis', {})
    home_players = player_analysis.get('home', {})
    away_players = player_analysis.get('away', {})
    
    home_qb_count = len(home_players.get('quarterbacks', []))
    away_qb_count = len(away_players.get('quarterbacks', []))
    home_wr_count = len(home_players.get('receivers', []))
    away_wr_count = len(away_players.get('receivers', []))
    
    if home_qb_count > 0 and away_qb_count > 0:
        score += 3  # QB data for both teams
    if home_wr_count >= 3 and away_wr_count >= 3:
        score += 4  # Good receiver data coverage
    
    # Advanced metrics completeness (+10 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    # Check for key EPA metrics
    if home_metrics.get('epa') and away_metrics.get('epa'):
        score += 3
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        score += 2
    if home_metrics.get('explosiveness') and away_metrics.get('explosiveness'):
        score += 2
    
    # Weather data availability (+3 points max)
    weather = details.get('weather', {})
    if weather.get('temperature') is not None:
        score += 1
    if weather.get('wind_speed') is not None:
        score += 1
    if weather.get('precipitation') is not None:
        score += 1
    
    return min(95, max(70, score))

def calculate_consistency_factor(prediction, details):
    """
    Calculate consistency factor (-5 to +10 range) based on prediction model consistency
    Factors: model stability, data variance, historical accuracy patterns
    """
    factor = 0  # Base factor
    
    # Market consensus alignment (+5 points max)
    model_spread = prediction.predicted_spread
    market_spread = getattr(prediction, 'market_spread', None)
    
    if market_spread is not None:
        spread_diff = abs(model_spread - market_spread)
        if spread_diff <= 1.5:
            factor += 5  # Very close to market consensus
        elif spread_diff <= 3.0:
            factor += 3  # Reasonable alignment
        elif spread_diff <= 5.0:
            factor += 1  # Some alignment
        else:
            factor -= 2  # Significant divergence from market
    
    # EPA differential consistency (+3 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_diff = home_metrics['epa'] - away_metrics['epa']
        # Check if EPA differential supports the spread prediction
        if (model_spread > 0 and epa_diff > 0) or (model_spread < 0 and epa_diff < 0):
            factor += 3  # EPA supports prediction direction
        elif abs(epa_diff) < 0.1:  # Very close EPA values
            factor += 1
    
    # Talent rating consistency (+2 points max)
    ratings = details.get('ratings', {})
    home_talent = ratings.get('home', {}).get('talent', 0)
    away_talent = ratings.get('away', {}).get('talent', 0)
    
    if home_talent and away_talent:
        talent_diff = home_talent - away_talent
        spread_direction = 1 if model_spread > 0 else -1
        talent_direction = 1 if talent_diff > 0 else -1
        
        if spread_direction == talent_direction:
            factor += 2  # Talent ratings support prediction
    
    # Data variance penalty (subtract points for high variance)
    advanced_metrics = details.get('advanced_metrics', {})
    if isinstance(advanced_metrics, dict):
        # Check for unusual metric combinations that might indicate uncertainty
        consistency_metrics = advanced_metrics.get('consistency', {})
        if consistency_metrics.get('high_variance_flag', False):
            factor -= 3
    
    return max(-5, min(10, factor))

def calculate_differential_strength(prediction, details):
    """
    Calculate differential strength (0 to +15 range) based on statistical differentials
    Factors: EPA differentials, talent gaps, market consensus alignment
    """
    strength = 0  # Base strength
    
    # EPA differential strength (+6 points max)
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_diff = abs(home_metrics['epa'] - away_metrics['epa'])
        if epa_diff >= 0.4:
            strength += 6  # Very strong EPA differential
        elif epa_diff >= 0.2:
            strength += 4  # Strong EPA differential
        elif epa_diff >= 0.1:
            strength += 2  # Moderate EPA differential
    
    # Talent gap strength (+4 points max)
    ratings = details.get('ratings', {})
    home_talent = ratings.get('home', {}).get('talent', 0)
    away_talent = ratings.get('away', {}).get('talent', 0)
    
    if home_talent and away_talent:
        talent_gap = abs(home_talent - away_talent)
        if talent_gap >= 15:
            strength += 4  # Large talent gap
        elif talent_gap >= 8:
            strength += 3  # Significant talent gap
        elif talent_gap >= 4:
            strength += 1  # Moderate talent gap
    
    # Success rate differential (+3 points max)
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        success_diff = abs(home_metrics['success_rate'] - away_metrics['success_rate'])
        if success_diff >= 8:
            strength += 3  # Large success rate gap
        elif success_diff >= 4:
            strength += 2  # Significant success rate gap
        elif success_diff >= 2:
            strength += 1  # Moderate success rate gap
    
    # Multiple indicators agreement (+2 points max)
    agreement_count = 0
    model_spread = prediction.predicted_spread
    
    # Check if EPA, talent, and success rate all point in same direction
    if home_metrics.get('epa') and away_metrics.get('epa'):
        epa_favors_home = home_metrics['epa'] > away_metrics['epa']
        if (model_spread > 0) == epa_favors_home:
            agreement_count += 1
    
    if home_talent and away_talent:
        talent_favors_home = home_talent > away_talent
        if (model_spread > 0) == talent_favors_home:
            agreement_count += 1
    
    if home_metrics.get('success_rate') and away_metrics.get('success_rate'):
        success_favors_home = home_metrics['success_rate'] > away_metrics['success_rate']
        if (model_spread > 0) == success_favors_home:
            agreement_count += 1
    
    if agreement_count >= 3:
        strength += 2  # All indicators agree
    elif agreement_count >= 2:
        strength += 1  # Most indicators agree
    
    return min(15, max(0, strength))

def format_prediction_for_api(prediction, home_team_data, away_team_data):
    """
    Bridge function that captures the output from run.py's format_prediction_output 
    and formats it for API consumption with both text and structured JSON
    """
    import io
    import sys
    from contextlib import redirect_stdout
    
    # Capture the formatted output from run.py with larger buffer
    captured_output = io.StringIO()
    
    # Ensure we capture ALL output by temporarily redirecting stdout
    original_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        format_prediction_output(prediction, home_team_data, away_team_data)
    finally:
        sys.stdout = original_stdout
    
    formatted_analysis = captured_output.getvalue()
    
    # Debug: Check if we got all 18 sections
    section_count = formatted_analysis.count('[1') + formatted_analysis.count('[2')
    print(f"🔍 DEBUG: Captured {section_count} sections in formatted analysis")
    print(f"🔍 DEBUG: Total analysis length: {len(formatted_analysis)} characters")
    
    # If we don't have enough sections, there might be an issue
    if section_count < 18:
        print(f"⚠️  WARNING: Only {section_count} sections captured, expected 18")
    else:
        print(f"✅ SUCCESS: All {section_count} sections captured!")
    
    # Also build a structured UI components object for the React frontend
    # This uses the actual prediction data, not hardcoded values
    details = getattr(prediction, 'detailed_analysis', {}) or {}
    
    def get_val(d, *keys, default=0):
        """Helper to safely get nested values"""
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key, {})
            else:
                return default
        return d if d != {} else default
    
    # Load AP Poll data for rankings
    home_ranking = None
    away_ranking = None
    try:
        with open('frontend/src/data/ap.json', 'r') as f:
            ap_data = json.load(f)
        
        current_week = 'week_8'
        if current_week in ap_data:
            for rank_entry in ap_data[current_week]['ranks']:
                if rank_entry['school'] == prediction.home_team:
                    home_ranking = rank_entry
                elif rank_entry['school'] == prediction.away_team:
                    away_ranking = rank_entry
    except Exception as e:
        print(f"Note: AP Poll data not available: {e}")
    
    # Get season records
    season_records = get_val(details, 'season_records', default={})
    home_record = season_records.get('home', {'wins': 0, 'losses': 0})
    away_record = season_records.get('away', {'wins': 0, 'losses': 0})
    
    # Calculate win probabilities
    away_win_prob = (1 - prediction.home_win_prob) * 100
    home_win_prob = prediction.home_win_prob * 100
    
    # Calculate scores
    market_spread = getattr(prediction, 'market_spread', 0) or 0
    market_total = getattr(prediction, 'market_total', 0) or 0
    
    if prediction.predicted_spread > 0:
        home_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
        away_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
    else:
        home_score = round((prediction.predicted_total + abs(prediction.predicted_spread)) / 2)
        away_score = round((prediction.predicted_total - abs(prediction.predicted_spread)) / 2)
    
    # Get weather data
    weather_data = get_val(details, 'weather', default={})
    print(f"🔍 DEBUG: Flask weather_data keys: {list(weather_data.keys()) if weather_data else 'None'}")
    print(f"🔍 DEBUG: Flask weather_data values: {weather_data}")
    
    # Build UI components structure with REAL data
    ui_components = {
        "team_selector": {
            "away_team": {
                "id": away_team_data.get('id', 'N/A'),
                "name": prediction.away_team,
                "logo": away_team_data.get('logo_url', 'N/A'),
                "primary_color": away_team_data.get('primary_color', '#000000'),
                "alt_color": away_team_data.get('alt_color', '#ffffff')
            },
            "home_team": {
                "id": home_team_data.get('id', 'N/A'),
                "name": prediction.home_team,
                "logo": home_team_data.get('logo_url', 'N/A'),
                "primary_color": home_team_data.get('primary_color', '#000000'),
                "alt_color": home_team_data.get('alt_color', '#ffffff')
            }
        },
        "header": {
            "game_info": {
                "date": getattr(prediction, 'game_date', "October 19, 2025"),
                "time": getattr(prediction, 'game_time', "7:30 PM ET"),
                "network": prediction.media_info[0].get('name', 'TBD') if prediction.media_info else 'TBD',
                "excitement_index": 4.2
            },
            "teams": {
                "away": {
                    "rank": away_ranking['rank'] if away_ranking else None,
                    "name": prediction.away_team,
                    "record": f"{away_record.get('wins', 0)}-{away_record.get('losses', 0)}",
                    "logo": away_team_data.get('logo_url', 'N/A')
                },
                "home": {
                    "rank": home_ranking['rank'] if home_ranking else None,
                    "name": prediction.home_team,
                    "record": f"{home_record.get('wins', 0)}-{home_record.get('losses', 0)}",
                    "logo": home_team_data.get('logo_url', 'N/A')
                }
            }
        },
        "prediction_cards": {
            "win_probability": {
                "home_team_prob": home_win_prob,
                "away_team_prob": away_win_prob,
                "favored_team": prediction.home_team if home_win_prob > away_win_prob else prediction.away_team
            },
            "predicted_spread": {
                "model_spread": prediction.predicted_spread,
                "model_spread_display": f"{prediction.home_team} {prediction.predicted_spread:+.1f}",
                "market_spread": market_spread,
                "edge": abs(prediction.predicted_spread - market_spread) if market_spread else 0
            },
            "predicted_total": {
                "model_total": prediction.predicted_total,
                "market_total": market_total,
                "edge": abs(prediction.predicted_total - market_total) if market_total else 0
            }
        },
        "confidence": {
            "overall_confidence": prediction.confidence * 100,
            "breakdown": {
                "base_data_quality": calculate_base_data_quality(prediction, details),
                "consistency_factor": calculate_consistency_factor(prediction, details),
                "differential_strength": calculate_differential_strength(prediction, details),
                "trend_factor": 5,  # Keep existing trend factor for now
                "weather_calendar": 5  # Keep existing weather/calendar factor for now
            },
            "calibration": {
                "raw_probability": home_win_prob,
                "calibrated_probability": home_win_prob,
                "adjustment": 0.0
            }
        },
        "contextual_analysis": {
            "weather": {
                "temperature": weather_data.get('temperature'),
                "wind_speed": weather_data.get('wind_speed'), 
                "precipitation": weather_data.get('precipitation'),
                "humidity": weather_data.get('humidity'),
                "dewpoint": weather_data.get('dewpoint'),
                "pressure": weather_data.get('pressure'),
                "snowfall": weather_data.get('snowfall'),
                "wind_direction": weather_data.get('wind_direction'),
                "wind_gust": weather_data.get('wind_gust'),
                "weather_condition_code": weather_data.get('weather_condition_code'),
                "weather_factor": weather_data.get('weather_factor', 0.0)
            },
            "rankings": {
                "away_rank": away_ranking['rank'] if away_ranking else None,
                "home_rank": home_ranking['rank'] if home_ranking else None
            }
        },
        "season_records": {
            "away": extract_team_season_games(details, 'awaySeasonGames', 'awayTeamId', prediction.away_team, away_team_data),
            "home": extract_team_season_games(details, 'homeSeasonGames', 'homeTeamId', prediction.home_team, home_team_data)
        },
        "final_prediction": {
            "predicted_score": {
                "away_score": away_score,
                "home_score": home_score,
                "total": prediction.predicted_total
            },
            "key_factors": prediction.key_factors[:5],
            "confidence": prediction.confidence * 100
        },
        "detailed_analysis": {
            "enhanced_player_analysis": details.get('enhanced_player_analysis', {})
        }
    }
    
    return {
        "formatted_analysis": formatted_analysis,
        "ui_components": ui_components
    }

# Predictor will be initialized lazily within the endpoint
api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
predictor = None

def get_predictor():
    """Initializes and returns a single instance of the predictor."""
    global predictor
    if predictor is None:
        predictor = LightningPredictor(api_key)
    return predictor

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Gameday GraphQL Predictor",
        "version": "1.0.0",
        "accepts": "team names or IDs"
    })

@app.route('/test.html', methods=['GET'])
def serve_test_page():
    return send_file('test.html')

@app.route('/debug', methods=['GET'])
def serve_debug_page():
    return send_file('debug_frontend_data.html')

@app.route('/test.js', methods=['GET'])
def serve_test_js():
    return send_file('test.js', mimetype='application/javascript')

@app.route('/test_report.html', methods=['GET'])
def serve_test_report_page():
    return send_file('test_report.html')

@app.route('/test_report.js', methods=['GET'])
def serve_test_report_js():
    return send_file('test_report.js', mimetype='application/javascript')

@app.route('/predict', methods=['POST'])
def predict_game():
    try:
        data = request.get_json()
        
        if not data or 'home_team' not in data or 'away_team' not in data:
            return jsonify({
                "error": "Missing required fields: home_team, away_team"
            }), 400
        
        # Convert team names to IDs
        try:
            home_team_id = get_team_id(data['home_team'])
            away_team_id = get_team_id(data['away_team'])
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400
        
        # Print the same detailed analysis as run.py to terminal
        print(f"🔍 Looking up teams: {data['home_team']} (home) vs {data['away_team']} (away)")
        print(f"✅ {data['home_team']} (ID: {home_team_id})")
        print(f"✅ {data['away_team']} (ID: {away_team_id})")
        print(f"\nPredicting game: {data['home_team']} vs {data['away_team']}")
        
        # Run async prediction
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            predictor = get_predictor()
            prediction = loop.run_until_complete(
                predictor.predict_game(home_team_id, away_team_id)
            )
            
            # Print the same detailed output as run.py to terminal
            print(f"\n🏈 {prediction.away_team} @ {prediction.home_team}")
            print(f"🎯 Home Win Probability: {prediction.home_win_prob:.1%}")
            print(f"📊 Predicted Spread: {prediction.home_team} {prediction.predicted_spread:+.1f}")
            print(f"🔢 Predicted Total: {prediction.predicted_total:.1f}")
            print(f"🎪 Confidence: {prediction.confidence:.1%}")
            
            # Display value picks if available
            if hasattr(prediction, 'value_spread_pick') and prediction.value_spread_pick:
                print(f"\n💰 VALUE PICK (Spread): {prediction.value_spread_pick} ({getattr(prediction, 'spread_edge', 0):.1f}-point edge)")
            if hasattr(prediction, 'value_total_pick') and prediction.value_total_pick:
                print(f"💰 VALUE PICK (Total): {prediction.value_total_pick} ({getattr(prediction, 'total_edge', 0):.1f}-point edge)")
            
            print(f"\n🔑 Key Factors: {', '.join(getattr(prediction, 'key_factors', []))}")
            
            # Get team data for comprehensive formatting
            try:
                import json
                with open('fbs.json', 'r') as f:
                    teams_list = json.load(f)
                
                # Find team data for both teams
                home_team_fbs = next((team for team in teams_list if team['id'] == home_team_id), None)
                away_team_fbs = next((team for team in teams_list if team['id'] == away_team_id), None)
                
                home_team_data = {
                    'id': home_team_id,
                    'name': home_team_fbs['school'] if home_team_fbs else prediction.home_team,
                    'logo_url': home_team_fbs['logos'][0] if home_team_fbs and home_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
                    'logo_dark_url': home_team_fbs['logos'][1] if home_team_fbs and len(home_team_fbs['logos']) > 1 else f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
                    'primary_color': home_team_fbs['primary_color'] if home_team_fbs else '#000000',
                    'alt_color': home_team_fbs['alt_color'] if home_team_fbs else '#ffffff'
                }
                
                away_team_data = {
                    'id': away_team_id,
                    'name': away_team_fbs['school'] if away_team_fbs else prediction.away_team,
                    'logo_url': away_team_fbs['logos'][0] if away_team_fbs and away_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
                    'logo_dark_url': away_team_fbs['logos'][1] if away_team_fbs and len(away_team_fbs['logos']) > 1 else f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
                    'primary_color': away_team_fbs['primary_color'] if away_team_fbs else '#000000',
                    'alt_color': away_team_fbs['alt_color'] if away_team_fbs else '#ffffff'
                }
                
            except Exception as e:
                print(f"Warning: Could not load team data from fbs.json: {e}")
                # Create fallback team data
                home_team_data = {
                    'id': home_team_id,
                    'name': prediction.home_team,
                    'logo_url': f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
                    'logo_dark_url': f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
                    'primary_color': '#000000',
                    'alt_color': '#ffffff'
                }
                away_team_data = {
                    'id': away_team_id,
                    'name': prediction.away_team,
                    'logo_url': f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
                    'logo_dark_url': f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
                    'primary_color': '#000000',
                    'alt_color': '#ffffff'
                }
            
            print(f"🎨 TEAM LOGOS:")
            print(f"   🏠 {prediction.home_team}: {home_team_data['logo_url']} (light), {home_team_data['logo_dark_url']} (dark)")
            print(f"   ✈️  {prediction.away_team}: {away_team_data['logo_url']} (light), {away_team_data['logo_dark_url']} (dark)")
            
            # Generate comprehensive analysis using the working logic from run.py
            print("\n" + "=" * 80)
            print("🎯 GENERATING COMPREHENSIVE 18-SECTION ANALYSIS...")
            print("=" * 80)
            
            comprehensive_analysis = format_prediction_for_api(prediction, home_team_data, away_team_data)
            
            # The formatted analysis is already printed by format_prediction_output
            
            print("\n" + "=" * 80)
            print("🎯 ANALYSIS COMPLETE - RETURNING STRUCTURED JSON")
            print("=" * 80)
            
            # Return the comprehensive analysis from formatter
            return jsonify({
                "success": True,
                **comprehensive_analysis
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route('/predict/<home_team>/<away_team>', methods=['GET'])
def predict_game_get(home_team, away_team):
    """GET endpoint for easy testing - accepts team names or IDs"""
    try:
        # Convert team names to IDs
        try:
            home_team_id = get_team_id(home_team)
            away_team_id = get_team_id(away_team)
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400
        # Run async prediction
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            predictor = get_predictor()
            prediction = loop.run_until_complete(
                predictor.predict_game(home_team_id, away_team_id)
            )
            
            return jsonify({
                "success": True,
                "prediction": {
                    "home_team": prediction.home_team,
                    "away_team": prediction.away_team,
                    "predicted_winner": prediction.predicted_winner,
                    "home_score": prediction.home_score,
                    "away_score": prediction.away_score,
                    "spread": prediction.spread,
                    "total": prediction.total,
                    "home_win_probability": prediction.home_win_probability,
                    "confidence": prediction.confidence,
                    "key_factors": prediction.key_factors
                }
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route('/predict-detailed/<home_team>/<away_team>', methods=['GET'])
def predict_game_detailed(home_team, away_team):
    """GET endpoint that provides the same detailed output as run.py"""
    try:
        # Convert team names to IDs
        try:
            home_team_id = get_team_id(home_team)
            away_team_id = get_team_id(away_team)
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400
        
        # Get team data for logos
        teams_data = {}
        try:
            import json
            
            # Load teams from local fbs.json file
            with open('fbs.json', 'r') as f:
                teams_list = json.load(f)
            
            # Create lookup dictionary
            for team in teams_list:
                teams_data[team['id']] = {
                    'id': team['id'],
                    'name': team['school'],
                    'logo': team['logos'][0]  # Use working ESPN CDN logo
                }
            
        except Exception as e:
            print(f"Warning: Could not fetch team logos: {e}")
        
        print(f"🔍 Looking up teams: {home_team} (home) vs {away_team} (away)")
        if home_team_id in teams_data:
            print(f"✅ {teams_data[home_team_id]['name']} (ID: {home_team_id}) - Logo: {teams_data[home_team_id]['logo']}")
        if away_team_id in teams_data:
            print(f"✅ {teams_data[away_team_id]['name']} (ID: {away_team_id}) - Logo: {teams_data[away_team_id]['logo']}")
        
        print(f"\nPredicting game: {home_team} vs {away_team}")
        
        # Run async prediction with detailed output (same as run.py)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            predictor = get_predictor()
            prediction = loop.run_until_complete(
                predictor.predict_game(home_team_id, away_team_id)
            )
            
            # Print the same detailed output as run.py
            print(f"\n🏈 {prediction.away_team} @ {prediction.home_team}")
            print(f"🎯 Home Win Probability: {prediction.home_win_prob:.1%}")
            print(f"📊 Predicted Spread: {prediction.home_team} {prediction.predicted_spread:+.1f}")
            print(f"🔢 Predicted Total: {prediction.predicted_total:.1f}")
            print(f"🎪 Confidence: {prediction.confidence:.1%}")
            print(f"🔑 Key Factors: {', '.join(prediction.key_factors)}")
            
            # Display team logos
            if home_team_id in teams_data and away_team_id in teams_data:
                print(f"\n🏈 Team Logos (for future UI integration):")
                print(f"🏠 {teams_data[home_team_id]['name']}: {teams_data[home_team_id]['logo']}")
                print(f"✈️  {teams_data[away_team_id]['name']}: {teams_data[away_team_id]['logo']}")
            
            # Return comprehensive JSON response
            response_data = {
                "success": True,
                "prediction": {
                    "home_team": prediction.home_team,
                    "away_team": prediction.away_team,
                    "predicted_winner": prediction.predicted_winner,
                    "home_score": prediction.home_score,
                    "away_score": prediction.away_score,
                    "spread": prediction.predicted_spread,
                    "total": prediction.predicted_total,
                    "home_win_probability": prediction.home_win_prob,
                    "confidence": prediction.confidence,
                    "key_factors": prediction.key_factors
                }
            }
            
            # Add team logos if available
            if home_team_id in teams_data and away_team_id in teams_data:
                response_data["team_data"] = {
                    "home_team": teams_data[home_team_id],
                    "away_team": teams_data[away_team_id]
                }
            
            return jsonify(response_data)
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route('/teams', methods=['GET'])
def get_teams():
    """Get list of FBS teams for dropdowns from local fbs.json file"""
    try:
        import json
        
        # Load teams from local fbs.json file
        with open('fbs.json', 'r') as f:
            teams_data = json.load(f)
        
        # Sort teams by school name and format for frontend
        sorted_teams = sorted(teams_data, key=lambda x: x['school'])
        formatted_teams = []
        
        for team in sorted_teams:
            formatted_teams.append({
                'id': team['id'], 
                'name': team['school'],
                'logo': team['logos'][0],  # Regular logo (light mode)
                'logo_dark': team['logos'][1],  # Dark logo (dark mode)
                'mascot': team['mascot'],
                'conference': team['conference'],
                'primary_color': team['primary_color'],
                'alt_color': team['alt_color']
            })
        
        return jsonify({'success': True, 'teams': formatted_teams})
            
    except Exception as e:
        return jsonify({'error': f'Failed to load teams: {str(e)}'}), 500

# Serve React Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serve the React frontend"""
    try:
        # Serve static files
        if path and os.path.exists(os.path.join('frontend/dist', path)):
            return send_from_directory('frontend/dist', path)
        else:
            # Serve index.html for React Router
            return send_from_directory('frontend/dist', 'index.html')
    except Exception as e:
        return jsonify({'error': 'Frontend not available', 'details': str(e)}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))  # Changed from 5001 to 5002
    app.run(host='0.0.0.0', port=port)