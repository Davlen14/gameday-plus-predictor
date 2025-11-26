import { GlassCard } from './GlassCard';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { useEffect, useState } from 'react';

interface ATSComparisonProps {
  predictionData?: any;
}

interface ATSData {
  year: number;
  teamId: number;
  team: string;
  conference: string | null;
  games: number;
  atsWins: number;
  atsLosses: number;
  atsPushes: number;
  avgCoverMargin: number;
}

export function ATSComparison({ predictionData }: ATSComparisonProps) {
  const [atsData, setAtsData] = useState<ATSData[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Extract team data
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png" };
  
  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    // Check for blue colors (dark blue, navy, etc.)
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    // Check for black/very dark colors
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Team colors - use alt_color if primary is blue/black
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam.primary_color || awayTeam.color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam.primary_color || homeTeam.color || '#f97316');

  // Load ATS data
  useEffect(() => {
    const loadAtsData = async () => {
      try {
        const response = await fetch('/ats_data_2025.json');
        const data = await response.json();
        setAtsData(data);
        setLoading(false);
      } catch (error) {
        console.error('Error loading ATS data:', error);
        setLoading(false);
      }
    };
    
    loadAtsData();
  }, []);

  // Find team ATS records
  const homeTeamATS = atsData.find(team => 
    team.team.toLowerCase() === homeTeam.name.toLowerCase()
  );
  
  const awayTeamATS = atsData.find(team => 
    team.team.toLowerCase() === awayTeam.name.toLowerCase()
  );

  // Calculate ATS percentages
  const calculateATSPercentage = (wins: number, losses: number, pushes: number) => {
    const totalGames = wins + losses + pushes;
    if (totalGames === 0) return 0;
    return (wins / totalGames) * 100;
  };

  const homeATSPct = homeTeamATS ? calculateATSPercentage(homeTeamATS.atsWins, homeTeamATS.atsLosses, homeTeamATS.atsPushes) : 0;
  const awayATSPct = awayTeamATS ? calculateATSPercentage(awayTeamATS.atsWins, awayTeamATS.atsLosses, awayTeamATS.atsPushes) : 0;

  // Determine ATS rating
  const getATSRating = (percentage: number) => {
    if (percentage >= 60) return { label: 'ELITE', color: '#10b981' };
    if (percentage >= 55) return { label: 'STRONG', color: '#3b82f6' };
    if (percentage >= 50) return { label: 'AVERAGE', color: '#f59e0b' };
    if (percentage >= 45) return { label: 'BELOW AVG', color: '#f97316' };
    return { label: 'POOR', color: '#ef4444' };
  };

  const homeRating = getATSRating(homeATSPct);
  const awayRating = getATSRating(awayATSPct);

  if (loading) {
    return (
      <GlassCard className="p-4 sm:p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
        </div>
      </GlassCard>
    );
  }

  return (
    <GlassCard className="p-4 sm:p-6">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <Activity className="w-5 h-5 text-purple-400" />
          Against The Spread (ATS) Performance
        </h3>
        <div className="flex items-center gap-2 px-3 py-1 bg-purple-500/30 rounded-full border border-purple-400/50 backdrop-blur-sm">
          <span className="text-purple-400 font-bold text-xs">2025 SEASON</span>
        </div>
      </div>

      {/* ATS Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Away Team Card */}
        <div 
          className="relative overflow-hidden rounded-xl p-5 border-2 backdrop-blur-sm transition-all duration-300"
          style={{
            borderColor: `${awayTeamColor}50`,
            background: `linear-gradient(135deg, ${awayTeamColor}25 0%, ${awayTeamColor}10 50%, ${awayTeamColor}05 100%)`,
            boxShadow: `0 0 20px ${awayTeamColor}15`
          }}
        >
          {/* Team Logo Background */}
          <div className="absolute right-4 top-1/2 -translate-y-1/2 opacity-10">
            <ImageWithFallback 
              src={awayTeam.logo}
              alt={awayTeam.name}
              className="w-24 h-24 object-contain"
              style={{ filter: 'drop-shadow(4px 4px 8px rgba(0,0,0,0.5))' }}
            />
          </div>

          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback
                src={awayTeam.logo}
                alt={awayTeam.name}
                className="w-12 h-12 object-contain"
                style={{ filter: `drop-shadow(0 0 8px ${awayTeamColor}80)` }}
              />
              <div>
                <h4 
                  className="font-bold text-lg font-orbitron"
                  style={{ 
                    color: awayTeamColor,
                    textShadow: `0 0 10px ${awayTeamColor}40`
                  }}
                >
                  {awayTeam.name}
                </h4>
                <p className="text-slate-400 text-xs font-orbitron">Away Team</p>
              </div>
            </div>

            {awayTeamATS ? (
              <>
                {/* ATS Record */}
                <div className="mb-4">
                  <p className="text-slate-400 text-xs mb-2 font-orbitron">ATS Record</p>
                  <div className="flex items-baseline gap-2">
                    <span 
                      className="text-4xl font-bold font-orbitron"
                      style={{ 
                        color: awayTeamColor,
                        textShadow: `0 0 12px ${awayTeamColor}50`
                      }}
                    >
                      {awayTeamATS.atsWins}-{awayTeamATS.atsLosses}
                    </span>
                    {awayTeamATS.atsPushes > 0 && (
                      <span className="text-slate-400 text-lg font-orbitron">-{awayTeamATS.atsPushes}</span>
                    )}
                  </div>
                </div>

                {/* ATS Percentage */}
                <div className="mb-4">
                  <p className="text-slate-400 text-xs mb-2 font-orbitron">Cover Rate</p>
                  <div className="flex items-center gap-3">
                    <span 
                      className="text-3xl font-bold font-orbitron"
                      style={{ 
                        color: awayRating.color,
                        textShadow: `0 0 12px ${awayRating.color}50`
                      }}
                    >
                      {awayATSPct.toFixed(1)}%
                    </span>
                    <div 
                      className="px-2 py-1 rounded-lg border"
                      style={{
                        backgroundColor: `${awayRating.color}25`,
                        borderColor: `${awayRating.color}50`
                      }}
                    >
                      <span 
                        className="text-xs font-bold font-orbitron"
                        style={{ color: awayRating.color }}
                      >
                        {awayRating.label}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Average Cover Margin */}
                <div className="pt-3 border-t" style={{ borderColor: `${awayTeamColor}30` }}>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-xs font-orbitron">Avg Cover Margin</span>
                    <div className="flex items-center gap-2">
                      {awayTeamATS.avgCoverMargin > 0 ? (
                        <TrendingUp className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-400" />
                      )}
                      <span 
                        className={`text-lg font-bold font-orbitron ${awayTeamATS.avgCoverMargin > 0 ? 'text-emerald-400' : 'text-red-400'}`}
                      >
                        {awayTeamATS.avgCoverMargin > 0 ? '+' : ''}{awayTeamATS.avgCoverMargin.toFixed(1)}
                      </span>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-4">
                <p className="text-slate-400 text-sm">No ATS data available</p>
              </div>
            )}
          </div>
        </div>

        {/* Home Team Card */}
        <div 
          className="relative overflow-hidden rounded-xl p-5 border-2 backdrop-blur-sm transition-all duration-300"
          style={{
            borderColor: `${homeTeamColor}50`,
            background: `linear-gradient(135deg, ${homeTeamColor}25 0%, ${homeTeamColor}10 50%, ${homeTeamColor}05 100%)`,
            boxShadow: `0 0 20px ${homeTeamColor}15`
          }}
        >
          {/* Team Logo Background */}
          <div className="absolute right-4 top-1/2 -translate-y-1/2 opacity-10">
            <ImageWithFallback 
              src={homeTeam.logo}
              alt={homeTeam.name}
              className="w-24 h-24 object-contain"
              style={{ filter: 'drop-shadow(4px 4px 8px rgba(0,0,0,0.5))' }}
            />
          </div>

          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback
                src={homeTeam.logo}
                alt={homeTeam.name}
                className="w-12 h-12 object-contain"
                style={{ filter: `drop-shadow(0 0 8px ${homeTeamColor}80)` }}
              />
              <div>
                <h4 
                  className="font-bold text-lg font-orbitron"
                  style={{ 
                    color: homeTeamColor,
                    textShadow: `0 0 10px ${homeTeamColor}40`
                  }}
                >
                  {homeTeam.name}
                </h4>
                <p className="text-slate-400 text-xs font-orbitron">Home Team</p>
              </div>
            </div>

            {homeTeamATS ? (
              <>
                {/* ATS Record */}
                <div className="mb-4">
                  <p className="text-slate-400 text-xs mb-2 font-orbitron">ATS Record</p>
                  <div className="flex items-baseline gap-2">
                    <span 
                      className="text-4xl font-bold font-orbitron"
                      style={{ 
                        color: homeTeamColor,
                        textShadow: `0 0 12px ${homeTeamColor}50`
                      }}
                    >
                      {homeTeamATS.atsWins}-{homeTeamATS.atsLosses}
                    </span>
                    {homeTeamATS.atsPushes > 0 && (
                      <span className="text-slate-400 text-lg font-orbitron">-{homeTeamATS.atsPushes}</span>
                    )}
                  </div>
                </div>

                {/* ATS Percentage */}
                <div className="mb-4">
                  <p className="text-slate-400 text-xs mb-2 font-orbitron">Cover Rate</p>
                  <div className="flex items-center gap-3">
                    <span 
                      className="text-3xl font-bold font-orbitron"
                      style={{ 
                        color: homeRating.color,
                        textShadow: `0 0 12px ${homeRating.color}50`
                      }}
                    >
                      {homeATSPct.toFixed(1)}%
                    </span>
                    <div 
                      className="px-2 py-1 rounded-lg border"
                      style={{
                        backgroundColor: `${homeRating.color}25`,
                        borderColor: `${homeRating.color}50`
                      }}
                    >
                      <span 
                        className="text-xs font-bold font-orbitron"
                        style={{ color: homeRating.color }}
                      >
                        {homeRating.label}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Average Cover Margin */}
                <div className="pt-3 border-t" style={{ borderColor: `${homeTeamColor}30` }}>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-xs font-orbitron">Avg Cover Margin</span>
                    <div className="flex items-center gap-2">
                      {homeTeamATS.avgCoverMargin > 0 ? (
                        <TrendingUp className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-400" />
                      )}
                      <span 
                        className={`text-lg font-bold font-orbitron ${homeTeamATS.avgCoverMargin > 0 ? 'text-emerald-400' : 'text-red-400'}`}
                      >
                        {homeTeamATS.avgCoverMargin > 0 ? '+' : ''}{homeTeamATS.avgCoverMargin.toFixed(1)}
                      </span>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-4">
                <p className="text-slate-400 text-sm">No ATS data available</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ATS Comparison Summary */}
      {homeTeamATS && awayTeamATS && (
        <div 
          className="relative overflow-hidden rounded-lg p-4 border backdrop-blur-sm"
          style={{
            borderColor: 'rgba(168, 85, 247, 0.3)',
            background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(168, 85, 247, 0.05) 100%)'
          }}
        >
          <div className="flex items-start gap-3">
            <Activity className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
            <div>
              <h5 className="text-purple-400 font-bold text-sm mb-2 font-orbitron">ATS Betting Intelligence</h5>
              <p className="text-slate-300 text-sm leading-relaxed">
                {homeATSPct > awayATSPct ? (
                  <>
                    <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam.name}</span> has covered {homeATSPct.toFixed(1)}% of spreads this season ({homeTeamATS.atsWins}-{homeTeamATS.atsLosses}), 
                    {(homeATSPct - awayATSPct).toFixed(1)}% better than <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam.name}</span>'s {awayATSPct.toFixed(1)}% rate ({awayTeamATS.atsWins}-{awayTeamATS.atsLosses}).
                  </>
                ) : awayATSPct > homeATSPct ? (
                  <>
                    <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam.name}</span> has covered {awayATSPct.toFixed(1)}% of spreads this season ({awayTeamATS.atsWins}-{awayTeamATS.atsLosses}), 
                    {(awayATSPct - homeATSPct).toFixed(1)}% better than <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam.name}</span>'s {homeATSPct.toFixed(1)}% rate ({homeTeamATS.atsWins}-{homeTeamATS.atsLosses}).
                  </>
                ) : (
                  <>
                    Both teams have identical {homeATSPct.toFixed(1)}% ATS cover rates this season. 
                    <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam.name}</span> ({homeTeamATS.atsWins}-{homeTeamATS.atsLosses}) and 
                    <span style={{ color: awayTeamColor }} className="font-bold ml-1">{awayTeam.name}</span> ({awayTeamATS.atsWins}-{awayTeamATS.atsLosses}).
                  </>
                )}
                {' '}
                {homeTeamATS.avgCoverMargin > 0 && awayTeamATS.avgCoverMargin < 0 && (
                  <span className="text-emerald-400 font-semibold">
                    {homeTeam.name} averages beating the spread by {homeTeamATS.avgCoverMargin.toFixed(1)} points while {awayTeam.name} typically falls short by {Math.abs(awayTeamATS.avgCoverMargin).toFixed(1)} points.
                  </span>
                )}
                {awayTeamATS.avgCoverMargin > 0 && homeTeamATS.avgCoverMargin < 0 && (
                  <span className="text-emerald-400 font-semibold">
                    {awayTeam.name} averages beating the spread by {awayTeamATS.avgCoverMargin.toFixed(1)} points while {homeTeam.name} typically falls short by {Math.abs(homeTeamATS.avgCoverMargin).toFixed(1)} points.
                  </span>
                )}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* What It Means */}
      <div className="mt-4 pt-4 border-t border-gray-600/40">
        <p className="text-slate-400 text-xs">
          <span className="font-semibold text-purple-400">What is ATS?</span> Against The Spread (ATS) records show how often teams cover the betting spread. 
          A team with a high ATS percentage consistently performs better than oddsmakers expect, indicating potential betting value. 
          Teams covering &gt;55% are historically profitable bets.
        </p>
      </div>
    </GlassCard>
  );
}
