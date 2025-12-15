#!/usr/bin/env python3
"""
Track Betting Line Movements Over Time
Creates historical snapshots to show how lines move
"""

import sqlite3
from datetime import datetime
from update_betting_lines import BettingLinesUpdater

def create_history_table():
    """Create table to track line movements over time"""
    conn = sqlite3.connect('instance/predictions.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sportsbook_lines_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            provider TEXT NOT NULL,
            spread REAL,
            over_under REAL,
            home_moneyline INTEGER,
            away_moneyline INTEGER,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_game 
        ON sportsbook_lines_history(game_id, captured_at)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_teams 
        ON sportsbook_lines_history(home_team, away_team, captured_at)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Created line movement history table")

def snapshot_current_lines():
    """Take a snapshot of current lines and store in history"""
    conn = sqlite3.connect('instance/predictions.db')
    cursor = conn.cursor()
    
    # Copy current lines to history
    cursor.execute("""
        INSERT INTO sportsbook_lines_history 
        (game_id, home_team, away_team, provider, spread, over_under, 
         home_moneyline, away_moneyline, captured_at)
        SELECT 
            game_id, home_team, away_team, provider, spread, over_under,
            home_moneyline, away_moneyline, CURRENT_TIMESTAMP
        FROM sportsbook_lines
    """)
    
    count = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"✅ Captured snapshot of {count} sportsbook lines")
    return count

def show_line_movement(home_team: str = None, away_team: str = None):
    """Show line movement timeline for a specific game"""
    conn = sqlite3.connect('instance/predictions.db')
    cursor = conn.cursor()
    
    if home_team and away_team:
        cursor.execute("""
            SELECT home_team, away_team, provider, spread, over_under, captured_at
            FROM sportsbook_lines_history
            WHERE home_team LIKE ? AND away_team LIKE ?
            ORDER BY captured_at ASC, provider
        """, (f'%{home_team}%', f'%{away_team}%'))
    else:
        # Show all recent movements
        cursor.execute("""
            SELECT home_team, away_team, provider, spread, over_under, captured_at
            FROM sportsbook_lines_history
            WHERE captured_at >= datetime('now', '-7 days')
            ORDER BY captured_at ASC, game_id, provider
            LIMIT 50
        """)
    
    rows = cursor.fetchall()
    
    if not rows:
        print("No historical data found")
        return
    
    print("\n📊 LINE MOVEMENT TIMELINE")
    print("=" * 100)
    
    current_game = None
    current_time = None
    
    for row in rows:
        game_label = f"{row[1]} @ {row[0]}"
        time_label = row[5][:16]  # Show up to minutes
        
        if game_label != current_game:
            if current_game is not None:
                print()
            current_game = game_label
            current_time = None
            print(f"\n🏈 {game_label}")
            print("-" * 100)
        
        if time_label != current_time:
            current_time = time_label
            print(f"\n  {time_label}")
        
        spread_str = f"Spread: {row[3]:+.1f}" if row[3] is not None else "Spread: N/A"
        ou_str = f"O/U: {row[4]:.1f}" if row[4] is not None else "O/U: N/A"
        print(f"    {row[2]:<15} {spread_str:<15} {ou_str}")
    
    conn.close()

def calculate_movement_stats(home_team: str, away_team: str):
    """Calculate movement statistics"""
    conn = sqlite3.connect('instance/predictions.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT provider, 
               MIN(captured_at) as first_seen,
               MAX(captured_at) as last_seen,
               MIN(spread) as min_spread,
               MAX(spread) as max_spread,
               MIN(over_under) as min_ou,
               MAX(over_under) as max_ou,
               COUNT(*) as snapshots
        FROM sportsbook_lines_history
        WHERE home_team LIKE ? AND away_team LIKE ?
        GROUP BY provider
    """, (f'%{home_team}%', f'%{away_team}%'))
    
    rows = cursor.fetchall()
    
    if rows:
        print(f"\n📈 MOVEMENT STATISTICS: {away_team} @ {home_team}")
        print("=" * 100)
        
        for row in rows:
            print(f"\n{row[0]}:")
            print(f"  First captured: {row[1][:16]}")
            print(f"  Last captured:  {row[2][:16]}")
            print(f"  Spread range:   {row[3]:+.1f} to {row[4]:+.1f} (movement: {abs(row[4] - row[3]):.1f} pts)")
            if row[5] and row[6]:
                print(f"  O/U range:      {row[5]:.1f} to {row[6]:.1f} (movement: {abs(row[6] - row[5]):.1f} pts)")
            print(f"  Snapshots:      {row[7]}")
    
    conn.close()

if __name__ == '__main__':
    import sys
    
    print("=" * 100)
    print("📊 BETTING LINE MOVEMENT TRACKER")
    print("=" * 100)
    
    # Create history table if needed
    create_history_table()
    
    # Update current lines first
    print("\n1. Fetching latest lines...")
    updater = BettingLinesUpdater()
    all_games = []
    for week in range(1, 5):
        games = updater.fetch_betting_lines(season=2025, week=week, season_type='postseason')
        all_games.extend(games)
    
    if all_games:
        updater.update_database(all_games)
    
    # Take snapshot
    print("\n2. Capturing snapshot...")
    snapshot_current_lines()
    
    # Show movement for specific game if requested
    if len(sys.argv) >= 3:
        home = sys.argv[1]
        away = sys.argv[2]
        show_line_movement(home, away)
        calculate_movement_stats(home, away)
    else:
        print("\n3. Recent line movements (last 7 days):")
        show_line_movement()
        
        print("\n\n💡 To track a specific game:")
        print("   python track_line_movements.py Texas Michigan")
