#!/usr/bin/env python3
"""
Test the enhanced player analysis with comprehensive JSON files
"""

import asyncio
from graphqlpredictor import LightningPredictor

async def test_enhanced_player_analysis():
    """Test enhanced player analysis"""
    
    # Initialize predictor with API key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🏈 Testing Enhanced Player Analysis")
    print("=" * 50)
    
    # Test with USC vs Notre Dame (known teams with likely player data)
    home_team_id = 30   # USC  
    away_team_id = 87   # Notre Dame
    
    print(f"🎯 Testing: Notre Dame @ USC")
    print(f"Team IDs: {away_team_id} @ {home_team_id}")
    
    try:
        # Run the prediction with enhanced player analysis
        prediction = await predictor.predict_game(
            home_team_id=home_team_id,
            away_team_id=away_team_id
        )
        
        if prediction:
            print(f"\n✅ Enhanced Player Analysis Test Successful!")
            print(f"   Winner: {'USC' if prediction.home_win_prob > 50 else 'Notre Dame'}")
            print(f"   Confidence: {prediction.confidence:.1f}%")
            print(f"   Spread: {prediction.predicted_spread:+.1f} (Home)")
        else:
            print("❌ Enhanced Player Analysis Test Failed")
            
    except Exception as e:
        print(f"❌ Error during enhanced player analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_player_analysis())