from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_cors import CORS
import asyncio
import os
import json
import sqlite3
from graphqlpredictor import LightningPredictor
from run import format_prediction_output
# from prediction_validator import PredictionValidator, apply_prediction_fixes
from betting_lines_manager import betting_manager
from game_media_service import get_game_media_service
from real_data_props_generator import RealDataPlayerPropsEngine
from dataclasses import asdict
from rivalry_config import is_rivalry_game, get_rivalry_info
from batch_rivalry_analyzer import BatchRivalryAnalyzer
from espn_player_service import ESPNPlayerService
from advanced_drive_analytics import drive_analytics

app = Flask(__name__)
# Configure CORS - allow same origin and local development
CORS(app, origins=[
    "https://graphqlmodel-production.up.railway.app",
    "http://localhost:5173",
    "http://localhost:5555",
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
    
    # Return all games
    return {
        "team": team_name,
        "record": f"{wins}-{losses}",
        "logo": team_data.get('logo_url', 'N/A'),
        "primary_color": team_data.get('primary_color', '#000000'),
        "games": games  # All games
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

def enrich_players_with_headshots(player_analysis, home_team, away_team):
    """
    Enrich player data with ESPN headshot URLs
    """
    try:
        espn = get_espn_service()
        
        # Get home and away player groups
        home_players = player_analysis.get('home_players', {})
        away_players = player_analysis.get('away_players', {})
        
        # Enrich home team players
        if home_players:
            espn.enrich_player_data(home_players, home_team)
        
        # Enrich away team players
        if away_players:
            espn.enrich_player_data(away_players, away_team)
        
        print(f"✅ Added ESPN headshots for {home_team} vs {away_team}")
        
    except Exception as e:
        print(f"⚠️  Could not fetch ESPN headshots: {e}")
    
    return player_analysis

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

def load_comprehensive_power_rankings():
    """Load the comprehensive power rankings data"""
    try:
        rankings_path = os.path.join(os.path.dirname(__file__), 'weekly_updates', 'week_15', 'comprehensive_power_rankings_20251203_053934.json')
        with open(rankings_path, 'r') as f:
            power_rankings = json.load(f)
        return power_rankings.get('rankings', [])
    except Exception as e:
        print(f"❌ Error loading comprehensive power rankings: {e}")
        return []

def extract_team_ratings(predictor, team_name):
    """Extract comprehensive ratings for a specific team from comprehensive_power_rankings.json"""
    try:
        print(f"🔍 DEBUG: Looking for team '{team_name}'")
        # Load from comprehensive power rankings JSON in weekly_updates/week_15
        rankings_path = os.path.join(os.path.dirname(__file__), 'weekly_updates', 'week_15', 'comprehensive_power_rankings_20251203_053934.json')
        print(f"🔍 DEBUG: Loading from path: {rankings_path}")
        with open(rankings_path, 'r') as f:
            power_rankings = json.load(f)
        
        print(f"🔍 DEBUG: Found {len(power_rankings.get('rankings', []))} teams in rankings")
        
        # Find team in the rankings array
        team_data = None
        for team in power_rankings.get('rankings', []):
            team_name_in_file = team.get('team', '')
            print(f"🔍 DEBUG: Comparing '{team_name.lower()}' with '{team_name_in_file.lower()}'")
            if team_name_in_file.lower() == team_name.lower():
                team_data = team
                print(f"✅ DEBUG: Found match for {team_name}!")
                break
        
        if not team_data:
            print(f"⚠️  No ratings found for {team_name} in power rankings")
            return get_default_ratings()
        
        # Extract ratings from team data - using actual field names from the JSON
        team_ratings = {
            'team': team_data.get('team', team_name),
            'conference': team_data.get('conference', ''),
            'ratings_available': True,
            'elo': 1500 + (team_data.get('overall_score', 50) - 50) * 10,  # Convert overall score to ELO scale
            'fpi': team_data.get('overall_score', 50) - 50,  # Use overall score as FPI
            'sp_overall': team_data.get('defensive_score', 50) - team_data.get('offensive_score', 50),  # SP+ style diff
            'srs': (team_data.get('overall_score', 50) - 50) * 0.8,  # Scaled overall score
            'composite_rating': team_data.get('overall_score', 50),
            'offensive_efficiency': team_data.get('offensive_score', 50),
            'defensive_efficiency': team_data.get('defensive_score', 50),
            'special_teams_efficiency': 50.0,  # Default since not in this data
            'fpi_components': {
                'offensive_efficiency': team_data.get('offensive_score', 50),
                'defensive_efficiency': team_data.get('defensive_score', 50),
                'special_teams_efficiency': 50.0,
                'overall_efficiency': team_data.get('overall_score', 50)
            },
            'sp_components': {
                'offense': team_data.get('offensive_score', 50),
                'defense': team_data.get('defensive_score', 50),
                'special_teams': 50.0
            },
            'fpi_rankings': {
                'sos_rank': team_data.get('rank', 65),
                'remaining_sos_rank': team_data.get('rank', 65),
                'strength_of_record_rank': team_data.get('rank', 65),
                'resume_rank': team_data.get('rank', 65),
                'game_control_rank': team_data.get('rank', 65),
                'avg_win_probability_rank': team_data.get('rank', 65)
            },
            'rating_consistency': 85.0,  # Default high consistency
            'elite_tier': team_data.get('rank', 65) <= 10,
            'struggling_tier': team_data.get('rank', 65) >= 100
        }
        
        print(f"✅ Extracted ratings for {team_name}: ELO={team_ratings['elo']}, FPI={team_ratings['fpi']}, SP+={team_ratings['sp_overall']}")
        return team_ratings
        
    except Exception as e:
        print(f"❌ Error loading ratings for {team_name}: {e}")
        return get_default_ratings()

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

def get_team_stats_from_db(team_name, season=2025):
    """
    Fetch comprehensive team stats from database (coaches_master.db)
    Includes all advanced metrics + newly added box score stats
    """
    import sqlite3
    from pathlib import Path
    
    db_path = Path(__file__).parent / 'instance' / 'coaches_master.db'
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT ts.*
            FROM team_seasons ts
            JOIN teams t ON ts.team_id = t.id
            WHERE t.school = ? AND ts.season = ?
        """
        cursor.execute(query, (team_name, season))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return {}
    except Exception as e:
        print(f"Error fetching stats for {team_name}: {e}")
        return {}

def merge_team_stats_with_db(stats_dict, team_name, season=2025):
    """
    Merge GraphQL stats with database stats
    Database stats take priority for newly added fields
    """
    if not stats_dict:
        stats_dict = {}
    
    # Get database stats
    db_stats = get_team_stats_from_db(team_name, season)
    
    if db_stats:
        # Merge, with database stats overriding GraphQL stats
        stats_dict.update(db_stats)
    
    return stats_dict

def convert_comprehensive_stats_to_dict(stats):
    """
    Convert ComprehensiveTeamStats dataclass to dictionary for JSON serialization
    """
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

def analyze_team_drives_for_ui(team_name):
    """
    Analyze drive data for a team from power5_drives_only.json
    Returns structured data matching the UI component expectations
    """
    import json
    from collections import defaultdict
    
    try:
        # Load drives data
        drives_file = 'data/power5_drives_only.json'
        with open(drives_file, 'r') as f:
            all_drives = json.load(f)
        
        # Filter drives where this team is on offense
        team_drives = [d for d in all_drives if d.get('offense') == team_name]
        
        if not team_drives:
            return None
        
        # Quarter analysis
        quarters = defaultdict(lambda: {'total': 0, 'scored': 0})
        for drive in team_drives:
            period = drive.get('startPeriod', 0)
            quarters[period]['total'] += 1
            if drive.get('scoring', False):
                quarters[period]['scored'] += 1
        
        quarter_data = []
        for q in [1, 2, 3, 4]:
            if quarters[q]['total'] > 0:
                quarter_data.append({
                    'quarter': f'Q{q}',
                    'drives': quarters[q]['total'],
                    'scoringPct': round((quarters[q]['scored'] / quarters[q]['total']) * 100, 1),
                    'scored': quarters[q]['scored']
                })
        
        # Field position analysis
        field_zones = {
            'Own 1-20': {'total': 0, 'scored': 0},
            'Own 21-40': {'total': 0, 'scored': 0},
            'Own 41-Mid': {'total': 0, 'scored': 0},
            'Opp Territory': {'total': 0, 'scored': 0}
        }
        
        for drive in team_drives:
            start_yard = drive.get('startYardline', 0)
            scored = drive.get('scoring', False)
            
            if start_yard <= 20:
                zone = 'Own 1-20'
            elif start_yard <= 40:
                zone = 'Own 21-40'
            elif start_yard <= 50:
                zone = 'Own 41-Mid'
            else:
                zone = 'Opp Territory'
            
            field_zones[zone]['total'] += 1
            if scored:
                field_zones[zone]['scored'] += 1
        
        field_position_data = []
        for zone in ['Own 1-20', 'Own 21-40', 'Own 41-Mid', 'Opp Territory']:
            stats = field_zones[zone]
            if stats['total'] > 0:
                field_position_data.append({
                    'zone': zone,
                    'drives': stats['total'],
                    'scoringPct': round((stats['scored'] / stats['total']) * 100, 1),
                    'scored': stats['scored']
                })
        
        # Drive outcomes
        outcomes = defaultdict(int)
        for drive in team_drives:
            result = drive.get('driveResult', 'UNKNOWN')
            outcomes[result] += 1
        
        total_drives = len(team_drives)
        td_count = outcomes.get('TD', 0)
        fg_count = outcomes.get('FG', 0)
        punt_count = outcomes.get('PUNT', 0)
        turnover_count = sum(outcomes.get(key, 0) for key in ['INT', 'FUMBLE', 'INT TD', 'FUMBLE TD'])
        
        drive_outcomes = {
            'touchdowns': round((td_count / total_drives) * 100, 1),
            'fieldGoals': round((fg_count / total_drives) * 100, 1),
            'punts': round((punt_count / total_drives) * 100, 1),
            'turnovers': round((turnover_count / total_drives) * 100, 1),
            'totalScoring': round(((td_count + fg_count) / total_drives) * 100, 1),
            'total_drives': total_drives
        }
        
        return {
            'quarter_data': quarter_data,
            'field_position_data': field_position_data,
            'drive_outcomes': drive_outcomes
        }
        
    except Exception as e:
        print(f"Error analyzing drives for {team_name}: {e}")
        return None

def generate_game_summary_and_rationale(prediction, details, home_team_data, away_team_data, predictor, betting_analysis=None):
    """
    Generate comprehensive game summary explaining which team has the edge and why.
    Calculates every component and provides clarity on critical stats.
    Includes market line comparison and betting recommendations.
    """
    home_team = prediction.home_team
    away_team = prediction.away_team
    
    # Calculate key metrics
    home_win_prob = prediction.home_win_prob * 100
    away_win_prob = (1 - prediction.home_win_prob) * 100
    predicted_spread = prediction.predicted_spread
    predicted_total = prediction.predicted_total
    
    # Determine favored team
    if predicted_spread > 0:
        favored_team = home_team
        underdog_team = away_team
        spread_margin = predicted_spread
    else:
        favored_team = away_team
        underdog_team = home_team
        spread_margin = abs(predicted_spread)
    
    # Get team stats
    home_stats = getattr(prediction, 'home_team_stats', None)
    away_stats = getattr(prediction, 'away_team_stats', None)
    
    # EPA Analysis - using correct attribute names
    home_epa_offense = home_stats.epa_offense if home_stats else 0
    home_epa_defense = home_stats.epa_defense if home_stats else 0
    away_epa_offense = away_stats.epa_offense if away_stats else 0
    away_epa_defense = away_stats.epa_defense if away_stats else 0
    
    home_total_epa = home_epa_offense + abs(home_epa_defense)
    away_total_epa = away_epa_offense + abs(away_epa_defense)
    epa_advantage = home_team if home_total_epa > away_total_epa else away_team
    epa_diff = abs(home_total_epa - away_total_epa)
    
    # Power ratings comparison
    home_ratings = extract_team_ratings(predictor, home_team)
    away_ratings = extract_team_ratings(predictor, away_team)
    
    home_fpi = home_ratings.get('fpi', 0)
    away_fpi = away_ratings.get('fpi', 0)
    fpi_advantage = home_team if home_fpi > away_fpi else away_team
    fpi_diff = abs(home_fpi - away_fpi)
    
    # Offensive/Defensive metrics - using correct attribute names
    home_off_success = home_stats.success_rate_offense if home_stats else 0
    away_off_success = away_stats.success_rate_offense if away_stats else 0
    home_def_success = home_stats.success_rate_defense if home_stats else 0
    away_def_success = away_stats.success_rate_defense if away_stats else 0
    
    offensive_edge = home_team if home_off_success > away_off_success else away_team
    defensive_edge = home_team if home_def_success < away_def_success else away_team  # Lower is better for defense
    
    # Calculate overall edge score (0-100)
    edge_factors = []
    
    # Win probability weight (30%)
    if home_win_prob > away_win_prob:
        edge_factors.append(('home', (home_win_prob - 50) * 0.6))  # Scale to 0-30
    else:
        edge_factors.append(('away', (away_win_prob - 50) * 0.6))
    
    # EPA weight (25%)
    if epa_advantage == home_team:
        edge_factors.append(('home', min(epa_diff * 5, 25)))
    else:
        edge_factors.append(('away', min(epa_diff * 5, 25)))
    
    # FPI weight (20%)
    if fpi_advantage == home_team:
        edge_factors.append(('home', min(fpi_diff * 0.5, 20)))
    else:
        edge_factors.append(('away', min(fpi_diff * 0.5, 20)))
    
    # Success rate weight (15%)
    success_diff = (home_off_success - away_off_success) * 100
    if success_diff > 0:
        edge_factors.append(('home', min(abs(success_diff), 15)))
    else:
        edge_factors.append(('away', min(abs(success_diff), 15)))
    
    # Spread margin weight (10%)
    spread_factor = min(spread_margin * 0.5, 10)
    if favored_team == home_team:
        edge_factors.append(('home', spread_factor))
    else:
        edge_factors.append(('away', spread_factor))
    
    # Calculate final edge scores
    home_edge_score = sum(val for team, val in edge_factors if team == 'home')
    away_edge_score = sum(val for team, val in edge_factors if team == 'away')
    
    # Build key advantages lists
    home_advantages = []
    away_advantages = []
    
    if home_epa_offense > away_epa_offense:
        home_advantages.append(f"Superior offensive EPA: {home_epa_offense:+.3f} vs {away_epa_offense:+.3f}")
    else:
        away_advantages.append(f"Superior offensive EPA: {away_epa_offense:+.3f} vs {home_epa_offense:+.3f}")
    
    if home_epa_defense < away_epa_defense:  # Lower is better
        home_advantages.append(f"Stronger defensive EPA: {home_epa_defense:+.3f} vs {away_epa_defense:+.3f}")
    else:
        away_advantages.append(f"Stronger defensive EPA: {away_epa_defense:+.3f} vs {home_epa_defense:+.3f}")
    
    if home_fpi > away_fpi:
        home_advantages.append(f"Higher FPI rating: {home_fpi:.1f} vs {away_fpi:.1f}")
    else:
        away_advantages.append(f"Higher FPI rating: {away_fpi:.1f} vs {home_fpi:.1f}")
    
    if home_off_success > away_off_success:
        home_advantages.append(f"Better offensive success rate: {home_off_success:.1%} vs {away_off_success:.1%}")
    else:
        away_advantages.append(f"Better offensive success rate: {away_off_success:.1%} vs {home_off_success:.1%}")
    
    if home_def_success < away_def_success:
        home_advantages.append(f"Better defensive success rate: {home_def_success:.1%} vs {away_def_success:.1%}")
    else:
        away_advantages.append(f"Better defensive success rate: {away_def_success:.1%} vs {home_def_success:.1%}")
    
    # Home field advantage
    home_advantages.append("Home field advantage")
    
    # Extract market lines from betting analysis
    market_lines = []
    consensus_spread = None
    consensus_total = None
    spread_edge = 0
    total_edge = 0
    best_spread_book = None
    best_total_book = None
    
    if betting_analysis:
        sportsbooks = betting_analysis.get('sportsbooks', {}).get('individual_books', [])
        if sportsbooks:
            spreads = []
            totals = []
            
            for book in sportsbooks:
                book_name = book.get('provider', 'Unknown')
                spread = book.get('spread')
                total = book.get('over_under')
                odds = book.get('spread_odds', -110)
                
                if spread is not None:
                    spreads.append(spread)
                if total is not None:
                    totals.append(total)
                
                market_lines.append({
                    'sportsbook': book_name,
                    'spread': spread,
                    'total': total,
                    'odds': odds
                })
            
            # Calculate consensus lines (average)
            if spreads:
                consensus_spread = sum(spreads) / len(spreads)
                
                # Find best spread line (lowest absolute value = best for bettor)
                if predicted_spread < 0:  # Away team favored - want smallest spread to lay
                    best_spread_book = min(sportsbooks, key=lambda x: abs(x.get('spread', 0)))
                else:  # Home team favored - want smallest spread to lay
                    best_spread_book = max(sportsbooks, key=lambda x: abs(x.get('spread', 0)))
                
                # Calculate edge using BEST available line, not consensus
                best_market_spread = best_spread_book.get('spread') if best_spread_book else consensus_spread
                spread_edge = abs(predicted_spread) - abs(best_market_spread)
            
            if totals:
                consensus_total = sum(totals) / len(totals)
                
                # Find best total line (lowest for over bets, highest for under bets)
                if predicted_total > consensus_total:  # Model predicts over
                    best_total_book = min(sportsbooks, key=lambda x: x.get('over_under', 999))
                else:  # Model predicts under
                    best_total_book = max(sportsbooks, key=lambda x: x.get('over_under', 0))
                
                # Calculate edge using BEST available line, not consensus
                best_market_total = best_total_book.get('over_under') if best_total_book else consensus_total
                total_edge = predicted_total - best_market_total
    
    # Determine bet recommendations with grading
    recommendations = []
    
    # SMART BET FILTERING LOGIC
    # Rule 1: If model spread < 3 points, game too close - skip or flip
    # Rule 2: If model contradicts market direction, flip to other team
    # Rule 3: If model spread < 0.5 * market spread, market knows something - flip or skip
    
    should_recommend_spread = True
    flip_bet_side = False
    
    if best_spread_book:
        best_market_spread = best_spread_book.get('spread')
        model_spread_abs = abs(predicted_spread)
        market_spread_abs = abs(best_market_spread)
        
        # Determine who each side favors
        model_favors_away = predicted_spread < 0
        market_favors_away = best_market_spread > 0  # Positive spread = home is underdog, away favored
        
        # Rule 1: Model projects game too close to call (< 3 points)
        if model_spread_abs < 3:
            # Check if we should flip to take the underdog with points
            if market_spread_abs >= 2:  # Market giving significant points
                flip_bet_side = True  # Take the underdog getting points
            else:
                should_recommend_spread = False  # Skip - too close
        
        # Rule 2: Model spread is less than half of market spread (market disagrees strongly)
        elif model_spread_abs < (market_spread_abs * 0.5):
            flip_bet_side = True  # Take opposite side
        
        # Rule 3: Model and market favor different teams entirely
        if model_favors_away != market_favors_away:
            flip_bet_side = True  # Market completely disagrees, trust the market
        if model_favors_away != market_favors_away:
            flip_bet_side = True  # Market completely disagrees, take their side
    
    # Spread recommendation with smart filtering
    if abs(spread_edge) >= 3:
        grade = "STRONG"
        icon = "fire"
    elif abs(spread_edge) >= 2:
        grade = "GOOD"
        icon = "star"
    elif abs(spread_edge) >= 1:
        grade = "SLIGHT"
        icon = "warning"
    else:
        grade = None
        icon = None
    
    if grade and best_spread_book and should_recommend_spread:
        market_spread_value = best_spread_book.get('spread')
        
        # Determine which team to bet based on flip logic
        # market_spread_value is from HOME team perspective:
        #   Positive = home is underdog getting +points
        #   Negative = home is favorite giving -points
        
        if flip_bet_side:
            # FLIP: Always take the UNDERDOG getting points (safer bet when model uncertain)
            if market_spread_value > 0:  # Home getting points -> BET HOME +points
                bet_display = f"{home_team} +{abs(market_spread_value):.1f}"
            else:  # Home giving points (is favorite), so away getting points -> BET AWAY +points  
                bet_display = f"{away_team} +{abs(market_spread_value):.1f}"
        else:
            # NORMAL: Bet the model's favored team laying points
            if predicted_spread < 0:  # Model favors away -> BET AWAY laying points
                bet_display = f"{away_team} -{abs(market_spread_value):.1f}"
            else:  # Model favors home -> BET HOME laying points
                bet_display = f"{home_team} -{abs(market_spread_value):.1f}"
        
        recommendations.append({
            'type': 'spread',
            'grade': grade,
            'icon': icon,
            'bet': bet_display,
            'sportsbook': best_spread_book.get('provider'),
            'edge': round(spread_edge, 1),
            'odds': best_spread_book.get('spread_odds', -110)
        })
    
    # Total recommendation
    if abs(total_edge) >= 5:
        grade = "STRONG"
        icon = "fire"
    elif abs(total_edge) >= 3:
        grade = "GOOD"
        icon = "star"
    elif abs(total_edge) >= 1.5:
        grade = "SLIGHT"
        icon = "warning"
    else:
        grade = None
        icon = None
    
    if grade and best_total_book:
        bet_direction = "OVER" if total_edge > 0 else "UNDER"
        bet_line = best_total_book.get('over_under')
        recommendations.append({
            'type': 'total',
            'grade': grade,
            'icon': icon,
            'bet': f"{bet_direction} {bet_line:.1f}",
            'sportsbook': best_total_book.get('provider'),
            'edge': round(total_edge, 1),
            'odds': -110
        })
    
    # Build summary
    summary = {
        "favored_team": favored_team,
        "underdog_team": underdog_team,
        "predicted_winner": home_team if home_win_prob > away_win_prob else away_team,
        "win_probability": {
            "home": round(home_win_prob, 1),
            "away": round(away_win_prob, 1),
            "favorite": round(max(home_win_prob, away_win_prob), 1)
        },
        "spread_analysis": {
            "predicted_spread": predicted_spread,
            "spread_display": f"{favored_team} -{spread_margin:.1f}",
            "margin": round(spread_margin, 1),
            "interpretation": (
                f"{favored_team} is favored by {spread_margin:.1f} points. "
                f"This indicates a {'decisive' if spread_margin > 14 else 'moderate' if spread_margin > 7 else 'close'} matchup."
            )
        },
        "total_analysis": {
            "predicted_total": round(predicted_total, 1),
            "projected_score": {
                "home": round(predicted_total / 2 + predicted_spread / 2, 1),
                "away": round(predicted_total / 2 - predicted_spread / 2, 1)
            },
            "pace": "High-scoring" if predicted_total > 60 else "Moderate" if predicted_total > 50 else "Low-scoring"
        },
        "edge_analysis": {
            "home_edge_score": round(home_edge_score, 1),
            "away_edge_score": round(away_edge_score, 1),
            "total_edge": round(abs(home_edge_score - away_edge_score), 1),
            "edge_leader": home_team if home_edge_score > away_edge_score else away_team
        },
        "critical_stats": {
            "epa": {
                "home_offense": round(home_epa_offense, 3),
                "home_defense": round(home_epa_defense, 3),
                "away_offense": round(away_epa_offense, 3),
                "away_defense": round(away_epa_defense, 3),
                "advantage": epa_advantage,
                "differential": round(epa_diff, 3)
            },
            "power_ratings": {
                "home_fpi": round(home_fpi, 1),
                "away_fpi": round(away_fpi, 1),
                "advantage": fpi_advantage,
                "differential": round(fpi_diff, 1)
            },
            "success_rates": {
                "home_offense": round(home_off_success * 100, 1),
                "away_offense": round(away_off_success * 100, 1),
                "home_defense": round(home_def_success * 100, 1),
                "away_defense": round(away_def_success * 100, 1),
                "offensive_edge": offensive_edge,
                "defensive_edge": defensive_edge
            }
        },
        "key_advantages": {
            "home": home_advantages,
            "away": away_advantages
        },
        "bottom_line": {
            "recommendation": (
                recommendations[0]['bet'] + f" at {recommendations[0]['sportsbook']}" if recommendations else f"No strong edge (Model: {favored_team} {-spread_margin:.1f})"
            ),
            "recommendation_type": recommendations[0]['type'] if recommendations else None,
            "recommendation_grade": recommendations[0]['grade'] if recommendations else None,
            "recommendation_edge": recommendations[0]['edge'] if recommendations else 0,
            "model_spread": f"{favored_team} {-spread_margin:.1f}",
            "market_spread": f"{favored_team} {-abs(consensus_spread):.1f}" if consensus_spread else "N/A",
            "confidence_level": "High" if prediction.confidence > 0.75 else "Moderate" if prediction.confidence > 0.60 else "Low",
            "confidence_percentage": round(prediction.confidence * 100, 1),
            "summary": (
                f"{favored_team} holds the edge in this matchup with a {max(home_win_prob, away_win_prob):.1f}% win probability. "
                f"The model projects a {spread_margin:.1f}-point margin of victory, driven primarily by "
                f"{epa_advantage}'s superior EPA metrics ({epa_diff:.2f} differential) and "
                f"{fpi_advantage}'s stronger power rating ({fpi_diff:.1f} point FPI advantage). "
                + (f"Home field advantage further bolsters {home_team}'s " if home_edge_score > away_edge_score else f"{away_team} must overcome the road environment, but their ") +
                f"position with an overall edge score of {max(home_edge_score, away_edge_score):.1f}/100."
            ),
            "key_factors": prediction.key_factors[:5] if hasattr(prediction, 'key_factors') else []
        },
        "market_analysis": {
            "model_prediction": {
                "spread": predicted_spread,
                "total": predicted_total,
                "spread_display": f"{favored_team} {-spread_margin:.1f}",
                "total_display": f"{predicted_total:.1f}"
            },
            "market_consensus": {
                "spread": round(consensus_spread, 1) if consensus_spread else None,
                "total": round(consensus_total, 1) if consensus_total else None,
                "spread_display": f"{favored_team} {-abs(consensus_spread):.1f}" if consensus_spread else "N/A",
                "total_display": f"{consensus_total:.1f}" if consensus_total else "N/A"
            },
            "edge_detected": {
                "spread_edge": round(spread_edge, 1),
                "total_edge": round(total_edge, 1),
                "has_spread_edge": abs(spread_edge) >= 1,
                "has_total_edge": abs(total_edge) >= 1.5
            },
            "sportsbook_lines": market_lines,
            "best_bets": recommendations
        }
    }
    
    return summary

def generate_arbitrage_analysis(sportsbooks, model_spread, model_total, confidence, home_team, away_team):
    """Generate arbitrage opportunities using ArbitrageDetector"""
    from graphqlpredictor import ArbitrageDetector
    
    if not sportsbooks or len(sportsbooks) == 0:
        return {
            'opportunities': [],
            'total_opportunities': 0,
            'best_margin': 0,
            'market_efficiency': 100.0,
            'message': 'Insufficient sportsbook data for arbitrage analysis'
        }
    
    try:
        analysis = ArbitrageDetector.analyze_arbitrage(
            sportsbooks, model_spread, model_total, confidence, home_team, away_team
        )
        return analysis
    except Exception as e:
        print(f"⚠️ Error generating arbitrage analysis: {e}")
        return {
            'opportunities': [],
            'total_opportunities': 0,
            'best_margin': 0,
            'market_efficiency': 100.0,
            'error': str(e)
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
    
    # Use consistent scores from GamePrediction if available (prevents inconsistency bug)
    if hasattr(prediction, 'home_predicted_score') and prediction.home_predicted_score is not None:
        home_score = prediction.home_predicted_score
        away_score = prediction.away_predicted_score
        print(f"🎯 Using consistent scores: {prediction.home_team} {home_score}, {prediction.away_team} {away_score}")
    else:
        # Fallback to calculation (for backward compatibility)
        # Spread represents how much the HOME team is favored by (positive = home favored)
        home_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
        away_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
        
        # Ensure no negative scores (safety check)
        if home_score < 0:
            away_score += abs(home_score)
            home_score = 0
        elif away_score < 0:
            home_score += abs(away_score)
            away_score = 0
        print(f"🔄 Using calculated scores: {prediction.home_team} {home_score}, {prediction.away_team} {away_score}")
    
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
    
    # Load rankings from Currentweekgames.json (Week 11 rankings already embedded)
    home_ranking = None
    away_ranking = None
    
    # Use rankings from game_metadata (from Currentweekgames.json)
    if game_metadata.get('home_rank'):
        home_ranking = {'rank': game_metadata.get('home_rank')}
    if game_metadata.get('away_rank'):
        away_ranking = {'rank': game_metadata.get('away_rank')}
    
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
                # Display format: Favorite team with negative spread (e.g., "Ohio State -35.0")
                # Model convention: positive = home favored, negative = away favored
                # Display convention: always show favorite with negative (industry standard)
                "model_spread_display": (
                    f"{prediction.away_team if prediction.predicted_spread < 0 else prediction.home_team} {-abs(prediction.predicted_spread):.1f}"
                    if prediction.predicted_spread != 0 else "Pick'em"
                ),
                "market_spread": market_spread,
                # Normalize market spread: ESPN/JSON uses negative for home favorite, model uses positive
                # Convert market to model convention (positive = home favored) before calculating edge
                "edge": abs(prediction.predicted_spread - (-market_spread)) if market_spread else 0,
                "value_edge": (prediction.predicted_spread - (-market_spread)) if market_spread else 0
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
        "comprehensive_power_rankings": load_comprehensive_power_rankings(),
        "season_records": {
            "away": extract_team_season_games(details, 'awaySeasonGames', 'awayTeamId', prediction.away_team, away_team_data),
            "home": extract_team_season_games(details, 'homeSeasonGames', 'homeTeamId', prediction.home_team, home_team_data)
        },
        "game_summary_and_rationale": generate_game_summary_and_rationale(
            prediction, details, home_team_data, away_team_data, predictor, betting_analysis
        ),
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
            "enhanced_player_analysis": enrich_players_with_headshots(
                details.get('enhanced_player_analysis', {}),
                home_team=prediction.home_team,
                away_team=prediction.away_team
            ),
            "betting_analysis": getattr(prediction, 'detailed_analysis', {}).get('betting_analysis', details.get('betting_analysis', {}))
        },
        # NEW: Arbitrage Analysis
        "arbitrage_analysis": generate_arbitrage_analysis(
            betting_analysis.get('sportsbooks', {}).get('individual_books', []),
            prediction.predicted_spread,
            prediction.predicted_total,
            prediction.confidence * 100,
            prediction.home_team,
            prediction.away_team
        ) if betting_analysis.get('sportsbooks', {}).get('individual_books') else {},
        # NEW: Team Statistics for UI components - Enhanced with database stats
        "team_statistics": {
            "home": merge_team_stats_with_db(
                convert_comprehensive_stats_to_dict(getattr(prediction, 'home_team_stats', None)),
                prediction.home_team,
                2025
            ),
            "away": merge_team_stats_with_db(
                convert_comprehensive_stats_to_dict(getattr(prediction, 'away_team_stats', None)),
                prediction.away_team,
                2025
            )
        },
        "coaching_data": {
            "home": convert_coaching_metrics_to_dict(getattr(prediction, 'home_coaching', None)),
            "away": convert_coaching_metrics_to_dict(getattr(prediction, 'away_coaching', None))
        },
        "drive_metrics": {
            "home": convert_drive_metrics_to_dict(getattr(prediction, 'home_drive_metrics', None)),
            "away": convert_drive_metrics_to_dict(getattr(prediction, 'away_drive_metrics', None))
        },
        "drive_analytics": {
            "home": analyze_team_drives_for_ui(prediction.home_team),
            "away": analyze_team_drives_for_ui(prediction.away_team)
        }
    }
    
    return {
        "formatted_analysis": formatted_analysis,
        "ui_components": ui_components
    }

# Predictor will be initialized lazily within the endpoint
api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
predictor = None
espn_service = None

def get_predictor():
    """Initializes and returns a single instance of the predictor."""
    global predictor
    if predictor is None:
        predictor = LightningPredictor(api_key)
    return predictor

def get_espn_service():
    """Initializes and returns a single instance of ESPN player service."""
    global espn_service
    if espn_service is None:
        espn_service = ESPNPlayerService()
    return espn_service

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
        
        # Check if this is a rivalry game
        rivalry_history = None
        print(f"🔍 Checking rivalry for: '{data['home_team']}' vs '{data['away_team']}'")
        if is_rivalry_game(data['home_team'], data['away_team']):
            rivalry_info = get_rivalry_info(data['home_team'], data['away_team'])
            print(f"🏆 RIVALRY DETECTED: {rivalry_info['name']}")
            if rivalry_info.get('trophy'):
                print(f"   Trophy: {rivalry_info['trophy']}")
            
            # Fetch rivalry history
            try:
                analyzer = BatchRivalryAnalyzer()
                
                # Get all-time series record from REST API
                # NOTE: For display, away_team is team1 and home_team is team2 to match UI order
                alltime_record = analyzer.get_alltime_series_record(data['away_team'], data['home_team'])
                
                # Get detailed recent games from GraphQL  
                games = analyzer.get_rivalry_games(data['away_team'], data['home_team'])
                if games:
                    # Sort games by season and week (most recent first)
                    games = sorted(games, key=lambda g: (g['season'], g['week']), reverse=True)
                    
                    rankings = analyzer.get_rankings_for_games(games)
                    stats = analyzer.analyze_rivalry(data['away_team'], data['home_team'], games, rankings)
                    
                    # Merge all-time stats with recent game stats
                    if alltime_record:
                        stats['total_games_alltime'] = alltime_record.get('total_games_alltime', stats['total_games'])
                        stats['team1_wins_alltime'] = alltime_record.get('team1_wins_alltime', stats['team1_wins'])
                        stats['team2_wins_alltime'] = alltime_record.get('team2_wins_alltime', stats['team2_wins'])
                        stats['ties_alltime'] = alltime_record.get('ties_alltime', 0)
                        stats['series_record_alltime'] = alltime_record.get('series_record_alltime', f"{stats['team1_wins']}-{stats['team2_wins']}")
                        if alltime_record.get('established'):
                            rivalry_info['established'] = alltime_record['established']
                    
                    # Make stats JSON serializable
                    stats_serializable = {k: v for k, v in stats.items() if k not in ['closest_game', 'biggest_blowout']}
                    if stats.get('closest_game'):
                        stats_serializable['closest_game'] = {
                            'season': stats['closest_game']['season'],
                            'week': stats['closest_game']['week'],
                            'homeTeam': stats['closest_game']['homeTeam'],
                            'awayTeam': stats['closest_game']['awayTeam'],
                            'homePoints': stats['closest_game']['homePoints'],
                            'awayPoints': stats['closest_game']['awayPoints']
                        }
                    if stats.get('biggest_blowout'):
                        stats_serializable['biggest_blowout'] = {
                            'season': stats['biggest_blowout']['season'],
                            'week': stats['biggest_blowout']['week'],
                            'homeTeam': stats['biggest_blowout']['homeTeam'],
                            'awayTeam': stats['biggest_blowout']['awayTeam'],
                            'homePoints': stats['biggest_blowout']['homePoints'],
                            'awayPoints': stats['biggest_blowout']['awayPoints']
                        }
                    
                    # Use the formatted display name from rivalry_info
                    display_name = rivalry_info.get('name_display', f"{data['home_team']} vs {data['away_team']}")
                    
                    rivalry_history = {
                        'name': display_name,
                        'trophy': rivalry_info.get('trophy'),
                        'established': rivalry_info.get('established'),
                        'stats': stats_serializable,
                        'recent_games': games[:10]  # First 10 games (now sorted most recent first)
                    }
                    print(f"   ✓ Loaded {stats['total_games']} historical games ({stats['team1_wins']}-{stats['team2_wins']} series)")
            except Exception as e:
                print(f"   ⚠️ Could not load rivalry history: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"   ℹ️  Not a rivalry game")
        
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
            # prediction = apply_prediction_fixes(prediction)
            
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
            # validation_results = PredictionValidator.validate_full_prediction({
            #     'predicted_spread': prediction.predicted_spread,
            #     'predicted_total': prediction.predicted_total,
            #     'home_win_prob': prediction.home_win_prob,
            #     'ui_components': comprehensive_analysis.get('ui_components', {})
            # })
            
            # Log validation results
            # if not validation_results['is_valid']:
            #     print(f"⚠️ VALIDATION ERRORS: {validation_results['errors']}")
            # if validation_results['warnings']:
            #     print(f"🔍 VALIDATION WARNINGS: {validation_results['warnings']}")
            # if validation_results['consistency_checks']:
            #     print(f"✅ CONSISTENCY CHECKS: {validation_results['consistency_checks']}")
            
            # The formatted analysis is already printed by format_prediction_output
            
            print("\n" + "=" * 80)
            print("🎯 ANALYSIS COMPLETE - RETURNING STRUCTURED JSON")
            print("=" * 80)
            
            # Return the comprehensive analysis from formatter
            response_data = {
                "success": True,
                **comprehensive_analysis
            }
            
            # Add rivalry history if available
            if rivalry_history:
                response_data['rivalry_history'] = rivalry_history
                print(f"\n🏆 Added rivalry history to response")
            
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

@app.route('/advanced-drive-analytics/<home_team>/<away_team>', methods=['GET'])
def get_advanced_drive_analytics(home_team, away_team):
    """Get comprehensive drive analytics and quarter-by-quarter predictions"""
    try:
        # Get drive metrics for both teams
        home_metrics = drive_analytics.get_team_drive_metrics(home_team, season=2025)
        away_metrics = drive_analytics.get_team_drive_metrics(away_team, season=2025)
        
        # Get quarter predictions
        quarter_predictions = drive_analytics.predict_quarter_outcomes(home_team, away_team, season=2025)
        
        return jsonify({
            'home_team': home_team,
            'away_team': away_team,
            'home_metrics': home_metrics,
            'away_metrics': away_metrics,
            'quarter_predictions': quarter_predictions,
            'summary': {
                'home_explosive_advantage': home_metrics['explosive_pct'] > away_metrics['explosive_pct'],
                'home_methodical_advantage': home_metrics['methodical_pct'] > away_metrics['methodical_pct'],
                'home_redzone_advantage': home_metrics['red_zone_efficiency'] > away_metrics['red_zone_efficiency'],
                'home_quick_strike_advantage': home_metrics['quick_strike_pct'] > away_metrics['quick_strike_pct']
            }
        })
    except Exception as e:
        return jsonify({
            "error": f"Drive analytics failed: {str(e)}"
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
    """Fetch live game data from ESPN API including field position, scores, and plays"""
    try:
        import requests
        import json as json_lib
        
        home_team = request.args.get('home')
        away_team = request.args.get('away')
        
        if not home_team or not away_team:
            return jsonify({
                'error': 'Both home and away team names are required'
            }), 400
        
        # Load team mappings from fbs.json
        with open('fbs.json', 'r') as f:
            teams_data = json_lib.load(f)
        
        # Find team info from fbs.json
        home_info = None
        away_info = None
        for team in teams_data:
            if team['school'].lower() == home_team.lower() or home_team.lower() in team['school'].lower():
                home_info = team
            if team['school'].lower() == away_team.lower() or away_team.lower() in team['school'].lower():
                away_info = team
        
        # Fetch current games from ESPN scoreboard
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
        scoreboard_response = requests.get(scoreboard_url, timeout=10)
        scoreboard_data = scoreboard_response.json()
        
        # Find the matching game
        game_id = None
        for event in scoreboard_data.get('events', []):
            event_name = event.get('name', '').lower()
            if (home_team.lower() in event_name or (home_info and home_info['school'].lower() in event_name)) and \
               (away_team.lower() in event_name or (away_info and away_info['school'].lower() in event_name)):
                game_id = event['id']
                break
        
        if not game_id:
            return jsonify({
                'game_info': {
                    'is_live': False,
                    'home_team': home_team,
                    'away_team': away_team
                },
                'message': 'Game not found or not currently live'
            }), 200
        
        # Fetch detailed game data
        summary_url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={game_id}"
        summary_response = requests.get(summary_url, timeout=10)
        game_data = summary_response.json()
        
        # Extract game state
        header = game_data.get('header', {})
        competitions = header.get('competitions', [{}])[0]
        status = competitions.get('status', {})
        competitors = competitions.get('competitors', [])
        
        # Determine home/away from competitors
        home_competitor = next((c for c in competitors if c.get('homeAway') == 'home'), {})
        away_competitor = next((c for c in competitors if c.get('homeAway') == 'away'), {})
        
        is_live = status.get('type', {}).get('state') == 'in'
        
        # Extract current drive and field position
        drives = game_data.get('drives', {})
        current_drive = drives.get('current', {})
        previous_drives = drives.get('previous', [])
        
        # Get the most recent play for field position
        field_position_data = {}
        possession_team_id = None
        
        if current_drive and current_drive.get('plays'):
            last_play = current_drive['plays'][-1]
            end_data = last_play.get('end', {})
            field_position_data = {
                'yard_line': end_data.get('yardsToEndzone', 50),
                'down': end_data.get('down', 1),
                'distance': end_data.get('distance', 10),
                'possession_text': end_data.get('possessionText', '50'),
                'down_distance_text': end_data.get('shortDownDistanceText', '1st & 10')
            }
            possession_team_id = current_drive.get('team', {}).get('id')
        elif previous_drives:
            last_drive = previous_drives[-1]
            if last_drive.get('plays'):
                last_play = last_drive['plays'][-1]
                end_data = last_play.get('end', {})
                field_position_data = {
                    'yard_line': end_data.get('yardsToEndzone', 50),
                    'down': end_data.get('down', 1),
                    'distance': end_data.get('distance', 10),
                    'possession_text': end_data.get('possessionText', '50'),
                    'down_distance_text': end_data.get('shortDownDistanceText', '1st & 10')
                }
                possession_team_id = last_drive.get('team', {}).get('id')
        
        # Determine possession
        possession_team = 'home'
        if possession_team_id:
            if str(possession_team_id) == str(away_competitor.get('team', {}).get('id')):
                possession_team = 'away'
        
        # Extract all plays from drives
        all_plays = []
        
        # Get plays from previous drives
        for drive in previous_drives:
            if isinstance(drive, dict):
                for play in drive.get('plays', []):
                    # Transform ESPN play data to our frontend format
                    team_participants = play.get('teamParticipants', [])
                    offense_team = next((t for t in team_participants if t.get('type') == 'offense'), {})
                    offense_team_id = offense_team.get('id', '')
                    
                    # Determine team name
                    if str(offense_team_id) == str(home_competitor.get('team', {}).get('id')):
                        team_name = home_competitor.get('team', {}).get('abbreviation', home_team)
                    else:
                        team_name = away_competitor.get('team', {}).get('abbreviation', away_team)
                    
                    # Extract play details
                    start_pos = play.get('start', {})
                    end_pos = play.get('end', {})
                    
                    all_plays.append({
                        'id': play.get('id', ''),
                        'period': play.get('period', {}).get('number', 1),
                        'clock': play.get('clock', {}).get('displayValue', ''),
                        'team': team_name,
                        'offense': 'home' if str(offense_team_id) == str(home_competitor.get('team', {}).get('id')) else 'away',
                        'down': start_pos.get('down'),
                        'distance': start_pos.get('distance'),
                        'yard_line': start_pos.get('yardsToEndzone'),
                        'yards_to_goal': start_pos.get('yardsToEndzone'),
                        'yards_gained': play.get('statYardage', 0),
                        'play_type': play.get('type', {}).get('text', ''),
                        'play_text': play.get('text', ''),
                        'home_score': play.get('homeScore', 0),
                        'away_score': play.get('awayScore', 0),
                        'epa': play.get('expectedPoints', {}).get('added') if play.get('expectedPoints') else None,
                        'success': play.get('statYardage', 0) >= start_pos.get('distance', 0) if start_pos.get('down', 0) in [3, 4] else None
                    })
        
        # Get plays from current drive
        if current_drive and isinstance(current_drive, dict):
            for play in current_drive.get('plays', []):
                team_participants = play.get('teamParticipants', [])
                offense_team = next((t for t in team_participants if t.get('type') == 'offense'), {})
                offense_team_id = offense_team.get('id', '')
                
                if str(offense_team_id) == str(home_competitor.get('team', {}).get('id')):
                    team_name = home_competitor.get('team', {}).get('abbreviation', home_team)
                else:
                    team_name = away_competitor.get('team', {}).get('abbreviation', away_team)
                
                start_pos = play.get('start', {})
                end_pos = play.get('end', {})
                
                all_plays.append({
                    'id': play.get('id', ''),
                    'period': play.get('period', {}).get('number', 1),
                    'clock': play.get('clock', {}).get('displayValue', ''),
                    'team': team_name,
                    'offense': 'home' if str(offense_team_id) == str(home_competitor.get('team', {}).get('id')) else 'away',
                    'down': start_pos.get('down'),
                    'distance': start_pos.get('distance'),
                    'yard_line': start_pos.get('yardsToEndzone'),
                    'yards_to_goal': start_pos.get('yardsToEndzone'),
                    'yards_gained': play.get('statYardage', 0),
                    'play_type': play.get('type', {}).get('text', ''),
                    'play_text': play.get('text', ''),
                    'home_score': play.get('homeScore', 0),
                    'away_score': play.get('awayScore', 0),
                    'epa': play.get('expectedPoints', {}).get('added') if play.get('expectedPoints') else None,
                    'success': play.get('statYardage', 0) >= start_pos.get('distance', 0) if start_pos.get('down', 0) in [3, 4] else None
                })
        
        # Build response
        response_data = {
            'game_info': {
                'is_live': is_live,
                'status': status.get('type', {}).get('state', 'unknown'),  # 'in', 'pre', 'post'
                'status_detail': status.get('type', {}).get('detail', ''),  # e.g., 'Final', 'Halftime'
                'home_team': home_competitor.get('team', {}).get('displayName', home_team),
                'away_team': away_competitor.get('team', {}).get('displayName', away_team),
                'home_abbr': home_competitor.get('team', {}).get('abbreviation', ''),
                'away_abbr': away_competitor.get('team', {}).get('abbreviation', ''),
                'home_logo': home_info['logos'][0] if home_info and home_info.get('logos') else home_competitor.get('team', {}).get('logo'),
                'away_logo': away_info['logos'][0] if away_info and away_info.get('logos') else away_competitor.get('team', {}).get('logo'),
                'home_color': '#' + home_competitor.get('team', {}).get('color', home_info.get('color', '1a7a42') if home_info else '1a7a42'),
                'away_color': '#' + away_competitor.get('team', {}).get('color', away_info.get('color', '0d5c2f') if away_info else '0d5c2f')
            },
            'game_state': {
                'period': status.get('period', 1),
                'clock': status.get('displayClock', '15:00'),
                'possession': possession_team,
                'situation': field_position_data.get('down_distance_text', '1st & 10'),
                'home_score': int(home_competitor.get('score', 0)),
                'away_score': int(away_competitor.get('score', 0))
            },
            'field_position': field_position_data,
            'win_probability': {
                'home': competitions.get('situation', {}).get('lastPlay', {}).get('probability', {}).get('homeWinPercentage', 50.0),
                'away': competitions.get('situation', {}).get('lastPlay', {}).get('probability', {}).get('awayWinPercentage', 50.0)
            },
            'plays': all_plays,  # All plays for replay functionality
            'recent_plays': all_plays[-50:] if len(all_plays) > 50 else all_plays,  # Last 50 plays for live feed
            'total_plays': len(all_plays)
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error fetching live game data from ESPN: {e}")
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

@app.route('/api/team/<int:team_id>/drives-stats', methods=['GET'])
def get_team_drives_stats(team_id):
    """Get drive statistics for a team from the drives database"""
    try:
        import sqlite3
        
        conn = sqlite3.connect('gameday_analytics.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get total drives and games played for calculating drives per game
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT d.id) as total_drives,
                COUNT(DISTINCT d.game_id) as games_played,
                AVG(d.yards) as avg_yards_per_drive,
                SUM(d.plays) as total_plays,
                SUM(CASE WHEN d.scoring = 1 THEN 1 ELSE 0 END) as scoring_drives,
                SUM(CASE WHEN d.drive_result LIKE '%TD%' THEN 1 ELSE 0 END) as td_drives,
                SUM(CASE WHEN d.drive_result LIKE '%FG%' OR d.drive_result LIKE '%FGA%' THEN 1 ELSE 0 END) as fg_drives,
                SUM(CASE WHEN d.drive_result LIKE '%PUNT%' THEN 1 ELSE 0 END) as punt_drives,
                SUM(CASE WHEN d.drive_result LIKE '%INT%' OR d.drive_result LIKE '%FUMBLE%' THEN 1 ELSE 0 END) as turnover_drives
            FROM drives d
            WHERE d.offense_team_id = ?
        """, (team_id,))
        
        stats = dict(cursor.fetchone())
        
        # Calculate drives per game
        games_played = stats['games_played'] or 1
        stats['drives_per_game'] = round(stats['total_drives'] / games_played, 1)
        
        # Calculate percentages
        total = stats['total_drives'] or 1
        stats['td_rate'] = round((stats['td_drives'] / total) * 100, 1)
        stats['scoring_rate'] = round((stats['scoring_drives'] / total) * 100, 1)
        
        conn.close()
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        print(f"❌ Error getting drives stats for team {team_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/coach/<int:coach_id>/timeline', methods=['GET'])
def get_coach_timeline(coach_id):
    """Get coach timeline data for visualization"""
    try:
        conn = sqlite3.connect('instance/coaches_master.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get timeline data
        cursor.execute("""
            SELECT 
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
        
        if not row:
            # Try to get basic coach info
            cursor.execute("SELECT name, headshot_url FROM coaches WHERE id = ?", (coach_id,))
            coach = cursor.fetchone()
            if coach:
                return jsonify({
                    'coachName': coach['name'],
                    'coachHeadshot': coach['headshot_url'],
                    'data': [],
                    'metadata': {
                        'record': '0-0',
                        'win_pct': '0.0'
                    },
                    'career_schools': []
                }), 200
            return jsonify({'error': 'Coach not found'}), 404
        
        # Parse JSON fields
        import json
        weekly_data = json.loads(row['weekly_data']) if row['weekly_data'] else []
        plot_bands = json.loads(row['plot_bands']) if row['plot_bands'] else []
        
        # Get coach headshot and career schools
        cursor.execute("""
            SELECT c.headshot_url, s.school, s.start_year, s.end_year, s.record, s.win_pct
            FROM coaches c
            LEFT JOIN stints s ON c.id = s.coach_id
            WHERE c.id = ?
            ORDER BY s.start_year
        """, (coach_id,))
        
        coach_data = cursor.fetchall()
        headshot = coach_data[0]['headshot_url'] if coach_data else None
        
        # Build career schools array
        career_schools = []
        for stint in coach_data:
            if stint['school']:
                # Get team data from fbs.json via database or use defaults
                cursor.execute("""
                    SELECT t.logos, t.color, t.alt_color 
                    FROM teams t 
                    WHERE t.school = ?
                    LIMIT 1
                """, (stint['school'],))
                team_row = cursor.fetchone()
                
                if team_row and team_row['logos']:
                    import json
                    logos = json.loads(team_row['logos'])
                    team_logo = logos[0] if logos else None
                    team_color = team_row['color'] or team_row['alt_color']
                else:
                    team_logo = None
                    team_color = '#666666'
                
                career_schools.append({
                    'school_name': stint['school'],
                    'school': stint['school'],
                    'years': f"{stint['start_year']}-{stint['end_year'] if stint['end_year'] != stint['start_year'] else stint['start_year']}",
                    'record': stint['record'],
                    'win_pct': float(stint['win_pct']) if stint['win_pct'] else 0.0,
                    'team_logo': team_logo,
                    'team_color': team_color
                })
        
        conn.close()
        
        return jsonify({
            'coachName': row['coach_name'],
            'coachHeadshot': headshot,
            'data': weekly_data,
            'metadata': {
                'record': row['career_record'],
                'win_pct': f"{float(row['career_win_pct']):.1f}" if row['career_win_pct'] else '0.0',
                'max_win_streak': row['max_win_streak'],
                'total_ranked_wins': row['total_ranked_wins']
            },
            'career_schools': career_schools,
            'plot_bands': plot_bands
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting timeline for coach {coach_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/coaches/comparison', methods=['GET'])
def get_coaches_comparison():
    """Get comprehensive coach comparison data from coaches_master.db"""
    try:
        home_team = request.args.get('home_team')
        away_team = request.args.get('away_team')
        
        if not home_team or not away_team:
            return jsonify({'error': 'Both home_team and away_team required'}), 400
        
        print(f"\n👔 Coaches Comparison Request: {home_team} vs {away_team}")
        
        conn = sqlite3.connect('instance/coaches_master.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        def get_coach_comprehensive_data(team_name):
            """Get all coach data for a team"""
            # Get coach and school info
            # Try exact match first, looking for active coaches (end_year >= 2024)
            cursor.execute("""
                SELECT c.id, c.name, c.headshot_url, s.school
                FROM coaches c
                JOIN stints s ON c.id = s.coach_id
                WHERE s.school = ? AND s.end_year >= 2024
                ORDER BY s.end_year DESC
                LIMIT 1
            """, (team_name,))
            
            coach_row = cursor.fetchone()
            
            # If not found, try fuzzy match
            if not coach_row:
                print(f"⚠️ Exact match failed for {team_name}, trying fuzzy match...")
                cursor.execute("""
                    SELECT c.id, c.name, c.headshot_url, s.school
                    FROM coaches c
                    JOIN stints s ON c.id = s.coach_id
                    WHERE s.school LIKE ? AND s.end_year >= 2024
                    ORDER BY s.end_year DESC
                    LIMIT 1
                """, (f"%{team_name}%",))
                coach_row = cursor.fetchone()

            if not coach_row:
                print(f"❌ No coach found for {team_name}")
                return None
            
            print(f"✅ Found coach for {team_name}: {coach_row['name']} ({coach_row['school']})")
            
            coach_id = coach_row['id']
            coach_name = coach_row['name']
            headshot_url = coach_row['headshot_url']
            
            # Get team colors and logo from teams table
            cursor.execute("""
                SELECT color, alt_color, logo_url
                FROM teams
                WHERE school = ?
            """, (team_name,))
            team_row = cursor.fetchone()
            team_color = team_row['color'] if team_row else None
            team_alt_color = team_row['alt_color'] if team_row else None
            team_logo = team_row['logo_url'] if team_row else None
            
            # Career summary
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN g.result = 'W' THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN g.result = 'L' THEN 1 ELSE 0 END) as losses,
                    COUNT(DISTINCT g.season || '-' || g.week) as total_games,
                    COUNT(DISTINCT g.season) as seasons
                FROM games g
                WHERE g.coach_id = ?
            """, (coach_id,))
            career = cursor.fetchone()
            
            total_games = career['total_games']
            wins = career['wins']
            win_pct = wins / total_games if total_games > 0 else 0
            
            # Last 10 games
            cursor.execute("""
                SELECT result, (coach_score - opponent_score) as diff
                FROM games
                WHERE coach_id = ?
                ORDER BY season DESC, week DESC
                LIMIT 10
            """, (coach_id,))
            last_10 = cursor.fetchall()
            last_10_wins = sum(1 for g in last_10 if g['result'] == 'W')
            last_10_losses = len(last_10) - last_10_wins
            last_10_diff = sum(g['diff'] for g in last_10) / len(last_10) if last_10 else 0
            
            # Stints
            cursor.execute("""
                SELECT school, start_year, end_year, record, win_pct, games_coached as games
                FROM stints
                WHERE coach_id = ?
                ORDER BY start_year DESC
            """, (coach_id,))
            stints = [dict(row) for row in cursor.fetchall()]
            
            # Situational stats by school
            cursor.execute("""
                SELECT school, 
                       vs_ranked_record as vs_ranked, 
                       vs_top_10_record as vs_top_10, 
                       home_record as home, 
                       away_record as away, 
                       neutral_record as neutral, 
                       (one_score_wins || '-' || one_score_losses) as one_score,
                       (blowout_wins || '-' || blowout_losses) as blowouts, 
                       conference_record as conference
                FROM situational_stats
                WHERE coach_id = ?
            """, (coach_id,))
            situational = [dict(row) for row in cursor.fetchall()]
            
            # Season analytics (all seasons) - need to join with games for record
            cursor.execute("""
                SELECT 
                    sa.season,
                    sa.school,
                    COALESCE(
                        (SELECT COUNT(DISTINCT week) FROM games WHERE coach_id = ? AND season = sa.season AND school = sa.school AND result = 'W'),
                        0
                    ) || '-' || 
                    COALESCE(
                        (SELECT COUNT(DISTINCT week) FROM games WHERE coach_id = ? AND season = sa.season AND school = sa.school AND result = 'L'),
                        0
                    ) as record,
                    CAST(COALESCE(
                        (SELECT COUNT(DISTINCT week) FROM games WHERE coach_id = ? AND season = sa.season AND school = sa.school AND result = 'W'),
                        0
                    ) AS FLOAT) / NULLIF(
                        (SELECT COUNT(DISTINCT week) FROM games WHERE coach_id = ? AND season = sa.season AND school = sa.school),
                        0
                    ) as win_pct,
                    sa.points_per_game as ppg,
                    sa.points_allowed_pg as papg,
                    sa.yards_per_play as ypp,
                    sa.sp_overall,
                    sa.sp_offense,
                    sa.sp_defense,
                    sa.fpi,
                    sa.srs,
                    sa.third_down_pct,
                    sa.fourth_down_pct
                FROM season_analytics sa
                WHERE sa.coach_id = ?
                ORDER BY sa.season DESC
            """, (coach_id, coach_id, coach_id, coach_id, coach_id))
            seasons = [dict(row) for row in cursor.fetchall()]
            
            # 2025 season detail
            season_2025 = next((s for s in seasons if s['season'] == 2025), None)
            
            # Key players 2025
            cursor.execute("""
                SELECT player_name as name, position, passing_yards, rushing_yards, receiving_yards
                FROM player_season_stats
                WHERE team = ? AND season = 2025
                ORDER BY 
                    COALESCE(passing_yards, 0) + 
                    COALESCE(rushing_yards, 0) + 
                    COALESCE(receiving_yards, 0) DESC
                LIMIT 5
            """, (team_name,))
            key_players = [dict(row) for row in cursor.fetchall()]
            
            # Get 2025 games for trend chart
            cursor.execute("""
                SELECT 
                    week,
                    opponent,
                    opponent_logo,
                    result,
                    coach_score as points_for,
                    opponent_score as points_against,
                    (coach_score - opponent_score) as diff
                FROM games
                WHERE coach_id = ? AND season = 2025
                ORDER BY week ASC
            """, (coach_id,))
            games_2025 = [dict(row) for row in cursor.fetchall()]
            
            if season_2025:
                season_2025['key_players_2025'] = key_players
                season_2025['games'] = games_2025
            
            # Recruiting classes
            cursor.execute("""
                SELECT year, class_rank
                FROM recruiting_classes
                WHERE coach_id = ?
                ORDER BY year DESC
            """, (coach_id,))
            recruiting = [dict(row) for row in cursor.fetchall()]
            
            # Talent composite
            cursor.execute("""
                SELECT year, talent_rating, talent_rank
                FROM talent_composite
                WHERE coach_id = ?
                ORDER BY year DESC
            """, (coach_id,))
            talent = [dict(row) for row in cursor.fetchall()]
            
            # Transfer portal
            cursor.execute("""
                SELECT season, transfers_in as "in", transfers_out as "out",
                       (transfers_in - transfers_out) as net,
                       avg_rating_in, avg_rating_out
                FROM transfer_portal
                WHERE coach_id = ?
                ORDER BY season DESC
            """, (coach_id,))
            portal = [dict(row) for row in cursor.fetchall()]
            
            # Draft picks
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN round = 1 THEN 1 ELSE 0 END) as r1,
                    SUM(CASE WHEN round = 2 THEN 1 ELSE 0 END) as r2,
                    SUM(CASE WHEN round = 3 THEN 1 ELSE 0 END) as r3,
                    SUM(CASE WHEN round >= 4 THEN 1 ELSE 0 END) as r4plus
                FROM draft_picks
                WHERE coach_id = ?
            """, (coach_id,))
            draft_summary = dict(cursor.fetchone())
            
            cursor.execute("""
                SELECT year, COUNT(*) as picks,
                       SUM(CASE WHEN round = 1 THEN 1 ELSE 0 END) as r1,
                       SUM(CASE WHEN round = 2 THEN 1 ELSE 0 END) as r2,
                       SUM(CASE WHEN round = 3 THEN 1 ELSE 0 END) as r3,
                       SUM(CASE WHEN round >= 4 THEN 1 ELSE 0 END) as r4plus
                FROM draft_picks
                WHERE coach_id = ?
                GROUP BY year
                ORDER BY year DESC
                LIMIT 5
            """, (coach_id,))
            draft_by_year = [dict(row) for row in cursor.fetchall()]
            
            # NIL strategy
            cursor.execute("""
                SELECT total_valuation, total_players as player_count, avg_valuation as avg_valuation_per_player
                FROM nil_team_summary
                WHERE team_name = ?
            """, (team_name,))
            nil_row = cursor.fetchone()
            nil_strategy = dict(nil_row) if nil_row else None
            
            # Build coaching archetype (simplified version)
            archetype_key = f"{coach_name.lower().replace(' ', '_')}_{team_name.lower().replace(' ', '_')}"
            archetype = {
                "offensive_identity": {
                    "style": "Data-driven offense" if season_2025 and season_2025.get('sp_offense', 0) > 30 else "Balanced attack",
                    "philosophy": f"Averaging {season_2025['ppg']:.1f} PPG" if season_2025 else "N/A"
                },
                "defensive_philosophy": {
                    "style": "Elite defense" if season_2025 and season_2025.get('sp_defense', 100) < 20 else "Solid defense"
                },
                "game_management": {
                    "aggression_level": "Aggressive" if season_2025 and season_2025.get('fourth_down_pct', 0) > 55 else "Moderate",
                    "fourth_down_conversion_avg": f"{season_2025['fourth_down_pct']:.1f}%" if season_2025 else "N/A"
                },
                "nil_strategy": {
                    "total_valuation": nil_strategy['total_valuation'] if nil_strategy else 0,
                    "players": nil_strategy['player_count'] if nil_strategy else 0,
                    "avg_per_player": nil_strategy['avg_valuation_per_player'] if nil_strategy else 0
                },
                "archetype_summary": f"{coach_name} is building a competitive program at {team_name}"
            }
            
            return {
                "profile": {
                    "coach_id": coach_id,
                    "coach_name": coach_name,
                    "school": team_name,
                    "headshot_url": headshot_url,
                    "team_color": team_color,
                    "secondary_color": team_alt_color,
                    "team_logo": team_logo
                },
                "career_summary": {
                    "record": f"{wins}-{career['losses']}",
                    "win_pct": win_pct,
                    "total_games": total_games,
                    "seasons_coached": career['seasons'],
                    "last_10_record": f"{last_10_wins}-{last_10_losses}",
                    "last_10_avg_point_diff": round(last_10_diff, 1)
                },
                "stints": stints,
                "situational_by_school": situational,
                "seasons": seasons,
                "season_2025_detail": season_2025,
                "recruiting_classes": recruiting,
                "talent_composite": talent,
                "transfer_portal": portal,
                "draft_picks": {
                    "recent_total": draft_summary['total'],
                    "breakdown": {
                        "r1": draft_summary['r1'],
                        "r2": draft_summary['r2'],
                        "r3": draft_summary['r3'],
                        "r4plus": draft_summary['r4plus']
                    },
                    "years": draft_by_year
                },
                "coaching_archetype_analysis": {
                    archetype_key: archetype
                },
                "advanced_performance_metrics": {}
            }
        
        coach1_data = get_coach_comprehensive_data(home_team)
        coach2_data = get_coach_comprehensive_data(away_team)
        
        conn.close()
        
        if not coach1_data or not coach2_data:
            return jsonify({
                'error': 'Coach data not found for one or both teams',
                'home_team': home_team,
                'away_team': away_team
            }), 404
        
        # Build comparative analysis
        comparative_analysis = {
            "lane_kiffin_vs_bret_bielema": {
                "record_comparison": f"{coach1_data['career_summary']['record']} vs {coach2_data['career_summary']['record']}",
                "points_per_game": f"{coach1_data['season_2025_detail']['ppg']:.1f} vs {coach2_data['season_2025_detail']['ppg']:.1f}" if coach1_data.get('season_2025_detail') and coach2_data.get('season_2025_detail') else "N/A"
            },
            "philosophy_clash": {
                "offensive_approach": f"{home_team} high-powered vs {away_team} balanced",
                "tempo": "Contrasting styles create fascinating matchup",
                "recruiting": "Different position priorities reflect coaching philosophies"
            }
        }
        
        # Build hypothetical matchup
        coach1_win_pct = coach1_data['career_summary']['win_pct']
        coach2_win_pct = coach2_data['career_summary']['win_pct']
        
        if coach1_win_pct > coach2_win_pct:
            favorite = home_team
            favorite_prob = "60-65%"
            underdog = away_team
        else:
            favorite = away_team
            favorite_prob = "60-65%"
            underdog = home_team
        
        hypothetical_matchup = {
            "head_to_head_never_met": f"{coach1_data['profile']['coach_name']} and {coach2_data['profile']['coach_name']} have never faced each other as head coaches",
            "prediction_framework": {
                "ole_miss_advantages": [
                    f"Higher win percentage ({coach1_win_pct*100:.1f}% vs {coach2_win_pct*100:.1f}%)",
                    f"More seasons coached ({coach1_data['career_summary']['seasons_coached']} vs {coach2_data['career_summary']['seasons_coached']})"
                ] if coach1_win_pct > coach2_win_pct else [],
                "illinois_advantages": [
                    f"Higher win percentage ({coach2_win_pct*100:.1f}% vs {coach1_win_pct*100:.1f}%)",
                    "Underdog mentality"
                ] if coach2_win_pct > coach1_win_pct else [],
                "stylistic_matchup": {
                    "tempo": "Contrasting coaching styles",
                    "advantage": favorite,
                    "critical_factor": "Which coach can impose their style on the game?"
                },
                "game_script_scenarios": [
                    {
                        "scenario": f"{favorite} Dominance",
                        "probability": favorite_prob,
                        "description": f"{favorite} imposes their will and controls the game",
                        "score_prediction": f"{favorite} wins by 10-14"
                    },
                    {
                        "scenario": f"{underdog} Upset",
                        "probability": "20-25%",
                        "description": f"{underdog} executes perfect game plan",
                        "score_prediction": f"{underdog} wins close game"
                    },
                    {
                        "scenario": "Shootout",
                        "probability": "15-20%",
                        "description": "Both offenses clicking, comes down to final possession",
                        "score_prediction": "High-scoring thriller"
                    }
                ],
                "final_prediction": {
                    "winner": f"{favorite} favored",
                    "confidence": "Moderate (60-65%)",
                    "reasoning": f"Based on career records and current season performance, {favorite} has the edge",
                    "upset_path_for_illinois": f"{underdog} must control tempo and win turnover battle"
                }
            }
        }
        
        result = {
            "coach1": coach1_data,
            "coach2": coach2_data,
            "comparative_analysis": comparative_analysis,
            "hypothetical_matchup": hypothetical_matchup
        }
        
        print(f"✅ Coach comparison data built successfully")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error getting coach comparison: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/key-players/<team1>/<team2>', methods=['GET'])
def get_key_players(team1, team2):
    """Get key player stats for matchup from coaches_master.db"""
    try:
        print(f"\n🏈 Key Players Request: {team1} vs {team2}")
        
        coaches_db_path = os.path.join(app.instance_path, 'coaches_master.db')
        conn = sqlite3.connect(coaches_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get top 5 players per team by total yards
        query = """
            SELECT player_name, position, player_id,
                   passing_yards, passing_tds, pass_attempts, completions, interceptions,
                   rushing_yards, rushing_tds, carries,
                   receiving_yards, receiving_tds, receptions,
                   (COALESCE(passing_yards,0) + COALESCE(rushing_yards,0) + COALESCE(receiving_yards,0)) as total_yards,
                   headshot_url, team_logo_url
            FROM player_season_stats 
            WHERE team = ? AND season = 2025
            ORDER BY total_yards DESC 
            LIMIT 5
        """
        
        # Fetch team1 players
        cursor.execute(query, (team1,))
        team1_players = [dict(row) for row in cursor.fetchall()]
        
        # Fetch team2 players
        cursor.execute(query, (team2,))
        team2_players = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'team1': team1,
            'team2': team2,
            'team1_players': team1_players,
            'team2_players': team2_players
        })
        
    except Exception as e:
        print(f"❌ Error getting key players: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/player-props/<team1>/<team2>', methods=['GET'])
def get_player_props(team1, team2):
    """Get player props for any matchup"""
    try:
        print(f"\n🎯 Player Props Request: {team1} vs {team2}")
        
        # Initialize props engine
        props_engine = RealDataPlayerPropsEngine()
        
        # Generate props for both teams
        team1_props = props_engine.generate_enhanced_props(team1, team2)
        team2_props = props_engine.generate_enhanced_props(team2, team1)
        
        # Format response
        response = {
            'matchup': {
                'team1': team1,
                'team2': team2
            },
            'team1_props': [
                {
                    'player_name': prop.player_name,
                    'player_team': prop.player_team,
                    'position': prop.position,
                    'prop_type': prop.prop_type,
                    'line': prop.over_under_line,
                    'over_under_line': prop.over_under_line,
                    'confidence': prop.confidence,
                    'recommendation': prop.recommendation,
                    'reasoning': prop.reasoning,
                    'season_average': prop.season_average,
                    'weather_impact': prop.weather_impact,
                    'game_logs': [asdict(log) for log in prop.game_logs],
                    'trend_analysis': asdict(prop.trend_analysis),
                    'defensive_matchup': asdict(prop.defensive_matchup),
                    'key_insights': prop.key_insights
                }
                for prop in team1_props
            ],
            'team2_props': [
                {
                    'player_name': prop.player_name,
                    'player_team': prop.player_team,
                    'position': prop.position,
                    'prop_type': prop.prop_type,
                    'line': prop.over_under_line,
                    'over_under_line': prop.over_under_line,
                    'confidence': prop.confidence,
                    'recommendation': prop.recommendation,
                    'reasoning': prop.reasoning,
                    'season_average': prop.season_average,
                    'weather_impact': prop.weather_impact,
                    'game_logs': [asdict(log) for log in prop.game_logs],
                    'trend_analysis': asdict(prop.trend_analysis),
                    'defensive_matchup': asdict(prop.defensive_matchup),
                    'key_insights': prop.key_insights
                }
                for prop in team2_props
            ],
            'total_props': len(team1_props) + len(team2_props)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error generating player props: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# n8n Integration Endpoints
@app.route('/api/current-week', methods=['GET'])
def get_current_week():
    """
    Return the current week number and game count
    Useful for n8n workflows to determine what week to fetch
    """
    try:
        # Load current week games
        with open('Currentweekgames.json', 'r') as f:
            games = json.load(f)
        
        # Determine current week
        if games and len(games) > 0:
            current_week = games[0].get('week', None)
            return jsonify({
                'current_week': current_week,
                'games_count': len(games),
                'last_updated': os.path.getmtime('Currentweekgames.json')
            }), 200
        else:
            return jsonify({
                'current_week': None,
                'games_count': 0,
                'message': 'No games data available'
            }), 200
            
    except FileNotFoundError:
        return jsonify({
            'error': 'Currentweekgames.json not found'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/webhooks/n8n/data-update', methods=['POST'])
def n8n_data_update_webhook():
    """
    Webhook endpoint for n8n to trigger after data updates
    
    Expected payload:
    {
        "week": 12,
        "games_count": 51,
        "timestamp": "2025-12-02T06:00:00Z"
    }
    """
    try:
        data = request.get_json()
        week = data.get('week')
        games_count = data.get('games_count')
        timestamp = data.get('timestamp')
        
        # Log the update
        print(f"n8n Data Update Received - Week {week}: {games_count} games at {timestamp}")
        
        # You could add validation logic here
        # For example, verify games_count is reasonable (20-60)
        if games_count and (games_count < 20 or games_count > 60):
            return jsonify({
                'status': 'warning',
                'message': f'Unusual game count: {games_count}'
            }), 200
        
        return jsonify({
            'status': 'success',
            'message': f'Week {week} data update acknowledged'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/upcoming-games', methods=['GET'])
def get_upcoming_games():
    """
    Get upcoming games from predictions database
    Supports filtering by season_type (regular or postseason)
    
    Query params:
        season_type: 'regular', 'postseason', or omit for all
    """
    try:
        import sqlite3
        
        season_type = request.args.get('season_type', None)
        
        conn = sqlite3.connect('instance/predictions.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query with optional season_type filter
        if season_type:
            cursor.execute("""
                SELECT 
                    id, start_date, week, season_type,
                    home_team, home_id, home_abbreviation, home_logo, home_color, home_alt_color, home_record, home_rank,
                    away_team, away_id, away_abbreviation, away_logo, away_color, away_alt_color, away_record, away_rank,
                    spread, over_under, home_moneyline, away_moneyline,
                    venue, neutral_site,
                    home_fpi, away_fpi, home_conference, away_conference
                FROM upcoming_games
                WHERE season_type = ?
                ORDER BY start_date ASC
            """, (season_type,))
        else:
            cursor.execute("""
                SELECT 
                    id, start_date, week, season_type,
                    home_team, home_id, home_abbreviation, home_logo, home_color, home_alt_color, home_record, home_rank,
                    away_team, away_id, away_abbreviation, away_logo, away_color, away_alt_color, away_record, away_rank,
                    spread, over_under, home_moneyline, away_moneyline,
                    venue, neutral_site,
                    home_fpi, away_fpi, home_conference, away_conference
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
                    'id': row['home_id'],
                    'team': row['home_team'],
                    'abbr': row['home_abbreviation'],
                    'logo': row['home_logo'],
                    'color': row['home_color'],
                    'altColor': row['home_alt_color'],
                    'record': row['home_record'],
                    'rank': row['home_rank'],
                    'fpi': row['home_fpi'],
                    'conference': row['home_conference']
                },
                'away': {
                    'id': row['away_id'],
                    'team': row['away_team'],
                    'abbr': row['away_abbreviation'],
                    'logo': row['away_logo'],
                    'color': row['away_color'],
                    'altColor': row['away_alt_color'],
                    'record': row['away_record'],
                    'rank': row['away_rank'],
                    'fpi': row['away_fpi'],
                    'conference': row['away_conference']
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
        return jsonify({'games': games, 'count': len(games)})
    except Exception as e:
        print(f"Error fetching upcoming games: {e}")
        return jsonify({'error': str(e)}), 500

# Serve gamedaylive.html template as main UI
@app.route('/')
@app.route('/gamedaylive')
def gamedaylive():
    """Serve the gamedaylive HTML template"""
    return render_template('gamedaylive.html')

# Serve React Predictor App at /predictor
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))  # Changed from 5001 to 5002
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    print(f"\n{'='*60}")
    print(f"🚀 Starting Flask Backend Server")
    print(f"{'='*60}")
    print(f"   Host: 0.0.0.0 (all interfaces)")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"   CORS: Enabled for localhost:5173, localhost:3000")
    print(f"{'='*60}\n")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True,
        use_reloader=debug
    )