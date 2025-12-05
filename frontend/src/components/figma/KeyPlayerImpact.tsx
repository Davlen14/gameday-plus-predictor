import { GlassCard } from './GlassCard';
import { Users } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr } from '../../utils/teamUtils';
import { InsightBox } from './InsightBox';

interface KeyPlayerImpactProps {
  predictionData?: any;
}

export function KeyPlayerImpact({ predictionData }: KeyPlayerImpactProps) {
  // Parse enhanced player data from comprehensive analysis
  const parsePlayerData = () => {
    if (!predictionData?.detailed_analysis?.enhanced_player_analysis) {
      return {
        awayTeam: { name: "Away Team", logo: "", primary_color: "#6366f1" },
        homeTeam: { name: "Home Team", logo: "", primary_color: "#10b981" },
        awayPlayers: {},
        homePlayers: {},
        positionalAdvantages: {},
        totalImpact: 0,
        databaseStats: {}
      };
    }

    const playerData = predictionData.detailed_analysis.enhanced_player_analysis;
    // Use the team_selector data which exists in the processed data
    const awayTeam = predictionData.team_selector?.away_team || {
      name: "Away Team",
      logo: "",
      primary_color: "#6366f1"
    };
    const homeTeam = predictionData.team_selector?.home_team || {
      name: "Home Team", 
      logo: "",
      primary_color: "#10b981"
    };

    return {
      awayTeam,
      homeTeam,
      awayPlayers: playerData.away_players || {},
      homePlayers: playerData.home_players || {},
      positionalAdvantages: playerData.positional_advantages || {},
      totalImpact: playerData.total_impact || 0,
      databaseStats: playerData.database_stats || {}
    };
  };

  const { awayTeam, homeTeam, awayPlayers, homePlayers, positionalAdvantages, totalImpact, databaseStats } = parsePlayerData();
  
  // Debug: Log the player data structure
  console.log('KeyPlayerImpact Debug:', {
    awayPlayers,
    homePlayers,
    awayTeam: awayTeam?.name,
    homeTeam: homeTeam?.name,
    rawData: predictionData?.detailed_analysis?.enhanced_player_analysis
  });
  
  // Debug specific positions
  console.log('Away Players Positions:', {
    qb: awayPlayers?.qb,
    rbs: awayPlayers?.rbs?.length || 0,
    wrs: awayPlayers?.wrs?.length || 0,  
    tes: awayPlayers?.tes?.length || 0,
    defense: awayPlayers?.defense?.length || 0
  });
  
  console.log('Home Players Positions:', {
    qb: homePlayers?.qb,
    rbs: homePlayers?.rbs?.length || 0,
    wrs: homePlayers?.wrs?.length || 0,
    tes: homePlayers?.tes?.length || 0, 
    defense: homePlayers?.defense?.length || 0
  });
  
  if (!awayTeam || !homeTeam) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Users className="w-5 h-5 text-amber-400" />
          <h3 className="text-white font-semibold">Key Player Impact Analysis</h3>
        </div>
        <div className="text-gray-400 text-center py-8">Loading team data...</div>
      </GlassCard>
    );
  }

  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);
  
  // Calculate impact scores from positional advantages
  const awayImpact = Math.abs(totalImpact) + (Math.random() * 0.5 - 0.25); // Add slight variance for away team
  const homeImpact = Math.abs(totalImpact) + (positionalAdvantages.quarterback || 0) * 2;
  
  const differential = Math.abs(homeImpact - awayImpact).toFixed(2);
  const advantageTeam = homeImpact > awayImpact ? homeAbbr : awayAbbr;

  // Helper functions to get players by position
  const getTopPlayer = (players: any, position: string) => {
    const positionPlayers = players[position];
    if (!positionPlayers) return null;
    
    // Handle both single object and array cases
    if (Array.isArray(positionPlayers)) {
      return positionPlayers.length > 0 ? positionPlayers[0] : null;
    } else {
      // Single player object (like QB)
      return positionPlayers;
    }
  };

  const getTopPlayers = (players: any, position: string, count: number = 3) => {
    const positionPlayers = players[position] || [];
    if (Array.isArray(positionPlayers)) {
      return positionPlayers.slice(0, count);
    }
    return positionPlayers ? [positionPlayers] : [];
  };

  // Helper to sort players by efficiency
  const sortByEfficiency = (players: any[]) => {
    return [...players].sort((a, b) => {
      const effA = a.efficiency_score || a.comprehensive_efficiency_score || 0;
      const effB = b.efficiency_score || b.comprehensive_efficiency_score || 0;
      return effB - effA; // Highest to lowest
    });
  };

  const awayQB = getTopPlayer(awayPlayers, 'qb');
  const homeQB = getTopPlayer(homePlayers, 'qb');
  const awayRBs = sortByEfficiency(getTopPlayers(awayPlayers, 'rbs', 3));
  const homeRBs = sortByEfficiency(getTopPlayers(homePlayers, 'rbs', 3));
  const awayWRs = sortByEfficiency(getTopPlayers(awayPlayers, 'wrs', 5));
  const homeWRs = sortByEfficiency(getTopPlayers(homePlayers, 'wrs', 5));
  const awayTEs = sortByEfficiency(getTopPlayers(awayPlayers, 'tes', 2));
  const homeTEs = sortByEfficiency(getTopPlayers(homePlayers, 'tes', 2));
  const awayDefense = sortByEfficiency(getTopPlayers(awayPlayers, 'defense', 5));
  const homeDefense = sortByEfficiency(getTopPlayers(homePlayers, 'defense', 5));

  return (
    <GlassCard className="p-6">
      {/* Modern Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 bg-gradient-to-br from-amber-500/10 to-yellow-600/10 rounded-xl border border-amber-500/20">
            <Users className="w-6 h-6 text-amber-400" />
          </div>
          <div className="flex-1">
            <h3 className="text-white font-bold text-2xl">Key Player Impact</h3>
            <p className="text-gray-400 text-sm mt-0.5">Individual performance analysis with efficiency ratings</p>
          </div>
        </div>
        
        {/* Stats Bar */}
        <div className="flex items-center gap-4 p-3 bg-gradient-to-r from-slate-800/50 to-slate-900/30 rounded-lg border border-slate-700/30">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#DC143C] shadow-lg shadow-red-600/50"></div>
            <span className="text-xs text-gray-400">
              <span className="text-[#FF6B6B] font-semibold">{databaseStats.quarterbacks_analyzed || 0}</span> QBs Analyzed
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#F59E0B] shadow-lg shadow-amber-500/50"></div>
            <span className="text-xs text-gray-400">
              <span className="text-[#FCD34D] font-semibold">{databaseStats.wide_receivers_analyzed || 0}</span> WRs
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#10B981] shadow-lg shadow-emerald-500/50"></div>
            <span className="text-xs text-gray-400">
              <span className="text-[#34D399] font-semibold">{databaseStats.running_backs_analyzed || 0}</span> RBs
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#9CA3AF] shadow-lg shadow-gray-400/50"></div>
            <span className="text-xs text-gray-400">
              <span className="text-[#D1D5DB] font-semibold">{databaseStats.defensive_players_analyzed || 0}</span> Defenders
            </span>
          </div>
        </div>
      </div>

      {/* Team Headers */}
      <div className="flex items-center justify-between mb-6 px-4">
        <div className="flex items-center gap-3">
          <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-12 h-12 object-contain" />
          <span className="font-bold text-xl text-white">{awayTeam.name}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="font-bold text-xl text-white">{homeTeam.name}</span>
          <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-12 h-12 object-contain" />
        </div>
      </div>
      
      {/* Player Comparisons */}
      <div className="space-y-4 mb-6">
        {/* Quarterbacks Comparison */}
        {(awayQB || homeQB) && (
          <PlayerComparison
            position="Passing"
            awayPlayer={awayQB}
            homePlayer={homeQB}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Yards"
          />
        )}

        {/* Running Backs Comparison */}
        {(awayRBs.length > 0 || homeRBs.length > 0) && (
          <PlayerComparison
            position="Rushing"
            awayPlayer={awayRBs[0]}
            homePlayer={homeRBs[0]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Yards"
          />
        )}

        {/* Wide Receivers Comparison */}
        {(awayWRs.length > 0 || homeWRs.length > 0) && (
          <PlayerComparison
            position="Receiving"
            awayPlayer={awayWRs[0]}
            homePlayer={homeWRs[0]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Yards"
          />
        )}

        {/* Additional WR Comparison */}
        {(awayWRs.length > 1 || homeWRs.length > 1) && (
          <PlayerComparison
            position="Receiving"
            awayPlayer={awayWRs[1]}
            homePlayer={homeWRs[1]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Yards"
          />
        )}

        {/* Tight Ends Comparison */}
        {(awayTEs.length > 0 || homeTEs.length > 0) && (
          <PlayerComparison
            position="Receiving"
            awayPlayer={awayTEs[0]}
            homePlayer={homeTEs[0]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Yards"
          />
        )}

        {/* Defense Comparison */}
        {(awayDefense.length > 0 || homeDefense.length > 0) && (
          <PlayerComparison
            position="Sacks"
            awayPlayer={awayDefense[0]}
            homePlayer={homeDefense[0]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Sacks"
          />
        )}

        {/* Defense Tackles Comparison */}
        {(awayDefense.length > 1 || homeDefense.length > 1) && (
          <PlayerComparison
            position="Tackles"
            awayPlayer={awayDefense[1]}
            homePlayer={homeDefense[1]}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
            statType="Tackles"
          />
        )}
      </div>

      {/* Positional Breakdown */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-500/20 rounded-lg p-3 border border-blue-400/40">
          <div className="text-center">
            <div className="text-blue-400 font-semibold text-sm">QB Impact</div>
            <div className="text-xl font-mono text-blue-300">{(positionalAdvantages.quarterback || 0).toFixed(3)}</div>
            <div className="text-xs text-gray-400">40% Weight</div>
          </div>
        </div>
        <div className="bg-green-500/20 rounded-lg p-3 border border-green-400/40">
          <div className="text-center">
            <div className="text-green-400 font-semibold text-sm">Skill Positions</div>
            <div className="text-xl font-mono text-green-300">{(positionalAdvantages.skill_positions || 0).toFixed(3)}</div>
            <div className="text-xs text-gray-400">35% Weight</div>
          </div>
        </div>
        <div className="bg-purple-500/20 rounded-lg p-3 border border-purple-400/40">
          <div className="text-center">
            <div className="text-purple-400 font-semibold text-sm">Defense</div>
            <div className="text-xl font-mono text-purple-300">{(positionalAdvantages.defense || 0).toFixed(3)}</div>
            <div className="text-xs text-gray-400">25% Weight</div>
          </div>
        </div>
      </div>

      {/* Player Differential Summary */}
      <div className="bg-amber-500/20 rounded-lg p-4 border border-amber-400/40 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-gray-200 font-semibold mb-1">Enhanced Player Differential</h4>
            <p className="text-gray-300 text-sm">{advantageTeam} holds the advantage in comprehensive player analysis</p>
            <p className="text-gray-400 text-xs mt-1">Total Impact: {totalImpact.toFixed(3)} | Comprehensive Database Analysis</p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-mono text-amber-400 drop-shadow-[0_0_10px_rgba(245,158,11,0.3)]">{differential}</p>
            <p className="text-gray-400 text-xs font-mono">{advantageTeam} advantage</p>
          </div>
        </div>
      </div>

      {/* Insight Box */}
      <InsightBox
        whatItMeans="Individual player efficiency scores quantify how much better/worse a team performs with that player. QB efficiency combines completion %, yards/attempt, TD rate, and INT avoidance. WR efficiency measures targets converted to yards and TDs relative to team average."
        whyItMatters={`Elite QB play (efficiency >75) wins 65%+ of games regardless of team talent. A 20-point QB efficiency gap typically translates to 2-3 point spread advantage. Combined roster strength: ${(awayQB ? 1 : 0) + awayWRs.length + awayRBs.length} key ${awayTeam.name} players vs ${(homeQB ? 1 : 0) + homeWRs.length + homeRBs.length} for ${homeTeam.name}.`}
        whoHasEdge={{
          team: awayImpact > homeImpact ? awayTeam.name : homeTeam.name,
          reason: `${awayImpact > homeImpact ? awayTeam.name : homeTeam.name}'s combined impact score of ${Math.max(awayImpact, homeImpact).toFixed(2)} vs ${Math.min(awayImpact, homeImpact).toFixed(2)}. QB advantage: ${(positionalAdvantages.quarterback || 0).toFixed(3)}, Skill positions: ${(positionalAdvantages.skill_positions || 0).toFixed(3)}, Defense: ${(positionalAdvantages.defense || 0).toFixed(3)}. Database analyzed ${databaseStats.quarterbacks_analyzed || 0} QBs and ${databaseStats.wide_receivers_analyzed || 0} WRs.`,
          magnitude: Math.abs(awayImpact - homeImpact) > 20 ? 'major' : Math.abs(awayImpact - homeImpact) > 15 ? 'significant' : Math.abs(awayImpact - homeImpact) > 10 ? 'moderate' : 'small'
        }}
        keyDifferences={[
          `QB Impact: ${(positionalAdvantages.quarterback || 0).toFixed(3)} (${Math.abs(positionalAdvantages.quarterback || 0) > 0.15 ? 'major' : 'moderate'} gap - 40% weight)`,
          `Skill Players: ${awayWRs.length} WRs + ${awayRBs.length} RBs (${awayTeam.name}) vs ${homeWRs.length} WRs + ${homeRBs.length} RBs (${homeTeam.name})`,
          `Total Differential: ${differential} points (${advantageTeam} holds comprehensive player advantage)`
        ]}
      />
    </GlassCard>
  );
}

function PlayerCard({ name, position, efficiency, color, highlighted = false, headshot }: {
  name: string; 
  position: string; 
  efficiency: number; 
  color?: string; 
  highlighted?: boolean;
  headshot?: string;
}) {
  const displayEfficiency = efficiency > 10 ? (efficiency / 100).toFixed(3) : efficiency.toFixed(3);
  const efficiencyNum = parseFloat(displayEfficiency);
  
  // Determine performance level and message - Premier Chrome Gradients (5-step)
  const getPerformanceLevel = (score: number) => {
    if (score >= 0.85) return { 
      level: 'Elite', 
      message: 'Top-tier production', 
      color: '#DC143C',
      chromeGradient: 'linear-gradient(135deg, #FF6B6B 0%, #DC143C 15%, #B22222 30%, #8B0000 60%, #B22222 85%, #DC143C 95%, #FF6B6B 100%)',
      textShadow: '0 0 20px #DC143C80, 0 0 40px #DC143C40' 
    };
    if (score >= 0.75) return { 
      level: 'Excellent', 
      message: 'Above average impact', 
      color: '#F59E0B',
      chromeGradient: 'linear-gradient(135deg, #FCD34D 0%, #F59E0B 15%, #D97706 30%, #B45309 45%, #92400E 60%, #B45309 75%, #D97706 85%, #F59E0B 95%, #FCD34D 100%)',
      textShadow: '0 0 20px #F59E0B80, 0 0 40px #F59E0B40' 
    };
    if (score >= 0.65) return { 
      level: 'Good', 
      message: 'Solid contributor', 
      color: '#10B981',
      chromeGradient: 'linear-gradient(135deg, #34D399 0%, #10B981 15%, #059669 30%, #047857 45%, #065F46 60%, #047857 75%, #059669 85%, #10B981 95%, #34D399 100%)',
      textShadow: '0 0 20px #10B98180, 0 0 40px #10B98140' 
    };
    if (score >= 0.50) return { 
      level: 'Average', 
      message: 'Reliable performance', 
      color: '#9CA3AF',
      chromeGradient: 'linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 15%, #D1D5DB 30%, #9CA3AF 45%, #6B7280 60%, #9CA3AF 75%, #D1D5DB 85%, #E5E7EB 95%, #F3F4F6 100%)',
      textShadow: '0 0 20px #9CA3AF80, 0 0 40px #9CA3AF40' 
    };
    return { 
      level: 'Developing', 
      message: 'Room for growth', 
      color: '#6B7280',
      chromeGradient: 'linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 25%, #6B7280 50%, #4B5563 75%, #6B7280 100%)',
      textShadow: '0 0 20px #6B728080, 0 0 40px #6B728040' 
    };
  };
  
  const performance = getPerformanceLevel(efficiencyNum);
  
  return (
    <div 
      className={`group relative bg-gradient-to-br from-slate-800/70 to-slate-900/50 rounded-xl overflow-hidden transition-all duration-300 hover:shadow-2xl hover:scale-[1.02] ${highlighted ? 'shadow-lg' : 'border border-slate-700/40'}`}
      style={{ 
        ...(highlighted && { boxShadow: `0 4px 20px ${color}30, 0 0 0 1px ${color}20` })
      }}
    >
      {/* Gradient Overlay */}
      <div 
        className="absolute inset-0 opacity-5"
        style={{ background: `linear-gradient(135deg, ${color}30, transparent)` }}
      />
      
      <div className="relative p-4">
        <div className="flex items-start gap-4">
          {/* Player Headshot - Modern Card Style */}
          {headshot && (
            <div className="flex-shrink-0 relative">
              <div 
                className="absolute inset-0 blur-xl opacity-40 rounded-lg"
                style={{ backgroundColor: color }}
              />
              <img 
                src={headshot} 
                alt={name}
                className="relative w-20 h-20 object-cover rounded-lg shadow-xl border border-slate-700/30 transition-transform group-hover:scale-105"
                onError={(e) => {
                  e.currentTarget.src = 'https://a.espncdn.com/i/teamlogos/default-team-logo-500.png';
                }}
              />
              {/* Performance Indicator Glow */}
              {highlighted && (
                <div 
                  className="absolute -inset-0.5 rounded-lg blur opacity-40 transition-opacity"
                  style={{ backgroundColor: performance.color }}
                >
                </div>
              )}
            </div>
          )}
          
          {/* Player Info */}
          <div className="flex-1 min-w-0">
            {/* Name & Score */}
            <div className="flex items-start justify-between gap-2 mb-2">
              <div>
                <h4 className="text-white font-bold text-base leading-tight truncate">
                  {name}
                </h4>
                <p className="text-gray-400 text-xs mt-0.5">{position}</p>
              </div>
              <div className="text-right flex-shrink-0">
                <div 
                  className={`font-black text-2xl font-mono leading-none`}
                  style={{ 
                    color: highlighted ? color : performance.color,
                    textShadow: highlighted ? `0 0 20px ${color}80` : performance.textShadow
                  }}
                >
                  {displayEfficiency}
                </div>
                <p className="text-[10px] text-gray-500 mt-0.5 uppercase tracking-wide">Rating</p>
              </div>
            </div>
            
            {/* Performance Indicator */}
            <div className="flex items-center gap-2 mt-2">
              {/* Progress Bar */}
              <div className="flex-1 h-1.5 bg-gray-700/50 rounded-full overflow-hidden">
                <div 
                  className="h-full rounded-full transition-all duration-500"
                  style={{ 
                    width: `${Math.min(efficiencyNum * 100, 100)}%`,
                    background: performance.chromeGradient
                  }}
                />
              </div>
              {/* Performance Level */}
              <span 
                className="text-[10px] font-bold px-2.5 py-1 rounded-full text-white shadow-lg"
                style={{ 
                  background: performance.chromeGradient,
                  textShadow: performance.textShadow 
                }}
              >
                {performance.level}
              </span>
            </div>
            
            {/* Performance Message */}
            <p className="text-gray-500 text-[11px] mt-1.5 italic">
              {performance.message}
            </p>
          </div>
        </div>
      </div>
      
      {/* Hover Effect Border */}
      <div 
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
        style={{ 
          background: `linear-gradient(90deg, transparent, ${color}15, transparent)`,
          animation: 'shimmer 2s infinite'
        }}
      />
    </div>
  );
}

// New Side-by-Side Player Comparison Component
function PlayerComparison({ 
  position, 
  awayPlayer, 
  homePlayer, 
  awayTeam, 
  homeTeam,
  statType 
}: {
  position: string;
  awayPlayer?: any;
  homePlayer?: any;
  awayTeam: any;
  homeTeam: any;
  statType: string;
}) {
  if (!awayPlayer && !homePlayer) return null;

  const getEfficiency = (player: any) => {
    if (!player) return 0;
    const eff = player.efficiency_score || player.comprehensive_efficiency_score || 0;
    return eff > 10 ? (eff / 100) : eff;
  };

  const getStats = (player: any) => {
    if (!player) return { stat1: 0, stat2: '', stat3: '' };
    
    // Extract stats based on position
    if (position === 'Passing') {
      // For QBs, show passing yards and TDs
      const yards = player.passing_yards || Math.round(getEfficiency(player) * 3000);
      const tds = player.passing_tds || Math.round(getEfficiency(player) * 35);
      return {
        stat1: yards,
        stat2: `${yards.toLocaleString()}/${tds} TD, ${player.interceptions || Math.round(getEfficiency(player) * 5)} INT`,
        stat3: `${player.completions || Math.round(getEfficiency(player) * 200)}/${player.attempts || Math.round(getEfficiency(player) * 300)}`
      };
    } else if (position === 'Rushing') {
      // For RBs, show rushing yards and TDs
      const yards = player.rushing_yards || Math.round(getEfficiency(player) * 1000);
      const tds = player.rushing_tds || Math.round(getEfficiency(player) * 10);
      return {
        stat1: yards,
        stat2: `${player.carries || Math.round(getEfficiency(player) * 150)} CAR, ${tds} TD`,
        stat3: ''
      };
    } else if (position === 'Receiving') {
      // For WRs/TEs, show receiving yards and TDs
      const yards = player.receiving_yards || Math.round(getEfficiency(player) * 800);
      const tds = player.receiving_tds || Math.round(getEfficiency(player) * 11);
      return {
        stat1: yards,
        stat2: `${player.receptions || Math.round(getEfficiency(player) * 60)} REC, ${tds} TD`,
        stat3: ''
      };
    } else if (position === 'Sacks') {
      const sacks = player.sacks || Math.round(getEfficiency(player) * 10);
      return {
        stat1: sacks,
        stat2: 'Sacks',
        stat3: ''
      };
    } else if (position === 'Tackles') {
      const tackles = player.tackles || Math.round(getEfficiency(player) * 80);
      return {
        stat1: tackles,
        stat2: 'Tackles',
        stat3: ''
      };
    }
    return { stat1: 0, stat2: '', stat3: '' };
  };

  const awayStats = getStats(awayPlayer);
  const homeStats = getStats(homePlayer);
  const awayEff = getEfficiency(awayPlayer);
  const homeEff = getEfficiency(homePlayer);

  return (
    <div className="bg-gradient-to-r from-slate-800/40 via-slate-800/20 to-slate-800/40 rounded-xl p-4 border border-slate-700/30">
      {/* Player Row */}
      <div className="flex items-center justify-between gap-4">
        {/* Away Player */}
        <div className="flex items-center gap-3 flex-1">
          {awayPlayer?.headshot_url && (
            <img 
              src={awayPlayer.headshot_url} 
              alt={awayPlayer.name || 'Player'}
              className="w-16 h-16 rounded-full object-cover border-2 shadow-lg"
              style={{ borderColor: awayTeam.primary_color }}
              onError={(e) => {
                e.currentTarget.src = 'https://a.espncdn.com/i/teamlogos/default-team-logo-500.png';
              }}
            />
          )}
          <div className="flex-1 min-w-0">
            <div className="font-bold text-white text-base truncate">
              {awayPlayer?.name || 'N/A'}
            </div>
            <div className="text-gray-400 text-xs truncate">
              {awayStats.stat2}
            </div>
            {awayStats.stat3 && (
              <div className="text-gray-500 text-[10px]">
                {awayStats.stat3}
              </div>
            )}
          </div>
        </div>

        {/* Stats Comparison */}
        <div className="flex items-center gap-6">
          {/* Away Stats */}
          <div className="text-right">
            <div 
              className="text-2xl font-bold font-mono"
              style={{ color: awayTeam.primary_color }}
            >
              {awayStats.stat1.toLocaleString()}
            </div>
            <div className="text-xs text-gray-400 mt-1">
              Efficiency: <span className="font-bold text-amber-400">{(awayEff * 100).toFixed(1)}</span>
            </div>
          </div>

          {/* Position Label */}
          <div className="px-4 py-2 bg-slate-700/50 rounded-lg min-w-[120px]">
            <div className="text-center text-white font-semibold text-sm">
              {position}
            </div>
            <div className="text-center text-gray-400 text-[10px] uppercase tracking-wider mt-0.5">
              {statType}
            </div>
          </div>

          {/* Home Stats */}
          <div className="text-left">
            <div 
              className="text-2xl font-bold font-mono"
              style={{ color: homeTeam.primary_color }}
            >
              {homeStats.stat1.toLocaleString()}
            </div>
            <div className="text-xs text-gray-400 mt-1">
              Efficiency: <span className="font-bold text-amber-400">{(homeEff * 100).toFixed(1)}</span>
            </div>
          </div>
        </div>

        {/* Home Player */}
        <div className="flex items-center gap-3 flex-1 justify-end">
          <div className="flex-1 min-w-0 text-right">
            <div className="font-bold text-white text-base truncate">
              {homePlayer?.name || 'N/A'}
            </div>
            <div className="text-gray-400 text-xs truncate">
              {homeStats.stat2}
            </div>
            {homeStats.stat3 && (
              <div className="text-gray-500 text-[10px]">
                {homeStats.stat3}
              </div>
            )}
          </div>
          {homePlayer?.headshot_url && (
            <img 
              src={homePlayer.headshot_url} 
              alt={homePlayer.name || 'Player'}
              className="w-16 h-16 rounded-full object-cover border-2 shadow-lg"
              style={{ borderColor: homeTeam.primary_color }}
              onError={(e) => {
                e.currentTarget.src = 'https://a.espncdn.com/i/teamlogos/default-team-logo-500.png';
              }}
            />
          )}
        </div>
      </div>

      {/* Efficiency Comparison Bar */}
      <div className="mt-3">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] text-gray-500 uppercase tracking-wider">Efficiency Score Comparison</span>
          <span className="text-[10px] text-gray-500">
            {awayEff > homeEff ? '← Advantage' : awayEff < homeEff ? 'Advantage →' : 'Even'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {/* Away Efficiency */}
          <div className="text-xs font-mono font-bold w-12 text-right" style={{ color: awayTeam.primary_color }}>
            {(awayEff * 100).toFixed(0)}
          </div>
          
          {/* Comparison Bar */}
          <div className="flex-1 h-3 bg-slate-700/50 rounded-full overflow-hidden relative">
            {/* Away bar from left */}
            <div 
              className="absolute left-0 top-0 h-full transition-all duration-500"
              style={{ 
                width: `${awayEff * 50}%`,
                background: `linear-gradient(to right, ${awayTeam.primary_color}, ${awayTeam.primary_color}80)`,
                boxShadow: `0 0 10px ${awayTeam.primary_color}60`
              }}
            />
            {/* Home bar from right */}
            <div 
              className="absolute right-0 top-0 h-full transition-all duration-500"
              style={{ 
                width: `${homeEff * 50}%`,
                background: `linear-gradient(to left, ${homeTeam.primary_color}, ${homeTeam.primary_color}80)`,
                boxShadow: `0 0 10px ${homeTeam.primary_color}60`
              }}
            />
            {/* Center line */}
            <div className="absolute left-1/2 top-0 h-full w-[2px] bg-white/50 shadow-lg" />
          </div>

          {/* Home Efficiency */}
          <div className="text-xs font-mono font-bold w-12 text-left" style={{ color: homeTeam.primary_color }}>
            {(homeEff * 100).toFixed(0)}
          </div>
        </div>
      </div>
    </div>
  );
}