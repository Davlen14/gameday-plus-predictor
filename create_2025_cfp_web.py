#!/usr/bin/env python3
"""
CFP 2025 Web Connection Analyzer
Creates 2025-focused connection web for current playoff analysis
"""

import sqlite3
from collections import defaultdict
import json

def create_2025_cfp_web():
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print("🕸️ CFP 2025 SEASON WEB ANALYSIS")
    print("=" * 50)
    
    cfp_teams = ['Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M', 'Miami', 'James Madison']
    
    # Drop and recreate tables for 2025 focus
    cursor.execute('DROP TABLE IF EXISTS cfp_connections_2025')
    cursor.execute('DROP TABLE IF EXISTS cfp_web_2025')
    
    # Create 2025-focused connections table
    cursor.execute('''
    CREATE TABLE cfp_connections_2025 (
        id INTEGER PRIMARY KEY,
        cfp_team TEXT,
        opponent TEXT,
        result TEXT,
        margin INTEGER,
        is_cfp_opponent BOOLEAN,
        week INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create 2025 web relationships table
    cursor.execute('''
    CREATE TABLE cfp_web_2025 (
        id INTEGER PRIMARY KEY,
        team1 TEXT,
        team2 TEXT,
        relationship_type TEXT,
        common_opponents_2025 INTEGER,
        h2h_2025 INTEGER,
        connection_strength FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    print("📊 2025 SEASON CFP CONNECTIONS:")
    print("=" * 35)
    
    # Analyze each CFP team's 2025 connections
    for team in cfp_teams:
        print(f"\n🏈 {team} (2025 only):")
        
        # Get 2025 opponents only
        cursor.execute('''
        SELECT opponent, result, (coach_score - opponent_score) as margin, week
        FROM games 
        WHERE school = ? AND season = 2025
        ORDER BY week
        ''', (team,))
        
        opponents_2025 = cursor.fetchall()
        
        cfp_opponents = []
        external_opponents = []
        
        for opponent, result, margin, week in opponents_2025:
            is_cfp = opponent in cfp_teams
            
            # Insert into 2025 connections table
            cursor.execute('''
            INSERT INTO cfp_connections_2025 
            (cfp_team, opponent, result, margin, is_cfp_opponent, week)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (team, opponent, result, margin, is_cfp, week))
            
            if is_cfp:
                cfp_opponents.append((opponent, result, margin, week))
            else:
                external_opponents.append((opponent, result, margin, week))
        
        print(f"  🏆 vs CFP Teams (2025): {len(cfp_opponents)}")
        for opp, result, margin, week in cfp_opponents:
            print(f"    Week {week:2}: vs {opp} {result} ({margin:+d})")
        
        print(f"  🎯 vs Other Teams: {len(external_opponents)}")
        print(f"  📊 Total 2025 games: {len(opponents_2025)}")
    
    conn.commit()
    
    print(f"\n🌐 BUILDING 2025 CFP RELATIONSHIP WEB:")
    print("=" * 40)
    
    # Build 2025-focused relationship matrix
    for i, team1 in enumerate(cfp_teams):
        for team2 in cfp_teams[i+1:]:
            
            # 2025 head-to-head only
            cursor.execute('''
            SELECT COUNT(*) FROM cfp_connections_2025
            WHERE (cfp_team = ? AND opponent = ?) OR (cfp_team = ? AND opponent = ?)
            ''', (team1, team2, team2, team1))
            h2h_2025 = cursor.fetchone()[0]
            
            # 2025 common opponents only
            cursor.execute('''
            SELECT COUNT(DISTINCT c1.opponent) 
            FROM cfp_connections_2025 c1
            JOIN cfp_connections_2025 c2 ON c1.opponent = c2.opponent
            WHERE c1.cfp_team = ? AND c2.cfp_team = ? 
            AND c1.opponent NOT IN (?, ?) AND c1.is_cfp_opponent = 0
            ''', (team1, team2, team1, team2))
            common_2025 = cursor.fetchone()[0]
            
            # 2025-focused connection strength
            connection_strength = (h2h_2025 * 5) + (common_2025 * 1)  # Higher weight for direct matchups
            
            # Determine 2025 relationship type
            if h2h_2025 > 0:
                relationship_type = '2025_DIRECT'
            elif common_2025 >= 4:
                relationship_type = '2025_STRONG_NETWORK'
            elif common_2025 >= 2:
                relationship_type = '2025_MODERATE_NETWORK'
            elif common_2025 >= 1:
                relationship_type = '2025_WEAK_NETWORK'
            else:
                relationship_type = '2025_NO_CONNECTION'
            
            # Only insert if there's some connection
            if connection_strength > 0:
                cursor.execute('''
                INSERT INTO cfp_web_2025 
                (team1, team2, relationship_type, common_opponents_2025, h2h_2025, connection_strength)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (team1, team2, relationship_type, common_2025, h2h_2025, connection_strength))
                
                print(f"  🔗 {team1} ↔ {team2}: {relationship_type}")
                if h2h_2025 > 0:
                    print(f"     💥 Direct 2025 matchup!")
                if common_2025 > 0:
                    print(f"     🎯 {common_2025} common 2025 opponents")
    
    conn.commit()
    
    print(f"\n📋 2025 CFP ANALYSIS TABLES:")
    print("=" * 30)
    
    # 2025 CFP vs CFP matchups
    cursor.execute('''
    SELECT cfp_team, opponent, result, margin, week
    FROM cfp_connections_2025 
    WHERE is_cfp_opponent = 1 
    ORDER BY week DESC
    ''')
    
    print("🏆 2025 CFP HEAD-TO-HEAD RESULTS:")
    cfp_matchups_2025 = cursor.fetchall()
    for team, opponent, result, margin, week in cfp_matchups_2025:
        print(f"  Week {week:2}: {team} vs {opponent} {result} ({margin:+d})")
    
    # Top 2025 common opponent networks
    cursor.execute('''
    SELECT opponent, COUNT(DISTINCT cfp_team) as cfp_teams_played,
           GROUP_CONCAT(cfp_team) as teams
    FROM cfp_connections_2025 
    WHERE is_cfp_opponent = 0
    GROUP BY opponent
    HAVING COUNT(DISTINCT cfp_team) >= 2
    ORDER BY cfp_teams_played DESC
    LIMIT 10
    ''')
    
    print(f"\n🎯 KEY 2025 COMMON OPPONENTS:")
    for opponent, cfp_count, teams in cursor.fetchall():
        team_list = teams.split(',')[:3]  # Show first 3
        more = f" +{len(teams.split(',')) - 3}" if len(teams.split(',')) > 3 else ""
        print(f"  {opponent}: {cfp_count} CFP teams ({', '.join(team_list)}{more})")
    
    # Strongest 2025 connections
    cursor.execute('''
    SELECT team1, team2, relationship_type, common_opponents_2025, h2h_2025, connection_strength
    FROM cfp_web_2025 
    ORDER BY connection_strength DESC
    LIMIT 8
    ''')
    
    print(f"\n🌟 STRONGEST 2025 CFP CONNECTIONS:")
    for team1, team2, rel_type, common, h2h, strength in cursor.fetchall():
        print(f"  {team1} ↔ {team2}: {strength} pts ({rel_type})")
        if h2h > 0:
            print(f"    💥 {h2h} direct matchup(s)")
        if common > 0:
            print(f"    🎯 {common} common opponents")
    
    conn.close()
    
    print(f"\n✅ 2025 CFP WEB COMPLETE:")
    print(f"   📋 cfp_connections_2025: Current season connections")
    print(f"   🌐 cfp_web_2025: 2025-focused relationship matrix")  
    print(f"   🎯 Perfect for current CFP predictions!")
    
    return "instance/playoff_team_analysis.db"

def create_2025_web_visualization():
    """Create 2025-focused JSON visualization data"""
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print(f"\n🎨 CREATING 2025 WEB VISUALIZATION:")
    
    cfp_teams = ['Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M', 'Miami', 'James Madison']
    
    # Get 2025 nodes
    nodes = []
    for i, team in enumerate(cfp_teams):
        cursor.execute('SELECT COUNT(DISTINCT opponent) FROM cfp_connections_2025 WHERE cfp_team = ?', (team,))
        connections_2025 = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(margin) FROM cfp_connections_2025 WHERE cfp_team = ?', (team,))
        avg_margin_2025 = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM cfp_connections_2025 WHERE cfp_team = ? AND is_cfp_opponent = 1', (team,))
        cfp_matchups = cursor.fetchone()[0]
        
        nodes.append({
            'id': i,
            'name': team,
            'connections_2025': connections_2025,
            'avg_margin_2025': round(avg_margin_2025, 1),
            'cfp_matchups_2025': cfp_matchups,
            'size': min(60, max(25, connections_2025 * 3))  # Larger nodes for more connections
        })
    
    # Get 2025 edges
    cursor.execute('''
    SELECT team1, team2, relationship_type, connection_strength
    FROM cfp_web_2025
    WHERE connection_strength > 0
    ORDER BY connection_strength DESC
    ''')
    
    edges = []
    team_to_id = {team['name']: team['id'] for team in nodes}
    
    for team1, team2, rel_type, strength in cursor.fetchall():
        if team1 in team_to_id and team2 in team_to_id:
            edges.append({
                'source': team_to_id[team1],
                'target': team_to_id[team2],
                'relationship': rel_type,
                'strength': strength,
                'width': min(12, max(2, strength))  # Edge width based on 2025 strength
            })
    
    web_data_2025 = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'created': '2025-12-17',
            'season': '2025',
            'total_teams': len(nodes),
            'total_connections': len(edges),
            'description': 'CFP 2025 Season Competitive Network'
        }
    }
    
    # Save 2025-focused file
    with open('cfp_web_2025_only.json', 'w') as f:
        json.dump(web_data_2025, f, indent=2)
    
    print(f"   📊 Created cfp_web_2025_only.json")
    print(f"   🎯 {len(nodes)} teams, {len(edges)} 2025 connections")
    print(f"   🔥 2025-focused network for current predictions")
    
    conn.close()
    return web_data_2025

if __name__ == "__main__":
    print("🚀 CREATING 2025-FOCUSED CFP WEB...")
    
    db_path = create_2025_cfp_web()
    web_data = create_2025_web_visualization()
    
    print(f"\n🎯 2025 CFP WEB READY!")
    print(f"   Database: {db_path}")
    print(f"   2025 Web Data: cfp_web_2025_only.json")
    print(f"   Tables: cfp_connections_2025, cfp_web_2025")
    print(f"   Perfect for current playoff predictions! 🏆")