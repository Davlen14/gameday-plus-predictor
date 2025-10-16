#!/usr/bin/env python3
"""
Final verification script - Test the complete fix
This validates that the API produces 100% dynamic output with real team data
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor
from app import format_prediction_for_api

async def final_verification():
    """Final test to confirm the fix worked"""
    
    print("🎯 FINAL VERIFICATION - API BACKEND FIX")
    print("=" * 80)
    
    # Initialize predictor with real API
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    # Test with Minnesota vs Nebraska (our verification case)
    home_team_id = 135   # Minnesota  
    away_team_id = 158   # Nebraska
    
    # Load team data
    with open('fbs.json', 'r') as f:
        fbs_teams = json.load(f)
    
    home_team_fbs = next((team for team in fbs_teams if team['id'] == home_team_id), None)
    away_team_fbs = next((team for team in fbs_teams if team['id'] == away_team_id), None)
    
    home_team_data = {
        'id': home_team_id,
        'name': home_team_fbs['school'],
        'logo_url': home_team_fbs['logos'][0] if home_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
        'primary_color': home_team_fbs['primary_color'],
        'alt_color': home_team_fbs['alt_color']
    }
    
    away_team_data = {
        'id': away_team_id,
        'name': away_team_fbs['school'], 
        'logo_url': away_team_fbs['logos'][0] if away_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
        'primary_color': away_team_fbs['primary_color'],
        'alt_color': away_team_fbs['alt_color']
    }
    
    print(f"Testing: {away_team_data['name']} @ {home_team_data['name']}")
    
    # Make real prediction
    prediction = await predictor.predict_game(home_team_id, away_team_id)
    
    # Use the new API format function
    result = format_prediction_for_api(prediction, home_team_data, away_team_data)
    
    # Verify the results
    print("\n🔍 VERIFICATION RESULTS:")
    print("=" * 50)
    
    analysis = result['formatted_analysis']
    ui_components = result['ui_components']
    
    # Check 1: Real team names
    if prediction.home_team in analysis and prediction.away_team in analysis:
        print(f"✅ Real team names: {prediction.home_team} & {prediction.away_team}")
    else:
        print("❌ Team names not found in analysis")
    
    # Check 2: No hardcoded USC/Notre Dame
    if 'USC' not in analysis and 'Notre Dame' not in analysis:
        print("✅ No hardcoded USC/Notre Dame teams")
    else:
        print("❌ Still contains hardcoded teams!")
    
    # Check 3: Real coaches (P.J. Fleck, Matt Rhule)
    if 'P.J. Fleck' in analysis and 'Matt Rhule' in analysis:
        print("✅ Real coaches: P.J. Fleck (Minnesota) & Matt Rhule (Nebraska)")
    elif 'Lincoln Riley' in analysis or 'Marcus Freeman' in analysis:
        print("❌ Still has hardcoded coaches!")
    else:
        print("⚠️  Coaches not clearly identified")
    
    # Check 4: UI Components structure
    if 'team_selector' in ui_components and 'header' in ui_components:
        print("✅ Proper UI components structure")
    else:
        print("❌ Missing UI components")
    
    # Check 5: Dynamic prediction values
    if hasattr(prediction, 'home_win_prob') and prediction.home_win_prob != 0.577:
        print(f"✅ Dynamic win probability: {prediction.home_win_prob:.1%}")
    else:
        print("❌ Win probability might be hardcoded")
    
    # Check 6: JSON serializable
    try:
        json.dumps(result)
        print("✅ Result is JSON serializable")
    except:
        print("❌ Result not JSON serializable")
    
    print("\n🎯 FINAL RESULT:")
    print("=" * 50)
    
    if ('P.J. Fleck' in analysis and 'Matt Rhule' in analysis and 
        'USC' not in analysis and 'Notre Dame' not in analysis):
        print("🎉 SUCCESS! API backend is now 100% dynamic!")
        print("🎉 No more hardcoded USC vs Notre Dame data!")
        print("🎉 Real coaches and team data are being used!")
        return True
    else:
        print("❌ Fix incomplete - still has hardcoded elements")
        return False

if __name__ == "__main__":
    success = asyncio.run(final_verification())
    if success:
        print("\n✅ BACKEND FIX VERIFIED AND COMPLETE!")
    else:
        print("\n❌ Additional fixes needed")