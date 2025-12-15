import { GlassCard } from './GlassCard';
import { Target, TrendingUp, TrendingDown, Award, BarChart3, Activity } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface GameSummaryRationaleProps {
  predictionData?: any;
}

export function GameSummaryRationale({ predictionData }: GameSummaryRationaleProps) {
  // Support both direct and ui_components paths
  const summary = predictionData?.ui_components?.game_summary_and_rationale || predictionData?.game_summary_and_rationale;
  const teams = predictionData?.ui_components?.team_selector || predictionData?.team_selector || predictionData?.header?.teams;
  
  if (!summary || !teams) {
    return null;
  }

  const awayTeam = teams.away_team || teams.away;
  const homeTeam = teams.home_team || teams.home;
  
  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Team colors - use alt_color if primary is blue/black
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || '#f97316') 
    : (awayTeam.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || '#10b981') 
    : (homeTeam.primary_color || '#f97316');
  
  const favoredTeam = summary.favored_team;
  const isFavoredAway = favoredTeam === awayTeam?.name;
  const isFavoredHome = favoredTeam === homeTeam?.name;
  
  // Determine glow color and gradient based on favored team using actual team colors
  const favoredColor = isFavoredAway ? awayTeamColor : homeTeamColor;
  const glowColor = `from-[${favoredColor}]/20 to-[${favoredColor}]/10`;
  const bannerGradient = isFavoredAway 
    ? `from-[${awayTeamColor}]/40 to-[${awayTeamColor}]/30 border-[${awayTeamColor}]/50`
    : `from-[${homeTeamColor}]/40 to-[${homeTeamColor}]/30 border-[${homeTeamColor}]/50`;

  const winProb = summary.win_probability;
  const spreadAnalysis = summary.spread_analysis;
  const totalAnalysis = summary.total_analysis;
  const edgeAnalysis = summary.edge_analysis;
  const criticalStats = summary.critical_stats;
  const keyAdvantages = summary.key_advantages;
  const bottomLine = summary.bottom_line;
  const marketAnalysis = summary.market_analysis;

  return (
    <GlassCard glowColor={glowColor} className="p-6 border-white/20">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-500/40">
          <Target className="w-5 h-5 text-purple-400" />
        </div>
        <h3 className="text-white font-semibold text-lg">Game Summary & Prediction Rationale</h3>
      </div>

      {/* Predicted Winner Banner */}
      <div className="mb-6">
        <div className={`relative overflow-hidden rounded-xl border-2 p-6 bg-gradient-to-br ${bannerGradient}`}
          style={{
            borderColor: favoredColor,
            backgroundColor: `${favoredColor}20`
          }}>
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <ImageWithFallback 
                src={isFavoredAway ? awayTeam?.logo : homeTeam?.logo} 
                alt={favoredTeam} 
                className="w-20 h-20 object-contain drop-shadow-2xl" 
              />
              <div>
                <div className="text-sm text-gray-300 mb-1">Predicted Winner</div>
                <div className="text-3xl font-bold text-white mb-1">{favoredTeam}</div>
                <div className="text-lg text-emerald-400 font-semibold">{winProb.favorite}% Win Probability</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-white mb-1">{spreadAnalysis.spread_display}</div>
              <div className="text-sm text-gray-300">{spreadAnalysis.interpretation}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Win Probability & Score Projection */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Win Probability */}
        <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-5">
          <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" />
            Win Probability
          </h4>
          <div className="space-y-3">
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <ImageWithFallback src={awayTeam?.logo} alt={awayTeam?.name} className="w-6 h-6 object-contain" />
                  <span className="text-sm text-gray-300">{awayTeam?.name}</span>
                </div>
                <span className="text-lg font-bold text-white">{winProb.away}%</span>
              </div>
              <div className="w-full bg-gray-700/40 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-500"
                  style={{ 
                    width: `${winProb.away}%`,
                    background: `linear-gradient(to right, ${awayTeamColor}, ${awayTeamColor}dd)`
                  }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <ImageWithFallback src={homeTeam?.logo} alt={homeTeam?.name} className="w-6 h-6 object-contain" />
                  <span className="text-sm text-gray-300">{homeTeam?.name}</span>
                </div>
                <span className="text-lg font-bold text-white">{winProb.home}%</span>
              </div>
              <div className="w-full bg-gray-700/40 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-500"
                  style={{ 
                    width: `${winProb.home}%`,
                    background: `linear-gradient(to right, ${homeTeamColor}, ${homeTeamColor}dd)`
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Score Projection */}
        <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-5">
          <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-emerald-400" />
            Projected Score
          </h4>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ImageWithFallback src={awayTeam?.logo} alt={awayTeam?.name} className="w-6 h-6 object-contain" />
                <span className="text-sm text-gray-300">{awayTeam?.name}</span>
              </div>
              <span className="text-2xl font-bold text-white">{totalAnalysis.projected_score.away}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ImageWithFallback src={homeTeam?.logo} alt={homeTeam?.name} className="w-6 h-6 object-contain" />
                <span className="text-sm text-gray-300">{homeTeam?.name}</span>
              </div>
              <span className="text-2xl font-bold text-white">{totalAnalysis.projected_score.home}</span>
            </div>
            <div className="pt-3 border-t border-gray-600/40">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Projected Total</span>
                <span className="text-xl font-bold text-emerald-400">{totalAnalysis.predicted_total}</span>
              </div>
              <div className="text-xs text-gray-500 mt-1">{totalAnalysis.pace} game expected</div>
            </div>
          </div>
        </div>
      </div>

      {/* Market Analysis & Sportsbooks */}
      {marketAnalysis && marketAnalysis.sportsbook_lines && marketAnalysis.sportsbook_lines.length > 0 && (
        <div className="mb-6">
          <div className="bg-gradient-to-br from-blue-900/30 to-purple-900/30 border border-blue-500/40 rounded-lg p-6">
            <h4 className="text-blue-300 font-semibold text-lg mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              Live Sportsbook Lines
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {marketAnalysis.sportsbook_lines.map((book: any, idx: number) => (
                <div key={idx} className="backdrop-blur-sm border border-slate-700/50 rounded-lg p-4">
                  <div className="text-center mb-3">
                    <div className="text-white font-semibold">{book.sportsbook}</div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-400">Spread:</span>
                      <span className="text-white font-mono">{book.spread > 0 ? '+' : ''}{book.spread?.toFixed(1) || 'N/A'}</span>
                    </div>
                    {book.total && (
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Total:</span>
                        <span className="text-white font-mono">{book.total?.toFixed(1)}</span>
                      </div>
                    )}
                    {book.odds && (
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">Odds:</span>
                        <span className="text-white font-mono">{book.odds > 0 ? '+' : ''}{book.odds}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Best Bets */}
            {marketAnalysis.best_bets && marketAnalysis.best_bets.length > 0 && (
              <div className="mt-4 pt-4 border-t border-blue-500/20">
                <div className="text-sm text-blue-300 font-semibold mb-3">Recommended Bets:</div>
                <div className="space-y-2">
                  {marketAnalysis.best_bets.map((bet: any, idx: number) => (
                    <div key={idx} className="bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-lg p-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`px-2 py-1 rounded text-xs font-bold ${
                            bet.grade === 'STRONG' ? 'bg-red-500/20 text-red-400' :
                            bet.grade === 'GOOD' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-blue-500/20 text-blue-400'
                          }`}>
                            {bet.grade}
                          </div>
                          <div>
                            <div className="text-white font-semibold">{bet.bet}</div>
                            <div className="text-xs text-gray-400">{bet.sportsbook}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-green-400 font-bold">{bet.edge > 0 ? '+' : ''}{bet.edge?.toFixed(1)} edge</div>
                          <div className="text-xs text-gray-400">{bet.odds > 0 ? '+' : ''}{bet.odds}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Edge Analysis */}
      <div className="mb-6">
        <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 border border-purple-500/30 rounded-lg p-5">
          <h4 className="text-gray-200 font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-400" />
            Overall Edge Analysis
          </h4>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">{awayTeam?.name}</div>
              <div className="text-3xl font-bold" style={{ color: awayTeamColor }}>{edgeAnalysis.away_edge_score}</div>
              <div className="text-xs text-gray-500">Edge Score</div>
            </div>
            <div className="text-center flex items-center justify-center">
              <div className="text-lg font-semibold text-gray-300">vs</div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">{homeTeam?.name}</div>
              <div className="text-3xl font-bold" style={{ color: homeTeamColor }}>{edgeAnalysis.home_edge_score}</div>
              <div className="text-xs text-gray-500">Edge Score</div>
            </div>
          </div>
          <div className="text-center pt-3 border-t border-gray-600/40">
            <span className="text-sm text-gray-300">
              <span className="text-emerald-400 font-bold">{edgeAnalysis.edge_leader}</span> holds a{' '}
              <span className="text-white font-bold">{edgeAnalysis.total_edge}</span> point overall edge
            </span>
          </div>
        </div>
      </div>

      {/* Critical Stats Comparison */}
      <div className="mb-6">
        <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-yellow-400" />
          Critical Stats Comparison
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* EPA */}
          <StatCard
            title="EPA Performance"
            awayTeam={awayTeam?.name}
            homeTeam={homeTeam?.name}
            awayValue={`Off: ${criticalStats.epa.away_offense >= 0 ? '+' : ''}${criticalStats.epa.away_offense.toFixed(3)} | Def: ${criticalStats.epa.away_defense >= 0 ? '+' : ''}${criticalStats.epa.away_defense.toFixed(3)}`}
            homeValue={`Off: ${criticalStats.epa.home_offense >= 0 ? '+' : ''}${criticalStats.epa.home_offense.toFixed(3)} | Def: ${criticalStats.epa.home_defense >= 0 ? '+' : ''}${criticalStats.epa.home_defense.toFixed(3)}`}
            advantage={criticalStats.epa.advantage}
            awayLogo={awayTeam?.logo}
            homeLogo={homeTeam?.logo}
          />
          
          {/* FPI */}
          <StatCard
            title="FPI Rating"
            awayTeam={awayTeam?.name}
            homeTeam={homeTeam?.name}
            awayValue={criticalStats.power_ratings.away_fpi.toFixed(1)}
            homeValue={criticalStats.power_ratings.home_fpi.toFixed(1)}
            advantage={criticalStats.power_ratings.advantage}
            awayLogo={awayTeam?.logo}
            homeLogo={homeTeam?.logo}
          />

          {/* Success Rates */}
          <StatCard
            title="Success Rates"
            awayTeam={awayTeam?.name}
            homeTeam={homeTeam?.name}
            awayValue={`Off: ${criticalStats.success_rates.away_offense}% | Def: ${criticalStats.success_rates.away_defense}%`}
            homeValue={`Off: ${criticalStats.success_rates.home_offense}% | Def: ${criticalStats.success_rates.home_defense}%`}
            advantage={criticalStats.success_rates.offensive_edge}
            awayLogo={awayTeam?.logo}
            homeLogo={homeTeam?.logo}
          />
        </div>
      </div>

      {/* Key Advantages */}
      <div className="mb-6">
        <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
          <Award className="w-5 h-5 text-amber-400" />
          Key Advantages
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Away Team Advantages */}
          <div className="rounded-lg p-4" style={{ 
            backgroundColor: `${awayTeamColor}20`, 
            borderColor: `${awayTeamColor}50`,
            borderWidth: '1px',
            borderStyle: 'solid'
          }}>
            <div className="flex items-center gap-2 mb-3">
              <ImageWithFallback src={awayTeam?.logo} alt={awayTeam?.name} className="w-6 h-6 object-contain" />
              <h5 className="font-semibold" style={{ color: awayTeamColor }}>{awayTeam?.name} Advantages</h5>
            </div>
            {keyAdvantages.away && keyAdvantages.away.length > 0 ? (
              <ul className="space-y-2">
                {keyAdvantages.away.map((adv: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                    <TrendingUp className="w-4 h-4 mt-0.5 flex-shrink-0" style={{ color: awayTeamColor }} />
                    <span>{adv}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500 italic">No significant statistical advantages</p>
            )}
          </div>

          {/* Home Team Advantages */}
          <div className="rounded-lg p-4" style={{ 
            backgroundColor: `${homeTeamColor}20`, 
            borderColor: `${homeTeamColor}50`,
            borderWidth: '1px',
            borderStyle: 'solid'
          }}>
            <div className="flex items-center gap-2 mb-3">
              <ImageWithFallback src={homeTeam?.logo} alt={homeTeam?.name} className="w-6 h-6 object-contain" />
              <h5 className="font-semibold" style={{ color: homeTeamColor }}>{homeTeam?.name} Advantages</h5>
            </div>
            {keyAdvantages.home && keyAdvantages.home.length > 0 ? (
              <ul className="space-y-2">
                {keyAdvantages.home.map((adv: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                    <TrendingUp className="w-4 h-4 mt-0.5 flex-shrink-0" style={{ color: homeTeamColor }} />
                    <span>{adv}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-gray-500 italic">No significant statistical advantages</p>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Line Summary */}
      <div className="bg-gradient-to-br from-emerald-900/30 to-green-900/30 border border-emerald-500/40 rounded-lg p-6">
        <div className="flex items-start gap-3 mb-4">
          <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40">
            <Target className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="flex-1">
            <h4 className="text-emerald-300 font-semibold text-lg mb-1">The Bottom Line</h4>
            <div className="text-sm text-gray-400">
              Confidence: <span className={`font-bold ${
                bottomLine.confidence_level === 'High' ? 'text-emerald-400' : 
                bottomLine.confidence_level === 'Moderate' ? 'text-yellow-400' : 'text-orange-400'
              }`}>{bottomLine.confidence_level}</span> ({bottomLine.confidence_percentage}%)
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400 mb-1">Recommendation</div>
            <div className="text-xl font-bold text-white">{bottomLine.recommendation}</div>
          </div>
        </div>
        
        <p className="text-gray-200 leading-relaxed mb-4">{bottomLine.summary}</p>
        
        {bottomLine.key_factors && bottomLine.key_factors.length > 0 && (
          <div className="pt-4 border-t border-emerald-500/20">
            <div className="text-sm text-emerald-300 font-semibold mb-2">Supporting Factors:</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {bottomLine.key_factors.map((factor: string, idx: number) => (
                <div key={idx} className="flex items-center gap-2 text-sm text-gray-300">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                  <span>{factor}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </GlassCard>
  );
}

interface StatCardProps {
  title: string;
  awayTeam: string;
  homeTeam: string;
  awayValue: string;
  homeValue: string;
  advantage: string;
  awayLogo: string;
  homeLogo: string;
}

function StatCard({ title, awayTeam, homeTeam, awayValue, homeValue, advantage, awayLogo, homeLogo }: StatCardProps) {
  const awayHasAdvantage = advantage === awayTeam;
  const homeHasAdvantage = advantage === homeTeam;
  
  return (
    <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-4">
      <h5 className="text-gray-400 text-sm font-semibold mb-3">{title}</h5>
      <div className="space-y-3">
        <div className={`flex items-center justify-between p-2 rounded transition-all ${awayHasAdvantage ? 'bg-emerald-500/10 border border-emerald-500/30' : 'opacity-70'}`}>
          <div className="flex items-center gap-2">
            <ImageWithFallback src={awayLogo} alt={awayTeam} className="w-5 h-5 object-contain" />
            <span className="text-xs text-gray-300">{awayTeam}</span>
          </div>
          <span className={`text-sm font-bold ${awayHasAdvantage ? 'text-emerald-400' : 'text-gray-400'}`}>
            {awayValue}
          </span>
        </div>
        <div className={`flex items-center justify-between p-2 rounded transition-all ${homeHasAdvantage ? 'bg-emerald-500/10 border border-emerald-500/30' : 'opacity-70'}`}>
          <div className="flex items-center gap-2">
            <ImageWithFallback src={homeLogo} alt={homeTeam} className="w-5 h-5 object-contain" />
            <span className="text-xs text-gray-300">{homeTeam}</span>
          </div>
          <span className={`text-sm font-bold ${homeHasAdvantage ? 'text-emerald-400' : 'text-gray-400'}`}>
            {homeValue}
          </span>
        </div>
      </div>
    </div>
  );
}
