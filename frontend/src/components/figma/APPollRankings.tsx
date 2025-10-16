import { GlassCard } from './GlassCard';
import { Trophy, TrendingUp, TrendingDown, Minus, Award, Star } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { extractSection, generateTeamAbbr } from '../../utils/teamUtils';

interface APPollRankingsProps {
  predictionData?: any;
}

export function APPollRankings({ predictionData }: APPollRankingsProps) {
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;

  // Parse AP Poll data from section [18]
  const parseAPPollData = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 18) : null;
    
    if (!section || !awayTeam || !homeTeam) {
      return {
        currentRankings: [],
        weeklyProgression: { away: [], home: [] },
        currentWeek: 7
      };
    }

    // Parse current rankings
    const parseCurrentRankings = () => {
      const rankings: any[] = [];
      
      // Pattern: "TeamName           #Rank             Points        Conference           FirstPlaceVotes"
      const awayPattern = new RegExp(`${awayTeam.name}\\s+#(\\d+|NR)\\s+(\\d+)\\s+(\\w+[\\w\\s]*)\\s+(\\d+)`, 'i');
      const homePattern = new RegExp(`${homeTeam.name}\\s+#(\\d+|NR)\\s+(\\d+)\\s+(\\w+[\\w\\s]*)\\s+(\\d+)`, 'i');
      
      const awayMatch = section.match(awayPattern);
      const homeMatch = section.match(homePattern);
      
      if (awayMatch) {
        rankings.push({
          team: 'away',
          rank: awayMatch[1] === 'NR' ? 'NR' : `#${awayMatch[1]}`,
          points: parseInt(awayMatch[2]),
          conference: awayMatch[3].trim(),
          firstPlaceVotes: parseInt(awayMatch[4])
        });
      }
      
      if (homeMatch) {
        rankings.push({
          team: 'home',
          rank: homeMatch[1] === 'NR' ? 'NR' : `#${homeMatch[1]}`,
          points: parseInt(homeMatch[2]),
          conference: homeMatch[3].trim(),
          firstPlaceVotes: parseInt(homeMatch[4])
        });
      }
      
      return rankings;
    };

    // Parse weekly progression
    const parseWeeklyProgression = () => {
      const weeklySection = section.match(/WEEKLY RANKINGS PROGRESSION:([\s\S]*?)(?:================|$)/i);
      if (!weeklySection) return { away: [], home: [] };
      
      const weeklyText = weeklySection[1];
      
      // Extract weeks for away team
      const awayWeeks: any[] = [];
      const homeWeeks: any[] = [];
      
      // Need to escape special characters in team names
      const awayEscaped = awayTeam.name.replace(/[()]/g, '\\$&');
      const homeEscaped = homeTeam.name.replace(/[()]/g, '\\$&');
      
      for (let week = 1; week <= 8; week++) {
        // Try both possible orders since backend might list teams in different order
        // Pattern 1: Away first, Home second
        let weekPattern = new RegExp(
          `Week ${week}\\s+${awayEscaped}:\\s+(NR|#\\d+)\\s+${homeEscaped}:\\s+(NR|#\\d+)`,
          'i'
        );
        let match = weeklyText.match(weekPattern);
        
        if (match) {
          const awayRank = match[1];
          const homeRank = match[2];
          
          const awayTrend = awayWeeks.length > 0 ? getTrend(awayWeeks[awayWeeks.length - 1].rank, awayRank) : undefined;
          const homeTrend = homeWeeks.length > 0 ? getTrend(homeWeeks[homeWeeks.length - 1].rank, homeRank) : undefined;
          
          awayWeeks.push({ week, rank: awayRank, trend: awayTrend });
          homeWeeks.push({ week, rank: homeRank, trend: homeTrend });
        } else {
          // Pattern 2: Home first, Away second
          weekPattern = new RegExp(
            `Week ${week}\\s+${homeEscaped}:\\s+(NR|#\\d+)\\s+${awayEscaped}:\\s+(NR|#\\d+)`,
            'i'
          );
          match = weeklyText.match(weekPattern);
          
          if (match) {
            const homeRank = match[1];
            const awayRank = match[2];
            
            const awayTrend = awayWeeks.length > 0 ? getTrend(awayWeeks[awayWeeks.length - 1].rank, awayRank) : undefined;
            const homeTrend = homeWeeks.length > 0 ? getTrend(homeWeeks[homeWeeks.length - 1].rank, homeRank) : undefined;
            
            awayWeeks.push({ week, rank: awayRank, trend: awayTrend });
            homeWeeks.push({ week, rank: homeRank, trend: homeTrend });
          }
        }
      }
      
      return { away: awayWeeks, home: homeWeeks };
    };

    const getTrend = (prevRank: string, currentRank: string) => {
      if (prevRank === 'NR' && currentRank !== 'NR') return 'new';
      if (prevRank !== 'NR' && currentRank === 'NR') return 'down';
      if (prevRank === currentRank) return 'static';
      
      const prevNum = prevRank === 'NR' ? 999 : parseInt(prevRank.replace('#', ''));
      const currNum = currentRank === 'NR' ? 999 : parseInt(currentRank.replace('#', ''));
      
      return currNum < prevNum ? 'up' : 'down';
    };

    return {
      currentRankings: parseCurrentRankings(),
      weeklyProgression: parseWeeklyProgression(),
      currentWeek: 8 // Can be dynamic if needed
    };
  };

  const { currentRankings, weeklyProgression, currentWeek } = parseAPPollData();
  
  // Get team-specific data
  const team1Logo = awayTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png";
  const team2Logo = homeTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png";
  const team1Name = awayTeam?.name || "Ohio State";
  const team2Name = homeTeam?.name || "Illinois";
  const team1Color = awayTeam?.primary_color || "#ce1141";
  const team2Color = homeTeam?.primary_color || "#ff5f05";
  const team1Abbr = awayTeam ? generateTeamAbbr(awayTeam.name) : "OSU";
  const team2Abbr = homeTeam ? generateTeamAbbr(homeTeam.name) : "ILL";
  const team1Record = predictionData?.header?.teams?.away?.record || "6-0";
  const team2Record = predictionData?.header?.teams?.home?.record || "5-2";
  
  // Get current rankings for each team
  const awayRanking = currentRankings.find(r => r.team === 'away');
  const homeRanking = currentRankings.find(r => r.team === 'home');
  
  // Determine which team has better ranking
  const awayRankNum = awayRanking?.rank === 'NR' ? 999 : parseInt(awayRanking?.rank?.replace('#', '') || '999');
  const homeRankNum = homeRanking?.rank === 'NR' ? 999 : parseInt(homeRanking?.rank?.replace('#', '') || '999');
  const betterRanked = awayRankNum < homeRankNum ? team1Abbr : team2Abbr;
  const higherPoints = Math.max(awayRanking?.points || 0, homeRanking?.points || 0);

  // Helper to generate trend description
  const getTrendDescription = (weeks: any[]) => {
    if (weeks.length < 2) return "Insufficient data";
    
    const firstRank = weeks[0].rank;
    const lastRank = weeks[weeks.length - 1].rank;
    
    if (lastRank === 'NR') return "Dropped out of rankings";
    if (firstRank === 'NR' && lastRank !== 'NR') return "Entered rankings";
    if (firstRank === lastRank) return "Maintained ranking";
    
    const firstNum = firstRank === 'NR' ? 999 : parseInt(firstRank.replace('#', ''));
    const lastNum = lastRank === 'NR' ? 999 : parseInt(lastRank.replace('#', ''));
    
    if (lastNum < firstNum) return "Rising in rankings";
    return "Declining in rankings";
  };

  // Helper to get trend color based on progression
  const getTrendColor = (weeks: any[]) => {
    if (weeks.length < 2) return "rgb(148, 163, 184)"; // slate-400
    
    const firstRank = weeks[0].rank;
    const lastRank = weeks[weeks.length - 1].rank;
    
    if (lastRank === 'NR') return "rgb(239, 68, 68)"; // red-500
    if (firstRank === 'NR' && lastRank !== 'NR') return "rgb(59, 130, 246)"; // blue-500
    if (firstRank === lastRank) return "rgb(234, 179, 8)"; // yellow-500
    
    const firstNum = firstRank === 'NR' ? 999 : parseInt(firstRank.replace('#', ''));
    const lastNum = lastRank === 'NR' ? 999 : parseInt(lastRank.replace('#', ''));
    const lastRankNum = parseInt(lastRank.replace('#', ''));
    
    // Rising or maintaining top 5 = green
    if (lastNum < firstNum || (lastNum === firstNum && lastRankNum <= 5)) {
      return "rgb(34, 197, 94)"; // green-500
    }
    // Declining = red
    return "rgb(239, 68, 68)"; // red-500
  };
  return (
    <GlassCard glowColor="from-yellow-500/20 to-amber-500/20" className="p-6 border-yellow-500/40">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-yellow-500/20 border border-yellow-500/40">
          <Trophy className="w-5 h-5 text-yellow-400" />
        </div>
        <h3 className="text-white font-semibold">AP Poll Rankings Progression</h3>
      </div>
      
      {/* Current Rankings */}
      <div className="mb-6">
        <h4 className="text-slate-300 font-medium mb-4 flex items-center gap-2">
          <Award className="w-4 h-4" />
          Current Rankings (Week {currentWeek})
        </h4>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-600/40">
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Team</th>
                <th className="text-center py-3 px-4 text-slate-300 font-medium">Current Rank</th>
                <th className="text-center py-3 px-4 text-slate-300 font-medium">Points</th>
                <th className="text-center py-3 px-4 text-slate-300 font-medium">Conference</th>
                <th className="text-center py-3 px-4 text-slate-300 font-medium">First Place Votes</th>
              </tr>
            </thead>
            <tbody>
              {awayRanking && (
                <tr className="border-b border-slate-700/30">
                  <td className="py-3 px-4 text-slate-300 font-medium">
                    <div className="flex items-center gap-2">
                      <ImageWithFallback src={team1Logo} alt={team1Name} className="w-6 h-6 object-contain" />
                      <span style={{ color: team1Color }}>{team1Name}</span>
                      {awayRankNum === 1 && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full text-sm font-bold">
                      {awayRanking.rank}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center font-mono text-yellow-400 font-semibold">{awayRanking.points}</td>
                  <td className="py-3 px-4 text-center font-mono text-slate-200">{awayRanking.conference}</td>
                  <td className="py-3 px-4 text-center font-mono text-slate-200">{awayRanking.firstPlaceVotes}</td>
                </tr>
              )}
              {homeRanking && (
                <tr className="border-b border-slate-700/30">
                  <td className="py-3 px-4 text-slate-300 font-medium">
                    <div className="flex items-center gap-2">
                      <ImageWithFallback src={team2Logo} alt={team2Name} className="w-6 h-6 object-contain" />
                      <span style={{ color: team2Color }}>{team2Name}</span>
                      {homeRankNum === 1 && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full text-sm font-bold">
                      {homeRanking.rank}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center font-mono text-yellow-400 font-semibold">{homeRanking.points}</td>
                  <td className="py-3 px-4 text-center font-mono text-slate-200">{homeRanking.conference}</td>
                  <td className="py-3 px-4 text-center font-mono text-slate-200">{homeRanking.firstPlaceVotes}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Weekly Progression */}
      <div className="mb-6">
        <h4 className="text-slate-300 font-medium mb-4 flex items-center gap-2">
          <TrendingUp className="w-4 h-4" />
          Weekly Rankings Progression
        </h4>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Away Team Progression */}
          <div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br" style={{
            background: `linear-gradient(to bottom right, ${team1Color}26, ${team1Color}0D)`,
            borderColor: `${team1Color}66`
          }}>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={team1Logo} alt={team1Name} className="w-10 h-10 object-contain" />
              <h5 className="font-semibold" style={{ color: team1Color }}>{team1Name} ({team1Record})</h5>
              {awayRankNum === 1 && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
            </div>
            
            <div className="space-y-2">
              {weeklyProgression.away.length > 0 ? (
                weeklyProgression.away.map((week: any, idx: number) => (
                  <WeeklyRank key={idx} week={week.week} rank={week.rank} trend={week.trend} teamColor={team1Color} />
                ))
              ) : (
                <div className="text-xs text-slate-400 text-center py-4">No weekly data available</div>
              )}
            </div>
            
            {weeklyProgression.away.length > 0 && (
              <div 
                className="mt-4 p-3 rounded-lg border"
                style={{
                  backgroundColor: `${getTrendColor(weeklyProgression.away)}1A`,
                  borderColor: `${getTrendColor(weeklyProgression.away)}4D`
                }}
              >
                <div className="text-xs" style={{ color: getTrendColor(weeklyProgression.away) }}>
                  <span className="font-semibold">Trend:</span> {getTrendDescription(weeklyProgression.away)}
                </div>
              </div>
            )}
          </div>

          {/* Home Team Progression */}
          <div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br" style={{
            background: `linear-gradient(to bottom right, ${team2Color}26, ${team2Color}0D)`,
            borderColor: `${team2Color}66`
          }}>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={team2Logo} alt={team2Name} className="w-10 h-10 object-contain" />
              <h5 className="font-semibold" style={{ color: team2Color }}>{team2Name} ({team2Record})</h5>
              {homeRankNum === 1 && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
            </div>
            
            <div className="space-y-2">
              {weeklyProgression.home.length > 0 ? (
                weeklyProgression.home.map((week: any, idx: number) => (
                  <WeeklyRank key={idx} week={week.week} rank={week.rank} trend={week.trend} teamColor={team2Color} />
                ))
              ) : (
                <div className="text-xs text-slate-400 text-center py-4">No weekly data available</div>
              )}
            </div>
            
            {weeklyProgression.home.length > 0 && (
              <div 
                className="mt-4 p-3 rounded-lg border"
                style={{
                  backgroundColor: `${getTrendColor(weeklyProgression.home)}1A`,
                  borderColor: `${getTrendColor(weeklyProgression.home)}4D`
                }}
              >
                <div className="text-xs" style={{ color: getTrendColor(weeklyProgression.home) }}>
                  <span className="font-semibold">Trend:</span> {getTrendDescription(weeklyProgression.home)}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Poll Impact Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-yellow-500/10 to-amber-500/10 border border-yellow-500/30 rounded-lg p-4 text-center">
          <Trophy className="w-6 h-6 text-yellow-400 mx-auto mb-2" />
          <div className="text-lg font-bold text-yellow-400 mb-1">
            {awayRanking?.rank || 'NR'} vs {homeRanking?.rank || 'NR'}
          </div>
          <div className="text-xs text-slate-300">{betterRanked} carries elite momentum</div>
        </div>
        
        <div className="bg-gradient-to-br from-emerald-500/10 to-green-500/10 border border-emerald-500/30 rounded-lg p-4 text-center">
          <Award className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
          <div className="text-lg font-bold text-emerald-400 mb-1">{higherPoints} Points</div>
          <div className="text-xs text-slate-300">Strong poll support</div>
        </div>
        
        <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-lg p-4 text-center">
          <TrendingUp className="w-6 h-6 text-blue-400 mx-auto mb-2" />
          <div className="text-lg font-bold text-blue-400 mb-1">
            {awayRankNum === 1 || homeRankNum === 1 ? '#1 Status' : 'Consistency'}
          </div>
          <div className="text-xs text-slate-300">
            {awayRankNum === 1 || homeRankNum === 1 ? 'Top ranking advantage' : 'Maintaining position'}
          </div>
        </div>
      </div>
    </GlassCard>
  );
}

function WeeklyRank({ week, rank, trend, teamColor }: { week: number; rank: string; trend?: string; teamColor?: string }) {
  const isRanked = rank !== "NR";
  
  // Determine the indicator color based on trend and ranking
  let indicatorColor = "";
  
  if (!isRanked) {
    // Never ranked - gray
    indicatorColor = "rgb(71, 85, 105)"; // slate-600
  } else {
    const rankNum = parseInt(rank.replace('#', ''));
    const isTopFive = rankNum <= 5;
    
    if (trend === 'up' || (trend === 'static' && isTopFive)) {
      // Trending up or consistently top 5 - green
      indicatorColor = "rgb(34, 197, 94)"; // green-500
    } else if (trend === 'down') {
      // Declining - red
      indicatorColor = "rgb(239, 68, 68)"; // red-500
    } else if (trend === 'static') {
      // Static but not top 5 - yellow
      indicatorColor = "rgb(234, 179, 8)"; // yellow-500
    } else if (trend === 'new') {
      // New to rankings - blue
      indicatorColor = "rgb(59, 130, 246)"; // blue-500
    } else {
      // Default for first week
      indicatorColor = "rgb(234, 179, 8)"; // yellow-500
    }
  }
  
  // Use team color with transparency for background
  const bgColor = teamColor ? `${teamColor}33` : "rgba(234, 179, 8, 0.2)"; // 20% opacity
  const borderColor = teamColor ? `${teamColor}66` : "rgba(234, 179, 8, 0.4)"; // 40% opacity
  const textColor = isRanked ? (teamColor || "rgb(250, 204, 21)") : "rgb(148, 163, 184)"; // slate-400 for NR
  
  const getTrendIcon = () => {
    if (!trend) return null;
    
    switch (trend) {
      case "up":
        return <TrendingUp className="w-4 h-4" style={{ color: indicatorColor }} />;
      case "down":
        return <TrendingDown className="w-4 h-4" style={{ color: indicatorColor }} />;
      case "static":
        return <Minus className="w-4 h-4" style={{ color: indicatorColor }} />;
      case "new":
        return <Star className="w-4 h-4" style={{ color: indicatorColor }} />;
      default:
        return null;
    }
  };
  
  return (
    <div 
      className="relative flex justify-between items-center py-2 px-3 rounded-lg border overflow-hidden"
      style={{
        backgroundColor: bgColor,
        borderColor: borderColor
      }}
    >
      <div className="flex flex-col gap-1 relative z-10">
        <span className="text-sm text-slate-300">Week {week}</span>
        {/* Colored indicator under trend icon */}
        {trend && (
          <div className="flex items-center gap-1">
            {getTrendIcon()}
            <div 
              className="h-0.5 flex-1 rounded-full"
              style={{ backgroundColor: `${indicatorColor}80` }} // 50% opacity
            ></div>
          </div>
        )}
      </div>
      <span 
        className="text-sm font-mono font-semibold relative z-10"
        style={{ color: textColor }}
      >
        {rank}
      </span>
    </div>
  );
}