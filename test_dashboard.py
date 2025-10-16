#!/usr/bin/env python3
"""
Test the new dashboard output format
"""

import asyncio
from run import TeamMapper, format_prediction_output
from graphqlpredictor import LightningPredictor

async def main():
    # API Key for College Football Data
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    # Initialize team mapper and predictor
    team_mapper = TeamMapper()
    predictor = LightningPredictor(api_key)
    
    try:
        # Fetch teams from REST API
        print("🔄 Fetching teams from REST API...")
        teams_loaded = await team_mapper.fetch_teams()
        
        if not teams_loaded:
            print("❌ Could not load teams from REST API. Make sure app.py is running on port 8080")
            return
        
        # Define teams by name instead of ID
        home_team_name = "Illinois"
        away_team_name = "Ohio State"
        
        # Get team data from REST API
        home_team_data = team_mapper.get_team_id(home_team_name)
        away_team_data = team_mapper.get_team_id(away_team_name)
        
        # Make prediction using IDs
        prediction = await predictor.predict_game(home_team_data['id'], away_team_data['id'])
        
        # Format and display the prediction
        format_prediction_output(prediction, home_team_data, away_team_data)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
