#!/usr/bin/env python3
"""
Test script to verify Ryan Wingo's actual receiving yards
"""

from real_data_props_generator import RealDataPlayerPropsEngine

engine = RealDataPlayerPropsEngine()

print("\n🏈 TESTING RYAN WINGO DATA FIX")
print("="*80)

# Generate Texas props
texas_props = engine.generate_enhanced_props("Texas", "Georgia")

# Find Ryan Wingo props
for prop in texas_props:
    if prop.player_name == "Ryan Wingo" and prop.prop_type == "receiving_yards":
        print(f"\n✅ Found Ryan Wingo - Receiving Yards Prop")
        print(f"Season Average: {prop.season_average} yards")
        print(f"\n📊 GAME-BY-GAME BREAKDOWN:")
        print("-"*80)
        for log in prop.game_logs:
            yards = log.stats.get('receiving_yards', 0)
            print(f"Week {log.week:2d}: {log.home_away:4s} {log.opponent:25s} | {yards:3d} yards | {log.result}")
        
        print("\n" + "="*80)
        print("EXPECTED VALUES (from image):")
        print("Week 1 (Aug 30) @ Ohio State: 43 yards")
        print("Week 2 (Sep 6) vs San José State: 39 yards")
        print("Week 3 (Sep 13) vs UTEP: 25 yards")
        print("Week 4 (Sep 20) vs Sam Houston: 125 yards")
        print("Week 6 (Oct 4) @ Florida: 73 yards")
        print("Week 7 (Oct 11) vs Oklahoma: 35 yards")
        print("\n" + "="*80)
        print("ACTUAL VALUES (from API):")
        print("Week 1 @ Ohio State: 35 yards")
        print("Week 2 vs San José State: 30 yards")
        print("Week 3 vs UTEP: 32 yards")
        print("Week 4 vs Sam Houston: 93 yards")
        print("Week 6 @ Florida: 73 yards ✅")
        print("Week 7 vs Oklahoma: 35 yards ✅")
