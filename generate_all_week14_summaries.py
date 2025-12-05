#!/usr/bin/env python3
"""
Generate game summaries for all Week 14 games from Currentweekgames.json
"""

import json
import asyncio
import os
from graphqlpredictor import LightningPredictor

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
    
    raise ValueError(f"Team '{team_name}' not found in fbs.json")

async def generate_all_summaries():
    """Generate summaries for all games in current week"""
    
    # Load current week games
    print("📊 Loading Week 14 games...")
    with open('Currentweekgames.json', 'r') as f:
        games_data = json.load(f)
    
    all_games = games_data['games']['all']
    print(f"Found {len(all_games)} games to analyze\n")
    
    # Initialize predictor
    print("⚡ Initializing LightningPredictor...")
    api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    predictor = LightningPredictor(api_key)
    
    # Store game results for sorting
    game_results = []
    
    # Process each game
    for idx, game in enumerate(all_games, 1):
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        
        print(f"\n[{idx}/{len(all_games)}] Analyzing {away_team} @ {home_team}...")
        
        try:
            # Convert team names to IDs
            home_team_id = get_team_id(home_team)
            away_team_id = get_team_id(away_team)
            
            # Run prediction
            prediction = await predictor.predict_game(home_team_id, away_team_id)
            
            # Extract key data
            home_win_prob = prediction.home_win_prob * 100
            away_win_prob = (1 - prediction.home_win_prob) * 100
            predicted_spread = prediction.predicted_spread
            predicted_total = prediction.predicted_total
            
            # Determine winner and spread display
            if home_win_prob > away_win_prob:
                winner = home_team
                winner_prob = home_win_prob
            else:
                winner = away_team
                winner_prob = away_win_prob
            
            if predicted_spread > 0:
                favored = home_team
                spread_val = predicted_spread
            else:
                favored = away_team
                spread_val = abs(predicted_spread)
            
            spread_display = f"{favored} -{spread_val:.1f}"
            
            # Get team stats
            home_stats = getattr(prediction, 'home_team_stats', None)
            away_stats = getattr(prediction, 'away_team_stats', None)
            
            home_epa_off = home_stats.epa_offense if home_stats else 0
            home_epa_def = home_stats.epa_defense if home_stats else 0
            away_epa_off = away_stats.epa_offense if away_stats else 0
            away_epa_def = away_stats.epa_defense if away_stats else 0
            
            home_succ_off = home_stats.success_rate_offense * 100 if home_stats else 0
            home_succ_def = home_stats.success_rate_defense * 100 if home_stats else 0
            away_succ_off = away_stats.success_rate_offense * 100 if away_stats else 0
            away_succ_def = away_stats.success_rate_defense * 100 if away_stats else 0
            
            # Get FPI ratings from detailed_analysis
            home_fpi = 0
            away_fpi = 0
            if hasattr(prediction, 'detailed_analysis') and prediction.detailed_analysis:
                ratings = prediction.detailed_analysis.get('ratings', {})
                home_fpi = ratings.get('home', {}).get('fpi', 0)
                away_fpi = ratings.get('away', {}).get('fpi', 0)
            
            # Calculate edge scores (simplified)
            home_edge = 0
            away_edge = 0
            
            if home_win_prob > 50:
                home_edge += (home_win_prob - 50) * 0.6
            else:
                away_edge += (away_win_prob - 50) * 0.6
            
            if (home_epa_off + abs(home_epa_def)) > (away_epa_off + abs(away_epa_def)):
                home_edge += 12.5
            else:
                away_edge += 12.5
            
            if home_fpi > away_fpi:
                home_edge += min(abs(home_fpi - away_fpi) * 0.5, 20)
            else:
                away_edge += min(abs(home_fpi - away_fpi) * 0.5, 20)
            
            # Build advantages lists
            home_advantages = []
            away_advantages = []
            
            if home_epa_off > away_epa_off:
                home_advantages.append(f"Superior offensive EPA: {home_epa_off:+.3f} vs {away_epa_off:+.3f}")
            else:
                away_advantages.append(f"Superior offensive EPA: {away_epa_off:+.3f} vs {home_epa_off:+.3f}")
            
            if home_epa_def < away_epa_def:
                home_advantages.append(f"Stronger defensive EPA: {home_epa_def:+.3f} vs {away_epa_def:+.3f}")
            else:
                away_advantages.append(f"Stronger defensive EPA: {away_epa_def:+.3f} vs {home_epa_def:+.3f}")
            
            if home_fpi > away_fpi:
                home_advantages.append(f"Higher FPI rating: {home_fpi:.1f} vs {away_fpi:.1f}")
            elif away_fpi > home_fpi:
                away_advantages.append(f"Higher FPI rating: {away_fpi:.1f} vs {home_fpi:.1f}")
            
            if home_succ_off > away_succ_off:
                home_advantages.append(f"Better offensive success rate: {home_succ_off:.1f}% vs {away_succ_off:.1f}%")
            else:
                away_advantages.append(f"Better offensive success rate: {away_succ_off:.1f}% vs {home_succ_off:.1f}%")
            
            if home_succ_def < away_succ_def:
                home_advantages.append(f"Better defensive success rate: {home_succ_def:.1f}% vs {away_succ_def:.1f}%")
            else:
                away_advantages.append(f"Better defensive success rate: {away_succ_def:.1f}% vs {home_succ_def:.1f}%")
            
            home_advantages.append("Home field advantage")
            
            # Calculate projected scores
            home_proj_score = predicted_total / 2 + predicted_spread / 2
            away_proj_score = predicted_total / 2 - predicted_spread / 2
            
            # Matchup interpretation
            if spread_val > 14:
                matchup_type = "decisive"
            elif spread_val > 7:
                matchup_type = "moderate"
            else:
                matchup_type = "close"
            
            # Total interpretation
            if predicted_total > 60:
                total_desc = "High-scoring game expected"
            elif predicted_total > 50:
                total_desc = "Moderate-scoring game expected"
            else:
                total_desc = "Low-scoring game expected"
            
            # Confidence
            confidence = prediction.confidence * 100
            if confidence > 75:
                conf_level = "High"
            elif confidence > 60:
                conf_level = "Moderate"
            else:
                conf_level = "Low"
            
            # Extract betting lines from game data
            betting_lines = game.get('bettingLines', {})
            consensus = betting_lines.get('consensus', {})
            market_spread = consensus.get('spread', None)
            market_total = consensus.get('total', None)
            providers = betting_lines.get('allProviders', [])
            
            # Calculate betting edge and recommendations
            spread_edge = None
            total_edge = None
            spread_recommendation = None
            total_recommendation = None
            best_spread_bet = None
            best_total_bet = None
            
            if market_spread is not None:
                # Spread edge: Model spread - Market spread (from home team perspective)
                spread_edge = predicted_spread - market_spread
                
                # Recommend bet if edge > 3 points
                if abs(spread_edge) >= 3.0:
                    if spread_edge > 0:
                        # Model has HOME winning by LESS than market (or losing by more)
                        # Example: Model -4.3, Market -6.8, Edge = +2.5
                        # Bet AWAY team to cover
                        spread_recommendation = f"{away_team} {-market_spread:+.1f}"
                        best_spread_bet = "AWAY"
                    else:
                        # Model has HOME winning by MORE than market (or losing by less)
                        # Example: Model -10, Market -7, Edge = -3
                        # Bet HOME team to cover  
                        spread_recommendation = f"{home_team} {market_spread:+.1f}"
                        best_spread_bet = "HOME"
            
            if market_total is not None:
                # Total edge: Model total - Market total
                total_edge = predicted_total - market_total
                
                # Recommend bet if edge > 4 points
                if abs(total_edge) >= 4.0:
                    if total_edge > 0:
                        total_recommendation = f"OVER {market_total}"
                    else:
                        total_recommendation = f"UNDER {market_total}"
            
            # Store game result
            game_results.append({
                'home_team': home_team,
                'away_team': away_team,
                'winner': winner,
                'winner_prob': winner_prob,
                'spread_display': spread_display,
                'spread_val': spread_val,
                'favored': favored,
                'matchup_type': matchup_type,
                'home_win_prob': home_win_prob,
                'away_win_prob': away_win_prob,
                'home_proj_score': home_proj_score,
                'away_proj_score': away_proj_score,
                'market_spread': market_spread,
                'market_total': market_total,
                'spread_edge': spread_edge,
                'total_edge': total_edge,
                'spread_recommendation': spread_recommendation,
                'total_recommendation': total_recommendation,
                'best_spread_bet': best_spread_bet,
                'providers': providers,
                'predicted_total': predicted_total,
                'total_desc': total_desc,
                'home_edge': home_edge,
                'away_edge': away_edge,
                'home_epa_off': home_epa_off,
                'home_epa_def': home_epa_def,
                'away_epa_off': away_epa_off,
                'away_epa_def': away_epa_def,
                'home_fpi': home_fpi,
                'away_fpi': away_fpi,
                'home_succ_off': home_succ_off,
                'home_succ_def': home_succ_def,
                'away_succ_off': away_succ_off,
                'away_succ_def': away_succ_def,
                'home_advantages': home_advantages,
                'away_advantages': away_advantages,
                'confidence': confidence,
                'conf_level': conf_level
            })
            
            print(f"✅ Complete: {winner} {winner_prob:.0f}% ({spread_display})")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            game_results.append({
                'home_team': home_team,
                'away_team': away_team,
                'error': str(e),
                'winner_prob': 0
            })
            continue
    
    # Sort games by win probability (highest confidence first)
    game_results.sort(key=lambda x: x.get('winner_prob', 0), reverse=True)
    
    # Build output
    output_lines = []
    output_lines.append("# Week 14 Game Predictions - Sorted by Confidence")
    output_lines.append(f"\nGenerated: {games_data['summary']['generatedAt']}")
    output_lines.append(f"Total Games: {len(all_games)}")
    output_lines.append("Sorted by: Win Probability (Highest Confidence First)\n")
    output_lines.append("---\n")
    
    # Add games to output
    for game_data in game_results:
        if 'error' in game_data:
            output_lines.append(f"## {game_data['away_team']} @ {game_data['home_team']}\n")
            output_lines.append(f"⚠️ **Prediction failed:** {game_data['error']}\n")
            output_lines.append("---\n")
            continue
        
        # Extract data
        home_team = game_data['home_team']
        away_team = game_data['away_team']
        winner = game_data['winner']
        winner_prob = game_data['winner_prob']
        spread_display = game_data['spread_display']
        spread_val = game_data['spread_val']
        favored = game_data['favored']
        matchup_type = game_data['matchup_type']
        home_win_prob = game_data['home_win_prob']
        away_win_prob = game_data['away_win_prob']
        home_proj_score = game_data['home_proj_score']
        away_proj_score = game_data['away_proj_score']
        predicted_total = game_data['predicted_total']
        total_desc = game_data['total_desc']
        home_edge = game_data['home_edge']
        away_edge = game_data['away_edge']
        home_epa_off = game_data['home_epa_off']
        home_epa_def = game_data['home_epa_def']
        away_epa_off = game_data['away_epa_off']
        away_epa_def = game_data['away_epa_def']
        home_fpi = game_data['home_fpi']
        away_fpi = game_data['away_fpi']
        home_succ_off = game_data['home_succ_off']
        home_succ_def = game_data['home_succ_def']
        away_succ_off = game_data['away_succ_off']
        away_succ_def = game_data['away_succ_def']
        home_advantages = game_data['home_advantages']
        away_advantages = game_data['away_advantages']
        confidence = game_data['confidence']
        conf_level = game_data['conf_level']
        market_spread = game_data.get('market_spread')
        market_total = game_data.get('market_total')
        spread_edge = game_data.get('spread_edge')
        total_edge = game_data.get('total_edge')
        spread_recommendation = game_data.get('spread_recommendation')
        total_recommendation = game_data.get('total_recommendation')
        providers = game_data.get('providers', [])
        
        # Add to output
        output_lines.append(f"## {away_team} @ {home_team}\n")
        output_lines.append(f"### Game Summary & Prediction Rationale\n")
        output_lines.append(f"**{winner}**  ")
        output_lines.append(f"Predicted Winner\n")
        output_lines.append(f"**{winner}**  ")
        output_lines.append(f"**{winner_prob:.0f}% Win Probability**\n")
        output_lines.append(f"**{spread_display}**\n")
        output_lines.append(f"{favored} is favored by {spread_val:.1f} points. This indicates a {matchup_type} matchup.\n")
        
        # Add betting analysis section if lines available
        if market_spread is not None or market_total is not None:
            output_lines.append(f"#### 💰 Betting Analysis\n")
            
            if market_spread is not None:
                output_lines.append(f"**Market Spread:** {home_team} {market_spread:+.1f}")
                output_lines.append(f"**Model Spread:** {spread_display}")
                output_lines.append(f"**Edge:** {spread_edge:+.1f} points\n")
                
                if spread_recommendation:
                    output_lines.append(f"🎯 **RECOMMENDED BET:** {spread_recommendation}")
                    output_lines.append(f"   *(Edge of {abs(spread_edge):.1f} points)*\n")
                else:
                    output_lines.append(f"⚠️  No strong edge on spread (< 3 points)\n")
            
            if market_total is not None:
                output_lines.append(f"**Market Total:** {market_total}")
                output_lines.append(f"**Model Total:** {predicted_total:.1f}")
                output_lines.append(f"**Edge:** {total_edge:+.1f} points\n")
                
                if total_recommendation:
                    output_lines.append(f"🎯 **RECOMMENDED BET:** {total_recommendation}")
                    output_lines.append(f"   *(Edge of {abs(total_edge):.1f} points)*\n")
                else:
                    output_lines.append(f"⚠️  No strong edge on total (< 4 points)\n")
            
            # Show available sportsbook lines
            if providers:
                output_lines.append(f"**Available Lines:**")
                for provider in providers:
                    prov_name = provider.get('provider', 'Unknown')
                    prov_spread = provider.get('spread')
                    prov_total = provider.get('overUnder')
                    if prov_spread is not None:
                        output_lines.append(f"  - {prov_name}: {home_team} {prov_spread:+.1f}, O/U {prov_total}")
                output_lines.append("")
        
        output_lines.append(f"#### Win Probability")
        output_lines.append(f"- **{home_team}**: {home_win_prob:.0f}%")
        output_lines.append(f"- **{away_team}**: {away_win_prob:.0f}%\n")
        
        output_lines.append(f"#### Projected Score")
        output_lines.append(f"- **{home_team}**: {home_proj_score:.1f}")
        output_lines.append(f"- **{away_team}**: {away_proj_score:.1f}\n")
        
        output_lines.append(f"#### Projected Total")
        output_lines.append(f"**{predicted_total:.1f}**  ")
        output_lines.append(f"{total_desc}\n")
        
        output_lines.append(f"#### Overall Edge Analysis")
        output_lines.append(f"- **{home_team}**: {home_edge:.1f} Edge Score")
        output_lines.append(f"- **{away_team}**: {away_edge:.1f} Edge Score")
        output_lines.append(f"- {winner} holds a {abs(home_edge - away_edge):.1f} point overall edge\n")
        
        output_lines.append(f"#### Critical Stats Comparison\n")
        output_lines.append(f"**EPA Performance**")
        output_lines.append(f"- **{home_team}**: Off: {home_epa_off:+.3f} | Def: {home_epa_def:+.3f}")
        output_lines.append(f"- **{away_team}**: Off: {away_epa_off:+.3f} | Def: {away_epa_def:+.3f}\n")
        
        output_lines.append(f"**FPI Rating**")
        output_lines.append(f"- **{home_team}**: {home_fpi:.1f}")
        output_lines.append(f"- **{away_team}**: {away_fpi:.1f}\n")
        
        output_lines.append(f"**Success Rates**")
        output_lines.append(f"- **{home_team}**: Off: {home_succ_off:.1f}% | Def: {home_succ_def:.1f}%")
        output_lines.append(f"- **{away_team}**: Off: {away_succ_off:.1f}% | Def: {away_succ_def:.1f}%\n")
        
        output_lines.append(f"#### Key Advantages\n")
        output_lines.append(f"**{home_team} Advantages**")
        for adv in home_advantages:
            output_lines.append(f"- {adv}")
        
        output_lines.append(f"\n**{away_team} Advantages**")
        for adv in away_advantages:
            output_lines.append(f"- {adv}")
        
        output_lines.append(f"\n#### The Bottom Line")
        output_lines.append(f"**Confidence:** {conf_level} ({confidence:.0f}%)")
        output_lines.append(f"**Recommendation:** {spread_display}\n")
        
        output_lines.append(f"{favored} holds the edge in this matchup with a {max(home_win_prob, away_win_prob):.1f}% win probability. ")
        output_lines.append(f"The model projects a {spread_val:.1f}-point margin of victory.\n")
        
        output_lines.append("---\n")
    
    # Write output file
    output_file = 'Week14_Game_Summaries.md'
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n✅ Complete! Output saved to {output_file}")
    print(f"📊 Total games analyzed: {len(all_games)}")

if __name__ == "__main__":
    asyncio.run(generate_all_summaries())
