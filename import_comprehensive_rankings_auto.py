#!/usr/bin/env python3
"""
Auto-Import Comprehensive Power Rankings
Automatically maps JSON fields to database columns
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = 'instance/predictions.db'
JSON_PATH = 'weekly_updates/week_15/comprehensive_power_rankings_20251203_053934.json'

def create_table_from_json(conn, sample_team):
    """Create table dynamically based on JSON structure"""
    cursor = conn.cursor()
    
    # Get all metric keys
    off_norm_keys = list(sample_team['detailed_metrics']['offensive_normalized'].keys())
    def_norm_keys = list(sample_team['detailed_metrics']['defensive_normalized'].keys())
    off_raw_keys = list(sample_team['detailed_metrics']['offensive_raw'].keys())
    def_raw_keys = list(sample_team['detailed_metrics']['defensive_raw'].keys())
    
    # Build column definitions
    columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "team_name TEXT NOT NULL",
        "conference TEXT",
        "season INTEGER NOT NULL",
        "week INTEGER NOT NULL",
        "rank INTEGER",
        "overall_score REAL",
        "offensive_score REAL",
        "defensive_score REAL",
        "total_metrics_analyzed INTEGER",
    ]
    
    # Add offensive normalized columns
    for key in off_norm_keys:
        col_name = f"off_norm_{key}"
        columns.append(f"{col_name} REAL")
    
    # Add defensive normalized columns (strip def_ prefix if present)
    for key in def_norm_keys:
        clean_key = key.replace('def_', '', 1) if key.startswith('def_') else key
        col_name = f"def_norm_{clean_key}"
        columns.append(f"{col_name} REAL")
    
    # Add offensive raw columns
    for key in off_raw_keys:
        col_name = f"off_raw_{key}"
        columns.append(f"{col_name} REAL")
    
    # Add defensive raw columns (strip def_ prefix if present)
    for key in def_raw_keys:
        clean_key = key.replace('def_', '', 1) if key.startswith('def_') else key
        col_name = f"def_raw_{clean_key}"
        columns.append(f"{col_name} REAL")
    
    columns.extend([
        "generated_at TEXT",
        "imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "UNIQUE(team_name, season, week)"
    ])
    
    columns_str = ',\n    '.join(columns)
    create_sql = f"CREATE TABLE IF NOT EXISTS comprehensive_power_rankings (\n    {columns_str}\n)"
    
    cursor.execute(create_sql)
    conn.commit()
    
    total_cols = len(columns) - 2  # Subtract UNIQUE and id (autoincrement)
    print(f"✅ Created table with {total_cols} columns (160 metrics + 9 basic fields)")
    
    return off_norm_keys, def_norm_keys, off_raw_keys, def_raw_keys

def import_data(conn, json_path, keys):
    """Import data using dynamic key mapping"""
    off_norm_keys, def_norm_keys, off_raw_keys, def_raw_keys = keys
    
    cursor = conn.cursor()
    
    with open(json_path) as f:
        data = json.load(f)
    
    metadata = data['metadata']
    rankings = data['rankings']
    
    week = 15
    season = 2025
    
    print(f"Importing {len(rankings)} teams...")
    
    imported = 0
    for team_data in rankings:
        try:
            # Build column names
            col_names = [
                "team_name", "conference", "season", "week",
                "rank", "overall_score", "offensive_score", "defensive_score", "total_metrics_analyzed"
            ]
            
            # Add all metric column names (strip def_ prefix for defensive metrics)
            col_names.extend([f"off_norm_{k}" for k in off_norm_keys])
            col_names.extend([f"def_norm_{k.replace('def_', '', 1) if k.startswith('def_') else k}" for k in def_norm_keys])
            col_names.extend([f"off_raw_{k}" for k in off_raw_keys])
            col_names.extend([f"def_raw_{k.replace('def_', '', 1) if k.startswith('def_') else k}" for k in def_raw_keys])
            col_names.append("generated_at")
            
            # Build values
            off_norm = team_data['detailed_metrics']['offensive_normalized']
            def_norm = team_data['detailed_metrics']['defensive_normalized']
            off_raw = team_data['detailed_metrics']['offensive_raw']
            def_raw = team_data['detailed_metrics']['defensive_raw']
            
            values = [
                team_data['team'], team_data['conference'], season, week,
                team_data['rank'], team_data['overall_score'],
                team_data['offensive_score'], team_data['defensive_score'],
                team_data['total_metrics_analyzed']
            ]
            
            # Add all metric values
            values.extend([off_norm.get(k) for k in off_norm_keys])
            values.extend([def_norm.get(k) for k in def_norm_keys])
            values.extend([off_raw.get(k) for k in off_raw_keys])
            values.extend([def_raw.get(k) for k in def_raw_keys])
            values.append(metadata['generated_at'])
            
            # Build INSERT query
            placeholders = ','.join(['?' for _ in values])
            insert_sql = f"INSERT OR REPLACE INTO comprehensive_power_rankings ({','.join(col_names)}) VALUES ({placeholders})"
            
            cursor.execute(insert_sql, values)
            imported += 1
            
        except Exception as e:
            print(f"❌ Error importing {team_data['team']}: {e}")
            continue
    
    conn.commit()
    print(f"✅ Successfully imported {imported} teams")

def verify(conn):
    """Verify the import"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM comprehensive_power_rankings WHERE season = 2025 AND week = 15")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total teams in database: {count}")
    
    cursor.execute("""
        SELECT team_name, rank, overall_score, offensive_score, defensive_score 
        FROM comprehensive_power_rankings 
        WHERE season = 2025 AND week = 15 
        ORDER BY rank 
        LIMIT 5
    """)
    
    print("\n🏆 Top 5 Teams:")
    for row in cursor.fetchall():
        print(f"  #{row[1]} {row[0]}: Overall={row[2]:.2f}, Off={row[3]:.2f}, Def={row[4]:.2f}")

def main():
    print("=" * 60)
    print("Auto-Import Comprehensive Power Rankings")
    print("=" * 60)
    
    # Load sample to determine structure
    with open(JSON_PATH) as f:
        data = json.load(f)
    sample_team = data['rankings'][0]
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create table
        keys = create_table_from_json(conn, sample_team)
        
        # Import data
        import_data(conn, JSON_PATH, keys)
        
        # Verify
        verify(conn)
        
        print("\n✅ Import completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
