#!/usr/bin/env python3
"""
Update Betting Lines from GraphQL API
Fetches latest lines from multiple sportsbooks and stores them in database
"""

import sqlite3
import requests
from datetime import datetime
import json

class BettingLinesUpdater:
    def __init__(self):
        self.db_path = 'instance/predictions.db'
        self.api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
    
    def create_sportsbook_lines_table(self):
        """Create table to store multiple sportsbook lines per game"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sportsbook_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                provider TEXT NOT NULL,
                spread REAL,
                over_under REAL,
                home_moneyline INTEGER,
                away_moneyline INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(game_id, provider)
            )
        """)
        
        # Create index for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sportsbook_game 
            ON sportsbook_lines(game_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sportsbook_teams 
            ON sportsbook_lines(home_team, away_team)
        """)
        
        conn.commit()
        conn.close()
        print("✅ Created sportsbook_lines table")
    
    def fetch_betting_lines(self, season: int = 2025, week: int = 1, season_type: str = 'postseason'):
        """Fetch betting lines from GraphQL API"""
        query = """
        query {
          game(where: {
            season: {_eq: %d}, 
            week: {_eq: %d},
            seasonType: {_eq: "%s"}
          }) {
            id
            homeTeam
            awayTeam
            lines {
              provider {
                name
              }
              spread
              overUnder
            }
          }
        }
        """ % (season, week, season_type)
        
        try:
            print(f"🔍 Fetching lines for {season_type} week {week}...")
            response = requests.post(
                self.graphql_url,
                json={"query": query},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'errors' in data:
                    print(f"❌ GraphQL errors: {json.dumps(data['errors'], indent=2)}")
                    return []
                
                games = data.get('data', {}).get('game', [])
                print(f"✅ Fetched {len(games)} games")
                return games
            else:
                print(f"❌ API returned status {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching betting lines: {e}")
            return []
    
    def update_database(self, games):
        """Update database with fetched betting lines"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updated_count = 0
        inserted_count = 0
        
        for game in games:
            game_id = game.get('id')
            home_team = game.get('homeTeam')
            away_team = game.get('awayTeam')
            lines = game.get('lines', [])
            
            if not lines:
                continue
            
            for line in lines:
                provider_obj = line.get('provider', {})
                provider = provider_obj.get('name') if isinstance(provider_obj, dict) else str(provider_obj)
                spread = line.get('spread')
                over_under = line.get('overUnder')
                home_ml = None  # Moneylines not available in API
                away_ml = None  # Moneylines not available in API
                
                # Skip if no actual line data
                if spread is None and over_under is None:
                    continue
                
                try:
                    # Try to update existing record
                    cursor.execute("""
                        INSERT INTO sportsbook_lines 
                        (game_id, home_team, away_team, provider, spread, over_under, 
                         home_moneyline, away_moneyline, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(game_id, provider) 
                        DO UPDATE SET
                            spread = excluded.spread,
                            over_under = excluded.over_under,
                            home_moneyline = excluded.home_moneyline,
                            away_moneyline = excluded.away_moneyline,
                            updated_at = CURRENT_TIMESTAMP
                    """, (game_id, home_team, away_team, provider, spread, over_under, home_ml, away_ml))
                    
                    if cursor.rowcount > 0:
                        if cursor.lastrowid:
                            inserted_count += 1
                        else:
                            updated_count += 1
                
                except Exception as e:
                    print(f"⚠️ Error updating {home_team} vs {away_team} ({provider}): {e}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Updated {updated_count} lines, inserted {inserted_count} new lines")
        return updated_count + inserted_count
    
    def run(self):
        """Main execution"""
        print("="*80)
        print("🏈 BETTING LINES UPDATER")
        print("="*80)
        
        # Create table if it doesn't exist
        self.create_sportsbook_lines_table()
        
        # Fetch postseason lines (weeks 1-2 typically cover bowl games)
        all_games = []
        for week in range(1, 5):  # Check weeks 1-4 for postseason
            games = self.fetch_betting_lines(season=2025, week=week, season_type='postseason')
            all_games.extend(games)
        
        if all_games:
            total = self.update_database(all_games)
            print(f"\n🎯 Total: {total} sportsbook lines updated")
        else:
            print("\n⚠️ No games fetched")
        
        # Show summary
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT provider, COUNT(*) 
            FROM sportsbook_lines 
            GROUP BY provider 
            ORDER BY COUNT(*) DESC
        """)
        
        print("\n📊 Sportsbook Coverage:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} games")
        
        conn.close()
        print("\n✅ Update complete!")

if __name__ == '__main__':
    updater = BettingLinesUpdater()
    updater.run()
