import React, { useState } from 'react';
import { Info, ChevronDown, ChevronUp, ArrowRight, ArrowLeft } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';

interface ComprehensiveMetricsProps {
  predictionData?: any;
  powerRankingsData?: any;
}

interface MetricConfig {
  name: string;
  awayValue: number;
  homeValue: number;
  category: string;
  description: string;
  unit?: string;
}

const ComprehensiveMetricsDashboard: React.FC<ComprehensiveMetricsProps> = ({
  predictionData,
  powerRankingsData,
}) => {
  const [expandedMetric, setExpandedMetric] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<'overview' | 'offense' | 'defense'>('overview');

  if (!predictionData || !powerRankingsData) {
    return null;
  }

  const teamData = predictionData.team_selector;
  const away = teamData?.away_team;
  const home = teamData?.home_team;
  const awayColor = away?.primary_color || '#3B82F6';
  const homeColor = home?.primary_color || '#EF4444';

  const homeTeam = predictionData.home_team || home?.name || 'Home';
  const awayTeam = predictionData.away_team || away?.name || 'Away';

  // Find team data in power rankings
  const homeRankingData = powerRankingsData.rankings?.find(
    (team: any) => team.team === homeTeam
  );
  const awayRankingData = powerRankingsData.rankings?.find(
    (team: any) => team.team === awayTeam
  );

  if (!homeRankingData || !awayRankingData) {
    return (
      <GlassCard className="p-6 space-y-6">
        <h3 className="text-xl font-bold text-white">Comprehensive Power Rankings</h3>
        <p className="text-slate-400">Power rankings data not available for this matchup.</p>
      </GlassCard>
    );
  }

  // Helper function to calculate bar width
  const getBarWidth = (value: number, maxValue: number) => {
    return `${(value / maxValue) * 100}%`;
  };

  // Calculate difference with proper color
  const getDifference = (metric: MetricConfig) => {
    const diff = metric.homeValue - metric.awayValue;
    const absDiff = Math.abs(diff);
    const formatted = absDiff.toFixed(1);
    
    let color = 'text-cyan-400';
    if (diff > 0.5) color = `text-[${homeColor}]`;
    if (diff < -0.5) color = `text-[${awayColor}]`;
    
    const advantage = diff > 0.5 ? home?.abbreviation : diff < -0.5 ? away?.abbreviation : 'Even';
    
    return { formatted, color, advantage, diff };
  };

  // Build offensive metrics array (ALL 40 metrics)
  const offensiveMetrics: MetricConfig[] = [
    { name: 'Offensive EPA', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_ppa || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_ppa || 50, category: 'EPA', description: 'Expected Points Added per offensive play', unit: 'percentile' },
    { name: 'Success Rate', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_success_rate || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_success_rate || 50, category: 'Efficiency', description: 'Percentage of plays achieving positive EPA', unit: 'percentile' },
    { name: 'Explosiveness', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_explosiveness || 50, category: 'Big Plays', description: 'Frequency of explosive plays', unit: 'percentile' },
    { name: 'Yards Per Play', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.yards_per_play || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.yards_per_play || 50, category: 'Efficiency', description: 'Average yards per offensive play', unit: 'percentile' },
    { name: 'Yards Per Game', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.yards_per_game || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.yards_per_game || 50, category: 'Production', description: 'Total yards per game', unit: 'percentile' },
    { name: 'Third Down %', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.third_down_pct || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.third_down_pct || 50, category: 'Situational', description: 'Third down conversion rate', unit: 'percentile' },
    { name: 'Fourth Down %', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.fourth_down_pct || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.fourth_down_pct || 50, category: 'Situational', description: 'Fourth down conversion rate', unit: 'percentile' },
    { name: 'First Downs Per Game', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.first_downs_per_game || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.first_downs_per_game || 50, category: 'Production', description: 'First downs earned per game', unit: 'percentile' },
    { name: 'Points Per Opportunity', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.points_per_opportunity || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.points_per_opportunity || 50, category: 'Scoring', description: 'Red zone efficiency', unit: 'percentile' },
    { name: 'Passing Success', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.passing_success || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.passing_success || 50, category: 'Passing', description: 'Pass play success rate', unit: 'percentile' },
    { name: 'Passing EPA', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.passing_ppa || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.passing_ppa || 50, category: 'Passing', description: 'EPA per pass attempt', unit: 'percentile' },
    { name: 'Passing Explosiveness', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.passing_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.passing_explosiveness || 50, category: 'Passing', description: 'Big play frequency passing', unit: 'percentile' },
    { name: 'Completion %', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.completion_pct || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.completion_pct || 50, category: 'Passing', description: 'Pass completion percentage', unit: 'percentile' },
    { name: 'Yards Per Pass', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.yards_per_pass || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.yards_per_pass || 50, category: 'Passing', description: 'Average yards per pass attempt', unit: 'percentile' },
    { name: 'Pass TD Rate', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.pass_td_rate || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.pass_td_rate || 50, category: 'Passing', description: 'Passing touchdown rate', unit: 'percentile' },
    { name: 'Interception %', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.interception_pct || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.interception_pct || 50, category: 'Passing', description: 'Interception percentage (higher is better)', unit: 'percentile' },
    { name: 'Rushing Success', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.rushing_success || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.rushing_success || 50, category: 'Rushing', description: 'Rush play success rate', unit: 'percentile' },
    { name: 'Rushing EPA', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.rushing_ppa || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.rushing_ppa || 50, category: 'Rushing', description: 'EPA per rush attempt', unit: 'percentile' },
    { name: 'Rushing Explosiveness', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.rushing_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.rushing_explosiveness || 50, category: 'Rushing', description: 'Big play frequency rushing', unit: 'percentile' },
    { name: 'Yards Per Rush', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.yards_per_rush || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.yards_per_rush || 50, category: 'Rushing', description: 'Average yards per rush', unit: 'percentile' },
    { name: 'Rush TD Rate', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.rush_td_rate || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.rush_td_rate || 50, category: 'Rushing', description: 'Rushing touchdown rate', unit: 'percentile' },
    { name: 'Line Yards', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.line_yards || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.line_yards || 50, category: 'Line Play', description: 'Yards before contact', unit: 'percentile' },
    { name: 'Second Level Yards', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.second_level_yards || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.second_level_yards || 50, category: 'Line Play', description: 'Yards 5-10 yards downfield', unit: 'percentile' },
    { name: 'Open Field Yards', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.open_field_yards || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.open_field_yards || 50, category: 'Line Play', description: 'Yards beyond 10 yards', unit: 'percentile' },
    { name: 'Power Success', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.power_success || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.power_success || 50, category: 'Line Play', description: 'Success on power runs', unit: 'percentile' },
    { name: 'Stuff Rate', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.stuff_rate || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.stuff_rate || 50, category: 'Line Play', description: 'Rate of avoiding stuffs', unit: 'percentile' },
    { name: 'Standard Downs Success', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.standard_downs_success || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.standard_downs_success || 50, category: 'Situational', description: '1st & 2nd down success', unit: 'percentile' },
    { name: 'Standard Downs EPA', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.standard_downs_ppa || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.standard_downs_ppa || 50, category: 'Situational', description: 'EPA on standard downs', unit: 'percentile' },
    { name: 'Passing Downs Success', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.passing_downs_success || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.passing_downs_success || 50, category: 'Situational', description: 'Success on passing downs', unit: 'percentile' },
    { name: 'Passing Downs EPA', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.passing_downs_ppa || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.passing_downs_ppa || 50, category: 'Situational', description: 'EPA on passing downs', unit: 'percentile' },
    { name: 'Turnover Margin', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.turnover_margin || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.turnover_margin || 50, category: 'Turnovers', description: 'Turnover differential', unit: 'percentile' },
    { name: 'Possession Time %', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.possession_time_pct || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.possession_time_pct || 50, category: 'Control', description: 'Time of possession', unit: 'percentile' },
    { name: 'Avg Starting Field Position', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.avg_starting_field_position || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.avg_starting_field_position || 50, category: 'Field Position', description: 'Average drive start yardline', unit: 'percentile' },
    { name: 'Avg Predicted Points Start', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.avg_predicted_points_start || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.avg_predicted_points_start || 50, category: 'Field Position', description: 'Expected points at drive start', unit: 'percentile' },
    { name: 'Offense Havoc Total', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_total || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_total || 50, category: 'Havoc Created', description: 'Total havoc created', unit: 'percentile' },
    { name: 'Offense Havoc Front Seven', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_front_seven || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_front_seven || 50, category: 'Havoc Created', description: 'Havoc vs front seven', unit: 'percentile' },
    { name: 'Offense Havoc DB', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_db || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.offense_havoc_db || 50, category: 'Havoc Created', description: 'Havoc vs defensive backs', unit: 'percentile' },
    { name: 'Kick Return Avg', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.kick_return_avg || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.kick_return_avg || 50, category: 'Special Teams', description: 'Kickoff return average', unit: 'percentile' },
    { name: 'Punt Return Avg', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.punt_return_avg || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.punt_return_avg || 50, category: 'Special Teams', description: 'Punt return average', unit: 'percentile' },
    { name: 'Penalty Yards Per Game', awayValue: awayRankingData.detailed_metrics?.offensive_normalized?.penalty_yards_per_game || 50, homeValue: homeRankingData.detailed_metrics?.offensive_normalized?.penalty_yards_per_game || 50, category: 'Discipline', description: 'Penalty yards committed', unit: 'percentile' }
  ];

  // Build defensive metrics array (ALL 40 metrics)
  const defensiveMetrics: MetricConfig[] = [
    { name: 'Defensive EPA', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_ppa || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_ppa || 50, category: 'EPA', description: 'EPA allowed per play', unit: 'percentile' },
    { name: 'Success Rate Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_success_rate || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_success_rate || 50, category: 'Efficiency', description: 'Opponent success rate', unit: 'percentile' },
    { name: 'Explosiveness Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_explosiveness || 50, category: 'Big Plays', description: 'Opponent explosive plays', unit: 'percentile' },
    { name: 'Yards Per Play Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.yards_allowed_per_play || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.yards_allowed_per_play || 50, category: 'Efficiency', description: 'Yards allowed per play', unit: 'percentile' },
    { name: 'Yards Allowed Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.yards_allowed_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.yards_allowed_per_game || 50, category: 'Production', description: 'Total yards allowed per game', unit: 'percentile' },
    { name: 'Third Down % Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.third_down_pct_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.third_down_pct_allowed || 50, category: 'Situational', description: 'Third down conversion allowed', unit: 'percentile' },
    { name: 'Fourth Down % Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.fourth_down_pct_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.fourth_down_pct_allowed || 50, category: 'Situational', description: 'Fourth down conversion allowed', unit: 'percentile' },
    { name: 'Points Per Opportunity Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_points_per_opportunity || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_points_per_opportunity || 50, category: 'Scoring', description: 'Red zone defense', unit: 'percentile' },
    { name: 'Passing Success Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_passing_success || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_passing_success || 50, category: 'Pass Defense', description: 'Pass success rate allowed', unit: 'percentile' },
    { name: 'Passing EPA Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_passing_ppa || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_passing_ppa || 50, category: 'Pass Defense', description: 'EPA per pass allowed', unit: 'percentile' },
    { name: 'Passing Explosiveness Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_passing_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_passing_explosiveness || 50, category: 'Pass Defense', description: 'Big pass plays allowed', unit: 'percentile' },
    { name: 'Completion % Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.completion_pct_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.completion_pct_allowed || 50, category: 'Pass Defense', description: 'Pass completion % allowed', unit: 'percentile' },
    { name: 'Yards Per Pass Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.yards_per_pass_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.yards_per_pass_allowed || 50, category: 'Pass Defense', description: 'Yards per pass allowed', unit: 'percentile' },
    { name: 'Pass TD Rate Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.pass_td_allowed_rate || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.pass_td_allowed_rate || 50, category: 'Pass Defense', description: 'Passing TDs allowed rate', unit: 'percentile' },
    { name: 'Interceptions Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.interceptions_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.interceptions_per_game || 50, category: 'Turnovers', description: 'Interceptions per game', unit: 'percentile' },
    { name: 'Rushing Success Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_rushing_success || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_rushing_success || 50, category: 'Run Defense', description: 'Rush success rate allowed', unit: 'percentile' },
    { name: 'Rushing EPA Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_rushing_ppa || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_rushing_ppa || 50, category: 'Run Defense', description: 'EPA per rush allowed', unit: 'percentile' },
    { name: 'Rushing Explosiveness Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_rushing_explosiveness || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_rushing_explosiveness || 50, category: 'Run Defense', description: 'Big rush plays allowed', unit: 'percentile' },
    { name: 'Yards Per Rush Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.yards_per_rush_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.yards_per_rush_allowed || 50, category: 'Run Defense', description: 'Yards per rush allowed', unit: 'percentile' },
    { name: 'Rush TD Rate Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.rush_td_allowed_rate || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.rush_td_allowed_rate || 50, category: 'Run Defense', description: 'Rushing TDs allowed rate', unit: 'percentile' },
    { name: 'Line Yards Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_line_yards || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_line_yards || 50, category: 'Line Play', description: 'Yards before contact allowed', unit: 'percentile' },
    { name: 'Second Level Yards Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_second_level_yards || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_second_level_yards || 50, category: 'Line Play', description: 'Yards 5-10 downfield allowed', unit: 'percentile' },
    { name: 'Open Field Yards Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_open_field_yards || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_open_field_yards || 50, category: 'Line Play', description: 'Yards beyond 10 allowed', unit: 'percentile' },
    { name: 'Power Success Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_power_success || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_power_success || 50, category: 'Line Play', description: 'Power run success allowed', unit: 'percentile' },
    { name: 'Stuff Rate', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_stuff_rate || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_stuff_rate || 50, category: 'Line Play', description: 'Rate of stuffing runs', unit: 'percentile' },
    { name: 'Standard Downs Success Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_standard_downs_success || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_standard_downs_success || 50, category: 'Situational', description: '1st & 2nd down defense', unit: 'percentile' },
    { name: 'Standard Downs EPA Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_standard_downs_ppa || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_standard_downs_ppa || 50, category: 'Situational', description: 'EPA on standard downs', unit: 'percentile' },
    { name: 'Passing Downs Success Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_passing_downs_success || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_passing_downs_success || 50, category: 'Situational', description: 'Passing downs defense', unit: 'percentile' },
    { name: 'Passing Downs EPA Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.def_passing_downs_ppa || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.def_passing_downs_ppa || 50, category: 'Situational', description: 'EPA on passing downs', unit: 'percentile' },
    { name: 'Fumbles Recovered Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.fumbles_recovered_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.fumbles_recovered_per_game || 50, category: 'Turnovers', description: 'Fumble recoveries per game', unit: 'percentile' },
    { name: 'Takeaways Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.takeaways_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.takeaways_per_game || 50, category: 'Turnovers', description: 'Total takeaways per game', unit: 'percentile' },
    { name: 'Sacks Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.sacks_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.sacks_per_game || 50, category: 'Pressure', description: 'Sacks per game', unit: 'percentile' },
    { name: 'Sack Rate', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.sack_rate || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.sack_rate || 50, category: 'Pressure', description: 'Sack percentage', unit: 'percentile' },
    { name: 'Tackles For Loss Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.tackles_for_loss_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.tackles_for_loss_per_game || 50, category: 'Pressure', description: 'TFLs per game', unit: 'percentile' },
    { name: 'Defense Havoc Total', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_total || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_total || 50, category: 'Havoc', description: 'Total havoc created', unit: 'percentile' },
    { name: 'Defense Havoc Front Seven', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_front_seven || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_front_seven || 50, category: 'Havoc', description: 'Front seven havoc', unit: 'percentile' },
    { name: 'Defense Havoc DB', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_db || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.defense_havoc_db || 50, category: 'Havoc', description: 'Defensive back havoc', unit: 'percentile' },
    { name: 'Kick Return Avg Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.kick_return_avg_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.kick_return_avg_allowed || 50, category: 'Special Teams', description: 'Kickoff return average allowed', unit: 'percentile' },
    { name: 'Punt Return Avg Allowed', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.punt_return_avg_allowed || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.punt_return_avg_allowed || 50, category: 'Special Teams', description: 'Punt return average allowed', unit: 'percentile' },
    { name: 'Opponent Penalty Yards Per Game', awayValue: awayRankingData.detailed_metrics?.defensive_normalized?.opponent_penalty_yards_per_game || 50, homeValue: homeRankingData.detailed_metrics?.defensive_normalized?.opponent_penalty_yards_per_game || 50, category: 'Discipline', description: 'Opponent penalty yards drawn', unit: 'percentile' }
  ];

  // Overview metrics (composite scores)
  const overviewMetrics: MetricConfig[] = [
    {
      name: 'Overall Power Score',
      awayValue: awayRankingData.overall_score || 50,
      homeValue: homeRankingData.overall_score || 50,
      category: 'Composite',
      description: 'Comprehensive power rating combining all 167 offensive and defensive metrics.',
      unit: 'score'
    },
    {
      name: 'Offensive Power Score',
      awayValue: awayRankingData.offensive_score || 50,
      homeValue: homeRankingData.offensive_score || 50,
      category: 'Composite',
      description: 'Aggregate offensive rating across 40+ metrics including EPA, success rates, and explosiveness.',
      unit: 'score'
    },
    {
      name: 'Defensive Power Score',
      awayValue: awayRankingData.defensive_score || 50,
      homeValue: homeRankingData.defensive_score || 50,
      category: 'Composite',
      description: 'Aggregate defensive rating across 40+ metrics including havoc rates and opponent efficiency.',
      unit: 'score'
    },
    {
      name: 'National Rank',
      awayValue: 131 - (awayRankingData.rank || 65),  // Invert so higher is better
      homeValue: 131 - (homeRankingData.rank || 65),
      category: 'Ranking',
      description: 'Overall national ranking based on comprehensive power ratings. Out of 130 FBS teams.',
      unit: 'rank'
    }
  ];

  const renderMetricSection = (metrics: MetricConfig[], sectionTitle: string, sectionColor: string) => {
    return (
      <div className="space-y-4">
        <div className="flex items-center gap-2 pb-2">
          <div className="w-1 h-5 rounded-full" style={{ backgroundColor: sectionColor }} />
          <h3 className="text-white">{sectionTitle}</h3>
        </div>

        <div className="space-y-3">
          {metrics.map((metric) => {
            const diff = getDifference(metric);
            const isExpanded = expandedMetric === metric.name;
            const maxValue = Math.max(metric.homeValue, metric.awayValue);

            return (
              <div key={metric.name} className="space-y-0">
                <div 
                  className="bg-gray-800/40 backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-gray-800/60"
                  onClick={() => setExpandedMetric(isExpanded ? null : metric.name)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: awayColor,
                          textShadow: `0 0 10px ${awayColor}40`
                        }}
                      >
                        {metric.awayValue.toFixed(1)}
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.awayValue, maxValue),
                          background: `linear-gradient(to right, ${awayColor}80, ${awayColor})`,
                          boxShadow: `0 0 12px ${awayColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff.diff < -0.5 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{metric.name}</span>
                        {diff.diff > 0.5 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className={`analytical-number text-sm ${diff.color}`}
                        style={{ textShadow: `0 0 8px ${diff.diff > 0 ? homeColor : awayColor}40` }}
                      >
                        {diff.advantage} +{diff.formatted}
                      </div>
                      <span className="text-xs text-slate-500">{metric.category}</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: homeColor,
                          textShadow: `0 0 10px ${homeColor}40`
                        }}
                      >
                        {metric.homeValue.toFixed(1)}
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.homeValue, maxValue),
                          background: `linear-gradient(to left, ${homeColor}80, ${homeColor})`,
                          boxShadow: `0 0 12px ${homeColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10 bg-gray-900/50 backdrop-blur-sm rounded-b-lg px-4 pb-4">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {metric.description}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <GlassCard className="p-6 space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between pb-4 border-b border-white/10">
        {/* Away Team (Left) */}
        <div className="flex items-center gap-3">
          <ImageWithFallback 
            src={away?.logo || ''}
            alt={away?.name || 'Away Team'}
            className="w-12 h-12 object-contain"
          />
          <div>
            <div className="text-white" style={{ fontSize: '1.125rem' }}>
              {away?.name || 'Away Team'}
            </div>
            <div className="text-sm text-slate-400">
              {away?.mascot || 'Team'}
            </div>
          </div>
        </div>

        {/* Center Badge */}
        <div className="flex flex-col items-center">
          <div className="text-slate-500 text-xs uppercase tracking-wider mb-1">
            Power Rankings
          </div>
          <div className="px-3 py-1 rounded-full glass-card-light border border-cyan-500/30 text-cyan-400 text-xs"
               style={{ textShadow: '0 0 10px rgba(34, 211, 238, 0.3)' }}>
            167 Advanced Metrics
          </div>
        </div>

        {/* Home Team (Right) */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-white" style={{ fontSize: '1.125rem' }}>
              {home?.name || 'Home Team'}
            </div>
            <div className="text-sm text-slate-400">
              {home?.mascot || 'Team'}
            </div>
          </div>
          <ImageWithFallback 
            src={home?.logo || ''}
            alt={home?.name || 'Home Team'}
            className="w-12 h-12 object-contain"
          />
        </div>
      </div>

      {/* Section Navigation */}
      <div className="flex gap-2 sm:gap-3 border-b border-white/10 pb-3 sm:pb-4 overflow-x-auto scrollbar-hide">
        <button
          onClick={() => setActiveSection('overview')}
          className={`px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-xl font-semibold transition-all duration-300 backdrop-blur-xl border whitespace-nowrap flex-shrink-0 text-sm sm:text-base ${
            activeSection === 'overview'
              ? 'bg-white/20 text-white border-white/30 shadow-[0_8px_32px_0_rgba(255,255,255,0.1)] scale-105'
              : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10 hover:border-white/20 shadow-[0_4px_16px_0_rgba(0,0,0,0.3)]'
          }`}
          style={{
            boxShadow: activeSection === 'overview' 
              ? '0 8px 32px 0 rgba(255, 255, 255, 0.15), inset 0 2px 4px 0 rgba(255, 255, 255, 0.1)' 
              : '0 4px 16px 0 rgba(0, 0, 0, 0.4), inset 0 1px 2px 0 rgba(255, 255, 255, 0.05)'
          }}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveSection('offense')}
          className={`px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-xl font-semibold transition-all duration-300 backdrop-blur-xl border whitespace-nowrap flex-shrink-0 text-sm sm:text-base ${
            activeSection === 'offense'
              ? 'bg-white/20 text-white border-white/30 shadow-[0_8px_32px_0_rgba(255,255,255,0.1)] scale-105'
              : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10 hover:border-white/20 shadow-[0_4px_16px_0_rgba(0,0,0,0.3)]'
          }`}
          style={{
            boxShadow: activeSection === 'offense'
              ? '0 8px 32px 0 rgba(255, 255, 255, 0.15), inset 0 2px 4px 0 rgba(255, 255, 255, 0.1)' 
              : '0 4px 16px 0 rgba(0, 0, 0, 0.4), inset 0 1px 2px 0 rgba(255, 255, 255, 0.05)'
          }}
        >
          <span className="hidden sm:inline">Offensive Metrics</span>
          <span className="sm:hidden">Offense</span>
        </button>
        <button
          onClick={() => setActiveSection('defense')}
          className={`px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-xl font-semibold transition-all duration-300 backdrop-blur-xl border whitespace-nowrap flex-shrink-0 text-sm sm:text-base ${
            activeSection === 'defense'
              ? 'bg-white/20 text-white border-white/30 shadow-[0_8px_32px_0_rgba(255,255,255,0.1)] scale-105'
              : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10 hover:border-white/20 shadow-[0_4px_16px_0_rgba(0,0,0,0.3)]'
          }`}
          style={{
            boxShadow: activeSection === 'defense'
              ? '0 8px 32px 0 rgba(255, 255, 255, 0.15), inset 0 2px 4px 0 rgba(255, 255, 255, 0.1)' 
              : '0 4px 16px 0 rgba(0, 0, 0, 0.4), inset 0 1px 2px 0 rgba(255, 255, 255, 0.05)'
          }}
        >
          <span className="hidden sm:inline">Defensive Metrics</span>
          <span className="sm:hidden">Defense</span>
        </button>
      </div>

      {/* Overview Section */}
      {activeSection === 'overview' && renderMetricSection(overviewMetrics, 'Composite Power Ratings', homeColor)}

      {/* Offensive Section */}
      {activeSection === 'offense' && renderMetricSection(offensiveMetrics, 'Top Offensive Metrics', '#10b981')}

      {/* Defensive Section */}
      {activeSection === 'defense' && renderMetricSection(defensiveMetrics, 'Top Defensive Metrics', '#ef4444')}

      {/* Legend */}
      <div className="pt-4 border-t border-white/10 flex items-center justify-center gap-6 text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: awayColor }} />
          <span>{away?.abbreviation} Advantage</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: homeColor }} />
          <span>{home?.abbreviation} Advantage</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-cyan-400" />
          <span>Even Matchup</span>
        </div>
      </div>
    </GlassCard>
  );
};

export default ComprehensiveMetricsDashboard;