#!/usr/bin/env python3
"""
Analyze Explosiveness Rankings for all FBS teams
Calculate accurate percentiles and list all teams ranked by explosiveness
"""

import json
import statistics

# Load the comprehensive power rankings data
with open('weekly_updates/week_15/comprehensive_power_rankings_20251203_053934.json', 'r') as f:
    data = json.load(f)

# Extract explosiveness data from all teams
explosiveness_data = []

for team in data['rankings']:
    metrics = team['detailed_metrics']
    
    if 'offense_explosiveness' in metrics.get('offensive_raw', {}):
        explosiveness_raw = metrics['offensive_raw']['offense_explosiveness']
        explosiveness_data.append({
            'team': team['team'],
            'rank': team['rank'],
            'conference': team['conference'],
            'raw_coefficient': explosiveness_raw,
            'as_percentage': (explosiveness_raw * 100)  # Convert to percentage
        })

# Sort by raw coefficient (descending)
explosiveness_data_sorted = sorted(explosiveness_data, key=lambda x: x['raw_coefficient'], reverse=True)

# Calculate statistics
raw_values = [t['raw_coefficient'] for t in explosiveness_data]
percentage_values = [t['as_percentage'] for t in explosiveness_data]

print("=" * 80)
print("EXPLOSIVENESS ANALYSIS - ALL FBS TEAMS")
print("=" * 80)
print(f"Total Teams: {len(explosiveness_data)}")
print()

# Calculate percentiles from raw coefficients
values_sorted = sorted(raw_values)
n = len(values_sorted)

elite_idx = int(n * 0.80)  # 80th percentile
avg_idx = int(n * 0.50)    # 50th percentile
below_idx = int(n * 0.30)  # 30th percentile

elite_raw = values_sorted[elite_idx]
avg_raw = values_sorted[avg_idx]
below_raw = values_sorted[below_idx]

print("RAW COEFFICIENT STATISTICS:")
print(f"  Min:    {min(raw_values):.3f}")
print(f"  Max:    {max(raw_values):.3f}")
print(f"  Mean:   {statistics.mean(raw_values):.3f}")
print(f"  Median: {statistics.median(raw_values):.3f}")
print()
print("BENCHMARKS (Raw Coefficients):")
print(f"  Elite (80th percentile):     {elite_raw:.3f}")
print(f"  Average (50th percentile):   {avg_raw:.3f}")
print(f"  Below Avg (30th percentile): {below_raw:.3f}")
print()
print("BENCHMARKS (As Percentages - Multiplied by 100):")
print(f"  Elite:     {elite_raw * 100:.1f}%")
print(f"  Average:   {avg_raw * 100:.1f}%")
print(f"  Below Avg: {below_raw * 100:.1f}%")
print()

print("=" * 80)
print("TOP 25 MOST EXPLOSIVE TEAMS")
print("=" * 80)
print(f"{'Rank':<6} {'Team':<30} {'Conference':<15} {'Coefficient':<12} {'%':<8}")
print("-" * 80)

for i, team in enumerate(explosiveness_data_sorted[:25], 1):
    print(f"{i:<6} {team['team']:<30} {team['conference']:<15} {team['raw_coefficient']:<12.3f} {team['as_percentage']:<8.1f}")

print()
print("=" * 80)
print("BOTTOM 25 LEAST EXPLOSIVE TEAMS")
print("=" * 80)
print(f"{'Rank':<6} {'Team':<30} {'Conference':<15} {'Coefficient':<12} {'%':<8}")
print("-" * 80)

for i, team in enumerate(explosiveness_data_sorted[-25:], len(explosiveness_data_sorted) - 24):
    print(f"{i:<6} {team['team']:<30} {team['conference']:<15} {team['raw_coefficient']:<12.3f} {team['as_percentage']:<8.1f}")

print()
print("=" * 80)
print("ALL FBS TEAMS - COMPLETE EXPLOSIVENESS RANKINGS")
print("=" * 80)
print(f"{'Exp Rank':<10} {'Team':<30} {'Conference':<15} {'Overall Rank':<12} {'Coefficient':<12} {'%':<8}")
print("-" * 80)

for i, team in enumerate(explosiveness_data_sorted, 1):
    print(f"{i:<10} {team['team']:<30} {team['conference']:<15} {team['rank']:<12} {team['raw_coefficient']:<12.3f} {team['as_percentage']:<8.1f}")

# Save to file
output = {
    'analysis_date': data['metadata']['generated_at'],
    'total_teams': len(explosiveness_data),
    'statistics': {
        'min': min(raw_values),
        'max': max(raw_values),
        'mean': statistics.mean(raw_values),
        'median': statistics.median(raw_values)
    },
    'benchmarks_raw': {
        'elite': elite_raw,
        'average': avg_raw,
        'below_avg': below_raw
    },
    'benchmarks_percentage': {
        'elite': round(elite_raw * 100, 1),
        'average': round(avg_raw * 100, 1),
        'below_avg': round(below_raw * 100, 1)
    },
    'rankings': explosiveness_data_sorted
}

with open('explosiveness_complete_rankings.json', 'w') as f:
    json.dump(output, f, indent=2)

print()
print("=" * 80)
print("✅ Complete rankings saved to: explosiveness_complete_rankings.json")
print("=" * 80)
