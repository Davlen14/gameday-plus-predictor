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
      <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-6 border-gray-500/40">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
            <Shield className="w-5 h-5 text-red-400" />
          </div>
          <h3 className="text-white font-semibold">Extended Defensive Analytics</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600/40">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Metric</th>
                <th className="text-center py-3 px-4 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team1Logo}
                      alt={team1Name}
                      className="w-8 h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team1Color }}>{team1Name}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team2Logo}
                      alt={team2Name}
                      className="w-8 h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team2Color }}>{team2Name}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-300 font-medium">Advantage</th>
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
      <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-6 border-gray-500/40">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
            <BarChart3 className="w-5 h-5 text-purple-400" />
          </div>
          <h3 className="text-white font-semibold">Season Summary Statistics</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600/40">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Metric</th>
                <th className="text-center py-3 px-4 text-gray-300 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team1Logo}
                      alt={team1Name}
                      className="w-8 h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team1Color }}>{team1Name}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-300 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team2Logo}
                      alt={team2Name}
                      className="w-8 h-8 object-contain transform hover:scale-110 transition-transform duration-200"
                      style={{
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                        transform: 'perspective(100px) rotateX(15deg)'
                      }}
                    />
                    <span style={{ color: team2Color }}>{team2Name}</span>
                  </div>
                </th>
                <th className="text-center py-3 px-4 text-gray-300 font-medium">Advantage</th>
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

      {/* Defensive Efficiency Visualization */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <GlassCard glowColor="from-green-500/20 to-emerald-500/20" className="p-4 border-green-500/40 text-center">
          <Target className="w-8 h-8 text-green-400 mx-auto mb-3" />
          <div className="text-2xl font-bold text-green-400 mb-1">{defensePlaysAway} vs {defensePlaysHome}</div>
          <div className="text-sm text-gray-300">Defense Plays Faced</div>
          <div className="text-xs text-green-400 mt-1">{playsAdvantage} Advantage: {playsDiff} fewer</div>
        </GlassCard>

        <GlassCard glowColor="from-blue-500/20 to-cyan-500/20" className="p-4 border-blue-500/40 text-center">
          <TrendingDown className="w-8 h-8 text-blue-400 mx-auto mb-3" />
          <div className="text-2xl font-bold text-blue-400 mb-1">{pointsPerOppAway} vs {pointsPerOppHome}</div>
          <div className="text-sm text-gray-300">Points Per Opportunity</div>
          <div className="text-xs text-blue-400 mt-1">{pointsAdvantage} allows {pointsDiff} fewer</div>
        </GlassCard>

        <GlassCard glowColor="from-amber-500/20 to-yellow-500/20" className="p-4 border-amber-500/40 text-center">
          <Shield className="w-8 h-8 text-amber-400 mx-auto mb-3" />
          <div className="text-2xl font-bold text-amber-400 mb-1">{turnoverMarginAway} vs {turnoverMarginHome}</div>
          <div className="text-sm text-gray-300">Turnover Margin</div>
          <div className="text-xs text-amber-400 mt-1">{marginAdvantage} +{marginDiff} advantage</div>
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
        <div className="flex items-center justify-center gap-1">
          <div className="relative">
            <ImageWithFallback 
              src={awayTeam.logo}
              alt={awayTeam.name}
              className="w-6 h-6 object-contain transform hover:scale-110 transition-transform duration-200"
              style={{
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                transform: 'perspective(100px) rotateX(15deg)'
              }}
            />
            <Check className="absolute -top-1 -right-1 w-3 h-3 text-green-400 bg-green-900/80 rounded-full p-0.5" />
          </div>
        </div>
      );
    }
    
    if (isHomeAdvantage) {
      return (
        <div className="flex items-center justify-center gap-1">
          <div className="relative">
            <ImageWithFallback 
              src={homeTeam.logo}
              alt={homeTeam.name}
              className="w-6 h-6 object-contain transform hover:scale-110 transition-transform duration-200"
              style={{
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                transform: 'perspective(100px) rotateX(15deg)'
              }}
            />
            <Check className="absolute -top-1 -right-1 w-3 h-3 text-green-400 bg-green-900/80 rounded-full p-0.5" />
          </div>
        </div>
      );
    }
    
    return (
      <span className="px-2 py-1 rounded-full text-xs font-semibold text-gray-400 bg-slate-500/20">
        {adv}
      </span>
    );
  };

  return (
    <tr className="border-b border-gray-700/30 hover:bg-gray-800/30 transition-colors">
      <td className="py-3 px-4 text-gray-300 font-medium">{metric}</td>
      <td className="py-3 px-4 text-center font-mono text-gray-200">{away}</td>
      <td className="py-3 px-4 text-center font-mono text-gray-200">{home}</td>
      <td className="py-3 px-4 text-center">
        {getAdvantageDisplay(advantage)}
      </td>
    </tr>
  );
}