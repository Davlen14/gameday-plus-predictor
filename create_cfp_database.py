#!/usr/bin/env python3
"""
CFP Team Analysis Database Creator
Creates a focused database with only the 12 CFP teams and their relevant data
"""

import sqlite3
import shutil
from pathlib import Path

# 12 CFP Teams
CFP_TEAMS = [
    'Indiana', 'Ohio State', 'Georgia', 'Texas Tech',  # Top 4 seeds
    'Oregon', 'Ole Miss', 'Texas A&M', 'Oklahoma',    # Seeds 5-8
    'Alabama', 'Miami', 'Tulane', 'James Madison'     # Seeds 9-12
]

def create_cfp_database():
    """Create playoff_team_analysis.db with CFP teams data"""
    
    # Source and target database paths
    source_db = Path('instance/coaches_master.db')
    target_db = Path('instance/playoff_team_analysis.db')
    
    if not source_db.exists():
        print(f"❌ Source database not found: {source_db}")
        return False
    
    # Copy the entire database first
    print(f"📋 Copying database from {source_db} to {target_db}...")
    shutil.copy2(source_db, target_db)
    
    # Connect to the new database
    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"📊 Found {len(tables)} tables in database")
    
    print("🔍 Analyzing table structures and filtering CFP data...")
    
    # Custom filters for each table based on actual column names
    cfp_team_list = ','.join([f'"{team}"' for team in CFP_TEAMS])
    
    table_filters = {
        'teams': f"school IN ({cfp_team_list})",
        'games': f"school IN ({cfp_team_list}) OR opponent IN ({cfp_team_list})",
        'coaches': f"school IN ({cfp_team_list})",
        'stints': f"school IN ({cfp_team_list})",
        'team_rankings': f"school IN ({cfp_team_list})",
        'recruiting_classes': f"team IN ({cfp_team_list})",
        'talent_composite': f"team IN ({cfp_team_list})",
        'transfer_portal': f"team IN ({cfp_team_list})"
    }
    
    for table in tables:
        try:
            if table in table_filters:
                print(f"🔍 Processing table: {table}")
                
                # Count original rows
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                original_count = cursor.fetchone()[0]
                
                # Create a backup of the table
                cursor.execute(f"ALTER TABLE {table} RENAME TO {table}_full;")
                
                # Create new table with CFP data only
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}_full';")
                create_sql = cursor.fetchone()[0].replace(f'{table}_full', table)
                cursor.execute(create_sql)
                
                # Insert CFP-related data
                cursor.execute(f"INSERT INTO {table} SELECT * FROM {table}_full WHERE {table_filters[table]};")
                
                # Count filtered rows
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                filtered_count = cursor.fetchone()[0]
                
                # Drop the backup if filtering worked
                if filtered_count > 0:
                    cursor.execute(f"DROP TABLE {table}_full;")
                    print(f"   ✅ {table}: {original_count} → {filtered_count} rows")
                else:
                    # Restore original if no matches
                    cursor.execute(f"DROP TABLE {table};")
                    cursor.execute(f"ALTER TABLE {table}_full RENAME TO {table};")
                    print(f"   ⚠️  {table}: No CFP matches found, kept all {original_count} rows")
            
        except Exception as e:
            print(f"   ⚠️  Error processing {table}: {e}")
            try:
                # Try to restore if backup exists
                cursor.execute(f"DROP TABLE IF EXISTS {table};")
                cursor.execute(f"ALTER TABLE {table}_full RENAME TO {table};")
            except:
                pass
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ CFP database created: {target_db}")
    return True

def analyze_cfp_database():
    """Quick analysis of the CFP database"""
    
    db_path = Path('instance/playoff_team_analysis.db')
    if not db_path.exists():
        print("❌ CFP database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n📊 CFP DATABASE ANALYSIS")
    print("=" * 50)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in sorted(tables):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"{table:30} {count:>8} rows")
        except:
            pass
    
    # Look for CFP teams specifically
    print(f"\n🏈 CFP TEAMS IN DATABASE:")
    print("-" * 30)
    
    try:
        cursor.execute("SELECT DISTINCT school FROM teams ORDER BY school;")
        teams = [row[0] for row in cursor.fetchall()]
        
        cfp_found = []
        for cfp_team in CFP_TEAMS:
            matching_teams = [team for team in teams if cfp_team.lower() in team.lower()]
            if matching_teams:
                cfp_found.extend(matching_teams)
                print(f"✅ {cfp_team:15} → {matching_teams}")
            else:
                print(f"❌ {cfp_team:15} → NOT FOUND")
        
        print(f"\n📈 Found {len(cfp_found)} CFP teams in database")
        
        # Also check coaches for these teams
        print(f"\n👨‍💼 CFP COACHES:")
        cursor.execute("SELECT DISTINCT school, name FROM coaches WHERE school IN (SELECT school FROM teams) ORDER BY school;")
        for school, coach in cursor.fetchall():
            print(f"   {school:20} → {coach}")
        
    except Exception as e:
        print(f"Error querying teams: {e}")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 CREATING CFP ANALYSIS DATABASE")
    print("=" * 50)
    
    success = create_cfp_database()
    if success:
        analyze_cfp_database()
    
    print("\n✅ CFP Database setup complete!")