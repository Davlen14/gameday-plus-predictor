#!/usr/bin/env python3
"""
Comprehensive FBS Power Rankings Generator
Uses ALL available statistics to create composite power rankings
"""

import json
import math
from typing import Dict, List, Tuple
from datetime import datetime

class ComprehensivePowerRankings:
    def __init__(self, stats_file: str):
        """Initialize with stats file"""
        with open(stats_file, 'r') as f:
            data = json.load(f)
            self.teams = data.get('teams', data) if isinstance(data, dict) else data
        
        self.team_scores = {}
        self.stat_rankings = {}
        
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
        
        # Time of possession
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
        
        # Penalty discipline
        metrics['penalty_yards_per_game'] = self.safe_division(stats.get('penaltyYards', 0), stats.get('games', 1))
        
        return metrics
    
    def calculate_defensive_metrics(self, team_data: Dict) -> Dict[str, float]:
        """Calculate all defensive derived metrics"""
        stats = team_data['stats']
        metrics = {}
        
        # Basic efficiency metrics (lower is better for defense)
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
        
        # Line play metrics (lower is better)
        metrics['def_line_yards'] = stats.get('defense_lineYards', 0)
        metrics['def_second_level_yards'] = stats.get('defense_secondLevelYards', 0)
        metrics['def_open_field_yards'] = stats.get('defense_openFieldYards', 0)
        metrics['def_power_success'] = stats.get('defense_powerSuccess', 0) * 100
        metrics['def_stuff_rate'] = stats.get('defense_stuffRate', 0) * 100
        
        # Advanced defensive metrics (lower is better for PPA, higher for success rate and havoc)
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
        
        # Havoc metrics (higher is better)
        havoc = stats.get('defense_havoc', {})
        metrics['defense_havoc_total'] = havoc.get('total', 0) * 100
        metrics['defense_havoc_front_seven'] = havoc.get('frontSeven', 0) * 100
        metrics['defense_havoc_db'] = havoc.get('db', 0) * 100
        
        # Special teams defense
        metrics['kick_return_avg_allowed'] = self.safe_division(stats.get('kickReturnYardsOpponent', 0), stats.get('kickReturnsOpponent', 1))
        metrics['punt_return_avg_allowed'] = self.safe_division(stats.get('puntReturnYardsOpponent', 0), stats.get('puntReturnsOpponent', 1))
        
        # Opponent penalty advantage
        metrics['opponent_penalty_yards_per_game'] = self.safe_division(stats.get('penaltyYardsOpponent', 0), stats.get('games', 1))
        
        return metrics
    
    def calculate_composite_score(self) -> Dict[str, Dict]:
        """Calculate comprehensive composite scores using ALL metrics"""
        
        # Extract all metrics for all teams
        all_offensive_metrics = {}
        all_defensive_metrics = {}
        
        for i, team_data in enumerate(self.teams):
            team_name = team_data['team']
            all_offensive_metrics[i] = self.calculate_offensive_metrics(team_data)
            all_defensive_metrics[i] = self.calculate_defensive_metrics(team_data)
        
        # Get all unique metric names
        offensive_metric_names = set()
        defensive_metric_names = set()
        
        for metrics in all_offensive_metrics.values():
            offensive_metric_names.update(metrics.keys())
        for metrics in all_defensive_metrics.values():
            defensive_metric_names.update(metrics.keys())
        
        # Normalize each metric across all teams
        normalized_scores = {}
        
        for i in range(len(self.teams)):
            team_name = self.teams[i]['team']
            normalized_scores[team_name] = {
                'offensive': {},
                'defensive': {},
                'raw_offensive': all_offensive_metrics[i],
                'raw_defensive': all_defensive_metrics[i]
            }
        
        # Normalize offensive metrics
        for metric in offensive_metric_names:
            values = []
            team_indices = []
            
            for i in range(len(self.teams)):
                if metric in all_offensive_metrics[i]:
                    values.append(all_offensive_metrics[i][metric])
                    team_indices.append(i)
            
            if values:
                # Determine if metric should be reversed (lower is better)
                reverse_metrics = [
                    'interception_pct', 'stuff_rate', 'penalty_yards_per_game'
                ]
                reverse = any(rev in metric for rev in reverse_metrics)
                
                normalized = self.normalize_stat(values, reverse=reverse)
                
                for idx, team_idx in enumerate(team_indices):
                    team_name = self.teams[team_idx]['team']
                    normalized_scores[team_name]['offensive'][metric] = normalized[idx]
        
        # Normalize defensive metrics
        for metric in defensive_metric_names:
            values = []
            team_indices = []
            
            for i in range(len(self.teams)):
                if metric in all_defensive_metrics[i]:
                    values.append(all_defensive_metrics[i][metric])
                    team_indices.append(i)
            
            if values:
                # For defense, most metrics are "lower is better" except takeaways, sacks, havoc, stuff rate
                reverse_metrics = [
                    'yards_allowed', 'completion_pct_allowed', 'yards_per', 
                    'allowed', 'ppa', 'explosiveness', 'line_yards',
                    'second_level_yards', 'open_field_yards', 'power_success',
                    'points_per_opportunity', 'return_avg_allowed'
                ]
                
                good_metrics = [
                    'interceptions', 'fumbles_recovered', 'takeaways',
                    'sacks', 'tackles_for_loss', 'havoc', 'stuff_rate',
                    'success_rate', 'opponent_penalty'
                ]
                
                reverse = any(rev in metric for rev in reverse_metrics) and not any(good in metric for good in good_metrics)
                
                normalized = self.normalize_stat(values, reverse=reverse)
                
                for idx, team_idx in enumerate(team_indices):
                    team_name = self.teams[team_idx]['team']
                    normalized_scores[team_name]['defensive'][metric] = normalized[idx]
        
        # Calculate weighted composite scores
        composite_rankings = {}
        
        for team_name, scores in normalized_scores.items():
            # Offensive score (equal weight to all offensive metrics)
            offensive_score = sum(scores['offensive'].values()) / len(scores['offensive']) if scores['offensive'] else 0
            
            # Defensive score (equal weight to all defensive metrics)
            defensive_score = sum(scores['defensive'].values()) / len(scores['defensive']) if scores['defensive'] else 0
            
            # Overall composite (60% offense, 40% defense - can adjust)
            overall_score = (offensive_score * 0.55) + (defensive_score * 0.45)
            
            composite_rankings[team_name] = {
                'overall_score': overall_score,
                'offensive_score': offensive_score,
                'defensive_score': defensive_score,
                'offensive_metrics': scores['offensive'],
                'defensive_metrics': scores['defensive'],
                'raw_offensive_metrics': scores['raw_offensive'],
                'raw_defensive_metrics': scores['raw_defensive'],
                'conference': next(t['conference'] for t in self.teams if t['team'] == team_name),
                'total_metrics_used': len(scores['offensive']) + len(scores['defensive'])
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
    
    def save_rankings(self, output_file: str, detailed: bool = True):
        """Save rankings to JSON file"""
        rankings = self.generate_rankings()
        
        output = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_teams': len(rankings),
                'methodology': 'Comprehensive composite score using ALL available offensive and defensive metrics',
                'weighting': 'Offensive: 55%, Defensive: 45%',
                'normalization': 'All metrics normalized to 0-100 scale'
            },
            'rankings': []
        }
        
        for rank, team, data in rankings:
            team_ranking = {
                'rank': rank,
                'team': team,
                'conference': data['conference'],
                'overall_score': round(data['overall_score'], 2),
                'offensive_score': round(data['offensive_score'], 2),
                'defensive_score': round(data['defensive_score'], 2),
                'total_metrics_analyzed': data['total_metrics_used']
            }
            
            if detailed:
                team_ranking['detailed_metrics'] = {
                    'offensive_normalized': {k: round(v, 2) for k, v in data['offensive_metrics'].items()},
                    'defensive_normalized': {k: round(v, 2) for k, v in data['defensive_metrics'].items()},
                    'offensive_raw': {k: round(v, 3) if isinstance(v, float) else v 
                                     for k, v in data['raw_offensive_metrics'].items()},
                    'defensive_raw': {k: round(v, 3) if isinstance(v, float) else v 
                                     for k, v in data['raw_defensive_metrics'].items()}
                }
            
            output['rankings'].append(team_ranking)
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        return output
    
    def print_top_rankings(self, top_n: int = 25):
        """Print top N rankings to console"""
        rankings = self.generate_rankings()
        
        print(f"\n{'='*100}")
        print(f"COMPREHENSIVE FBS POWER RANKINGS - TOP {top_n}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*100}\n")
        
        print(f"{'Rank':<6} {'Team':<30} {'Conference':<20} {'Overall':<10} {'Offense':<10} {'Defense':<10}")
        print(f"{'-'*100}")
        
        for rank, team, data in rankings[:top_n]:
            print(f"{rank:<6} {team:<30} {data['conference']:<20} "
                  f"{data['overall_score']:>7.2f}    {data['offensive_score']:>7.2f}    "
                  f"{data['defensive_score']:>7.2f}")
        
        print(f"\n{'='*100}\n")


def main():
    """Main execution"""
    print("🏈 Comprehensive FBS Power Rankings Generator")
    print("=" * 80)
    
    # Load and generate rankings
    ranker = ComprehensivePowerRankings('weekly_updates/week_15/fbs_team_stats_complete.json')
    
    print(f"✅ Loaded {len(ranker.teams)} teams")
    print("⚙️  Calculating comprehensive metrics...")
    
    # Save detailed rankings
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'comprehensive_power_rankings_{timestamp}.json'
    
    ranker.save_rankings(output_file, detailed=True)
    
    # Print top 25
    ranker.print_top_rankings(25)
    
    print(f"💾 Detailed rankings saved to: {output_file}")
    print(f"📊 Total metrics per team: ~{ranker.generate_rankings()[0][2]['total_metrics_used']} offensive + defensive metrics")
    print("\n✅ Complete!\n")


if __name__ == '__main__':
    main()
