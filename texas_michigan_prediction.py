#!/usr/bin/env python3
"""
Texas vs Michigan Bowl Game Prediction Script
"""
import asyncio
import json
from graphqlpredictor import LightningPredictor
from betting_lines_manager import betting_manager

async def texas_michigan_prediction():
    print('🏈 TEXAS vs MICHIGAN BOWL GAME PREDICTION')
    print('=' * 60)
    
    predictor = LightningPredictor('T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
    
    # Texas = 251, Michigan = 130 (verified from College Football Data API)
    texas_id = 251  # Home team
    michigan_id = 130  # Away team
    
    print(f'🔍 Running prediction: Michigan (ID: {michigan_id}) @ Texas (ID: {texas_id})')
    
    try:
        prediction = await predictor.predict_game(texas_id, michigan_id)
        
        print(f'\n🎯 FINAL PREDICTION RESULTS')
        print('━' * 50)
        
        # Win probabilities
        texas_win_prob = prediction.home_win_prob * 100
        michigan_win_prob = (1 - prediction.home_win_prob) * 100
        
        print(f'🏆 WIN PROBABILITIES:')
        print(f'   Texas (Home): {texas_win_prob:.1f}%')
        print(f'   Michigan (Away): {michigan_win_prob:.1f}%')
        
        # Spread prediction
        print(f'\n📊 SPREAD PREDICTION:')
        print(f'   Raw Spread: Texas {prediction.predicted_spread:+.1f}')
        
        if prediction.predicted_spread > 0:
            favorite = 'Texas'
            spread_value = prediction.predicted_spread
            print(f'   Formatted: Texas -{spread_value:.1f}')
        else:
            favorite = 'Michigan'
            spread_value = abs(prediction.predicted_spread)
            print(f'   Formatted: Michigan -{spread_value:.1f}')
        
        # Total prediction
        print(f'\n🔢 TOTAL PREDICTION:')
        print(f'   Predicted Total: {prediction.predicted_total:.1f}')
        
        # Final score calculation
        if hasattr(prediction, 'home_predicted_score') and prediction.home_predicted_score is not None:
            texas_score = prediction.home_predicted_score
            michigan_score = prediction.away_predicted_score
            print(f'\n🏈 FINAL SCORE (Consistent):')
        else:
            # Calculate from spread/total
            texas_score = round((prediction.predicted_total + prediction.predicted_spread) / 2)
            michigan_score = round((prediction.predicted_total - prediction.predicted_spread) / 2)
            
            # Ensure no negative scores
            if texas_score < 0:
                michigan_score += abs(texas_score)
                texas_score = 0
            elif michigan_score < 0:
                texas_score += abs(michigan_score)
                michigan_score = 0
            
            print(f'\n🏈 FINAL SCORE (Calculated):')
        
        print(f'   Michigan: {michigan_score}')
        print(f'   Texas: {texas_score}')
        print(f'   ────────────')
        print(f'   Total: {texas_score + michigan_score}')
        
        # Winner announcement
        if texas_score > michigan_score:
            margin = texas_score - michigan_score
            print(f'\n🏆 PREDICTED WINNER: Texas by {margin} points')
        elif michigan_score > texas_score:
            margin = michigan_score - texas_score
            print(f'\n🏆 PREDICTED WINNER: Michigan by {margin} points')
        else:
            print(f'\n🤝 PREDICTED: Tie Game')
        
        print(f'\n🎪 MODEL CONFIDENCE: {prediction.confidence:.1%}')
        
        # Market comparison using our College Football Data API integration
        print(f'\n💰 MARKET COMPARISON:')
        betting_analysis = betting_manager.get_betting_analysis('Texas', 'Michigan', prediction.predicted_spread, prediction.predicted_total)
        
        market_spread = betting_analysis.get('market_spread', 0)
        market_total = betting_analysis.get('market_total', 0)
        
        print(f'   Market Spread: Texas {market_spread:+.1f}')
        print(f'   Market Total: {market_total:.1f}')
        print(f'   Data Source: {betting_analysis.get("data_source", "N/A")}')
        
        # Calculate edges
        spread_edge = abs(prediction.predicted_spread - market_spread) if market_spread != 0 else 0
        total_edge = abs(prediction.predicted_total - market_total) if market_total != 0 else 0
        
        print(f'\n🎯 VALUE ANALYSIS:')
        print(f'   Spread Edge: {spread_edge:.1f} points')
        print(f'   Total Edge: {total_edge:.1f} points')
        
        # Betting recommendations
        spread_rec = betting_analysis.get('spread_recommendation', 'No recommendation')
        total_rec = betting_analysis.get('total_recommendation', 'No recommendation')
        
        print(f'\n🎲 BETTING RECOMMENDATIONS:')
        print(f'   Spread: {spread_rec}')
        print(f'   Total: {total_rec}')
        
        # Individual sportsbook lines
        sportsbooks = betting_analysis.get('sportsbooks', {}).get('individual_books', [])
        if sportsbooks:
            print(f'\n📊 SPORTSBOOK LINES:')
            for book in sportsbooks:
                provider = book.get('provider', 'Unknown')
                book_spread = book.get('spread', 'N/A')
                book_total = book.get('overUnder', 'N/A')
                print(f'   {provider}: Texas {book_spread}, O/U {book_total}')
        
        print('\n' + '━' * 60)
        print('✅ PREDICTION COMPLETE!')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(texas_michigan_prediction())