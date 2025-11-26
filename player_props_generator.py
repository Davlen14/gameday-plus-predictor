#!/usr/bin/env python3
"""
Player Props Generator for College Football
Focused implementation for Ohio State vs Michigan - Week 14, 2025
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import statistics
import math

@dataclass
class PlayerProp:
    """Represents a generated player prop bet"""
    player_name: str
    player_team: str
    position: str
    prop_type: str  # 'passing_yards', 'rushing_yards', 'receiving_yards', 'passing_tds', etc.
    over_under_line: float
    confidence: float  # 0-100
    recommendation: str  # 'over', 'under', 'avoid'
    reasoning: str
    season_average: float
    recent_form: float  # Last 3 games average
    opponent_defense_rank: str
    weather_impact: str

@dataclass
class GameContext:
    """Game context for prop generation"""
    home_team: str
    away_team: str
    spread: float
    total: float
    weather: Dict
    is_rivalry: bool = False
    is_conference_game: bool = False

class PlayerPropsEngine:
    """
    Player Props Generator using CFBD-style data analysis
    """
    
    def __init__(self):
        self.fbs_players = self._load_fbs_players_database()
        self.game_context = None
        
    def _load_fbs_players_database(self) -> Dict:
        """Load real 2025 usage data for Ohio State and Michigan"""
        return {
            'Ohio State': {
                'quarterback': {'name': 'Julian Sayin', 'usage': 45.9, 'season_averages': {'passing_yards_per_game': 285.0, 'passing_tds_per_game': 2.3, 'rushing_yards_per_game': 18.0}},
                'wide_receivers': [
                    {'name': 'Jeremiah Smith', 'usage': 13.4, 'season_averages': {'receiving_yards_per_game': 95.0, 'receptions_per_game': 6.2}},
                    {'name': 'Carnell Tate', 'usage': 9.7, 'season_averages': {'receiving_yards_per_game': 78.0, 'receptions_per_game': 5.8}}
                ],
                'running_backs': [
                    {'name': 'Bo Jackson', 'usage': 21.5, 'season_averages': {'rushing_yards_per_game': 85.0, 'rushing_attempts_per_game': 18.5}},
                    {'name': 'James Peoples', 'usage': 9.8, 'season_averages': {'rushing_yards_per_game': 45.0, 'rushing_attempts_per_game': 10.2}}
                ]
            },
            'Michigan': {
                'quarterback': {'name': 'Bryce Underwood', 'usage': 48.2, 'season_averages': {'passing_yards_per_game': 225.0, 'passing_tds_per_game': 1.8, 'rushing_yards_per_game': 34.0}},
                'wide_receivers': [
                    {'name': 'Andrew Marsh', 'usage': 8.9, 'season_averages': {'receiving_yards_per_game': 72.0, 'receptions_per_game': 5.1}},
                    {'name': 'Donaven McCulley', 'usage': 8.0, 'season_averages': {'receiving_yards_per_game': 68.0, 'receptions_per_game': 4.8}}
                ],
                'running_backs': [
                    {'name': 'Justice Haynes', 'usage': 28.4, 'season_averages': {'rushing_yards_per_game': 95.0, 'rushing_attempts_per_game': 20.1}},
                    {'name': 'Jordan Marshall', 'usage': 22.8, 'season_averages': {'rushing_yards_per_game': 78.0, 'rushing_attempts_per_game': 16.5}}
                ]
            }
        }
    
    def set_game_context(self, home_team: str, away_team: str, game_data: Dict):
        """Set the game context for prop generation"""
        betting_lines = game_data.get('bettingLines', {})
        consensus = betting_lines.get('consensus', {})
        
        self.game_context = GameContext(
            home_team=home_team,
            away_team=away_team,
            spread=abs(consensus.get('spread', 0)),
            total=consensus.get('total', 50),
            weather=game_data.get('weather', {}),
            is_rivalry=self._is_rivalry_game(home_team, away_team),
            is_conference_game=game_data.get('gameInfo', {}).get('conferenceGame', False)
        )
    
    def _is_rivalry_game(self, home_team: str, away_team: str) -> bool:
        """Check if this is a known rivalry game"""
        rivalry_pairs = [
            ('Ohio State', 'Michigan'),
            ('Alabama', 'Auburn'),
            ('Georgia', 'Georgia Tech'),
            ('Florida', 'Florida State'),
            ('Texas', 'Oklahoma')
        ]
        
        teams = {home_team.lower(), away_team.lower()}
        for team1, team2 in rivalry_pairs:
            if {team1.lower(), team2.lower()}.issubset(teams):
                return True
        return False
    
    def _get_team_players(self, team_name: str) -> Dict[str, Any]:
        """Get all players for a specific team from usage database"""
        # Direct lookup for Ohio State and Michigan
        if team_name in self.fbs_players:
            return self.fbs_players[team_name]
        
        # Try fuzzy matching
        for fbs_team, team_data in self.fbs_players.items():
            if team_name.lower() in fbs_team.lower() or fbs_team.lower() in team_name.lower():
                return team_data
        
        # Return empty structure if no match found
        return {
            'quarterback': None,
            'wide_receivers': [],
            'running_backs': []
        }
    
    def _clean_team_name(self, team_name: str) -> str:
        """Clean team name for database lookup"""
        if not team_name:
            return ""
        
        # Handle common variations
        team_mappings = {
            'USC': 'Southern California',
            'UCF': 'Central Florida',
            'UConn': 'Connecticut',
            'UMass': 'Massachusetts'
        }
        
        return team_mappings.get(team_name, team_name)
    
    def _matches_team(self, player_team: str, target_team: str) -> bool:
        """Check if player team matches target team"""
        if not player_team or not target_team:
            return False
        
        # Clean team names for comparison
        player_clean = player_team.lower().replace('(', '').replace(')', '').strip()
        target_clean = target_team.lower().strip()
        
        # Direct match
        if target_clean in player_clean or player_clean in target_clean:
            return True
        
        # Handle common variations
        team_variations = {
            'ohio state': ['buckeyes', 'osu'],
            'michigan': ['wolverines', 'um'],
            'alabama': ['crimson tide', 'bama'],
            'georgia': ['bulldogs', 'uga']
        }
        
        for canonical, variations in team_variations.items():
            if canonical in target_clean:
                return any(var in player_clean for var in variations + [canonical])
        
        return False
    
    def generate_qb_props(self, team_name: str) -> List[PlayerProp]:
        """Generate quarterback props for a team - only the primary QB"""
        props = []
        team_players = self._get_team_players(team_name)
        
        # Get the primary QB from the database
        qb = team_players.get('quarterback')
        if not qb:
            return props
            
        # Get season averages (our main data source now)
        season_averages = qb.get('season_averages', {})
        
        # Skip if not enough data (basic validation)
        if season_averages.get('passing_yards_per_game', 0) < 50:
            return props
            
        # Generate passing yards prop
        season_avg = season_averages.get('passing_yards_per_game', 0)
        
        props.append(PlayerProp(
            player_name=qb['name'],
            player_team=team_name,
            position='QB',
            prop_type='passing_yards',
            over_under_line=self._calculate_prop_line(season_avg, 'passing_yards'),
            confidence=self._calculate_confidence(qb, 'passing_yards'),
            recommendation=self._generate_recommendation(qb, 'passing_yards', season_avg),
            reasoning=self._generate_reasoning(qb, 'passing_yards', season_avg),
            season_average=season_avg,
            recent_form=season_avg * 0.95,  # Placeholder for recent form
            opponent_defense_rank="TBD",
            weather_impact=self._assess_weather_impact('passing')
        ))
        
        # Generate passing TDs prop
        season_td_avg = season_averages.get('passing_tds_per_game', 0)
        props.append(PlayerProp(
            player_name=qb['name'],
            player_team=team_name,
            position='QB',
            prop_type='passing_tds',
            over_under_line=self._calculate_prop_line(season_td_avg, 'passing_tds'),
            confidence=self._calculate_confidence(qb, 'passing_tds'),
            recommendation=self._generate_recommendation(qb, 'passing_tds', season_td_avg),
            reasoning=self._generate_reasoning(qb, 'passing_tds', season_td_avg),
            season_average=season_td_avg,
            recent_form=season_td_avg,
            opponent_defense_rank="TBD",
            weather_impact=self._assess_weather_impact('passing')
        ))
        
        # Add rushing yards prop for QB
        rushing_avg = season_averages.get('rushing_yards_per_game', 0)
        if rushing_avg > 10:  # Only if QB has meaningful rushing yards
            props.append(PlayerProp(
                player_name=qb['name'],
                player_team=team_name,
                position='QB',
                prop_type='rushing_yards',
                over_under_line=self._calculate_prop_line(rushing_avg, 'rushing_yards'),
                confidence=self._calculate_confidence(qb, 'rushing_yards'),
                recommendation=self._generate_recommendation(qb, 'rushing_yards', rushing_avg),
                reasoning=self._generate_reasoning(qb, 'rushing_yards', rushing_avg),
                season_average=rushing_avg,
                recent_form=rushing_avg,
                opponent_defense_rank="TBD",
                weather_impact=self._assess_weather_impact('rushing')
            ))
        
        return props
    
    def generate_wr_props(self, team_name: str) -> List[PlayerProp]:
        """Generate wide receiver props for a team"""
        props = []
        team_players = self._get_team_players(team_name)
        
        # Get WRs from database (already sorted by performance)
        wrs = team_players.get('wide_receivers', [])
        
        # Generate props for top 2 WRs
        for wr in wrs[:2]:
            season_averages = wr.get('season_averages', {})
            
            if season_averages.get('receptions_per_game', 0) < 2:  # Skip players with minimal involvement
                continue
            
            # Receiving yards prop
            season_avg = season_averages.get('receiving_yards_per_game', 0)
            props.append(PlayerProp(
                player_name=wr['name'],
                player_team=team_name,
                position='WR',
                prop_type='receiving_yards',
                over_under_line=self._calculate_prop_line(season_avg, 'receiving_yards'),
                confidence=self._calculate_confidence(wr, 'receiving_yards'),
                recommendation=self._generate_recommendation(wr, 'receiving_yards', season_avg),
                reasoning=self._generate_reasoning(wr, 'receiving_yards', season_avg),
                season_average=season_avg,
                recent_form=season_avg,
                opponent_defense_rank="TBD",
                weather_impact=self._assess_weather_impact('receiving')
            ))
            
            # Receptions prop
            receptions_avg = season_averages.get('receptions_per_game', 0)
            props.append(PlayerProp(
                player_name=wr['name'],
                player_team=team_name,
                position='WR',
                prop_type='receptions',
                over_under_line=self._calculate_prop_line(receptions_avg, 'receptions'),
                confidence=self._calculate_confidence(wr, 'receptions'),
                recommendation=self._generate_recommendation(wr, 'receptions', receptions_avg),
                reasoning=self._generate_reasoning(wr, 'receptions', receptions_avg),
                season_average=receptions_avg,
                recent_form=receptions_avg,
                opponent_defense_rank="TBD",
                weather_impact=self._assess_weather_impact('receiving')
            ))
        
        return props
    
    def generate_rb_props(self, team_name: str) -> List[PlayerProp]:
        """Generate running back props for a team"""
        props = []
        team_players = self._get_team_players(team_name)
        
        # Get RBs from database (already sorted by performance)
        rbs = team_players.get('running_backs', [])
        
        # Generate props for top 2 RBs
        for rb in rbs[:2]:
            season_averages = rb.get('season_averages', {})
            
            if season_averages.get('rushing_yards_per_game', 0) < 20:  # Skip players with minimal involvement
                continue
            
            # Rushing yards prop
            season_avg = season_averages.get('rushing_yards_per_game', 0)
            props.append(PlayerProp(
                player_name=rb['name'],
                player_team=team_name,
                position='RB',
                prop_type='rushing_yards',
                over_under_line=self._calculate_prop_line(season_avg, 'rushing_yards'),
                confidence=self._calculate_confidence(rb, 'rushing_yards'),
                recommendation=self._generate_recommendation(rb, 'rushing_yards', season_avg),
                reasoning=self._generate_reasoning(rb, 'rushing_yards', season_avg),
                season_average=season_avg,
                recent_form=season_avg,
                opponent_defense_rank="TBD",
                weather_impact=self._assess_weather_impact('rushing')
            ))
            
            # Rushing attempts prop
            attempts_avg = season_averages.get('rushing_attempts_per_game', 0)
            if attempts_avg > 5:  # Only if meaningful carries
                props.append(PlayerProp(
                    player_name=rb['name'],
                    player_team=team_name,
                    position='RB',
                    prop_type='rushing_attempts',
                    over_under_line=self._calculate_prop_line(attempts_avg, 'rushing_attempts'),
                    confidence=self._calculate_confidence(rb, 'rushing_attempts'),
                    recommendation=self._generate_recommendation(rb, 'rushing_attempts', attempts_avg),
                    reasoning=self._generate_reasoning(rb, 'rushing_attempts', attempts_avg),
                    season_average=attempts_avg,
                    recent_form=attempts_avg,
                    opponent_defense_rank="TBD",
                    weather_impact=self._assess_weather_impact('rushing')
                ))
        
        return props
    
    def _calculate_prop_line(self, season_avg: float, prop_type: str) -> float:
        """Calculate the over/under line for a prop"""
        if prop_type in ['passing_yards', 'rushing_yards', 'receiving_yards']:
            # Round to nearest 5 for yards
            return round(season_avg / 5) * 5
        elif prop_type in ['passing_tds', 'rushing_tds', 'receiving_tds']:
            # Round to nearest 0.5 for TDs
            return round(season_avg * 2) / 2
        elif prop_type in ['receptions', 'rushing_attempts']:
            # Round to nearest 0.5 for receptions and attempts
            return round(season_avg * 2) / 2
        else:
            return round(season_avg, 1)
    
    def _calculate_confidence(self, player_data: Dict, prop_type: str) -> float:
        """Calculate confidence level for a prop"""
        base_confidence = 65
        
        # Boost confidence for high-usage players
        if prop_type in ['passing_yards', 'passing_tds']:
            attempts = player_data.get('passing_stats', {}).get('attempts', 0)
            if attempts > 300:
                base_confidence += 15
        elif prop_type in ['receiving_yards', 'receptions']:
            receptions = player_data.get('receptions', 0)
            if receptions > 50:
                base_confidence += 15
        elif prop_type in ['rushing_yards', 'rushing_attempts']:
            rushing_yards = player_data.get('rushing_yards', 0)
            if rushing_yards > 500:
                base_confidence += 15
        
        # Weather adjustment
        if self.game_context and self.game_context.weather:
            temp = self.game_context.weather.get('temperature', 70)
            wind = self.game_context.weather.get('windSpeed', 0)
            
            if temp < 32 or wind > 15:  # Cold or windy
                if prop_type in ['passing_yards', 'receiving_yards']:
                    base_confidence -= 10
        
        # Rivalry game adjustment (increased volatility)
        if self.game_context and self.game_context.is_rivalry:
            base_confidence -= 5
        
        return min(95, max(25, base_confidence))
    
    def _generate_recommendation(self, player_data: Dict, prop_type: str, season_avg: float) -> str:
        """Generate betting recommendation"""
        if not self.game_context:
            return 'avoid'
        
        # Simple logic - would be enhanced with opponent defensive rankings
        if season_avg > 0:
            # In rivalry games, lean towards unders due to defensive intensity
            if self.game_context.is_rivalry:
                return 'under'
            
            # In cold weather, lean towards passing unders, rushing overs
            if self.game_context.weather.get('temperature', 70) < 35:
                if prop_type in ['passing_yards', 'receiving_yards', 'passing_tds', 'receptions']:
                    return 'under'
                elif prop_type in ['rushing_yards', 'rushing_attempts']:
                    return 'over'
            
            return 'over'
        
        return 'avoid'
    
    def _generate_reasoning(self, player_data: Dict, prop_type: str, season_avg: float) -> str:
        """Generate human-readable reasoning"""
        reasons = []
        
        if season_avg > 0:
            reasons.append(f"Season average: {season_avg:.1f}")
        
        if self.game_context:
            if self.game_context.is_rivalry:
                reasons.append("Rivalry game - expect defensive battle")
            
            temp = self.game_context.weather.get('temperature', 70)
            wind = self.game_context.weather.get('windSpeed', 0)
            
            if temp < 35:
                reasons.append(f"Cold weather ({temp}°F) - affects passing game")
            if wind > 15:
                reasons.append(f"Windy conditions ({wind} mph) - impacts accuracy")
        
        return "; ".join(reasons) if reasons else "Standard projection based on season performance"
    
    def _assess_weather_impact(self, play_type: str) -> str:
        """Assess weather impact on different play types"""
        if not self.game_context:
            return "No weather data"
        
        temp = self.game_context.weather.get('temperature', 70)
        wind = self.game_context.weather.get('windSpeed', 0)
        precipitation = self.game_context.weather.get('precipitation', 0)
        
        impacts = []
        
        if temp < 32:
            if play_type == 'passing':
                impacts.append("Cold reduces QB accuracy")
            elif play_type == 'receiving':
                impacts.append("Cold affects ball handling")
            else:
                impacts.append("Cold weather game")
        
        if wind > 15 and play_type in ['passing', 'receiving']:
            impacts.append("Wind impacts passing game")
        
        if precipitation > 0:
            impacts.append("Wet conditions favor ground game")
        
        return "; ".join(impacts) if impacts else "Minimal weather impact"
    
    def generate_all_props(self, home_team: str, away_team: str) -> Dict[str, List[PlayerProp]]:
        """Generate all props for both teams"""
        props = {
            'home_team': home_team,
            'away_team': away_team,
            'home_props': [],
            'away_props': []
        }
        
        # Generate props for home team
        props['home_props'].extend(self.generate_qb_props(home_team))
        props['home_props'].extend(self.generate_wr_props(home_team))
        props['home_props'].extend(self.generate_rb_props(home_team))
        
        # Generate props for away team
        props['away_props'].extend(self.generate_qb_props(away_team))
        props['away_props'].extend(self.generate_wr_props(away_team))
        props['away_props'].extend(self.generate_rb_props(away_team))
        
        return props

def main():
    """Generate props for Ohio State vs Michigan"""
    print("🏈 Player Props Generator - Ohio State @ Michigan")
    print("=" * 60)
    
    # Load Ohio State vs Michigan game data
    try:
        with open('Currentweekgames.json', 'r') as f:
            games_data = json.load(f)
    except Exception as e:
        print(f"Error loading games data: {e}")
        return
    
    # Find the Ohio State vs Michigan game
    target_game = None
    for game in games_data.get('games', {}).get('all', []):
        home_team = game.get('homeTeam', {}).get('name', '')
        away_team = game.get('awayTeam', {}).get('name', '')
        
        if ('Ohio State' in home_team or 'Ohio State' in away_team) and \
           ('Michigan' in home_team or 'Michigan' in away_team):
            if 'Michigan State' not in home_team and 'Michigan State' not in away_team:
                target_game = game
                break
    
    if not target_game:
        print("❌ Ohio State vs Michigan game not found")
        return
    
    home_team = target_game['homeTeam']['name']
    away_team = target_game['awayTeam']['name']
    
    print(f"🎯 Found Game: {away_team} @ {home_team}")
    print(f"📊 Spread: {target_game['bettingLines']['consensus']['spread']:.1f}")
    print(f"🎯 Total: {target_game['bettingLines']['consensus']['total']}")
    print(f"🌡️ Weather: {target_game['weather']['temperature']}°F, Wind: {target_game['weather']['windSpeed']} mph")
    print()
    
    # Initialize props engine
    engine = PlayerPropsEngine()
    engine.set_game_context(home_team, away_team, target_game)
    
    # Generate all props
    all_props = engine.generate_all_props(home_team, away_team)
    
    # Display results
    print(f"🔥 GENERATED PLAYER PROPS")
    print("=" * 60)
    
    # Away team props (Ohio State)
    print(f"\n🏈 {away_team} Props:")
    for prop in all_props['away_props']:
        print(f"  {prop.player_name} ({prop.position})")
        print(f"    {prop.prop_type.replace('_', ' ').title()}: O/U {prop.over_under_line}")
        print(f"    Recommendation: {prop.recommendation.upper()} (Confidence: {prop.confidence:.0f}%)")
        print(f"    Reasoning: {prop.reasoning}")
        print(f"    Weather Impact: {prop.weather_impact}")
        print()
    
    # Home team props (Michigan)
    print(f"\n🏈 {home_team} Props:")
    for prop in all_props['home_props']:
        print(f"  {prop.player_name} ({prop.position})")
        print(f"    {prop.prop_type.replace('_', ' ').title()}: O/U {prop.over_under_line}")
        print(f"    Recommendation: {prop.recommendation.upper()} (Confidence: {prop.confidence:.0f}%)")
        print(f"    Reasoning: {prop.reasoning}")
        print(f"    Weather Impact: {prop.weather_impact}")
        print()
    
    # Save props to JSON
    output_file = f"player_props_{away_team.replace(' ', '_')}_vs_{home_team.replace(' ', '_')}_week14.json"
    
    # Convert props to serializable format
    serializable_props = {
        'game_info': {
            'home_team': home_team,
            'away_team': away_team,
            'spread': target_game['bettingLines']['consensus']['spread'],
            'total': target_game['bettingLines']['consensus']['total'],
            'weather': target_game['weather']
        },
        'props': []
    }
    
    for prop in all_props['away_props'] + all_props['home_props']:
        serializable_props['props'].append({
            'player_name': prop.player_name,
            'player_team': prop.player_team,
            'position': prop.position,
            'prop_type': prop.prop_type,
            'over_under_line': prop.over_under_line,
            'confidence': prop.confidence,
            'recommendation': prop.recommendation,
            'reasoning': prop.reasoning,
            'season_average': prop.season_average,
            'weather_impact': prop.weather_impact
        })
    
    with open(output_file, 'w') as f:
        json.dump(serializable_props, f, indent=2)
    
    print(f"💾 Props saved to: {output_file}")
    print(f"📊 Total props generated: {len(serializable_props['props'])}")

if __name__ == "__main__":
    main()