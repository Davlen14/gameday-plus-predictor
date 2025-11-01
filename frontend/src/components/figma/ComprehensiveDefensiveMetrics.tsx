import React from 'react';

interface DefensiveMetrics {
  fumbles_recovered_per_game: number;
  def_passing_downs_success: number;
  def_second_level_yards: number;
  tackles_for_loss_per_game: number;
  def_stuff_rate: number;
  defense_success_rate: number;
  def_rushing_success: number;
  sacks_per_game: number;
  def_passing_ppa: number;
  completion_pct_allowed: number;
  def_standard_downs_success: number;
  interceptions_per_game: number;
  def_points_per_opportunity: number;
  def_passing_downs_ppa: number;
  pass_td_allowed_rate: number;
  def_rushing_ppa: number;
  defense_havoc_db: number;
  opponent_penalty_yards_per_game: number;
  def_line_yards: number;
  defense_havoc_total: number;
  fourth_down_pct_allowed: number;
  def_open_field_yards: number;
  rush_td_allowed_rate: number;
  yards_allowed_per_game: number;
  kick_return_avg_allowed: number;
  def_passing_explosiveness: number;
  def_power_success: number;
  third_down_pct_allowed: number;
  yards_per_pass_allowed: number;
  def_standard_downs_ppa: number;
  yards_per_rush_allowed: number;
  defense_havoc_front_seven: number;
  def_rushing_explosiveness: number;
  yards_allowed_per_play: number;
  defense_ppa: number;
  takeaways_per_game: number;
  def_passing_success: number;
  sack_rate: number;
  defense_explosiveness: number;
  punt_return_avg_allowed: number;
}

interface TeamMetrics {
  normalized: DefensiveMetrics;
  raw: DefensiveMetrics;
}

interface ComprehensiveDefensiveMetricsProps {
  homeTeam: string;
  awayTeam: string;
  homeMetrics?: TeamMetrics;
  awayMetrics?: TeamMetrics;
}

const ComprehensiveDefensiveMetrics: React.FC<ComprehensiveDefensiveMetricsProps> = ({
  homeTeam,
  awayTeam,
  homeMetrics,
  awayMetrics,
}) => {
  if (!homeMetrics || !awayMetrics) {
    return (
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h3 className="text-xl font-bold text-white mb-4">Comprehensive Defensive Metrics</h3>
        <p className="text-gray-300">Metrics not available</p>
      </div>
    );
  }

  const metricLabels: { [key: string]: string } = {
    defense_ppa: 'Defense PPA',
    defense_success_rate: 'Success Rate',
    defense_explosiveness: 'Explosiveness',
    yards_allowed_per_play: 'Yards Allowed/Play',
    yards_allowed_per_game: 'Yards Allowed/Game',
    def_passing_success: 'Passing Success',
    def_rushing_success: 'Rushing Success',
    def_passing_ppa: 'Passing PPA',
    def_rushing_ppa: 'Rushing PPA',
    def_passing_explosiveness: 'Passing Explosiveness',
    def_rushing_explosiveness: 'Rushing Explosiveness',
    def_standard_downs_success: 'Standard Downs Success',
    def_passing_downs_success: 'Passing Downs Success',
    def_standard_downs_ppa: 'Standard Downs PPA',
    def_passing_downs_ppa: 'Passing Downs PPA',
    third_down_pct_allowed: 'Third Down % Allowed',
    fourth_down_pct_allowed: 'Fourth Down % Allowed',
    completion_pct_allowed: 'Completion % Allowed',
    yards_per_pass_allowed: 'Yards/Pass Allowed',
    yards_per_rush_allowed: 'Yards/Rush Allowed',
    pass_td_allowed_rate: 'Pass TD Rate Allowed',
    rush_td_allowed_rate: 'Rush TD Rate Allowed',
    interceptions_per_game: 'Interceptions/Game',
    fumbles_recovered_per_game: 'Fumbles Recovered/Game',
    takeaways_per_game: 'Takeaways/Game',
    sacks_per_game: 'Sacks/Game',
    sack_rate: 'Sack Rate',
    tackles_for_loss_per_game: 'Tackles for Loss/Game',
    def_points_per_opportunity: 'Points Allowed/Opportunity',
    def_line_yards: 'Line Yards Allowed',
    def_second_level_yards: 'Second Level Yards',
    def_open_field_yards: 'Open Field Yards',
    def_power_success: 'Power Success Allowed',
    def_stuff_rate: 'Stuff Rate',
    defense_havoc_total: 'Havoc Total',
    defense_havoc_front_seven: 'Havoc Front Seven',
    defense_havoc_db: 'Havoc DB',
    kick_return_avg_allowed: 'Kick Return Allowed',
    punt_return_avg_allowed: 'Punt Return Allowed',
    opponent_penalty_yards_per_game: 'Opp Penalty Yds/Game',
  };

  const calculateDifferential = (away: number, home: number): { value: number; advantage: 'away' | 'home' | 'even' } => {
    const diff = away - home;
    if (Math.abs(diff) < 0.01) return { value: diff, advantage: 'even' };
    // For defense, HIGHER normalized percentile = BETTER defense, so reverse advantage
    return { value: diff, advantage: diff > 0 ? 'away' : 'home' };
  };

  const renderMetricRow = (key: keyof DefensiveMetrics, label: string, showRaw: boolean = false) => {
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
            <div className={`flex-1 text-right ${diff.advantage === 'away' ? 'text-blue-400 font-semibold' : 'text-gray-300'}`}>
              <div className="text-sm sm:text-base font-bold">{formatValue(awayValue)}</div>
            </div>
            
            <div className="flex flex-col items-center min-w-[100px] sm:min-w-[120px] px-2">
              <div className={`text-base sm:text-lg font-bold px-2 sm:px-3 py-1 rounded-lg ${
                diff.advantage === 'away' 
                  ? 'bg-blue-500/20 text-blue-400' 
                  : diff.advantage === 'home'
                  ? 'bg-orange-500/20 text-orange-400'
                  : 'bg-gray-500/20 text-gray-400'
              }`}>
                {diff.advantage === 'away' && '+'}{formatValue(diff.value)}
              </div>
            </div>
            
            <div className={`flex-1 text-left ${diff.advantage === 'home' ? 'text-blue-400 font-semibold' : 'text-gray-300'}`}>
              <div className="text-sm sm:text-base font-bold">{formatValue(homeValue)}</div>
            </div>
          </div>
        </div>
        
        {/* Desktop Layout */}
        <div key={`${key}-desktop`} className="hidden md:grid grid-cols-[1fr_auto_1fr] items-center gap-4 py-3 border-b border-white/10">
          {/* Away Team */}
          <div className={`text-right ${diff.advantage === 'away' ? 'text-blue-400 font-semibold' : 'text-gray-300'}`}>
            {formatValue(awayValue)}
          </div>

          {/* Label & Differential */}
          <div className="flex flex-col items-center min-w-[220px]">
            <div className="text-xs text-gray-400 mb-1">{label}</div>
            <div className={`text-sm font-bold px-3 py-1 rounded-lg ${
              diff.advantage === 'away' 
                ? 'bg-blue-500/20 text-blue-400' 
                : diff.advantage === 'home'
                ? 'bg-orange-500/20 text-orange-400'
                : 'bg-gray-500/20 text-gray-400'
            }`}>
              {diff.advantage === 'away' && '+'}{formatValue(diff.value)}
            </div>
          </div>

          {/* Home Team */}
          <div className={`text-left ${diff.advantage === 'home' ? 'text-blue-400 font-semibold' : 'text-gray-300'}`}>
            {formatValue(homeValue)}
          </div>
        </div>
      </>
    );
  };

  return (
    <div className="bg-gradient-to-br from-red-900/30 to-orange-900/30 backdrop-blur-xl rounded-xl sm:rounded-2xl p-4 sm:p-6 md:p-8 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center mb-4 sm:mb-6 gap-2">
        <h3 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
          <span className="text-2xl sm:text-3xl">🛡️</span>
          <span className="hidden sm:inline">Comprehensive Defensive Metrics</span>
          <span className="sm:hidden">Defensive Metrics</span>
        </h3>
        <div className="text-xs sm:text-sm text-gray-400">
          40 Advanced Defensive Stats
        </div>
      </div>

      {/* Team Names */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-4 mb-4 pb-4 border-b-2 border-white/30">
        <div className="text-right">
          <div className="text-lg font-bold text-white">{awayTeam}</div>
          <div className="text-xs text-gray-400">Away</div>
        </div>
        <div className="text-center">
          <div className="text-xs text-gray-400">VS</div>
        </div>
        <div className="text-left">
          <div className="text-lg font-bold text-white">{homeTeam}</div>
          <div className="text-xs text-gray-400">Home</div>
        </div>
      </div>

      {/* Metrics Grid - Normalized (0-100 Percentile) */}
      <div className="mb-6">
        <div className="text-sm font-semibold text-red-300 mb-3 flex items-center gap-2">
          <span>📈</span> Normalized Percentile Scores (0-100)
        </div>
        <div className="space-y-1">
          {Object.keys(metricLabels).map((key) => 
            renderMetricRow(key as keyof DefensiveMetrics, metricLabels[key], false)
          )}
        </div>
      </div>

      {/* Metrics Grid - Raw Values */}
      <div>
        <div className="text-sm font-semibold text-orange-300 mb-3 flex items-center gap-2">
          <span>🔢</span> Raw Statistical Values
        </div>
        <div className="space-y-1">
          {Object.keys(metricLabels).map((key) => 
            renderMetricRow(key as keyof DefensiveMetrics, metricLabels[key], true)
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 pt-4 border-t border-white/20 flex justify-center gap-6 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500/20 border border-blue-400 rounded"></div>
          <span className="text-gray-400">Better Defense</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-gray-500/20 border border-gray-400 rounded"></div>
          <span className="text-gray-400">Even</span>
        </div>
      </div>
    </div>
  );
};

export default ComprehensiveDefensiveMetrics;
