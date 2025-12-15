"""
Database Helper for College Football Predictor
Replaces JSON file loading with SQLite database queries
"""

import sqlite3
import os
from typing import Dict, List, Optional, Any
import json

class DatabaseHelper:
    """Helper class for querying prediction database"""
    
    def __init__(self, db_path: str = None, master_db_path: str = None):
        """Initialize database connections"""
        if db_path is None:
            db_path = os.path.join('instance', 'predictions.db')
        if master_db_path is None:
            master_db_path = os.path.join('instance', 'coaches_master.db')
            
        self.db_path = db_path
        self.master_db_path = master_db_path
        
    def _get_connection(self, attach_master: bool = True):
        """Get database connection with optional master DB attachment"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        
        if attach_master and os.path.exists(self.master_db_path):
            conn.execute(f"ATTACH DATABASE '{self.master_db_path}' AS master")
            
        return conn
    
    def get_drives(self, team: str = None, season: int = 2025) -> List[Dict]:
        """Get drive data for a team or all teams"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if team:
            cursor.execute("""
                SELECT d.*, t.school as team_name
                FROM drives_complete d
                LEFT JOIN master.teams t ON d.team_id = t.id
                WHERE t.school = ? AND d.season = ?
            """, (team, season))
        else:
            cursor.execute("""
                SELECT d.*, t.school as team_name
                FROM drives_complete d
                LEFT JOIN master.teams t ON d.team_id = t.id
                WHERE d.season = ?
            """, (season,))
        
        drives = []
        for row in cursor.fetchall():
            drive = dict(row)
            # Parse JSON fields
            if drive.get('plays_data'):
                drive['plays'] = json.loads(drive['plays_data'])
            drives.append(drive)
        
        conn.close()
        return drives
    
    def get_coach_rankings(self, coach_name: str = None, season: int = 2025) -> Optional[Dict]:
        """Get coach rankings data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if coach_name:
            cursor.execute("""
                SELECT cr.*, c.name, c.current_school
                FROM coach_rankings cr
                JOIN master.coaches c ON cr.coach_id = c.id
                WHERE c.name = ? AND cr.season = ?
            """, (coach_name, season))
            row = cursor.fetchone()
            result = dict(row) if row else None
        else:
            cursor.execute("""
                SELECT cr.*, c.name, c.current_school
                FROM coach_rankings cr
                JOIN master.coaches c ON cr.coach_id = c.id
                WHERE cr.season = ?
                ORDER BY cr.composite_rank
            """, (season,))
            result = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return result
    
    def get_team_rankings(self, team: str = None) -> Optional[Dict]:
        """Get team power rankings"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if team:
            cursor.execute("""
                SELECT tr.*, t.school as team_name
                FROM team_power_rankings tr
                JOIN master.teams t ON tr.team_id = t.id
                WHERE t.school = ?
            """, (team,))
            row = cursor.fetchone()
            result = dict(row) if row else None
        else:
            cursor.execute("""
                SELECT tr.*, t.school as team_name
                FROM team_power_rankings tr
                JOIN master.teams t ON tr.team_id = t.id
                ORDER BY tr.composite_rank
            """)
            result = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return result
    
    def get_conferences(self) -> List[Dict]:
        """Get conference data"""
        conn = self._get_connection(attach_master=False)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM conferences")
        conferences = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return conferences
    
    def get_team_by_name(self, team_name: str) -> Optional[Dict]:
        """Get team info from master database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM master.teams
            WHERE school = ?
        """, (team_name,))
        
        row = cursor.fetchone()
        result = dict(row) if row else None
        
        conn.close()
        return result
    
    def get_team_season_data(self, team: str, season: int = 2025) -> Optional[Dict]:
        """Get team season stats from master database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ts.*, t.school as team_name
            FROM master.team_seasons ts
            JOIN master.teams t ON ts.team_id = t.id
            WHERE t.school = ? AND ts.year = ?
        """, (team, season))
        
        row = cursor.fetchone()
        result = dict(row) if row else None
        
        conn.close()
        return result
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute custom query and return results"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_all_team_epa_stats(self, season=2025) -> List[Dict]:
        """Get EPA stats for all teams - formatted like fbs_teams_stats_only.json"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT team_name as team, season, conference,
                   off_plays, off_ppa, off_success_rate, off_explosiveness,
                   def_plays, def_ppa, def_success_rate, def_explosiveness
            FROM team_epa_metrics
            WHERE season = ?
            ORDER BY team_name
        """, (season,))
        
        teams = []
        for row in cursor.fetchall():
            team_dict = dict(row)
            # Format like JSON: nested stats object
            teams.append({
                'team': team_dict['team'],
                'season': team_dict['season'],
                'conference': team_dict['conference'],
                'stats': {
                    'offensivePlays': team_dict['off_plays'],
                    'offensivePPA': team_dict['off_ppa'],
                    'offensiveSuccessRate': team_dict['off_success_rate'],
                    'offensiveExplosiveness': team_dict['off_explosiveness'],
                    'defensivePlays': team_dict['def_plays'],
                    'defensivePPA': team_dict['def_ppa'],
                    'defensiveSuccessRate': team_dict['def_success_rate'],
                    'defensiveExplosiveness': team_dict['def_explosiveness']
                }
            })
        
        conn.close()
        return teams
    
    def get_all_offensive_stats(self, season=2025) -> Dict[str, Dict]:
        """Get offensive stats for all teams - formatted like fbs_offensive_stats.json"""
        conn = self._get_connection(attach_master=True)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.school as team, os.*
            FROM team_offensive_stats os
            JOIN master.teams t ON os.team_id = t.id
            WHERE os.season = ?
            ORDER BY t.school
        """, (season,))
        
        stats_dict = {}
        for row in cursor.fetchall():
            team_dict = dict(row)
            team_name = team_dict['team']
            stats_dict[team_name] = {
                'team': team_name,
                'season': team_dict['season'],
                'yardsPerPlay': team_dict['yards_per_play'],
                'yardsPerGame': team_dict['yards_per_game'],
                'pointsPerGame': team_dict['points_per_game']
            }
        
        conn.close()
        return {'offensive_stats': stats_dict}
    
    def get_all_defensive_stats(self, season=2025) -> Dict[str, Dict]:
        """Get defensive stats for all teams - formatted like fbs_defensive_stats.json"""
        conn = self._get_connection(attach_master=True)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.school as team, ds.*
            FROM team_defensive_stats ds
            JOIN master.teams t ON ds.team_id = t.id
            WHERE ds.season = ?
            ORDER BY t.school
        """, (season,))
        
        stats_dict = {}
        for row in cursor.fetchall():
            team_dict = dict(row)
            team_name = team_dict['team']
            stats_dict[team_name] = {
                'team': team_name,
                'season': team_dict['season'],
                'yardsPerPlay': team_dict['yards_per_play_allowed'],
                'yardsPerGame': team_dict['yards_per_game_allowed'],
                'pointsPerGame': team_dict['points_per_game_allowed']
            }
        
        conn.close()
        return {'defensive_stats': stats_dict}
    
    def get_all_season_summaries(self, season=2025) -> List[Dict]:
        """Get season summaries for all teams"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT team_name as team, season, wins, losses, win_pct as winPercent
            FROM team_season_summaries
            WHERE season = ?
            ORDER BY team_name
        """, (season,))
        
        summaries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return summaries
    
    def get_drive_efficiency(self, season=2025) -> Dict[str, Dict]:
        """Get drive efficiency for all teams - formatted like react_power5_efficiency.json"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT team_name, offensive_drives, defensive_drives,
                   offensive_scoring, defensive_scoring_allowed,
                   offensive_scoring_pct, defensive_stop_pct,
                   avg_yards_per_drive, avg_points_per_drive
            FROM team_drive_efficiency
            WHERE season = ?
            ORDER BY team_name
        """, (season,))
        
        efficiency_dict = {}
        for row in cursor.fetchall():
            team_dict = dict(row)
            team_name = team_dict['team_name']
            efficiency_dict[team_name] = {
                'team': team_name,
                'offensive_drives': team_dict['offensive_drives'],
                'defensive_drives': team_dict['defensive_drives'],
                'offensive_scoring': team_dict['offensive_scoring'],
                'defensive_scoring_allowed': team_dict['defensive_scoring_allowed'],
                'offensive_scoring_pct': team_dict['offensive_scoring_pct'],
                'defensive_stop_pct': team_dict['defensive_stop_pct'],
                'avg_yards_per_drive': team_dict['avg_yards_per_drive'],
                'avg_points_per_drive': team_dict['avg_points_per_drive']
            }
        
        conn.close()
        return efficiency_dict
    
    def get_ap_polls(self, season=2025) -> Dict[str, Dict]:
        """Get AP poll rankings by week - formatted like ap.json"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT week, rank, school, conference, first_place_votes, points
            FROM ap_poll_rankings
            WHERE season = ?
            ORDER BY week, rank
        """, (season,))
        
        polls_dict = {}
        for row in cursor.fetchall():
            row_dict = dict(row)
            week = row_dict['week']
            week_key = f"week_{week}"
            
            if week_key not in polls_dict:
                polls_dict[week_key] = {
                    'poll': 'AP Top 25',
                    'season': season,
                    'seasonType': 'regular',
                    'week': week,
                    'ranks': []
                }
            
            polls_dict[week_key]['ranks'].append({
                'rank': row_dict['rank'],
                'school': row_dict['school'],
                'conference': row_dict['conference'],
                'firstPlaceVotes': row_dict['first_place_votes'],
                'points': row_dict['points']
            })
        
        conn.close()
        return polls_dict
    
    def get_coaches_rankings_from_db(self) -> List[Dict]:
        """Get all coaches rankings from predictions.db"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT coach_id, coach_name, current_team, conference,
                   career_wins, career_losses, season_2025_wins, season_2025_losses,
                   overall_rank, data_json
            FROM coaches_rankings_data
            ORDER BY overall_rank ASC
        """)
        
        coaches = []
        for row in cursor.fetchall():
            try:
                coach_data = json.loads(row['data_json']) if row['data_json'] else {}
                coaches.append(coach_data)
            except:
                coaches.append({
                    'id': row['coach_id'],
                    'name': row['coach_name'],
                    'currentTeam': {'school': row['current_team'], 'conference': row['conference']},
                    'careerRecord': {'wins': row['career_wins'], 'losses': row['career_losses']},
                    'current2025Season': {'wins': row['season_2025_wins'], 'losses': row['season_2025_losses']},
                    'rankings': {'overallRank': row['overall_rank']}
                })
        
        conn.close()
        return coaches
    
    def get_fbs_ratings_from_db(self) -> List[Dict]:
        """Get FBS comprehensive ratings from predictions.db"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT team_id, team_name, conference, rating, rank, data_json
            FROM fbs_ratings_comprehensive
            ORDER BY rank ASC
        """)
        
        teams = []
        for row in cursor.fetchall():
            try:
                team_data = json.loads(row['data_json']) if row['data_json'] else {}
                teams.append(team_data)
            except:
                teams.append({
                    'id': row['team_id'],
                    'name': row['team_name'],
                    'team_name': row['team_name'],
                    'conference': row['conference'],
                    'rating': row['rating'],
                    'rank': row['rank']
                })
        
        conn.close()
        return teams
    
    def get_player_metrics_from_db(self) -> List[Dict]:
        """Get all player metrics from predictions.db"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT position, player_name, team, metric_type, metric_value, data_json
            FROM player_metrics_data
            ORDER BY position, metric_value DESC
        """)
        
        players = []
        for row in cursor.fetchall():
            try:
                player_data = json.loads(row['data_json']) if row['data_json'] else {}
                players.append(player_data)
            except:
                players.append({
                    'position': row['position'],
                    'name': row['player_name'],
                    'player_name': row['player_name'],
                    'team': row['team'],
                    'metric_type': row['metric_type'],
                    'metric_value': row['metric_value']
                })
        
        conn.close()
        return players
    
    def get_historical_win_probabilities(self, season=None) -> List[Dict]:
        """Get historical game results - formatted like complete_win_probabilities.json"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if season:
            cursor.execute("""
                SELECT game_id as gameId, season, week, season_type as seasonType,
                       home_team as homeTeam, away_team as awayTeam,
                       home_score as homeScore, away_score as awayScore,
                       home_postgame_wp as homePostgameWP, away_postgame_wp as awayPostgameWP,
                       home_pregame_wp as homePregameWP, away_pregame_wp as awayPregameWP
                FROM historical_game_results
                WHERE season = ?
                ORDER BY week, game_id
            """, (season,))
        else:
            cursor.execute("""
                SELECT game_id as gameId, season, week, season_type as seasonType,
                       home_team as homeTeam, away_team as awayTeam,
                       home_score as homeScore, away_score as awayScore,
                       home_postgame_wp as homePostgameWP, away_postgame_wp as awayPostgameWP,
                       home_pregame_wp as homePregameWP, away_pregame_wp as awayPregameWP
                FROM historical_game_results
                ORDER BY season DESC, week, game_id
            """)
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
