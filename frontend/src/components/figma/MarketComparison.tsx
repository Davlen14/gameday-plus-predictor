import { GlassCard } from './GlassCard';
import { TrendingUp, AlertTriangle, Info, BarChart3 } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

// Sportsbook SVGs from public folder (Vite will serve these correctly)
const BovadaLogo = '/Bovada-Casino-Logo.svg';
const ESPNBetLogo = '/espnbet.svg';
const DraftKingsLogo = '/Draftking.svg';

interface MarketComparisonProps {
  predictionData?: any;
}

export function MarketComparison({ predictionData }: MarketComparisonProps) {
  // Live API data integration
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png" };
  
  // Extract team colors (use primary_color like ComprehensiveRatingsComparison does)
  const awayTeamColor = awayTeam.primary_color || awayTeam.color || '#3b82f6';
  const homeTeamColor = homeTeam.primary_color || homeTeam.color || '#f97316';
  
  // Use corrected betting analysis data if available
  const bettingAnalysis = predictionData?.detailed_analysis?.betting_analysis;
  
  // Market comparison data - use real betting analysis when available
  const modelSpread = predictionData?.prediction_cards?.predicted_spread?.model_spread || 0;
  
  // Format model spread with correct team name (negative = away team favored in model)
  let modelSpreadDisplay = predictionData?.prediction_cards?.predicted_spread?.model_spread_display;
  if (!modelSpreadDisplay && modelSpread !== null) {
    if (modelSpread < 0) {
      // Negative means away team is favored
      modelSpreadDisplay = `${awayTeam.name} ${modelSpread.toFixed(1)}`;
    } else if (modelSpread > 0) {
      // Positive means home team is favored
      modelSpreadDisplay = `${homeTeam.name} -${modelSpread.toFixed(1)}`;
    } else {
      modelSpreadDisplay = 'EVEN';
    }
  }
  
  // Use real market data from betting analysis if available
  const marketSpread = bettingAnalysis?.market_spread || predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5;
  const marketSpreadDisplay = bettingAnalysis?.formatted_spread || `${homeTeam.name} ${marketSpread >= 0 ? '+' : ''}${marketSpread.toFixed(1)}`;
  const valueEdge = bettingAnalysis?.spread_edge || predictionData?.prediction_cards?.predicted_spread?.value_edge || 0;
  const spreadEdge = Math.abs(valueEdge);
  
  const modelTotal = predictionData?.prediction_cards?.predicted_total?.model_total || 52.5;
  const marketTotal = bettingAnalysis?.market_total || predictionData?.prediction_cards?.predicted_total?.market_total || 45.0;
  const totalEdge = bettingAnalysis?.total_edge || predictionData?.prediction_cards?.predicted_total?.edge || 8.0;
  
  // Determine who is the favorite and format spreads correctly
  const determineFavoriteAndSpread = (rawSpread: number, homeTeamName: string, awayTeamName: string) => {
    if (rawSpread < 0) {
      // Home team is favorite
      return {
        favoriteTeam: homeTeamName,
        underdogTeam: awayTeamName,
        favoriteSpread: rawSpread, // Keep negative
        underdogSpread: -rawSpread // Make positive
      };
    } else {
      // Away team is favorite  
      return {
        favoriteTeam: awayTeamName,
        underdogTeam: homeTeamName,
        favoriteSpread: -rawSpread, // Make negative
        underdogSpread: rawSpread // Keep positive
      };
    }
  };
  
  // Use real betting analysis spread format, or generate sportsbook variations
  const baseSpreadDisplay = marketSpreadDisplay;
  
  // All sportsbooks use the same spread display (with team name)
  const bovadaSpreadDisplay = baseSpreadDisplay;
  const draftKingsSpreadDisplay = baseSpreadDisplay; 
  const espnBetSpreadDisplay = baseSpreadDisplay;
  
  // Use real betting analysis recommendations if available
  const valueBetSpread = bettingAnalysis?.spread_recommendation || 
    (valueEdge >= 2 ? `${homeTeam.name} ${marketSpread >= 0 ? '+' : ''}${marketSpread.toFixed(1)}` :
     valueEdge <= -2 ? `${awayTeam.name} ${(-marketSpread) >= 0 ? '+' : ''}${(-marketSpread).toFixed(1)}` :
     "No significant edge");
  
  const valueBetTotal = bettingAnalysis?.total_recommendation ||
    (modelTotal > marketTotal + 3 ? `OVER ${marketTotal}` :
     modelTotal < marketTotal - 3 ? `UNDER ${marketTotal}` :
     "No significant edge");

  
  // Market display for favorite perspective (corrected) - only if no betting analysis
  const marketDisplay = determineFavoriteAndSpread(marketSpread, homeTeam.name, awayTeam.name);
  const fallbackMarketDisplay = `${marketDisplay.favoriteTeam} ${marketDisplay.favoriteSpread.toFixed(1)}`;
  
  // Sportsbook totals
  const bovadaTotal = marketTotal - 0.5;
  const draftKingsTotal = marketTotal;
  const espnBetTotal = marketTotal + 1.0;
  
  // Check for upset alert from API
  const isUpsetAlert = bettingAnalysis?.is_upset_alert || false;
  const modelFavorite = bettingAnalysis?.model_favorite || homeTeam.name;
  const marketFavorite = bettingAnalysis?.market_favorite || homeTeam.name;
  
  // Determine which team to theme the upset alert by (the team the model predicts will win)
  const upsetTeam = modelFavorite === homeTeam.name ? homeTeam : awayTeam;
  const upsetTeamColor = modelFavorite === homeTeam.name ? homeTeamColor : awayTeamColor;
  
  // Primary team color for Model Projection and Market sections
  // Use the team that the MODEL favors (based on spread)
  const modelFavoredTeam = modelSpread < 0 ? awayTeam : homeTeam;
  const primaryTeamColor = modelSpread < 0 ? awayTeamColor : homeTeamColor;  return (
    <GlassCard className="p-6">
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
      
      <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-emerald-400" />
          Market Comparison
        </h3>
        <div className="flex items-center gap-2 px-3 py-1 bg-red-500/30 rounded-full border border-red-400/50 backdrop-blur-sm">
          <AlertTriangle className="w-4 h-4 text-red-400" />
          <span className="text-red-400 font-bold text-xs">{spreadEdge.toFixed(1)} POINT DISCREPANCY</span>
        </div>
      </div>

      {/* Model vs Market Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div 
          className="relative overflow-hidden rounded-lg p-5 border backdrop-blur-sm"
          style={{
            borderColor: `${primaryTeamColor}50`,
            background: `linear-gradient(135deg, ${primaryTeamColor}25 0%, ${primaryTeamColor}10 50%, ${primaryTeamColor}05 100%)`,
            boxShadow: `0 0 20px ${primaryTeamColor}15`
          }}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 
                className="w-5 h-5" 
                style={{ 
                  color: primaryTeamColor,
                  filter: `drop-shadow(0 0 4px ${primaryTeamColor}60)`
                }}
              />
              <span 
                className="font-semibold text-sm font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 10px ${primaryTeamColor}40`
                }}
              >
                Model Projection
              </span>
            </div>
          </div>
            <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-gray-400 text-xs mb-1 font-orbitron">Spread</p>
              <p 
                className="text-3xl font-bold font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 12px ${primaryTeamColor}50`
                }}
              >
                {modelSpreadDisplay}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-xs mb-1 font-orbitron">Total</p>
              <p 
                className="text-3xl font-bold font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 12px ${primaryTeamColor}50`
                }}
              >
                {modelTotal}
              </p>
            </div>
          </div>
          <div 
            className="mt-3 pt-3 border-t"
            style={{ borderColor: `${primaryTeamColor}30` }}
          >
            <p 
              className="text-xs font-semibold font-orbitron"
              style={{ 
                color: primaryTeamColor,
                textShadow: `0 0 8px ${primaryTeamColor}40`
              }}
            >
              Model projection: {spreadEdge.toFixed(1)} point difference from market
            </p>
          </div>
        </div>

        <div 
          className="relative overflow-hidden rounded-lg p-5 border backdrop-blur-sm"
          style={{
            borderColor: `${primaryTeamColor}50`,
            background: `linear-gradient(135deg, ${primaryTeamColor}25 0%, ${primaryTeamColor}10 50%, ${primaryTeamColor}05 100%)`,
            boxShadow: `0 0 20px ${primaryTeamColor}15`
          }}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 
                className="w-5 h-5"
                style={{ 
                  color: primaryTeamColor,
                  filter: `drop-shadow(0 0 4px ${primaryTeamColor}60)`
                }}
              />
              <span 
                className="font-semibold text-sm font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 10px ${primaryTeamColor}40`
                }}
              >
                Market Consensus
              </span>
            </div>
          </div>
            <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-gray-400 text-xs mb-1 font-orbitron">Spread</p>
              <p 
                className="text-3xl font-bold font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 12px ${primaryTeamColor}50`
                }}
              >
                {marketSpreadDisplay}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-xs mb-1 font-orbitron">Total</p>
              <p 
                className="text-3xl font-bold font-orbitron"
                style={{ 
                  color: primaryTeamColor,
                  textShadow: `0 0 12px ${primaryTeamColor}50`
                }}
              >
                {marketTotal}
              </p>
            </div>
          </div>
          <div 
            className="mt-3 pt-3 border-t"
            style={{ borderColor: `${primaryTeamColor}30` }}
          >
            <p 
              className="text-xs font-semibold font-orbitron"
              style={{ 
                color: primaryTeamColor,
                textShadow: `0 0 8px ${primaryTeamColor}40`
              }}
            >
              Value edge: {valueEdge >= 0 ? `+${valueEdge.toFixed(1)}` : valueEdge.toFixed(1)} points
            </p>
          </div>
        </div>
      </div>

      {/* Sportsbook Lines */}
      <div className="mb-4">
        <h4 
          className="font-semibold text-sm mb-3 flex items-center gap-2 font-orbitron"
          style={{ 
            color: primaryTeamColor,
            textShadow: `0 0 8px ${primaryTeamColor}40`
          }}
        >
          <Info 
            className="w-4 h-4"
            style={{ 
              color: primaryTeamColor,
              filter: `drop-shadow(0 0 4px ${primaryTeamColor}60)`
            }}
          />
          Live Sportsbook Lines
        </h4>
        <div className="space-y-3">
          <SportsbookLine 
            name="Bovada" 
            logo={BovadaLogo}
            spread={bovadaSpreadDisplay}
            total={bovadaTotal.toString()} 
            spreadBadge="CONSENSUS"
            spreadBadgeColor="emerald"
            totalDiff={`${(bovadaTotal - modelTotal).toFixed(1)}`}
          />
          <SportsbookLine 
            name="ESPN Bet" 
            logo={ESPNBetLogo}
            spread={espnBetSpreadDisplay}
            total={espnBetTotal.toString()} 
            spreadBadge="+1.0"
            spreadBadgeColor="amber"
            totalDiff={`${(espnBetTotal - modelTotal).toFixed(1)}`}
          />
          <SportsbookLine 
            name="DraftKings" 
            logo={DraftKingsLogo}
            spread={draftKingsSpreadDisplay}
            total={draftKingsTotal.toString()} 
            spreadBadge="CONSENSUS"
            spreadBadgeColor="emerald"
            totalDiff={`${(draftKingsTotal - modelTotal).toFixed(1)}`}
          />
        </div>

        {/* Model's Line - Featured - Team Themed & Transparent */}
        <div 
          className="relative overflow-hidden rounded-xl p-6 border-2 backdrop-blur-sm mt-4 transition-all duration-500"
          style={{
            background: `linear-gradient(135deg, ${valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}15` : valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}15` : 'rgba(16, 185, 129, 0.15)'} 0%, rgba(15, 23, 42, 0.3) 100%)`,
            borderColor: valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}40` : valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}40` : 'rgba(16, 185, 129, 0.4)',
            boxShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 30px ${homeTeam.color || '#f97316'}15, inset 0 0 60px ${homeTeam.color || '#f97316'}08` : valueBetSpread.includes(awayTeam.name) ? `0 0 30px ${awayTeam.color || '#3b82f6'}15, inset 0 0 60px ${awayTeam.color || '#3b82f6'}08` : '0 0 30px rgba(16, 185, 129, 0.15), inset 0 0 60px rgba(16, 185, 129, 0.08)'
          }}
        >
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <div 
                    className="flex items-center justify-center w-10 h-10 rounded-lg border transition-all duration-300"
                    style={{
                      backgroundColor: `${homeTeam.color || '#f97316'}20`,
                      borderColor: `${homeTeam.color || '#f97316'}40`,
                      boxShadow: `0 0 12px ${homeTeam.color || '#f97316'}25`
                    }}
                  >
                    <ImageWithFallback
                      src={homeTeam.logo}
                      alt={homeTeam.name}
                      className="w-8 h-8 object-contain"
                      style={{ filter: `drop-shadow(0 0 6px ${homeTeam.color || '#f97316'}60)` }}
                    />
                  </div>
                  <span className="text-xs text-slate-400">vs</span>
                  <div 
                    className="flex items-center justify-center w-10 h-10 rounded-lg border transition-all duration-300"
                    style={{
                      backgroundColor: `${awayTeam.color || '#3b82f6'}20`,
                      borderColor: `${awayTeam.color || '#3b82f6'}40`,
                      boxShadow: `0 0 12px ${awayTeam.color || '#3b82f6'}25`
                    }}
                  >
                    <ImageWithFallback
                      src={awayTeam.logo}
                      alt={awayTeam.name}
                      className="w-8 h-8 object-contain"
                      style={{ filter: `drop-shadow(0 0 6px ${awayTeam.color || '#3b82f6'}60)` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="text-white text-sm font-semibold uppercase tracking-wide">Market Value Analysis</div>
                  <div className="text-slate-400 text-xs">
                    {bettingAnalysis?.spread_recommendation || 
                     (valueEdge >= 2 ? `Market undervalues ${homeTeam.name} by ${valueEdge.toFixed(1)} points` :
                      valueEdge <= -2 ? `Market overvalues ${homeTeam.name} by ${Math.abs(valueEdge).toFixed(1)} points` :
                      `No significant value edge detected`)}
                  </div>
                </div>
              </div>
              <div 
                className="px-3 py-1.5 border rounded-lg transition-all duration-300"
                style={{
                  backgroundColor: valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}25` : valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}25` : 'rgba(16, 185, 129, 0.25)',
                  borderColor: valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}50` : valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}50` : 'rgba(16, 185, 129, 0.5)',
                  boxShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 15px ${homeTeam.color || '#f97316'}30` : valueBetSpread.includes(awayTeam.name) ? `0 0 15px ${awayTeam.color || '#3b82f6'}30` : '0 0 15px rgba(16, 185, 129, 0.3)'
                }}
              >
                <span 
                  className="text-xs font-semibold"
                  style={{
                    color: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : '#10b981',
                    textShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 12px ${homeTeam.color || '#f97316'}60` : valueBetSpread.includes(awayTeam.name) ? `0 0 12px ${awayTeam.color || '#3b82f6'}60` : '0 0 12px rgba(16, 185, 129, 0.6)'
                  }}
                >
                  VALUE OPPORTUNITY
                </span>
              </div>
            </div>
            
            {/* Modern 3D Themed Recommendation Cards */}
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex gap-6">
                {/* Spread Bet Card - Team Themed */}
                <div 
                  className="relative overflow-hidden rounded-xl px-6 py-4 border-2 transition-all duration-500 min-w-[240px]"
                  style={{ 
                    backgroundColor: valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}15` : 
                                   valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}15` : 
                                   'rgba(42, 47, 56, 0.3)',
                    borderColor: valueBetSpread.includes(homeTeam.name) ? `${homeTeam.color || '#f97316'}40` : 
                               valueBetSpread.includes(awayTeam.name) ? `${awayTeam.color || '#3b82f6'}40` : 
                               'rgba(16, 185, 129, 0.4)',
                    boxShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 30px ${homeTeam.color || '#f97316'}20, inset 0 0 60px ${homeTeam.color || '#f97316'}10` : 
                             valueBetSpread.includes(awayTeam.name) ? `0 0 30px ${awayTeam.color || '#3b82f6'}20, inset 0 0 60px ${awayTeam.color || '#3b82f6'}10` : 
                             '0 0 30px rgba(16, 185, 129, 0.2), inset 0 0 60px rgba(16, 185, 129, 0.1)'
                  }}
                >
                  {/* 3D Team Logo Background */}
                  {(valueBetSpread.includes(homeTeam.name) || valueBetSpread.includes(awayTeam.name)) && (
                    <div className="absolute right-4 top-1/2 -translate-y-1/2 opacity-15 pointer-events-none">
                      <ImageWithFallback 
                        src={valueBetSpread.includes(homeTeam.name) ? homeTeam.logo : awayTeam.logo}
                        alt="Team Logo"
                        className="w-24 h-24 object-contain"
                        style={{ 
                          filter: 'drop-shadow(6px 6px 10px rgba(0,0,0,0.5)) drop-shadow(0px 0px 15px rgba(255,255,255,0.3))',
                          transform: 'perspective(150px) rotateY(-12deg) scale(1.15) rotate(8deg)'
                        }}
                      />
                    </div>
                  )}
                  
                  <div className="relative z-10 flex flex-col gap-3">
                    <span className="text-slate-400 text-xs font-semibold uppercase tracking-wide font-orbitron">Recommended Spread Bet</span>
                    <div className="flex items-center gap-2">
                      {valueBetSpread.includes(homeTeam.name) && (
                        <ImageWithFallback
                          src={homeTeam.logo}
                          alt={homeTeam.name}
                          className="w-7 h-7 object-contain"
                          style={{ filter: `drop-shadow(0 0 8px ${homeTeam.color || '#f97316'}80)` }}
                        />
                      )}
                      {valueBetSpread.includes(awayTeam.name) && (
                        <ImageWithFallback
                          src={awayTeam.logo}
                          alt={awayTeam.name}
                          className="w-7 h-7 object-contain"
                          style={{ filter: `drop-shadow(0 0 8px ${awayTeam.color || '#3b82f6'}80)` }}
                        />
                      )}
                      <span 
                        className="text-lg font-bold font-orbitron"
                        style={{ 
                          color: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : 
                                valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : 
                                '#10b981',
                          textShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 20px ${homeTeam.color || '#f97316'}60` : 
                                     valueBetSpread.includes(awayTeam.name) ? `0 0 20px ${awayTeam.color || '#3b82f6'}60` : 
                                     '0 0 20px rgba(16, 185, 129, 0.6)'
                        }}
                      >
                        {valueBetSpread}
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div 
                        className="w-2 h-2 rounded-full"
                        style={{ 
                          backgroundColor: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : 
                                          valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : 
                                          '#10b981',
                          boxShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 8px ${homeTeam.color || '#f97316'}80` : 
                                    valueBetSpread.includes(awayTeam.name) ? `0 0 8px ${awayTeam.color || '#3b82f6'}80` : 
                                    '0 0 8px rgba(16, 185, 129, 0.8)'
                        }}
                      />
                      <span 
                        className="text-xs font-semibold font-orbitron"
                        style={{ 
                          color: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : 
                                valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : 
                                '#10b981'
                        }}
                      >
                        {spreadEdge.toFixed(1)}PT EDGE
                      </span>
                    </div>
                  </div>
                </div>
                
                {/* Total Bet Card - Emerald Themed */}
                <div 
                  className="relative overflow-hidden rounded-xl px-6 py-4 border-2 transition-all duration-500 min-w-[240px]"
                  style={{ 
                    backgroundColor: 'rgba(16, 185, 129, 0.15)',
                    borderColor: 'rgba(16, 185, 129, 0.4)',
                    boxShadow: '0 0 30px rgba(16, 185, 129, 0.2), inset 0 0 60px rgba(16, 185, 129, 0.1)'
                  }}
                >
                  <div className="relative z-10 flex flex-col gap-3">
                    <span className="text-slate-400 text-xs font-semibold uppercase tracking-wide font-orbitron">Recommended Total Bet</span>
                    <span 
                      className="text-lg font-bold text-emerald-400 font-orbitron"
                      style={{ textShadow: '0 0 20px rgba(16, 185, 129, 0.6)' }}
                    >
                      {valueBetTotal}
                    </span>
                    <div className="flex items-center gap-1.5">
                      <div 
                        className="w-2 h-2 rounded-full bg-emerald-500"
                        style={{ boxShadow: '0 0 8px rgba(16, 185, 129, 0.8)' }}
                      />
                      <span className="text-emerald-400 text-xs font-semibold font-orbitron">{Math.abs(totalEdge).toFixed(1)}PT EDGE</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-end gap-1">
                <div className="flex items-center gap-1.5">
                  <div 
                    className="w-2 h-2 rounded-full animate-pulse" 
                    style={{ 
                      backgroundColor: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : '#10b981',
                      boxShadow: valueBetSpread.includes(homeTeam.name) ? `0 0 8px ${homeTeam.color || '#f97316'}80` : valueBetSpread.includes(awayTeam.name) ? `0 0 8px ${awayTeam.color || '#3b82f6'}80` : '0 0 8px rgba(16, 185, 129, 0.8)'
                    }}
                  />
                  <span 
                    className="text-xs font-medium"
                    style={{ 
                      color: valueBetSpread.includes(homeTeam.name) ? homeTeam.color || '#f97316' : valueBetSpread.includes(awayTeam.name) ? awayTeam.color || '#3b82f6' : '#10b981'
                    }}
                  >
                    LIVE
                  </span>
                </div>
                <span className="text-slate-500 text-xs">Updated: Now</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-600/40">
              <p className="text-gray-300 text-xs">
                <span className="font-semibold text-emerald-400">Analysis:</span> 
                Model: {modelSpreadDisplay} vs Market: {marketSpreadDisplay}. 
                Value edge: {valueEdge >= 0 ? `+${valueEdge.toFixed(1)}` : valueEdge.toFixed(1)} points. 
                Total model {modelTotal} vs market {marketTotal} ({totalEdge.toFixed(1)}pt edge). 
                {valueBetSpread !== "No significant edge" ? `Recommended: ${valueBetSpread}` : "No spread value"} 
                {valueBetTotal !== "No significant edge" ? ` and ${valueBetTotal}` : ""}.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Moneylines */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
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

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="relative overflow-hidden rounded-lg p-4 border border-red-500/50 backdrop-blur-sm bg-gradient-to-br from-red-500/20 to-red-500/5">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-red-400" />
            <p className="text-red-400 font-bold text-sm">
              {spreadEdge >= 7 ? "Significant Market Disagreement" : 
               spreadEdge >= 3 ? "Notable Market Difference" : 
               "Minor Market Variance"}
            </p>
          </div>
          <p className="text-gray-300 text-xs">
            {valueEdge >= 2 ? `Market gives ${homeTeam.name} better odds than model suggests (${valueEdge.toFixed(1)}pt value)` :
             valueEdge <= -2 ? `Market overvalues ${homeTeam.name} vs model projection (${Math.abs(valueEdge).toFixed(1)}pt difference)` :
             `Model and market are in relative agreement (${spreadEdge.toFixed(1)}pt difference)`}
          </p>
        </div>
        <div className="relative overflow-hidden rounded-lg p-4 border border-amber-500/50 backdrop-blur-sm bg-gradient-to-br from-amber-500/20 to-amber-500/5">
          <div className="flex items-center gap-2 mb-2">
            <Info className="w-5 h-5 text-amber-400" />
            <p className="text-amber-400 font-bold text-sm">Total Points Analysis</p>
          </div>
          <p className="text-gray-300 text-xs">
            Model projects {modelTotal > marketTotal ? `${(modelTotal - marketTotal).toFixed(1)} more` : `${(marketTotal - modelTotal).toFixed(1)} fewer`} points than market consensus 
            ({modelTotal} vs {marketTotal})
            {Math.abs(modelTotal - marketTotal) >= 3 ? ` - significant edge detected` : ` - minor variance`}
          </p>
        </div>
      </div>
    </GlassCard>
  );
}

function SportsbookLine({ 
  name, 
  logo,
  spread, 
  total, 
  spreadBadge, 
  spreadBadgeColor, 
  totalDiff 
}: { 
  name: string; 
  logo: string;
  spread: string; 
  total: string; 
  spreadBadge: string; 
  spreadBadgeColor: 'emerald' | 'amber'; 
  totalDiff: string;
}) {
  const badgeColors = {
    emerald: 'bg-emerald-500/30 border-emerald-400/50 text-emerald-400',
    amber: 'bg-amber-500/30 border-amber-400/50 text-amber-400'
  };

  return (
    <div className="relative overflow-hidden rounded-lg p-4 border border-gray-400/15 backdrop-blur-sm hover:border-emerald-400/40 transition-all duration-300 bg-[rgba(26,31,38,0.5)]">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3 flex-1">
          <div className="flex items-center gap-2">
            <img src={logo} alt={name} className="w-8 h-8 object-contain" />
            <div className="text-gray-300 font-semibold font-orbitron">{name}</div>
          </div>
          <div className="h-8 w-px bg-gray-600"></div>
          <div className="flex gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <span className="text-gray-400 text-xs font-orbitron">Spread</span>
              <span className="text-lg font-bold font-orbitron text-white">{spread}</span>
              <span className={`px-2 py-0.5 border rounded text-xs font-bold font-orbitron ${badgeColors[spreadBadgeColor]}`}>
                {spreadBadge}
              </span>
            </div>
            <div className="h-6 w-px bg-gray-600 hidden sm:block"></div>
            <div className="flex items-center gap-2">
              <span className="text-gray-400 text-xs font-orbitron">Total</span>
              <span className="text-lg font-bold font-orbitron text-white">{total}</span>
              <span className="px-2 py-0.5 bg-red-500/30 border border-red-400/50 rounded text-red-400 text-xs font-bold font-orbitron">{totalDiff}
              </span>
            </div>
          </div>
        </div>
        <svg className="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
        </svg>
      </div>
    </div>
  );
}
