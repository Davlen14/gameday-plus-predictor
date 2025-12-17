"""
ESPN Game Service - Fetches play-by-play, boxscore, and game data from ESPN API
"""
import requests
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class ESPNGameService:
    """Service for fetching and caching ESPN game data"""
    
    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football"
    
    def __init__(self, db_path: str = "instance/predictions.db", coaches_db_path: str = "instance/coaches_master.db"):
        self.db_path = db_path
        self.coaches_db_path = coaches_db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables for caching game data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create games cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS espn_game_cache (
                game_id TEXT PRIMARY KEY,
                data JSON,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                game_status TEXT,
                home_team TEXT,
                away_team TEXT,
                home_score INTEGER,
                away_score INTEGER
            )
        """)
        
        # Create plays cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS espn_plays_cache (
                game_id TEXT PRIMARY KEY,
                plays_data JSON,
                drives_data JSON,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES espn_game_cache(game_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _get_team_wordmark(self, team_name: str) -> Optional[str]:
        """Get team wordmark from coaches_master database"""
        try:
            conn = sqlite3.connect(self.coaches_db_path)
            cursor = conn.cursor()
            
            # Try exact match first
            cursor.execute("SELECT wordmark_url FROM teams WHERE school = ?", (team_name,))
            result = cursor.fetchone()
            
            if not result:
                # Extract first part of team name for partial match
                # e.g., "Washington Huskies" -> "Washington", "Boise State Broncos" -> "Boise State"
                team_parts = team_name.split()
                
                # Try matching with first word
                cursor.execute("SELECT wordmark_url FROM teams WHERE school LIKE ? AND wordmark_url IS NOT NULL LIMIT 1", 
                             (f"{team_parts[0]}%",))
                result = cursor.fetchone()
                
                # If still no match and we have 2+ words, try first two words
                if not result and len(team_parts) >= 2:
                    cursor.execute("SELECT wordmark_url FROM teams WHERE school LIKE ? AND wordmark_url IS NOT NULL LIMIT 1", 
                                 (f"{team_parts[0]} {team_parts[1]}%",))
                    result = cursor.fetchone()
            
            conn.close()
            
            if result and result[0]:
                print(f"✓ Wordmark found for {team_name}: {result[0][:80]}...")
                return result[0]
            else:
                print(f"✗ No wordmark found for {team_name}")
            
            return None
        except Exception as e:
            print(f"Error fetching wordmark for {team_name}: {e}")
            return None
    
    def get_game_summary(self, game_id: str, force_refresh: bool = False) -> Optional[Dict]:
        """Get game summary from ESPN API"""
        # Check cache first
        if not force_refresh:
            cached = self._get_cached_game(game_id)
            if cached:
                return cached
        
        url = f"{self.BASE_URL}/summary?event={game_id}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Cache the data
            self._cache_game(game_id, data)
            
            return data
        except Exception as e:
            print(f"Error fetching game {game_id}: {e}")
            # Return cached data if available
            return self._get_cached_game(game_id)
    
    def get_playbyplay(self, game_id: str, force_refresh: bool = False) -> Optional[Dict]:
        """Get play-by-play data from ESPN API"""
        # For completed games, try cache first
        if not force_refresh:
            cached = self._get_cached_plays(game_id)
            if cached:
                return cached
        
        # Fetch from ESPN summary endpoint (includes plays)
        data = self.get_game_summary(game_id, force_refresh)
        
        if data:
            plays_data = {
                'drives': data.get('drives', {}),
                'plays': data.get('plays', []),
                'scoringPlays': data.get('scoringPlays', []),
                'boxscore': data.get('boxscore', {}),
                'header': data.get('header', {}),
                'gameInfo': data.get('gameInfo', {}),
                'leaders': data.get('leaders', []),
                'winprobability': data.get('winprobability', [])
            }
            
            # Cache plays data
            self._cache_plays(game_id, plays_data)
            
            return plays_data
        
        return None
    
    def get_game_for_field(self, game_id: str, force_refresh: bool = False) -> Optional[Dict]:
        """Get all data needed for the game field visualization"""
        data = self.get_game_summary(game_id, force_refresh=force_refresh)
        
        if not data:
            return None
        
        # Extract key info
        header = data.get('header', {})
        competitions = header.get('competitions', [{}])[0]
        competitors = competitions.get('competitors', [])
        
        # Get team info
        home_team = None
        away_team = None
        
        for comp in competitors:
            team_data = comp.get('team', {})
            team_name = team_data.get('displayName', team_data.get('name', ''))
            team_info = {
                'id': team_data.get('id'),
                'name': team_name,
                'abbreviation': team_data.get('abbreviation', ''),
                'logo': team_data.get('logo', team_data.get('logos', [{}])[0].get('href', '') if team_data.get('logos') else ''),
                'wordmark': self._get_team_wordmark(team_name),
                'color': f"#{team_data.get('color', '333333')}",
                'alternateColor': f"#{team_data.get('alternateColor', '666666')}",
                'score': int(comp.get('score', 0)),
                'record': comp.get('record', [{}])[0].get('summary', '') if comp.get('record') else '',
                'rank': comp.get('curatedRank', {}).get('current', None)
            }
            
            if comp.get('homeAway') == 'home':
                home_team = team_info
            else:
                away_team = team_info
        
        # Get drives and plays
        drives = data.get('drives', {})
        previous_drives = drives.get('previous', [])
        current_drive = drives.get('current', {})
        
        # Process drives for field visualization
        processed_drives = []
        for drive in previous_drives:
            drive_info = self._process_drive(drive, home_team, away_team)
            processed_drives.append(drive_info)
        
        # Get game status
        status = competitions.get('status', {})
        status_type = status.get('type', {})
        
        # Get venue info
        game_info = data.get('gameInfo', {})
        venue = game_info.get('venue', {})
        
        # Get boxscore for player stats
        boxscore = data.get('boxscore', {})
        
        # Build response
        result = {
            'gameId': game_id,
            'status': {
                'state': status_type.get('state', 'post'),
                'detail': status_type.get('detail', 'Final'),
                'description': status_type.get('description', ''),
                'period': status.get('period', 4),
                'clock': status.get('displayClock', '0:00')
            },
            'home': home_team,
            'away': away_team,
            'venue': {
                'name': venue.get('fullName', ''),
                'city': venue.get('address', {}).get('city', ''),
                'state': venue.get('address', {}).get('state', '')
            },
            'drives': processed_drives,
            'currentDrive': self._process_drive(current_drive, home_team, away_team) if current_drive else None,
            'boxscore': self._process_boxscore(boxscore),
            'notes': competitions.get('notes', []),
            'broadcasts': competitions.get('broadcasts', []),
            'attendance': competitions.get('attendance', 0)
        }
        
        return result
    
    def _process_drive(self, drive: Dict, home_team: Dict, away_team: Dict) -> Dict:
        """Process a drive for field visualization"""
        if not drive:
            return {}
        
        team = drive.get('team', {})
        team_id = team.get('id')
        
        # Determine if this is home or away team
        is_home = str(team_id) == str(home_team.get('id')) if home_team else False
        team_info = home_team if is_home else away_team
        
        plays = drive.get('plays', [])
        processed_plays = []
        
        for play in plays:
            processed_play = self._process_play(play, team_info, is_home)
            processed_plays.append(processed_play)
        
        return {
            'id': drive.get('id'),
            'description': drive.get('description', ''),
            'result': drive.get('displayResult', drive.get('result', '')),
            'team': {
                'id': team_id,
                'name': team.get('displayName', team.get('name', '')),
                'abbreviation': team.get('abbreviation', ''),
                'logo': team.get('logos', [{}])[0].get('href', '') if team.get('logos') else '',
                'isHome': is_home
            },
            'start': {
                'period': drive.get('start', {}).get('period', {}).get('number', 1),
                'clock': drive.get('start', {}).get('clock', {}).get('displayValue', ''),
                'yardLine': drive.get('start', {}).get('yardLine', 0),
                'text': drive.get('start', {}).get('text', '')
            },
            'end': {
                'period': drive.get('end', {}).get('period', {}).get('number', 1),
                'clock': drive.get('end', {}).get('clock', {}).get('displayValue', ''),
                'yardLine': drive.get('end', {}).get('yardLine', 0)
            },
            'plays': processed_plays,
            'yards': drive.get('yards', 0),
            'timeOfPossession': drive.get('timeOfPossession', {}).get('displayValue', ''),
            'isScoring': drive.get('isScoring', False)
        }
    
    def _process_play(self, play: Dict, team_info: Dict, is_home: bool) -> Dict:
        """Process a single play for field visualization"""
        play_type = play.get('type', {}).get('text', 'Play')
        
        # Get yard line positions for SVG
        start = play.get('start', {})
        end = play.get('end', {})
        
        start_yard = start.get('yardLine', 50)
        end_yard = end.get('yardLine', 50)
        
        # Convert to SVG coordinates (0-100 yards -> 10-110 SVG)
        # If team is going right to left, flip the coordinates
        if is_home:
            svg_start = 110 - start_yard
            svg_end = 110 - end_yard
        else:
            svg_start = 10 + start_yard
            svg_end = 10 + end_yard
        
        # Get athletes involved
        athletes = []
        for athlete in play.get('athletesInvolved', []):
            athletes.append({
                'id': athlete.get('id'),
                'name': athlete.get('displayName', athlete.get('shortName', '')),
                'jersey': athlete.get('jersey', ''),
                'headshot': athlete.get('headshot', {}).get('href', '') if isinstance(athlete.get('headshot'), dict) else athlete.get('headshot', ''),
                'position': athlete.get('position', {}).get('abbreviation', '') if isinstance(athlete.get('position'), dict) else ''
            })
        
        # Determine play color based on type
        play_colors = {
            'Touchdown': '#22c55e',
            'Field Goal': '#10b981',
            'Interception': '#a855f7',
            'Fumble': '#ef4444',
            'Sack': '#ef4444',
            'Pass': team_info.get('alternateColor', '#0033A0') if team_info else '#0033A0',
            'Rush': team_info.get('color', '#fa4616') if team_info else '#fa4616',
            'Punt': '#6b7280',
            'Kickoff': '#6b7280'
        }
        
        color = '#ffffff'
        for key, val in play_colors.items():
            if key.lower() in play_type.lower():
                color = val
                break
        
        return {
            'id': play.get('id'),
            'type': play_type,
            'text': play.get('text', ''),
            'shortText': play.get('shortText', ''),
            'clock': play.get('clock', {}).get('displayValue', ''),
            'period': play.get('period', {}).get('number', 1),
            'down': start.get('down', 1),
            'distance': start.get('distance', 10),
            'downDistanceText': start.get('shortDownDistanceText', start.get('downDistanceText', '')),
            'scoringPlay': play.get('scoringPlay', False),
            'awayScore': play.get('awayScore', 0),
            'homeScore': play.get('homeScore', 0),
            'athletes': athletes,
            'svgCoords': {
                'start': svg_start,
                'end': svg_end,
                'path': self._generate_play_path(svg_start, svg_end, play_type)
            },
            'color': color
        }
    
    def _generate_play_path(self, start: float, end: float, play_type: str) -> str:
        """Generate SVG path for play visualization"""
        mid_x = (start + end) / 2
        
        # Curve up for passes, down for rushes
        if 'pass' in play_type.lower():
            mid_y = 10  # Curve up
        elif 'punt' in play_type.lower() or 'kick' in play_type.lower():
            mid_y = 5   # High arc
        else:
            mid_y = 35  # Curve down
        
        return f"M {start} 26.65 Q {mid_x} {mid_y} {end} 26.65"
    
    def _process_boxscore(self, boxscore: Dict) -> Dict:
        """Process boxscore data for player stats"""
        result = {
            'teams': [],
            'players': boxscore.get('players', [])  # ✅ PRESERVE RAW PLAYERS DATA WITH HEADSHOTS
        }
        
        for team_data in boxscore.get('players', []):
            team = team_data.get('team', {})
            stats = team_data.get('statistics', [])
            
            team_stats = {
                'team': {
                    'id': team.get('id'),
                    'name': team.get('displayName', ''),
                    'abbreviation': team.get('abbreviation', ''),
                    'logo': team.get('logo', '')
                },
                'passing': [],
                'rushing': [],
                'receiving': [],
                'defense': []
            }
            
            for stat_cat in stats:
                cat_name = stat_cat.get('name', '').lower()
                athletes = stat_cat.get('athletes', [])
                
                for athlete_data in athletes:
                    athlete = athlete_data.get('athlete', {})
                    stat_values = athlete_data.get('stats', [])
                    
                    player_info = {
                        'id': athlete.get('id'),
                        'name': athlete.get('displayName', ''),
                        'jersey': athlete.get('jersey', ''),
                        'headshot': athlete.get('headshot', {}).get('href', '') if isinstance(athlete.get('headshot'), dict) else '',
                        'position': athlete.get('position', {}).get('abbreviation', '') if isinstance(athlete.get('position'), dict) else '',
                        'stats': stat_values
                    }
                    
                    if cat_name == 'passing':
                        team_stats['passing'].append(player_info)
                    elif cat_name == 'rushing':
                        team_stats['rushing'].append(player_info)
                    elif cat_name == 'receiving':
                        team_stats['receiving'].append(player_info)
                    elif cat_name in ['defensive', 'defense']:
                        team_stats['defense'].append(player_info)
            
            result['teams'].append(team_stats)
        
        return result
    
    def _get_cached_game(self, game_id: str) -> Optional[Dict]:
        """Get cached game data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM espn_game_cache WHERE game_id = ?", (game_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
        except Exception as e:
            print(f"Cache read error: {e}")
        
        return None
    
    def _cache_game(self, game_id: str, data: Dict):
        """Cache game data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get team info
            header = data.get('header', {})
            competitions = header.get('competitions', [{}])[0]
            competitors = competitions.get('competitors', [])
            
            home_team = ''
            away_team = ''
            home_score = 0
            away_score = 0
            
            for comp in competitors:
                if comp.get('homeAway') == 'home':
                    home_team = comp.get('team', {}).get('abbreviation', '')
                    home_score = int(comp.get('score', 0))
                else:
                    away_team = comp.get('team', {}).get('abbreviation', '')
                    away_score = int(comp.get('score', 0))
            
            status = competitions.get('status', {}).get('type', {}).get('state', 'post')
            
            cursor.execute("""
                INSERT OR REPLACE INTO espn_game_cache 
                (game_id, data, game_status, home_team, away_team, home_score, away_score, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (game_id, json.dumps(data), status, home_team, away_team, home_score, away_score, datetime.now()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def _get_cached_plays(self, game_id: str) -> Optional[Dict]:
        """Get cached plays data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT plays_data, drives_data FROM espn_plays_cache WHERE game_id = ?", (game_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'plays': json.loads(row[0]) if row[0] else [],
                    'drives': json.loads(row[1]) if row[1] else {}
                }
        except Exception as e:
            print(f"Plays cache read error: {e}")
        
        return None
    
    def _cache_plays(self, game_id: str, data: Dict):
        """Cache plays data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO espn_plays_cache 
                (game_id, plays_data, drives_data, fetched_at)
                VALUES (?, ?, ?, ?)
            """, (
                game_id, 
                json.dumps(data.get('plays', [])),
                json.dumps(data.get('drives', {})),
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Plays cache write error: {e}")


# Convenience function
def get_espn_game(game_id: str, force_refresh: bool = False) -> Optional[Dict]:
    """Convenience function to get ESPN game data"""
    service = ESPNGameService()
    return service.get_game_for_field(game_id)
