"""
Backfill helper to populate missing opponent data in games table
Fetches opponent_logo, opponent_sp_overall, opponent_sp_offense, opponent_sp_defense, opponent_fpi, opponent_srs
from teams table and ESPN API
"""
import sqlite3
import time
from typing import Dict, Optional
import requests

DB_PATH = 'instance/coaches_master.db'

class GameDataBackfill:
    """Backfills missing opponent data in games table"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.updated_count = 0
        self.failed_count = 0
        
    def get_team_data(self, team_name: str) -> Optional[Dict]:
        """Get team data from teams table"""
        # Try exact match first
        self.cursor.execute("""
            SELECT school, logo_url as logo, color, alt_color
            FROM teams 
            WHERE school = ?
        """, (team_name,))
        
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        
        # Try fuzzy match - first word
        team_first_word = team_name.split()[0]
        self.cursor.execute("""
            SELECT school, logo_url as logo, color, alt_color
            FROM teams 
            WHERE school LIKE ?
            LIMIT 1
        """, (f"{team_first_word}%",))
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def backfill_opponent_data(self, limit: Optional[int] = None, only_nulls: bool = True):
        """
        Backfill missing opponent data
        
        Args:
            limit: Maximum number of records to update (None = all)
            only_nulls: Only update records where opponent_logo is NULL
        """
        print("🔄 Starting opponent data backfill...")
        
        # Get games that need backfill
        query = """
            SELECT DISTINCT opponent 
            FROM games 
        """
        if only_nulls:
            query += " WHERE opponent_logo IS NULL OR opponent_sp_overall IS NULL"
        
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        opponents = [row[0] for row in self.cursor.fetchall()]
        
        print(f"📊 Found {len(opponents)} unique opponents to backfill")
        
        for i, opponent in enumerate(opponents, 1):
            print(f"\n[{i}/{len(opponents)}] Processing: {opponent}")
            
            team_data = self.get_team_data(opponent)
            
            if team_data:
                # Update all games for this opponent (just logo for now - SP+/FPI/SRS not in DB yet)
                self.cursor.execute("""
                    UPDATE games 
                    SET opponent_logo = ?
                    WHERE opponent = ? AND opponent_logo IS NULL
                """, (
                    team_data.get('logo'),
                    opponent
                ))
                
                updated = self.cursor.rowcount
                self.updated_count += updated
                print(f"  ✅ Updated {updated} game(s) for {opponent}")
            else:
                self.failed_count += 1
                print(f"  ❌ No team data found for {opponent}")
        
        self.conn.commit()
        print(f"\n✅ Backfill complete!")
        print(f"   Updated: {self.updated_count} games")
        print(f"   Failed:  {self.failed_count} opponents (no data found)")
    
    def populate_vs_coaches(self):
        """
        Populate vs_coaches table by deriving head-to-head records from games table
        """
        print("\n🔄 Populating vs_coaches table from games...")
        
        # Clear existing data
        self.cursor.execute("DELETE FROM vs_coaches")
        
        # Get all coach matchups from games
        self.cursor.execute("""
            SELECT 
                g1.coach_id as coach_id,
                c2.name as opponent_coach,
                g2.school as opponent_school,
                SUM(CASE WHEN g1.result = 'W' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN g1.result = 'L' THEN 1 ELSE 0 END) as losses,
                AVG(g1.coach_score - g1.opponent_score) as avg_point_diff,
                MAX(g1.coach_score - g1.opponent_score) as biggest_win_margin,
                MIN(g1.coach_score - g1.opponent_score) as biggest_loss_margin,
                MIN(g1.season) as first_meeting_year,
                MAX(g1.season) as last_meeting_year
            FROM games g1
            LEFT JOIN games g2 ON 
                g1.season = g2.season AND 
                g1.week = g2.week AND
                g1.opponent = g2.school AND
                g1.school = g2.opponent
            LEFT JOIN coaches c2 ON g2.coach_id = c2.id
            WHERE g2.coach_id IS NOT NULL
            GROUP BY g1.coach_id, c2.name, g2.school
            HAVING COUNT(*) > 0
        """)
        
        matchups = self.cursor.fetchall()
        print(f"📊 Found {len(matchups)} unique coach matchups")
        
        inserted = 0
        for matchup in matchups:
            coach_id = matchup[0]
            opponent_coach = matchup[1]
            opponent_school = matchup[2]
            
            # Skip if opponent coach is NULL
            if not opponent_coach:
                continue
                
            wins = matchup[3]
            losses = matchup[4]
            record = f"{wins}-{losses}"
            avg_diff = matchup[5]
            biggest_win = matchup[6]
            biggest_loss = matchup[7]
            first_year = matchup[8]
            last_year = matchup[9]
            
            self.cursor.execute("""
                INSERT INTO vs_coaches 
                (coach_id, opponent_coach, opponent_school, wins, losses, record,
                 avg_point_differential, biggest_win_margin, biggest_loss_margin,
                 first_meeting_year, last_meeting_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                coach_id, opponent_coach, opponent_school, wins, losses, record,
                avg_diff, biggest_win, biggest_loss, first_year, last_year
            ))
            inserted += 1
        
        self.conn.commit()
        print(f"✅ Populated {inserted} vs_coaches records")
    
    def get_stats(self):
        """Print current backfill statistics"""
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(opponent_logo) as has_logo,
                COUNT(opponent_sp_overall) as has_sp,
                COUNT(opponent_fpi) as has_fpi,
                COUNT(opponent_srs) as has_srs
            FROM games
        """)
        
        stats = self.cursor.fetchone()
        print("\n📊 Current games table statistics:")
        print(f"   Total games:       {stats[0]:,}")
        print(f"   Has opponent_logo: {stats[1]:,} ({stats[1]/stats[0]*100:.1f}%)")
        print(f"   Has opponent_sp:   {stats[2]:,} ({stats[2]/stats[0]*100:.1f}%)")
        print(f"   Has opponent_fpi:  {stats[3]:,} ({stats[3]/stats[0]*100:.1f}%)")
        print(f"   Has opponent_srs:  {stats[4]:,} ({stats[4]/stats[0]*100:.1f}%)")
        
        self.cursor.execute("SELECT COUNT(*) FROM vs_coaches")
        vs_coaches_count = self.cursor.fetchone()[0]
        print(f"\n📊 vs_coaches table: {vs_coaches_count:,} records")
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Run backfill process"""
    backfill = GameDataBackfill()
    
    # Show current stats
    backfill.get_stats()
    
    # Run backfill
    print("\n" + "="*60)
    backfill.backfill_opponent_data(only_nulls=True)
    
    # Populate vs_coaches
    print("\n" + "="*60)
    backfill.populate_vs_coaches()
    
    # Show final stats
    print("\n" + "="*60)
    backfill.get_stats()
    
    backfill.close()
    print("\n✅ All done!")


if __name__ == '__main__':
    main()
