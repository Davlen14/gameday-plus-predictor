#!/usr/bin/env python3
"""
COMPREHENSIVE Team Metrics Ingestion - REST API
Captures EVERY available metric from College Football Data API
"""

import requests
import sqlite3
import time
import json
from typing import Optional, Dict, List

class ComprehensiveTeamMetricsIngestor:
    def __init__(self, api_key: str, db_path: str = "instance/coaches_master.db"):
        self.api_key = api_key
        self.db_path = db_path
        self.base_url = "https://api.collegefootballdata.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "accept": "application/json"
        }
        self.api_calls = 0
    
    def execute_rest(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Execute a REST API call"""
        self.api_calls += 1
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params or {},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ REST Error: {str(e)}")
            return None
    
    def ensure_columns_exist(self):
        """Add all necessary columns to team_seasons table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(team_seasons)")
        existing_cols = {row[1] for row in cursor.fetchall()}
        
        # Define ALL columns we need
        new_columns = {
            # SP+ Rankings
            'sp_ranking': 'INTEGER',
            'sp_special_teams': 'REAL',
            'sp_second_order_wins': 'REAL',
            'sp_sos': 'REAL',
            
            # FPI Rankings & Efficiencies
            'fpi_ranking': 'INTEGER',
            'fpi_strength_of_record': 'INTEGER',
            'fpi_avg_win_probability': 'INTEGER',
            'fpi_strength_of_schedule': 'INTEGER',
            'fpi_remaining_sos': 'INTEGER',
            'fpi_game_control': 'INTEGER',
            'fpi_overall_efficiency': 'REAL',
            'fpi_offense_efficiency': 'REAL',
            'fpi_defense_efficiency': 'REAL',
            'fpi_special_teams_efficiency': 'REAL',
            
            # Elo Rating
            'elo_rating': 'INTEGER',
            
            # Advanced Offense Stats
            'off_plays': 'INTEGER',
            'off_drives': 'INTEGER',
            'off_ppa': 'REAL',
            'off_total_ppa': 'REAL',
            'off_success_rate': 'REAL',
            'off_explosiveness': 'REAL',
            'off_power_success': 'REAL',
            'off_stuff_rate': 'REAL',
            'off_line_yards': 'REAL',
            'off_line_yards_total': 'INTEGER',
            'off_second_level_yards': 'REAL',
            'off_second_level_yards_total': 'INTEGER',
            'off_open_field_yards': 'REAL',
            'off_open_field_yards_total': 'INTEGER',
            'off_total_opportunities': 'INTEGER',
            'off_points_per_opportunity': 'REAL',
            'off_field_pos_avg_start': 'REAL',
            'off_field_pos_avg_predicted_points': 'REAL',
            'off_havoc_total': 'REAL',
            'off_havoc_front_seven': 'REAL',
            'off_havoc_db': 'REAL',
            
            # Offense Standard Downs
            'off_std_rate': 'REAL',
            'off_std_ppa': 'REAL',
            'off_std_success_rate': 'REAL',
            'off_std_explosiveness': 'REAL',
            
            # Offense Passing Downs
            'off_pass_down_rate': 'REAL',
            'off_pass_down_ppa': 'REAL',
            'off_pass_down_success_rate': 'REAL',
            'off_pass_down_explosiveness': 'REAL',
            
            # Offense Rushing Plays
            'off_rush_rate': 'REAL',
            'off_rush_ppa': 'REAL',
            'off_rush_total_ppa': 'REAL',
            'off_rush_success_rate': 'REAL',
            'off_rush_explosiveness': 'REAL',
            
            # Offense Passing Plays
            'off_pass_rate': 'REAL',
            'off_pass_ppa': 'REAL',
            'off_pass_total_ppa': 'REAL',
            'off_pass_success_rate': 'REAL',
            'off_pass_explosiveness': 'REAL',
            
            # Advanced Defense Stats
            'def_plays': 'INTEGER',
            'def_drives': 'INTEGER',
            'def_ppa': 'REAL',
            'def_total_ppa': 'REAL',
            'def_success_rate': 'REAL',
            'def_explosiveness': 'REAL',
            'def_power_success': 'REAL',
            'def_stuff_rate': 'REAL',
            'def_line_yards': 'REAL',
            'def_line_yards_total': 'INTEGER',
            'def_second_level_yards': 'REAL',
            'def_second_level_yards_total': 'INTEGER',
            'def_open_field_yards': 'REAL',
            'def_open_field_yards_total': 'INTEGER',
            'def_total_opportunities': 'INTEGER',
            'def_points_per_opportunity': 'REAL',
            'def_field_pos_avg_start': 'REAL',
            'def_field_pos_avg_predicted_points': 'REAL',
            'def_havoc_total': 'REAL',
            'def_havoc_front_seven': 'REAL',
            'def_havoc_db': 'REAL',
            
            # Defense Standard Downs
            'def_std_rate': 'REAL',
            'def_std_ppa': 'REAL',
            'def_std_success_rate': 'REAL',
            'def_std_explosiveness': 'REAL',
            
            # Defense Passing Downs
            'def_pass_down_rate': 'REAL',
            'def_pass_down_ppa': 'REAL',
            'def_pass_down_total_ppa': 'REAL',
            'def_pass_down_success_rate': 'REAL',
            'def_pass_down_explosiveness': 'REAL',
            
            # Defense Rushing Plays
            'def_rush_rate': 'REAL',
            'def_rush_ppa': 'REAL',
            'def_rush_total_ppa': 'REAL',
            'def_rush_success_rate': 'REAL',
            'def_rush_explosiveness': 'REAL',
            
            # Defense Passing Plays
            'def_pass_rate': 'REAL',
            'def_pass_ppa': 'REAL',
            'def_pass_total_ppa': 'REAL',
            'def_pass_success_rate': 'REAL',
            'def_pass_explosiveness': 'REAL',
        }
        
        # Add missing columns
        added = 0
        for col_name, col_type in new_columns.items():
            if col_name not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE team_seasons ADD COLUMN {col_name} {col_type}")
                    added += 1
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        print(f"⚠️  Could not add column {col_name}: {e}")
        
        conn.commit()
        conn.close()
        
        if added > 0:
            print(f"✅ Added {added} new columns to team_seasons table")
        
        return True
    
    def fetch_sp_ratings(self, team: str, year: int) -> Optional[Dict]:
        """Fetch SP+ ratings"""
        data = self.execute_rest("/ratings/sp", {"year": year, "team": team})
        if data and len(data) > 0:
            return data[0]  # First result is the team, second is national averages
        return None
    
    def fetch_fpi(self, team: str, year: int) -> Optional[Dict]:
        """Fetch FPI ratings and efficiencies"""
        data = self.execute_rest("/ratings/fpi", {"year": year, "team": team})
        if data and len(data) > 0:
            return data[0]
        return None
    
    def fetch_talent(self, year: int) -> Optional[List[Dict]]:
        """Fetch all talent ratings for a year"""
        return self.execute_rest("/talent", {"year": year})
    
    def fetch_recruiting(self, year: int) -> Optional[List[Dict]]:
        """Fetch all recruiting rankings for a year"""
        return self.execute_rest("/recruiting/teams", {"year": year})
    
    def fetch_advanced_stats(self, team: str, year: int) -> Optional[Dict]:
        """Fetch advanced season stats"""
        data = self.execute_rest("/stats/season/advanced", {"year": year, "team": team})
        if data and len(data) > 0:
            return data[0]
        return None
    
    def update_team_season(self, team_id: int, season: int, metrics: Dict):
        """Update team_seasons table with comprehensive metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        
        for key, value in metrics.items():
            if value is not None:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if set_clauses:
            values.extend([team_id, season])
            query = f"""
                UPDATE team_seasons 
                SET {', '.join(set_clauses)}
                WHERE team_id = ? AND season = ?
            """
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    def ingest_team_metrics(self, team_name: str, start_year: int = 2000, end_year: int = 2025):
        """Ingest ALL metrics for a team across multiple years"""
        # Ensure all columns exist
        self.ensure_columns_exist()
        
        # Get team ID
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM teams WHERE school = ?", (team_name,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            print(f"❌ Team '{team_name}' not found in database")
            return False
        
        team_id = result[0]
        
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE METRICS INGESTION: {team_name} (ID: {team_id})")
        print(f"{'='*80}")
        
        successful_years = 0
        
        for year in range(start_year, end_year + 1):
            print(f"\n[{year}] Fetching comprehensive metrics...", end=" ", flush=True)
            
            metrics = {}
            
            # 1. SP+ Ratings
            sp_data = self.fetch_sp_ratings(team_name, year)
            if sp_data:
                metrics['sp_rating'] = sp_data.get('rating')
                metrics['sp_ranking'] = sp_data.get('ranking')
                metrics['sp_second_order_wins'] = sp_data.get('secondOrderWins')
                metrics['sp_sos'] = sp_data.get('sos')
                
                if sp_data.get('offense'):
                    metrics['sp_offense'] = sp_data['offense'].get('rating')
                if sp_data.get('defense'):
                    metrics['sp_defense'] = sp_data['defense'].get('rating')
                if sp_data.get('specialTeams'):
                    metrics['sp_special_teams'] = sp_data['specialTeams'].get('rating')
            
            time.sleep(0.3)
            
            # 2. FPI Ratings
            fpi_data = self.fetch_fpi(team_name, year)
            if fpi_data:
                metrics['fpi'] = fpi_data.get('fpi')
                
                if fpi_data.get('resumeRanks'):
                    rr = fpi_data['resumeRanks']
                    metrics['fpi_ranking'] = rr.get('fpi')
                    metrics['fpi_strength_of_record'] = rr.get('strengthOfRecord')
                    metrics['fpi_avg_win_probability'] = rr.get('averageWinProbability')
                    metrics['fpi_strength_of_schedule'] = rr.get('strengthOfSchedule')
                    metrics['fpi_remaining_sos'] = rr.get('remainingStrengthOfSchedule')
                    metrics['fpi_game_control'] = rr.get('gameControl')
                
                if fpi_data.get('efficiencies'):
                    eff = fpi_data['efficiencies']
                    metrics['fpi_overall_efficiency'] = eff.get('overall')
                    metrics['fpi_offense_efficiency'] = eff.get('offense')
                    metrics['fpi_defense_efficiency'] = eff.get('defense')
                    metrics['fpi_special_teams_efficiency'] = eff.get('specialTeams')
            
            time.sleep(0.3)
            
            # 3. Advanced Stats (HUGE)
            adv_data = self.fetch_advanced_stats(team_name, year)
            if adv_data:
                # Offense
                if adv_data.get('offense'):
                    off = adv_data['offense']
                    metrics['off_plays'] = off.get('plays')
                    metrics['off_drives'] = off.get('drives')
                    metrics['off_ppa'] = off.get('ppa')
                    metrics['off_total_ppa'] = off.get('totalPPA')
                    metrics['off_success_rate'] = off.get('successRate')
                    metrics['off_explosiveness'] = off.get('explosiveness')
                    metrics['off_power_success'] = off.get('powerSuccess')
                    metrics['off_stuff_rate'] = off.get('stuffRate')
                    metrics['off_line_yards'] = off.get('lineYards')
                    metrics['off_line_yards_total'] = off.get('lineYardsTotal')
                    metrics['off_second_level_yards'] = off.get('secondLevelYards')
                    metrics['off_second_level_yards_total'] = off.get('secondLevelYardsTotal')
                    metrics['off_open_field_yards'] = off.get('openFieldYards')
                    metrics['off_open_field_yards_total'] = off.get('openFieldYardsTotal')
                    metrics['off_total_opportunities'] = off.get('totalOpportunies')  # Note: API typo
                    metrics['off_points_per_opportunity'] = off.get('pointsPerOpportunity')
                    
                    if off.get('fieldPosition'):
                        metrics['off_field_pos_avg_start'] = off['fieldPosition'].get('averageStart')
                        metrics['off_field_pos_avg_predicted_points'] = off['fieldPosition'].get('averagePredictedPoints')
                    
                    if off.get('havoc'):
                        metrics['off_havoc_total'] = off['havoc'].get('total')
                        metrics['off_havoc_front_seven'] = off['havoc'].get('frontSeven')
                        metrics['off_havoc_db'] = off['havoc'].get('db')
                    
                    if off.get('standardDowns'):
                        sd = off['standardDowns']
                        metrics['off_std_rate'] = sd.get('rate')
                        metrics['off_std_ppa'] = sd.get('ppa')
                        metrics['off_std_success_rate'] = sd.get('successRate')
                        metrics['off_std_explosiveness'] = sd.get('explosiveness')
                    
                    if off.get('passingDowns'):
                        pd = off['passingDowns']
                        metrics['off_pass_down_rate'] = pd.get('rate')
                        metrics['off_pass_down_ppa'] = pd.get('ppa')
                        metrics['off_pass_down_success_rate'] = pd.get('successRate')
                        metrics['off_pass_down_explosiveness'] = pd.get('explosiveness')
                    
                    if off.get('rushingPlays'):
                        rp = off['rushingPlays']
                        metrics['off_rush_rate'] = rp.get('rate')
                        metrics['off_rush_ppa'] = rp.get('ppa')
                        metrics['off_rush_total_ppa'] = rp.get('totalPPA')
                        metrics['off_rush_success_rate'] = rp.get('successRate')
                        metrics['off_rush_explosiveness'] = rp.get('explosiveness')
                    
                    if off.get('passingPlays'):
                        pp = off['passingPlays']
                        metrics['off_pass_rate'] = pp.get('rate')
                        metrics['off_pass_ppa'] = pp.get('ppa')
                        metrics['off_pass_total_ppa'] = pp.get('totalPPA')
                        metrics['off_pass_success_rate'] = pp.get('successRate')
                        metrics['off_pass_explosiveness'] = pp.get('explosiveness')
                
                # Defense
                if adv_data.get('defense'):
                    def_d = adv_data['defense']
                    metrics['def_plays'] = def_d.get('plays')
                    metrics['def_drives'] = def_d.get('drives')
                    metrics['def_ppa'] = def_d.get('ppa')
                    metrics['def_total_ppa'] = def_d.get('totalPPA')
                    metrics['def_success_rate'] = def_d.get('successRate')
                    metrics['def_explosiveness'] = def_d.get('explosiveness')
                    metrics['def_power_success'] = def_d.get('powerSuccess')
                    metrics['def_stuff_rate'] = def_d.get('stuffRate')
                    metrics['def_line_yards'] = def_d.get('lineYards')
                    metrics['def_line_yards_total'] = def_d.get('lineYardsTotal')
                    metrics['def_second_level_yards'] = def_d.get('secondLevelYards')
                    metrics['def_second_level_yards_total'] = def_d.get('secondLevelYardsTotal')
                    metrics['def_open_field_yards'] = def_d.get('openFieldYards')
                    metrics['def_open_field_yards_total'] = def_d.get('openFieldYardsTotal')
                    metrics['def_total_opportunities'] = def_d.get('totalOpportunies')
                    metrics['def_points_per_opportunity'] = def_d.get('pointsPerOpportunity')
                    
                    if def_d.get('fieldPosition'):
                        metrics['def_field_pos_avg_start'] = def_d['fieldPosition'].get('averageStart')
                        metrics['def_field_pos_avg_predicted_points'] = def_d['fieldPosition'].get('averagePredictedPoints')
                    
                    if def_d.get('havoc'):
                        metrics['def_havoc_total'] = def_d['havoc'].get('total')
                        metrics['def_havoc_front_seven'] = def_d['havoc'].get('frontSeven')
                        metrics['def_havoc_db'] = def_d['havoc'].get('db')
                    
                    if def_d.get('standardDowns'):
                        sd = def_d['standardDowns']
                        metrics['def_std_rate'] = sd.get('rate')
                        metrics['def_std_ppa'] = sd.get('ppa')
                        metrics['def_std_success_rate'] = sd.get('successRate')
                        metrics['def_std_explosiveness'] = sd.get('explosiveness')
                    
                    if def_d.get('passingDowns'):
                        pd = def_d['passingDowns']
                        metrics['def_pass_down_rate'] = pd.get('rate')
                        metrics['def_pass_down_ppa'] = pd.get('ppa')
                        metrics['def_pass_down_total_ppa'] = pd.get('totalPPA')
                        metrics['def_pass_down_success_rate'] = pd.get('successRate')
                        metrics['def_pass_down_explosiveness'] = pd.get('explosiveness')
                    
                    if def_d.get('rushingPlays'):
                        rp = def_d['rushingPlays']
                        metrics['def_rush_rate'] = rp.get('rate')
                        metrics['def_rush_ppa'] = rp.get('ppa')
                        metrics['def_rush_total_ppa'] = rp.get('totalPPA')
                        metrics['def_rush_success_rate'] = rp.get('successRate')
                        metrics['def_rush_explosiveness'] = rp.get('explosiveness')
                    
                    if def_d.get('passingPlays'):
                        pp = def_d['passingPlays']
                        metrics['def_pass_rate'] = pp.get('rate')
                        metrics['def_pass_ppa'] = pp.get('ppa')
                        metrics['def_pass_total_ppa'] = pp.get('totalPPA')
                        metrics['def_pass_success_rate'] = pp.get('successRate')
                        metrics['def_pass_explosiveness'] = pp.get('explosiveness')
            
            time.sleep(0.3)
            
            # 4. Talent (fetch once per year for all teams)
            # 5. Recruiting (fetch once per year for all teams)
            # These will be done in a separate batch call
            
            # Update database
            if metrics:
                self.update_team_season(team_id, year, metrics)
                successful_years += 1
                metric_count = len([v for v in metrics.values() if v is not None])
                print(f"✅ {metric_count} metrics")
            else:
                print("⚠️  No data")
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"\n{'='*80}")
        print(f"✅ Successfully updated {successful_years}/{end_year - start_year + 1} seasons")
        print(f"📊 Total API Calls: {self.api_calls}")
        print(f"{'='*80}")
        
        return True
    
    def batch_update_talent_recruiting(self, start_year: int = 2000, end_year: int = 2025):
        """Batch update talent and recruiting for all teams"""
        print(f"\n{'='*80}")
        print(f"📊 BATCH UPDATING TALENT & RECRUITING ({start_year}-{end_year})")
        print(f"{'='*80}")
        
        for year in range(start_year, end_year + 1):
            print(f"\n[{year}] Fetching talent & recruiting...", end=" ", flush=True)
            
            # Talent
            talent_data = self.fetch_talent(year)
            if talent_data:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for team_talent in talent_data:
                    team_name = team_talent.get('team')
                    talent_value = team_talent.get('talent')
                    
                    if team_name and talent_value:
                        cursor.execute("""
                            UPDATE team_seasons 
                            SET talent_composite = ?
                            WHERE season = ? AND team_id IN (
                                SELECT id FROM teams WHERE school = ?
                            )
                        """, (talent_value, year, team_name))
                
                conn.commit()
                conn.close()
            
            time.sleep(0.5)
            
            # Recruiting
            recruiting_data = self.fetch_recruiting(year)
            if recruiting_data:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for team_rec in recruiting_data:
                    team_name = team_rec.get('team')
                    rank = team_rec.get('rank')
                    points = team_rec.get('points')
                    
                    if team_name and rank:
                        cursor.execute("""
                            UPDATE team_seasons 
                            SET recruiting_rank = ?, recruiting_points = ?
                            WHERE season = ? AND team_id IN (
                                SELECT id FROM teams WHERE school = ?
                            )
                        """, (rank, points, year, team_name))
                
                conn.commit()
                conn.close()
                
                print(f"✅ Updated talent & recruiting")
            else:
                print("⚠️  No data")
            
            time.sleep(1)


if __name__ == "__main__":
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    ingestor = ComprehensiveTeamMetricsIngestor(api_key=api_key)
    
    # Get all teams from database
    conn = sqlite3.connect("instance/coaches_master.db")
    cursor = conn.cursor()
    cursor.execute("SELECT school FROM teams ORDER BY school")
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print(f"🏈 Starting ingestion for {len(teams)} teams...")
    print("=" * 80)
    
    # Ingest metrics for each team from 2000-2025
    for idx, team in enumerate(teams, 1):
        print(f"\n[{idx}/{len(teams)}] Processing {team}...")
        try:
            ingestor.ingest_team_metrics(team, start_year=2000, end_year=2025)
        except Exception as e:
            print(f"❌ Error with {team}: {e}")
            continue
    
    # Update talent & recruiting for all teams 2000-2025
    print("\n" + "=" * 80)
    print("🎓 Updating talent & recruiting data for all teams...")
    ingestor.batch_update_talent_recruiting(start_year=2000, end_year=2025)
    
    print("\n" + "=" * 80)
    print(f"✅ COMPLETE! API Calls Made: {ingestor.api_calls}")
    print("=" * 80)
