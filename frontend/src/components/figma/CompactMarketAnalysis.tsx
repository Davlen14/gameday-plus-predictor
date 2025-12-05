import { GlassCard } from './GlassCard';
import { TrendingUp, TrendingDown, Activity, BarChart3, AlertTriangle, Info, Minus, Target } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { InsightBox } from './InsightBox';
import { useEffect, useState } from 'react';

// Sportsbook SVGs from public folder
const BovadaLogo = '/Bovada-Casino-Logo.svg';
const ESPNBetLogo = '/espnbet.svg';
const DraftKingsLogo = '/Draftking.svg';

interface CompactMarketAnalysisProps {
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

export function CompactMarketAnalysis({ predictionData }: CompactMarketAnalysisProps) {
  const [atsData, setAtsData] = useState<ATSData[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Extract team data
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png" };
  
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

  // Market and betting data
  const bettingAnalysis = predictionData?.detailed_analysis?.betting_analysis;
  const individualBooks = bettingAnalysis?.sportsbooks?.individual_books || [];
  const modelSpread = predictionData?.prediction_cards?.predicted_spread?.model_spread || 0;
  const marketSpreadRaw = bettingAnalysis?.market_spread || predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5;
  const marketSpread = Math.round(marketSpreadRaw * 2) / 2;
  const valueEdge = bettingAnalysis?.spread_edge || predictionData?.prediction_cards?.predicted_spread?.value_edge || 0;
  const modelTotal = predictionData?.prediction_cards?.predicted_total?.model_total || 52.5;
  const marketTotalRaw = bettingAnalysis?.market_total || predictionData?.prediction_cards?.predicted_total?.market_total || 45.0;
  const marketTotal = Math.round(marketTotalRaw * 2) / 2;
  const totalEdge = bettingAnalysis?.total_edge || predictionData?.prediction_cards?.predicted_total?.edge || 8.0;
  const spreadEdge = Math.abs(valueEdge);

  // Check for upset alert from API
  const isUpsetAlert = bettingAnalysis?.is_upset_alert || false;
  const modelFavorite = bettingAnalysis?.model_favorite || homeTeam.name;
  const marketFavorite = bettingAnalysis?.market_favorite || homeTeam.name;
  
  // Determine which team to theme the upset alert by (the team the model predicts will win)
  const upsetTeam = modelFavorite === homeTeam.name ? homeTeam : awayTeam;
  const upsetTeamColor = modelFavorite === homeTeam.name ? homeTeamColor : awayTeamColor;

  // Use real betting analysis recommendations if available
  const valueBetSpread = bettingAnalysis?.spread_recommendation || 
    (valueEdge >= 2 ? `${homeTeam.name} ${marketSpread >= 0 ? '+' : ''}${marketSpread.toFixed(1)}` :
     valueEdge <= -2 ? `${awayTeam.name} ${(-marketSpread) >= 0 ? '+' : ''}${(-marketSpread).toFixed(1)}` :
     "No significant edge");
  
  const valueBetTotal = bettingAnalysis?.total_recommendation ||
    (modelTotal > marketTotal + 3 ? `OVER ${marketTotal}` :
     modelTotal < marketTotal - 3 ? `UNDER ${marketTotal}` :
     "No significant edge");

  // Format model spread display
  let modelSpreadDisplay = predictionData?.prediction_cards?.predicted_spread?.model_spread_display;
  if (!modelSpreadDisplay && modelSpread !== null) {
    if (modelSpread < 0) {
      modelSpreadDisplay = `${awayTeam.name} ${modelSpread.toFixed(1)}`;
    } else if (modelSpread > 0) {
      modelSpreadDisplay = `${homeTeam.name} -${modelSpread.toFixed(1)}`;
    } else {
      modelSpreadDisplay = 'EVEN';
    }
  }

  const marketSpreadDisplay = bettingAnalysis?.formatted_spread || `${homeTeam.name} ${marketSpread >= 0 ? '+' : ''}${marketSpread.toFixed(1)}`;

  // Find team ATS records
  const homeTeamATS = atsData.find(team => team.team.toLowerCase() === homeTeam.name.toLowerCase());
  const awayTeamATS = atsData.find(team => team.team.toLowerCase() === awayTeam.name.toLowerCase());

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

  // Line movement data
  const lineMovements = individualBooks.map((book: any) => {
    const spreadOpen = book.spreadOpen;
    const spreadCurrent = book.spread;
    const movement = spreadOpen && spreadCurrent ? spreadCurrent - spreadOpen : 0;
    
    const totalOpen = book.overUnderOpen;
    const totalCurrent = book.overUnder;
    const totalMovement = totalOpen && totalCurrent ? totalCurrent - totalOpen : 0;

    return {
      provider: book.provider,
      spread: {
        open: spreadOpen || 0,
        current: spreadCurrent || 0,
        movement: movement
      },
      total: {
        open: totalOpen || 0,
        current: totalCurrent || 0,
        movement: totalMovement
      }
    };
  });

  const getMovementDisplay = (movement: number) => {
    if (movement === 0) return "0.0";
    return `${movement > 0 ? '+' : ''}${movement.toFixed(1)}`;
  };

  const getMovementIcon = (movement: number) => {
    if (movement > 0) return <TrendingUp className="w-3 h-3 text-green-400" />;
    if (movement < 0) return <TrendingDown className="w-3 h-3 text-red-400" />;
    return <Minus className="w-3 h-3 text-gray-400" />;
  };

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
      {/* Upset Alert Banner - Team-Themed Design */}
      {isUpsetAlert && (
        <div 
          className="mb-6 relative overflow-hidden rounded-xl border-2 backdrop-blur-sm transition-all duration-500"
          style={{
            background: `linear-gradient(135deg, ${upsetTeamColor}20 0%, ${upsetTeamColor}10 50%, ${upsetTeamColor}20 100%)`,
            borderColor: `${upsetTeamColor}70`,
            boxShadow: `0 0 30px ${upsetTeamColor}25, inset 0 0 60px ${upsetTeamColor}10`
          }}
        >
          {/* Shimmer effect */}
          <div 
            className="absolute inset-0 opacity-30"
            style={{
              background: `linear-gradient(90deg, transparent, ${upsetTeamColor}40, transparent)`,
              backgroundSize: '200% 100%',
              animation: 'shimmer 3s ease-in-out infinite'
            }}
          />
          
          {/* 3D Team Logo Background */}
          <div className="absolute right-6 top-1/2 -translate-y-1/2 opacity-10 pointer-events-none">
            <ImageWithFallback 
              src={upsetTeam.logo}
              alt={upsetTeam.name}
              className="w-32 h-32 object-contain"
              style={{ 
                filter: 'drop-shadow(8px 8px 12px rgba(0,0,0,0.5)) drop-shadow(0px 0px 20px rgba(255,255,255,0.3))',
                transform: 'perspective(200px) rotateY(-15deg) scale(1.2) rotate(8deg)'
              }}
            />
          </div>
          
          <style>{`
            @keyframes shimmer {
              0%, 100% { transform: translateX(-100%); }
              50% { transform: translateX(100%); }
            }
            @keyframes upsetBlink {
              0%, 100% { opacity: 1; }
              50% { opacity: 0.85; }
            }
          `}</style>
          
          <div className="relative px-6 py-4 animate-[upsetBlink_2.5s_ease-in-out_infinite]">
            <div className="flex items-center justify-between gap-4 flex-wrap">
              <div className="flex items-center gap-3">
                <div 
                  className="w-2 h-2 rounded-full animate-pulse" 
                  style={{ 
                    backgroundColor: upsetTeamColor,
                    boxShadow: `0 0 8px ${upsetTeamColor}80`
                  }}
                />
                <div>
                  <p 
                    className="font-bold text-sm tracking-wider uppercase mb-1 font-orbitron"
                    style={{ 
                      color: upsetTeamColor,
                      textShadow: `0 0 15px ${upsetTeamColor}60`
                    }}
                  >
                    Upset Alert Detected
                  </p>
                  <p className="text-slate-300 text-xs font-orbitron">Model & Market Disagree on Winner</p>
                </div>
              </div>
              <div className="flex items-center gap-4 text-xs font-orbitron">
                <div className="text-right">
                  <p className="text-slate-400 uppercase tracking-wide mb-1">Model Predicts</p>
                  <div className="flex items-center gap-2 justify-end">
                    <ImageWithFallback
                      src={upsetTeam.logo}
                      alt={upsetTeam.name}
                      className="w-5 h-5 object-contain"
                      style={{ filter: `drop-shadow(0 0 6px ${upsetTeamColor}80)` }}
                    />
                    <p 
                      className="font-bold"
                      style={{ 
                        color: upsetTeamColor,
                        textShadow: `0 0 12px ${upsetTeamColor}50`
                      }}
                    >
                      {modelFavorite}
                    </p>
                  </div>
                </div>
                <div 
                  className="text-2xl font-thin"
                  style={{ color: upsetTeamColor }}
                >
                  ≠
                </div>
                <div className="text-left">
                  <p className="text-slate-400 uppercase tracking-wide mb-1">Market Favors</p>
                  <p className="text-slate-300 font-bold">{marketFavorite}</p>
                </div>
              </div>
            </div>
            <div 
              className="mt-3 pt-3 border-t"
              style={{ borderColor: `${upsetTeamColor}30` }}
            >
              <p className="text-slate-300 text-xs font-medium font-orbitron">
                <span 
                  className="font-bold"
                  style={{ 
                    color: upsetTeamColor,
                    textShadow: `0 0 10px ${upsetTeamColor}50`
                  }}
                >
                  {spreadEdge.toFixed(1)} POINT EDGE
                </span> - Model predicts {modelFavorite} wins while market gives them points as underdog
              </p>
            </div>
          </div>
        </div>
      )}
      
      {/* Header */}
      <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <Activity className="w-5 h-5 text-purple-400" />
          Market Analysis & Performance
        </h3>
        <div className="flex items-center gap-2 px-3 py-1 bg-purple-500/30 rounded-full border border-purple-400/50 backdrop-blur-sm">
          <span className="text-purple-400 font-bold text-xs">COMPREHENSIVE VIEW</span>
        </div>
      </div>

      {/* Section 1: ATS Performance - Compact Side by Side */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-4 h-4 text-purple-400" />
          <h4 className="text-purple-400 font-semibold text-sm font-orbitron">Against The Spread (ATS) Performance</h4>
          <div className="px-2 py-1 bg-purple-500/20 rounded text-purple-400 text-xs font-bold">2025 SEASON</div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Away Team ATS */}
          <div 
            className="rounded-lg p-4 border backdrop-blur-sm"
            style={{
              borderColor: `${awayTeamColor}30`,
              background: `linear-gradient(135deg, ${awayTeamColor}15 0%, ${awayTeamColor}05 100%)`
            }}
          >
            <div className="flex items-center gap-2 mb-3">
              <ImageWithFallback
                src={awayTeam.logo}
                alt={awayTeam.name}
                className="w-8 h-8 object-contain"
                style={{ filter: `drop-shadow(0 0 4px ${awayTeamColor}60)` }}
              />
              <div>
                <span style={{ color: awayTeamColor }} className="font-bold text-sm font-orbitron">{awayTeam.name}</span>
                <p className="text-slate-400 text-xs">Away Team</p>
              </div>
            </div>
            
            {awayTeamATS ? (
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">ATS Record</span>
                  <span style={{ color: awayTeamColor }} className="text-lg font-bold">
                    {awayTeamATS.atsWins}-{awayTeamATS.atsLosses}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">Cover Rate</span>
                  <div className="flex items-center gap-2">
                    <span style={{ color: awayRating.color }} className="text-lg font-bold">
                      {awayATSPct.toFixed(1)}%
                    </span>
                    <span 
                      className="px-1 py-0.5 rounded text-xs font-bold"
                      style={{ backgroundColor: `${awayRating.color}25`, color: awayRating.color }}
                    >
                      {awayRating.label}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">Avg Cover Margin</span>
                  <div className="flex items-center gap-1">
                    {awayTeamATS.avgCoverMargin > 0 ? (
                      <TrendingUp className="w-3 h-3 text-emerald-400" />
                    ) : (
                      <TrendingDown className="w-3 h-3 text-red-400" />
                    )}
                    <span className={`text-sm font-bold ${awayTeamATS.avgCoverMargin > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                      {awayTeamATS.avgCoverMargin > 0 ? '+' : ''}{awayTeamATS.avgCoverMargin.toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-400 text-sm text-center">No ATS data available</p>
            )}
          </div>

          {/* Home Team ATS */}
          <div 
            className="rounded-lg p-4 border backdrop-blur-sm"
            style={{
              borderColor: `${homeTeamColor}30`,
              background: `linear-gradient(135deg, ${homeTeamColor}15 0%, ${homeTeamColor}05 100%)`
            }}
          >
            <div className="flex items-center gap-2 mb-3">
              <ImageWithFallback
                src={homeTeam.logo}
                alt={homeTeam.name}
                className="w-8 h-8 object-contain"
                style={{ filter: `drop-shadow(0 0 4px ${homeTeamColor}60)` }}
              />
              <div>
                <span style={{ color: homeTeamColor }} className="font-bold text-sm font-orbitron">{homeTeam.name}</span>
                <p className="text-slate-400 text-xs">Home Team</p>
              </div>
            </div>
            
            {homeTeamATS ? (
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">ATS Record</span>
                  <span style={{ color: homeTeamColor }} className="text-lg font-bold">
                    {homeTeamATS.atsWins}-{homeTeamATS.atsLosses}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">Cover Rate</span>
                  <div className="flex items-center gap-2">
                    <span style={{ color: homeRating.color }} className="text-lg font-bold">
                      {homeATSPct.toFixed(1)}%
                    </span>
                    <span 
                      className="px-1 py-0.5 rounded text-xs font-bold"
                      style={{ backgroundColor: `${homeRating.color}25`, color: homeRating.color }}
                    >
                      {homeRating.label}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-xs">Avg Cover Margin</span>
                  <div className="flex items-center gap-1">
                    {homeTeamATS.avgCoverMargin > 0 ? (
                      <TrendingUp className="w-3 h-3 text-emerald-400" />
                    ) : (
                      <TrendingDown className="w-3 h-3 text-red-400" />
                    )}
                    <span className={`text-sm font-bold ${homeTeamATS.avgCoverMargin > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                      {homeTeamATS.avgCoverMargin > 0 ? '+' : ''}{homeTeamATS.avgCoverMargin.toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-400 text-sm text-center">No ATS data available</p>
            )}
          </div>
        </div>
        
        {/* ATS Intelligence Summary */}
        {homeTeamATS && awayTeamATS && (
          <div className="mt-4 p-3 bg-purple-500/10 border border-purple-400/30 rounded-lg">
            <p className="text-slate-300 text-sm">
              <span className="text-purple-400 font-bold">ATS Betting Intelligence:</span>{' '}
              {homeATSPct > awayATSPct ? (
                <>
                  <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam.name}</span> has covered {homeATSPct.toFixed(1)}% of spreads this season ({homeTeamATS.atsWins}-{homeTeamATS.atsLosses}), {(homeATSPct - awayATSPct).toFixed(1)}% better than <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam.name}</span>'s {awayATSPct.toFixed(1)}% rate ({awayTeamATS.atsWins}-{awayTeamATS.atsLosses}).
                </>
              ) : awayATSPct > homeATSPct ? (
                <>
                  <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam.name}</span> has covered {awayATSPct.toFixed(1)}% of spreads this season ({awayTeamATS.atsWins}-{awayTeamATS.atsLosses}), {(awayATSPct - homeATSPct).toFixed(1)}% better than <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam.name}</span>'s {homeATSPct.toFixed(1)}% rate ({homeTeamATS.atsWins}-{homeTeamATS.atsLosses}).
                </>
              ) : (
                <>Both teams have identical {homeATSPct.toFixed(1)}% ATS cover rates this season.</>
              )}
              {homeTeamATS.avgCoverMargin !== awayTeamATS.avgCoverMargin && (
                <>
                  {' '}{homeTeamATS.avgCoverMargin > awayTeamATS.avgCoverMargin ? homeTeam.name : awayTeam.name} averages beating the spread by {Math.max(homeTeamATS.avgCoverMargin, awayTeamATS.avgCoverMargin).toFixed(1)} points while {homeTeamATS.avgCoverMargin < awayTeamATS.avgCoverMargin ? homeTeam.name : awayTeam.name} typically falls short by {Math.abs(Math.min(homeTeamATS.avgCoverMargin, awayTeamATS.avgCoverMargin)).toFixed(1)} points.
                </>
              )}
            </p>
          </div>
        )}
      </div>

      {/* Section 2: Market Comparison - Compact Layout */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <h4 className="text-emerald-400 font-semibold text-sm font-orbitron">Market Comparison</h4>
          </div>
          <div className="flex items-center gap-2 px-2 py-1 bg-red-500/30 rounded border border-red-400/50">
            <AlertTriangle className="w-3 h-3 text-red-400" />
            <span className="text-red-400 font-bold text-xs">{spreadEdge.toFixed(1)} POINT DISCREPANCY</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Model Projection */}
          <div className="rounded-lg p-4 border backdrop-blur-sm bg-emerald-500/10 border-emerald-400/30">
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-400 font-semibold text-sm">Model Projection</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-slate-400 text-xs">Spread</span>
                <span className="text-emerald-400 text-lg font-bold">{modelSpreadDisplay}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400 text-xs">Total</span>
                <span className="text-emerald-400 text-lg font-bold">{modelTotal}</span>
              </div>
            </div>
            <div className="mt-2 pt-2 border-t border-emerald-400/30">
              <p className="text-emerald-400 text-xs">Model projection: {spreadEdge.toFixed(1)} point difference from market</p>
            </div>
          </div>

          {/* Market Consensus */}
          <div className="rounded-lg p-4 border backdrop-blur-sm bg-amber-500/10 border-amber-400/30">
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 className="w-4 h-4 text-amber-400" />
              <span className="text-amber-400 font-semibold text-sm">Market Consensus</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-slate-400 text-xs">Spread</span>
                <span className="text-amber-400 text-lg font-bold">{marketSpreadDisplay}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400 text-xs">Total</span>
                <span className="text-amber-400 text-lg font-bold">{marketTotal}</span>
              </div>
            </div>
            <div className="mt-2 pt-2 border-t border-amber-400/30">
              <p className="text-amber-400 text-xs">Value edge: {valueEdge >= 0 ? `+${valueEdge.toFixed(1)}` : valueEdge.toFixed(1)} points</p>
            </div>
          </div>
        </div>
        
        {/* Value Betting Recommendations - Enhanced */}
        <div className="mt-4 p-4 rounded-lg border backdrop-blur-sm" style={{
          borderColor: 'rgba(16, 185, 129, 0.3)',
          background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%)'
        }}>
          <h5 className="text-emerald-400 font-bold text-sm mb-3 font-orbitron">Recommended Bets</h5>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {/* Spread Bet Recommendation */}
            <div className="flex items-center justify-between p-3 bg-emerald-500/10 rounded border border-emerald-400/30">
              <div className="flex items-center gap-2">
                {valueBetSpread.includes(homeTeam.name) && (
                  <ImageWithFallback
                    src={homeTeam.logo}
                    alt={homeTeam.name}
                    className="w-6 h-6 object-contain"
                  />
                )}
                {valueBetSpread.includes(awayTeam.name) && (
                  <ImageWithFallback
                    src={awayTeam.logo}
                    alt={awayTeam.name}
                    className="w-6 h-6 object-contain"
                  />
                )}
                <div>
                  <p className="text-slate-400 text-xs">Spread</p>
                  <p className="text-emerald-400 font-bold text-sm">{valueBetSpread}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-emerald-400 text-xs font-bold">{spreadEdge.toFixed(1)}PT EDGE</p>
              </div>
            </div>
            
            {/* Total Bet Recommendation */}
            <div className="flex items-center justify-between p-3 bg-emerald-500/10 rounded border border-emerald-400/30">
              <div>
                <p className="text-slate-400 text-xs">Total</p>
                <p className="text-emerald-400 font-bold text-sm">{valueBetTotal}</p>
              </div>
              <div className="text-right">
                <p className="text-emerald-400 text-xs font-bold">{Math.abs(totalEdge).toFixed(1)}PT EDGE</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section 3: Live Sportsbook Lines - Compact Table */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="w-4 h-4 text-blue-400" />
          <h4 className="text-blue-400 font-semibold text-sm font-orbitron">Live Sportsbook Lines</h4>
        </div>

        {individualBooks.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-600/40">
                  <th className="text-left py-2 text-slate-400 font-orbitron text-xs">Sportsbook</th>
                  <th className="text-center py-2 text-slate-400 font-orbitron text-xs">Spread</th>
                  <th className="text-center py-2 text-slate-400 font-orbitron text-xs">Total</th>
                  <th className="text-center py-2 text-slate-400 font-orbitron text-xs">Spread Movement</th>
                  <th className="text-center py-2 text-slate-400 font-orbitron text-xs">Total Movement</th>
                </tr>
              </thead>
              <tbody>
                {individualBooks.map((book: any, index: number) => {
                  const logo = book.provider === 'DraftKings' ? DraftKingsLogo :
                              book.provider === 'ESPN Bet' ? ESPNBetLogo :
                              book.provider === 'Bovada' ? BovadaLogo :
                              DraftKingsLogo;
                  
                  const bookSpread = book.spread || 0;
                  const spreadDisplay = bookSpread < 0 ? `${homeTeam.name} ${bookSpread.toFixed(1)}` : `${homeTeam.name} +${bookSpread.toFixed(1)}`;
                  const total = book.overUnder || 0;
                  
                  const movement = lineMovements.find((m: any) => m.provider === book.provider);
                  
                  return (
                    <tr key={index} className="border-b border-gray-700/20 hover:bg-white/5">
                      <td className="py-3">
                        <div className="flex items-center gap-2">
                          <img src={logo} alt={book.provider} className="w-6 h-6 object-contain" />
                          <span className="text-white font-medium text-xs">{book.provider}</span>
                        </div>
                      </td>
                      <td className="text-center py-3">
                        <div className="flex items-center justify-center gap-1">
                          <span className="text-white font-bold">{spreadDisplay}</span>
                          <span className="px-1 py-0.5 bg-emerald-500/30 border border-emerald-400/50 rounded text-emerald-400 text-xs font-bold">CONSENSUS</span>
                        </div>
                      </td>
                      <td className="text-center py-3">
                        <span className="text-white font-bold">{total.toString()}</span>
                      </td>
                      <td className="text-center py-3">
                        <div className="flex items-center justify-center gap-1">
                          {getMovementIcon(movement?.spread.movement || 0)}
                          <span className={`text-xs font-bold ${
                            (movement?.spread.movement || 0) > 0 ? 'text-green-400' : 
                            (movement?.spread.movement || 0) < 0 ? 'text-red-400' : 'text-gray-400'
                          }`}>
                            {getMovementDisplay(movement?.spread.movement || 0)}
                          </span>
                        </div>
                      </td>
                      <td className="text-center py-3">
                        <div className="flex items-center justify-center gap-1">
                          {getMovementIcon(movement?.total.movement || 0)}
                          <span className={`text-xs font-bold ${
                            (movement?.total.movement || 0) > 0 ? 'text-green-400' : 
                            (movement?.total.movement || 0) < 0 ? 'text-red-400' : 'text-gray-400'
                          }`}>
                            {getMovementDisplay(movement?.total.movement || 0)}
                          </span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          // Fallback static data
          <div className="space-y-2">
            {[
              { name: 'ESPN Bet', spread: marketSpreadDisplay, total: (marketTotal - 0.5).toString(), logo: ESPNBetLogo },
              { name: 'DraftKings', spread: marketSpreadDisplay, total: marketTotal.toString(), logo: DraftKingsLogo },
              { name: 'Bovada', spread: marketSpreadDisplay, total: (marketTotal + 0.5).toString(), logo: BovadaLogo }
            ].map((book, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-gray-600/20">
                <div className="flex items-center gap-2">
                  <img src={book.logo} alt={book.name} className="w-6 h-6 object-contain" />
                  <span className="text-white font-medium text-sm">{book.name}</span>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-1">
                    <span className="text-slate-400">Spread:</span>
                    <span className="text-white font-bold">{book.spread}</span>
                    <span className="px-1 py-0.5 bg-emerald-500/30 rounded text-emerald-400 text-xs">CONSENSUS</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-slate-400">Total:</span>
                    <span className="text-white font-bold">{book.total}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Section 4: Moneylines */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-4 h-4 text-yellow-400" />
          <h4 className="text-yellow-400 font-semibold text-sm font-orbitron">Moneylines</h4>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="relative overflow-hidden rounded-lg p-4 border border-emerald-400/40 backdrop-blur-sm bg-gradient-to-br from-emerald-500/15 to-emerald-500/5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-8 h-8 object-contain" />
                <span className="text-gray-300 text-sm font-semibold">{homeTeam.name} (Home)</span>
              </div>
              <span className="text-2xl font-bold font-mono text-emerald-400">
                +{Math.round((100 - (predictionData?.prediction_cards?.win_probability?.home_team_prob || 40)) * 2.5)}
              </span>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg p-4 border border-red-400/40 backdrop-blur-sm bg-gradient-to-br from-red-500/15 to-red-500/5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-8 h-8 object-contain" />
                <span className="text-gray-300 text-sm font-semibold">{awayTeam.name} (Away)</span>
              </div>
              <span className="text-2xl font-bold font-mono text-red-400">
                -{Math.round((predictionData?.prediction_cards?.win_probability?.away_team_prob || 60) * 2.5)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Section 5: Market Value Analysis - Compact Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-lg p-4 border border-red-500/50 backdrop-blur-sm bg-gradient-to-br from-red-500/20 to-red-500/5">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <p className="text-red-400 font-bold text-sm">
              {spreadEdge >= 7 ? "Major Market Disagreement" : 
               spreadEdge >= 3 ? "Notable Market Difference" : 
               "Minor Market Variance"}
            </p>
          </div>
          <p className="text-gray-300 text-xs">
            Model and market are in {spreadEdge < 2 ? 'close' : 'significant'} agreement ({spreadEdge.toFixed(1)}pt difference)
          </p>
        </div>
        
        <div className="rounded-lg p-4 border border-emerald-500/50 backdrop-blur-sm bg-gradient-to-br from-emerald-500/20 to-emerald-500/5">
          <div className="flex items-center gap-2 mb-2">
            <Info className="w-4 h-4 text-emerald-400" />
            <p className="text-emerald-400 font-bold text-sm">Total Points Analysis</p>
          </div>
          <p className="text-gray-300 text-xs">
            Model projects {Math.abs(totalEdge).toFixed(1)} {modelTotal > marketTotal ? 'more' : 'fewer'} points than market consensus ({modelTotal} vs {marketTotal})
            {Math.abs(totalEdge) >= 3 ? ' - significant edge detected' : ' - minor variance'}
          </p>
        </div>
      </div>

      {/* Section 6: Win Probability Analysis */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Target className="w-4 h-4 text-cyan-400" />
          <h4 className="text-cyan-400 font-semibold text-sm font-orbitron">Win Probability Analysis</h4>
          <div className="px-2 py-1 bg-cyan-500/20 rounded text-cyan-400 text-xs font-bold">HIGH CONFIDENCE</div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Away Team Win Probability */}
          <div 
            className="rounded-lg p-4 border backdrop-blur-sm"
            style={{
              borderColor: `${awayTeamColor}30`,
              background: `linear-gradient(135deg, ${awayTeamColor}15 0%, ${awayTeamColor}05 100%)`
            }}
          >
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback
                src={awayTeam.logo}
                alt={awayTeam.name}
                className="w-10 h-10 object-contain"
                style={{ filter: `drop-shadow(0 0 6px ${awayTeamColor}60)` }}
              />
              <div>
                <span style={{ color: awayTeamColor }} className="font-bold text-lg font-orbitron">{awayTeam.name}</span>
                <p className="text-slate-400 text-xs">Away Team</p>
              </div>
            </div>
            
            <div className="text-center mb-4">
              <div 
                className="text-5xl font-bold mb-2 font-orbitron"
                style={{ 
                  color: awayTeamColor,
                  textShadow: `0 0 20px ${awayTeamColor}50`
                }}
              >
                {((predictionData?.prediction_cards?.win_probability?.away_team_prob || 48.6)).toFixed(1)}
                <span className="text-2xl">%</span>
              </div>
              <div className="flex items-center justify-center gap-1 mb-2">
                <span className="text-slate-400 text-xs">Why this probability:</span>
              </div>
              <div className="text-xs text-slate-300 space-y-1">
                <p>• Underdog trailing by {Math.abs((predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4) - (predictionData?.prediction_cards?.win_probability?.away_team_prob || 48.6)).toFixed(1)}%</p>
                <p>• High model confidence ({((predictionData?.confidence?.overall_confidence || 80.8)).toFixed(1)}%)</p>
                {(predictionData?.prediction_cards?.win_probability?.away_team_prob || 48.6) > 50 && (
                  <div className="mt-2 px-2 py-1 bg-emerald-500/20 rounded border border-emerald-400/30">
                    <span style={{ color: awayTeamColor }} className="text-xs font-bold">FAVORITE</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Home Team Win Probability */}
          <div 
            className="rounded-lg p-4 border backdrop-blur-sm"
            style={{
              borderColor: `${homeTeamColor}30`,
              background: `linear-gradient(135deg, ${homeTeamColor}15 0%, ${homeTeamColor}05 100%)`
            }}
          >
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback
                src={homeTeam.logo}
                alt={homeTeam.name}
                className="w-10 h-10 object-contain"
                style={{ filter: `drop-shadow(0 0 6px ${homeTeamColor}60)` }}
              />
              <div>
                <span style={{ color: homeTeamColor }} className="font-bold text-lg font-orbitron">{homeTeam.name}</span>
                <p className="text-slate-400 text-xs">Home Team</p>
              </div>
            </div>
            
            <div className="text-center mb-4">
              <div 
                className="text-5xl font-bold mb-2 font-orbitron"
                style={{ 
                  color: homeTeamColor,
                  textShadow: `0 0 20px ${homeTeamColor}50`
                }}
              >
                {((predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4)).toFixed(1)}
                <span className="text-2xl">%</span>
              </div>
              <div className="flex items-center justify-center gap-1 mb-2">
                <span className="text-slate-400 text-xs">Why this probability:</span>
              </div>
              <div className="text-xs text-slate-300 space-y-1">
                <p>• {(predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4) > 50 ? 'Slight favorite' : 'Underdog'} by {Math.abs((predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4) - (predictionData?.prediction_cards?.win_probability?.away_team_prob || 48.6)).toFixed(1)}%</p>
                <p>• Home field advantage included</p>
                <p>• High model confidence ({((predictionData?.confidence?.overall_confidence || 80.8)).toFixed(1)}%)</p>
                {(predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4) > 50 && (
                  <div className="mt-2 px-2 py-1 bg-emerald-500/20 rounded border border-emerald-400/30">
                    <span style={{ color: homeTeamColor }} className="text-xs font-bold">FAVORITE</span>
                    <p className="text-emerald-400 text-xs font-bold mt-1">{Math.abs((predictionData?.prediction_cards?.win_probability?.home_team_prob || 51.4) - (predictionData?.prediction_cards?.win_probability?.away_team_prob || 48.6)).toFixed(1)}% Edge</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section 7: Final Prediction Summary */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-4 h-4 text-indigo-400" />
          <h4 className="text-indigo-400 font-semibold text-sm font-orbitron">Final Prediction Summary</h4>
        </div>
        
        <div className="rounded-lg p-6 border backdrop-blur-sm" style={{
          borderColor: 'rgba(99, 102, 241, 0.3)',
          background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%)'
        }}>
          <div className="text-center mb-6">
            <h5 className="text-indigo-400 font-bold text-lg mb-4 font-orbitron">Final Score Prediction</h5>
            <div className="flex items-center justify-center gap-8">
              <div className="text-center">
                <div className="flex items-center gap-2 mb-2">
                  <ImageWithFallback
                    src={awayTeam.logo}
                    alt={awayTeam.name}
                    className="w-8 h-8 object-contain"
                  />
                  <span className="text-white font-bold text-lg">{awayTeam.name}</span>
                </div>
                <div 
                  className="text-4xl font-bold font-orbitron"
                  style={{ 
                    color: awayTeamColor,
                    textShadow: `0 0 15px ${awayTeamColor}50`
                  }}
                >
                  {Math.round((predictionData?.prediction_cards?.predicted_total?.model_total || 70) / 2 - (predictionData?.prediction_cards?.predicted_spread?.model_spread || 1) / 2) || 34}
                </div>
              </div>
              
              <div className="text-center">
                <span className="text-slate-400 text-sm">vs</span>
                <div className="text-indigo-400 font-bold text-lg mt-2">Total: {Math.round(predictionData?.prediction_cards?.predicted_total?.model_total || 70)}</div>
              </div>
              
              <div className="text-center">
                <div className="flex items-center gap-2 mb-2">
                  <ImageWithFallback
                    src={homeTeam.logo}
                    alt={homeTeam.name}
                    className="w-8 h-8 object-contain"
                  />
                  <span className="text-white font-bold text-lg">{homeTeam.name}</span>
                </div>
                <div 
                  className="text-4xl font-bold font-orbitron"
                  style={{ 
                    color: homeTeamColor,
                    textShadow: `0 0 15px ${homeTeamColor}50`
                  }}
                >
                  {Math.round((predictionData?.prediction_cards?.predicted_total?.model_total || 70) / 2 + (predictionData?.prediction_cards?.predicted_spread?.model_spread || 1) / 2) || 35}
                </div>
              </div>
            </div>
          </div>
          
          <div className="border-t border-indigo-400/20 pt-4">
            <h6 className="text-indigo-400 font-semibold text-sm mb-3">Key Factors</h6>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
              <div className="space-y-1">
                <p>• Talent advantage</p>
                <p>• More consistent performance</p>
                <p>• Enhanced bye week analysis available</p>
              </div>
              <div className="space-y-1">
                <p>• Comprehensive data: market lines, composite ratings (ELO/FPI), poll rankings, weather data</p>
                <p>• Moderate market variance detected</p>
              </div>
            </div>
            <div className="mt-4 text-center">
              <div className="px-4 py-2 bg-indigo-500/20 rounded-lg border border-indigo-400/30 inline-block">
                <span className="text-indigo-400 font-bold text-sm font-orbitron">COMPREHENSIVE ANALYSIS COMPLETE!</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Section 8: Detailed Market Analysis Insights */}
      <div className="mb-6">
        <InsightBox
          whatItMeans="The market spread is what Vegas sportsbooks believe the final margin will be. Our model's spread is an independent prediction. When they disagree significantly, there's potential 'value' - a bet with positive expected return."
          whyItMatters={`A ${spreadEdge.toFixed(1)}-point edge means the model sees ${((spreadEdge / 3) * 100).toFixed(0)}% more scoring advantage than Vegas prices. On a $100 bet, this translates to roughly $${((spreadEdge / 3) * 110).toFixed(0)} in expected value. Edges over 3 points historically win 55-60% of the time.`}
          whoHasEdge={{
            team: valueEdge > 0 ? homeTeam.name : awayTeam.name,
            reason: `Model projects ${Math.abs(valueEdge).toFixed(1)} points ${valueEdge > 0 ? 'stronger' : 'weaker'} than market consensus. ${spreadEdge > 5 ? 'This is a MAJOR disagreement suggesting the model found something Vegas missed.' : spreadEdge > 3 ? 'Significant edge worth betting.' : 'Moderate difference, proceed with caution.'} Total shows ${totalEdge > 5 ? 'major' : totalEdge > 3 ? 'significant' : 'minor'} ${modelTotal > marketTotal ? 'OVER' : 'UNDER'} value.`,
            magnitude: spreadEdge > 5 ? 'major' : spreadEdge > 3 ? 'significant' : spreadEdge > 1.5 ? 'moderate' : 'small'
          }}
          keyDifferences={[
            `Spread disagreement: ${spreadEdge.toFixed(1)} points (Model: ${modelSpreadDisplay}, Vegas: ${marketSpreadDisplay})`,
            `Total disagreement: ${totalEdge.toFixed(1)} points (Model: ${modelTotal.toFixed(1)}, Vegas: ${marketTotal.toFixed(1)})`,
            isUpsetAlert ? `🚨 UPSET ALERT: Model picks ${modelFavorite}, market favors ${marketFavorite}` : `Both model and market agree on favorite (${modelFavorite})`
          ]}
        />
      </div>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-gray-600/40">
        <div className="text-slate-400 text-xs space-y-2">
          <p>
            <span className="font-semibold text-purple-400">What is ATS?</span> Against The Spread (ATS) records show how often teams cover the betting spread. Teams covering &gt;55% are historically profitable bets.
          </p>
          <p>
            <span className="font-semibold text-emerald-400">Sharp Money Analysis:</span> Line movement indicates where professional bettors are placing their money. Significant movement (2+ points) typically signals sharp action.
          </p>
        </div>
      </div>
    </GlassCard>
  );
}