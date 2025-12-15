#!/usr/bin/env python3
"""
AppMap Recording Script for Gameday+ Predictor
Records a trace of the prediction workflow for visualization
"""

import os
import sys
import asyncio
import json

# Enable AppMap BEFORE importing anything else
os.environ['APPMAP'] = 'true'
os.environ['APPMAP_RECORD_PROCESS'] = 'true'

# Now import appmap
import appmap
from _appmap import recorder

# Import predictor
from graphqlpredictor import LightningPredictor

API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# Team IDs (from fbs.json)
TEAMS = {
    "Ohio State": 194,
    "Michigan": 130,
    "Alabama": 333,
    "Georgia": 61,
    "Texas": 251,
    "Oregon": 2483,
    "Penn State": 213,
    "Notre Dame": 87,
    "Miami": 2390,
    "Clemson": 228
}

async def run_prediction(home_team: str, away_team: str):
    """Run a prediction and return results"""
    home_id = TEAMS.get(home_team)
    away_id = TEAMS.get(away_team)
    
    if not home_id or not away_id:
        print(f"❌ Unknown team: {home_team if not home_id else away_team}")
        return None
    
    print(f"\n🏈 Predicting: {home_team} vs {away_team}")
    print("=" * 60)
    
    predictor = LightningPredictor(API_KEY)
    result = await predictor.predict_game(home_id, away_id)
    
    return result

def main():
    # Get teams from command line or use defaults
    home_team = sys.argv[1] if len(sys.argv) > 1 else "Ohio State"
    away_team = sys.argv[2] if len(sys.argv) > 2 else "Michigan"
    
    print("🗺️  AppMap Recording: Gameday+ Prediction Workflow")
    print("=" * 60)
    print(f"Home: {home_team} | Away: {away_team}")
    
    # Start recording
    rec = recorder.Recorder.get_current()
    rec.start_recording()
    
    try:
        # Run the prediction
        result = asyncio.run(run_prediction(home_team, away_team))
        
        if result:
            print("\n✅ Prediction Complete!")
            # Get key attributes if they exist
            if hasattr(result, 'predicted_winner'):
                print(f"Winner: {result.predicted_winner}")
            if hasattr(result, 'spread'):
                print(f"Spread: {result.spread}")
            if hasattr(result, 'confidence'):
                print(f"Confidence: {result.confidence}")
    finally:
        # Stop and save recording
        recording = rec.stop_recording()
        
        # Save to file
        output_dir = "tmp/appmap"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f"{output_dir}/prediction_{home_team.replace(' ', '_')}_vs_{away_team.replace(' ', '_')}.appmap.json"
        
        # Handle different recording return types
        if hasattr(recording, 'to_dict'):
            data = recording.to_dict()
        elif isinstance(recording, list):
            data = {"events": recording, "version": "1.0", "metadata": {"name": f"{home_team} vs {away_team}"}}
        else:
            data = {"events": list(recording) if recording else [], "version": "1.0"}
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n📊 AppMap saved to: {output_file}")
        print(f"   Events recorded: {len(data.get('events', []))}")
        print("Open this file in VS Code with the AppMap extension to visualize!")

if __name__ == "__main__":
    main()
