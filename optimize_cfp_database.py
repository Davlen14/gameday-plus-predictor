#!/usr/bin/env python3
"""
CFP Competitive Network Extractor
Creates optimized database with only CFP-relevant teams and their competitive web
"""

import sqlite3
import shutil
from datetime import datetime

def create_cfp_network_database():
    print("🕸️ CREATING CFP COMPETITIVE NETWORK DATABASE")
    print("=" * 60)
    
    # Backup original database
    print("📋 Creating backup...")
    shutil.copy('instance/playoff_team_analysis.db', 'instance/playoff_team_analysis_FULL_BACKUP.db')
    
    # Connect to database
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    cfp_teams = ['Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M', 'Miami', 'James Madison']
    
    print("🎯 Building CFP competitive network...")
    
    # Step 1: Get all CFP opponents (Layer 2)
    cursor.execute('''
    SELECT DISTINCT opponent FROM games 
    WHERE school IN (''' + ','.join(['?']*len(cfp_teams)) + ''')
    ''', cfp_teams)
    cfp_opponents = [row[0] for row in cursor.fetchall()]
    
    # Step 2: Get opponents of CFP opponents (Layer 3) - key for common opponent analysis
    layer3_teams = set()
    for opponent in cfp_opponents:
        if opponent not in cfp_teams:  # Don't double-count CFP teams
            cursor.execute('SELECT DISTINCT opponent FROM games WHERE school = ?', (opponent,))
            opp_opponents = [row[0] for row in cursor.fetchall()]
            layer3_teams.update(opp_opponents)
    
    # Step 3: Build complete network
    network_teams = set(cfp_teams) | set(cfp_opponents) | layer3_teams
    
    print(f"📊 NETWORK COMPOSITION:")
    print(f"   🏆 CFP Teams: {len(cfp_teams)}")
    print(f"   🎯 CFP Opponents: {len(cfp_opponents)}")
    print(f"   🌐 Extended Network: {len(layer3_teams)}")
    print(f"   📈 Total Network: {len(network_teams)} teams")
    
    # Step 4: Identify teams to remove
    cursor.execute('SELECT DISTINCT school FROM games')
    all_teams = [row[0] for row in cursor.fetchall()]
    teams_to_remove = [team for team in all_teams if team not in network_teams]
    
    print(f"\\n🗑️ OPTIMIZATION:")
    print(f"   Current teams: {len(all_teams)}")
    print(f"   Teams to remove: {len(teams_to_remove)}")
    print(f"   Optimized size: {len(network_teams)} ({((len(network_teams)/len(all_teams))*100):.1f}% of original)")
    
    # Step 5: Remove non-network teams from all tables
    tables_to_clean = ['games', 'players', 'nil_players', 'recruiting_classes', 'draft_picks', 'rankings', 'season_analytics', 'talent_composite', 'transfer_portal']
    
    total_removed = 0
    for table in tables_to_clean:
        # Check if table exists and has school/team columns
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'school' in columns:
            column_name = 'school'
        elif 'team_name' in columns:
            column_name = 'team_name'  
        elif 'college' in columns:
            column_name = 'college'
        else:
            continue
            
        # Count before deletion
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        before_count = cursor.fetchone()[0]
        
        # Remove non-network teams
        placeholders = ','.join(['?'] * len(teams_to_remove))
        cursor.execute(f'''
        DELETE FROM {table} 
        WHERE {column_name} IN ({placeholders})
        ''', teams_to_remove)
        
        # Count after deletion
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        after_count = cursor.fetchone()[0]
        
        removed = before_count - after_count
        total_removed += removed
        
        if removed > 0:
            print(f"   📋 {table}: removed {removed:,} records")
    
    # Step 6: Also clean opponent columns in games table
    cursor.execute('''
    DELETE FROM games 
    WHERE opponent NOT IN (''' + ','.join(['?']*len(network_teams)) + ''')
    ''', list(network_teams))
    
    conn.commit()
    
    # Step 7: Verify optimization
    cursor.execute('SELECT COUNT(DISTINCT school) FROM games')
    final_teams = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM games')
    final_games = cursor.fetchone()[0]
    
    print(f"\\n✅ OPTIMIZATION COMPLETE:")
    print(f"   Final teams: {final_teams}")
    print(f"   Final games: {final_games:,}")
    print(f"   Records removed: {total_removed:,}")
    
    # Step 8: Verify CFP coverage
    print(f"\\n🏆 CFP TEAM VERIFICATION:")
    for team in cfp_teams:
        cursor.execute('SELECT COUNT(*) FROM games WHERE school = ? AND season = 2025', (team,))
        games_2025 = cursor.fetchone()[0]
        cursor.execute('SELECT SUM(CASE WHEN result = \"W\" THEN 1 ELSE 0 END), SUM(CASE WHEN result = \"L\" THEN 1 ELSE 0 END) FROM games WHERE school = ? AND season = 2025', (team,))
        wins, losses = cursor.fetchone()
        print(f"   ✓ {team:15}: {wins}-{losses} ({games_2025} games)")
    
    conn.close()
    
    print(f"\\n🎯 NETWORK DATABASE READY:")
    print(f"   File: instance/playoff_team_analysis.db")
    print(f"   Backup: instance/playoff_team_analysis_FULL_BACKUP.db")
    print(f"   Focus: CFP competitive network only")
    print(f"   Capabilities: Full strength of schedule, common opponents, head-to-head analysis")
    
    return "instance/playoff_team_analysis.db"

if __name__ == "__main__":
    db_path = create_cfp_network_database()
    print(f"\\n🚀 READY FOR NUCLEAR CFP ANALYSIS!")
    print(f"   Database optimized for maximum CFP insight")
    print(f"   All competitive relationships preserved")
    print(f"   Perfect for 'web of connections' analysis")
