#!/usr/bin/env python3
"""
Full Integration Test - React Frontend + Flask Backend
Tests both the backend API and verifies React components will connect properly
"""

import json
import time
import subprocess
import sys
from pathlib import Path

def test_backend_api():
    """Test the Flask backend directly"""
    print("🎯 TESTING FLASK BACKEND API")
    print("=" * 60)
    
    try:
        # Import and test the Flask app
        from app import app
        
        # Create test client
        client = app.test_client()
        
        # Test home endpoint
        print("✅ Testing home endpoint...")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.get_json()}")
        
        # Test predict endpoint with Minnesota vs Nebraska
        print("\n✅ Testing prediction endpoint...")
        test_data = {
            "home_team": "Minnesota",
            "away_team": "Nebraska"
        }
        
        response = client.post('/predict', 
                            json=test_data,
                            headers={'Content-Type': 'application/json'})
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Success! Got prediction for {data.get('home_team')} vs {data.get('away_team')}")
            print(f"   📊 Win Probability: {data.get('home_win_probability', 0):.1f}%")
            print(f"   📊 Spread: {data.get('spread', 'N/A')}")
            print(f"   📊 Total: {data.get('total', 'N/A')}")
            print(f"   📊 Confidence: {data.get('confidence', 'N/A')}")
            
            # Check for real coach names (not hardcoded USC/Notre Dame)
            formatted_analysis = data.get('formatted_analysis', '')
            if 'P.J. Fleck' in formatted_analysis and 'Matt Rhule' in formatted_analysis:
                print("   ✅ Real coaches detected - no hardcoded data!")
            elif 'Lincoln Riley' in formatted_analysis or 'Marcus Freeman' in formatted_analysis:
                print("   ❌ Still contains hardcoded USC/Notre Dame coaches!")
                return False
            
            return True
        else:
            print(f"   ❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Backend test failed: {e}")
        return False

def test_frontend_structure():
    """Test that React frontend has all required components"""
    print("\n🎯 TESTING REACT FRONTEND STRUCTURE")
    print("=" * 60)
    
    frontend_path = Path("frontend/src")
    
    # Check main files
    required_files = [
        "App.tsx",
        "store.js", 
        "services/apiClient.js",
        "components/figma/TeamSelector.tsx",
        "components/figma/PredictionCards.tsx",
        "components/figma/Header.tsx"
    ]
    
    missing_files = []
    for file in required_files:
        if not (frontend_path / file).exists():
            missing_files.append(file)
        else:
            print(f"   ✅ Found: {file}")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    
    # Check component imports in App.tsx
    app_file = frontend_path / "App.tsx"
    try:
        content = app_file.read_text()
        
        # Count component imports
        import_lines = [line for line in content.split('\n') if 'import {' in line and 'figma' in line]
        print(f"\n   📊 Component imports found: {len(import_lines)}")
        
        # Check for key components
        key_components = ['TeamSelector', 'PredictionCards', 'Header', 'EPAComparison', 'AdvancedMetrics']
        found_components = []
        
        for comp in key_components:
            if comp in content:
                found_components.append(comp)
                print(f"   ✅ Component: {comp}")
        
        print(f"\n   📊 Total components rendered: {len([line for line in content.split('\n') if '<' in line and '/>' in line])}")
        
        return len(found_components) >= 4
        
    except Exception as e:
        print(f"   ❌ Error reading App.tsx: {e}")
        return False

def test_api_client_config():
    """Test API client configuration"""
    print("\n🎯 TESTING API CLIENT CONFIGURATION")
    print("=" * 60)
    
    try:
        api_file = Path("frontend/src/services/apiClient.js")
        content = api_file.read_text()
        
        # Check API base URL
        if "localhost:5002" in content:
            print("   ✅ API base URL configured for Flask backend")
        else:
            print("   ❌ API base URL not found or incorrect")
            return False
            
        # Check getPrediction method
        if "getPrediction" in content and "POST" in content:
            print("   ✅ getPrediction method properly configured")
        else:
            print("   ❌ getPrediction method missing or incorrect")
            return False
            
        # Check JSON structure
        if "home_team" in content and "away_team" in content:
            print("   ✅ Correct JSON payload structure")
            return True
        else:
            print("   ❌ JSON payload structure incorrect")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking API client: {e}")
        return False

def test_store_configuration():
    """Test Zustand store setup"""
    print("\n🎯 TESTING ZUSTAND STORE CONFIGURATION")
    print("=" * 60)
    
    try:
        store_file = Path("frontend/src/store.js")
        content = store_file.read_text()
        
        # Check key store functions
        functions_to_check = ['fetchPrediction', 'setPredictionData', 'predictionLoading']
        found_functions = []
        
        for func in functions_to_check:
            if func in content:
                found_functions.append(func)
                print(f"   ✅ Store function: {func}")
        
        # Check API client import
        if "ApiClient" in content:
            print("   ✅ ApiClient properly imported")
        else:
            print("   ❌ ApiClient not imported")
            return False
            
        return len(found_functions) >= 3
        
    except Exception as e:
        print(f"   ❌ Error checking store: {e}")
        return False

def run_integration_test():
    """Run the complete integration test"""
    print("🚀 GAMEDAY+ FULL INTEGRATION TEST")
    print("=" * 80)
    print(f"Testing React Frontend + Flask Backend Integration")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tests = [
        ("Backend API", test_backend_api),
        ("Frontend Structure", test_frontend_structure), 
        ("API Client Config", test_api_client_config),
        ("Store Configuration", test_store_configuration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 80)
    print(f"🎯 INTEGRATION TEST RESULTS")
    print("=" * 80)
    print(f"   Tests Passed: {passed}/{total}")
    print(f"   Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("   🎉 ALL TESTS PASSED! Frontend and Backend are ready!")
        print("\n📋 NEXT STEPS:")
        print("   1. Start Flask backend: python app.py")
        print("   2. Start React frontend: cd frontend && npm run dev") 
        print("   3. Visit http://localhost:5173 to see your app!")
        print("   4. Select teams to see live predictions!")
    else:
        print(f"   ⚠️  {total-passed} test(s) failed - check configuration")
    
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = run_integration_test()
    sys.exit(0 if success else 1)