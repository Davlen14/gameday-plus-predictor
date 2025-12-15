"""
NIL (Name, Image, Likeness) Database Builder
=============================================
Creates comprehensive NIL player valuation database from 2025 Player Valuation CSV.

Database Schema:
- nil_players: Individual player valuations with efficiency metrics
- nil_team_summary: Aggregated team-level NIL statistics
- nil_position_groups: Position group analytics per team
- nil_rankings: Player rankings by position and overall value
"""

import sqlite3
import csv
import os
from datetime import datetime

class NILDatabaseBuilder:
    def __init__(self, db_path='instance/coaches_master.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to database: {self.db_path}")
        
    def create_tables(self):
        """Create NIL database tables"""
        print("\n📊 Creating NIL tables...")
        
        # Main player valuations table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS nil_players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                team_name TEXT NOT NULL,
                position TEXT NOT NULL,
                position_order INTEGER,
                player_name TEXT NOT NULL,
                eff1 REAL,
                sigma1 REAL,
                eff2 REAL,
                sigma2 REAL,
                weight_2025 REAL,
                valuation INTEGER,
                is_backup BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        """)
        
        # Team-level NIL summary
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS nil_team_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER UNIQUE NOT NULL,
                team_name TEXT NOT NULL,
                total_valuation INTEGER,
                avg_valuation REAL,
                total_players INTEGER,
                qb_valuation INTEGER,
                rb_valuation INTEGER,
                wr_valuation INTEGER,
                te_valuation INTEGER,
                ol_valuation INTEGER,
                dl_valuation INTEGER,
                lb_valuation INTEGER,
                db_valuation INTEGER,
                k_valuation INTEGER,
                p_valuation INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        """)
        
        # Position group analytics
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS nil_position_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                team_name TEXT NOT NULL,
                position TEXT NOT NULL,
                total_players INTEGER,
                total_valuation INTEGER,
                avg_valuation REAL,
                avg_eff1 REAL,
                avg_eff2 REAL,
                avg_sigma1 REAL,
                avg_sigma2 REAL,
                starter_valuation INTEGER,
                backup_valuation INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(id),
                UNIQUE(team_id, position)
            )
        """)
        
        # Player rankings
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS nil_rankings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                position TEXT NOT NULL,
                overall_rank INTEGER,
                position_rank INTEGER,
                conference_rank INTEGER,
                valuation INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES nil_players(id)
            )
        """)
        
        # Create indexes for performance
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_nil_players_team ON nil_players(team_id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_nil_players_position ON nil_players(position)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_nil_players_valuation ON nil_players(valuation DESC)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_nil_team_summary_valuation ON nil_team_summary(total_valuation DESC)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_nil_position_groups_team_pos ON nil_position_groups(team_id, position)")
        
        self.conn.commit()
        print("✅ NIL tables created successfully")
        
    def parse_percentage(self, value):
        """Convert percentage string to float (e.g., '54%' -> 0.54)"""
        if not value or value == '---':
            return None
        try:
            return float(value.strip('%')) / 100.0
        except:
            return None
    
    def parse_integer(self, value):
        """Convert string to integer, handling commas (e.g., '1,000' -> 1000)"""
        if not value or value == '---':
            return 0
        try:
            return int(value.replace(',', ''))
        except:
            return 0
            
    def import_csv_data(self, csv_path):
        """Import player valuation data from CSV"""
        print(f"\n📥 Importing data from {csv_path}...")
        
        imported = 0
        errors = 0
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Parse values
                    team_id = int(row['TeamID'])
                    team_name = row['Team'].strip()
                    position = row['POS'].strip()
                    position_order = int(row['Order'])
                    player_name = row['Player'].strip()
                    eff1 = self.parse_percentage(row['Eff1'])
                    sigma1 = self.parse_percentage(row['Sigma1'])
                    eff2 = self.parse_percentage(row['Eff2'])
                    sigma2 = self.parse_percentage(row['Sigma2'])
                    weight_2025 = self.parse_percentage(row['2025 WGT'])
                    valuation = self.parse_integer(row['Valuation'])  # Handle comma-formatted numbers
                    
                    # Determine if backup (player name is '---')
                    is_backup = 1 if player_name == '---' else 0
                    
                    # Insert player
                    self.cursor.execute("""
                        INSERT INTO nil_players (
                            team_id, team_name, position, position_order, player_name,
                            eff1, sigma1, eff2, sigma2, weight_2025, valuation, is_backup
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        team_id, team_name, position, position_order, player_name,
                        eff1, sigma1, eff2, sigma2, weight_2025, valuation, is_backup
                    ))
                    
                    imported += 1
                    
                except Exception as e:
                    errors += 1
                    print(f"❌ Error importing row {imported + errors}: {e}")
                    print(f"   Data: {row}")
        
        self.conn.commit()
        print(f"✅ Imported {imported} players ({errors} errors)")
        return imported
        
    def calculate_team_summaries(self):
        """Calculate aggregated team-level statistics"""
        print("\n📊 Calculating team summaries...")
        
        # Get all unique teams
        self.cursor.execute("SELECT DISTINCT team_id, team_name FROM nil_players ORDER BY team_id")
        teams = self.cursor.fetchall()
        
        for team_id, team_name in teams:
            # Overall stats
            self.cursor.execute("""
                SELECT 
                    SUM(valuation) as total_val,
                    AVG(valuation) as avg_val,
                    COUNT(*) as player_count
                FROM nil_players 
                WHERE team_id = ?
            """, (team_id,))
            total_val, avg_val, player_count = self.cursor.fetchone()
            
            # Position-specific valuations
            position_vals = {}
            positions = ['QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'DB', 'K', 'P']
            
            for pos in positions:
                self.cursor.execute("""
                    SELECT COALESCE(SUM(valuation), 0)
                    FROM nil_players 
                    WHERE team_id = ? AND position = ?
                """, (team_id, pos))
                position_vals[pos] = self.cursor.fetchone()[0]
            
            # Insert or update team summary
            self.cursor.execute("""
                INSERT OR REPLACE INTO nil_team_summary (
                    team_id, team_name, total_valuation, avg_valuation, total_players,
                    qb_valuation, rb_valuation, wr_valuation, te_valuation, ol_valuation,
                    dl_valuation, lb_valuation, db_valuation, k_valuation, p_valuation,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                team_id, team_name, total_val, avg_val, player_count,
                position_vals['QB'], position_vals['RB'], position_vals['WR'], 
                position_vals['TE'], position_vals['OL'], position_vals['DL'],
                position_vals['LB'], position_vals['DB'], position_vals['K'], position_vals['P']
            ))
        
        self.conn.commit()
        print(f"✅ Calculated summaries for {len(teams)} teams")
        
    def calculate_position_groups(self):
        """Calculate position group analytics"""
        print("\n📊 Calculating position group analytics...")
        
        self.cursor.execute("""
            SELECT DISTINCT team_id, team_name, position 
            FROM nil_players 
            ORDER BY team_id, position
        """)
        groups = self.cursor.fetchall()
        
        for team_id, team_name, position in groups:
            # Overall position stats
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as player_count,
                    SUM(valuation) as total_val,
                    AVG(valuation) as avg_val,
                    AVG(eff1) as avg_eff1,
                    AVG(eff2) as avg_eff2,
                    AVG(sigma1) as avg_sigma1,
                    AVG(sigma2) as avg_sigma2
                FROM nil_players 
                WHERE team_id = ? AND position = ?
            """, (team_id, position))
            stats = self.cursor.fetchone()
            
            # Starter vs backup valuations
            self.cursor.execute("""
                SELECT COALESCE(SUM(valuation), 0)
                FROM nil_players 
                WHERE team_id = ? AND position = ? AND is_backup = 0
            """, (team_id, position))
            starter_val = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT COALESCE(SUM(valuation), 0)
                FROM nil_players 
                WHERE team_id = ? AND position = ? AND is_backup = 1
            """, (team_id, position))
            backup_val = self.cursor.fetchone()[0]
            
            # Insert position group
            self.cursor.execute("""
                INSERT OR REPLACE INTO nil_position_groups (
                    team_id, team_name, position, total_players, total_valuation, avg_valuation,
                    avg_eff1, avg_eff2, avg_sigma1, avg_sigma2, starter_valuation, backup_valuation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id, team_name, position, 
                stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6],
                starter_val, backup_val
            ))
        
        self.conn.commit()
        print(f"✅ Calculated analytics for {len(groups)} position groups")
        
    def calculate_rankings(self):
        """Calculate player rankings"""
        print("\n📊 Calculating player rankings...")
        
        # Get all players with valuations
        self.cursor.execute("""
            SELECT id, position, valuation 
            FROM nil_players 
            WHERE valuation > 0 
            ORDER BY valuation DESC
        """)
        all_players = self.cursor.fetchall()
        
        # Overall rankings
        for overall_rank, (player_id, position, valuation) in enumerate(all_players, 1):
            # Position rank
            self.cursor.execute("""
                SELECT COUNT(*) + 1
                FROM nil_players 
                WHERE position = ? AND valuation > ? AND valuation > 0
            """, (position, valuation))
            position_rank = self.cursor.fetchone()[0]
            
            # Insert ranking
            self.cursor.execute("""
                INSERT OR REPLACE INTO nil_rankings (
                    player_id, position, overall_rank, position_rank, valuation
                ) VALUES (?, ?, ?, ?, ?)
            """, (player_id, position, overall_rank, position_rank, valuation))
        
        self.conn.commit()
        print(f"✅ Calculated rankings for {len(all_players)} players")
        
    def print_statistics(self):
        """Print database statistics"""
        print("\n" + "="*70)
        print("📈 NIL DATABASE STATISTICS")
        print("="*70)
        
        # Total players
        self.cursor.execute("SELECT COUNT(*), SUM(valuation) FROM nil_players")
        player_count, total_val = self.cursor.fetchone()
        print(f"\n👥 Total Players: {player_count:,}")
        print(f"💰 Total Valuation: ${total_val:,}")
        
        # Teams
        self.cursor.execute("SELECT COUNT(*) FROM nil_team_summary")
        team_count = self.cursor.fetchone()[0]
        print(f"🏈 Teams: {team_count}")
        
        # Top 10 teams by valuation
        print("\n🏆 TOP 10 TEAMS BY TOTAL NIL VALUATION:")
        self.cursor.execute("""
            SELECT team_name, total_valuation, total_players, avg_valuation
            FROM nil_team_summary 
            ORDER BY total_valuation DESC 
            LIMIT 10
        """)
        for i, (name, total, players, avg) in enumerate(self.cursor.fetchall(), 1):
            print(f"  {i:2d}. {name:25s} - ${total:7,} ({players:3d} players, avg: ${avg:6,.0f})")
        
        # Top 10 players by valuation
        print("\n⭐ TOP 10 PLAYERS BY NIL VALUATION:")
        self.cursor.execute("""
            SELECT p.player_name, p.position, p.team_name, p.valuation, r.overall_rank
            FROM nil_players p
            LEFT JOIN nil_rankings r ON p.id = r.player_id
            WHERE p.is_backup = 0
            ORDER BY p.valuation DESC 
            LIMIT 10
        """)
        for rank, (name, pos, team, val, overall_rank) in enumerate(self.cursor.fetchall(), 1):
            print(f"  {rank:2d}. {name:30s} ({pos:2s}) - {team:25s} - ${val:6,}")
        
        # Position breakdown
        print("\n📊 VALUATION BY POSITION:")
        self.cursor.execute("""
            SELECT position, COUNT(*) as players, SUM(valuation) as total, AVG(valuation) as avg
            FROM nil_players 
            GROUP BY position 
            ORDER BY total DESC
        """)
        for pos, count, total, avg in self.cursor.fetchall():
            print(f"  {pos:3s}: {count:4d} players, ${total:8,} total, ${avg:6,.0f} avg")
        
        # Starter vs Backup
        print("\n👥 STARTER VS BACKUP ANALYSIS:")
        self.cursor.execute("""
            SELECT 
                SUM(CASE WHEN is_backup = 0 THEN 1 ELSE 0 END) as starters,
                SUM(CASE WHEN is_backup = 0 THEN valuation ELSE 0 END) as starter_val,
                SUM(CASE WHEN is_backup = 1 THEN 1 ELSE 0 END) as backups,
                SUM(CASE WHEN is_backup = 1 THEN valuation ELSE 0 END) as backup_val
            FROM nil_players
        """)
        starters, starter_val, backups, backup_val = self.cursor.fetchone()
        print(f"  Starters: {starters:4d} players, ${starter_val:10,} total, ${starter_val/starters:6,.0f} avg")
        print(f"  Backups:  {backups:4d} players, ${backup_val:10,} total, ${backup_val/backups:6,.0f} avg")
        
        print("\n" + "="*70)
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✅ Database connection closed")


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("🏈 NIL DATABASE BUILDER")
    print("="*70)
    
    # CSV file path
    csv_path = '/Users/davlenswain/Downloads/2025 Player Valuation.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    # Build database
    builder = NILDatabaseBuilder()
    
    try:
        builder.connect()
        builder.create_tables()
        builder.import_csv_data(csv_path)
        builder.calculate_team_summaries()
        builder.calculate_position_groups()
        builder.calculate_rankings()
        builder.print_statistics()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        builder.close()
    
    print("\n✅ NIL database build complete!")
    print(f"📁 Database location: instance/coaches_master.db")
    print("\n")


if __name__ == '__main__':
    main()
