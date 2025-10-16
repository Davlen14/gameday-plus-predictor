#!/usr/bin/env python3
"""
📊 Simple Performance Visualizer
Creates basic charts from backtesting results (no external dependencies)
"""

import json
import os
from typing import Dict, List

class SimpleVisualizer:
    """Simple text-based visualization for backtesting results"""
    
    def create_performance_dashboard(self, results_file: str = "backtesting_results/detailed_results.json"):
        """Create a text-based performance dashboard"""
        
        if not os.path.exists(results_file):
            print("❌ No results file found. Run backtesting first!")
            return
        
        print("📊 PERFORMANCE DASHBOARD")
        print("="*60)
        
        # Load results
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        results = data['results']
        total_games = len(results)
        
        # Calculate basic metrics
        winners_correct = sum(1 for r in results if r['winner_correct'])
        winner_accuracy = winners_correct / total_games
        
        # Spread errors
        spread_errors = [r['spread_error'] for r in results]
        avg_spread_error = sum(spread_errors) / len(spread_errors)
        
        # ATS performance  
        ats_results = [r for r in results if r['ats_correct'] is not None]
        if ats_results:
            ats_correct = sum(1 for r in ats_results if r['ats_correct'])
            ats_accuracy = ats_correct / len(ats_results)
        else:
            ats_accuracy = 0
            ats_correct = 0
            
        # Performance by season
        season_stats = {}
        for result in results:
            season = result['season']
            if season not in season_stats:
                season_stats[season] = {'games': 0, 'correct': 0}
            
            season_stats[season]['games'] += 1
            if result['winner_correct']:
                season_stats[season]['correct'] += 1
        
        # Print summary
        print(f"\n🎯 OVERALL PERFORMANCE")
        print(f"   Games Tested: {total_games:,}")
        print(f"   Winner Accuracy: {winner_accuracy:.1%} ({winners_correct}/{total_games})")
        print(f"   Average Spread Error: {avg_spread_error:.1f} points")
        
        if ats_results:
            print(f"   ATS Performance: {ats_accuracy:.1%} ({ats_correct}/{len(ats_results)})")
        
        # Performance by season
        print(f"\n📅 BY SEASON")
        for season, stats in sorted(season_stats.items()):
            accuracy = stats['correct'] / stats['games']
            print(f"   {season}: {accuracy:.1%} ({stats['correct']}/{stats['games']} games)")
        
        # Performance distribution (text histogram)
        print(f"\n📈 WINNER ACCURACY DISTRIBUTION")
        self._print_text_histogram(
            [1 if r['winner_correct'] else 0 for r in results],
            title="Correct Predictions by Game"
        )
        
        # Spread error distribution
        print(f"\n📏 SPREAD ERROR DISTRIBUTION")  
        self._print_spread_error_histogram(spread_errors)
        
        # Weekly performance trend
        weekly_stats = {}
        for result in results:
            week = result['week']
            if week not in weekly_stats:
                weekly_stats[week] = {'games': 0, 'correct': 0}
            
            weekly_stats[week]['games'] += 1
            if result['winner_correct']:
                weekly_stats[week]['correct'] += 1
        
        print(f"\n📊 WEEKLY PERFORMANCE TREND")
        for week in sorted(weekly_stats.keys()):
            if week <= 15:  # Regular season only
                stats = weekly_stats[week]
                accuracy = stats['correct'] / stats['games'] if stats['games'] > 0 else 0
                bar_length = int(accuracy * 20)  # Scale to 20 chars
                bar = "█" * bar_length + "░" * (20 - bar_length)
                print(f"   Week {week:2d}: {bar} {accuracy:.1%} ({stats['correct']}/{stats['games']})")
        
        print(f"\n" + "="*60)
    
    def _print_text_histogram(self, values: List[float], title: str = "", bins: int = 10):
        """Print a simple text-based histogram"""
        if not values:
            return
            
        min_val = min(values)
        max_val = max(values)
        
        if min_val == max_val:
            print(f"   All values are {min_val}")
            return
        
        # Create bins
        bin_width = (max_val - min_val) / bins
        bin_counts = [0] * bins
        
        for value in values:
            bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            bin_counts[bin_idx] += 1
        
        # Print histogram
        max_count = max(bin_counts)
        for i, count in enumerate(bin_counts):
            bin_start = min_val + i * bin_width
            bin_end = min_val + (i + 1) * bin_width
            
            bar_length = int((count / max_count) * 30) if max_count > 0 else 0
            bar = "█" * bar_length
            
            print(f"   {bin_start:.1f}-{bin_end:.1f}: {bar} ({count})")
    
    def _print_spread_error_histogram(self, errors: List[float]):
        """Print spread error histogram with meaningful buckets"""
        
        # Define meaningful buckets for spread errors
        buckets = [
            (0, 3, "Excellent"),
            (3, 7, "Good"), 
            (7, 14, "Fair"),
            (14, 21, "Poor"),
            (21, float('inf'), "Very Poor")
        ]
        
        bucket_counts = [0] * len(buckets)
        
        for error in errors:
            for i, (min_val, max_val, label) in enumerate(buckets):
                if min_val <= error < max_val:
                    bucket_counts[i] += 1
                    break
        
        total_errors = len(errors)
        max_count = max(bucket_counts) if bucket_counts else 1
        
        for i, ((min_val, max_val, label), count) in enumerate(zip(buckets, bucket_counts)):
            percentage = count / total_errors if total_errors > 0 else 0
            bar_length = int((count / max_count) * 25) if max_count > 0 else 0
            bar = "█" * bar_length
            
            range_str = f"{min_val}-{max_val if max_val != float('inf') else '21+'}pts"
            print(f"   {range_str:8s} ({label:9s}): {bar:25s} {percentage:.1%} ({count})")

def main():
    """Run the simple visualizer"""
    viz = SimpleVisualizer()
    viz.create_performance_dashboard()

if __name__ == "__main__":
    main()