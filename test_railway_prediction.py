#!/usr/bin/env python3
"""
Test script to diagnose prediction issues in Railway deployment
"""

import os
import sys
import traceback
import asyncio
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import sqlite3
        print("✅ sqlite3 imported successfully")
    except Exception as e:
        print(f"❌ sqlite3 import failed: {e}")
        return False
    
    try:
        from graphqlpredictor import LightningPredictor
        print("✅ LightningPredictor imported successfully")
    except Exception as e:
        print(f"❌ LightningPredictor import failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except Exception as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connectivity"""
    print("\n🗄️ Testing database connection...")
    
    try:
        import sqlite3
        
        # Test predictions.db
        if os.path.exists('instance/predictions.db'):
            conn = sqlite3.connect('instance/predictions.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM upcoming_games")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ predictions.db connected successfully ({count} games)")
        else:
            print("❌ predictions.db not found")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_predictor_creation():
    """Test creating LightningPredictor instance"""
    print("\n🤖 Testing predictor creation...")
    
    try:
        from graphqlpredictor import LightningPredictor
        
        # Use the same API key as app.py
        api_key = os.environ.get('CFB_API_KEY', 'T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p')
        predictor = LightningPredictor(api_key)
        print("✅ LightningPredictor instance created successfully")
        return predictor
    except Exception as e:
        print(f"❌ Predictor creation failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def test_simple_prediction(predictor):
    """Test a simple prediction"""
    print("\n🏈 Testing simple prediction...")
    
    try:
        # Test with team IDs instead of names
        # Ohio State ID: 194, Michigan ID: 130 (common IDs)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            prediction = loop.run_until_complete(
                predictor.predict_game(194, 130)  # Ohio State vs Michigan by ID
            )
            
            print(f"✅ Prediction successful!")
            
            # Calculate predicted winner from home_win_prob
            predicted_winner = prediction.home_team if prediction.home_win_prob > 0.5 else prediction.away_team
            print(f"   Winner: {predicted_winner}")
            print(f"   Home WP: {prediction.home_win_prob:.1%}")
            print(f"   Spread: {prediction.predicted_spread:+.1f}")
            print(f"   Total: {prediction.predicted_total:.1f}")
            return True
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_network_connectivity():
    """Test network connectivity to external APIs"""
    print("\n🌐 Testing network connectivity...")
    
    try:
        import requests
        
        # Test GraphQL API
        response = requests.get("https://api.collegefootballdata.com/", timeout=10)
        print(f"✅ CFBD API reachable (status: {response.status_code})")
        
        # Test ESPN API
        response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard", timeout=10)
        print(f"✅ ESPN API reachable (status: {response.status_code})")
        
        return True
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        return False

def main():
    print("🚀 Railway Prediction Diagnostics")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Environment: {'Railway' if os.getenv('RAILWAY_ENVIRONMENT') else 'Local'}")
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 5
    
    if test_imports():
        tests_passed += 1
    
    if test_database_connection():
        tests_passed += 1
    
    if test_network_connectivity():
        tests_passed += 1
    
    predictor = test_predictor_creation()
    if predictor:
        tests_passed += 1
        
        if test_simple_prediction(predictor):
            tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! Prediction system should work.")
    else:
        print("❌ Some tests failed. Check the output above for issues.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)