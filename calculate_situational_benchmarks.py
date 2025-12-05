#!/usr/bin/env python3
"""
Calculate FBS National Benchmarks for Situational Performance Metrics
Analyzes comprehensive power rankings data to determine Elite, Average, and Below Average thresholds
Uses RAW (actual percentage) data, not normalized scores
"""

import json
import statistics

# Load the comprehensive power rankings data
with open('weekly_updates/week_15/comprehensive_power_rankings_20251203_053934.json', 'r') as f:
    data = json.load(f)

# Extract the metrics we need from all teams (using RAW data)
success_rates = []
explosiveness_rates = []
passing_downs_rates = []
standard_downs_rates = []

for team in data['rankings']:
    metrics = team['detailed_metrics']
    
    # Success Rate - offensive success rate (RAW percentage)
    if 'offense_success_rate' in metrics.get('offensive_raw', {}):
        success_rates.append(metrics['offensive_raw']['offense_success_rate'])
    
    # Explosiveness - offensive explosiveness (RAW value)
    if 'offense_explosiveness' in metrics.get('offensive_raw', {}):
        explosiveness_rates.append(metrics['offensive_raw']['offense_explosiveness'])
    
    # Passing Downs Success (RAW percentage)
    if 'passing_downs_success' in metrics.get('offensive_raw', {}):
        passing_downs_rates.append(metrics['offensive_raw']['passing_downs_success'])
    
    # Standard Downs Success (RAW percentage)
    if 'standard_downs_success' in metrics.get('offensive_raw', {}):
        standard_downs_rates.append(metrics['offensive_raw']['standard_downs_success'])

def calculate_percentiles(values, metric_name):
    """Calculate Elite (80th), Average (50th), and Below Avg (30th) percentiles"""
    values_sorted = sorted(values)
    n = len(values_sorted)
    
    # Calculate percentile indices
    elite_idx = int(n * 0.80)  # 80th percentile (top 20%)
    avg_idx = int(n * 0.50)    # 50th percentile (median)
    below_idx = int(n * 0.30)  # 30th percentile (bottom 70%)
    
    elite = values_sorted[elite_idx]
    average = values_sorted[avg_idx]
    below_avg = values_sorted[below_idx]
    
    print(f"\n{metric_name}:")
    print(f"  Teams analyzed: {n}")
    print(f"  Min: {min(values):.1f}")
    print(f"  Max: {max(values):.1f}")
    print(f"  Mean: {statistics.mean(values):.1f}")
    print(f"  ✅ Elite (80th percentile): {elite:.1f}")
    print(f"  📊 Average (50th percentile): {average:.1f}")
    print(f"  ⚠️  Below Avg (30th percentile): {below_avg:.1f}")
    
    return {
        'elite': round(elite, 1),
        'average': round(average, 1),
        'below_avg': round(below_avg, 1),
        'mean': round(statistics.mean(values), 1),
        'sample_size': n
    }

print("=" * 70)
print("FBS NATIONAL BENCHMARKS - 2025 SEASON (Week 15)")
print("=" * 70)
print(f"Based on {len(data['rankings'])} FBS teams")
print("=" * 70)

benchmarks = {}

# Calculate benchmarks for each metric
benchmarks['success_rate'] = calculate_percentiles(success_rates, "SUCCESS RATE")
benchmarks['explosiveness'] = calculate_percentiles(explosiveness_rates, "EXPLOSIVENESS")
benchmarks['passing_downs'] = calculate_percentiles(passing_downs_rates, "PASSING DOWNS SUCCESS")
benchmarks['standard_downs'] = calculate_percentiles(standard_downs_rates, "STANDARD DOWNS SUCCESS")

print("\n" + "=" * 70)
print("TYPESCRIPT CODE FOR FRONTEND:")
print("=" * 70)
print("""
const situationalPerformanceData = [
  {
    metric: "Success Rate",
    [awayAbbr]: 46.0,
    [homeAbbr]: 48.0,
    Elite: """ + str(benchmarks['success_rate']['elite']) + """,
    Average: """ + str(benchmarks['success_rate']['average']) + """,
    BelowAvg: """ + str(benchmarks['success_rate']['below_avg']) + """
  },
  {
    metric: "Explosiveness",
    [awayAbbr]: 15.0,
    [homeAbbr]: 13.0,
    Elite: """ + str(benchmarks['explosiveness']['elite']) + """,
    Average: """ + str(benchmarks['explosiveness']['average']) + """,
    BelowAvg: """ + str(benchmarks['explosiveness']['below_avg']) + """
  },
  {
    metric: "Passing Downs",
    [awayAbbr]: situationalPerformance.away_passing_downs,
    [homeAbbr]: situationalPerformance.home_passing_downs,
    Elite: """ + str(benchmarks['passing_downs']['elite']) + """,
    Average: """ + str(benchmarks['passing_downs']['average']) + """,
    BelowAvg: """ + str(benchmarks['passing_downs']['below_avg']) + """
  },
  {
    metric: "Standard Downs",
    [awayAbbr]: situationalPerformance.away_standard_downs,
    [homeAbbr]: situationalPerformance.home_standard_downs,
    Elite: """ + str(benchmarks['standard_downs']['elite']) + """,
    Average: """ + str(benchmarks['standard_downs']['average']) + """,
    BelowAvg: """ + str(benchmarks['standard_downs']['below_avg']) + """
  }
];
""")

# Save benchmarks to JSON for reference
output = {
    'generated_at': data['metadata']['generated_at'],
    'fbs_teams_analyzed': len(data['rankings']),
    'benchmarks': benchmarks,
    'methodology': {
        'elite': '80th percentile (top 20% of FBS)',
        'average': '50th percentile (median)',
        'below_avg': '30th percentile (bottom 70%)'
    }
}

with open('fbs_situational_benchmarks.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n✅ Benchmarks saved to: fbs_situational_benchmarks.json")
