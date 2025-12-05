import React, { useMemo, useState, useEffect } from 'react';
import { Users, Trophy, Target, TrendingUp, Award, TrendingDown, GraduationCap, Activity, DollarSign, BarChart3, CheckCircle2, AlertTriangle, Zap, Star } from 'lucide-react';
import { ClearGlassCard } from './ClearGlassCard';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { RankBadge, getRankCategory } from './RankBadge';
import { FactorCard } from './FactorCard';
import { ComparisonBar } from './ComparisonBar';
import { CoachTimeline } from './CoachTimeline';
import coachRankings from '../../data/coaches_advanced_rankings.json';
import coachHeadshots from '../../data/power5_coaches_headshots.json';
import type { CoachRanking } from '../../types/coaching.types';
import './CoachingComponents.css';

interface CoachingComparisonProps {
  coach1Data?: any;
  coach2Data?: any;
  predictionData?: any;
}

// Get coach headshot from power5_coaches_headshots.json
const getCoachHeadshotUrl = (coachName: string, teamName: string): string | null => {
  if (!coachName || !teamName) return null;
  
  const allCoaches = [
    ...(coachHeadshots as any).big12 || [],
    ...(coachHeadshots as any).acc || [],
    ...(coachHeadshots as any).big_ten || [],
    ...(coachHeadshots as any).sec || []
  ];
  
  const coach = allCoaches.find((c: any) => {
    if (!c.coach || !c.school) return false;
    const coachLower = c.coach.toLowerCase();
    const schoolLower = c.school.toLowerCase();
    const nameLower = coachName.toLowerCase();
    const teamLower = teamName.toLowerCase();
    
    return coachLower.includes(nameLower) ||
           nameLower.includes(coachLower) ||
           schoolLower === teamLower;
  });
  
  return coach?.headshot_url || null;
};

const findCoachData = (teamName: string, coachName?: string): CoachRanking | undefined => {
  if (!teamName && !coachName) return undefined;
  
  // Primary: Look up by team name (most reliable)
  if (teamName) {
    const searchTeam = teamName.toLowerCase();
    const byTeam = (coachRankings as any[]).find(coach => {
      const team = coach?.team?.toLowerCase();
      return team && team === searchTeam;
    }) as CoachRanking | undefined;
    
    if (byTeam) return byTeam;
  }
  
  // Fallback: Look up by coach name if team lookup fails
  if (coachName) {
    const searchName = coachName.toLowerCase();
    return (coachRankings as any[]).find(coach => {
      const name = coach?.name?.toLowerCase();
      return name && (name.includes(searchName) || searchName.includes(name));
    }) as CoachRanking | undefined;
  }
  
  return undefined;
};

const removeEmojis = (text: string): string => {
  if (!text) return text;
  return text.replace(/[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '').trim();
};

const calculateBigGameRating = (bigGameAnalysis: any): number => {
  return bigGameAnalysis?.big_game_score || 0;
};

// Load timeline data for a coach
const loadCoachTimeline = async (coachName: string, teamName: string): Promise<any> => {
  try {
    // Convert name to file format (e.g., "Brian Kelly" -> "kelly_lsu")
    const lastName = coachName.split(' ').pop()?.toLowerCase() || '';
    const schoolSlug = teamName.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z_]/g, '');
    
    // Try to load FULL career timeline first (multi-school data)
    try {
      const fullTimelineModule = await import(`../../data/coach_timelines/${lastName}_${schoolSlug}_FULL_timeline.json`);
      console.log(`Loaded FULL career timeline for ${coachName}`);
      return fullTimelineModule.default || fullTimelineModule;
    } catch {
      // If FULL doesn't exist, fall back to single-school timeline
      const timelineModule = await import(`../../data/coach_timelines/${lastName}_${schoolSlug}_timeline.json`);
      return timelineModule.default || timelineModule;
    }
  } catch (error) {
    console.warn(`Timeline data not found for ${coachName} at ${teamName}`, error);
    return null;
  }
};

const CoachProfileCard = ({ coach, coachData }: { coach: any, coachData: any }) => {
  const category = getRankCategory(coachData.composite_rank);
  const analysis = coachData.enhanced_analysis;
  const season2025 = analysis.season_2025;
  const isTopTier = coachData.composite_rank <= 10;
  const teamColor = coach.primary_color || coach.color || '#6366f1';
  
  return (
    <div 
      className="relative rounded-xl overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${teamColor}08 0%, ${teamColor}03 100%)`
      }}
    >
      {/* Watermark Logo */}
      <div className="absolute top-0 right-0 w-48 h-48 opacity-5 overflow-hidden">
        <ImageWithFallback 
          src={coach.logo || coach.logos?.[0] || ''} 
          alt={coach.school || 'Team'} 
          className="w-full h-full object-contain scale-150"
        />
      </div>

      {/* Rank Badge with Glow */}
      <div className="absolute top-4 left-4 z-10">
        <div 
          className="px-3 py-1.5 rounded-lg font-bold text-sm"
          style={{
            background: `linear-gradient(135deg, ${teamColor}20, ${teamColor}10)`,
            boxShadow: `0 0 20px ${teamColor}25`,
            color: teamColor
          }}
        >
          <div className="flex items-center gap-1.5">
            {isTopTier ? <Star className="w-3.5 h-3.5" /> : <Target className="w-3.5 h-3.5" />}
            <span>#{coachData.composite_rank} {category.label}</span>
          </div>
        </div>
      </div>

      {/* Score Badge */}
      <div className="absolute top-4 right-4 z-10">
        <div 
          className="text-3xl font-black"
          style={{ 
            color: teamColor,
            textShadow: `0 0 20px ${teamColor}80, 0 0 40px ${teamColor}40`
          }}
        >
          {coachData.composite_score.toFixed(1)}/100
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10 pt-16 pb-6 px-6">
        {/* Coach Headshot - No Container, Direct Integration */}
        <div className="flex items-center gap-4 mb-6">
          <div className="relative w-24 h-24">
            <ImageWithFallback 
              src={getCoachHeadshotUrl(coachData.name, coach.school || coachData.team) || coach.logo || coach.logos?.[0]}
              alt={coachData.name}
              className="w-full h-full object-cover rounded-full"
              style={{ 
                filter: 'brightness(1.1) contrast(1.15)',
                boxShadow: `0 0 30px ${teamColor}40, 0 0 60px ${teamColor}20`
              }}
            />
          </div>
          
          <div className="flex-1">
            <h5 className="font-black text-white text-xl mb-1 drop-shadow-lg">{coachData.name}</h5>
            <p 
              className="text-base font-bold mb-1 drop-shadow-md"
              style={{ color: teamColor }}
            >
              {coachData.team}
            </p>
            <p className="text-xs text-gray-400 font-medium">{coachData.conference}</p>
          </div>
        </div>

        {/* 2025 Season Stats */}
        <div 
          className="mb-5 p-4 rounded-lg"
          style={{
            background: `linear-gradient(135deg, ${teamColor}15, ${teamColor}06)`
          }}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="text-xs text-gray-400 font-semibold tracking-wide">2025 SEASON</div>
            <div 
              className="text-xs font-bold px-2 py-1 rounded"
              style={{ 
                color: teamColor,
                background: `${teamColor}20`
              }}
            >
              {removeEmojis(season2025.rating)}
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <div 
              className="text-3xl font-black"
              style={{ color: teamColor }}
            >
              {coachData['2025Record']}
            </div>
            <div className="text-sm text-gray-300">
              ({season2025.win_pct.toFixed(1)}% Win Rate)
            </div>
          </div>
        </div>

        {/* Recent Momentum */}
        <div className="mb-5">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-gray-400 font-semibold tracking-wide">RECENT MOMENTUM</span>
            <span 
              className="text-lg font-black"
              style={{ color: teamColor }}
            >
              {(analysis.recent_trend?.weighted_win_pct || 0).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-800/30 rounded-full h-2.5 overflow-hidden">
            <div 
              className="h-full rounded-full transition-all duration-1000"
              style={{ 
                width: `${analysis.recent_trend.weighted_win_pct}%`,
                background: `linear-gradient(90deg, ${teamColor}, ${teamColor}80)`,
                boxShadow: `0 0 10px ${teamColor}60`
              }}
            />
          </div>
        </div>

        {/* Career Stats Grid */}
        <div className="grid grid-cols-2 gap-3">
          <div 
            className="p-3 rounded-lg"
            style={{
              background: 'rgba(15, 23, 42, 0.3)'
            }}
          >
            <div className="text-xs text-gray-400 mb-1 font-medium">CAREER</div>
            <div className="font-black text-white text-lg">{coachData.careerRecord}</div>
            <div 
              className="text-sm font-bold mt-0.5"
              style={{ color: teamColor }}
            >
              {(coachData.careerWinPct || 0).toFixed(1)}%
            </div>
          </div>
          <div 
            className="p-3 rounded-lg"
            style={{
              background: 'rgba(15, 23, 42, 0.3)'
            }}
          >
            <div className="text-xs text-gray-400 mb-1 font-medium">CLASSIFICATION</div>
            <div className="font-black text-white text-lg">Rank {coachData.composite_rank}</div>
            <div className="text-sm text-gray-300 mt-0.5">{category.label}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export function CoachingComparison({ coach1Data, coach2Data, predictionData }: CoachingComparisonProps) {
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;

  if (!awayTeam || !homeTeam) {
    return null;
  }

  // Get team names and coach names for lookup
  const awayTeamName = awayTeam.name;
  const homeTeamName = homeTeam.name;
  const apiCoach1Name = predictionData?.coaching_data?.away?.coach_name || awayTeam.coach;
  const apiCoach2Name = predictionData?.coaching_data?.home?.coach_name || homeTeam.coach;
  
  // Look up coaches by TEAM NAME first (more reliable), fallback to coach name
  const coach1Advanced = useMemo(() => 
    findCoachData(awayTeamName, apiCoach1Name), 
    [awayTeamName, apiCoach1Name]
  );
  const coach2Advanced = useMemo(() => 
    findCoachData(homeTeamName, apiCoach2Name), 
    [homeTeamName, apiCoach2Name]
  );  // Load timeline data
  const [coach1Timeline, setCoach1Timeline] = useState<any>(null);
  const [coach2Timeline, setCoach2Timeline] = useState<any>(null);

  useEffect(() => {
    if (coach1Advanced) {
      loadCoachTimeline(coach1Advanced.name, coach1Advanced.team).then(setCoach1Timeline);
    }
    if (coach2Advanced) {
      loadCoachTimeline(coach2Advanced.name, coach2Advanced.team).then(setCoach2Timeline);
    }
  }, [coach1Advanced, coach2Advanced]);

  if (!coach1Advanced || !coach2Advanced) {
    return (
      <ClearGlassCard className="p-6">
        <div className="text-center text-gray-400">
          <p>Advanced coaching analysis not available for these coaches.</p>
          <p className="text-sm mt-2">Looking for: {apiCoach1Name} vs {apiCoach2Name}</p>
        </div>
      </ClearGlassCard>
    );
  }

  return (
    <ClearGlassCard className="p-4 sm:p-6">
      <div className="flex items-center gap-2 sm:gap-3 mb-6 sm:mb-8">
        <div className="p-1.5 sm:p-2 rounded-lg" style={{ background: 'rgba(148, 163, 184, 0.08)' }}>
          <Users className="w-4 h-4 sm:w-5 sm:h-5 text-gray-400" />
        </div>
        <div>
          <h3 className="text-white font-semibold text-sm sm:text-base">
            Advanced Coaching Analysis
          </h3>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Comprehensive 9-Factor Performance Evaluation
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <CoachProfileCard coach={awayTeam} coachData={coach1Advanced} />
        <CoachProfileCard coach={homeTeam} coachData={coach2Advanced} />
      </div>

      <div className="mb-6 sm:mb-8">
        <h4 className="text-gray-300 font-medium mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
          <TrendingUp className="w-3 h-3 sm:w-4 sm:h-4 text-emerald-400" />
          Head-to-Head Comparison
        </h4>
        <div className="rounded-lg p-4 sm:p-6" style={{ background: 'rgba(15, 23, 42, 0.2)' }}>
          <ComparisonBar
            label="Overall Rank"
            coach1Value={coach1Advanced.composite_rank}
            coach2Value={coach2Advanced.composite_rank}
            max={72}
            inverse={true}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
          <ComparisonBar
            label="Composite Score"
            coach1Value={coach1Advanced.composite_score}
            coach2Value={coach2Advanced.composite_score}
            max={100}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
          <ComparisonBar
            label="2025 Win %"
            coach1Value={coach1Advanced.enhanced_analysis.season_2025.win_pct}
            coach2Value={coach2Advanced.enhanced_analysis.season_2025.win_pct}
            max={100}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
          <ComparisonBar
            label="Career Win %"
            coach1Value={coach1Advanced.careerWinPct}
            coach2Value={coach2Advanced.careerWinPct}
            max={100}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
          <ComparisonBar
            label="Recent Momentum"
            coach1Value={coach1Advanced.enhanced_analysis.recent_trend.weighted_win_pct}
            coach2Value={coach2Advanced.enhanced_analysis.recent_trend.weighted_win_pct}
            max={100}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
          <ComparisonBar
            label="NFL Draft Picks"
            coach1Value={coach1Advanced.enhanced_analysis.draft_analysis?.total_picks || 0}
            coach2Value={coach2Advanced.enhanced_analysis.draft_analysis?.total_picks || 0}
            max={Math.max(
              coach1Advanced.enhanced_analysis.draft_analysis?.total_picks || 0,
              coach2Advanced.enhanced_analysis.draft_analysis?.total_picks || 0,
              1
            ) * 1.2}
            coach1Name={coach1Advanced.name}
            coach2Name={coach2Advanced.name}
            coach1Color={awayTeam.primary_color || awayTeam.color || '#6366f1'}
            coach2Color={homeTeam.primary_color || homeTeam.color || '#3b82f6'}
          />
        </div>
      </div>

      {[
        { name: coach1Advanced.name, data: coach1Advanced, color: awayTeam.primary_color || awayTeam.color || '#6366f1' },
        { name: coach2Advanced.name, data: coach2Advanced, color: homeTeam.primary_color || homeTeam.color || '#3b82f6' }
      ].map((coachInfo, idx) => (
        <div key={idx} className="mb-6 sm:mb-8">
          <h4 className="text-gray-300 font-medium mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
            <Award className={`w-3 h-3 sm:w-4 sm:h-4 ${idx === 0 ? 'text-purple-400' : 'text-blue-400'}`} style={{ filter: `drop-shadow(0 0 6px ${idx === 0 ? 'rgba(168,85,247,0.7)' : 'rgba(59,130,246,0.7)'})` }} />
            {coachInfo.name} - 9-Factor Analysis
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            <FactorCard
              title="2025 Season"
              weight="25%"
              rating={coachInfo.data.enhanced_analysis.season_2025.season_score}
              icon={<Trophy className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Record', value: coachInfo.data.enhanced_analysis.season_2025.record },
                { label: 'Win %', value: `${(coachInfo.data.enhanced_analysis.season_2025?.win_pct || 0).toFixed(1)}%` },
                { label: 'Quality Wins', value: coachInfo.data.enhanced_analysis.season_2025.quality_wins },
                { label: 'Blowout Wins', value: coachInfo.data.enhanced_analysis.season_2025.blowout_wins }
              ]}
              badge={removeEmojis(coachInfo.data.enhanced_analysis.season_2025.rating)}
            />

            <FactorCard
              title="Recent Momentum"
              weight="15%"
              rating={coachInfo.data.enhanced_analysis.recent_trend.weighted_win_pct}
              icon={<TrendingUp className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Weighted Win%', value: `${(coachInfo.data.enhanced_analysis.recent_trend?.weighted_win_pct || 0).toFixed(1)}%` },
                { label: 'Trend', value: (coachInfo.data.enhanced_analysis.recent_trend?.avg_trend || 0) >= 0
                    ? `+${(coachInfo.data.enhanced_analysis.recent_trend?.avg_trend || 0).toFixed(1)}%`
                    : `${(coachInfo.data.enhanced_analysis.recent_trend?.avg_trend || 0).toFixed(1)}%`,
                  className: (coachInfo.data.enhanced_analysis.recent_trend?.avg_trend || 0) >= 0 ? 'text-green-400' : 'text-red-400'
                }
              ]}
            />

            <FactorCard
              title="Career Success"
              weight="15%"
              rating={coachInfo.data.careerWinPct}
              icon={<BarChart3 className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Record', value: coachInfo.data.careerRecord },
                { label: 'Win%', value: `${(coachInfo.data.careerWinPct || 0).toFixed(1)}%` },
                { label: 'Total Wins', value: coachInfo.data.totalWins || 0 }
              ]}
            />

            <FactorCard
              title="Talent Management"
              weight="15%"
              rating={Math.max(0, 50 + coachInfo.data.enhanced_analysis.talent_context.performance_delta)}
              icon={coachInfo.data.enhanced_analysis.talent_context.classification.includes('Miracle') ? <Zap className="w-5 h-5" style={{ color: coachInfo.color }} /> :
                    coachInfo.data.enhanced_analysis.talent_context.classification.includes('Underachieving') ? <AlertTriangle className="w-5 h-5" style={{ color: coachInfo.color }} /> : <CheckCircle2 className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Tier', value: coachInfo.data.enhanced_analysis.talent_context.tier },
              { label: 'Expected', value: `${coachInfo.data.enhanced_analysis.talent_context.expected_win_pct}%` },
              { label: 'Actual', value: `${(coachInfo.data.enhanced_analysis.talent_context?.actual_win_pct || 0).toFixed(1)}%` },
              { label: 'Delta', value: (coachInfo.data.enhanced_analysis.talent_context?.performance_delta || 0) >= 0
                    ? `+${(coachInfo.data.enhanced_analysis.talent_context?.performance_delta || 0).toFixed(1)}%`
                    : `${(coachInfo.data.enhanced_analysis.talent_context?.performance_delta || 0).toFixed(1)}%`,
                  className: coachInfo.data.enhanced_analysis.talent_context.performance_delta >= 0 ? 'text-green-400' : 'text-red-400'
                }
              ]}
              badge={removeEmojis(coachInfo.data.enhanced_analysis.talent_context.classification)}
            />

            <FactorCard
              title="Big Games"
              weight="12%"
              rating={calculateBigGameRating(coachInfo.data.enhanced_analysis.big_game_analysis)}
              icon={<Award className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'vs Top 5', value: coachInfo.data.enhanced_analysis.big_game_analysis.vs_top5_record || '0-0' },
                { label: 'Clutch Rating', value: removeEmojis(coachInfo.data.enhanced_analysis.big_game_analysis.clutch_rating) },
                { label: 'Big Games', value: coachInfo.data.enhanced_analysis.big_game_analysis.big_games_total || 0 }
              ]}
            />

            <FactorCard
              title="Recruiting"
              weight="12%"
              rating={coachInfo.data.enhanced_analysis.recruiting?.talent_rating || 50}
              icon={<GraduationCap className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Career Avg', value: coachInfo.data.enhanced_analysis.recruiting?.avg_talent_composite ? coachInfo.data.enhanced_analysis.recruiting.avg_talent_composite.toFixed(1) : 'Coming Soon' },
                { label: 'Recent Avg', value: coachInfo.data.enhanced_analysis.recruiting?.recent_avg_composite ? coachInfo.data.enhanced_analysis.recruiting.recent_avg_composite.toFixed(1) : 'Coming Soon' },
                { label: 'Rating', value: coachInfo.data.enhanced_analysis.recruiting?.talent_rating ? `${coachInfo.data.enhanced_analysis.recruiting.talent_rating}/100` : 'In Progress' }
              ]}
            />

            <FactorCard
              title="NFL Development"
              weight="8%"
              rating={coachInfo.data.enhanced_analysis.draft_analysis?.score || 0}
              icon={<Activity className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Total Picks', value: coachInfo.data.enhanced_analysis.draft_analysis?.total_picks || 0 },
                { label: '1st Rounders', value: coachInfo.data.enhanced_analysis.draft_analysis?.first_rounders || 0 },
                { label: 'Top 10', value: coachInfo.data.enhanced_analysis.draft_analysis?.top10_picks || 0 },
                { label: 'Draft Score', value: coachInfo.data.enhanced_analysis.draft_analysis?.score || 0 }
              ]}
            />

            <FactorCard
              title="Betting Performance 2025"
              weight="10%"
              rating={coachInfo.data.enhanced_analysis.betting_2025?.cover_rate || 0}
              icon={<DollarSign className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Games', value: coachInfo.data.enhanced_analysis.betting_2025?.total || 0 },
                { label: 'Covers', value: coachInfo.data.enhanced_analysis.betting_2025?.covers || 0 },
                { label: 'Cover Rate', value: `${(coachInfo.data.enhanced_analysis.betting_2025?.cover_rate || 0).toFixed(0)}%` }
              ]}
            />

            <FactorCard
              title="Consistency"
              weight="2%"
              rating={coachInfo.data.enhanced_analysis.consistency?.score || 0}
              icon={<TrendingDown className="w-5 h-5" style={{ color: coachInfo.color }} />}
              stats={[
                { label: 'Score', value: `${(coachInfo.data.enhanced_analysis.consistency?.score || 0).toFixed(1)}/100` },
                { label: 'Rating', value: removeEmojis(coachInfo.data.enhanced_analysis.consistency?.rating || 'N/A') }
              ]}
            />
          </div>
        </div>
      ))}

      {/* Coach Timeline Charts */}
      <div className="mb-6 sm:mb-8">
        <h3 className="text-base sm:text-lg font-semibold text-white mb-4 sm:mb-6 flex items-center gap-2 sm:gap-3">
          <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5 text-purple-400" style={{ filter: 'drop-shadow(0 0 6px rgba(168,85,247,0.7))' }} />
          Coaching Timeline - AP Poll Rankings
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CoachTimeline
            coachName={coach1Advanced.name}
            schoolName={coach1Advanced.team}
            teamColor={awayTeam.color}
            teamLogo={awayTeam.logo}
            timelineData={coach1Timeline}
          />
          <CoachTimeline
            coachName={coach2Advanced.name}
            schoolName={coach2Advanced.team}
            teamColor={homeTeam.color}
            teamLogo={homeTeam.logo}
            timelineData={coach2Timeline}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-lg p-4 sm:p-6" style={{ background: 'rgba(15, 23, 42, 0.2)' }}>
          <h4 className="text-base sm:text-lg font-semibold text-white mb-3 flex items-center gap-2">
            <Award className="w-4 h-4 sm:w-5 sm:h-5 text-purple-400 drop-shadow-[0_0_6px_rgba(168,85,247,0.7)]" />
            {coach1Advanced.name} Summary
          </h4>
          <p className="text-gray-200 leading-relaxed text-xs sm:text-sm">
            {coach1Advanced.coach_summary}
          </p>
        </div>
        <div className="rounded-lg p-4 sm:p-6" style={{ background: 'rgba(15, 23, 42, 0.2)' }}>
          <h4 className="text-base sm:text-lg font-semibold text-white mb-3 flex items-center gap-2">
            <Award className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400 drop-shadow-[0_0_6px_rgba(59,130,246,0.7)]" />
            {coach2Advanced.name} Summary
          </h4>
          <p className="text-gray-200 leading-relaxed text-xs sm:text-sm">
            {coach2Advanced.coach_summary}
          </p>
        </div>
      </div>
    </ClearGlassCard>
  );
}
