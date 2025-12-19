#!/usr/bin/env python3
"""
CFP Web Connection Analyzer
Creates detailed connection tables and web data for all CFP teams
"""

import sqlite3
from collections import defaultdict
import json

def analyze_cfp_connections():
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print("🕸️ CFP TEAM CONNECTION WEB ANALYSIS")
    print("=" * 60)
    
    cfp_teams = ['Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M', 'Miami', 'James Madison']
    
    # Create connections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cfp_connections (
        id INTEGER PRIMARY KEY,
        cfp_team TEXT,
        opponent TEXT,
        season INTEGER,
        result TEXT,
        margin INTEGER,
        is_cfp_opponent BOOLEAN,
        connection_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create web relationships table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cfp_web_relationships (
        id INTEGER PRIMARY KEY,
        team1 TEXT,
        team2 TEXT,
        relationship_type TEXT,
        common_opponents INTEGER,
        head_to_head_games INTEGER,
        connection_strength FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM cfp_connections')
    cursor.execute('DELETE FROM cfp_web_relationships')
    
    print("📊 ANALYZING EACH CFP TEAM'S CONNECTIONS:")
    print("=" * 50)
    
    team_connections = {}
    
    for team in cfp_teams:
        print(f"\n🏈 {team.upper()} CONNECTIONS:")
        
        # Get all opponents for this team
        cursor.execute('''
        SELECT opponent, season, result, (coach_score - opponent_score) as margin
        FROM games 
        WHERE school = ? 
        ORDER BY season DESC, week
        ''', (team,))
        
        opponents = cursor.fetchall()
        team_connections[team] = opponents
        
        # Separate by categories
        cfp_opponents = []
        recent_opponents = []
        historical_opponents = []
        
        for opponent, season, result, margin in opponents:
            is_cfp = opponent in cfp_teams
            
            # Insert into connections table
            cursor.execute('''
            INSERT INTO cfp_connections 
            (cfp_team, opponent, season, result, margin, is_cfp_opponent, connection_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (team, opponent, season, result, margin, is_cfp, 
                  'CFP_MATCHUP' if is_cfp else 'EXTERNAL_OPPONENT'))
            
            if is_cfp:
                cfp_opponents.append((opponent, season, result, margin))
            elif season >= 2024:
                recent_opponents.append((opponent, season, result, margin))
            else:
                historical_opponents.append((opponent, season, result, margin))
        
        print(f"  🏆 vs CFP Teams: {len(cfp_opponents)}")
        for opp, season, result, margin in cfp_opponents:
            print(f"    • {season} vs {opp}: {result} ({margin:+d})")
        
        print(f"  🎯 Recent Opponents (2024+): {len(recent_opponents)}")
        for opp, season, result, margin in recent_opponents[:5]:  # Show top 5
            print(f"    • {season} vs {opp}: {result} ({margin:+d})")
        
        if len(recent_opponents) > 5:
            print(f"    • ... and {len(recent_opponents) - 5} more")
        
        print(f"  📚 Total Network: {len(opponents)} connections")
    
    conn.commit()
    
    print(f"\n🌐 BUILDING CFP RELATIONSHIP WEB:")
    print("=" * 40)
    
    # Build relationship matrix
    for i, team1 in enumerate(cfp_teams):
        for team2 in cfp_teams[i+1:]:  # Avoid duplicates
            
            # Head-to-head games
            cursor.execute('''
            SELECT COUNT(*) FROM games 
            WHERE (school = ? AND opponent = ?) OR (school = ? AND opponent = ?)
            ''', (team1, team2, team2, team1))
            h2h_count = cursor.fetchone()[0]
            
            # Common opponents
            cursor.execute('''
            SELECT COUNT(DISTINCT g1.opponent) 
            FROM games g1
            JOIN games g2 ON g1.opponent = g2.opponent AND g1.season = g2.season
            WHERE g1.school = ? AND g2.school = ? AND g1.opponent NOT IN (?, ?)
            ''', (team1, team2, team1, team2))
            common_opps = cursor.fetchone()[0]
            
            # Connection strength (weighted score)
            connection_strength = (h2h_count * 3) + (common_opps * 1)
            
            # Determine relationship type
            if h2h_count > 0:
                relationship_type = 'DIRECT_RIVALS'
            elif common_opps >= 5:
                relationship_type = 'STRONG_NETWORK'
            elif common_opps >= 2:
                relationship_type = 'MODERATE_NETWORK'
            else:
                relationship_type = 'WEAK_CONNECTION'
            
            # Insert relationship
            cursor.execute('''
            INSERT INTO cfp_web_relationships 
            (team1, team2, relationship_type, common_opponents, head_to_head_games, connection_strength)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (team1, team2, relationship_type, common_opps, h2h_count, connection_strength))
            
            if connection_strength > 0:
                print(f"  🔗 {team1} ↔ {team2}: {relationship_type}")
                print(f"     H2H: {h2h_count}, Common: {common_opps}, Strength: {connection_strength}")
    
    conn.commit()
    
    print(f"\n📋 CONNECTION SUMMARY TABLES:")
    print("=" * 35)
    
    # CFP vs CFP matchups
    cursor.execute('''
    SELECT cfp_team, opponent, COUNT(*) as games, 
           SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) as wins
    FROM cfp_connections 
    WHERE is_cfp_opponent = 1 
    GROUP BY cfp_team, opponent
    ORDER BY cfp_team, games DESC
    ''')
    
    print("🏆 CFP HEAD-TO-HEAD RECORDS:")
    cfp_matchups = cursor.fetchall()
    for team, opponent, games, wins in cfp_matchups:
        losses = games - wins
        print(f"  {team} vs {opponent}: {wins}-{losses} ({games} games)")
    
    # Top connected teams
    cursor.execute('''
    SELECT team1, team2, common_opponents, head_to_head_games, connection_strength
    FROM cfp_web_relationships 
    ORDER BY connection_strength DESC
    LIMIT 10
    ''')
    
    print(f"\n🌟 STRONGEST CFP CONNECTIONS:")
    for team1, team2, common, h2h, strength in cursor.fetchall():
        print(f"  {team1} ↔ {team2}: Strength {strength} (H2H: {h2h}, Common: {common})")
    
    # Most connected individual teams
    cursor.execute('''
    SELECT cfp_team, COUNT(DISTINCT opponent) as total_opponents,
           SUM(CASE WHEN is_cfp_opponent = 1 THEN 1 ELSE 0 END) as cfp_opponents
    FROM cfp_connections 
    GROUP BY cfp_team
    ORDER BY total_opponents DESC
    ''')
    
    print(f"\n📊 MOST CONNECTED CFP TEAMS:")
    for team, total_opps, cfp_opps in cursor.fetchall():
        print(f"  {team}: {total_opps} total opponents ({cfp_opps} CFP teams)")
    
    # Common opponent networks
    print(f"\n🎯 COMMON OPPONENT NETWORKS:")
    cursor.execute('''
    SELECT opponent, COUNT(DISTINCT cfp_team) as cfp_teams_played
    FROM cfp_connections 
    WHERE season >= 2020
    GROUP BY opponent
    HAVING COUNT(DISTINCT cfp_team) >= 3
    ORDER BY cfp_teams_played DESC
    LIMIT 10
    ''')
    
    for opponent, cfp_count in cursor.fetchall():
        print(f"  {opponent}: played by {cfp_count} CFP teams")
    
    conn.close()
    
    print(f"\n✅ CFP WEB DATA ADDED TO DATABASE:")
    print(f"   📋 cfp_connections table: Team opponent relationships")
    print(f"   🌐 cfp_web_relationships table: CFP-to-CFP connection matrix")
    print(f"   🎯 Ready for advanced network analysis")
    
    return "instance/playoff_team_analysis.db"

def create_web_visualization_data():
    """Create JSON data for web visualization"""
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print(f"\n🎨 CREATING WEB VISUALIZATION DATA:")
    
    # Get nodes (CFP teams)
    cfp_teams = ['Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M', 'Miami', 'James Madison']
    
    nodes = []
    for i, team in enumerate(cfp_teams):
        cursor.execute('SELECT COUNT(DISTINCT opponent) FROM cfp_connections WHERE cfp_team = ?', (team,))
        connection_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(margin) FROM cfp_connections WHERE cfp_team = ? AND season = 2025', (team,))
        avg_margin = cursor.fetchone()[0] or 0
        
        nodes.append({
            'id': i,
            'name': team,
            'connections': connection_count,
            'avg_margin': round(avg_margin, 1),
            'size': min(50, max(20, connection_count))  # Node size based on connections
        })
    
    # Get edges (relationships)
    cursor.execute('''
    SELECT team1, team2, relationship_type, connection_strength
    FROM cfp_web_relationships
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
                'width': min(10, max(1, strength / 2))  # Edge width based on strength
            })
    
    web_data = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'created': '2025-12-17',
            'total_teams': len(nodes),
            'total_connections': len(edges),
            'description': 'CFP Competitive Network Web'
        }
    }
    
    # Save to file
    with open('cfp_web_data.json', 'w') as f:
        json.dump(web_data, f, indent=2)
    
    print(f"   📊 Created cfp_web_data.json")
    print(f"   🎯 {len(nodes)} nodes, {len(edges)} connections")
    print(f"   🔥 Ready for D3.js or other web visualization")
    
    conn.close()
    return web_data

if __name__ == "__main__":
    print("🚀 CFP WEB CONNECTION ANALYSIS STARTING...")
    
    db_path = analyze_cfp_connections()
    web_data = create_web_visualization_data()
    
    print(f"\n🎯 COMPLETE CFP WEB ANALYSIS READY!")
    print(f"   Database: {db_path}")
    print(f"   Web Data: cfp_web_data.json")
    print(f"   Tables: cfp_connections, cfp_web_relationships")
    print(f"   Ready for nuclear-level network analysis! 🔬")