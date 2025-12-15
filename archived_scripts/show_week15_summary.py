#!/usr/bin/env python3
"""Quick summary of Week 15 sharp plays"""

import json

with open('week15_sharp_analysis_results.json', 'r') as f:
    data = json.load(f)

print('╔' + '═'*92 + '╗')
print('║' + ' '*28 + '🏈 WEEK 15 SHARP MONEY GUIDE 🏈' + ' '*28 + '║')
print('╚' + '═'*92 + '╝')
print()
print('┌─────┬──────────────────────────────┬─────────────────────┬──────────┬─────────┬──────────────┐')
print('│ #   │ MATCHUP                      │ SHARP PLAY          │ SPREAD   │ CONF    │ BETS         │')
print('├─────┼──────────────────────────────┼─────────────────────┼──────────┼─────────┼──────────────┤')

sharp_plays = sorted(data['sharp_plays'], key=lambda x: x['sharp_indicators']['confidence'], reverse=True)

for i, game in enumerate(sharp_plays[:7], 1):
    sharp = game['sharp_indicators']
    matchup = f"{game['away_abbr']} @ {game['home_abbr']}"
    
    # Determine sharp side
    if sharp['sharp_on_away']:
        play = f"BET {game['away_abbr']}"
    else:
        play = f"BET {game['home_abbr']}"
    
    spread = game['spread_line']
    conf = f"{sharp['confidence']}%"
    bets = f"{game['num_bets']:,}"
    
    print(f'│ {i:<3} │ {matchup:<28} │ {play:<19} │ {spread:<8} │ {conf:<7} │ {bets:>12} │')

print('└─────┴──────────────────────────────┴─────────────────────┴──────────┴─────────┴──────────────┘')
print()
print('📌 KEY PATTERNS IDENTIFIED:')
print('   ✅ 5 games with 100% money on one side (EXTREMELY RARE)')
print('   ✅ 4 games with reverse line movement')
print('   ✅ Total bets tracked: 143,823')
print()
print('💰 TOP 3 MUST-PLAY GAMES:')
print('   1. INDIANA +10.5 @ Ohio State - 100% money, 50/50 public bets')
print('   2. GEORGIA -2.5 vs Alabama - 100% money, 60% public on Alabama')  
print('   3. NORTH TEXAS -2.5 @ Tulane - 100% money, nearly even public')
print()
print('📖 Full Report: WEEK15_SHARP_REPORT.md')
print('💾 Raw Data: week15_sharp_analysis_results.json')
print('🔧 Analysis Script: week15_sharp_analysis.py')
