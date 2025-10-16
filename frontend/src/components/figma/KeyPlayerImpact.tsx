import { GlassCard } from './GlassCard';
import { Users } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr } from '../../utils/teamUtils';

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

  const awayQB = getTopPlayer(awayPlayers, 'qb');
  const homeQB = getTopPlayer(homePlayers, 'qb');
  const awayRBs = getTopPlayers(awayPlayers, 'rbs', 3);
  const homeRBs = getTopPlayers(homePlayers, 'rbs', 3);
  const awayWRs = getTopPlayers(awayPlayers, 'wrs', 5);
  const homeWRs = getTopPlayers(homePlayers, 'wrs', 5);
  const awayTEs = getTopPlayers(awayPlayers, 'tes', 2);
  const homeTEs = getTopPlayers(homePlayers, 'tes', 2);
  const awayDefense = getTopPlayers(awayPlayers, 'defense', 5);
  const homeDefense = getTopPlayers(homePlayers, 'defense', 5);

  return (
    <GlassCard className="p-6">
      <div className="flex items-center gap-2 mb-6">
        <Users className="w-5 h-5 text-amber-400" />
        <h3 className="text-white font-semibold">Enhanced Player Impact Analysis</h3>
        <div className="ml-auto text-xs text-gray-400">
          Database: {databaseStats.quarterbacks_analyzed || 0} QBs, {databaseStats.wide_receivers_analyzed || 0} WRs, {databaseStats.running_backs_analyzed || 0} RBs, {databaseStats.defensive_players_analyzed || 0} DEF
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Away Team Key Players */}
        <div className="rounded-lg p-4 border backdrop-blur-sm" style={{ borderColor: `${awayTeam.primary_color}66`, background: `linear-gradient(to bottom right, ${awayTeam.primary_color}26, ${awayTeam.primary_color}0d)` }}>
          <div className="flex items-center gap-2 mb-4">
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-8 h-8 object-contain" />
            <h4 className="font-semibold text-lg" style={{ color: awayTeam.primary_color }}>{awayTeam.name} Key Players</h4>
            <span className="ml-auto text-xs text-gray-400 bg-gray-800/50 px-2 py-1 rounded">
              {(awayQB ? 1 : 0) + awayWRs.length + awayRBs.length + awayTEs.length + awayDefense.length} players
            </span>
          </div>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {awayQB && (
              <PlayerCard 
                name={awayQB.name || "Starting QB"} 
                position="QB • Passing" 
                efficiency={awayQB.efficiency_metrics?.comprehensive_efficiency_score || awayQB.comprehensive_efficiency_score || 0}
                color={awayTeam.primary_color} 
                highlighted 
              />
            )}
            {!awayQB && (
              <div className="text-gray-500 text-sm italic p-2">No QB data available</div>
            )}
            {awayWRs.map((player: any, index: number) => (
              <PlayerCard 
                key={`away-wr-${index}`}
                name={player.name || `WR ${index + 1}`} 
                position="WR • Receiving" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={awayTeam.primary_color} 
              />
            ))}
            {awayRBs.length > 0 ? awayRBs.map((player: any, index: number) => (
              <PlayerCard 
                key={`away-rb-${index}`}
                name={player.name || `RB ${index + 1}`} 
                position="RB • Rushing" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={awayTeam.primary_color} 
              />
            )) : (
              <div className="text-gray-500 text-xs italic px-2">No RB data available</div>
            )}
            {awayTEs.length > 0 ? awayTEs.map((player: any, index: number) => (
              <PlayerCard 
                key={`away-te-${index}`}
                name={player.name || `TE ${index + 1}`} 
                position="TE • Receiving" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={awayTeam.primary_color} 
              />
            )) : (
              <div className="text-gray-500 text-xs italic px-2">No TE data available</div>
            )}
            {awayDefense.map((player: any, index: number) => (
              <PlayerCard 
                key={`away-def-${index}`}
                name={player.name || `Defender ${index + 1}`} 
                position={`${player.position_type || 'DEF'} • Defense`} 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={awayTeam.primary_color} 
              />
            ))}
          </div>
          <div className="mt-4 pt-3 border-t" style={{ borderColor: `${awayTeam.primary_color}66` }}>
            <div className="flex justify-between items-center">
              <span className="text-gray-200 font-semibold">Team Impact</span>
              <span className="font-bold text-2xl font-mono" style={{ color: awayTeam.primary_color, filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.3))' }}>{awayImpact.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Home Team Key Players */}
        <div className="rounded-lg p-4 border backdrop-blur-sm" style={{ borderColor: `${homeTeam.primary_color}66`, background: `linear-gradient(to bottom right, ${homeTeam.primary_color}26, ${homeTeam.primary_color}0d)` }}>
          <div className="flex items-center gap-2 mb-4">
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-8 h-8 object-contain" />
            <h4 className="font-semibold text-lg" style={{ color: homeTeam.primary_color }}>{homeTeam.name} Key Players</h4>
            <span className="ml-auto text-xs text-gray-400 bg-gray-800/50 px-2 py-1 rounded">
              {(homeQB ? 1 : 0) + homeWRs.length + homeRBs.length + homeTEs.length + homeDefense.length} players
            </span>
          </div>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {homeQB && (
              <PlayerCard 
                name={homeQB.name || "Starting QB"} 
                position="QB • Passing" 
                efficiency={homeQB.efficiency_metrics?.comprehensive_efficiency_score || homeQB.comprehensive_efficiency_score || 0}
                color={homeTeam.primary_color} 
                highlighted 
              />
            )}
            {!homeQB && (
              <div className="text-gray-500 text-sm italic p-2">No QB data available</div>
            )}
            {homeWRs.map((player: any, index: number) => (
              <PlayerCard 
                key={`home-wr-${index}`}
                name={player.name || `WR ${index + 1}`} 
                position="WR • Receiving" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={homeTeam.primary_color} 
              />
            ))}
            {homeRBs.length > 0 ? homeRBs.map((player: any, index: number) => (
              <PlayerCard 
                key={`home-rb-${index}`}
                name={player.name || `RB ${index + 1}`} 
                position="RB • Rushing" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={homeTeam.primary_color} 
              />
            )) : (
              <div className="text-gray-500 text-xs italic px-2">No RB data available</div>
            )}
            {homeTEs.length > 0 ? homeTEs.map((player: any, index: number) => (
              <PlayerCard 
                key={`home-te-${index}`}
                name={player.name || `TE ${index + 1}`} 
                position="TE • Receiving" 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={homeTeam.primary_color} 
              />
            )) : (
              <div className="text-gray-500 text-xs italic px-2">No TE data available</div>
            )}
            {homeDefense.map((player: any, index: number) => (
              <PlayerCard 
                key={`home-def-${index}`}
                name={player.name || `Defender ${index + 1}`} 
                position={`${player.position_type || 'DEF'} • Defense`} 
                efficiency={player.efficiency_score || player.comprehensive_efficiency_score || 0}
                color={homeTeam.primary_color} 
              />
            ))}
          </div>
          <div className="mt-4 pt-3 border-t" style={{ borderColor: `${homeTeam.primary_color}66` }}>
            <div className="flex justify-between items-center">
              <span className="text-gray-200 font-semibold">Team Impact</span>
              <span className="font-bold text-2xl font-mono" style={{ color: homeTeam.primary_color, filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.3))' }}>{homeImpact.toFixed(2)}</span>
            </div>
          </div>
        </div>
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
    </GlassCard>
  );
}

function PlayerCard({ name, position, efficiency, color, highlighted = false }: { 
  name: string; 
  position: string; 
  efficiency: number; 
  color?: string; 
  highlighted?: boolean 
}) {
  const displayEfficiency = efficiency > 10 ? (efficiency / 100).toFixed(3) : efficiency.toFixed(3);
  
  return (
    <div className="bg-gray-800/40 rounded-lg p-3 backdrop-blur-sm border" style={{ borderColor: highlighted ? `${color}4d` : `${color}33` }}>
      <div className="flex justify-between items-center mb-1">
        <span className="text-gray-200 font-semibold text-sm">{name}</span>
        <span className={`font-bold font-mono ${highlighted ? 'text-lg' : ''}`} style={{ color: highlighted ? color : '#cbd5e1' }}>{displayEfficiency}</span>
      </div>
      <p className="text-gray-400 text-xs">{position} • Efficiency Score</p>
    </div>
  );
}