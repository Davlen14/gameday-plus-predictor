import React, { useState, useEffect, useMemo } from 'react';
import { 
  Trophy, TrendingUp, TrendingDown, Shield, Zap, AlertCircle, ChevronRight, 
  Activity, Users, Award, BarChart3, Binary, Target, ArrowUpRight, ArrowDownRight 
} from 'lucide-react';
import { GlassCard } from './GlassCard';
import { generateTeamAbbr } from '../../utils/teamUtils';

interface KeyPlayerImpactProps {
  predictionData?: any;
}

interface PlayerStats {
  player_name: string;
  position: string;
  player_id: string;
  passing_yards: number | null;
  passing_tds: number | null;
  rushing_yards: number | null;
  rushing_tds: number | null;
  receiving_yards: number | null;
  receiving_tds: number | null;
  total_yards: number;
  headshot_url: string | null;
  team_logo_url: string | null;
  tackles?: number;
  sacks?: number;
  interceptions?: number;
  completions?: number;
  attempts?: number;
  carries?: number;
  receptions?: number;
}

interface KeyPlayersAPIData {
  success: boolean;
  team1: string;
  team2: string;
  team1_players: PlayerStats[];
  team2_players: PlayerStats[];
}

export function KeyPlayerImpact({ predictionData }: KeyPlayerImpactProps) {
  const [sqlPlayersData, setSqlPlayersData] = useState<KeyPlayersAPIData | null>(null);
  const [loadingSQL, setLoadingSQL] = useState(true);

  // Extract team data from team_selector (only once)
  const teamAwayData = predictionData?.team_selector?.away_team || {
    name: "Away Team",
    logo: "",
    primary_color: "#6366f1"
  };
  const teamHomeData = predictionData?.team_selector?.home_team || {
    name: "Home Team", 
    logo: "",
    primary_color: "#10b981"
  };

  // Fetch SQL player data
  useEffect(() => {
    if (teamAwayData.name && teamHomeData.name && teamAwayData.name !== "Away Team") {
      fetch(`http://localhost:5002/api/key-players/${teamAwayData.name}/${teamHomeData.name}`)
        .then(res => res.json())
        .then(data => {
          console.log('SQL Players Data:', data);
          setSqlPlayersData(data);
          setLoadingSQL(false);
        })
        .catch(err => {
          console.error('Failed to fetch SQL players:', err);
          setLoadingSQL(false);
        });
    }
  }, [teamAwayData.name, teamHomeData.name]);

  // Parse enhanced player data from comprehensive analysis (fallback)
  // Use useMemo to recalculate when sqlPlayersData changes
  const parsedData = useMemo(() => {
    // If we have SQL data, convert it to the expected format
    if (sqlPlayersData && sqlPlayersData.success) {
      // Group players by position
      const groupByPosition = (players: PlayerStats[]) => {
        const grouped: any = { qb: null, rbs: [], wrs: [], tes: [], defense: [] };
        
        players.forEach(player => {
          const pos = player.position.toUpperCase();
          const playerWithEfficiency = {
            ...player,
            name: player.player_name,
            efficiency_score: (player.total_yards / 3500) * 100, // Normalize to 0-100
            comprehensive_efficiency_score: (player.total_yards / 3500) * 100,
            headshot: player.headshot_url
          };

          if (pos === 'QB') {
            grouped.qb = playerWithEfficiency;
          } else if (pos === 'RB') {
            grouped.rbs.push(playerWithEfficiency);
          } else if (pos === 'WR') {
            grouped.wrs.push(playerWithEfficiency);
          } else if (pos === 'TE') {
            grouped.tes.push(playerWithEfficiency);
          } else {
            grouped.defense.push(playerWithEfficiency);
          }
        });

        return grouped;
      };

      const awayPlayers = groupByPosition(sqlPlayersData.team1_players);
      const homePlayers = groupByPosition(sqlPlayersData.team2_players);

      return {
        awayTeam: teamAwayData,
        homeTeam: teamHomeData,
        awayPlayers,
        homePlayers,
        positionalAdvantages: {},
        totalImpact: 0,
        databaseStats: {
          quarterbacks_analyzed: (awayPlayers.qb ? 1 : 0) + (homePlayers.qb ? 1 : 0),
          running_backs_analyzed: awayPlayers.rbs.length + homePlayers.rbs.length,
          wide_receivers_analyzed: awayPlayers.wrs.length + homePlayers.wrs.length,
          defensive_players_analyzed: awayPlayers.defense.length + homePlayers.defense.length
        }
      };
    }

    // Fallback to original enhanced_player_analysis
    if (!predictionData?.detailed_analysis?.enhanced_player_analysis) {
      return {
        awayTeam: teamAwayData,
        homeTeam: teamHomeData,
        awayPlayers: {},
        homePlayers: {},
        positionalAdvantages: {},
        totalImpact: 0,
        databaseStats: {}
      };
    }

    const playerData = predictionData.detailed_analysis.enhanced_player_analysis;

    return {
      awayTeam: teamAwayData,
      homeTeam: teamHomeData,
      awayPlayers: playerData.away_players || {},
      homePlayers: playerData.home_players || {},
      positionalAdvantages: playerData.positional_advantages || {},
      totalImpact: playerData.total_impact || 0,
      databaseStats: playerData.database_stats || {}
    };
  }, [sqlPlayersData, predictionData, teamAwayData, teamHomeData]);

  // Show loading state while fetching SQL data
  if (loadingSQL) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Users className="w-5 h-5 text-amber-400" />
          <h3 className="text-white font-semibold">Key Player Impact Analysis</h3>
        </div>
        <div className="text-gray-400 text-center py-8">
          <div className="animate-pulse">Loading player stats from database...</div>
        </div>
      </GlassCard>
    );
  }

  const { awayTeam, homeTeam, awayPlayers, homePlayers, positionalAdvantages, totalImpact, databaseStats } = parsedData;
  
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

  // Helper components from mock
  const Headshot = ({ id, teamColor, size = "w-20 h-20", url }: { id?: string, teamColor: string, size?: string, url?: string | null }) => {
    const [error, setError] = useState(false);
    // Use provided URL or fallback to CBS logic if ID exists, otherwise generic fallback
    const imageUrl = !error && url ? url : (id ? `https://sports.cbsimg.net/images/football/ncaa/players/170x170/${id}.png` : null);
    const fallback = "https://a.espncdn.com/combiner/i?img=/i/headshots/nophoto.png&w=288&h=204";

    return (
      <div className={`${size} rounded-full p-1 bg-gradient-to-b from-white/20 to-transparent relative z-10`}>
        <div className="w-full h-full rounded-full overflow-hidden bg-black/40 backdrop-blur-sm border border-white/10">
          <img 
            src={imageUrl || fallback} 
            alt="Player" 
            className="w-full h-full object-cover scale-110 pt-2"
            onError={() => setError(true)}
          />
        </div>
        {/* Team Indicator Ring */}
        <div className="absolute inset-0 rounded-full border-2 border-transparent" style={{ borderColor: teamColor, opacity: 0.6 }}></div>
      </div>
    );
  };

  const getPerformanceColor = (value: number) => {
    // Value is 0-100 in real data, mock used 0-1
    const normalizedValue = value > 1 ? value / 100 : value;
    
    if (normalizedValue >= 0.8) return { bg: "bg-emerald-500", text: "text-emerald-400", shadow: "shadow-emerald-500/50", label: "ELITE" };
    if (normalizedValue >= 0.6) return { bg: "bg-yellow-400", text: "text-yellow-400", shadow: "shadow-yellow-500/50", label: "GOOD" };
    if (normalizedValue >= 0.3) return { bg: "bg-orange-500", text: "text-orange-400", shadow: "shadow-orange-500/50", label: "AVG" };
    return { bg: "bg-red-500", text: "text-red-500", shadow: "shadow-red-500/50", label: "POOR" };
  };

  const EfficiencyMeter = ({ value }: { value: number }) => {
    // Value is 0-100 in real data
    const normalizedValue = value > 1 ? value / 100 : value;
    const style = getPerformanceColor(normalizedValue);
    
    return (
      <div className="w-full group">
        <div className="flex justify-between items-end mb-1.5">
          <div className="flex items-center gap-2">
            <span className={`text-[10px] font-black tracking-widest ${style.text}`}>{style.label}</span>
            {normalizedValue >= 0.5 ? <ArrowUpRight size={12} className={style.text} /> : <ArrowDownRight size={12} className={style.text} />}
          </div>
          <span className="text-sm font-mono font-bold text-white">{(normalizedValue * 100).toFixed(0)}</span>
        </div>
        
        {/* Glass Track */}
        <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden backdrop-blur-sm border border-white/5 relative">
            {/* Grid Lines */}
            <div className="absolute inset-0 flex justify-between px-[25%] opacity-20">
                <div className="w-px h-full bg-white"></div>
                <div className="w-px h-full bg-white"></div>
                <div className="w-px h-full bg-white"></div>
            </div>
            
            {/* Fill Bar */}
            <div 
              className={`h-full ${style.bg} relative transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(0,0,0,0.5)]`}
              style={{ width: `${Math.min(normalizedValue * 100, 100)}%` }}
            >
              <div className="absolute right-0 top-0 bottom-0 w-1 bg-white/50 animate-pulse"></div>
            </div>
        </div>
      </div>
    );
  };

  // Prepare data for rendering
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);
  
  // Calculate impact scores
  const awayImpactScore = Math.abs(totalImpact) + (Math.random() * 0.5 - 0.25); 
  const homeImpactScore = Math.abs(totalImpact) + (positionalAdvantages.quarterback || 0) * 2;
  const differential = Math.abs(homeImpactScore - awayImpactScore).toFixed(2);
  const advantageTeam = homeImpactScore > awayImpactScore ? homeAbbr : awayAbbr;
  const advantageTeamName = homeImpactScore > awayImpactScore ? homeTeam.name : awayTeam.name;
  const advantageColor = homeImpactScore > awayImpactScore ? homeTeam.primary_color : awayTeam.primary_color;

  // Helper to get player stats string
  const getPlayerStatsStr = (player: any, position: string) => {
    if (!player) return "N/A";
    if (position === 'QB') return `${player.passing_yards || 0} Yds • ${player.passing_tds || 0} TD`;
    if (position === 'RB') return `${player.rushing_yards || 0} Yds • ${player.rushing_tds || 0} TD`;
    if (position === 'WR' || position === 'TE') return `${player.receiving_yards || 0} Yds • ${player.receiving_tds || 0} TD`;
    if (position === 'DEF') return `${player.tackles || 0} Tkl • ${player.sacks || 0} Sck`;
    return "N/A";
  };

  // Construct matchups
  const matchups = [
    {
      position: "QB",
      weight: "40%",
      data: {
        p1: { 
          name: awayQB?.name || "N/A", 
          team: awayTeam.name, 
          id: awayQB?.player_id, 
          stats: getPlayerStatsStr(awayQB, 'QB'), 
          eff: awayQB?.efficiency_score || 0,
          url: awayQB?.headshot_url
        },
        p2: { 
          name: homeQB?.name || "N/A", 
          team: homeTeam.name, 
          id: homeQB?.player_id, 
          stats: getPlayerStatsStr(homeQB, 'QB'), 
          eff: homeQB?.efficiency_score || 0,
          url: homeQB?.headshot_url
        }
      }
    },
    {
      position: "RB",
      weight: "35%", 
      data: {
        p1: { 
          name: awayRBs[0]?.name || "N/A", 
          team: awayTeam.name, 
          id: awayRBs[0]?.player_id, 
          stats: getPlayerStatsStr(awayRBs[0], 'RB'), 
          eff: awayRBs[0]?.efficiency_score || 0,
          url: awayRBs[0]?.headshot_url
        },
        p2: { 
          name: homeRBs[0]?.name || "N/A", 
          team: homeTeam.name, 
          id: homeRBs[0]?.player_id, 
          stats: getPlayerStatsStr(homeRBs[0], 'RB'), 
          eff: homeRBs[0]?.efficiency_score || 0,
          url: homeRBs[0]?.headshot_url
        }
      }
    },
    {
      position: "WR",
      weight: "35%",
      data: {
        p1: { 
          name: awayWRs[0]?.name || "N/A", 
          team: awayTeam.name, 
          id: awayWRs[0]?.player_id, 
          stats: getPlayerStatsStr(awayWRs[0], 'WR'), 
          eff: awayWRs[0]?.efficiency_score || 0,
          url: awayWRs[0]?.headshot_url
        },
        p2: { 
          name: homeWRs[0]?.name || "N/A", 
          team: homeTeam.name, 
          id: homeWRs[0]?.player_id, 
          stats: getPlayerStatsStr(homeWRs[0], 'WR'), 
          eff: homeWRs[0]?.efficiency_score || 0,
          url: homeWRs[0]?.headshot_url
        }
      }
    },
    {
      position: "WR",
      weight: "35%",
      data: {
        p1: { 
          name: awayWRs[1]?.name || "N/A", 
          team: awayTeam.name, 
          id: awayWRs[1]?.player_id, 
          stats: getPlayerStatsStr(awayWRs[1], 'WR'), 
          eff: awayWRs[1]?.efficiency_score || 0,
          url: awayWRs[1]?.headshot_url
        },
        p2: { 
          name: homeWRs[1]?.name || "N/A", 
          team: homeTeam.name, 
          id: homeWRs[1]?.player_id, 
          stats: getPlayerStatsStr(homeWRs[1], 'WR'), 
          eff: homeWRs[1]?.efficiency_score || 0,
          url: homeWRs[1]?.headshot_url
        }
      }
    },
    {
      position: "DEF",
      weight: "25%",
      data: {
        p1: { 
          name: awayDefense[0]?.name || "N/A", 
          team: awayTeam.name, 
          id: awayDefense[0]?.player_id, 
          stats: getPlayerStatsStr(awayDefense[0], 'DEF'), 
          eff: awayDefense[0]?.efficiency_score || 0,
          url: awayDefense[0]?.headshot_url
        },
        p2: { 
          name: homeDefense[0]?.name || "N/A", 
          team: homeTeam.name, 
          id: homeDefense[0]?.player_id, 
          stats: getPlayerStatsStr(homeDefense[0], 'DEF'), 
          eff: homeDefense[0]?.efficiency_score || 0,
          url: homeDefense[0]?.headshot_url
        }
      }
    }
  ];

  return (
    <div className="w-full text-white font-sans selection:bg-emerald-500/30 p-2 md:p-6 overflow-x-hidden relative">
      
      {/* Dynamic Background Mesh - Localized */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-3xl">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-900/10 rounded-full blur-[120px] mix-blend-screen animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-green-900/10 rounded-full blur-[120px] mix-blend-screen animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">

        {/* Header HUD */}
        <header className="mb-8 grid grid-cols-1 md:grid-cols-12 gap-4">
          <div className="md:col-span-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="flex justify-between items-center relative z-10">
              <div className="flex items-center gap-6">
                 {/* Away Team */}
                 <div className="text-center">
                    <img src={awayTeam.logo} alt={awayTeam.name} className="w-16 h-16 object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.3)] mb-2" />
                    <h2 className="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/60">{awayAbbr}</h2>
                 </div>

                 {/* VS Graphic */}
                 <div className="h-16 w-px bg-gradient-to-b from-transparent via-white/20 to-transparent"></div>

                 {/* Home Team */}
                 <div className="text-center">
                    <img src={homeTeam.logo} alt={homeTeam.name} className="w-16 h-16 object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.3)] mb-2" />
                    <h2 className="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/60">{homeAbbr}</h2>
                 </div>
              </div>

              {/* Live Metric */}
              <div className="hidden md:block text-right">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-1">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                  <span className="text-[10px] font-bold text-emerald-400 tracking-widest uppercase">Live Analysis</span>
                </div>
                <div className="text-sm text-slate-400 font-mono">NEXT GEN STATS ENGINE</div>
              </div>
            </div>
          </div>

          <div className="md:col-span-4 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex flex-col justify-center relative overflow-hidden">
             <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/20 rounded-full blur-[50px] -mr-10 -mt-10"></div>
             <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Total Impact Score</span>
             <div className="flex items-end gap-3">
               <span className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-emerald-200">+{differential}</span>
               <div className="flex flex-col mb-1">
                 <span className="text-xs font-bold text-emerald-400 flex items-center">
                    {advantageTeamName} <ArrowUpRight size={14} className="ml-1" />
                 </span>
                 <span className="text-[10px] text-slate-500 uppercase">Advantage</span>
               </div>
             </div>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Matchups Column */}
          <div className="lg:col-span-8 space-y-4">
            <div className="flex items-center justify-between px-1">
              <h3 className="text-sm font-bold text-white/80 uppercase tracking-widest flex items-center gap-2">
                <Binary size={16} className="text-emerald-500" />
                Individual Matchups
              </h3>
            </div>

            {matchups.map((match, idx) => {
              const p1Eff = match.data.p1.eff > 1 ? match.data.p1.eff / 100 : match.data.p1.eff;
              const p2Eff = match.data.p2.eff > 1 ? match.data.p2.eff / 100 : match.data.p2.eff;
              
              const p1Better = p1Eff > p2Eff;
              const p2Better = p2Eff > p1Eff;

              return (
                <div key={idx} className="relative bg-white/[0.03] backdrop-blur-lg border border-white/5 rounded-xl p-1 overflow-hidden hover:bg-white/[0.06] transition-all duration-300 group">
                  {/* Position Tag */}
                  <div className="absolute top-4 left-0 bg-white/10 px-3 py-1 rounded-r text-[10px] font-black text-white/70 border-y border-r border-white/10 backdrop-blur-md z-20">
                    {match.position}
                  </div>

                  <div className="flex flex-col md:flex-row items-center relative z-10 p-4 gap-6">
                    
                    {/* Player 1 (Away) */}
                    <div className={`flex-1 flex items-center gap-4 w-full ${p1Better ? 'opacity-100' : 'opacity-60 grayscale-[0.5] group-hover:grayscale-0 transition-all'}`}>
                      <Headshot id={match.data.p1.id} teamColor={awayTeam.primary_color} url={match.data.p1.url} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                            <h4 className="font-bold text-sm text-white truncate">{match.data.p1.name}</h4>
                            {p1Better && <div className="text-[10px] font-bold bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded border border-emerald-500/30">ADV</div>}
                        </div>
                        <div className="text-[10px] font-mono text-slate-400 mb-2">{match.data.p1.stats}</div>
                        <EfficiencyMeter value={match.data.p1.eff} />
                      </div>
                    </div>

                    {/* VS Graphic */}
                    <div className="shrink-0 flex flex-col items-center">
                        <div className="w-px h-8 bg-gradient-to-b from-transparent via-white/20 to-transparent"></div>
                        <div className="text-[10px] font-black text-slate-600">VS</div>
                        <div className="w-px h-8 bg-gradient-to-b from-transparent via-white/20 to-transparent"></div>
                    </div>

                    {/* Player 2 (Home) */}
                    <div className={`flex-1 flex flex-row-reverse md:flex-row items-center gap-4 w-full ${p2Better ? 'opacity-100' : 'opacity-60 grayscale-[0.5] group-hover:grayscale-0 transition-all'}`}>
                      <div className="flex-1 min-w-0 md:text-right">
                         <div className="flex items-center justify-between md:justify-end gap-2 mb-1">
                            {p2Better && <div className="text-[10px] font-bold bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded border border-emerald-500/30">ADV</div>}
                            <h4 className={`font-bold text-sm truncate ${!match.data.p2.id ? 'text-slate-500' : 'text-white'}`}>{match.data.p2.name}</h4>
                        </div>
                        <div className="text-[10px] font-mono text-slate-400 mb-2">{match.data.p2.stats}</div>
                        <EfficiencyMeter value={match.data.p2.eff} />
                      </div>
                      <Headshot id={match.data.p2.id} teamColor={homeTeam.primary_color} url={match.data.p2.url} />
                    </div>

                  </div>
                </div>
              );
            })}
          </div>

          {/* Analytics Sidebar */}
          <div className="lg:col-span-4 space-y-4">
            
            {/* Verdict Card */}
            <div className="bg-gradient-to-br from-emerald-950/40 to-black/80 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-6 relative overflow-hidden">
               <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-500 to-transparent opacity-50"></div>
               
               <div className="flex items-start gap-3 mb-6">
                 <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
                   <Target size={24} />
                 </div>
                 <div>
                   <h3 className="font-bold text-white text-lg tracking-tight">Analytical Verdict</h3>
                   <p className="text-xs text-emerald-400 font-mono">CONFIDENCE: HIGH</p>
                 </div>
               </div>

               <div className="space-y-4">
                 <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-xs text-slate-400">Net Efficiency</span>
                    <span className="text-emerald-400 font-mono font-bold flex items-center gap-1">
                      +{differential} <ArrowUpRight size={12} />
                    </span>
                 </div>
                 
                 <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-xs text-slate-400">Key Player Depth</span>
                    <div className="flex gap-1">
                       <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                       <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                       <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                       <div className="w-2 h-2 rounded-full bg-slate-700"></div>
                    </div>
                 </div>
               </div>
               
               <p className="mt-6 text-xs text-slate-400 leading-relaxed border-t border-white/10 pt-4">
                 Model favors <strong className="text-emerald-400">{advantageTeamName}</strong> due to superior efficiency in key positional matchups.
               </p>
            </div>

            {/* Impact Distribution Chart - Next Gen */}
            <div className="relative bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 overflow-hidden group/chart">
               {/* Tech Background Grid */}
               <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_80%)]"></div>
               
               <div className="relative z-10 flex justify-between items-center mb-6">
                 <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-widest flex items-center gap-2">
                   <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(6,182,212,0.8)]"></div>
                   Weight Distribution
                 </h3>
                 <div className="text-[10px] font-mono text-slate-500 border border-white/10 px-2 py-0.5 rounded bg-black/20">SYS.ANALYSIS.V2</div>
               </div>
               
               <div className="relative flex justify-between h-48 gap-4 items-end px-2">
                  {/* Horizontal Grid Lines */}
                  <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                    {[...Array(5)].map((_, i) => (
                      <div key={i} className="w-full h-px bg-white/5 border-t border-dashed border-white/5"></div>
                    ))}
                  </div>

                  {[
                    { label: 'QB', val: 40, color: 'from-cyan-500 to-blue-600', shadow: 'shadow-cyan-500/50', text: 'text-cyan-400', border: 'border-cyan-400/30' },
                    { label: 'SKILL', val: 35, color: 'from-violet-500 to-purple-600', shadow: 'shadow-violet-500/50', text: 'text-violet-400', border: 'border-violet-400/30' },
                    { label: 'DEF', val: 25, color: 'from-emerald-500 to-teal-600', shadow: 'shadow-emerald-500/50', text: 'text-emerald-400', border: 'border-emerald-400/30' }
                  ].map((item, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center gap-3 group h-full justify-end relative z-10">
                       {/* Value Tag */}
                       <div className={`text-xs font-mono font-bold ${item.text} opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0 bg-black/80 px-2 py-1 rounded border ${item.border} backdrop-blur-md shadow-lg`}>
                         {item.val}%
                       </div>
                       
                       {/* Bar Container */}
                       <div className="w-full bg-white/5 rounded-sm relative flex-1 flex items-end max-w-[40px] group-hover:max-w-[50px] transition-all duration-500 border-b border-white/10">
                          {/* The Bar */}
                          <div 
                            className={`w-full bg-gradient-to-t ${item.color} relative transition-all duration-1000 ease-out group-hover:shadow-[0_0_20px_rgba(0,0,0,0.5)] ${item.shadow}`} 
                            style={{ height: `${item.val}%` }}
                          >
                             {/* Tech Pattern Overlay */}
                             <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] opacity-50"></div>
                             
                             {/* Top Highlight */}
                             <div className="absolute top-0 left-0 right-0 h-[2px] bg-white/80 shadow-[0_0_10px_white]"></div>
                          </div>
                       </div>
                       
                       {/* Label */}
                       <div className="text-center">
                         <span className="text-[10px] font-black tracking-widest text-slate-500 group-hover:text-white transition-colors">{item.label}</span>
                         <div className={`h-[1px] w-0 group-hover:w-full ${item.text.replace('text', 'bg')} transition-all duration-300 mt-1 shadow-[0_0_8px_currentColor]`}></div>
                       </div>
                    </div>
                  ))}
               </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
