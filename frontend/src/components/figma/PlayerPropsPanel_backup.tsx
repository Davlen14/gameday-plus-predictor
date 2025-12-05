import { useState, useMemo } from 'react';
import { Flame, AlertTriangle, Target, Activity, Award, TrendingUp, Users } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface PlayerStats {
  pass_yards?: number;
  pass_tds?: number;
  pass_completions?: number;
  pass_attempts?: number;
  interceptions?: number;
  rush_yards?: number;
  rush_tds?: number;
  rush_attempts?: number;
  rec_yards?: number;
  rec_tds?: number;
  receptions?: number;
  targets?: number;
  tackles?: number;
  sacks?: number;
  interceptions_def?: number;
}

interface EfficiencyMetrics {
  comprehensive_efficiency_score?: number;
  efficiency_score?: number;
  passing_efficiency?: number;
  rushing_efficiency?: number;
  receiving_efficiency?: number;
  defensive_efficiency?: number;
}

interface Player {
  name: string;
  player_name?: string;
  team: string;
  position: string;
  position_type?: string;
  headshot_url?: string;
  stats?: PlayerStats;
  season_stats?: PlayerStats;
  efficiency_metrics?: EfficiencyMetrics;
  comprehensive_efficiency_score?: number; // For non-QBs (RB, WR, TE, Defense)
}

interface TeamPlayers {
  qb: Player | null;
  rbs: Player[];
  wrs: Player[];
  tes: Player[];
  defense: Player[];
}

interface PlayerPropsData {
  home_players?: TeamPlayers;
  away_players?: TeamPlayers;
  positional_advantages?: {
    quarterback?: number;
    skill_positions?: number;
    defense?: number;
  };
  total_impact?: number;
  database_stats?: {
    quarterbacks_analyzed?: number;
    running_backs_analyzed?: number;
    wide_receivers_analyzed?: number;
    defensive_backs_analyzed?: number;
  };
}

interface PlayerPropsPanelProps {
  predictionData?: {
    detailed_analysis?: {
      enhanced_player_analysis?: PlayerPropsData;
    };
    team_selector?: {
      home_team?: { name: string; logo: string; primary_color: string; alt_color?: string };
      away_team?: { name: string; logo: string; primary_color: string; alt_color?: string };
    };
  };
}

interface ThreatLevel {
  level: 'elite' | 'high' | 'medium' | 'low';
  label: string;
  gradient: string;
  borderColor: string;
  shadowColor: string;
  icon: typeof Flame;
}

const getThreatLevel = (efficiencyScore: number): ThreatLevel => {
  if (efficiencyScore >= 250) {
    return {
      level: 'elite',
      label: 'Elite',
      gradient: 'from-green-600 to-green-700',
      borderColor: 'border-green-500',
      shadowColor: 'shadow-none',
      icon: TrendingUp
    };
  } else if (efficiencyScore >= 200) {
    return {
      level: 'high',
      label: 'High',
      gradient: 'from-green-500 to-green-600',
      borderColor: 'border-green-400',
      shadowColor: 'shadow-none',
      icon: TrendingUp
    };
  } else if (efficiencyScore >= 150) {
    return {
      level: 'medium',
      label: 'Medium',
      gradient: 'from-yellow-500 to-yellow-600',
      borderColor: 'border-yellow-500',
      shadowColor: 'shadow-none',
      icon: Flame
    };
  } else {
    return {
      level: 'low',
      label: 'Low',
      gradient: 'from-red-500 to-red-600',
      borderColor: 'border-red-500',
      shadowColor: 'shadow-none',
      icon: AlertTriangle
    };
  }
};

const getPositionBadgeColor = (position: string | undefined): string => {
  // All positions use neutral gray for professional look
  return 'bg-gray-700 text-gray-200';
};

const getPrimaryStatLabel = (position: string | undefined): string => {
  if (!position) return 'Stats';
  const pos = position.toUpperCase();
  if (pos === 'QB') return 'Pass Yards';
  if (pos === 'RB') return 'Rush Yards';
  if (pos === 'WR' || pos === 'TE') return 'Rec Yards';
  if (['DB', 'LB', 'DL'].includes(pos)) return 'Tackles';
  return 'Stats';
};

const getPrimaryStatValue = (player: any): number => {
  if (!player.position) return 0;
  
  const pos = player.position.toUpperCase();
  
  // Check for comprehensive JSON data structure (flat then nested)
  if (pos === 'QB') {
    return player.passing_stats?.passing_yards || player.stats?.pass_yards || 0;
  }
  if (pos === 'RB') {
    return player.rushing_yards || player.rushing_stats?.rushing_yards || player.stats?.rush_yards || 0;
  }
  if (pos === 'WR' || pos === 'TE') {
    return player.receiving_yards || player.receiving_stats?.receiving_yards || player.stats?.rec_yards || 0;
  }
  if (['DB', 'LB', 'DL'].includes(pos)) {
    return player.tackles || player.defensive_stats?.tackles || player.stats?.tackles || 0;
  }
  return 0;
};

const getPlayerMetrics = (player: any): Array<{label: string; value: string | number}> => {
  if (!player.position) return [];
  
  const pos = player.position.toUpperCase();
  
  if (pos === 'QB') {
    const passing = player.passing_stats || {};
    const rushing = player.rushing_stats || {};
    return [
      { label: 'Comp', value: `${passing.completions || 0}/${passing.attempts || 0}` },
      { label: 'TDs', value: passing.passing_tds || 0 },
      { label: 'INTs', value: passing.interceptions || 0 },
      { label: 'Rush', value: rushing.rushing_yards || 0 }
    ];
  } else if (pos === 'RB') {
    // Check flat structure first (comprehensive JSON), then nested
    const rushAttempts = player.rushing_attempts || player.rushing_stats?.rushing_attempts || 0;
    const rushTds = player.rushing_tds || player.rushing_stats?.rushing_tds || 0;
    const receptions = player.receptions || player.receiving_stats?.receptions || 0;
    const rushAvg = player.rushing_avg || player.yards_per_carry || player.rushing_stats?.rushing_avg || 0;
    return [
      { label: 'Att', value: rushAttempts },
      { label: 'TDs', value: rushTds },
      { label: 'Rec', value: receptions },
      { label: 'YPC', value: typeof rushAvg === 'number' ? rushAvg.toFixed(1) : '0.0' }
    ];
  } else if (pos === 'WR' || pos === 'TE') {
    // Check flat structure first (comprehensive JSON), then nested
    const receptions = player.receptions || player.receiving_stats?.receptions || 0;
    const targets = player.targets || player.receiving_stats?.targets || 0;
    const recTds = player.receiving_tds || player.receiving_stats?.receiving_tds || 0;
    const ypr = player.yards_per_reception || player.receiving_avg || player.receiving_stats?.yards_per_reception || 0;
    return [
      { label: 'Rec', value: receptions },
      { label: 'Tgts', value: targets },
      { label: 'TDs', value: recTds },
      { label: 'YPR', value: typeof ypr === 'number' ? ypr.toFixed(1) : '0.0' }
    ];
  } else if (['DB', 'LB', 'DL'].includes(pos)) {
    // Check flat structure first (comprehensive JSON), then nested
    const tackles = player.tackles || player.defensive_stats?.tackles || 0;
    const sacks = player.sacks || player.defensive_stats?.sacks || 0;
    const ints = player.interceptions || player.defensive_stats?.interceptions || 0;
    return [
      { label: 'Tackles', value: tackles },
      { label: 'Sacks', value: sacks },
      { label: 'INTs', value: ints },
      { label: 'Type', value: player.position_type || pos }
    ];
  }
  
  return [];
};

interface PlayerCardProps {
  player: Player;
  teamLogo: string;
  teamColor: string;
  teamName: string;
}

interface MatchupCardProps {
  offensivePlayer: Player & { teamData: any };
  defensivePlayer: Player & { teamData: any };
}

const MatchupCard = ({ offensivePlayer, defensivePlayer }: MatchupCardProps) => {
  const offName = offensivePlayer.player_name || offensivePlayer.name;
  const defName = defensivePlayer.player_name || defensivePlayer.name;
  const offEfficiency = offensivePlayer.efficiency_metrics?.comprehensive_efficiency_score || 
                        offensivePlayer.efficiency_metrics?.efficiency_score ||
                        offensivePlayer.comprehensive_efficiency_score || 0;
  const defEfficiency = defensivePlayer.efficiency_metrics?.comprehensive_efficiency_score || 
                        defensivePlayer.efficiency_metrics?.efficiency_score ||
                        defensivePlayer.comprehensive_efficiency_score || 0;
  
  const offThreat = getThreatLevel(offEfficiency);
  const defThreat = getThreatLevel(defEfficiency);
  const advantage = offEfficiency > defEfficiency ? 'offense' : 'defense';
  const differential = Math.abs(offEfficiency - defEfficiency);
  
  return (
    <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-gray-900/90 via-gray-800/80 to-gray-900/90 border border-white/10 hover:border-white/20 transition-all backdrop-blur-sm">
      {/* Matchup Header */}
      <div className="p-3 border-b border-white/10 bg-white/5">
        <div className="flex items-center justify-center gap-2">
          <Target className="w-4 h-4 text-yellow-400" />
          <span className="text-xs font-bold text-white uppercase tracking-wide">Key Matchup</span>
        </div>
      </div>
      
      {/* Split View */}
      <div className="grid grid-cols-2 divide-x divide-white/10">
        {/* Offensive Player */}
        <div className="p-4 relative">
          <div className="absolute right-2 top-2 opacity-5 pointer-events-none">
            <ImageWithFallback 
              src={offensivePlayer.teamData?.logo}
              alt={offensivePlayer.teamData?.name}
              className="w-20 h-20 object-contain"
            />
          </div>
          
          <div className={`absolute top-2 left-2 bg-gradient-to-r ${offThreat.gradient} rounded px-2 py-1 text-[9px] text-white font-bold`}>
            {offEfficiency.toFixed(0)}
          </div>
          
          <div className="relative z-10">
            <div className="w-16 h-16 mx-auto mb-2">
              <ImageWithFallback
                src={offensivePlayer.headshot_url || '/default-player.png'}
                alt={offName}
                className="w-full h-full object-contain drop-shadow-lg"
              />
            </div>
            
            <div className="text-center">
              <h4 className="text-white font-bold text-xs mb-1 truncate">{offName}</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-gray-700 text-gray-200 font-semibold">
                {offensivePlayer.position?.toUpperCase()}
              </span>
              <div className="mt-2 text-[10px] text-gray-400">{offensivePlayer.teamData?.name}</div>
              
              <div className="mt-3 p-2 bg-white/5 rounded border border-white/5">
                <div className="text-[9px] text-gray-400">Primary Stat</div>
                <div className="text-lg font-bold text-white">{getPrimaryStatValue(offensivePlayer).toFixed(0)}</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Defensive Player */}
        <div className="p-4 relative">
          <div className="absolute left-2 top-2 opacity-5 pointer-events-none">
            <ImageWithFallback 
              src={defensivePlayer.teamData?.logo}
              alt={defensivePlayer.teamData?.name}
              className="w-20 h-20 object-contain"
            />
          </div>
          
          <div className={`absolute top-2 right-2 bg-gradient-to-r ${defThreat.gradient} rounded px-2 py-1 text-[9px] text-white font-bold`}>
            {defEfficiency.toFixed(0)}
          </div>
          
          <div className="relative z-10">
            <div className="w-16 h-16 mx-auto mb-2">
              <ImageWithFallback
                src={defensivePlayer.headshot_url || '/default-player.png'}
                alt={defName}
                className="w-full h-full object-contain drop-shadow-lg"
              />
            </div>
            
            <div className="text-center">
              <h4 className="text-white font-bold text-xs mb-1 truncate">{defName}</h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-gray-700 text-gray-200 font-semibold">
                {defensivePlayer.position?.toUpperCase()}
              </span>
              <div className="mt-2 text-[10px] text-gray-400">{defensivePlayer.teamData?.name}</div>
              
              <div className="mt-3 p-2 bg-white/5 rounded border border-white/5">
                <div className="text-[9px] text-gray-400">Primary Stat</div>
                <div className="text-lg font-bold text-white">{getPrimaryStatValue(defensivePlayer).toFixed(0)}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Matchup Analysis Footer */}
      <div className="p-3 border-t border-white/10 bg-white/5">
        <div className="text-center">
          <div className="text-[10px] text-gray-400 mb-1">EFFICIENCY ADVANTAGE</div>
          <div className={`text-sm font-bold ${advantage === 'offense' ? 'text-green-400' : 'text-red-400'}`}>
            {advantage === 'offense' ? offName.split(' ')[1] : defName.split(' ')[1]} +{differential.toFixed(0)}
          </div>
        </div>
      </div>
    </div>
  );
};

const PlayerCard = ({ player, teamLogo, teamColor, teamName }: PlayerCardProps) => {
  const name = player.player_name || player.name;
  // QBs have nested efficiency_metrics, other positions have it at root level
  const efficiencyScore = player.efficiency_metrics?.comprehensive_efficiency_score || 
                          player.efficiency_metrics?.efficiency_score ||
                          player.comprehensive_efficiency_score || 0;
  
  const threat = getThreatLevel(efficiencyScore);
  const ThreatIcon = threat.icon;
  const primaryStatValue = getPrimaryStatValue(player);
  const primaryStatLabel = getPrimaryStatLabel(player.position);
  const metrics = getPlayerMetrics(player);
  
  return (
    <div className="relative overflow-hidden rounded-lg p-3 bg-white/5 border border-white/10 hover:border-white/20 transition-all">
      {/* Team Logo Watermark */}
      <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-5 pointer-events-none">
        <ImageWithFallback 
          src={teamLogo}
          alt={teamName}
          className="w-20 h-20 object-contain"
        />
      </div>
      
      {/* Efficiency Badge - Top Right */}
      <div className={`absolute top-2 right-2 bg-gradient-to-r ${threat.gradient} rounded px-2 py-1 flex items-center gap-1`}>
        <ThreatIcon className="w-3 h-3 text-white" />
        <span className="text-xs font-bold text-white">{efficiencyScore.toFixed(0)}</span>
      </div>
      
      {/* Player Headshot - Transparent, no container */}
      <div className="mb-2 relative z-10">
        <ImageWithFallback
          src={player.headshot_url || '/default-player.png'}
          alt={name}
          className="w-16 h-16 mx-auto object-contain"
        />
      </div>
      
      {/* Player Info - Compact */}
      <div className="text-center mb-2 relative z-10">
        <h3 className="text-white font-semibold text-sm mb-1 truncate">
          {name}
        </h3>
        <div className="flex items-center justify-center gap-1.5 text-xs">
          <span className={`px-2 py-0.5 rounded ${getPositionBadgeColor(player.position)} font-medium`}>
            {player.position?.toUpperCase() || 'N/A'}
          </span>
          <span className="text-gray-400">{teamName}</span>
        </div>
      </div>
      
      {/* Primary Stat - Compact */}
      <div className="mb-2 p-2 bg-gray-800/50 rounded border border-white/5 relative z-10">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] text-gray-400 uppercase">{primaryStatLabel}</span>
          <Activity className="w-3 h-3 text-gray-500" />
        </div>
        <div className="text-xl font-bold text-white">
          {primaryStatValue.toFixed(0)}
        </div>
      </div>
      
      {/* Metrics Grid - Compact */}
      <div className="grid grid-cols-2 gap-1.5 relative z-10">
        {metrics.map((metric, idx) => (
          <div key={idx} className="p-1.5 bg-gray-800/30 rounded border border-white/5">
            <div className="text-[9px] text-gray-400 uppercase mb-0.5">{metric.label}</div>
            <div className="text-xs font-semibold text-white">{metric.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export function PlayerPropsPanel({ predictionData }: PlayerPropsPanelProps) {
  const [showAllPlayers, setShowAllPlayers] = useState(false);
  
  const playerData = useMemo(() => {
    const analysis = predictionData?.detailed_analysis?.enhanced_player_analysis;
    if (!analysis) return null;
    
    const homeTeam = predictionData.team_selector?.home_team;
    const awayTeam = predictionData.team_selector?.away_team;
    
    const homePlayers = analysis.home_players || {} as TeamPlayers;
    const awayPlayers = analysis.away_players || {} as TeamPlayers;
    
    // Compile all players with their efficiency scores
    const allPlayers: Array<Player & { teamData: any }> = [];
    
    // Add QBs with position field
    if (homePlayers.qb) allPlayers.push({ ...homePlayers.qb, position: 'QB', teamData: homeTeam });
    if (awayPlayers.qb) allPlayers.push({ ...awayPlayers.qb, position: 'QB', teamData: awayTeam });
    
    // Add RBs (top 2 per team) with position field
    homePlayers.rbs?.slice(0, 2).forEach(rb => allPlayers.push({ ...rb, position: 'RB', teamData: homeTeam }));
    awayPlayers.rbs?.slice(0, 2).forEach(rb => allPlayers.push({ ...rb, position: 'RB', teamData: awayTeam }));
    
    // Add WRs (top 3 per team) with position field
    homePlayers.wrs?.slice(0, 3).forEach(wr => allPlayers.push({ ...wr, position: 'WR', teamData: homeTeam }));
    awayPlayers.wrs?.slice(0, 3).forEach(wr => allPlayers.push({ ...wr, position: 'WR', teamData: awayTeam }));
    
    // Add TEs (top 2 per team) with position field
    homePlayers.tes?.slice(0, 2).forEach(te => allPlayers.push({ ...te, position: 'TE', teamData: homeTeam }));
    awayPlayers.tes?.slice(0, 2).forEach(te => allPlayers.push({ ...te, position: 'TE', teamData: awayTeam }));
    
    // Add all defense players (DBs, LBs, DLs) - top 3 per team from defense array
    homePlayers.defense?.slice(0, 3).forEach(def => {
      const position = def.position_type || 'DB';
      allPlayers.push({ ...def, position: position, teamData: homeTeam });
    });
    awayPlayers.defense?.slice(0, 3).forEach(def => {
      const position = def.position_type || 'DB';
      allPlayers.push({ ...def, position: position, teamData: awayTeam });
    });
    
    // Sort by efficiency score
    allPlayers.sort((a, b) => {
      const aScore = a.efficiency_metrics?.comprehensive_efficiency_score || 
                     a.efficiency_metrics?.efficiency_score || 
                     a.comprehensive_efficiency_score || 0;
      const bScore = b.efficiency_metrics?.comprehensive_efficiency_score || 
                     b.efficiency_metrics?.efficiency_score || 
                     b.comprehensive_efficiency_score || 0;
      return bScore - aScore;
    });
    
    // Calculate threat level counts
    const threatCounts = {
      elite: 0,
      high: 0,
      medium: 0,
      low: 0
    };
    
    allPlayers.forEach(player => {
      const score = player.efficiency_metrics?.comprehensive_efficiency_score || 
                    player.efficiency_metrics?.efficiency_score || 
                    player.comprehensive_efficiency_score || 0;
      const threat = getThreatLevel(score);
      threatCounts[threat.level]++;
    });
    
    return {
      allPlayers,
      threatCounts,
      databaseStats: analysis.database_stats,
      homeTeam,
      awayTeam
    };
  }, [predictionData]);
  
  if (!playerData || !playerData.allPlayers.length) {
    return (
      <div className="glassmorphism rounded-2xl p-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Users className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Enhanced Player Analysis</h2>
            <p className="text-sm text-gray-400">No player data available</p>
          </div>
        </div>
      </div>
    );
  }
  
  // Create matchup cards for WR vs DB
  const createMatchups = () => {
    const matchups: Array<{ offensivePlayer: Player & { teamData: any }; defensivePlayer: Player & { teamData: any } }> = [];
    
    // Get top WRs from each team
    const homeWRs = playerData.allPlayers.filter(p => p.position === 'WR' && p.teamData?.name === playerData.homeTeam?.name).slice(0, 2);
    const awayWRs = playerData.allPlayers.filter(p => p.position === 'WR' && p.teamData?.name === playerData.awayTeam?.name).slice(0, 2);
    
    // Get top DBs from each team
    const homeDBs = playerData.allPlayers.filter(p => p.position === 'DB' && p.teamData?.name === playerData.homeTeam?.name).slice(0, 2);
    const awayDBs = playerData.allPlayers.filter(p => p.position === 'DB' && p.teamData?.name === playerData.awayTeam?.name).slice(0, 2);
    
    // Create cross-team matchups (Home WR vs Away DB, Away WR vs Home DB)
    if (homeWRs[0] && awayDBs[0]) matchups.push({ offensivePlayer: homeWRs[0], defensivePlayer: awayDBs[0] });
    if (awayWRs[0] && homeDBs[0]) matchups.push({ offensivePlayer: awayWRs[0], defensivePlayer: homeDBs[0] });
    
    return matchups.slice(0, 2); // Show top 2 matchups
  };
  
  const matchups = createMatchups();
  const displayedPlayers = showAllPlayers ? playerData.allPlayers : playerData.allPlayers.slice(0, 12);
  
  return (
    <div className="glassmorphism rounded-2xl p-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-lg bg-gray-800 border border-white/10 flex items-center justify-center">
            <Users className="w-6 h-6 text-gray-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Player Analysis</h2>
            <p className="text-sm text-gray-400">Efficiency-based performance metrics</p>
          </div>
        </div>
        
        {/* Stats Summary */}
        <div className="text-right">
          <div className="flex items-center gap-4 mb-2">
            <div className="text-center">
              <div className="text-xs text-gray-400">Elite</div>
              <div className="text-xl font-bold text-green-400">{playerData.threatCounts.elite}</div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400">High</div>
              <div className="text-xl font-bold text-green-300">{playerData.threatCounts.high}</div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400">Medium</div>
              <div className="text-xl font-bold text-yellow-400">{playerData.threatCounts.medium}</div>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            {playerData.databaseStats?.quarterbacks_analyzed || 0} QBs analyzed
          </div>
        </div>
      </div>
      
      {/* Efficiency Scale Legend */}
      <div className="grid grid-cols-4 gap-3 mb-6">
        <div className="p-3 rounded-lg bg-white/5 border border-green-500/50">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-4 h-4 text-green-400" />
            <span className="text-sm font-semibold text-green-400">Elite (250+)</span>
          </div>
          <span className="text-xs text-gray-400">Top performers</span>
        </div>
        <div className="p-3 rounded-lg bg-white/5 border border-green-400/50">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-4 h-4 text-green-300" />
            <span className="text-sm font-semibold text-green-300">High (200-249)</span>
          </div>
          <span className="text-xs text-gray-400">Strong impact</span>
        </div>
        <div className="p-3 rounded-lg bg-white/5 border border-yellow-500/50">
          <div className="flex items-center gap-2 mb-1">
            <Flame className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-semibold text-yellow-400">Medium (150-199)</span>
          </div>
          <span className="text-xs text-gray-400">Solid contributors</span>
        </div>
        <div className="p-3 rounded-lg bg-white/5 border border-red-500/50">
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <span className="text-sm font-semibold text-red-400">Low (&lt;150)</span>
          </div>
          <span className="text-xs text-gray-400">Developing players</span>
        </div>
      </div>
      
      {/* Key Matchups Section */}
      {matchups.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-yellow-400" />
            Key Matchups to Watch
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {matchups.map((matchup, idx) => (
              <MatchupCard
                key={idx}
                offensivePlayer={matchup.offensivePlayer}
                defensivePlayer={matchup.defensivePlayer}
              />
            ))}
          </div>
        </div>
      )}
      
      {/* Players Grid */}
      <div className="mb-4">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-gray-400" />
          All Players
        </h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
        {displayedPlayers.map((player, idx) => (
          <PlayerCard
            key={idx}
            player={player}
            teamLogo={player.teamData?.logo || ''}
            teamColor={player.teamData?.primary_color || player.teamData?.alt_color || '#3B82F6'}
            teamName={player.teamData?.name || ''}
          />
        ))}
      </div>
      
      {/* Show More Button */}
      {playerData.allPlayers.length > 12 && (
        <div className="text-center">
          <button
            onClick={() => setShowAllPlayers(!showAllPlayers)}
            className="px-6 py-3 rounded-xl text-sm font-bold font-orbitron transition-all hover:scale-105 border-2 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-purple-500/50 text-purple-400 hover:from-purple-500/30 hover:to-pink-500/30"
          >
            {showAllPlayers 
              ? `Show Top 12 Players` 
              : `View All ${playerData.allPlayers.length} Players`}
          </button>
        </div>
      )}
      
      {/* Database Stats Footer */}
      <div className="mt-6 pt-4 border-t border-white/10 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-3 bg-white/5 rounded border border-white/10">
          <Users className="w-5 h-5 text-gray-400 mx-auto mb-1" />
          <div className="text-xs text-gray-400">Total Players</div>
          <div className="text-lg font-bold text-white">{playerData.allPlayers.length}</div>
        </div>
        <div className="text-center p-3 bg-white/5 rounded border border-white/10">
          <Activity className="w-5 h-5 text-gray-400 mx-auto mb-1" />
          <div className="text-xs text-gray-400">QBs Analyzed</div>
          <div className="text-lg font-bold text-white">{playerData.databaseStats?.quarterbacks_analyzed || 0}</div>
        </div>
        <div className="text-center p-3 bg-white/5 rounded border border-white/10">
          <Activity className="w-5 h-5 text-gray-400 mx-auto mb-1" />
          <div className="text-xs text-gray-400">RBs Analyzed</div>
          <div className="text-lg font-bold text-white">{playerData.databaseStats?.running_backs_analyzed || 0}</div>
        </div>
        <div className="text-center p-3 bg-white/5 rounded border border-white/10">
          <Activity className="w-5 h-5 text-gray-400 mx-auto mb-1" />
          <div className="text-xs text-gray-400">WRs Analyzed</div>
          <div className="text-lg font-bold text-white">{playerData.databaseStats?.wide_receivers_analyzed || 0}</div>
        </div>
      </div>
    </div>
  );
}
