import React from 'react';

interface OffensiveMetrics {
  offense_havoc_front_seven: number;
  passing_success: number;
  third_down_pct: number;
  fourth_down_pct: number;
  offense_ppa: number;
  line_yards: number;
  yards_per_play: number;
  rushing_success: number;
  standard_downs_success: number;
  rushing_ppa: number;
  offense_havoc_db: number;
  turnover_margin: number;
  avg_starting_field_position: number;
  offense_explosiveness: number;
  punt_return_avg: number;
  standard_downs_ppa: number;
  yards_per_game: number;
  passing_downs_success: number;
  points_per_opportunity: number;
  avg_predicted_points_start: number;
  offense_success_rate: number;
  yards_per_pass: number;
  interception_pct: number;
  rushing_explosiveness: number;
  offense_havoc_total: number;
  rush_td_rate: number;
  first_downs_per_game: number;
  pass_td_rate: number;
  stuff_rate: number;
  second_level_yards: number;
  power_success: number;
  passing_explosiveness: number;
  penalty_yards_per_game: number;
  completion_pct: number;
  passing_downs_ppa: number;
  possession_time_pct: number;
  yards_per_rush: number;
  kick_return_avg: number;
  passing_ppa: number;
  open_field_yards: number;
}

interface TeamMetrics {
  normalized: OffensiveMetrics;
  raw: OffensiveMetrics;
}

interface ComprehensiveOffensiveMetricsProps {
  homeTeam: string;
  awayTeam: string;
  homeMetrics?: TeamMetrics;
  awayMetrics?: TeamMetrics;
}

const ComprehensiveOffensiveMetrics: React.FC<ComprehensiveOffensiveMetricsProps> = ({
  homeTeam,
  awayTeam,
  homeMetrics,
  awayMetrics,
}) => {
  if (!homeMetrics || !awayMetrics) {
    return (
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h3 className="text-xl font-bold text-white mb-4">Comprehensive Offensive Metrics</h3>
        <p className="text-gray-300">Metrics not available</p>
      </div>
    );
  }

  const metricLabels: { [key: string]: string } = {
    offense_ppa: 'Offense PPA',
    offense_success_rate: 'Success Rate',
    offense_explosiveness: 'Explosiveness',
    yards_per_play: 'Yards Per Play',
    yards_per_game: 'Yards Per Game',
    passing_success: 'Passing Success',
    rushing_success: 'Rushing Success',
    passing_ppa: 'Passing PPA',
    rushing_ppa: 'Rushing PPA',
    passing_explosiveness: 'Passing Explosiveness',
    rushing_explosiveness: 'Rushing Explosiveness',
    standard_downs_success: 'Standard Downs Success',
    passing_downs_success: 'Passing Downs Success',
    standard_downs_ppa: 'Standard Downs PPA',
    passing_downs_ppa: 'Passing Downs PPA',
    third_down_pct: 'Third Down %',
    fourth_down_pct: 'Fourth Down %',
    completion_pct: 'Completion %',
    yards_per_pass: 'Yards Per Pass',
    yards_per_rush: 'Yards Per Rush',
    pass_td_rate: 'Pass TD Rate',
    rush_td_rate: 'Rush TD Rate',
    interception_pct: 'Interception %',
    first_downs_per_game: 'First Downs/Game',
    points_per_opportunity: 'Points Per Opportunity',
    turnover_margin: 'Turnover Margin',
    possession_time_pct: 'Possession Time %',
    line_yards: 'Line Yards',
    second_level_yards: 'Second Level Yards',
    open_field_yards: 'Open Field Yards',
    power_success: 'Power Success',
    stuff_rate: 'Stuff Rate',
    avg_starting_field_position: 'Avg Starting Position',
    avg_predicted_points_start: 'Avg Predicted Points',
    offense_havoc_total: 'Havoc Total',
    offense_havoc_front_seven: 'Havoc Front Seven',
    offense_havoc_db: 'Havoc DB',
    kick_return_avg: 'Kick Return Avg',
    punt_return_avg: 'Punt Return Avg',
    penalty_yards_per_game: 'Penalty Yards/Game',
  };

  const calculateDifferential = (away: number, home: number): { value: number; advantage: 'away' | 'home' | 'even' } => {
    const diff = away - home;
    if (Math.abs(diff) < 0.01) return { value: diff, advantage: 'even' };
    return { value: diff, advantage: diff > 0 ? 'away' : 'home' };
  };

  const renderMetricRow = (key: keyof OffensiveMetrics, label: string, showRaw: boolean = false) => {
    const awayValue = showRaw ? awayMetrics.raw[key] : awayMetrics.normalized[key];
    const homeValue = showRaw ? homeMetrics.raw[key] : homeMetrics.normalized[key];
    const diff = calculateDifferential(awayValue, homeValue);
    
    const formatValue = (val: number) => {
      if (showRaw) {
        if (key.includes('pct') || key.includes('success') || key.includes('rate')) {
          return val.toFixed(1) + '%';
        }
        return val.toFixed(2);
      }
      return val.toFixed(1);
    };

    return (
      <>
        {/* Mobile Layout */}
        <div key={`${key}-mobile`} className="md:hidden space-y-3 py-3 border-b border-white/10">
          <div className="text-center text-xs font-semibold text-slate-300 uppercase tracking-wider">
            {label}
          </div>
          
          <div className="flex justify-between items-center gap-2">
            <div className={`flex-1 text-right ${diff.advantage === 'away' ? 'text-green-400 font-semibold' : 'text-gray-300'}`}>
              <div className="text-sm sm:text-base font-bold">{formatValue(awayValue)}</div>
            </div>
            
            <div className="flex flex-col items-center min-w-[100px] sm:min-w-[120px] px-2">
              <div className={`text-base sm:text-lg font-bold px-2 sm:px-3 py-1 rounded-lg ${
                diff.advantage === 'away' 
                  ? 'bg-green-500/20 text-green-400' 
                  : diff.advantage === 'home'
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-gray-500/20 text-gray-400'
              }`}>
                {diff.advantage === 'away' && '+'}{formatValue(diff.value)}
              </div>
            </div>
            
            <div className={`flex-1 text-left ${diff.advantage === 'home' ? 'text-green-400 font-semibold' : 'text-gray-300'}`}>
              <div className="text-sm sm:text-base font-bold">{formatValue(homeValue)}</div>
            </div>
          </div>
        </div>
        
        {/* Desktop Layout */}
        <div key={`${key}-desktop`} className="hidden md:grid grid-cols-[1fr_auto_1fr] items-center gap-4 py-3 border-b border-white/10">
          {/* Away Team */}
          <div className={`text-right ${diff.advantage === 'away' ? 'text-green-400 font-semibold' : 'text-gray-300'}`}>
            {formatValue(awayValue)}
          </div>

          {/* Label & Differential */}
          <div className="flex flex-col items-center min-w-[200px]">
            <div className="text-xs text-gray-400 mb-1">{label}</div>
            <div className={`text-sm font-bold px-3 py-1 rounded-lg ${
              diff.advantage === 'away' 
                ? 'bg-green-500/20 text-green-400' 
                : diff.advantage === 'home'
                ? 'bg-red-500/20 text-red-400'
                : 'bg-gray-500/20 text-gray-400'
            }`}>
              {diff.advantage === 'away' && '+'}{formatValue(diff.value)}
            </div>
          </div>

          {/* Home Team */}
          <div className={`text-left ${diff.advantage === 'home' ? 'text-green-400 font-semibold' : 'text-gray-300'}`}>
            {formatValue(homeValue)}
          </div>
        </div>
      </>
    );
  };

  return (
    <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-xl rounded-xl sm:rounded-2xl p-4 sm:p-6 md:p-8 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center mb-4 sm:mb-6 gap-2">
        <h3 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
          <span className="text-2xl sm:text-3xl">📊</span>
          <span className="hidden sm:inline">Comprehensive Offensive Metrics</span>
          <span className="sm:hidden">Offensive Metrics</span>
        </h3>
        <div className="text-xs sm:text-sm text-gray-400">
          40 Advanced Offensive Stats
        </div>
      </div>

      {/* Team Names */}
            {/* Team Names */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 sm:gap-4 mb-4 pb-4 border-b-2 border-white/30">
        <div className="text-right">
          <div className="text-base sm:text-lg font-bold text-white truncate">{awayTeam}</div>
          <div className="text-xs sm:text-sm font-semibold text-purple-300 mb-3 flex items-center justify-end gap-2">
            <span className="hidden sm:inline">Away Team</span>
            <span className="sm:hidden">Away</span>
          </div>
        </div>
        
        <div className="text-center min-w-[80px] sm:min-w-[120px] md:min-w-[160px]">
          <div className="text-xs sm:text-sm font-semibold text-slate-300 uppercase tracking-wider">
            VS
          </div>
        </div>
        
        <div className="text-left">
          <div className="text-base sm:text-lg font-bold text-white truncate">{homeTeam}</div>
          <div className="text-xs sm:text-sm font-semibold text-blue-300 mb-3 flex items-center gap-2">
            <span className="hidden sm:inline">Home Team</span>
            <span className="sm:hidden">Home</span>
          </div>
        </div>
      </div>

      {/* Metrics Grid - Normalized (0-100 Percentile) */}
      <div className="mb-6">
        <div className="text-sm font-semibold text-purple-300 mb-3 flex items-center gap-2">
          <span>📈</span> Normalized Percentile Scores (0-100)
        </div>
        <div className="space-y-1">
          {Object.keys(metricLabels).map((key) => 
            renderMetricRow(key as keyof OffensiveMetrics, metricLabels[key], false)
          )}
        </div>
      </div>

      {/* Metrics Grid - Raw Values */}
      <div>
        <div className="text-sm font-semibold text-blue-300 mb-3 flex items-center gap-2">
          <span>🔢</span> Raw Statistical Values
        </div>
        <div className="space-y-1">
          {Object.keys(metricLabels).map((key) => 
            renderMetricRow(key as keyof OffensiveMetrics, metricLabels[key], true)
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 pt-4 border-t border-white/20 flex justify-center gap-6 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500/20 border border-green-400 rounded"></div>
          <span className="text-gray-400">Better Performance</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-gray-500/20 border border-gray-400 rounded"></div>
          <span className="text-gray-400">Even</span>
        </div>
      </div>
    </div>
  );
};

export default ComprehensiveOffensiveMetrics;
