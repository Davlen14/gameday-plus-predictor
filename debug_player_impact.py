#!/usr/bin/env python3
"""
Analyze the player impact component to understand the enhanced system behavior
"""

import asyncio
import json
from graphqlpredictor import LightningPredictor

async def analyze_player_impact():
    """Debug the player impact component specifically"""
    
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("🔍 PLAYER IMPACT COMPONENT ANALYSIS")
    print("=" * 55)
    
    # Test USC vs Michigan (USC won 31-13, so this should favor USC)
    home_team_id = 30   # USC  
    away_team_id = 130  # Michigan
    
    print(f"🏈 Analyzing USC vs Michigan player impacts")
    print(f"   Actual Result: USC 31-13 Michigan (USC won by 18)")
    
    try:
        # Load comprehensive player data directly to check what we're getting
        data_files = {
            'qb': 'backtesting/comprehensive_qb_analysis_2025_20251015_034259.json',
            'rb': 'backtesting/comprehensive_rb_analysis_2025_20251015_043434.json', 
            'wr': 'backtesting/comprehensive_wr_analysis_2025_20251015_045922.json',
            'te': 'backtesting/comprehensive_te_analysis_2025_20251015_050510.json',
            'db': 'backtesting/comprehensive_db_analysis_2025_20251015_051747.json',
            'lb': 'backtesting/comprehensive_lb_analysis_2025_20251015_053156.json',
            'dl': 'backtesting/comprehensive_dl_analysis_2025_20251015_051056.json'
        }
        
        comprehensive_data = {}
        for pos, filename in data_files.items():
            try:
                with open(filename, 'r') as f:
                    raw_data = json.load(f)
                    # Extract the correct nested data structure
                    if pos == 'qb':
                        comprehensive_data[pos] = raw_data.get('quarterbacks', [])
                    elif pos == 'rb':
                        comprehensive_data[pos] = raw_data.get('running_backs', [])
                    elif pos == 'wr':
                        comprehensive_data[pos] = raw_data.get('all_wrs', [])
                    elif pos == 'te':
                        comprehensive_data[pos] = raw_data.get('tight_ends', [])
                    elif pos == 'db':
                        comprehensive_data[pos] = raw_data.get('dbs', [])
                    elif pos == 'lb':
                        comprehensive_data[pos] = raw_data.get('linebackers', [])
                    elif pos == 'dl':
                        comprehensive_data[pos] = raw_data.get('defensive_linemen', [])
                print(f"   ✅ Loaded {pos.upper()}: {len(comprehensive_data[pos])} players")
            except FileNotFoundError:
                print(f"   ❌ Missing {pos.upper()} data file: {filename}")
                comprehensive_data[pos] = []
        
        # Check for USC and Michigan players specifically
        print(f"\n🔍 USC Players Found:")
        for pos, data in comprehensive_data.items():
            usc_players = [p for p in data if p.get('team') == 'USC']
            print(f"   {pos.upper()}: {len(usc_players)} players")
            if usc_players and pos in ['qb', 'wr']:
                for player in usc_players[:2]:  # Show top 2
                    eff = player.get('efficiency_score', 0)
                    print(f"      - {player.get('player', 'Unknown')}: {eff}")
        
        print(f"\n🔍 Michigan Players Found:")
        for pos, data in comprehensive_data.items():
            mich_players = [p for p in data if p.get('team') == 'Michigan']
            print(f"   {pos.upper()}: {len(mich_players)} players")
            if mich_players and pos in ['qb', 'wr']:
                for player in mich_players[:2]:  # Show top 2
                    eff = player.get('efficiency_score', 0)
                    print(f"      - {player.get('player', 'Unknown')}: {eff}")
                    
        # Now run the actual prediction to see component weights
        print(f"\n🎯 Running full prediction to see component breakdown...")
        
        prediction = await predictor.predict_game(
            home_team_id=home_team_id,
            away_team_id=away_team_id
        )
        
        if prediction:
            print(f"\n📊 PREDICTION ANALYSIS:")
            print(f"   Winner: {'USC' if prediction.home_win_prob > 50 else 'Michigan'}")
            print(f"   Actual Winner: USC")
            print(f"   Match: {'✅' if (prediction.home_win_prob > 50) else '❌'}")
            print(f"   Confidence: {prediction.confidence:.1f}%")
            print(f"   Spread: {prediction.predicted_spread:+.1f} (USC)")
            print(f"   Actual Spread: +18.0 (USC)")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze_player_impact())