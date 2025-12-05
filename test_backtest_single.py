#!/usr/bin/env python3
"""
Single Game Backtest - Oregon vs USC Week 13
"""

import json
import asyncio
import requests
from graphqlpredictor import LightningPredictor

async def main():
    # Initialize predictor
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key=api_key)
    
    print("🏈 SINGLE GAME BACKTEST - Oregon vs USC")
    print("=" * 80)
    
    # Oregon ID: 2483, USC ID: 30
    oregon_id = 2483
    usc_id = 30
    
    # Fetch actual result
    url = "https://graphql.collegefootballdata.com/v1/graphql"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    query = """
    query GetOregonUSC {
      game(where: {
        season: {_eq: 2025}, 
        week: {_eq: 13}, 
        seasonType: {_eq: "regular"},
        _or: [
          {homeTeamId: {_eq: 2483}, awayTeamId: {_eq: 30}},
          {homeTeamId: {_eq: 30}, awayTeamId: {_eq: 2483}}
        ]
      }) {
        id
        homeTeamId
        homeTeam
        homePoints
        awayTeamId
        awayTeam
        awayPoints
      }
    }
    """
    
    response = requests.post(url, json={"query": query}, headers=headers)
    result = response.json()
    
    if 'errors' in result:
        print(f"❌ GraphQL Errors: {result['errors']}")
        return
    
    games = result['data']['game']
    
    if not games:
        print("❌ No game found")
        return
    
    game = games[0]
    
    # Use market spread from our predictions file
    market_spread = -10.0  # USC was +10 underdog
    lines = [{'provider': 'Market Consensus', 'spread': market_spread, 'overUnder': 62.5}]
    
    print(f"\n📊 ACTUAL RESULT:")
    print(f"   {game['awayTeam']} @ {game['homeTeam']}")
    print(f"   Score: {game['awayTeam']} {game['awayPoints']}, {game['homeTeam']} {game['homePoints']}")
    
    actual_margin = game['homePoints'] - game['awayPoints']
    actual_winner = game['homeTeam'] if actual_margin > 0 else game['awayTeam']
    print(f"   Margin: {game['homeTeam']} {actual_margin:+.1f}")
    print(f"   Winner: {actual_winner}")
    
    # Get market lines
    if lines:
        print(f"\n💰 BETTING LINES:")
        for line in lines:
            print(f"   {line['provider']}: Spread {line['spread']:+.1f}, O/U {line['overUnder']}")
        
        # Calculate consensus
        spreads = [l['spread'] for l in lines if l.get('spread')]
        market_spread = sum(spreads) / len(spreads) if spreads else None
        print(f"   Consensus Spread: {market_spread:+.1f}" if market_spread else "   No spread data")
    
    # Generate model prediction
    print(f"\n🤖 GENERATING MODEL PREDICTION...")
    
    # Determine home/away IDs
    home_id = game['homeTeamId']
    away_id = game['awayTeamId']
    
    prediction = await predictor.predict_game(home_id, away_id)
    
    # Extract prediction from object attributes (not detailed_analysis dict)
    predicted_spread = prediction.predicted_spread
    predicted_total = prediction.predicted_total
    confidence = prediction.confidence * 100
    home_win_prob = prediction.home_win_prob * 100
    
    # Calculate scores from spread and total
    # Spread is from home team's perspective (negative = home favored)
    # Oregon -12.3 means Oregon wins by 12.3
    # Total 69.5: Oregon 41, USC 29
    home_score = (predicted_total - predicted_spread) / 2  # (69.5 - (-12.3)) / 2 = 40.9
    away_score = (predicted_total + predicted_spread) / 2  # (69.5 + (-12.3)) / 2 = 28.6
    
    # Predicted winner: negative spread means home team favored
    predicted_winner = game['homeTeam'] if predicted_spread < 0 else game['awayTeam']
    
    print(f"\n🎯 MODEL PREDICTION:")
    print(f"   Predicted Score: {game['awayTeam']} {away_score:.0f}, {game['homeTeam']} {home_score:.0f}")
    print(f"   Predicted Spread: {game['homeTeam']} {predicted_spread:+.1f}")
    print(f"   Predicted Winner: {predicted_winner} ({home_win_prob:.1f}% confidence)")
    
    # Analysis
    print(f"\n📊 ANALYSIS:")
    winner_correct = (predicted_winner == actual_winner)
    spread_error = abs(predicted_spread - actual_margin)
    
    print(f"   ✅ Winner: {'CORRECT' if winner_correct else 'WRONG'}")
    print(f"   📏 Spread Error: {spread_error:.1f} points")
    
    if market_spread:
        model_edge = predicted_spread - market_spread
        print(f"   💰 Model vs Market Edge: {model_edge:+.1f} points")
        
        # Check ATS result
        if abs(model_edge) >= 3.0:
            # Bet the side with the edge
            if model_edge < 0:
                # Model has home team winning by more than market (Oregon -12.3 vs -10)
                # Bet home team to cover
                bet_team = game['homeTeam']
                bet_line = market_spread
                # Did home team cover the spread?
                ats_margin = actual_margin - abs(market_spread)
                ats_result = ats_margin > 0
            else:
                # Model has away team covering better than market
                # Bet away team + points
                bet_team = game['awayTeam']
                bet_line = market_spread
                # Did away team cover?
                ats_margin = (game['awayPoints'] + abs(market_spread)) - game['homePoints']
                ats_result = ats_margin > 0
            
            print(f"   🎯 Recommended Bet: {bet_team} {bet_line:+.1f} (edge: {abs(model_edge):.1f})")
            print(f"   {'✅ BET WON' if ats_result else '❌ BET LOST'}")

if __name__ == "__main__":
    asyncio.run(main())
