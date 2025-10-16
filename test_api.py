#!/usr/bin/env python3
"""
Test script for the Gameday GraphQL Predictor API
Usage: python test_api.py [base_url]
"""

import requests
import json
import sys

def test_api(base_url="http://localhost:5002"):
    print(f"Testing API at: {base_url}")
    print("="*50)
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50)
    
    # Test prediction endpoint
    print("2. Testing prediction (Illinois vs Ohio State)...")
    try:
        response = requests.get(f"{base_url}/predict/356/194")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                pred = data['prediction']
                print("✅ Prediction successful!")
                print(f"Game: {pred['away_team']} @ {pred['home_team']}")
                print(f"Winner: {pred['predicted_winner']}")
                print(f"Score: {pred['away_team']} {pred['away_score']} - {pred['home_team']} {pred['home_score']}")
                print(f"Spread: {pred['home_team']} {pred['spread']:+.1f}")
                print(f"Total: {pred['total']}")
                print(f"Home Win %: {pred['home_win_probability']:.1f}%")
                print(f"Confidence: {pred['confidence']:.1f}%")
            else:
                print("❌ Prediction failed")
                print(f"Response: {data}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5002"
    test_api(base_url)