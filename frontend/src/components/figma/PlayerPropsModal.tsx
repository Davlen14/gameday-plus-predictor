import { X, TrendingUp, TrendingDown, Minus, Target, Shield, Activity, BarChart3, Home, Plane, CheckCircle, XCircle } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { teamService } from '../../services/teamService';

interface GameLog {
  week: number;
  opponent: string;
  home_away: string;
  result: string;
  stats: { [key: string]: number };
  defense_rank: number | null;
  opponent_logo?: string | null;
  opponent_color?: string | null;
}

interface PlayerProp {
  player_name: string;
  player_team: string;
  position: string;
  prop_type: string;
  line?: number;
  over_under_line: number;
  confidence: number;
  recommendation: string;
  reasoning: string;
  season_average: number;
  weather_impact: string;
  game_logs: GameLog[];
  trend_analysis: {
    last_3_games_avg: number;
    last_5_games_avg: number;
    season_avg: number;
    vs_good_defenses_avg: number;
    vs_poor_defenses_avg: number;
    home_vs_away_diff: number;
    trend_direction: string;
  };
  defensive_matchup: {
    opponent: string;
    category: string;
    sp_plus_rank: number | null;
    sp_plus_rating: number | null;
  };
  key_insights: string[];
}

interface PlayerPropsModalProps {
  prop: PlayerProp;
  isOpen: boolean;
  onClose: () => void;
  teamLogo?: string;
  teamColor?: string;
}

export function PlayerPropsModal({ prop, isOpen, onClose, teamLogo, teamColor = '#3B82F6' }: PlayerPropsModalProps) {
  if (!isOpen) return null;

  const propLine = prop.line ?? prop.over_under_line;

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'improving':
        return <TrendingUp className="w-5 h-5 text-green-400" />;
      case 'declining':
        return <TrendingDown className="w-5 h-5 text-red-400" />;
      default:
        return <Minus className="w-5 h-5 text-gray-400" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 60) return 'from-green-500 to-emerald-600';
    if (confidence >= 50) return 'from-yellow-500 to-orange-600';
    return 'from-red-500 to-pink-600';
  };

  const formatPropType = (type: string) => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
  };

  const getStatFromGameLog = (gameLog: GameLog): number => {
    return gameLog.stats[prop.prop_type] || 0;
  };

  const getMaxStatValue = (): number => {
    if (!prop.game_logs || prop.game_logs.length === 0) return propLine * 1.5;
    const maxGameStat = Math.max(...prop.game_logs.map(getStatFromGameLog));
    return Math.max(maxGameStat * 1.1, propLine * 1.2);
  };

  const getOpponentTeamData = (opponentName: string) => {
    const team = teamService.findTeam(opponentName);
    if (!team) return null;
    return {
      logo: teamService.getTeamLogos(team).light,
      colors: teamService.getTeamColors(team)
    };
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div 
        className="rounded-2xl w-full max-h-[90vh] overflow-y-auto border-4 backdrop-blur-xl"
        style={{
          maxWidth: '95vw',
          borderColor: `${teamColor}60`,
          background: `linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(31, 41, 55, 0.95) 100%)`,
          boxShadow: `0 0 40px ${teamColor}30, inset 0 0 60px rgba(0, 0, 0, 0.5)`
        }}
      >
        {/* Header */}
        <div 
          className="sticky top-0 z-10 backdrop-blur-xl p-6 border-b-2 overflow-hidden"
          style={{
            borderColor: `${teamColor}50`,
            background: `linear-gradient(135deg, ${teamColor}25 0%, ${teamColor}10 50%, ${teamColor}05 100%)`
          }}
        >
          {/* Team Logo Background */}
          <div className="absolute right-6 top-1/2 -translate-y-1/2 opacity-10">
            {teamLogo && (
              <ImageWithFallback 
                src={teamLogo}
                alt="Team Logo"
                className="w-32 h-32 object-contain"
                style={{ filter: 'drop-shadow(4px 4px 8px rgba(0,0,0,0.5))' }}
              />
            )}
          </div>

          <div className="flex items-start justify-between relative z-10">
            <div className="flex items-center gap-4">
              {teamLogo ? (
                <div 
                  className="w-16 h-16 rounded-xl flex items-center justify-center p-2 border-2"
                  style={{
                    background: `linear-gradient(135deg, ${teamColor}20 0%, ${teamColor}10 100%)`,
                    borderColor: `${teamColor}50`,
                    boxShadow: `0 0 20px ${teamColor}30`
                  }}
                >
                  <ImageWithFallback 
                    src={teamLogo} 
                    alt="Team Logo" 
                    className="w-full h-full object-contain"
                    style={{ filter: `drop-shadow(0 0 8px ${teamColor}80)` }}
                  />
                </div>
              ) : (
                <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <Target className="w-8 h-8 text-white" />
                </div>
              )}
              <div>
                <h2 
                  className="text-2xl font-bold font-orbitron"
                  style={{ 
                    color: teamColor,
                    textShadow: `0 0 20px ${teamColor}60`
                  }}
                >
                  {prop.player_name}
                </h2>
                <div className="flex items-center gap-3 mt-1">
                  <span 
                    className="text-sm px-3 py-1 rounded-full font-medium font-orbitron"
                    style={{
                      backgroundColor: `${teamColor}20`,
                      color: teamColor,
                      border: `1px solid ${teamColor}40`
                    }}
                  >
                    {prop.position}
                  </span>
                  <span className="text-sm text-gray-400 font-orbitron">
                    {formatPropType(prop.prop_type)}
                  </span>
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-3 rounded-xl transition-all hover:scale-110 border-2"
              style={{
                background: `linear-gradient(135deg, ${teamColor}30 0%, ${teamColor}15 100%)`,
                borderColor: `${teamColor}60`,
                boxShadow: `0 0 15px ${teamColor}40`
              }}
            >
              <X 
                className="w-6 h-6" 
                style={{ 
                  color: teamColor,
                  filter: `drop-shadow(0 0 4px ${teamColor}80)`
                }} 
              />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Recommendation Card */}
          <div className={`rounded-xl p-6 bg-gradient-to-br ${getConfidenceColor(prop.confidence)}/10 border border-white/10`}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-sm text-gray-400 mb-1">Recommendation</div>
                <div className="text-4xl font-bold text-white uppercase">
                  {prop.recommendation}
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-400 mb-1">Line</div>
                <div className="text-4xl font-bold text-white">
                  {propLine}
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-300">{prop.reasoning}</div>
              <div className={`px-4 py-2 rounded-lg bg-gradient-to-r ${getConfidenceColor(prop.confidence)}`}>
                <div className="text-xs text-white/80">Confidence</div>
                <div className="text-2xl font-bold text-white">{prop.confidence}%</div>
              </div>
            </div>
          </div>

          {/* Trend Analysis */}
          <div className="glassmorphism-card rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              {getTrendIcon(prop.trend_analysis.trend_direction)}
              <div>
                <h3 className="text-lg font-bold text-white">Performance Trends</h3>
                <p className="text-sm text-gray-400 capitalize">
                  {prop.trend_analysis.trend_direction} trajectory
                </p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-3 rounded-lg bg-white/5">
                <div className="text-xs text-gray-400 mb-1">Last 3 Games</div>
                <div className="text-2xl font-bold text-white">
                  {prop.trend_analysis.last_3_games_avg.toFixed(1)}
                </div>
              </div>
              <div className="text-center p-3 rounded-lg bg-white/5">
                <div className="text-xs text-gray-400 mb-1">Last 5 Games</div>
                <div className="text-2xl font-bold text-white">
                  {prop.trend_analysis.last_5_games_avg.toFixed(1)}
                </div>
              </div>
              <div className="text-center p-3 rounded-lg bg-white/5">
                <div className="text-xs text-gray-400 mb-1">Season Avg</div>
                <div className="text-2xl font-bold text-white">
                  {prop.trend_analysis.season_avg.toFixed(1)}
                </div>
              </div>
            </div>

            {/* Splits */}
            <div className="mt-4 grid grid-cols-2 gap-4">
              <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="w-4 h-4 text-red-400" />
                  <span className="text-xs text-red-400 font-medium">vs Good D</span>
                </div>
                <div className="text-xl font-bold text-white">
                  {prop.trend_analysis.vs_good_defenses_avg.toFixed(1)}
                </div>
              </div>
              <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-4 h-4 text-green-400" />
                  <span className="text-xs text-green-400 font-medium">vs Poor D</span>
                </div>
                <div className="text-xl font-bold text-white">
                  {prop.trend_analysis.vs_poor_defenses_avg.toFixed(1)}
                </div>
              </div>
            </div>

            {prop.trend_analysis.home_vs_away_diff !== 0 && (
              <div className="mt-4 p-3 rounded-lg bg-blue-500/10 border border-blue-500/20">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Home/Away Split</span>
                  <span className={`text-lg font-bold ${prop.trend_analysis.home_vs_away_diff > 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {prop.trend_analysis.home_vs_away_diff > 0 ? '+' : ''}
                    {prop.trend_analysis.home_vs_away_diff.toFixed(1)}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Defensive Matchup */}
          <div className="glassmorphism-card rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Shield className="w-6 h-6 text-red-400" />
              <div>
                <h3 className="text-lg font-bold text-white">Defensive Matchup</h3>
                <p className="text-sm text-gray-400">vs {prop.defensive_matchup.opponent}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-white/5">
                <div className="text-xs text-gray-400 mb-1">Defense Quality</div>
                <div className="text-xl font-bold text-white capitalize">
                  {prop.defensive_matchup.category}
                </div>
              </div>
              {prop.defensive_matchup.sp_plus_rank && (
                <div className="p-4 rounded-lg bg-white/5">
                  <div className="text-xs text-gray-400 mb-1">SP+ Rank</div>
                  <div className="text-xl font-bold text-white">
                    #{prop.defensive_matchup.sp_plus_rank}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Key Insights */}
          {prop.key_insights && prop.key_insights.length > 0 && (
            <div className="glassmorphism-card rounded-xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <BarChart3 className="w-6 h-6 text-blue-400" />
                <h3 className="text-lg font-bold text-white">Key Insights</h3>
              </div>
              <div className="space-y-3">
                {prop.key_insights.map((insight, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400 mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-gray-300">{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Game Log Visualization */}
          {prop.game_logs && prop.game_logs.length > 0 && (
            <div className="glassmorphism-card rounded-xl p-6">
              <div className="flex items-center gap-3 mb-6">
                <BarChart3 className="w-6 h-6 text-purple-400" />
                <div>
                  <h3 className="text-lg font-bold text-white font-orbitron">Game Log Analysis</h3>
                  <p className="text-sm text-gray-400">Last {prop.game_logs.length} games performance</p>
                </div>
              </div>

              {/* Bar Chart */}
              <div className="relative h-64 mb-6 p-4 rounded-xl bg-black/30">
                {/* Y-axis labels */}
                <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500 font-orbitron pr-2 py-2">
                  <span>{Math.round(getMaxStatValue())}</span>
                  <span>{Math.round(getMaxStatValue() * 0.75)}</span>
                  <span>{Math.round(getMaxStatValue() * 0.5)}</span>
                  <span>{Math.round(getMaxStatValue() * 0.25)}</span>
                  <span>0</span>
                </div>

                {/* Chart area */}
                <div className="ml-10 h-full relative py-2">
                  <div className="h-full flex items-end justify-between gap-1">
                    {[...prop.game_logs].reverse().map((gameLog, index) => {
                      const statValue = getStatFromGameLog(gameLog);
                      const maxValue = getMaxStatValue();
                      const barHeightPercent = maxValue > 0 ? (statValue / maxValue) * 100 : 0;
                      const exceededLine = statValue >= propLine;
                      
                      // Use opponent data from backend if available, fallback to teamService
                      const opponentData = gameLog.opponent_logo && gameLog.opponent_color 
                        ? { logo: gameLog.opponent_logo, colors: { primary: gameLog.opponent_color } }
                        : getOpponentTeamData(gameLog.opponent);
                      const opponentColor = opponentData?.colors.primary || (exceededLine ? teamColor : '#EF4444');
                      const opponentLogo = opponentData?.logo;
                      
                      // Determine defense quality based on defensive_matchup data
                      const getDefenseQuality = () => {
                        if (gameLog.defense_rank) {
                          if (gameLog.defense_rank <= 20) return { label: 'Great', color: '#10B981' }; // Green - Top 20
                          if (gameLog.defense_rank <= 70) return { label: 'Average', color: '#F59E0B' }; // Yellow - 21-70
                          return { label: 'Bad', color: '#EF4444' }; // Red - 70+
                        }
                        return null;
                      };
                      const defenseQuality = getDefenseQuality();

                      return (
                        <div key={index} className="flex-1 h-full relative group flex items-end">
                          {/* Bar - Glassmorphism style */}
                          <div 
                            className="w-full rounded-t-xl transition-all duration-300 hover:scale-105 cursor-pointer relative overflow-hidden border backdrop-blur-xl"
                            style={{
                              height: `${Math.max(barHeightPercent, statValue > 0 ? 2 : 0)}%`,
                              background: `linear-gradient(180deg, ${opponentColor}30 0%, ${opponentColor}20 50%, ${opponentColor}15 100%)`,
                              boxShadow: `0 0 20px ${opponentColor}40, 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.2)`,
                              borderColor: `${opponentColor}60`,
                            }}
                          >
                            {/* Glass reflection effect */}
                            <div 
                              className="absolute inset-0 opacity-40"
                              style={{
                                background: `linear-gradient(180deg, rgba(255,255,255,0.3) 0%, transparent 40%, rgba(0,0,0,0.2) 100%)`
                              }}
                            />
                            
                            {/* Opponent logo watermark */}
                            {opponentLogo && (
                              <div className="absolute inset-0 flex items-center justify-center opacity-25">
                                <ImageWithFallback
                                  src={opponentLogo}
                                  alt={gameLog.opponent}
                                  className="w-12 h-12 object-contain"
                                  style={{
                                    filter: `drop-shadow(0 0 8px ${opponentColor}80)`
                                  }}
                                />
                              </div>
                            )}
                            
                            {/* Gradient glow overlay */}
                            <div 
                              className="absolute inset-0 opacity-50"
                              style={{
                                background: `radial-gradient(circle at 50% 100%, ${opponentColor}40 0%, transparent 70%)`
                              }}
                            />
                            
                            {/* Stat value on bar */}
                            <div 
                              className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold font-orbitron whitespace-nowrap"
                              style={{ 
                                color: opponentColor,
                                textShadow: `0 0 10px ${opponentColor}80, 0 2px 4px rgba(0,0,0,0.5)`
                              }}
                            >
                              {statValue.toFixed(0)}
                            </div>
                            
                            {/* Defense quality badge */}
                            {defenseQuality && (
                              <div 
                                className="absolute top-1 left-1/2 -translate-x-1/2 p-1 rounded-full border"
                                style={{
                                  backgroundColor: `${defenseQuality.color}30`,
                                  borderColor: `${defenseQuality.color}80`,
                                  boxShadow: `0 0 8px ${defenseQuality.color}60`
                                }}
                              >
                                <Shield className="w-3 h-3" style={{ color: defenseQuality.color }} />
                              </div>
                            )}
                          </div>

                          {/* Tooltip on hover */}
                          <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-20 whitespace-nowrap">
                            <div 
                              className="px-3 py-2 rounded-lg text-xs font-orbitron border-2 backdrop-blur-xl"
                              style={{
                                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                borderColor: `${opponentColor}60`,
                                boxShadow: `0 0 20px ${opponentColor}60`
                              }}
                            >
                              <div className="flex items-center gap-2 mb-1">
                                {opponentData?.logo && (
                                  <ImageWithFallback
                                    src={opponentData.logo}
                                    alt={gameLog.opponent}
                                    className="w-5 h-5 object-contain"
                                  />
                                )}
                                <div className="text-white font-bold">{statValue.toFixed(1)}</div>
                              </div>
                              <div className="text-gray-400">Week {gameLog.week}</div>
                              <div className="text-gray-400">vs {gameLog.opponent}</div>
                              {defenseQuality && (
                                <div className="flex items-center gap-1 text-xs font-bold mt-1" style={{ color: defenseQuality.color }}>
                                  <Shield className="w-3 h-3" />
                                  {defenseQuality.label} Defense (#{gameLog.defense_rank})
                                </div>
                              )}
                              <div className={`text-xs font-bold ${gameLog.result === 'W' ? 'text-green-400' : 'text-red-400'}`}>
                                {gameLog.result === 'W' ? 'WIN' : 'LOSS'}
                              </div>
                            </div>
                          </div>

                          {/* Week label with opponent logo */}
                          <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1">
                            {opponentData?.logo && (
                              <ImageWithFallback
                                src={opponentData.logo}
                                alt={gameLog.opponent}
                                className="w-6 h-6 object-contain"
                              />
                            )}
                            <div className="text-xs text-gray-400 font-orbitron">
                              W{gameLog.week}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Prop line reference */}
                  <div 
                    className="absolute left-0 right-0 border-t-2 border-dashed pointer-events-none"
                    style={{
                      bottom: `${(propLine / getMaxStatValue()) * 100}%`,
                      borderColor: `${teamColor}80`,
                    }}
                  >
                    <div 
                      className="absolute left-1/2 -translate-x-1/2 -top-5 px-3 py-1 rounded-lg text-sm font-bold font-orbitron backdrop-blur-sm"
                      style={{
                        backgroundColor: `${teamColor}40`,
                        color: teamColor,
                        border: `2px solid ${teamColor}80`,
                        boxShadow: `0 0 15px ${teamColor}50`
                      }}
                    >
                      Line: {propLine}
                    </div>
                  </div>
                </div>
              </div>

              {/* Game Log Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-700">
                      <th className="text-left py-3 px-2 text-gray-400 font-orbitron text-xs">Week</th>
                      <th className="text-left py-3 px-2 text-gray-400 font-orbitron text-xs">Opponent</th>
                      <th className="text-center py-3 px-2 text-gray-400 font-orbitron text-xs">Defense</th>
                      <th className="text-center py-3 px-2 text-gray-400 font-orbitron text-xs">H/A</th>
                      <th className="text-center py-3 px-2 text-gray-400 font-orbitron text-xs">Result</th>
                      <th className="text-right py-3 px-2 text-gray-400 font-orbitron text-xs">Stat</th>
                      <th className="text-center py-3 px-2 text-gray-400 font-orbitron text-xs">vs Line</th>
                    </tr>
                  </thead>
                  <tbody className="font-orbitron">
                    {[...prop.game_logs].reverse().map((gameLog, index) => {
                      const statValue = getStatFromGameLog(gameLog);
                      const exceededLine = statValue >= propLine;
                      
                      // Use opponent data from backend if available, fallback to teamService
                      const opponentData = gameLog.opponent_logo && gameLog.opponent_color 
                        ? { logo: gameLog.opponent_logo, colors: { primary: gameLog.opponent_color } }
                        : getOpponentTeamData(gameLog.opponent);
                      const opponentLogo = opponentData?.logo;
                      
                      // Defense quality for table
                      const getDefenseQuality = () => {
                        if (gameLog.defense_rank) {
                          if (gameLog.defense_rank <= 20) return { label: 'Great', color: '#10B981' }; // Green - Top 20
                          if (gameLog.defense_rank <= 70) return { label: 'Average', color: '#F59E0B' }; // Yellow - 21-70
                          return { label: 'Bad', color: '#EF4444' }; // Red - 70+
                        }
                        return null;
                      };
                      const defenseQuality = getDefenseQuality();
                      
                      return (
                        <tr 
                          key={index}
                          className="border-b border-gray-800 hover:bg-white/5 transition-colors"
                        >
                          <td className="py-3 px-2">
                            <span className="text-white font-bold">{gameLog.week}</span>
                          </td>
                          <td className="py-3 px-2">
                            <div className="flex items-center gap-2">
                              {opponentLogo && (
                                <ImageWithFallback
                                  src={opponentLogo}
                                  alt={gameLog.opponent}
                                  className="w-6 h-6 object-contain"
                                />
                              )}
                              <span className="text-gray-300">{gameLog.opponent}</span>
                            </div>
                          </td>
                          <td className="py-3 px-2 text-center">
                            {defenseQuality ? (
                              <div className="flex flex-col items-center gap-0.5">
                                <Shield className="w-4 h-4" style={{ color: defenseQuality.color }} />
                                <span className="text-[9px] text-gray-500">#{gameLog.defense_rank}</span>
                              </div>
                            ) : (
                              <span className="text-gray-600 text-xs">-</span>
                            )}
                          </td>
                          <td className="py-3 px-2 text-center">
                            {gameLog.home_away === 'home' ? (
                              <Home className="w-4 h-4 text-blue-400 inline" />
                            ) : (
                              <Plane className="w-4 h-4 text-orange-400 inline" />
                            )}
                          </td>
                          <td className="py-3 px-2 text-center">
                            <span 
                              className={`font-bold ${
                                gameLog.result === 'W' ? 'text-green-400' : 'text-red-400'
                              }`}
                            >
                              {gameLog.result}
                            </span>
                          </td>
                          <td className="py-3 px-2 text-right">
                            <span 
                              className="font-medium text-base tracking-tight"
                              style={{ 
                                color: statValue > prop.season_average * 1.1 
                                  ? '#10B981'  // Green - above average (>110%)
                                  : statValue < prop.season_average * 0.9 
                                    ? '#EF4444'  // Red - below average (<90%)
                                    : '#F59E0B'  // Yellow - average (90-110%)
                              }}
                            >
                              {statValue.toFixed(1)}
                            </span>
                          </td>
                          <td className="py-3 px-2 text-center">
                            {exceededLine ? (
                              <CheckCircle className="w-5 h-5 text-green-400 inline" />
                            ) : (
                              <XCircle className="w-5 h-5 text-red-400 inline" />
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Summary Stats */}
              <div className="mt-4 grid grid-cols-3 gap-3">
                <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/30">
                  <div className="text-xs text-green-400 mb-1 font-orbitron">Over Line</div>
                  <div className="text-xl font-bold text-white font-orbitron">
                    {prop.game_logs.filter(g => getStatFromGameLog(g) >= propLine).length}/{prop.game_logs.length}
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30">
                  <div className="text-xs text-red-400 mb-1 font-orbitron">Under Line</div>
                  <div className="text-xl font-bold text-white font-orbitron">
                    {prop.game_logs.filter(g => getStatFromGameLog(g) < propLine).length}/{prop.game_logs.length}
                  </div>
                </div>
                <div 
                  className="p-3 rounded-lg border"
                  style={{
                    backgroundColor: `${teamColor}10`,
                    borderColor: `${teamColor}30`
                  }}
                >
                  <div className="text-xs mb-1 font-orbitron" style={{ color: teamColor }}>Hit Rate</div>
                  <div className="text-xl font-bold text-white font-orbitron">
                    {((prop.game_logs.filter(g => getStatFromGameLog(g) >= propLine).length / prop.game_logs.length) * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
