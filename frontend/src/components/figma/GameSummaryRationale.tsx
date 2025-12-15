import { GlassCard } from './GlassCard';
import { Target, TrendingUp, TrendingDown, Award, BarChart3, Activity, Calendar, CheckCircle } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface GameSummaryRationaleProps {
  predictionData?: any;
}

// Helper to replace emojis with icon components
const renderTextWithIcons = (text: string) => {
  if (!text) return text;
  
  // Replace emojis with icon names that we can render
  const parts = text.split(/(\📅|\✅|📊|🏈|⚡|🎯)/g);
  
  return parts.map((part, idx) => {
    if (part === '📅') return <Calendar key={idx} className="w-4 h-4 inline-block mx-1 text-blue-400" />;
    if (part === '✅') return <CheckCircle key={idx} className="w-4 h-4 inline-block mx-1 text-emerald-400" />;
    if (part === '📊') return <BarChart3 key={idx} className="w-4 h-4 inline-block mx-1 text-purple-400" />;
    if (part === '🏈') return <Activity key={idx} className="w-4 h-4 inline-block mx-1 text-orange-400" />;
    if (part === '⚡') return <TrendingUp key={idx} className="w-4 h-4 inline-block mx-1 text-yellow-400" />;
    if (part === '🎯') return <Target key={idx} className="w-4 h-4 inline-block mx-1 text-red-400" />;
    return part;
  });
};

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
  const keyAdvantages = summary.key_advantages;
  const bottomLine = summary.bottom_line;
  const marketAnalysis = summary.market_analysis;
  
  // Get team stats for accurate data
  const awayStats = predictionData?.team_statistics?.away;
  const homeStats = predictionData?.team_statistics?.home;
  
  // Build critical stats from team_statistics if summary has zeros
  const criticalStats = summary.critical_stats || {};
  
  // Check if EPA data is missing/zero and populate from team_statistics
  const epaData = (!criticalStats.epa || criticalStats.epa.away_offense === 0) && awayStats && homeStats ? {
    away_offense: awayStats.off_ppa || 0,
    away_defense: awayStats.def_ppa || 0,
    home_offense: homeStats.off_ppa || 0,
    home_defense: homeStats.def_ppa || 0,
    advantage: (awayStats.off_ppa || 0) > (homeStats.off_ppa || 0) ? awayTeam?.name : homeTeam?.name
  } : criticalStats.epa;
  
  // Check if power ratings are missing/zero and populate from team_statistics
  const powerRatings = (!criticalStats.power_ratings || criticalStats.power_ratings.away_fpi === 0) && awayStats && homeStats ? {
    away_fpi: awayStats.fpi || 0,
    home_fpi: homeStats.fpi || 0,
    advantage: (awayStats.fpi || 0) > (homeStats.fpi || 0) ? awayTeam?.name : homeTeam?.name
  } : criticalStats.power_ratings;
  
  // Check if success rates are missing/zero and populate from team_statistics
  const successRates = (!criticalStats.success_rates || criticalStats.success_rates.away_offense === 0) && awayStats && homeStats ? {
    away_offense: ((awayStats.off_success_rate || 0) * 100).toFixed(1),
    away_defense: ((awayStats.def_success_rate || 0) * 100).toFixed(1),
    home_offense: ((homeStats.off_success_rate || 0) * 100).toFixed(1),
    home_defense: ((homeStats.def_success_rate || 0) * 100).toFixed(1),
    offensive_edge: (awayStats.off_success_rate || 0) > (homeStats.off_success_rate || 0) ? awayTeam?.name : homeTeam?.name
  } : criticalStats.success_rates;
  
  const enhancedCriticalStats = {
    epa: epaData,
    power_ratings: powerRatings,
    success_rates: successRates
  };
  
  // Build key advantages from team_statistics if summary has zeros/empty
  const buildKeyAdvantages = () => {
    if (!awayStats || !homeStats) return keyAdvantages;
    
    // Check if keyAdvantages has content or is showing zeros
    const hasValidData = keyAdvantages?.away?.length > 0 && 
                        !keyAdvantages.away[0].includes('0.000') && 
                        !keyAdvantages.away[0].includes('0.0%');
    
    if (hasValidData) return keyAdvantages;
    
    // Build advantages from actual stats
    const awayAdvantages = [];
    const homeAdvantages = [];
    
    // EPA advantages
    if ((awayStats.off_ppa || 0) > (homeStats.off_ppa || 0)) {
      awayAdvantages.push(`Superior offensive EPA: ${awayStats.off_ppa >= 0 ? '+' : ''}${awayStats.off_ppa.toFixed(3)} vs ${homeStats.off_ppa >= 0 ? '+' : ''}${homeStats.off_ppa.toFixed(3)}`);
    } else {
      homeAdvantages.push(`Superior offensive EPA: ${homeStats.off_ppa >= 0 ? '+' : ''}${homeStats.off_ppa.toFixed(3)} vs ${awayStats.off_ppa >= 0 ? '+' : ''}${awayStats.off_ppa.toFixed(3)}`);
    }
    
    if ((awayStats.def_ppa || 0) < (homeStats.def_ppa || 0)) {
      awayAdvantages.push(`Stronger defensive EPA: ${awayStats.def_ppa >= 0 ? '+' : ''}${awayStats.def_ppa.toFixed(3)} vs ${homeStats.def_ppa >= 0 ? '+' : ''}${homeStats.def_ppa.toFixed(3)}`);
    } else {
      homeAdvantages.push(`Stronger defensive EPA: ${homeStats.def_ppa >= 0 ? '+' : ''}${homeStats.def_ppa.toFixed(3)} vs ${awayStats.def_ppa >= 0 ? '+' : ''}${awayStats.def_ppa.toFixed(3)}`);
    }
    
    // Success rate advantages
    if ((awayStats.off_success_rate || 0) > (homeStats.off_success_rate || 0)) {
      awayAdvantages.push(`Better offensive success rate: ${((awayStats.off_success_rate || 0) * 100).toFixed(1)}% vs ${((homeStats.off_success_rate || 0) * 100).toFixed(1)}%`);
    } else {
      homeAdvantages.push(`Better offensive success rate: ${((homeStats.off_success_rate || 0) * 100).toFixed(1)}% vs ${((awayStats.off_success_rate || 0) * 100).toFixed(1)}%`);
    }
    
    if ((awayStats.def_success_rate || 0) < (homeStats.def_success_rate || 0)) {
      awayAdvantages.push(`Better defensive success rate: ${((awayStats.def_success_rate || 0) * 100).toFixed(1)}% vs ${((homeStats.def_success_rate || 0) * 100).toFixed(1)}%`);
    } else {
      homeAdvantages.push(`Better defensive success rate: ${((homeStats.def_success_rate || 0) * 100).toFixed(1)}% vs ${((awayStats.def_success_rate || 0) * 100).toFixed(1)}%`);
    }
    
    // FPI advantage
    if ((awayStats.fpi || 0) > (homeStats.fpi || 0)) {
      awayAdvantages.push(`Higher FPI rating: ${awayStats.fpi.toFixed(1)} vs ${homeStats.fpi.toFixed(1)}`);
    } else {
      homeAdvantages.push(`Higher FPI rating: ${homeStats.fpi.toFixed(1)} vs ${awayStats.fpi.toFixed(1)}`);
    }
    
    // Explosiveness
    if ((awayStats.off_explosiveness || 0) > (homeStats.off_explosiveness || 0)) {
      awayAdvantages.push(`Higher explosiveness: ${awayStats.off_explosiveness.toFixed(2)} vs ${homeStats.off_explosiveness.toFixed(2)}`);
    } else {
      homeAdvantages.push(`Higher explosiveness: ${homeStats.off_explosiveness.toFixed(2)} vs ${awayStats.off_explosiveness.toFixed(2)}`);
    }
    
    // Home field advantage
    homeAdvantages.push('Home field advantage');
    
    return {
      away: awayAdvantages,
      home: homeAdvantages
    };
  };
  
  const enhancedKeyAdvantages = buildKeyAdvantages();

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
            awayValue={`Off: ${enhancedCriticalStats.epa.away_offense >= 0 ? '+' : ''}${enhancedCriticalStats.epa.away_offense.toFixed(3)} | Def: ${enhancedCriticalStats.epa.away_defense >= 0 ? '+' : ''}${enhancedCriticalStats.epa.away_defense.toFixed(3)}`}
            homeValue={`Off: ${enhancedCriticalStats.epa.home_offense >= 0 ? '+' : ''}${enhancedCriticalStats.epa.home_offense.toFixed(3)} | Def: ${enhancedCriticalStats.epa.home_defense >= 0 ? '+' : ''}${enhancedCriticalStats.epa.home_defense.toFixed(3)}`}
            advantage={enhancedCriticalStats.epa.advantage}
            awayLogo={awayTeam?.logo}
            homeLogo={homeTeam?.logo}
          />
          
          {/* FPI */}
          <StatCard
            title="FPI Rating"
            awayTeam={awayTeam?.name}
            homeTeam={homeTeam?.name}
            awayValue={enhancedCriticalStats.power_ratings.away_fpi.toFixed(1)}
            homeValue={enhancedCriticalStats.power_ratings.home_fpi.toFixed(1)}
            advantage={enhancedCriticalStats.power_ratings.advantage}
            awayLogo={awayTeam?.logo}
            homeLogo={homeTeam?.logo}
          />

          {/* Success Rates */}
          <StatCard
            title="Success Rates"
            awayTeam={awayTeam?.name}
            homeTeam={homeTeam?.name}
            awayValue={`Off: ${enhancedCriticalStats.success_rates.away_offense}% | Def: ${enhancedCriticalStats.success_rates.away_defense}%`}
            homeValue={`Off: ${enhancedCriticalStats.success_rates.home_offense}% | Def: ${enhancedCriticalStats.success_rates.home_defense}%`}
            advantage={enhancedCriticalStats.success_rates.offensive_edge}
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
            {enhancedKeyAdvantages.away && enhancedKeyAdvantages.away.length > 0 ? (
              <ul className="space-y-2">
                {enhancedKeyAdvantages.away.map((adv: string, idx: number) => (
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
            {enhancedKeyAdvantages.home && enhancedKeyAdvantages.home.length > 0 ? (
              <ul className="space-y-2">
                {enhancedKeyAdvantages.home.map((adv: string, idx: number) => (
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
        
        <p className="text-gray-200 leading-relaxed mb-4">{renderTextWithIcons(bottomLine.summary)}</p>
        
        {bottomLine.key_factors && bottomLine.key_factors.length > 0 && (
          <div className="pt-4 border-t border-emerald-500/20">
            <div className="text-sm text-emerald-300 font-semibold mb-2">Supporting Factors:</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {bottomLine.key_factors.map((factor: string, idx: number) => (
                <div key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0"></div>
                  <span>{renderTextWithIcons(factor)}</span>
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
