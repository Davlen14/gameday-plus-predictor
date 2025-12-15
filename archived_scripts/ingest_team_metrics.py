#!/usr/bin/env python3
"""
Ingest team advanced metrics from College Football Data GraphQL API
Populates: SP+ Rating, FPI, SRS, Talent Composite, Recruiting Rankings
"""

import requests
import sqlite3
import time
from typing import Optional, Dict, List

class TeamMetricsIngestor:
    def __init__(self, api_key: str, db_path: str = "instance/coaches_master.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.endpoint = "https://graphql.collegefootballdata.com/v1/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.api_calls = 0
    
    def execute_graphql(self, query: str, variables: Dict = None) -> Optional[Dict]:
        """Execute a GraphQL query"""
        self.api_calls += 1
        try:
            response = requests.post(
                self.endpoint,
                json={"query": query, "variables": variables or {}},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                print(f"❌ GraphQL Error: {result['errors']}")
                return None
                
            return result.get("data")
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return None
    
    def get_team_info(self, team_name: str) -> Optional[tuple]:
        """Get team_id and teamId (API ID) from database by school name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Assuming you have a column for the API team ID - if not, we'll use the database ID
        cursor.execute("SELECT id FROM teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            # For now, return same ID for both - adjust if you have separate API ID column
            return (result[0], result[0])
        return None
    
    def fetch_all_metrics(self, team: str, year: int) -> Optional[Dict]:
        """Fetch all metrics (SP+, FPI, SRS) in one query"""
        query = """
        query ($year: smallint!, $team: String!) {
          ratings(where: {year: {_eq: $year}, team: {_eq: $team}}) {
            year
            team
            spOverall
            spOffense
            spDefense
            fpi
            srs
          }
        }
        """
        data = self.execute_graphql(query, {"year": year, "team": team})
        if data and data.get("ratings") and len(data["ratings"]) > 0:
            return data["ratings"][0]
        return None
    
    def fetch_recruiting(self, team_id: int, year: int) -> Optional[Dict]:
        """Fetch recruiting rankings for a team/year using team relation"""
        query = """
        query ($year: smallint!, $teamId: Int!) {
          recruitingTeam(where: {year: {_eq: $year}, team: {teamId: {_eq: $teamId}}}) {
            year
            rank
            points
            team {
              school
            }
          }
        }
        """
        data = self.execute_graphql(query, {"year": year, "teamId": team_id})
        if data and data.get("recruitingTeam") and len(data["recruitingTeam"]) > 0:
            return data["recruitingTeam"][0]
        return None
    
    def update_team_season(self, team_id: int, season: int, metrics: Dict):
        """Update team_seasons table with advanced metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE team_seasons 
            SET sp_rating = ?,
                sp_offense = ?,
                sp_defense = ?,
                fpi = ?,
                talent_composite = ?,
                recruiting_rank = ?,
                recruiting_points = ?
            WHERE team_id = ? AND season = ?
        """, (
            metrics.get('sp_rating'),
            metrics.get('sp_offense'),
            metrics.get('sp_defense'),
            metrics.get('fpi'),
            metrics.get('talent'),
            metrics.get('recruiting_rank'),
            metrics.get('recruiting_points'),
            team_id,
            season
        ))
        
        conn.commit()
        conn.close()
    
    def ingest_team_metrics(self, team_name: str, start_year: int = 2000, end_year: int = 2025):
        """Ingest all metrics for a team across multiple years"""
        team_info = self.get_team_info(team_name)
        if not team_info:
            print(f"❌ Team '{team_name}' not found in database")
            return False
        
        team_id, api_team_id = team_info
        
        print(f"\n{'='*80}")
        print(f"📊 INGESTING METRICS FOR {team_name} (Team ID: {team_id})")
        print(f"{'='*80}")
        
        successful_years = 0
        
        for year in range(start_year, end_year + 1):
            print(f"\n[{year}] Fetching metrics...", end=" ", flush=True)
            
            metrics = {}
            
            # Fetch all ratings in one query (SP+, FPI, SRS)
            ratings_data = self.fetch_all_metrics(team_name, year)
            if ratings_data:
                metrics['sp_rating'] = ratings_data.get('spOverall')
                metrics['sp_offense'] = ratings_data.get('spOffense')
                metrics['sp_defense'] = ratings_data.get('spDefense')
                metrics['fpi'] = ratings_data.get('fpi')
                metrics['srs'] = ratings_data.get('srs')
            
            time.sleep(0.5)  # Rate limiting
            
            # Fetch Recruiting
            recruiting_data = self.fetch_recruiting(api_team_id, year)
            if recruiting_data:
                metrics['recruiting_rank'] = recruiting_data.get('rank')
                metrics['recruiting_points'] = recruiting_data.get('points')
            
            # Update database
            if metrics:
                self.update_team_season(team_id, year, metrics)
                successful_years += 1
                print(f"✅ SP+={metrics.get('sp_rating', 'N/A')}, FPI={metrics.get('fpi', 'N/A')}, SRS={metrics.get('srs', 'N/A')}, Recruiting=#{metrics.get('recruiting_rank', 'N/A')}")
            else:
                print("⚠️  No data available")
            
            time.sleep(1)  # Rate limiting between years
        
        print(f"\n{'='*80}")
        print(f"✅ Successfully updated {successful_years}/{end_year - start_year + 1} seasons")
        print(f"📊 Total API Calls: {self.api_calls}")
        print(f"{'='*80}")
        
        return True


if __name__ == "__main__":
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    ingestor = TeamMetricsIngestor(api_key=api_key)
    
    # Ingest Ohio State metrics from 2000-2025
    ingestor.ingest_team_metrics("Ohio State", start_year=2000, end_year=2025)
