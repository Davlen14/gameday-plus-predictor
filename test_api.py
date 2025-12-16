#!/usr/bin/env python3
"""
Test script to verify the API endpoint returns correct data
"""
import requests
import json

def test_api():
    try:
        response = requests.get('http://localhost:5555/api/game-preview/401778309', timeout=10)
        print(f'Status Code: {response.status_code}\n')
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                game_data = data['data']
                sa = game_data.get('season_analytics', {})
                
                print('=' * 80)
                print('SEASON ANALYTICS - API RESPONSE')
                print('=' * 80)
                
                for key in ['primary', 'opponent']:
                    if key in sa and sa[key]:
                        analytics = sa[key]
                        print(f'\n{key.upper()} ({analytics.get("school", "Unknown")}):')
                        print(f'  points_per_game: {analytics.get("points_per_game")}')
                        print(f'  yards_per_game: {analytics.get("yards_per_game")}')
                        print(f'  third_down_pct: {analytics.get("third_down_pct")}')
                        print(f'  red_zone_pct: {analytics.get("red_zone_pct")}')
                        print(f'  points_allowed_pg: {analytics.get("points_allowed_pg")}')
                        print(f'  sacks_per_game: {analytics.get("sacks_per_game")}')
                        print(f'  turnovers_gained_pg: {analytics.get("turnovers_gained_pg")}')
                        print(f'  sp_overall: {analytics.get("sp_overall")}')
                        print(f'  sp_offense: {analytics.get("sp_offense")}')
                        print(f'  sp_defense: {analytics.get("sp_defense")}')
                        print(f'  fpi: {analytics.get("fpi")}')
                    else:
                        print(f'\n❌ {key.upper()}: No data')
                
                print('\n' + '=' * 80)
                print('✅ API IS WORKING CORRECTLY')
                print('=' * 80)
                
            else:
                print(f'❌ API Error: {data.get("error")}')
        else:
            print(f'❌ HTTP Error: {response.status_code}')
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to server. Is it running on port 5555?')
    except Exception as e:
        print(f'❌ Exception: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_api()
