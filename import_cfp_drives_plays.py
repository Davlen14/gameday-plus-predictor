#!/usr/bin/env python3
"""
Import drives and plays data for all 12 CFP teams from CSV files.
This will give us complete drives/plays coverage for nuclear CFP prediction.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path
import json

def import_cfp_drives_and_plays():
    """Import drives and plays data for all CFP teams from CSV files"""
    
    # CFP teams as they appear in filenames
    cfp_teams = [
        'Indiana', 'Ohio_State', 'Georgia', 'Texas_Tech', 'Oregon', 
        'Oklahoma', 'Alabama', 'Ole_Miss', 'Tulane', 'Texas_AandM', 
        'Miami', 'James_Madison'
    ]
    
    # Connect to database
    conn = sqlite3.connect('instance/playoff_team_analysis.db')
    cursor = conn.cursor()
    
    print("🏈 IMPORTING CFP DRIVES & PLAYS DATA")
    print("=" * 40)
    
    # Create drives table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cfp_drives (
        id TEXT PRIMARY KEY,
        gameId TEXT,
        offense TEXT,
        offenseConference TEXT,
        defense TEXT,
        defenseConference TEXT,
        driveNumber INTEGER,
        scoring BOOLEAN,
        startPeriod INTEGER,
        startYardline INTEGER,
        startYardsToGoal INTEGER,
        startTime TEXT,
        endPeriod INTEGER,
        endYardline INTEGER,
        endYardsToGoal INTEGER,
        endTime TEXT,
        elapsed TEXT,
        plays INTEGER,
        yards INTEGER,
        driveResult TEXT,
        isHomeOffense BOOLEAN,
        startOffenseScore INTEGER,
        startDefenseScore INTEGER,
        endOffenseScore INTEGER,
        endDefenseScore INTEGER
    )
    ''')
    
    # Create plays table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cfp_plays (
        gameId TEXT,
        driveId TEXT,
        id TEXT PRIMARY KEY,
        driveNumber INTEGER,
        playNumber INTEGER,
        offense TEXT,
        offenseConference TEXT,
        offenseScore INTEGER,
        defense TEXT,
        defenseConference TEXT,
        defenseScore INTEGER,
        home TEXT,
        away TEXT,
        period INTEGER,
        clock TEXT,
        offenseTimeouts INTEGER,
        defenseTimeouts INTEGER,
        yardline INTEGER,
        yardsToGoal INTEGER,
        down INTEGER,
        distance INTEGER,
        yardsGained INTEGER,
        scoring BOOLEAN,
        playType TEXT,
        playText TEXT,
        ppa REAL,
        wallclock TEXT
    )
    ''')
    
    # Clear existing data to avoid conflicts
    cursor.execute('DROP TABLE IF EXISTS cfp_drives')
    cursor.execute('DROP TABLE IF EXISTS cfp_plays')
    
    drives_folder = Path('/Users/davlenswain/Desktop/Gameday_Graphql_Model/drives')
    
    total_drives = 0
    total_plays = 0
    
    for team in cfp_teams:
        drives_file = drives_folder / f"{team}_Drives.csv"
        plays_file = drives_folder / f"{team}_Plays.csv"
        
        if drives_file.exists() and plays_file.exists():
            print(f"📊 Importing {team}...")
            
            try:
                # Import drives
                drives_df = pd.read_csv(drives_file)
                drives_count = len(drives_df)
                
                # Clean boolean columns for drives
                drives_df['scoring'] = drives_df['scoring'].map({True: 1, False: 0, 'True': 1, 'False': 0})
                drives_df['isHomeOffense'] = drives_df['isHomeOffense'].map({True: 1, False: 0, 'True': 1, 'False': 0})
                
                # Convert time columns to JSON strings
                for col in ['startTime', 'endTime', 'elapsed']:
                    if col in drives_df.columns:
                        drives_df[col] = drives_df[col].astype(str)
                
                drives_df.to_sql('cfp_drives', conn, if_exists='append', index=False)
                
                # Import plays
                plays_df = pd.read_csv(plays_file)
                plays_count = len(plays_df)
                
                # Clean boolean columns for plays
                plays_df['scoring'] = plays_df['scoring'].map({True: 1, False: 0, 'True': 1, 'False': 0})
                
                # Convert time columns to strings
                for col in ['clock', 'wallclock']:
                    if col in plays_df.columns:
                        plays_df[col] = plays_df[col].astype(str)
                
                plays_df.to_sql('cfp_plays', conn, if_exists='append', index=False)
                
                total_drives += drives_count
                total_plays += plays_count
                
                print(f"   ✅ {team}: {drives_count:,} drives, {plays_count:,} plays")
                
            except Exception as e:
                print(f"   ❌ {team}: Error importing - {str(e)}")
        else:
            print(f"   ⚠️  {team}: Missing CSV files")
    
    print(f"\n📊 IMPORT SUMMARY:")
    print(f"Total drives imported: {total_drives:,}")
    print(f"Total plays imported: {total_plays:,}")
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_drives_offense ON cfp_drives(offense)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_drives_defense ON cfp_drives(defense)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_drives_gameId ON cfp_drives(gameId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_plays_offense ON cfp_plays(offense)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_plays_defense ON cfp_plays(defense)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_plays_driveId ON cfp_plays(driveId)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cfp_plays_gameId ON cfp_plays(gameId)')
    
    conn.commit()
    
    # Analyze CFP team coverage
    print(f"\n🏈 CFP DRIVES ANALYSIS:")
    print("=" * 25)
    
    cfp_team_names = [
        'Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon',
        'Oklahoma', 'Alabama', 'Ole Miss', 'Tulane', 'Texas A&M',
        'Miami', 'James Madison'
    ]
    
    drives_by_team = {}
    plays_by_team = {}
    
    for team in cfp_team_names:
        # Count drives where team is offense
        cursor.execute('SELECT COUNT(*) FROM cfp_drives WHERE offense = ?', (team,))
        off_drives = cursor.fetchone()[0]
        
        # Count drives where team is defense (for completeness)
        cursor.execute('SELECT COUNT(*) FROM cfp_drives WHERE defense = ?', (team,))
        def_drives = cursor.fetchone()[0]
        
        total_drives = off_drives + def_drives
        
        # Count plays
        cursor.execute('SELECT COUNT(*) FROM cfp_plays WHERE offense = ? OR defense = ?', (team, team))
        team_plays = cursor.fetchone()[0]
        
        if total_drives > 0:
            drives_by_team[team] = total_drives
            plays_by_team[team] = team_plays
            print(f"{team}: {total_drives:,} drives, {team_plays:,} plays")
    
    cfp_coverage = len(drives_by_team)
    total_cfp_drives = sum(drives_by_team.values())
    total_cfp_plays = sum(plays_by_team.values())
    
    print(f"\n🎯 FINAL CFP COVERAGE:")
    print(f"Teams with data: {cfp_coverage}/12")
    print(f"Total CFP drives: {total_cfp_drives:,}")
    print(f"Total CFP plays: {total_cfp_plays:,}")
    
    # Updated weighting recommendation
    print(f"\n🔥 NUCLEAR CFP PREDICTOR WEIGHTING:")
    print("=" * 35)
    
    if cfp_coverage >= 10:
        print("✅ DRIVES/PLAYS: NUCLEAR INCLUSION")
        print(f"   Complete data for {cfp_coverage}/12 CFP teams")
        print("")
        print("   🎯 NUCLEAR CFP PREDICTOR:")
        print("     • Direct H2H: 35%")
        print("     • Advanced metrics: 30%")
        print("     • Drive efficiency: 20%")
        print("     • Network analysis: 15%")
        
    elif cfp_coverage >= 8:
        print("✅ DRIVES/PLAYS: ENHANCED INCLUSION")
        print(f"   Strong data for {cfp_coverage}/12 CFP teams")
        print("")
        print("   🔥 ENHANCED CFP PREDICTOR:")
        print("     • Direct H2H: 40%")
        print("     • Advanced metrics: 30%")
        print("     • Drive efficiency: 15%")
        print("     • Network analysis: 15%")
    
    else:
        print("🟡 DRIVES/PLAYS: CORE MODEL")
        print(f"   Limited data for {cfp_coverage}/12 CFP teams")
        print("")
        print("   🏈 CORE CFP PREDICTOR:")
        print("     • Direct H2H: 50%")
        print("     • Advanced metrics: 30%")
        print("     • Network analysis: 20%")
    
    print(f"\n✅ NUCLEAR CFP DATA READY FOR PREDICTIONS!")
    
    conn.close()

if __name__ == "__main__":
    import_cfp_drives_and_plays()