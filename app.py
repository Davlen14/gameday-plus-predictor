from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import asyncio
import os
import json
from graphqlpredictor import LightningPredictor
from run import format_prediction_output
from prediction_validator import PredictionValidator, apply_prediction_fixes
from betting_lines_manager import betting_manager
from game_media_service import get_game_media_service

app = Flask(__name__)
# Configure CORS - allow same origin and local development
CORS(app, origins=[
    "https://graphqlmodel-production.up.railway.app",
    "http://localhost:5173",
    "http://localhost:3000"
], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])

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

def generate_confidence_explanation(prediction, details, home_team_name, away_team_name):
    """
    Generate detailed, game-specific confidence explanation based on matchup analysis
    Returns contextual analysis explaining WHY the model has this confidence level
    """
    # Get model vs market comparison
    model_spread = prediction.predicted_spread
    market_spread = getattr(prediction, 'market_spread', None)
    market_lines = details.get('market_lines', [])
    
    # Get team stats
    team_metrics = details.get('team_metrics', {})
    home_metrics = team_metrics.get('home', {})
    away_metrics = team_metrics.get('away', {})
    
    # Get advanced metrics
    advanced_metrics = details.get('advanced_metrics', {})
    
    # Determine favored team and margin
    home_favored = model_spread > 0
    favored_team = home_team_name if home_favored else away_team_name
    underdog_team = away_team_name if home_favored else home_team_name
    spread_magnitude = abs(model_spread)
    
    # Calculate market disagreement
    market_disagreement = 0
    market_opposite = False
    if market_spread is not None:
        market_disagreement = abs(model_spread - market_spread)
        market_home_favored = market_spread > 0
        market_opposite = home_favored != market_home_favored
    
    # Build explanation based on game characteristics
    explanations = []
    
    # 1. Spread magnitude confidence factors
    if spread_magnitude > 20:
        explanations.append(f"🔥 **Dominant Matchup**: {spread_magnitude:.1f}-point spread indicates significant talent gap")
        explanations.append(f"• Model projects {favored_team} to control all phases of the game")
    elif spread_magnitude > 10:
        explanations.append(f"⚡ **Clear Advantage**: {spread_magnitude:.1f}-point spread suggests {favored_team} superiority")
        explanations.append(f"• Multiple statistical indicators favor {favored_team}")
    elif spread_magnitude > 3:
        explanations.append(f"📊 **Moderate Edge**: {spread_magnitude:.1f}-point spread in competitive matchup")
        explanations.append(f"• {favored_team} holds statistical advantages but {underdog_team} remains viable")
    else:
        explanations.append(f"🎯 **Pick'em Game**: {spread_magnitude:.1f}-point spread indicates near-even matchup")
        explanations.append(f"• Both {home_team_name} and {away_team_name} project as highly competitive")
    
    # 2. Market comparison analysis
    if market_disagreement > 0:
        num_sportsbooks = len(market_lines)
        if market_opposite:
            explanations.append(f"🚨 **Market Contradiction**: Model completely opposite to {num_sportsbooks} sportsbook consensus")
            explanations.append(f"• Market favors {underdog_team}, model strongly favors {favored_team}")
            explanations.append(f"• {market_disagreement:.1f}-point disagreement suggests model found significant edge")
        elif market_disagreement > 10:
            explanations.append(f"📈 **Major Disagreement**: {market_disagreement:.1f}-point gap vs market consensus")
            explanations.append(f"• Model projects {favored_team} {market_disagreement:.1f} points stronger than {num_sportsbooks} sportsbooks price")
        elif market_disagreement > 5:
            explanations.append(f"📊 **Notable Variance**: {market_disagreement:.1f}-point difference from market lines")
            explanations.append(f"• Model algorithm weights factors differently than betting markets")
        else:
            explanations.append(f"✅ **Market Alignment**: Close agreement with {num_sportsbooks} sportsbook consensus")
            explanations.append(f"• Model and market both see similar competitive balance")
    
    # 3. Performance metrics analysis
    home_ppg = home_metrics.get('points_per_game', 0)
    away_ppg = away_metrics.get('points_per_game', 0)
    home_papg = home_metrics.get('points_allowed_per_game', 0)
    away_papg = away_metrics.get('points_allowed_per_game', 0)
    
    if home_ppg and away_ppg:
        offensive_gap = abs(home_ppg - away_ppg)
        defensive_gap = abs(home_papg - away_papg) if home_papg and away_papg else 0
        
        if offensive_gap > 15:
            high_offense_team = home_team_name if home_ppg > away_ppg else away_team_name
            explanations.append(f"🏈 **Offensive Mismatch**: {high_offense_team} averages {offensive_gap:.1f} more PPG")
        
        if defensive_gap > 10:
            better_defense_team = home_team_name if home_papg < away_papg else away_team_name
            explanations.append(f"🛡️ **Defensive Edge**: {better_defense_team} allows {defensive_gap:.1f} fewer PPG")
    
    # 4. Advanced metrics insights
    if advanced_metrics:
        epa_diff = advanced_metrics.get('overall_epa_diff', 0)
        if abs(epa_diff) > 0.3:
            epa_leader = favored_team if epa_diff * (1 if home_favored else -1) > 0 else underdog_team
            explanations.append(f"📈 **EPA Advantage**: {epa_leader} shows superior efficiency per play")
        
        explosiveness_diff = advanced_metrics.get('explosiveness_diff', 0)
        if abs(explosiveness_diff) > 0.1:
            explosive_team = home_team_name if explosiveness_diff > 0 else away_team_name
            explanations.append(f"💥 **Big Play Factor**: {explosive_team} generates more explosive plays")
    
    # 5. Data quality and reliability notes
    data_quality = calculate_base_data_quality(prediction, details)
    if data_quality >= 90:
        explanations.append(f"✅ **High Data Quality**: {data_quality}% complete data with {len(market_lines)} market sources")
    elif data_quality >= 80:
        explanations.append(f"📊 **Good Data Quality**: {data_quality}% data completeness supports reliable projection")
    else:
        explanations.append(f"⚠️ **Limited Data**: {data_quality}% data completeness may affect prediction reliability")
    
    return explanations

def extract_team_ratings(predictor, team_name):
    """Extract comprehensive ratings for a specific team from backtesting data"""
    if not hasattr(predictor, 'static_data') or not predictor.static_data:
        print(f"⚠️  No static_data available for {team_name}")
        return get_default_ratings()

    backtesting_ratings = predictor.static_data.get('backtesting_ratings', {})

    # Try exact match first
    team_ratings = backtesting_ratings.get(team_name, {})

    # If no exact match, try case-insensitive search
    if not team_ratings:
        for key in backtesting_ratings.keys():
            if key.lower() == team_name.lower():
                team_ratings = backtesting_ratings[key]
                print(f"✅ Found team ratings for {team_name} (matched as '{key}')")
                break

    if not team_ratings:
        print(f"⚠️  No ratings found for {team_name} in backtesting data")
        print(f"   Available teams: {list(backtesting_ratings.keys())[:5]}...")
        return get_default_ratings()

    # Ensure all required fields are present
    # The ratings should already have ratings_available=True from _process_backtesting_data
    if "ratings_available" not in team_ratings:
        team_ratings["ratings_available"] = True

    print(f"✅ Extracted ratings for {team_name}: ELO={team_ratings.get('elo', 'N/A')}, FPI={team_ratings.get('fpi', 'N/A')}")
    return team_ratings

def get_default_ratings():
    """Return default ratings when no data is available"""
    return {
        "elo": 1500,
        "fpi": 0.0,
        "sp_overall": 0.0,
        "srs": 0.0,
        "composite_rating": 0.0,
        "offensive_efficiency": 50.0,
        "defensive_efficiency": 50.0,
        "special_teams_efficiency": 50.0,
        "fpi_components": {
            "offensive_efficiency": 50.0,
            "defensive_efficiency": 50.0,
            "special_teams_efficiency": 50.0,
            "overall_efficiency": 50.0
        },
        "sp_components": {
            "offense": 25.0,
            "defense": 25.0,
            "special_teams": 0.0
        },
        "fpi_rankings": {
            "sos_rank": 65,
            "remaining_sos_rank": 65,
            "strength_of_record_rank": 65,
            "resume_rank": 65,
            "game_control_rank": 65,
            "avg_win_probability_rank": 65
        },
        "sos_rank": 65,
        "resume_rank": 65,
        "game_control_rank": 65,
        "rating_consistency": 10.0,
        "elite_tier": False,
        "struggling_tier": False,
        "ratings_available": False
    }

def calculate_ratings_comparison(predictor, away_team, home_team):
    """Calculate comprehensive comparison between team ratings"""
    away_ratings = extract_team_ratings(predictor, away_team)
    home_ratings = extract_team_ratings(predictor, home_team)
    
    if not away_ratings.get("ratings_available") or not home_ratings.get("ratings_available"):
        return {
            "elo_differential": 0,
            "fpi_differential": 0,
            "sp_differential": 0,
            "srs_differential": 0,
            "composite_differential": 0,
            "offensive_efficiency_differential": 0,
            "defensive_efficiency_differential": 0,
            "special_teams_differential": 0,
            "ranking_advantage": "neutral",
            "elite_matchup": False,
            "talent_gap": "balanced",
            "consistency_advantage": "neutral"
        }
    
    # Calculate differentials (home - away) - using the actual field names from the JSON
    elo_diff = home_ratings["elo"] - away_ratings["elo"]
    fpi_diff = home_ratings["fpi"] - away_ratings["fpi"]
    sp_diff = home_ratings["sp_overall"] - away_ratings["sp_overall"]
    srs_diff = home_ratings["srs"] - away_ratings["srs"]
    composite_diff = home_ratings.get("composite_rating", 0) - away_ratings.get("composite_rating", 0)
    
    # Efficiency differentials using fpi_components
    home_fpi = home_ratings.get("fpi_components", {})
    away_fpi = away_ratings.get("fpi_components", {})
    off_eff_diff = home_fpi.get("offensive_efficiency", 50) - away_fpi.get("offensive_efficiency", 50)
    def_eff_diff = home_fpi.get("defensive_efficiency", 50) - away_fpi.get("defensive_efficiency", 50)
    st_eff_diff = home_fpi.get("special_teams_efficiency", 50) - away_fpi.get("special_teams_efficiency", 50)
    
    # Determine advantages
    def get_advantage(differential, low_threshold=5, high_threshold=15):
        if differential > high_threshold:
            return "significant_home"
        elif differential > low_threshold:
            return "moderate_home"
        elif differential < -high_threshold:
            return "significant_away"
        elif differential < -low_threshold:
            return "moderate_away"
        else:
            return "neutral"
    
    ranking_advantage = get_advantage(fpi_diff, 5, 15)
    
    # Elite matchup detection
    elite_matchup = (home_ratings.get("elite_tier", False) or away_ratings.get("elite_tier", False))
    
    # Talent gap assessment
    talent_gap = "balanced"
    if abs(elo_diff) > 200 or abs(fpi_diff) > 20:
        talent_gap = "large"
    elif abs(elo_diff) > 100 or abs(fpi_diff) > 10:
        talent_gap = "moderate"
    
    # Consistency advantage
    home_consistency = home_ratings.get("rating_consistency", 10)
    away_consistency = away_ratings.get("rating_consistency", 10)
    consistency_diff = away_consistency - home_consistency  # Lower is better, so reverse
    consistency_advantage = get_advantage(consistency_diff, 3, 8)
    
    return {
        "elo_differential": round(elo_diff, 1),
        "fpi_differential": round(fpi_diff, 2),
        "sp_differential": round(sp_diff, 1),
        "srs_differential": round(srs_diff, 1),
        "composite_differential": round(composite_diff, 2),
        "offensive_efficiency_differential": round(off_eff_diff, 1),
        "defensive_efficiency_differential": round(def_eff_diff, 1),
        "special_teams_differential": round(st_eff_diff, 1),
        "ranking_advantage": ranking_advantage,
        "elite_matchup": elite_matchup,
        "talent_gap": talent_gap,
        "consistency_advantage": consistency_advantage
    }

def convert_comprehensive_stats_to_dict(stats):
    """Convert ComprehensiveTeamStats dataclass to dictionary for JSON serialization"""
    if stats is None:
        return {}
    
    # Convert dataclass to dict using __dict__
    return {
        k: v for k, v in stats.__dict__.items()
    }

def convert_coaching_metrics_to_dict(coaching):
    """Convert CoachingMetrics dataclass to dictionary for JSON serialization"""
    if coaching is None:
        return {}
    
    return {
        k: v for k, v in coaching.__dict__.items()
    }

def convert_drive_metrics_to_dict(drives):
    """Convert DriveMetrics dataclass to dictionary for JSON serialization"""
    if drives is None:
        return {}
    
    return {
        k: v for k, v in drives.__dict__.items()
    }

def format_prediction_for_api(prediction, home_team_data, away_team_data, predictor):
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
    
    # Inject real betting analysis from week8.json data
    home_team_name = home_team_data.get('name', prediction.home_team)
    away_team_name = away_team_data.get('name', prediction.away_team)
    
    # Get model spread and total from prediction object
    model_spread = getattr(prediction, 'predicted_spread', None)
    model_total = getattr(prediction, 'predicted_total', None)
    
    print(f"🎯 Integrating betting lines for {home_team_name} vs {away_team_name}")
    print(f"🔍 Model spread: {model_spread}, Model total: {model_total}")
    print(f"🔍 DEBUG: home_team_data.get('school') = '{home_team_data.get('school')}'")
    print(f"🔍 DEBUG: away_team_data.get('school') = '{away_team_data.get('school')}'")
    print(f"🔍 DEBUG: Calling betting_manager.get_betting_analysis('{home_team_name}', '{away_team_name}', {model_spread}, {model_total})")
    
    betting_analysis = betting_manager.get_betting_analysis(
        home_team_name, away_team_name, model_spread, model_total
    )
    
    # Update details with real betting analysis
    details['betting_analysis'] = betting_analysis
    print(f"📊 Betting analysis integrated: {betting_analysis.get('data_source', 'No data')}")
    print(f"🔍 DEBUG: betting_analysis keys: {list(betting_analysis.keys()) if betting_analysis else 'Empty'}")
    
    def get_val(d, *keys, default=0):
        """Helper to safely get nested values"""
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key, {})
            else:
                return default
        return d if d != {} else default
    
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
    
    # FIXED: Correct score calculation logic
    # Spread represents how much the HOME team is favored by (positive = home favored)
    # If home is favored by +7, they score 7 more than away team
    # Total = home_score + away_score, so:
    # home_score = (total + spread) / 2
    # away_score = (total - spread) / 2
    
    home_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
    away_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
    
    # Ensure no negative scores (safety check)
    if home_score < 0:
        away_score += abs(home_score)
        home_score = 0
    elif away_score < 0:
        home_score += abs(away_score)
        away_score = 0
    
    # Get weather data
    weather_data = get_val(details, 'weather', default={})
    print(f"🔍 DEBUG: Flask weather_data keys: {list(weather_data.keys()) if weather_data else 'None'}")
    print(f"🔍 DEBUG: Flask weather_data values: {weather_data}")
    
    # Get game metadata from Week 9 media service
    media_service = get_game_media_service()
    game_media_info = media_service.get_game_info(prediction.home_team, prediction.away_team)
    
    # Start with betting manager metadata as fallback
    game_metadata = betting_manager.get_game_metadata(prediction.home_team, prediction.away_team)
    
    # Override with actual game media data if available
    if game_media_info:
        print(f"✅ Found game media for {prediction.home_team} vs {prediction.away_team}")
        game_metadata['date'] = game_media_info.get('date', game_metadata.get('date', 'TBD'))
        game_metadata['time'] = game_media_info.get('time', game_metadata.get('time', 'TBD'))
        game_metadata['network'] = game_media_info.get('network', game_metadata.get('network', 'TBD'))
        
        # Also override weather if available from media service
        if game_media_info.get('weather'):
            media_weather = game_media_info['weather']
            if not weather_data or not weather_data.get('temperature'):
                weather_data = {
                    'temperature': media_weather.get('temperature'),
                    'wind_speed': media_weather.get('windSpeed'),
                    'precipitation': media_weather.get('precipitation'),
                    'humidity': media_weather.get('humidity'),
                    'conditions': 'Clear' if media_weather.get('weatherConditionCode', 0) == 0 else 'Various'
                }
    else:
        # Fallback to prediction object attributes
        if hasattr(prediction, 'game_date') and prediction.game_date:
            game_metadata['date'] = prediction.game_date
        if hasattr(prediction, 'game_time') and prediction.game_time:
            game_metadata['time'] = prediction.game_time
        
        # Extract network from media_info if available
        if hasattr(prediction, 'media_info') and prediction.media_info:
            for media in prediction.media_info:
                if media.get('mediaType') == 'TV' or media.get('mediaType') == 'television':
                    network_name = media.get('name', 'TBD')
                    game_metadata['network'] = network_name
                    break
    
    # Load rankings from AP Poll week_9 (most current)
    home_ranking = None
    away_ranking = None
    try:
        with open('frontend/src/data/ap.json', 'r') as f:
            ap_data = json.load(f)
        
        current_week = 'week_10'
        if current_week in ap_data:
            for rank_entry in ap_data[current_week]['ranks']:
                if rank_entry['school'] == prediction.home_team:
                    home_ranking = rank_entry
                elif rank_entry['school'] == prediction.away_team:
                    away_ranking = rank_entry
    except Exception as e:
        print(f"Note: AP Poll data not available: {e}")
        # Fallback to current week data if AP Poll fails
        home_ranking = {'rank': game_metadata.get('home_rank')} if game_metadata.get('home_rank') else None
        away_ranking = {'rank': game_metadata.get('away_rank')} if game_metadata.get('away_rank') else None
    
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
                "date": game_metadata.get('date', 'October 25, 2025'),
                "time": game_metadata.get('time', '4:00 PM ET'),
                "network": game_metadata.get('network', 'TBD'),
                "excitement_index": game_metadata.get('excitement_index', 4.2)
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
                "model_spread_display": f"{prediction.away_team if prediction.predicted_spread < 0 else prediction.home_team} {abs(prediction.predicted_spread):.1f}" if prediction.predicted_spread != 0 else "Pick'em",
                "market_spread": market_spread,
                "edge": abs(market_spread - prediction.predicted_spread) if market_spread else 0,
                "value_edge": (market_spread - prediction.predicted_spread) if market_spread else 0
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
            },
            "detailed_explanation": generate_confidence_explanation(
                prediction, details, prediction.home_team, prediction.away_team
            )
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
        "comprehensive_ratings": {
            "away_team": extract_team_ratings(predictor, prediction.away_team),
            "home_team": extract_team_ratings(predictor, prediction.home_team),
            "comparison": calculate_ratings_comparison(predictor, prediction.away_team, prediction.home_team)
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
            "confidence": {
                "overall_confidence": prediction.confidence * 100,
                "detailed_explanation": generate_confidence_explanation(
                    prediction, details, prediction.home_team, prediction.away_team
                )
            }
        },
        "detailed_analysis": {
            "enhanced_player_analysis": details.get('enhanced_player_analysis', {}),
            "betting_analysis": getattr(prediction, 'detailed_analysis', {}).get('betting_analysis', details.get('betting_analysis', {}))
        },
        # NEW: Team Statistics for UI components showing zeros
        "team_statistics": {
            "home": convert_comprehensive_stats_to_dict(getattr(prediction, 'home_team_stats', None)),
            "away": convert_comprehensive_stats_to_dict(getattr(prediction, 'away_team_stats', None))
        },
        "coaching_data": {
            "home": convert_coaching_metrics_to_dict(getattr(prediction, 'home_coaching', None)),
            "away": convert_coaching_metrics_to_dict(getattr(prediction, 'away_coaching', None))
        },
        "drive_metrics": {
            "home": convert_drive_metrics_to_dict(getattr(prediction, 'home_drive_metrics', None)),
            "away": convert_drive_metrics_to_dict(getattr(prediction, 'away_drive_metrics', None))
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

@app.route('/health', methods=['GET'])
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

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict_game():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return '', 200
        
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
            print(f"🔍 Debug: Calling predict_game with IDs: {home_team_id}, {away_team_id}")
            print(f"🔍 Debug: Team names in request: '{data['home_team']}', '{data['away_team']}'")
            prediction = loop.run_until_complete(
                predictor.predict_game(home_team_id, away_team_id)
            )
            
            # Apply consistency fixes
            prediction = apply_prediction_fixes(prediction)
            
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
            
            comprehensive_analysis = format_prediction_for_api(prediction, home_team_data, away_team_data, predictor)
            
            # Validate prediction consistency
            validation_results = PredictionValidator.validate_full_prediction({
                'predicted_spread': prediction.predicted_spread,
                'predicted_total': prediction.predicted_total,
                'home_win_prob': prediction.home_win_prob,
                'ui_components': comprehensive_analysis.get('ui_components', {})
            })
            
            # Log validation results
            if not validation_results['is_valid']:
                print(f"⚠️ VALIDATION ERRORS: {validation_results['errors']}")
            if validation_results['warnings']:
                print(f"🔍 VALIDATION WARNINGS: {validation_results['warnings']}")
            if validation_results['consistency_checks']:
                print(f"✅ CONSISTENCY CHECKS: {validation_results['consistency_checks']}")
            
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
            
            # Calculate predicted winner based on home win probability
            predicted_winner = prediction.home_team if prediction.home_win_prob > 0.5 else prediction.away_team
            
            # Calculate implied scores from spread and total
            home_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
            away_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
            
            return jsonify({
                "success": True,
                "prediction": {
                    "home_team": prediction.home_team,
                    "away_team": prediction.away_team,
                    "predicted_winner": predicted_winner,
                    "home_score": home_score,
                    "away_score": away_score,
                    "spread": prediction.predicted_spread,
                    "total": prediction.predicted_total,
                    "home_win_probability": prediction.home_win_prob,
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
            
            # Calculate predicted winner based on home win probability
            predicted_winner = prediction.home_team if prediction.home_win_prob > 0.5 else prediction.away_team
            
            # Calculate implied scores from spread and total
            home_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
            away_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
            
            # Return comprehensive JSON response
            response_data = {
                "success": True,
                "prediction": {
                    "home_team": prediction.home_team,
                    "away_team": prediction.away_team,
                    "predicted_winner": predicted_winner,
                    "home_score": home_score,
                    "away_score": away_score,
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

@app.route('/api/live-game', methods=['GET'])
def get_live_game():
    """Fetch live game data including win probability, field position, and plays"""
    try:
        home_team = request.args.get('home')
        away_team = request.args.get('away')
        
        if not home_team or not away_team:
            return jsonify({
                'error': 'Both home and away team names are required'
            }), 400
        
        # Import the live data fetcher
        import sys
        import importlib.util
        
        # Load the test script as a module
        spec = importlib.util.spec_from_file_location("live_fetcher", "test_iowa_state_live.py")
        live_fetcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(live_fetcher)
        
        # Fetch live data
        live_data = live_fetcher.get_complete_live_data(home_team, away_team)
        
        return jsonify(live_data)
        
    except Exception as e:
        print(f"Error fetching live game data: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to fetch live game data: {str(e)}'
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