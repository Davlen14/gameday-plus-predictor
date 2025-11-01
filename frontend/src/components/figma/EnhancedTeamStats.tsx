import { GlassCard } from './GlassCard';
import { BarChart3, TrendingUp, Zap, Target, Clock, Trophy, AlertCircle, Timer, Gauge, Flag } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr } from '../../utils/teamUtils';

interface EnhancedTeamStatsProps {
  predictionData?: any;
}

export function EnhancedTeamStats({ predictionData }: EnhancedTeamStatsProps) {
  if (!predictionData?.comprehensive_stats) {
    return null;
  }

  const awayTeam = predictionData.team_selector?.away_team;
  const homeTeam = predictionData.team_selector?.home_team;
  const awayStats = predictionData.comprehensive_stats?.away;
  const homeStats = predictionData.comprehensive_stats?.home;
  const driveData = predictionData.drive_efficiency;

  if (!awayTeam || !homeTeam || !awayStats || !homeStats) {
    return null;
  }

  const awayAbbr = generateTeamAbbr(awayTeam.name);
  const homeAbbr = generateTeamAbbr(homeTeam.name);

  // Helper function to determine advantage
  const getAdvantage = (awayVal: number, homeVal: number, higherIsBetter: boolean = true) => {
    if (awayVal === homeVal) return 'Tied';
    if (higherIsBetter) {
      return awayVal > homeVal ? 'Away' : 'Home';
    } else {
      return awayVal < homeVal ? 'Away' : 'Home';
    }
  };

  // Stat Row Component
  const StatRow = ({ 
    label, 
    awayValue, 
    homeValue, 
    advantage, 
    format = 'number'
  }: { 
    label: string; 
    awayValue: number | string; 
    homeValue: number | string; 
    advantage: string;
    format?: 'number' | 'percent' | 'time' | 'decimal';
  }) => {
    const formatValue = (val: number | string) => {
      if (typeof val === 'string') return val;
      switch (format) {
        case 'percent':
          return `${val}%`;
        case 'decimal':
          return val.toFixed(2);
        case 'time':
          return val.toFixed(1);
        default:
          return val.toLocaleString();
      }
    };

    return (
      <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
        <td className="py-3 px-4 text-gray-300 text-sm">{label}</td>
        <td className="py-3 px-4 text-right">
          <span className="font-mono font-semibold" style={{ color: awayTeam.primary_color }}>
            {formatValue(awayValue)}
          </span>
        </td>
        <td className="py-3 px-4 text-right">
          <span className="font-mono font-semibold" style={{ color: homeTeam.primary_color }}>
            {formatValue(homeValue)}
          </span>
        </td>
        <td className="py-3 px-4 text-center">
          {advantage !== 'Tied' && (
            <span 
              className="text-xs font-bold px-2 py-1 rounded-full"
              style={{
                backgroundColor: `${advantage === 'Away' ? awayTeam.primary_color : homeTeam.primary_color}20`,
                color: advantage === 'Away' ? awayTeam.primary_color : homeTeam.primary_color
              }}
            >
              {advantage === 'Away' ? awayAbbr : homeAbbr}
            </span>
          )}
        </td>
      </tr>
    );
  };

  return (
    <>
      {/* BASIC OFFENSIVE STATISTICS */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          <h3 className="text-white font-semibold">Basic Offensive Statistics</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-gray-400 text-sm font-semibold">Metric</th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-5 h-5" />
                    <span style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
                  </div>
                </th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-5 h-5" />
                    <span style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-400 text-sm font-semibold">Advantage</th>
              </tr>
            </thead>
            <tbody>
              <StatRow 
                label="Total Yards" 
                awayValue={awayStats.total_yards || 0} 
                homeValue={homeStats.total_yards || 0} 
                advantage={getAdvantage(awayStats.total_yards, homeStats.total_yards)}
              />
              <StatRow 
                label="Rushing Yards" 
                awayValue={awayStats.rushing_yards || 0} 
                homeValue={homeStats.rushing_yards || 0} 
                advantage={getAdvantage(awayStats.rushing_yards, homeStats.rushing_yards)}
              />
              <StatRow 
                label="Passing Yards" 
                awayValue={awayStats.passing_yards || 0} 
                homeValue={homeStats.passing_yards || 0} 
                advantage={getAdvantage(awayStats.passing_yards, homeStats.passing_yards)}
              />
              <StatRow 
                label="First Downs" 
                awayValue={awayStats.first_downs || 0} 
                homeValue={homeStats.first_downs || 0} 
                advantage={getAdvantage(awayStats.first_downs, homeStats.first_downs)}
              />
              <StatRow 
                label="Rushing TDs" 
                awayValue={awayStats.rushing_tds || 0} 
                homeValue={homeStats.rushing_tds || 0} 
                advantage={getAdvantage(awayStats.rushing_tds, homeStats.rushing_tds)}
              />
              <StatRow 
                label="Passing TDs" 
                awayValue={awayStats.passing_tds || 0} 
                homeValue={homeStats.passing_tds || 0} 
                advantage={getAdvantage(awayStats.passing_tds, homeStats.passing_tds)}
              />
              <StatRow 
                label="Rush Attempts" 
                awayValue={awayStats.rush_attempts || 0} 
                homeValue={homeStats.rush_attempts || 0} 
                advantage={getAdvantage(awayStats.rush_attempts, homeStats.rush_attempts)}
              />
              <StatRow 
                label="Pass Attempts" 
                awayValue={awayStats.pass_attempts || 0} 
                homeValue={homeStats.pass_attempts || 0} 
                advantage={getAdvantage(awayStats.pass_attempts, homeStats.pass_attempts)}
              />
              <StatRow 
                label="Pass Completions" 
                awayValue={awayStats.pass_completions || 0} 
                homeValue={homeStats.pass_completions || 0} 
                advantage={getAdvantage(awayStats.pass_completions, homeStats.pass_completions)}
              />
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* OFFENSIVE EFFICIENCY & SITUATIONAL */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Target className="w-5 h-5 text-green-400" />
          <h3 className="text-white font-semibold">Offensive Efficiency & Situational Performance</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-gray-400 text-sm font-semibold">Metric</th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-5 h-5" />
                    <span style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
                  </div>
                </th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-5 h-5" />
                    <span style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-400 text-sm font-semibold">Advantage</th>
              </tr>
            </thead>
            <tbody>
              <StatRow 
                label="Third Down %" 
                awayValue={awayStats.third_down_pct || 0} 
                homeValue={homeStats.third_down_pct || 0} 
                advantage={getAdvantage(awayStats.third_down_pct, homeStats.third_down_pct)}
                format="percent"
              />
              <StatRow 
                label="Points Per Opportunity" 
                awayValue={awayStats.offense_points_per_opportunity || 0} 
                homeValue={homeStats.offense_points_per_opportunity || 0} 
                advantage={getAdvantage(awayStats.offense_points_per_opportunity, homeStats.offense_points_per_opportunity)}
                format="decimal"
              />
              <StatRow 
                label="Standard Downs PPA" 
                awayValue={awayStats.offense_standard_downs_ppa || 0} 
                homeValue={homeStats.offense_standard_downs_ppa || 0} 
                advantage={getAdvantage(awayStats.offense_standard_downs_ppa, homeStats.offense_standard_downs_ppa)}
                format="decimal"
              />
              <StatRow 
                label="Standard Downs Success %" 
                awayValue={awayStats.offense_standard_downs_success_rate ? awayStats.offense_standard_downs_success_rate * 100 : 0} 
                homeValue={homeStats.offense_standard_downs_success_rate ? homeStats.offense_standard_downs_success_rate * 100 : 0} 
                advantage={getAdvantage(awayStats.offense_standard_downs_success_rate, homeStats.offense_standard_downs_success_rate)}
                format="percent"
              />
              <StatRow 
                label="Passing Downs PPA" 
                awayValue={awayStats.offense_passing_downs_ppa || 0} 
                homeValue={homeStats.offense_passing_downs_ppa || 0} 
                advantage={getAdvantage(awayStats.offense_passing_downs_ppa, homeStats.offense_passing_downs_ppa)}
                format="decimal"
              />
              <StatRow 
                label="Passing Downs Success %" 
                awayValue={awayStats.offense_passing_downs_success_rate ? awayStats.offense_passing_downs_success_rate * 100 : 0} 
                homeValue={homeStats.offense_passing_downs_success_rate ? homeStats.offense_passing_downs_success_rate * 100 : 0} 
                advantage={getAdvantage(awayStats.offense_passing_downs_success_rate, homeStats.offense_passing_downs_success_rate)}
                format="percent"
              />
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* SPECIAL TEAMS & FIELD POSITION */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Flag className="w-5 h-5 text-yellow-400" />
          <h3 className="text-white font-semibold">Special Teams & Field Position</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-gray-400 text-sm font-semibold">Metric</th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-5 h-5" />
                    <span style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
                  </div>
                </th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-5 h-5" />
                    <span style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-400 text-sm font-semibold">Advantage</th>
              </tr>
            </thead>
            <tbody>
              <StatRow 
                label="Avg Field Position" 
                awayValue={awayStats.offense_field_position_avg_start || 0} 
                homeValue={homeStats.offense_field_position_avg_start || 0} 
                advantage={getAdvantage(awayStats.offense_field_position_avg_start, homeStats.offense_field_position_avg_start, false)}
                format="decimal"
              />
              <StatRow 
                label="Kick Return Yards" 
                awayValue={awayStats.kick_return_yards || 0} 
                homeValue={homeStats.kick_return_yards || 0} 
                advantage={getAdvantage(awayStats.kick_return_yards, homeStats.kick_return_yards)}
              />
              <StatRow 
                label="Punt Return Yards" 
                awayValue={awayStats.punt_return_yards || 0} 
                homeValue={homeStats.punt_return_yards || 0} 
                advantage={getAdvantage(awayStats.punt_return_yards, homeStats.punt_return_yards)}
              />
              <StatRow 
                label="Kick Return TDs" 
                awayValue={awayStats.kick_return_tds || 0} 
                homeValue={homeStats.kick_return_tds || 0} 
                advantage={getAdvantage(awayStats.kick_return_tds, homeStats.kick_return_tds)}
              />
              <StatRow 
                label="Punt Return TDs" 
                awayValue={awayStats.punt_return_tds || 0} 
                homeValue={homeStats.punt_return_tds || 0} 
                advantage={getAdvantage(awayStats.punt_return_tds, homeStats.punt_return_tds)}
              />
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* TURNOVERS & TAKEAWAYS */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <AlertCircle className="w-5 h-5 text-red-400" />
          <h3 className="text-white font-semibold">Turnovers & Takeaways Breakdown</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-gray-400 text-sm font-semibold">Metric</th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-5 h-5" />
                    <span style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
                  </div>
                </th>
                <th className="text-right py-3 px-4 text-gray-400 text-sm font-semibold">
                  <div className="flex items-center justify-end gap-2">
                    <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-5 h-5" />
                    <span style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-400 text-sm font-semibold">Advantage</th>
              </tr>
            </thead>
            <tbody>
              <StatRow 
                label="Turnovers" 
                awayValue={awayStats.turnovers_lost || 0} 
                homeValue={homeStats.turnovers_lost || 0} 
                advantage={getAdvantage(awayStats.turnovers_lost, homeStats.turnovers_lost, false)}
              />
              <StatRow 
                label="Turnovers Forced" 
                awayValue={awayStats.turnovers_created || 0} 
                homeValue={homeStats.turnovers_created || 0} 
                advantage={getAdvantage(awayStats.turnovers_created, homeStats.turnovers_created)}
              />
              <StatRow 
                label="Interception TDs" 
                awayValue={awayStats.interception_tds || 0} 
                homeValue={homeStats.interception_tds || 0} 
                advantage={getAdvantage(awayStats.interception_tds, homeStats.interception_tds)}
              />
              <StatRow 
                label="Interception Yards" 
                awayValue={awayStats.interception_yards || 0} 
                homeValue={homeStats.interception_yards || 0} 
                advantage={getAdvantage(awayStats.interception_yards, homeStats.interception_yards)}
              />
              <StatRow 
                label="Fumbles Lost" 
                awayValue={awayStats.fumbles_lost || 0} 
                homeValue={homeStats.fumbles_lost || 0} 
                advantage={getAdvantage(awayStats.fumbles_lost, homeStats.fumbles_lost, false)}
              />
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* TEMPO & TIME MANAGEMENT - From Drive Data */}
      {driveData && (
        <GlassCard className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <Clock className="w-5 h-5 text-purple-400" />
            <h3 className="text-white font-semibold">Tempo & Time Management Analysis</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Away Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Avg Time Per Drive</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.avg_time_per_drive || '0:00'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Quick Drives (&lt;2 min)</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.quick_drives_count || 0} ({driveData.away?.quick_drives_pct || 0}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Sustained Drives (&gt;5m)</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.sustained_drives_count || 0} ({driveData.away?.sustained_drives_pct || 0}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Two-Minute Drill</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.two_minute_drill || '0/0 (0.0%)'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Plays Per Drive</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.plays_per_drive?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Yards Per Play</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.yards_per_play?.toFixed(1) || '0.0'}</span>
                </div>
              </div>
            </div>

            {/* Home Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Avg Time Per Drive</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.avg_time_per_drive || '0:00'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Quick Drives (&lt;2 min)</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.quick_drives_count || 0} ({driveData.home?.quick_drives_pct || 0}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Sustained Drives (&gt;5m)</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.sustained_drives_count || 0} ({driveData.home?.sustained_drives_pct || 0}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Two-Minute Drill</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.two_minute_drill || '0/0 (0.0%)'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Plays Per Drive</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.plays_per_drive?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Yards Per Play</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.yards_per_play?.toFixed(1) || '0.0'}</span>
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      )}

      {/* RED ZONE & GOAL LINE - From Drive Data */}
      {driveData && (
        <GlassCard className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <Trophy className="w-5 h-5 text-orange-400" />
            <h3 className="text-white font-semibold">Red Zone & Goal Line Excellence</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Away Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Red Zone Efficiency</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.red_zone_efficiency || '0/0 (0.0%)'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Goal Line (≤5 yds)</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.goal_line_efficiency || '0/0 (0.0%)'}</span>
                </div>
              </div>
            </div>

            {/* Home Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Red Zone Efficiency</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.red_zone_efficiency || '0/0 (0.0%)'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Goal Line (≤5 yds)</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.goal_line_efficiency || '0/0 (0.0%)'}</span>
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      )}

      {/* MOMENTUM & PSYCHOLOGICAL - From Drive Data */}
      {driveData && (
        <GlassCard className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <Zap className="w-5 h-5 text-yellow-400" />
            <h3 className="text-white font-semibold">Momentum & Psychological Factors</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Away Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={awayTeam.logo} alt={awayAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Max Consecutive Scores</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.max_consecutive_scores || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Comeback Drives</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.comeback_drives || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Three & Outs Forced</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.three_and_outs_forced || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Overall Scoring %</span>
                  <span className="font-mono font-bold text-white">{driveData.away?.overall_scoring_pct?.toFixed(1) || 0}%</span>
                </div>
              </div>
            </div>

            {/* Home Team */}
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 rounded-lg p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback src={homeTeam.logo} alt={homeAbbr} className="w-6 h-6" />
                <h4 className="font-semibold" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Max Consecutive Scores</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.max_consecutive_scores || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Comeback Drives</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.comeback_drives || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Three & Outs Forced</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.three_and_outs_forced || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Overall Scoring %</span>
                  <span className="font-mono font-bold text-white">{driveData.home?.overall_scoring_pct?.toFixed(1) || 0}%</span>
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      )}
    </>
  );
}

