import { GlassCard } from './GlassCard';
import { Shield, Target, TrendingDown, BarChart3, Check } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { extractSection, generateTeamAbbr } from '../../utils/teamUtils';

interface ExtendedDefensiveAnalyticsProps {
  predictionData?: any;
}

export function ExtendedDefensiveAnalytics({ predictionData }: ExtendedDefensiveAnalyticsProps) {
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;

  // Parse Extended Defensive Analytics from section [18]
  const parseDefensiveAnalytics = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 18) : null;
    
    if (!section || !awayTeam || !homeTeam) {
      return [];
    }

    const metrics = [
      'Defense Plays',
      'Defense Drives',
      'Defense Total PPA',
      'Defense Points Per Opp',
      'Def Field Pos Avg Start',
      'Def Field Pos Pred Pts',
      'Def Havoc Front Seven',
      'Def Havoc DB',
      'Def Rush Plays PPA',
      'Def Rush Success Rate',
      'Def Pass Plays PPA',
      'Def Pass Success Rate'
    ];

    return metrics.map(metric => {
      const pattern = new RegExp(`${metric.replace(/[()]/g, '\\$&')}\\s+([\\d.\\-]+)%?\\s+([\\d.\\-]+)%?\\s+(\\w+)`, 'i');
      const match = section.match(pattern);
      
      if (match) {
        const advantageRaw = match[3].trim();
        const advantage = advantageRaw === 'Home' ? homeTeam.name : 
                         advantageRaw === 'Away' ? awayTeam.name : 
                         advantageRaw;
        
        // Add % suffix for percentage metrics
        const isPercent = metric.includes('Rate') || metric.includes('Havoc');
        const awayValue = isPercent ? `${match[1]}%` : match[1];
        const homeValue = isPercent ? `${match[2]}%` : match[2];
        
        return { metric, away: awayValue, home: homeValue, advantage };
      }
      return { metric, away: '0', home: '0', advantage: 'Tied' };
    });
  };

  // Parse Season Summary Statistics from section [18]
  const parseSeasonSummary = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 18) : null;
    
    if (!section || !awayTeam || !homeTeam) {
      return [];
    }

    const metrics = [
      'Games Played',
      'Total Offensive Yards',
      'First Downs Allowed',
      'Turnovers Created',
      'Turnovers Lost',
      'Turnover Margin',
      'Penalties Per Game',
      'Penalty Yards Per Game'
    ];

    return metrics.map(metric => {
      const pattern = new RegExp(`${metric}\\s+([\\d.,+\\-]+)\\s+([\\d.,+\\-]+)\\s+(\\w+)`, 'i');
      const match = section.match(pattern);
      
      if (match) {
        const advantageRaw = match[3].trim();
        const advantage = advantageRaw === 'Home' ? homeTeam.name : 
                         advantageRaw === 'Away' ? awayTeam.name : 
                         advantageRaw;
        
        return { metric, away: match[1], home: match[2], advantage };
      }
      return { metric, away: '0', home: '0', advantage: 'Tied' };
    });
  };

  const defensiveData = parseDefensiveAnalytics();
  const summaryData = parseSeasonSummary();
  
  // Use team data or fallback
  const team1Logo = awayTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png";
  const team2Logo = homeTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png";
  const team1Name = awayTeam?.name || "Ohio State";
  const team2Name = homeTeam?.name || "Illinois";
  const team1Color = awayTeam?.primary_color || "#ce1141";
  const team2Color = homeTeam?.primary_color || "#ff5f05";
  const team1Abbr = awayTeam ? generateTeamAbbr(awayTeam.name) : "OSU";
  const team2Abbr = homeTeam ? generateTeamAbbr(homeTeam.name) : "ILL";

  // Calculate highlights from data
  const defensePlaysAway = defensiveData.find(d => d.metric === 'Defense Plays')?.away || '0';
  const defensePlaysHome = defensiveData.find(d => d.metric === 'Defense Plays')?.home || '0';
  const playsAwayNum = parseInt(defensePlaysAway);
  const playsHomeNum = parseInt(defensePlaysHome);
  const playsDiff = Math.abs(playsAwayNum - playsHomeNum);
  const playsAdvantage = playsAwayNum < playsHomeNum ? team1Abbr : team2Abbr;

  const pointsPerOppAway = defensiveData.find(d => d.metric === 'Defense Points Per Opp')?.away || '0';
  const pointsPerOppHome = defensiveData.find(d => d.metric === 'Defense Points Per Opp')?.home || '0';
  const pointsAwayNum = parseFloat(pointsPerOppAway);
  const pointsHomeNum = parseFloat(pointsPerOppHome);
  const pointsDiff = Math.abs(pointsAwayNum - pointsHomeNum).toFixed(2);
  const pointsAdvantage = pointsAwayNum < pointsHomeNum ? team1Abbr : team2Abbr;

  const turnoverMarginAway = summaryData.find(d => d.metric === 'Turnover Margin')?.away || '0';
  const turnoverMarginHome = summaryData.find(d => d.metric === 'Turnover Margin')?.home || '0';
  const marginAwayNum = parseInt(turnoverMarginAway.replace('+', ''));
  const marginHomeNum = parseInt(turnoverMarginHome.replace('+', ''));
  const marginDiff = Math.abs(marginAwayNum - marginHomeNum);
  const marginAdvantage = marginAwayNum > marginHomeNum ? team1Abbr : team2Abbr;
  return (
    <div className="space-y-6">
      {/* Extended Defensive Analytics */}
      <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-4 sm:p-6 border-gray-500/40">
        <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
          <div className="p-1.5 sm:p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
            <Shield className="w-4 h-4 sm:w-5 sm:h-5 text-red-400" />
          </div>
          <h3 className="text-white font-semibold text-sm sm:text-base">Extended Defensive Analytics</h3>
        </div>
        
        <div className="overflow-x-auto -mx-2 sm:mx-0">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-gray-600/40">
                <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">Metric</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 font-medium text-xs sm:text-sm">
                  <div className="flex items-center justify-center gap-1 sm:gap-2">
                    <ImageWithFallback 
                      src={team1Logo}
                      alt={team1Name}
                      className="w-6 h-6 sm:w-8 sm:h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team1Color }}>{team1Name}</span>
                  </div>
                </th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 font-medium text-xs sm:text-sm">
                  <div className="flex items-center justify-center gap-1 sm:gap-2">
                    <ImageWithFallback 
                      src={team2Logo}
                      alt={team2Name}
                      className="w-6 h-6 sm:w-8 sm:h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team2Color }}>{team2Name}</span>
                  </div>
                </th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">Advantage</th>
              </tr>
            </thead>
            <tbody>
              {defensiveData.map((data, index) => (
                <DefenseStatRow 
                  key={index}
                  metric={data.metric} 
                  away={data.away} 
                  home={data.home} 
                  advantage={data.advantage}
                  awayTeam={awayTeam}
                  homeTeam={homeTeam}
                />
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* Season Summary Statistics */}
      <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-4 sm:p-6 border-gray-500/40">
        <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
          <div className="p-1.5 sm:p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
            <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5 text-purple-400" />
          </div>
          <h3 className="text-white font-semibold text-sm sm:text-base">Season Summary Statistics</h3>
        </div>
        
        <div className="overflow-x-auto -mx-2 sm:mx-0">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-gray-600/40">
                <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">Metric</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">
                  <div className="flex items-center justify-center gap-1 sm:gap-2">
                    <ImageWithFallback 
                      src={team1Logo}
                      alt={team1Name}
                      className="w-6 h-6 sm:w-8 sm:h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team1Abbr }}>{team1Abbr}</span>
                  </div>
                </th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">
                  <div className="flex items-center justify-center gap-1 sm:gap-2">
                    <ImageWithFallback 
                      src={team2Logo}
                      alt={team2Name}
                      className="w-6 h-6 sm:w-8 sm:h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team2Abbr }}>{team2Abbr}</span>
                  </div>
                </th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">Advantage</th>
              </tr>
            </thead>
            <tbody>
              {summaryData.map((data, index) => (
                <DefenseStatRow
                  key={index}
                  metric={data.metric} 
                  away={data.away} 
                  home={data.home} 
                  advantage={data.advantage}
                  awayTeam={awayTeam}
                  homeTeam={homeTeam}
                />
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* Defensive Efficiency Visualization - Modernized */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Defense Plays Card */}
        <GlassCard glowColor="from-emerald-500/20 to-green-500/20" className="p-5 border-emerald-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-green-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40 shadow-lg shadow-emerald-500/20">
                <Target className="w-6 h-6 text-emerald-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                ELITE
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-white drop-shadow-lg">{defensePlaysAway}</span>
                <span className="text-sm text-gray-400">vs</span>
                <span className="text-3xl font-bold text-white drop-shadow-lg">{defensePlaysHome}</span>
              </div>
              <div className="text-sm text-gray-300 font-medium">Defense Plays Faced</div>
              <div className="mt-3 p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                <div className="text-xs text-emerald-400 font-semibold">
                  {playsAdvantage} Advantage: <span className="text-white">{playsDiff}</span> fewer plays
                </div>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Points Per Opportunity Card */}
        <GlassCard glowColor="from-cyan-500/20 to-blue-500/20" className="p-5 border-cyan-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-cyan-500/20 border border-cyan-500/40 shadow-lg shadow-cyan-500/20">
                <TrendingDown className="w-6 h-6 text-cyan-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                EFFICIENCY
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-white drop-shadow-lg">{pointsPerOppAway}</span>
                <span className="text-sm text-gray-400">vs</span>
                <span className="text-3xl font-bold text-white drop-shadow-lg">{pointsPerOppHome}</span>
              </div>
              <div className="text-sm text-gray-300 font-medium">Points Per Opportunity</div>
              <div className="mt-3 p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
                <div className="text-xs text-cyan-400 font-semibold">
                  {pointsAdvantage} allows <span className="text-white">{pointsDiff}</span> fewer points
                </div>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Turnover Margin Card */}
        <GlassCard glowColor="from-amber-500/20 to-orange-500/20" className="p-5 border-amber-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-amber-500/20 border border-amber-500/40 shadow-lg shadow-amber-500/20">
                <Shield className="w-6 h-6 text-amber-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/40">
                IMPACT
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-white drop-shadow-lg">{turnoverMarginAway}</span>
                <span className="text-sm text-gray-400">vs</span>
                <span className="text-3xl font-bold text-white drop-shadow-lg">{turnoverMarginHome}</span>
              </div>
              <div className="text-sm text-gray-300 font-medium">Turnover Margin</div>
              <div className="mt-3 p-2 rounded-lg bg-amber-500/10 border border-amber-500/30">
                <div className="text-xs text-amber-400 font-semibold">
                  {marginAdvantage} <span className="text-white">+{marginDiff}</span> advantage
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

function DefenseStatRow({ metric, away, home, advantage, awayTeam, homeTeam }: { 
  metric: string; 
  away: string; 
  home: string; 
  advantage: string;
  awayTeam?: any;
  homeTeam?: any;
}) {
  const getAdvantageDisplay = (adv: string) => {
    // Check if advantage matches team name
    const isAwayAdvantage = awayTeam && adv === awayTeam.name;
    const isHomeAdvantage = homeTeam && adv === homeTeam.name;
    
    if (isAwayAdvantage) {
      return (
        <div className="flex items-center justify-center gap-2">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-green-500/20 rounded-lg blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <ImageWithFallback 
              src={awayTeam.logo}
              alt={awayTeam.name}
              className="relative w-7 h-7 object-contain transform hover:scale-125 transition-all duration-200"
              style={{
                filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.4))',
              }}
            />
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-emerald-400 to-green-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/50">
              <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
            </div>
          </div>
        </div>
      );
    }
    
    if (isHomeAdvantage) {
      return (
        <div className="flex items-center justify-center gap-2">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-green-500/20 rounded-lg blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <ImageWithFallback 
              src={homeTeam.logo}
              alt={homeTeam.name}
              className="relative w-7 h-7 object-contain transform hover:scale-125 transition-all duration-200"
              style={{
                filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.4))',
              }}
            />
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-emerald-400 to-green-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/50">
              <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
            </div>
          </div>
        </div>
      );
    }
    
    return (
      <span className="px-3 py-1.5 rounded-full text-xs font-bold text-slate-400 bg-slate-500/20 border border-slate-500/30 hover:border-slate-500/50 transition-colors">
        {adv}
      </span>
    );
  };

  return (
    <tr className="border-b border-gray-700/20 hover:bg-gradient-to-r hover:from-gray-800/40 hover:to-gray-800/20 transition-all duration-200 group">
      <td className="py-4 px-4 text-gray-300 font-semibold group-hover:text-white transition-colors">{metric}</td>
      <td className="py-4 px-4 text-center">
        <span className="font-mono text-base text-gray-200 group-hover:text-white transition-colors font-semibold">
          {away}
        </span>
      </td>
      <td className="py-4 px-4 text-center">
        <span className="font-mono text-base text-gray-200 group-hover:text-white transition-colors font-semibold">
          {home}
        </span>
      </td>
      <td className="py-4 px-4 text-center">
        {getAdvantageDisplay(advantage)}
      </td>
    </tr>
  );
}