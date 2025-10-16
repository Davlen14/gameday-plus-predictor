import React, { useState } from 'react';
import { Info, ChevronDown, ChevronUp, ArrowRight, ArrowLeft } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';

interface RatingsData {
  // Basic team info
  team?: string;
  conference?: string;
  teamId?: number;
  year?: number;
  ratings_available: boolean;
  
  // Core ratings
  elo: number;
  fpi: number;
  sp_overall: number;
  srs: number;
  composite_rating?: number;
  
  // Legacy field names for compatibility
  elo_rating?: number;
  fpi_rating?: number;
  sp_rating?: number;
  srs_rating?: number;
  
  // Direct efficiency fields
  offensive_efficiency?: number;
  defensive_efficiency?: number;
  special_teams_efficiency?: number;
  
  // FPI Components (comprehensive breakdown)
  fpi_components: {
    offensive_efficiency: number;
    defensive_efficiency: number;
    special_teams_efficiency: number;
    overall_efficiency: number;
  };
  
  // SP+ Components (detailed breakdown)
  sp_components: {
    offense: number;
    defense: number;
    special_teams: number;
  };
  
  // FPI Rankings (all ranking categories)
  fpi_rankings: {
    sos_rank: number;
    remaining_sos_rank: number;
    strength_of_record_rank: number;
    resume_rank: number;
    game_control_rank: number;
    avg_win_probability_rank: number;
  };
  
  // Legacy ranking fields for compatibility
  sos_rank?: number;
  resume_rank?: number;
  game_control_rank?: number;
  
  // Analysis fields
  rating_consistency?: number;
  elite_tier?: boolean;
  struggling_tier?: boolean;
}

interface ComparisonData {
  elo_differential: number;
  fpi_differential: number;
  sp_differential: number;
  srs_differential: number;
  composite_differential: number;
  offensive_efficiency_differential: number;
  defensive_efficiency_differential: number;
  special_teams_differential: number;
  ranking_advantage: string;
  elite_matchup: boolean;
  talent_gap: string;
  consistency_advantage: string;
}

interface ComponentProps {
  predictionData?: {
    comprehensive_ratings?: {
      away_team: RatingsData;
      home_team: RatingsData;
      comparison: ComparisonData;
    };
    team_selector?: {
      away_team: { name: string; primary_color: string; logo: string; abbreviation: string; mascot: string };
      home_team: { name: string; primary_color: string; logo: string; abbreviation: string; mascot: string };
    };
  };
}

interface MetricConfig {
  name: string;
  awayValue: number;
  homeValue: number;
  category: string;
  description: string;
  isRanking?: boolean;
}

const ComprehensiveRatingsComparison: React.FC<ComponentProps> = ({ predictionData }) => {
  const ratingsData = predictionData?.comprehensive_ratings;
  const teamData = predictionData?.team_selector;
  const [expandedMetric, setExpandedMetric] = useState<string | null>(null);

  if (!ratingsData?.away_team?.ratings_available || !ratingsData?.home_team?.ratings_available) {
    return (
      <div className="glass-card p-6 space-y-6">
        <h3 className="text-xl font-bold text-white">Comprehensive Ratings Comparison</h3>
        <p className="text-slate-400">Advanced ratings data not available for this matchup.</p>
      </div>
    );
  }

  const { away_team, home_team, comparison } = ratingsData;
  const away = teamData?.away_team;
  const home = teamData?.home_team;
  const awayColor = away?.primary_color || '#3B82F6';
  const homeColor = home?.primary_color || '#EF4444';

  // Helper function to safely get rating values
  const getRating = (team: RatingsData, fieldName: string): number => {
    const newFieldName = fieldName.replace('_rating', '');
    return (team as any)[newFieldName] ?? (team as any)[fieldName] ?? 0;
  };

  // Metrics configuration with descriptions
  const coreRatings: MetricConfig[] = [
    {
      name: 'ELO Rating',
      awayValue: getRating(away_team, 'elo_rating'),
      homeValue: getRating(home_team, 'elo_rating'),
      category: 'Core Systems',
      description: 'ELO is a rating system that measures team strength based on game results and opponent quality. Higher values indicate stronger teams with better win records against quality opponents.'
    },
    {
      name: 'FPI Rating',
      awayValue: getRating(away_team, 'fpi_rating'),
      homeValue: getRating(home_team, 'fpi_rating'),
      category: 'Core Systems',
      description: 'ESPN\'s Football Power Index predicts team performance using efficiency metrics and strength of schedule. Positive values indicate above-average teams expected to perform well.'
    },
    {
      name: 'SP+ Overall',
      awayValue: getRating(away_team, 'sp_rating'),
      homeValue: getRating(home_team, 'sp_rating'),
      category: 'Core Systems',
      description: 'SP+ measures team efficiency on a per-play basis, adjusted for opponent strength. It combines offensive, defensive, and special teams performance into a comprehensive rating.'
    },
    {
      name: 'SRS Rating',
      awayValue: getRating(away_team, 'srs_rating'),
      homeValue: getRating(home_team, 'srs_rating'),
      category: 'Core Systems',
      description: 'Simple Rating System combines average point differential with strength of schedule. Positive values indicate teams that beat opponents by larger margins against tougher competition.'
    }
  ];

  const efficiencyMetrics: MetricConfig[] = [
    {
      name: 'Offensive Efficiency',
      awayValue: away_team.offensive_efficiency ?? away_team.fpi_components?.offensive_efficiency ?? 50,
      homeValue: home_team.offensive_efficiency ?? home_team.fpi_components?.offensive_efficiency ?? 50,
      category: 'Efficiency',
      description: 'Measures how effectively a team moves the ball and scores points per drive. Higher percentages indicate explosive, consistent offenses that convert opportunities into points.'
    },
    {
      name: 'Defensive Efficiency',
      awayValue: away_team.defensive_efficiency ?? away_team.fpi_components?.defensive_efficiency ?? 50,
      homeValue: home_team.defensive_efficiency ?? home_team.fpi_components?.defensive_efficiency ?? 50,
      category: 'Efficiency',
      description: 'Evaluates how well a defense prevents scoring and limits opponent yards per play. Higher values mean the defense forces more punts, turnovers, and field goals.'
    },
    {
      name: 'Special Teams',
      awayValue: away_team.special_teams_efficiency ?? away_team.fpi_components?.special_teams_efficiency ?? 50,
      homeValue: home_team.special_teams_efficiency ?? home_team.fpi_components?.special_teams_efficiency ?? 50,
      category: 'Efficiency',
      description: 'Accounts for field position gained through kickoffs, punts, returns, and field goal accuracy. Elite special teams can swing field position and momentum significantly.'
    }
  ];

  const rankings: MetricConfig[] = [
    {
      name: 'SOS Rank',
      awayValue: away_team.sos_rank ?? away_team.fpi_rankings?.sos_rank ?? 65,
      homeValue: home_team.sos_rank ?? home_team.fpi_rankings?.sos_rank ?? 65,
      category: 'Rankings',
      description: 'Strength of Schedule ranking measures difficulty of opponents faced. Lower ranks (#1-25) indicate teams that have played tougher competition.',
      isRanking: true
    },
    {
      name: 'Resume Rank',
      awayValue: away_team.resume_rank ?? away_team.fpi_rankings?.resume_rank ?? 65,
      homeValue: home_team.resume_rank ?? home_team.fpi_rankings?.resume_rank ?? 65,
      category: 'Rankings',
      description: 'Resume ranking evaluates the quality and impressiveness of a team\'s wins and losses. Considers margin of victory and opponent strength.',
      isRanking: true
    },
    {
      name: 'Game Control',
      awayValue: away_team.game_control_rank ?? away_team.fpi_rankings?.game_control_rank ?? 65,
      homeValue: home_team.game_control_rank ?? home_team.fpi_rankings?.game_control_rank ?? 65,
      category: 'Rankings',
      description: 'Measures how often teams control games from start to finish. Elite teams dominate time of possession, limit opponent scoring chances, and avoid close finishes.',
      isRanking: true
    }
  ];

  // Calculate bar width for visual representation
  const getBarWidth = (value: number, metric: MetricConfig) => {
    if (metric.isRanking) {
      // For rankings, lower is better, so invert
      const maxRank = Math.max(metric.homeValue, metric.awayValue);
      const normalized = ((maxRank - value) / maxRank) * 100;
      return `${Math.max(normalized, 10)}%`;
    }
    const maxValue = Math.max(metric.homeValue, metric.awayValue);
    return `${(value / maxValue) * 100}%`;
  };

  // Calculate difference with proper color
  const getDifference = (metric: MetricConfig) => {
    const diff = metric.isRanking 
      ? metric.awayValue - metric.homeValue  // For rankings, lower is better
      : metric.homeValue - metric.awayValue;
    
    const absDiff = Math.abs(diff);
    const formatted = metric.isRanking ? absDiff.toFixed(0) : absDiff.toFixed(1);
    
    let color = 'text-cyan-400';
    if (diff > 0) color = `text-[${homeColor}]`;
    if (diff < 0) color = `text-[${awayColor}]`;
    
    const advantage = diff > 0 ? home?.abbreviation : diff < 0 ? away?.abbreviation : 'Even';
    
    return { formatted, color, advantage, diff };
  };

  // Summary calculations
  const getOverallAdvantage = () => {
    const coreAvg = (comparison.elo_differential + comparison.fpi_differential + comparison.sp_differential + comparison.srs_differential) / 4;
    if (Math.abs(coreAvg) < 2) return { team: 'Even', color: 'text-cyan-400' };
    return coreAvg > 0 
      ? { team: home?.abbreviation || 'Home', color: `text-[${homeColor}]` }
      : { team: away?.abbreviation || 'Away', color: `text-[${awayColor}]` };
  };

  const getEfficiencyAdvantage = () => {
    const effAvg = (comparison.offensive_efficiency_differential + comparison.defensive_efficiency_differential + comparison.special_teams_differential) / 3;
    if (Math.abs(effAvg) < 3) return { team: 'Even', color: 'text-cyan-400' };
    return effAvg > 0
      ? { team: home?.abbreviation || 'Home', color: `text-[${homeColor}]` }
      : { team: away?.abbreviation || 'Away', color: `text-[${awayColor}]` };
  };

  // Get match quality rating based on competitiveness and talent level
  const getMatchQuality = () => {
    const avgRating = (getRating(away_team, 'elo_rating') + getRating(home_team, 'elo_rating')) / 2;
    const coreAvg = Math.abs((comparison.elo_differential + comparison.fpi_differential + comparison.sp_differential + comparison.srs_differential) / 4);
    
    // Both teams highly rated (elite matchup)
    if (avgRating > 1600 && coreAvg < 5) {
      return { quality: 'Elite Matchup', description: 'Two top-tier programs with minimal separation in advanced metrics' };
    }
    
    // Close matchup between good teams
    if (avgRating > 1500 && coreAvg < 8) {
      return { quality: 'Competitive Matchup', description: 'Evenly matched teams with similar efficiency profiles' };
    }
    
    // One-sided but high level
    if (avgRating > 1550 && coreAvg > 15) {
      return { quality: 'Mismatch', description: 'Significant talent gap favoring the higher-rated team' };
    }
    
    // Close low-level game
    if (avgRating < 1450 && coreAvg < 8) {
      return { quality: 'Toss-Up', description: 'Neither team holds decisive advantages in key metrics' };
    }
    
    // Moderate advantage
    if (coreAvg >= 8 && coreAvg < 15) {
      return { quality: 'Moderate Advantage', description: 'Clear but not overwhelming edge in core rating systems' };
    }
    
    // Blowout potential
    if (coreAvg >= 20) {
      return { quality: 'Heavy Favorite', description: 'Substantial gap across all advanced metrics and efficiency ratings' };
    }
    
    return { quality: 'Balanced Matchup', description: 'Teams show comparable strength across rating systems' };
  };

  // Determine who has upper hand and build the case
  const getUpperHandAnalysis = () => {
    const coreAvg = (comparison.elo_differential + comparison.fpi_differential + comparison.sp_differential + comparison.srs_differential) / 4;
    const effAvg = (comparison.offensive_efficiency_differential + comparison.defensive_efficiency_differential + comparison.special_teams_differential) / 3;
    
    const coreWinner = coreAvg > 2 ? 'home' : coreAvg < -2 ? 'away' : 'even';
    const effWinner = effAvg > 3 ? 'home' : effAvg < -3 ? 'away' : 'even';
    
    // Build the case
    let winner = 'even';
    let casePoints: string[] = [];
    
    if (coreWinner === 'home' && effWinner === 'home') {
      winner = 'home';
      casePoints = [
        `${home?.name} dominates core rating systems with ${Math.abs(coreAvg).toFixed(1)} point average advantage`,
        `Superior efficiency metrics across offense, defense, and special teams (+${Math.abs(effAvg).toFixed(1)}%)`,
        `Comprehensive edge suggests control in all phases of the game`
      ];
    } else if (coreWinner === 'away' && effWinner === 'away') {
      winner = 'away';
      casePoints = [
        `${away?.name} leads in all core rating systems by ${Math.abs(coreAvg).toFixed(1)} points on average`,
        `Efficiency advantage of ${Math.abs(effAvg).toFixed(1)}% indicates better execution`,
        `Systematic edge across multiple evaluation methods`
      ];
    } else if (coreWinner === 'home' && effWinner === 'away') {
      winner = 'split';
      casePoints = [
        `${home?.name} has stronger overall ratings but ${away?.name} executes more efficiently`,
        `Talent vs. execution dynamic creates competitive uncertainty`,
        `Game outcome may depend on which factor proves more decisive`
      ];
    } else if (coreWinner === 'away' && effWinner === 'home') {
      winner = 'split';
      casePoints = [
        `${away?.name} rated higher but ${home?.name} shows better on-field efficiency`,
        `Contrasting strengths suggest a tactical chess match`,
        `Coaching adjustments could be the difference maker`
      ];
    } else if (coreWinner === 'home' && effWinner === 'even') {
      winner = 'home';
      casePoints = [
        `${home?.name} holds rating advantage while efficiency metrics are balanced`,
        `Slight edge in talent evaluation systems`,
        `Similar execution levels make ratings differential meaningful`
      ];
    } else if (coreWinner === 'away' && effWinner === 'even') {
      winner = 'away';
      casePoints = [
        `${away?.name} leads in ratings with matched efficiency profiles`,
        `Core system advantage without execution gap`,
        `Higher floor based on consistent metric superiority`
      ];
    } else if (coreWinner === 'even' && effWinner === 'home') {
      winner = 'home';
      casePoints = [
        `${home?.name} executes better despite similar ratings`,
        `Efficiency edge of ${Math.abs(effAvg).toFixed(1)}% suggests recent momentum`,
        `Performance trends favor home team execution`
      ];
    } else if (coreWinner === 'even' && effWinner === 'away') {
      winner = 'away';
      casePoints = [
        `${away?.name} shows superior efficiency with matched ratings`,
        `Better execution across all three phases`,
        `Operational advantage despite similar talent assessments`
      ];
    } else {
      winner = 'even';
      casePoints = [
        `Nearly identical ratings and efficiency metrics across both teams`,
        `No clear systematic advantage for either side`,
        `Expect a closely contested game decided by execution and adjustments`
      ];
    }
    
    return { winner, casePoints };
  };

  const matchQuality = getMatchQuality();
  const upperHand = getUpperHandAnalysis();

  return (
    <GlassCard className="p-6 space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between pb-4 border-b border-white/10">
        {/* Away Team (Left) */}
        <div className="flex items-center gap-3">
          <ImageWithFallback 
            src={away?.logo || ''}
            alt={away?.name || 'Away Team'}
            className="w-12 h-12 object-contain"
          />
          <div>
            <div className="text-white" style={{ fontSize: '1.125rem' }}>
              {away?.name || 'Away Team'}
            </div>
            <div className="text-sm text-slate-400">
              {away?.mascot || 'Team'}
            </div>
          </div>
        </div>

        {/* Center Badge */}
        <div className="flex flex-col items-center">
          <div className="text-slate-500 text-xs uppercase tracking-wider mb-1">
            Ratings
          </div>
          <div className="px-3 py-1 rounded-full glass-card-light border border-cyan-500/30 text-cyan-400 text-xs"
               style={{ textShadow: '0 0 10px rgba(34, 211, 238, 0.3)' }}>
            {comparison.elite_matchup ? 'Elite Matchup' : 'Advanced Systems'}
          </div>
        </div>

        {/* Home Team (Right) */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-white" style={{ fontSize: '1.125rem' }}>
              {home?.name || 'Home Team'}
            </div>
            <div className="text-sm text-slate-400">
              {home?.mascot || 'Team'}
            </div>
          </div>
          <ImageWithFallback 
            src={home?.logo || ''}
            alt={home?.name || 'Home Team'}
            className="w-12 h-12 object-contain"
          />
        </div>
      </div>

      {/* Core Rating Systems Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 pb-2">
          <div className="w-1 h-5 rounded-full" style={{ backgroundColor: homeColor }} />
          <h3 className="text-white">Core Rating Systems</h3>
        </div>

        <div className="space-y-3">
          {coreRatings.map((metric) => {
            const diff = getDifference(metric);
            const isExpanded = expandedMetric === metric.name;

            return (
              <div key={metric.name} className="space-y-0">
                <div 
                  className="bg-gray-800/40 backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-gray-800/60"
                  onClick={() => setExpandedMetric(isExpanded ? null : metric.name)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: awayColor,
                          textShadow: `0 0 10px ${awayColor}40`
                        }}
                      >
                        {metric.awayValue.toFixed(1)}
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.awayValue, metric),
                          background: `linear-gradient(to right, ${awayColor}80, ${awayColor})`,
                          boxShadow: `0 0 12px ${awayColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff.diff < -0.1 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{metric.name}</span>
                        {diff.diff > 0.1 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className={`analytical-number text-sm ${diff.color}`}
                        style={{ textShadow: `0 0 8px ${diff.diff > 0 ? homeColor : awayColor}40` }}
                      >
                        {diff.advantage} +{diff.formatted}
                      </div>
                      <span className="text-xs text-slate-500">{metric.category}</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: homeColor,
                          textShadow: `0 0 10px ${homeColor}40`
                        }}
                      >
                        {metric.homeValue.toFixed(1)}
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.homeValue, metric),
                          background: `linear-gradient(to left, ${homeColor}80, ${homeColor})`,
                          boxShadow: `0 0 12px ${homeColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {metric.description}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Efficiency Metrics Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 pb-2">
          <div className="w-1 h-5 rounded-full" style={{ backgroundColor: awayColor }} />
          <h3 className="text-white">Efficiency Metrics</h3>
        </div>

        <div className="space-y-3">
          {efficiencyMetrics.map((metric) => {
            const diff = getDifference(metric);
            const isExpanded = expandedMetric === metric.name;

            return (
              <div key={metric.name} className="space-y-0">
                <div 
                  className="bg-gray-800/40 backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-gray-800/60"
                  onClick={() => setExpandedMetric(isExpanded ? null : metric.name)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: awayColor,
                          textShadow: `0 0 10px ${awayColor}40`
                        }}
                      >
                        {metric.awayValue.toFixed(1)}%
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.awayValue, metric),
                          background: `linear-gradient(to right, ${awayColor}80, ${awayColor})`,
                          boxShadow: `0 0 12px ${awayColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff.diff < -0.1 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{metric.name}</span>
                        {diff.diff > 0.1 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className={`analytical-number text-sm ${diff.color}`}
                        style={{ textShadow: `0 0 8px ${diff.diff > 0 ? homeColor : awayColor}40` }}
                      >
                        {diff.advantage} +{diff.formatted}%
                      </div>
                      <span className="text-xs text-slate-500">{metric.category}</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: homeColor,
                          textShadow: `0 0 10px ${homeColor}40`
                        }}
                      >
                        {metric.homeValue.toFixed(1)}%
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.homeValue, metric),
                          background: `linear-gradient(to left, ${homeColor}80, ${homeColor})`,
                          boxShadow: `0 0 12px ${homeColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10 bg-gray-900/50 backdrop-blur-sm rounded-b-lg px-4 pb-4">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {metric.description}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* FPI Rankings Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 pb-2">
          <div className="w-1 h-5 rounded-full bg-gradient-to-r from-cyan-500 to-blue-500" />
          <h3 className="text-white">FPI Rankings</h3>
        </div>

        <div className="space-y-3">
          {rankings.map((metric) => {
            const diff = getDifference(metric);
            const isExpanded = expandedMetric === metric.name;

            return (
              <div key={metric.name} className="space-y-0">
                <div 
                  className="bg-gray-800/40 backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-gray-800/60"
                  onClick={() => setExpandedMetric(isExpanded ? null : metric.name)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: awayColor,
                          textShadow: `0 0 10px ${awayColor}40`
                        }}
                      >
                        #{metric.awayValue.toFixed(0)}
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.awayValue, metric),
                          background: `linear-gradient(to right, ${awayColor}80, ${awayColor})`,
                          boxShadow: `0 0 12px ${awayColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff.diff < -0.1 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{metric.name}</span>
                        {diff.diff > 0.1 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className={`analytical-number text-sm ${diff.color}`}
                        style={{ textShadow: `0 0 8px ${diff.diff > 0 ? homeColor : awayColor}40` }}
                      >
                        {diff.advantage} +{diff.formatted}
                      </div>
                      <span className="text-xs text-slate-500">{metric.category}</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold" 
                        style={{ 
                          fontSize: '1.25rem',
                          color: homeColor,
                          textShadow: `0 0 10px ${homeColor}40`
                        }}
                      >
                        #{metric.homeValue.toFixed(0)}
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: getBarWidth(metric.homeValue, metric),
                          background: `linear-gradient(to left, ${homeColor}80, ${homeColor})`,
                          boxShadow: `0 0 12px ${homeColor}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10 bg-gray-900/50 backdrop-blur-sm rounded-b-lg px-4 pb-4">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {metric.description}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="space-y-4 pt-4 border-t border-white/10">
        <div className="flex items-center justify-between">
          <h3 className="text-white">Match Quality & Analysis</h3>
          <div className="px-3 py-1 rounded-full glass-card-light border border-cyan-500/30 text-cyan-400 text-xs"
               style={{ textShadow: '0 0 10px rgba(34, 211, 238, 0.3)' }}>
            {matchQuality.quality}
          </div>
        </div>
        
        {/* Upper Hand Analysis Card - Themed with team color */}
        <div 
          className="relative overflow-hidden rounded-xl p-6 border-2 transition-all duration-500"
          style={{ 
            backgroundColor: upperHand.winner === 'away' ? `${awayColor}15` : 
                           upperHand.winner === 'home' ? `${homeColor}15` : 
                           'rgba(42, 47, 56, 0.3)',
            borderColor: upperHand.winner === 'away' ? `${awayColor}40` : 
                        upperHand.winner === 'home' ? `${homeColor}40` : 
                        'rgba(255, 255, 255, 0.1)',
            boxShadow: upperHand.winner === 'away' ? `0 0 30px ${awayColor}20, inset 0 0 60px ${awayColor}10` : 
                      upperHand.winner === 'home' ? `0 0 30px ${homeColor}20, inset 0 0 60px ${homeColor}10` : 
                      '0 8px 32px 0 rgba(0, 0, 0, 0.3)'
          }}
        >
          {/* 3D Team Logo Background */}
          {upperHand.winner !== 'even' && upperHand.winner !== 'split' && (
            <div className="absolute right-6 top-1/2 -translate-y-1/2 opacity-20 pointer-events-none">
              <ImageWithFallback 
                src={upperHand.winner === 'away' ? away?.logo || '' : home?.logo || ''}
                alt="Team Logo"
                className="w-32 h-32 object-contain transform rotate-12"
                style={{ 
                  filter: 'drop-shadow(8px 8px 12px rgba(0,0,0,0.5)) drop-shadow(0px 0px 20px rgba(255,255,255,0.3))',
                  transform: 'perspective(200px) rotateY(-15deg) scale(1.2)'
                }}
              />
            </div>
          )}

          {/* Content */}
          <div className="relative z-10">
            <p className="text-sm text-slate-400 leading-relaxed mb-4">
              {matchQuality.description}
            </p>
            
            <div className="space-y-3">
              <div className="flex items-center gap-3 pb-3 border-b border-white/10">
                <div className="flex items-center gap-2">
                  {upperHand.winner === 'away' && (
                    <div className="flex items-center gap-2">
                      <ArrowLeft className="w-6 h-6 text-green-400 animate-pulse" />
                      <ImageWithFallback 
                        src={away?.logo || ''}
                        alt={away?.name}
                        className="w-8 h-8 object-contain"
                        style={{ filter: 'drop-shadow(0 0 10px rgba(74, 222, 128, 0.5))' }}
                      />
                    </div>
                  )}
                  {upperHand.winner === 'home' && (
                    <div className="flex items-center gap-2">
                      <ImageWithFallback 
                        src={home?.logo || ''}
                        alt={home?.name}
                        className="w-8 h-8 object-contain"
                        style={{ filter: 'drop-shadow(0 0 10px rgba(74, 222, 128, 0.5))' }}
                      />
                      <ArrowRight className="w-6 h-6 text-green-400 animate-pulse" />
                    </div>
                  )}
                  <span 
                    className="text-white font-bold text-lg"
                    style={{ 
                      color: upperHand.winner === 'away' ? awayColor : 
                            upperHand.winner === 'home' ? homeColor : 
                            '#22d3ee',
                      textShadow: upperHand.winner === 'away' ? `0 0 20px ${awayColor}60` : 
                                 upperHand.winner === 'home' ? `0 0 20px ${homeColor}60` : 
                                 '0 0 20px rgba(34, 211, 238, 0.6)'
                    }}
                  >
                    {upperHand.winner === 'away' ? away?.name : 
                     upperHand.winner === 'home' ? home?.name : 
                     upperHand.winner === 'split' ? 'Split Advantages' : 
                     'Even Matchup'}
                  </span>
                </div>
                {upperHand.winner !== 'even' && upperHand.winner !== 'split' && (
                  <span 
                    className="text-sm font-semibold"
                    style={{ 
                      color: upperHand.winner === 'away' ? awayColor : homeColor,
                      opacity: 0.8
                    }}
                  >
                    has the upper hand
                  </span>
                )}
              </div>
              
              <div className="space-y-2">
                {upperHand.casePoints.map((point, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div 
                      className="w-2 h-2 rounded-full mt-1.5"
                      style={{ 
                        backgroundColor: upperHand.winner === 'away' ? awayColor : 
                                        upperHand.winner === 'home' ? homeColor : 
                                        '#22d3ee',
                        boxShadow: upperHand.winner === 'away' ? `0 0 8px ${awayColor}60` : 
                                  upperHand.winner === 'home' ? `0 0 8px ${homeColor}60` : 
                                  '0 0 8px rgba(34, 211, 238, 0.6)'
                      }}
                    />
                    <p className="text-sm text-slate-200 leading-relaxed flex-1">{point}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="glass-card-light p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="text-slate-400 text-sm capitalize mb-1">Overall Rating Advantage</div>
                <div className="flex items-center gap-2">
                  <span className="analytical-number text-white" style={{ fontSize: '1rem' }}>
                    {getOverallAdvantage().team}
                  </span>
                  <div 
                    className="w-2 h-2 rounded-full"
                    style={{ 
                      backgroundColor: getOverallAdvantage().team === 'Even' ? '#22d3ee' : 
                        getOverallAdvantage().team === (away?.abbreviation || 'Away') ? awayColor : homeColor,
                      boxShadow: `0 0 8px ${getOverallAdvantage().team === 'Even' ? '#22d3ee' : 
                        getOverallAdvantage().team === (away?.abbreviation || 'Away') ? awayColor : homeColor}60`
                    }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card-light p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="text-slate-400 text-sm capitalize mb-1">Efficiency Advantage</div>
                <div className="flex items-center gap-2">
                  <span className="analytical-number text-white" style={{ fontSize: '1rem' }}>
                    {getEfficiencyAdvantage().team}
                  </span>
                  <div 
                    className="w-2 h-2 rounded-full"
                    style={{ 
                      backgroundColor: getEfficiencyAdvantage().team === 'Even' ? '#22d3ee' : 
                        getEfficiencyAdvantage().team === (away?.abbreviation || 'Away') ? awayColor : homeColor,
                      boxShadow: `0 0 8px ${getEfficiencyAdvantage().team === 'Even' ? '#22d3ee' : 
                        getEfficiencyAdvantage().team === (away?.abbreviation || 'Away') ? awayColor : homeColor}60`
                    }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card-light p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="text-slate-400 text-sm capitalize mb-1">Talent Gap</div>
                <div className="flex items-center gap-2">
                  <span className="analytical-number text-white" style={{ fontSize: '1rem' }}>
                    {comparison.talent_gap.charAt(0).toUpperCase() + comparison.talent_gap.slice(1)}
                  </span>
                  <div 
                    className="w-2 h-2 rounded-full"
                    style={{ 
                      backgroundColor: comparison.talent_gap === 'minimal' ? '#22d3ee' : 
                        comparison.talent_gap === 'moderate' ? '#fbbf24' : '#ef4444',
                      boxShadow: `0 0 8px ${comparison.talent_gap === 'minimal' ? '#22d3ee' : 
                        comparison.talent_gap === 'moderate' ? '#fbbf24' : '#ef4444'}60`
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="pt-4 border-t border-white/10 flex items-center justify-center gap-6 text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: awayColor }} />
          <span>{away?.abbreviation} Advantage</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: homeColor }} />
          <span>{home?.abbreviation} Advantage</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-cyan-400" />
          <span>Even Matchup</span>
        </div>
      </div>
    </GlassCard>
  );
};

export default ComprehensiveRatingsComparison;