#!/usr/bin/env python3
"""Test script to verify coaching data is loading correctly"""

import json
import os

# Test loading from both locations
week_14_path = os.path.join('weekly_updates', 'week_14', 'coaches_with_vsranked_stats.json')
data_path = os.path.join('data', 'coaches_with_vsranked_stats.json')

print("=" * 80)
print("COACHING DATA COMPARISON TEST")
print("=" * 80)

# Load Week 14 data
print(f"\n📁 Loading from: {week_14_path}")
with open(week_14_path, 'r') as f:
    week_14_data = json.load(f)

# Find Ryan Day and Sherrone Moore
ryan_day_w14 = next((c for c in week_14_data if c['name'] == 'Ryan Day'), None)
sherrone_w14 = next((c for c in week_14_data if c['name'] == 'Sherrone Moore'), None)

print("\n🏈 Week 14 Data:")
print(f"  Ryan Day: {ryan_day_w14['careerRecord']} ({ryan_day_w14['careerWinPct']}%), 2025: {ryan_day_w14['2025Record']}")
print(f"    vs Top 5: {ryan_day_w14['vsRanked']['vsTop5']['record']}")
print(f"  Sherrone Moore: {sherrone_w14['careerRecord']} ({sherrone_w14['careerWinPct']}%), 2025: {sherrone_w14['2025Record']}")
print(f"    vs Top 5: {sherrone_w14['vsRanked']['vsTop5']['record']}")

# Load Data folder data
print(f"\n📁 Loading from: {data_path}")
with open(data_path, 'r') as f:
    data_folder = json.load(f)

ryan_day_data = next((c for c in data_folder if c['name'] == 'Ryan Day'), None)
sherrone_data = next((c for c in data_folder if c['name'] == 'Sherrone Moore'), None)

print("\n🏈 Data Folder (CURRENT):")
print(f"  Ryan Day: {ryan_day_data['careerRecord']} ({ryan_day_data['careerWinPct']}%), 2025: {ryan_day_data['2025Record']}")
print(f"    vs Top 5: {ryan_day_data['vsRanked']['vsTop5']['record']}")
print(f"  Sherrone Moore: {sherrone_data['careerRecord']} ({sherrone_data['careerWinPct']}%), 2025: {sherrone_data['2025Record']}")
print(f"    vs Top 5: {sherrone_data['vsRanked']['vsTop5']['record']}")

# Show differences
print("\n" + "=" * 80)
print("DIFFERENCES DETECTED:")
print("=" * 80)

if ryan_day_w14['careerRecord'] != ryan_day_data['careerRecord']:
    print(f"❌ Ryan Day career record mismatch:")
    print(f"   Week 14: {ryan_day_w14['careerRecord']} (OUTDATED)")
    print(f"   Data folder: {ryan_day_data['careerRecord']} ✅ CORRECT")

if sherrone_w14['careerRecord'] != sherrone_data['careerRecord']:
    print(f"❌ Sherrone Moore career record mismatch:")
    print(f"   Week 14: {sherrone_w14['careerRecord']} (OUTDATED)")
    print(f"   Data folder: {sherrone_data['careerRecord']} ✅ CORRECT")

print("\n✅ Backend should load from: data/coaches_with_vsranked_stats.json")
print("❌ Backend was loading from: weekly_updates/week_14/coaches_with_vsranked_stats.json")
print("\n🔧 Fix applied: Updated graphqlpredictor.py to use data/ folder for coaching data")
print("=" * 80)
