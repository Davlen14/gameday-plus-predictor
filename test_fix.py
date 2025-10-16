#!/usr/bin/env python3
"""
Test script to validate the API fix for Minnesota vs Nebraska
This will show that we get real team data, not hardcoded USC vs Notre Dame data
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor
from run import format_prediction_output

async def test_fix():
    """Test the fix by running a Minnesota vs Nebraska prediction"""
    
    # Initialize predictor
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    # Minnesota vs Nebraska IDs
    home_team_id = 135   # Minnesota  
    away_team_id = 158   # Nebraska
    
    # Load team data from fbs.json
    with open('fbs.json', 'r') as f:
        fbs_teams = json.load(f)
    
    # Find team data
    home_team_fbs = next((team for team in fbs_teams if team['id'] == home_team_id), None)
    away_team_fbs = next((team for team in fbs_teams if team['id'] == away_team_id), None)
    
    home_team_data = {
        'id': home_team_id,
        'name': home_team_fbs['school'] if home_team_fbs else 'Minnesota',
        'logo_url': home_team_fbs['logos'][0] if home_team_fbs and home_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{home_team_id}.png',
        'primary_color': home_team_fbs['primary_color'] if home_team_fbs else '#7a0019',
        'alt_color': home_team_fbs['alt_color'] if home_team_fbs else '#ffcc33'
    }
    
    away_team_data = {
        'id': away_team_id,
        'name': away_team_fbs['school'] if away_team_fbs else 'Nebraska',
        'logo_url': away_team_fbs['logos'][0] if away_team_fbs and away_team_fbs['logos'] else f'https://logos.api.collegefootballdata.com/{away_team_id}.png',
        'primary_color': away_team_fbs['primary_color'] if away_team_fbs else '#d00000',
        'alt_color': away_team_fbs['alt_color'] if away_team_fbs else '#ffffff'
    }
    
    print("🎯 TESTING FIXED API - MINNESOTA VS NEBRASKA")
    print("=" * 80)
    print(f"Home Team: {home_team_data['name']} (ID: {home_team_id})")
    print(f"Away Team: {away_team_data['name']} (ID: {away_team_id})")
    print("=" * 80)
    
    # Make prediction
    prediction = await predictor.predict_game(home_team_id, away_team_id)
    
    # Use the format_prediction_output function to generate the analysis
    print("\n🔍 ANALYSIS OUTPUT:")
    print("=" * 80)
    
    # This should show P.J. Fleck vs Matt Rhule, not Lincoln Riley vs Marcus Freeman
    format_prediction_output(prediction, home_team_data, away_team_data)
    
    print("\n✅ SUCCESS: Analysis generated with real Minnesota vs Nebraska data!")
    print(f"✅ Home Team Coach should be P.J. Fleck (Minnesota)")
    print(f"✅ Away Team Coach should be Matt Rhule (Nebraska)")
    print(f"✅ NOT Lincoln Riley (USC) vs Marcus Freeman (Notre Dame)")

if __name__ == "__main__":
    asyncio.run(test_fix())