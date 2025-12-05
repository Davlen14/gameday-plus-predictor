#!/usr/bin/env python3
"""
Enhanced FBS Power Rankings Generator
Combines ALL statistics + ratings (ELO, FPI, SP+, SRS)
"""

import json
import math
from typing import Dict, List, Tuple
from datetime import datetime

class EnhancedPowerRankings:
    def __init__(self, stats_file: str, ratings_file: str, schedule_file: str = None):
        """Initialize with stats, ratings, and optional schedule files"""
        # Load stats
        with open(stats_file, 'r') as f:
            data = json.load(f)
            self.teams_stats = data.get('teams', data) if isinstance(data, dict) else data
        
        # Load ratings
        with open(ratings_file, 'r') as f:
            ratings_data = json.load(f)
            self.teams_ratings = {team['team']: team for team in ratings_data['teams']}
        
        # Load schedule/SOS data if provided
        self.teams_schedules = {}
        if schedule_file:
            try:
                with open(schedule_file, 'r') as f:
                    schedule_data = json.load(f)
                    # Build dict using query_metadata.team as key
                    for team_entry in schedule_data.get('teams', []):
                        team_name = team_entry['query_metadata']['team']
                        self.teams_schedules[team_name] = team_entry
                    print(f"✅ Loaded schedule data for {len(self.teams_schedules)} teams")
            except FileNotFoundError:
                print(f"⚠️  Schedule file not found: {schedule_file}")
            except Exception as e:
                print(f"⚠️  Error loading schedule file: {e}")
        
        self.team_scores = {}
        
    def normalize_stat(self, values: List[float], reverse: bool = False) -> Dict[str, float]:
        """Normalize stat values to 0-100 scale"""
        if not values or len(values) == 0:
            return {}
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            return {i: 50.0 for i in range(len(values))}
        
        normalized = {}
        for i, val in enumerate(values):
            if reverse:
                normalized[i] = 100 * (max_val - val) / (max_val - min_val)
            else:
                normalized[i] = 100 * (val - min_val) / (max_val - min_val)
        
        return normalized
    
    def safe_division(self, numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers"""
        return numerator / denominator if denominator != 0 else default
    
    def calculate_offensive_metrics(self, team_data: Dict) -> Dict[str, float]:
        """Calculate all offensive derived metrics"""
        stats = team_data['stats']
        metrics = {}
        
        # Basic efficiency metrics
        metrics['yards_per_play'] = self.safe_division(stats.get('totalYards', 0), stats.get('offense_plays', 1))
        metrics['yards_per_game'] = self.safe_division(stats.get('totalYards', 0), stats.get('games', 1))
        metrics['points_per_game'] = stats.get('pointsPerGame', self.safe_division(stats.get('totalPoints', 0), stats.get('games', 1)))
        
        # Passing efficiency
        metrics['completion_pct'] = self.safe_division(stats.get('passCompletions', 0), stats.get('passAttempts', 1)) * 100
        metrics['yards_per_pass'] = self.safe_division(stats.get('netPassingYards', 0), stats.get('passAttempts', 1))
        metrics['pass_td_rate'] = self.safe_division(stats.get('passingTDs', 0), stats.get('passAttempts', 1)) * 100
        metrics['interception_pct'] = self.safe_division(stats.get('passesIntercepted', 0), stats.get('passAttempts', 1)) * 100
        
        # Rushing efficiency
        metrics['yards_per_rush'] = self.safe_division(stats.get('rushingYards', 0), stats.get('rushingAttempts', 1))
        metrics['rush_td_rate'] = self.safe_division(stats.get('rushingTDs', 0), stats.get('rushingAttempts', 1)) * 100
        
        # Down conversion efficiency
        metrics['third_down_pct'] = self.safe_division(stats.get('thirdDownConversions', 0), stats.get('thirdDowns', 1)) * 100
        metrics['fourth_down_pct'] = self.safe_division(stats.get('fourthDownConversions', 0), stats.get('fourthDowns', 1)) * 100
        
        # Advanced metrics
        metrics['first_downs_per_game'] = self.safe_division(stats.get('firstDowns', 0), stats.get('games', 1))
        metrics['points_per_opportunity'] = stats.get('offense_pointsPerOpportunity', 0)
        metrics['turnover_margin'] = stats.get('turnoversOpponent', 0) - stats.get('turnovers', 0)
        metrics['possession_time_pct'] = self.safe_division(stats.get('possessionTime', 0), 
                                                            stats.get('possessionTime', 0) + stats.get('possessionTimeOpponent', 1)) * 100
        
        # Line play metrics
        metrics['line_yards'] = stats.get('offense_lineYards', 0)
        metrics['second_level_yards'] = stats.get('offense_secondLevelYards', 0)
        metrics['open_field_yards'] = stats.get('offense_openFieldYards', 0)
        metrics['power_success'] = stats.get('offense_powerSuccess', 0) * 100
        metrics['stuff_rate'] = stats.get('offense_stuffRate', 0) * 100
        
        # Advanced offensive metrics
        metrics['offense_ppa'] = stats.get('offense_ppa', 0)
        metrics['offense_success_rate'] = stats.get('offense_successRate', 0) * 100
        metrics['offense_explosiveness'] = stats.get('offense_explosiveness', 0)
        
        # Standard vs passing downs
        std_downs = stats.get('offense_standardDowns', {})
        pass_downs = stats.get('offense_passingDowns', {})
        
        metrics['standard_downs_ppa'] = std_downs.get('ppa', 0)
        metrics['standard_downs_success'] = std_downs.get('successRate', 0) * 100
        metrics['passing_downs_ppa'] = pass_downs.get('ppa', 0)
        metrics['passing_downs_success'] = pass_downs.get('successRate', 0) * 100
        
        # Play type efficiency
        rush_plays = stats.get('offense_rushingPlays', {})
        pass_plays = stats.get('offense_passingPlays', {})
        
        metrics['rushing_ppa'] = rush_plays.get('ppa', 0)
        metrics['rushing_success'] = rush_plays.get('successRate', 0) * 100
        metrics['rushing_explosiveness'] = rush_plays.get('explosiveness', 0)
        
        metrics['passing_ppa'] = pass_plays.get('ppa', 0)
        metrics['passing_success'] = pass_plays.get('successRate', 0) * 100
        metrics['passing_explosiveness'] = pass_plays.get('explosiveness', 0)
        
        # Field position
        field_pos = stats.get('offense_fieldPosition', {})
        metrics['avg_starting_field_position'] = field_pos.get('averageStart', 0)
        metrics['avg_predicted_points_start'] = field_pos.get('averagePredictedPoints', 0)
        
        # Havoc metrics
        havoc = stats.get('offense_havoc', {})
        metrics['offense_havoc_total'] = havoc.get('total', 0) * 100
        metrics['offense_havoc_front_seven'] = havoc.get('frontSeven', 0) * 100
        metrics['offense_havoc_db'] = havoc.get('db', 0) * 100
        
        # Special teams
        metrics['kick_return_avg'] = self.safe_division(stats.get('kickReturnYards', 0), stats.get('kickReturns', 1))
        metrics['punt_return_avg'] = self.safe_division(stats.get('puntReturnYards', 0), stats.get('puntReturns', 1))
        metrics['penalty_yards_per_game'] = self.safe_division(stats.get('penaltyYards', 0), stats.get('games', 1))
        
        return metrics
    
    def calculate_defensive_metrics(self, team_data: Dict) -> Dict[str, float]:
        """Calculate all defensive derived metrics"""
        stats = team_data['stats']
        metrics = {}
        
        # Basic efficiency metrics
        metrics['yards_allowed_per_play'] = self.safe_division(stats.get('totalYardsOpponent', 0), stats.get('defense_plays', 1))
        metrics['yards_allowed_per_game'] = self.safe_division(stats.get('totalYardsOpponent', 0), stats.get('games', 1))
        
        # Passing defense
        metrics['completion_pct_allowed'] = self.safe_division(stats.get('passCompletionsOpponent', 0), stats.get('passAttemptsOpponent', 1)) * 100
        metrics['yards_per_pass_allowed'] = self.safe_division(stats.get('netPassingYardsOpponent', 0), stats.get('passAttemptsOpponent', 1))
        metrics['pass_td_allowed_rate'] = self.safe_division(stats.get('passingTDsOpponent', 0), stats.get('passAttemptsOpponent', 1)) * 100
        
        # Rushing defense
        metrics['yards_per_rush_allowed'] = self.safe_division(stats.get('rushingYardsOpponent', 0), stats.get('rushingAttemptsOpponent', 1))
        metrics['rush_td_allowed_rate'] = self.safe_division(stats.get('rushingTDsOpponent', 0), stats.get('rushingAttemptsOpponent', 1)) * 100
        
        # Down conversion defense
        metrics['third_down_pct_allowed'] = self.safe_division(stats.get('thirdDownConversionsOpponent', 0), stats.get('thirdDownsOpponent', 1)) * 100
        metrics['fourth_down_pct_allowed'] = self.safe_division(stats.get('fourthDownConversionsOpponent', 0), stats.get('fourthDownsOpponent', 1)) * 100
        
        # Takeaways
        metrics['interceptions_per_game'] = self.safe_division(stats.get('interceptions', 0), stats.get('games', 1))
        metrics['fumbles_recovered_per_game'] = self.safe_division(stats.get('fumblesRecovered', 0), stats.get('games', 1))
        metrics['takeaways_per_game'] = self.safe_division(stats.get('turnoversOpponent', 0), stats.get('games', 1))
        
        # Pressure metrics
        metrics['sacks_per_game'] = self.safe_division(stats.get('sacks', 0), stats.get('games', 1))
        metrics['tackles_for_loss_per_game'] = self.safe_division(stats.get('tacklesForLoss', 0), stats.get('games', 1))
        metrics['sack_rate'] = self.safe_division(stats.get('sacks', 0), stats.get('passAttemptsOpponent', 1)) * 100
        
        # Line play metrics
        metrics['def_line_yards'] = stats.get('defense_lineYards', 0)
        metrics['def_second_level_yards'] = stats.get('defense_secondLevelYards', 0)
        metrics['def_open_field_yards'] = stats.get('defense_openFieldYards', 0)
        metrics['def_power_success'] = stats.get('defense_powerSuccess', 0) * 100
        metrics['def_stuff_rate'] = stats.get('defense_stuffRate', 0) * 100
        
        # Advanced defensive metrics
        metrics['defense_ppa'] = stats.get('defense_ppa', 0)
        metrics['defense_success_rate'] = stats.get('defense_successRate', 0) * 100
        metrics['defense_explosiveness'] = stats.get('defense_explosiveness', 0)
        metrics['def_points_per_opportunity'] = stats.get('defense_pointsPerOpportunity', 0)
        
        # Standard vs passing downs
        std_downs = stats.get('defense_standardDowns', {})
        pass_downs = stats.get('defense_passingDowns', {})
        
        metrics['def_standard_downs_ppa'] = std_downs.get('ppa', 0)
        metrics['def_standard_downs_success'] = std_downs.get('successRate', 0) * 100
        metrics['def_passing_downs_ppa'] = pass_downs.get('ppa', 0)
        metrics['def_passing_downs_success'] = pass_downs.get('successRate', 0) * 100
        
        # Play type defense
        rush_plays = stats.get('defense_rushingPlays', {})
        pass_plays = stats.get('defense_passingPlays', {})
        
        metrics['def_rushing_ppa'] = rush_plays.get('ppa', 0)
        metrics['def_rushing_success'] = rush_plays.get('successRate', 0) * 100
        metrics['def_rushing_explosiveness'] = rush_plays.get('explosiveness', 0)
        
        metrics['def_passing_ppa'] = pass_plays.get('ppa', 0)
        metrics['def_passing_success'] = pass_plays.get('successRate', 0) * 100
        metrics['def_passing_explosiveness'] = pass_plays.get('explosiveness', 0)
        
        # Havoc metrics
        havoc = stats.get('defense_havoc', {})
        metrics['defense_havoc_total'] = havoc.get('total', 0) * 100
        metrics['defense_havoc_front_seven'] = havoc.get('frontSeven', 0) * 100
        metrics['defense_havoc_db'] = havoc.get('db', 0) * 100
        
        # Special teams defense
        metrics['kick_return_avg_allowed'] = self.safe_division(stats.get('kickReturnYardsOpponent', 0), stats.get('kickReturnsOpponent', 1))
        metrics['punt_return_avg_allowed'] = self.safe_division(stats.get('puntReturnYardsOpponent', 0), stats.get('puntReturnsOpponent', 1))
        metrics['opponent_penalty_yards_per_game'] = self.safe_division(stats.get('penaltyYardsOpponent', 0), stats.get('games', 1))
        
        return metrics
    
    def calculate_ratings_metrics(self, team_name: str) -> Dict[str, float]:
        """Extract ratings metrics for a team"""
        metrics = {}
        
        if team_name not in self.teams_ratings:
            return metrics
        
        team_ratings = self.teams_ratings[team_name]
        
        if not team_ratings.get('ratings_available', False):
            return metrics
        
        # Core ratings
        metrics['elo'] = team_ratings.get('elo', 1500)
        metrics['fpi'] = team_ratings.get('fpi', 0)
        metrics['sp_overall'] = team_ratings.get('sp_overall', 0)
        metrics['srs'] = team_ratings.get('srs', 0)
        
        # FPI components
        fpi_comp = team_ratings.get('fpi_components', {})
        metrics['fpi_offensive_eff'] = fpi_comp.get('offensive_efficiency', 0)
        metrics['fpi_defensive_eff'] = fpi_comp.get('defensive_efficiency', 0)
        metrics['fpi_special_teams_eff'] = fpi_comp.get('special_teams_efficiency', 0)
        metrics['fpi_overall_eff'] = fpi_comp.get('overall_efficiency', 0)
        
        # SP+ components
        sp_comp = team_ratings.get('sp_components', {})
        metrics['sp_offense'] = sp_comp.get('offense', 0)
        metrics['sp_defense'] = sp_comp.get('defense', 0)
        metrics['sp_special_teams'] = sp_comp.get('special_teams', 0)
        
        # FPI rankings (lower is better, so we'll reverse these)
        fpi_ranks = team_ratings.get('fpi_rankings', {})
        metrics['sos_rank'] = fpi_ranks.get('sos_rank', 130)
        metrics['remaining_sos_rank'] = fpi_ranks.get('remaining_sos_rank', 130)
        metrics['strength_of_record_rank'] = fpi_ranks.get('strength_of_record_rank', 130)
        metrics['resume_rank'] = fpi_ranks.get('resume_rank', 130)
        metrics['game_control_rank'] = fpi_ranks.get('game_control_rank', 130)
        metrics['avg_win_probability_rank'] = fpi_ranks.get('avg_win_probability_rank', 130)
        
        return metrics
    
    def calculate_composite_score(self) -> Dict[str, Dict]:
        """Calculate comprehensive composite scores using ALL metrics + ratings"""
        
        # Extract all metrics for all teams
        all_offensive_metrics = {}
        all_defensive_metrics = {}
        all_ratings_metrics = {}
        
        for i, team_data in enumerate(self.teams_stats):
            team_name = team_data['team']
            all_offensive_metrics[i] = self.calculate_offensive_metrics(team_data)
            all_defensive_metrics[i] = self.calculate_defensive_metrics(team_data)
            all_ratings_metrics[i] = self.calculate_ratings_metrics(team_name)
        
        # Get all unique metric names
        offensive_metric_names = set()
        defensive_metric_names = set()
        ratings_metric_names = set()
        
        for metrics in all_offensive_metrics.values():
            offensive_metric_names.update(metrics.keys())
        for metrics in all_defensive_metrics.values():
            defensive_metric_names.update(metrics.keys())
        for metrics in all_ratings_metrics.values():
            ratings_metric_names.update(metrics.keys())
        
        # Normalize each metric across all teams
        normalized_scores = {}
        
        for i in range(len(self.teams_stats)):
            team_name = self.teams_stats[i]['team']
            normalized_scores[team_name] = {
                'offensive': {},
                'defensive': {},
                'ratings': {},
                'raw_offensive': all_offensive_metrics[i],
                'raw_defensive': all_defensive_metrics[i],
                'raw_ratings': all_ratings_metrics[i]
            }
        
        # Normalize offensive metrics
        for metric in offensive_metric_names:
            values = []
            team_indices = []
            
            for i in range(len(self.teams_stats)):
                if metric in all_offensive_metrics[i]:
                    values.append(all_offensive_metrics[i][metric])
                    team_indices.append(i)
            
            if values:
                reverse_metrics = ['interception_pct', 'stuff_rate', 'penalty_yards_per_game']
                reverse = any(rev in metric for rev in reverse_metrics)
                normalized = self.normalize_stat(values, reverse=reverse)
                
                for idx, team_idx in enumerate(team_indices):
                    team_name = self.teams_stats[team_idx]['team']
                    normalized_scores[team_name]['offensive'][metric] = normalized[idx]
        
        # Normalize defensive metrics
        for metric in defensive_metric_names:
            values = []
            team_indices = []
            
            for i in range(len(self.teams_stats)):
                if metric in all_defensive_metrics[i]:
                    values.append(all_defensive_metrics[i][metric])
                    team_indices.append(i)
            
            if values:
                reverse_metrics = ['yards_allowed', 'completion_pct_allowed', 'yards_per', 
                                  'allowed', 'ppa', 'explosiveness', 'line_yards',
                                  'second_level_yards', 'open_field_yards', 'power_success',
                                  'points_per_opportunity', 'return_avg_allowed']
                
                good_metrics = ['interceptions', 'fumbles_recovered', 'takeaways',
                              'sacks', 'tackles_for_loss', 'havoc', 'stuff_rate',
                              'success_rate', 'opponent_penalty']
                
                reverse = any(rev in metric for rev in reverse_metrics) and not any(good in metric for good in good_metrics)
                normalized = self.normalize_stat(values, reverse=reverse)
                
                for idx, team_idx in enumerate(team_indices):
                    team_name = self.teams_stats[team_idx]['team']
                    normalized_scores[team_name]['defensive'][metric] = normalized[idx]
        
        # Normalize ratings metrics
        for metric in ratings_metric_names:
            values = []
            team_indices = []
            
            for i in range(len(self.teams_stats)):
                if metric in all_ratings_metrics[i]:
                    values.append(all_ratings_metrics[i][metric])
                    team_indices.append(i)
            
            if values:
                # Rankings are reverse (lower is better)
                rank_metrics = ['rank']
                reverse = any(rank in metric for rank in rank_metrics)
                normalized = self.normalize_stat(values, reverse=reverse)
                
                for idx, team_idx in enumerate(team_indices):
                    team_name = self.teams_stats[team_idx]['team']
                    normalized_scores[team_name]['ratings'][metric] = normalized[idx]
        
        # Calculate weighted composite scores
        composite_rankings = {}
        
        for team_name, scores in normalized_scores.items():
            # Offensive score
            offensive_score = sum(scores['offensive'].values()) / len(scores['offensive']) if scores['offensive'] else 0
            
            # Defensive score
            defensive_score = sum(scores['defensive'].values()) / len(scores['defensive']) if scores['defensive'] else 0
            
            # Ratings score
            ratings_score = sum(scores['ratings'].values()) / len(scores['ratings']) if scores['ratings'] else 0
            
            # SOS score (if schedule data available)
            sos_score = 0
            if team_name in self.teams_schedules:
                sos_data = self.teams_schedules[team_name]['season_summary']
                
                # Normalize SOS metrics to 0-100 scale
                # Average opponent ELO (higher is harder schedule)
                avg_opp_elo = sos_data.get('average_opponent_elo', 1500)
                sos_elo_score = ((avg_opp_elo - 1200) / 800) * 100  # Normalize 1200-2000 to 0-100
                sos_elo_score = max(0, min(100, sos_elo_score))
                
                # Average opponent FPI (higher is harder)
                avg_opp_fpi = sos_data.get('average_opponent_fpi', 0)
                sos_fpi_score = ((avg_opp_fpi + 20) / 40) * 100  # Normalize -20 to +20 to 0-100
                sos_fpi_score = max(0, min(100, sos_fpi_score))
                
                # Average opponent SP+ (higher is harder)
                avg_opp_sp = sos_data.get('average_opponent_sp_overall', 0)
                sos_sp_score = ((avg_opp_sp + 20) / 40) * 100  # Normalize -20 to +20 to 0-100
                sos_sp_score = max(0, min(100, sos_sp_score))
                
                # Combine SOS metrics (equal weight)
                sos_score = (sos_elo_score + sos_fpi_score + sos_sp_score) / 3
            
            # Overall composite: 35% stats, 40% ratings, 25% SOS
            # Within stats: 55% offense, 45% defense
            stats_score = (offensive_score * 0.55) + (defensive_score * 0.45)
            overall_score = (stats_score * 0.35) + (ratings_score * 0.40) + (sos_score * 0.25)
            
            composite_rankings[team_name] = {
                'overall_score': overall_score,
                'offensive_score': offensive_score,
                'defensive_score': defensive_score,
                'ratings_score': ratings_score,
                'sos_score': sos_score,
                'stats_score': stats_score,
                'offensive_metrics': scores['offensive'],
                'defensive_metrics': scores['defensive'],
                'ratings_metrics': scores['ratings'],
                'raw_offensive_metrics': scores['raw_offensive'],
                'raw_defensive_metrics': scores['raw_defensive'],
                'raw_ratings_metrics': scores['raw_ratings'],
                'conference': next(t['conference'] for t in self.teams_stats if t['team'] == team_name),
                'total_metrics_used': len(scores['offensive']) + len(scores['defensive']) + len(scores['ratings'])
            }
        
        return composite_rankings
    
    def generate_rankings(self) -> List[Tuple[int, str, Dict]]:
        """Generate final power rankings"""
        composite_scores = self.calculate_composite_score()
        
        # Sort by overall score
        ranked = sorted(
            composite_scores.items(),
            key=lambda x: x[1]['overall_score'],
            reverse=True
        )
        
        # Add rank number
        rankings = [(i + 1, team, data) for i, (team, data) in enumerate(ranked)]
        
        return rankings
    
    def generate_team_report(self, team_name: str, rank: int, data: Dict) -> Dict:
        """Generate detailed report for a team including quality wins and schedule analysis"""
        report = {
            'team': team_name,
            'rank': rank,
            'conference': data['conference'],
            'overall_score': data['overall_score'],
            'stats_score': data['stats_score'],
            'ratings_score': data['ratings_score'],
            'sos_score': data['sos_score'],
            'record': 'N/A',
            'quality_wins': [],
            'quality_losses': [],
            'ranked_games': [],
            'bad_losses': [],
            'key_stats': {},
            'key_ratings': {}
        }
        
        # Get schedule data if available
        if team_name in self.teams_schedules:
            team_schedule = self.teams_schedules[team_name]
            summary = team_schedule['season_summary']
            
            report['record'] = summary.get('record', 'N/A')
            report['wins'] = summary.get('wins', 0)
            report['losses'] = summary.get('losses', 0)
            report['avg_opponent_elo'] = summary.get('average_opponent_elo', 0)
            
            # Analyze games
            for game in team_schedule['games']:
                opponent = game['opponent']
                result = game.get('result', 'Scheduled')
                opp_ratings = game.get('opponent_ratings')
                
                if opp_ratings:
                    elo = opp_ratings.get('elo', 0)
                    
                    game_info = {
                        'opponent': opponent,
                        'result': result,
                        'score': f"{game.get('team_score', '?')}-{game.get('opponent_score', '?')}",
                        'elo': elo,
                        'location': game.get('location', 'N/A')
                    }
                    
                    # Quality wins (ELO > 1600 and won)
                    if result == 'W' and elo > 1600:
                        report['quality_wins'].append(game_info)
                    
                    # Quality losses (lost to ranked opponent)
                    elif result == 'L' and elo > 1600:
                        report['quality_losses'].append(game_info)
                    
                    # Bad losses (lost to weak opponent)
                    elif result == 'L' and elo < 1600:
                        report['bad_losses'].append(game_info)
                    
                    # All ranked matchups (ELO > 1600)
                    if elo > 1600:
                        report['ranked_games'].append(game_info)
        
        # Extract key stats
        raw_off = data['raw_offensive_metrics']
        raw_def = data['raw_defensive_metrics']
        raw_rat = data['raw_ratings_metrics']
        
        report['key_stats'] = {
            'points_per_game': raw_off.get('points_per_game', raw_off.get('yards_per_game', 0) / 10),  # Use actual PPG if available
            'yards_per_play': raw_off.get('yards_per_play', 0),
            'third_down_pct': raw_off.get('third_down_pct', 0),
            'turnovers_margin': raw_off.get('turnover_margin', 0),
            'yards_allowed_per_game': raw_def.get('yards_allowed_per_game', 0),
            'sacks_per_game': raw_def.get('sacks_per_game', 0),
            'takeaways_per_game': raw_def.get('takeaways_per_game', 0)
        }
        
        report['key_ratings'] = {
            'elo': raw_rat.get('elo', 1500),
            'fpi': raw_rat.get('fpi', 0),
            'sp_overall': raw_rat.get('sp_overall', 0),
            'srs': raw_rat.get('srs', 0)
        }
        
        return report
    
    def print_top_rankings(self, top_n: int = 25):
        """Print top N rankings to console"""
        rankings = self.generate_rankings()
        
        print(f"\n{'='*120}")
        print(f"ENHANCED FBS POWER RANKINGS - TOP {top_n}")
        print(f"(Stats + Ratings + Strength of Schedule)")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*120}\n")
        
        print(f"{'Rank':<6} {'Team':<25} {'Conference':<20} {'Overall':<9} {'Stats':<9} {'Ratings':<9} {'SOS':<9}")
        print(f"{'-'*120}")
        
        for rank, team, data in rankings[:top_n]:
            print(f"{rank:<6} {team:<25} {data['conference']:<20} "
                  f"{data['overall_score']:>6.2f}    {data['stats_score']:>6.2f}    "
                  f"{data['ratings_score']:>6.2f}    {data['sos_score']:>6.2f}")
        
        print(f"\n{'='*120}\n")
    
    def generate_detailed_reports(self, top_n: int = 25) -> Dict:
        """Generate detailed reports for top N teams"""
        rankings = self.generate_rankings()
        reports = {}
        
        for rank, team, data in rankings[:top_n]:
            reports[team] = self.generate_team_report(team, rank, data)
        
        return reports
    
    def save_detailed_reports(self, top_n: int = 25, output_file: str = None):
        """Save detailed reports to JSON file"""
        reports = self.generate_detailed_reports(top_n)
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"enhanced_power_rankings_detailed_{timestamp}.json"
        
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'algorithm': '40% Stats + 50% Ratings + 10% SOS',
                'stats_breakdown': '55% Offense + 45% Defense',
                'total_teams_analyzed': len(self.teams_stats),
                'top_n': top_n
            },
            'rankings': reports
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Detailed reports saved to: {output_file}")
        return output_file
    
    def save_markdown_report(self, top_n: int = 25, output_file: str = None):
        """Save detailed reports to Markdown file"""
        reports = self.generate_detailed_reports(top_n)
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"enhanced_power_rankings_report_{timestamp}.md"
        
        with open(output_file, 'w') as f:
            # Header
            f.write("# 🏈 Enhanced FBS Power Rankings - Detailed Analysis\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")
            f.write("---\n\n")
            
            # Algorithm explanation
            f.write("## 📊 Algorithm Methodology\n\n")
            f.write("**Weighting Formula:** `40% Stats + 50% Ratings + 10% Strength of Schedule`\n\n")
            f.write("### Stats Component (40%)\n")
            f.write("- **55% Offensive Metrics:** Yards/play, efficiency, passing/rushing stats, PPA, explosiveness\n")
            f.write("- **45% Defensive Metrics:** Yards allowed, sacks, takeaways, havoc rate, success rate\n")
            f.write("- **Total:** ~60 statistical categories per team\n\n")
            
            f.write("### Ratings Component (50%)\n")
            f.write("- **ELO Rating:** Team strength based on game results\n")
            f.write("- **FPI (Football Power Index):** ESPN's predictive rating with efficiency metrics\n")
            f.write("- **SP+ (Success Rate Plus):** Advanced efficiency rating\n")
            f.write("- **SRS (Simple Rating System):** Point differential adjusted for opponent strength\n\n")
            
            f.write("### Strength of Schedule (10%)\n")
            f.write("- Average opponent ELO rating (normalized to 0-100)\n")
            f.write("- Average opponent FPI rating (normalized to 0-100)\n")
            f.write("- Average opponent SP+ rating (normalized to 0-100)\n\n")
            
            f.write("---\n\n")
            
            # Rankings table
            f.write("## 🏆 Top 25 Rankings Summary\n\n")
            f.write("| Rank | Team | Conference | Overall | Stats | Ratings | SOS |\n")
            f.write("|------|------|------------|---------|-------|---------|-----|\n")
            
            for team_name, report in list(reports.items())[:top_n]:
                f.write(f"| {report['rank']} | **{team_name}** | {report['conference']} | "
                       f"{report['overall_score']:.2f} | {report['stats_score']:.2f} | "
                       f"{report['ratings_score']:.2f} | {report['sos_score']:.2f} |\n")
            
            f.write("\n---\n\n")
            
            # Detailed team reports
            f.write("## 📋 Detailed Team Analysis\n\n")
            
            for team_name, report in list(reports.items())[:top_n]:
                f.write(f"### #{report['rank']} {team_name} ({report['conference']})\n\n")
                
                # Overall scores
                f.write("**Overall Composite Score:** `{:.2f}`\n\n".format(report['overall_score']))
                f.write("| Component | Score |\n")
                f.write("|-----------|-------|\n")
                f.write(f"| Stats | {report['stats_score']:.2f} |\n")
                f.write(f"| Ratings | {report['ratings_score']:.2f} |\n")
                f.write(f"| SOS | {report['sos_score']:.2f} |\n\n")
                
                # Record
                f.write(f"**Record:** {report['record']}\n\n")
                if report.get('avg_opponent_elo'):
                    f.write(f"**Average Opponent ELO:** {report['avg_opponent_elo']:.1f}\n\n")
                
                # Quality wins
                if report['quality_wins']:
                    f.write(f"#### ✅ Quality Wins ({len(report['quality_wins'])})\n\n")
                    f.write("| Opponent | Score | ELO | Location |\n")
                    f.write("|----------|-------|-----|----------|\n")
                    for game in report['quality_wins']:
                        f.write(f"| {game['opponent']} | {game['score']} | {game['elo']:.0f} | {game['location']} |\n")
                    f.write("\n")
                else:
                    f.write("#### ✅ Quality Wins\n\nNone\n\n")
                
                # Quality losses
                if report['quality_losses']:
                    f.write(f"#### ❌ Losses to Ranked Opponents ({len(report['quality_losses'])})\n\n")
                    f.write("| Opponent | Score | ELO | Location |\n")
                    f.write("|----------|-------|-----|----------|\n")
                    for game in report['quality_losses']:
                        f.write(f"| {game['opponent']} | {game['score']} | {game['elo']:.0f} | {game['location']} |\n")
                    f.write("\n")
                
                # Bad losses
                if report['bad_losses']:
                    f.write(f"#### ⚠️ Bad Losses ({len(report['bad_losses'])})\n\n")
                    f.write("| Opponent | Score | ELO | Location |\n")
                    f.write("|----------|-------|-----|----------|\n")
                    for game in report['bad_losses']:
                        f.write(f"| {game['opponent']} | {game['score']} | {game['elo']:.0f} | {game['location']} |\n")
                    f.write("\n")
                
                # Key ratings
                ratings = report['key_ratings']
                f.write("#### 📈 Key Ratings\n\n")
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                f.write(f"| ELO | {ratings['elo']:.0f} |\n")
                f.write(f"| FPI | {ratings['fpi']:.1f} |\n")
                f.write(f"| SP+ | {ratings['sp_overall']:.1f} |\n")
                f.write(f"| SRS | {ratings['srs']:.2f} |\n\n")
                
                # Key stats
                stats = report['key_stats']
                f.write("#### 📊 Key Statistics\n\n")
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                f.write(f"| Yards per Play | {stats['yards_per_play']:.2f} |\n")
                f.write(f"| Third Down % | {stats['third_down_pct']:.1f}% |\n")
                f.write(f"| Turnover Margin | {stats['turnovers_margin']:+.0f} |\n")
                f.write(f"| Sacks per Game | {stats['sacks_per_game']:.1f} |\n")
                f.write(f"| Takeaways per Game | {stats['takeaways_per_game']:.1f} |\n")
                f.write(f"| Yards Allowed/Game | {stats['yards_allowed_per_game']:.1f} |\n\n")
                
                f.write("---\n\n")
            
            # Footer
            f.write("## 📌 Notes\n\n")
            f.write("- **Quality Win:** Victory against opponent with ELO rating > 1600 (typically ranked teams)\n")
            f.write("- **Quality Loss:** Loss to opponent with ELO rating > 1600\n")
            f.write("- **Bad Loss:** Loss to opponent with ELO rating < 1600 (unranked teams)\n")
            f.write("- **ELO Scale:** Average = 1500, Elite = 2000+, Top 25 ≈ 1600+\n\n")
            
            f.write(f"**Data Sources:**\n")
            f.write(f"- College Football Data API\n")
            f.write(f"- Week 10, 2025 Season\n")
            f.write(f"- 136 FBS teams analyzed\n")
        
        print(f"📄 Markdown report saved to: {output_file}")
        return output_file
    
    def print_detailed_analysis(self, top_n: int = 25):
        """Print detailed analysis for each top team"""
        reports = self.generate_detailed_reports(top_n)
        
        print(f"\n{'='*120}")
        print(f"DETAILED TEAM ANALYSIS - TOP {top_n}")
        print(f"{'='*120}\n")
        
        for team_name, report in list(reports.items())[:top_n]:
            print(f"\n{'='*120}")
            print(f"#{report['rank']} {team_name.upper()} ({report['conference']})")
            print(f"{'='*120}")
            
            print(f"\n📊 OVERALL SCORES:")
            print(f"  Composite: {report['overall_score']:.2f}")
            print(f"  Stats: {report['stats_score']:.2f} | Ratings: {report['ratings_score']:.2f} | SOS: {report['sos_score']:.2f}")
            
            print(f"\n🏈 RECORD: {report['record']}")
            
            if report.get('avg_opponent_elo'):
                print(f"📈 Average Opponent ELO: {report['avg_opponent_elo']:.1f}")
            
            # Quality wins
            if report['quality_wins']:
                print(f"\n✅ QUALITY WINS ({len(report['quality_wins'])}):")
                for game in report['quality_wins']:
                    print(f"   • {game['result']} vs {game['opponent']} ({game['score']}) - ELO: {game['elo']:.0f} [{game['location']}]")
            else:
                print(f"\n✅ QUALITY WINS: None")
            
            # Quality losses
            if report['quality_losses']:
                print(f"\n❌ LOSSES TO RANKED OPPONENTS ({len(report['quality_losses'])}):")
                for game in report['quality_losses']:
                    print(f"   • {game['result']} vs {game['opponent']} ({game['score']}) - ELO: {game['elo']:.0f} [{game['location']}]")
            
            # Bad losses
            if report['bad_losses']:
                print(f"\n⚠️  BAD LOSSES ({len(report['bad_losses'])}):")
                for game in report['bad_losses']:
                    print(f"   • {game['result']} vs {game['opponent']} ({game['score']}) - ELO: {game['elo']:.0f} [{game['location']}]")
            
            # Key ratings
            ratings = report['key_ratings']
            print(f"\n📈 KEY RATINGS:")
            print(f"   ELO: {ratings['elo']:.0f} | FPI: {ratings['fpi']:.1f} | SP+: {ratings['sp_overall']:.1f} | SRS: {ratings['srs']:.2f}")
            
            # Key stats
            stats = report['key_stats']
            print(f"\n📊 KEY STATS:")
            print(f"   Yards/Play: {stats['yards_per_play']:.2f} | 3rd Down: {stats['third_down_pct']:.1f}%")
            print(f"   Turnover Margin: {stats['turnovers_margin']:+.0f} | Sacks/Game: {stats['sacks_per_game']:.1f}")
            print(f"   Yards Allowed/Game: {stats['yards_allowed_per_game']:.1f}")
            
            print(f"\n{'-'*120}")


def main():
    """Main execution"""
    print("🏈 Enhanced FBS Power Rankings Generator")
    print("=" * 80)
    
    # File paths - using latest Week 15 data
    stats_file = 'weekly_updates/week_15/fbs_team_stats_complete.json'
    ratings_file = 'weekly_updates/week_15/all_fbs_ratings_comprehensive_2025_20251203_054653.json'
    schedule_file = 'weekly_updates/week_15/all_fbs_teams_schedules_2025_20251201_103736.json'
    
    # Load and generate rankings
    ranker = EnhancedPowerRankings(
        stats_file,
        ratings_file,
        schedule_file
    )
    
    print(f"✅ Loaded {len(ranker.teams_stats)} teams with stats")
    print(f"✅ Loaded {len(ranker.teams_ratings)} teams with ratings")
    print(f"✅ Loaded {len(ranker.teams_schedules)} teams with schedule data")
    print("⚙️  Calculating comprehensive metrics with ratings + SOS...")
    
    # Print top 25 summary
    ranker.print_top_rankings(25)
    
    print(f"📊 Weighting: 40% Stats + 50% Ratings + 10% SOS")
    print(f"📈 Total metrics per team: ~100 (stats + ratings + schedule strength)")
    
    # Print detailed analysis for each top 25 team
    ranker.print_detailed_analysis(25)
    
    # Save detailed reports to JSON for ALL 136 teams
    ranker.save_detailed_reports(136)
    
    # Save markdown report
    ranker.save_markdown_report(25)
    
    print("\n✅ Complete!\n")


if __name__ == '__main__':
    main()
