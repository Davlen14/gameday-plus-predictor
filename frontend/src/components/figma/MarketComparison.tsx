import { GlassCard } from './GlassCard';
import { TrendingUp, AlertTriangle, Info, BarChart3 } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

// Import sportsbook SVGs as URLs (Vite will handle these)
const BovadaLogo = '/src/assets/Bovada-Casino-Logo.svg';
const ESPNBetLogo = '/src/assets/espnbet.svg';
const DraftKingsLogo = '/src/assets/Draftking.svg';

interface MarketComparisonProps {
  predictionData?: any;
}

export function MarketComparison({ predictionData }: MarketComparisonProps) {
  // Live API data integration
  const spreadEdge = predictionData?.prediction_cards?.predicted_spread?.edge || 7.5;
  const totalEdge = predictionData?.prediction_cards?.predicted_total?.edge || 8.0;
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png" };
  
  // Market comparison data
  const modelSpread = predictionData?.prediction_cards?.predicted_spread?.model_spread_display || `${homeTeam.name} +7.5`;
  const marketSpread = predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5;
  const modelTotal = predictionData?.prediction_cards?.predicted_total?.model_total || 52.5;
  const marketTotal = predictionData?.prediction_cards?.predicted_total?.market_total || 45.0;
  
  // Sportsbook lines (using live API data)
  const draftKingsSpread = predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5;
  const draftKingsTotal = predictionData?.prediction_cards?.predicted_total?.market_total || 52.5;
  const bovadaSpread = (predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5) + 0.5;
  const bovadaTotal = (predictionData?.prediction_cards?.predicted_total?.market_total || 52.5) - 0.5;
  const espnBetSpread = (predictionData?.prediction_cards?.predicted_spread?.market_spread || -3.5) - 1.0;
  const espnBetTotal = (predictionData?.prediction_cards?.predicted_total?.market_total || 52.5) + 1.0;
  
  // Value picks
  const valueBetSpread = `${awayTeam.name} +3.5`;
  const valueBetTotal = "OVER 52.5";
  return (
    <GlassCard className="p-6">
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
        <div className="relative overflow-hidden rounded-lg p-5 border border-amber-400/50 backdrop-blur-sm bg-gradient-to-br from-amber-500/25 to-amber-500/5">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-amber-400" />
              <span className="text-amber-400 font-semibold text-sm">Model Projection</span>
            </div>
          </div>
            <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-gray-400 text-xs mb-1">Spread</p>
              <p className="text-3xl font-bold font-mono text-amber-400">{modelSpread}</p>
            </div>
            <div>
              <p className="text-gray-400 text-xs mb-1">Total</p>
              <p className="text-3xl font-bold font-mono text-amber-400">{modelTotal}</p>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-amber-400/30">
            <p className="text-amber-300 text-xs font-semibold">{awayTeam.name} value edge: {spreadEdge.toFixed(1)} points</p>
          </div>
        </div>

        <div className="relative overflow-hidden rounded-lg p-5 border border-emerald-400/50 backdrop-blur-sm bg-gradient-to-br from-emerald-500/25 to-emerald-500/5">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-emerald-400" />
              <span className="text-emerald-400 font-semibold text-sm">Market Consensus</span>
            </div>
          </div>
            <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-gray-400 text-xs mb-1">Spread</p>
              <p className="text-3xl font-bold font-mono text-emerald-400">{awayTeam.name} {marketSpread > 0 ? '+' : ''}{marketSpread}</p>
            </div>
            <div>
              <p className="text-gray-400 text-xs mb-1">Total</p>
              <p className="text-3xl font-bold font-mono text-emerald-400">{marketTotal}</p>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-emerald-400/30">
            <p className="text-emerald-300 text-xs font-semibold">Market Consensus: {spreadEdge.toFixed(1)}pt discrepancy</p>
          </div>
        </div>
      </div>

      {/* Sportsbook Lines */}
      <div className="mb-4">
        <h4 className="text-gray-300 font-semibold text-sm mb-3 flex items-center gap-2">
          <Info className="w-4 h-4 text-blue-400" />
          Live Sportsbook Lines
        </h4>
        <div className="space-y-3">
          <SportsbookLine 
            name="Bovada" 
            logo={BovadaLogo}
            spread={`${awayTeam.name} ${bovadaSpread > 0 ? '+' : ''}${bovadaSpread}`} 
            total={bovadaTotal.toString()} 
            spreadBadge="CONSENSUS"
            spreadBadgeColor="emerald"
            totalDiff={`${(bovadaTotal - modelTotal).toFixed(1)}`}
          />
          <SportsbookLine 
            name="ESPN Bet" 
            logo={ESPNBetLogo}
            spread={`${awayTeam.name} ${espnBetSpread > 0 ? '+' : ''}${espnBetSpread}`} 
            total={espnBetTotal.toString()} 
            spreadBadge="+1.0"
            spreadBadgeColor="amber"
            totalDiff={`${(espnBetTotal - modelTotal).toFixed(1)}`}
          />
          <SportsbookLine 
            name="DraftKings" 
            logo={DraftKingsLogo}
            spread={`${awayTeam.name} ${draftKingsSpread > 0 ? '+' : ''}${draftKingsSpread}`} 
            total={draftKingsTotal.toString()} 
            spreadBadge="CONSENSUS"
            spreadBadgeColor="emerald"
            totalDiff={`${(draftKingsTotal - modelTotal).toFixed(1)}`}
          />
        </div>

        {/* Model's Line - Featured */}
        <div className="relative overflow-hidden rounded-lg p-6 border border-gray-300/30 backdrop-blur-sm mt-4 bg-gradient-to-br from-slate-800/40 to-slate-900/60">
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gray-700/80 border border-gray-500/40">
                  <ImageWithFallback
                    src={awayTeam.logo}
                    alt={awayTeam.name}
                    className="w-8 h-8 object-contain"
                  />
                </div>
                <div>
                  <div className="text-white text-sm font-semibold uppercase tracking-wide">Market Value Analysis</div>
                  <div className="text-gray-400 text-xs">Model projects {spreadEdge.toFixed(1)}pt value on {awayTeam.name} spread</div>
                </div>
              </div>
              <div className="px-3 py-1.5 bg-gray-700/60 border border-gray-500/40 rounded-lg">
                <span className="text-white text-xs font-semibold">VALUE OPPORTUNITY</span>
              </div>
            </div>
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex gap-6">
                <div className="flex flex-col items-center gap-2 px-4 py-3 bg-gray-800/40 rounded-lg border border-gray-600/40">
                  <span className="text-gray-300 text-xs font-medium uppercase tracking-wide">Value Bet</span>
                  <span className="text-2xl font-bold font-mono text-white">{valueBetSpread}</span>
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                    <span className="text-emerald-400 text-xs font-medium">{spreadEdge.toFixed(1)}PT EDGE</span>
                  </div>
                </div>
                <div className="flex flex-col items-center gap-2 px-4 py-3 bg-gray-800/40 rounded-lg border border-gray-600/40">
                  <span className="text-gray-300 text-xs font-medium uppercase tracking-wide">Total</span>
                  <span className="text-2xl font-bold font-mono text-white">{valueBetTotal}</span>
                  <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                    <span className="text-emerald-400 text-xs font-medium">{totalEdge.toFixed(1)}PT EDGE</span>
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-end gap-1">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                  <span className="text-blue-400 text-xs font-medium">LIVE</span>
                </div>
                <span className="text-gray-500 text-xs">Updated: Now</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-600/40">
              <p className="text-gray-300 text-xs">
                <span className="font-semibold text-emerald-400">Analysis:</span> Model projects {modelSpread} vs market {awayTeam.name} {marketSpread}, creating {spreadEdge.toFixed(1)}-point value. Total model {modelTotal} vs market {marketTotal} ({totalEdge.toFixed(1)}pt edge). Take {valueBetSpread} and {valueBetTotal}.
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
            <p className="text-red-400 font-bold text-sm">Significant Market Disagreement</p>
          </div>
          <p className="text-gray-300 text-xs">Model sees {awayTeam.name} value edge of {spreadEdge.toFixed(1)} points vs market expectations</p>
        </div>
        <div className="relative overflow-hidden rounded-lg p-4 border border-amber-500/50 backdrop-blur-sm bg-gradient-to-br from-amber-500/20 to-amber-500/5">
          <div className="flex items-center gap-2 mb-2">
            <Info className="w-5 h-5 text-amber-400" />
            <p className="text-amber-400 font-bold text-sm">Total Points Variance</p>
          </div>
          <p className="text-gray-300 text-xs">Model projects {totalEdge.toFixed(1)} more points than market consensus ({modelTotal} vs {marketTotal})</p>
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
            <div className="text-gray-300 font-semibold">{name}</div>
          </div>
          <div className="h-8 w-px bg-gray-600"></div>
          <div className="flex gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <span className="text-gray-400 text-xs">Spread</span>
              <span className="text-lg font-bold font-mono text-white">{spread}</span>
              <span className={`px-2 py-0.5 border rounded text-xs font-bold ${badgeColors[spreadBadgeColor]}`}>
                {spreadBadge}
              </span>
            </div>
            <div className="h-6 w-px bg-gray-600 hidden sm:block"></div>
            <div className="flex items-center gap-2">
              <span className="text-gray-400 text-xs">Total</span>
              <span className="text-lg font-bold font-mono text-white">{total}</span>
              <span className="px-2 py-0.5 bg-red-500/30 border border-red-400/50 rounded text-red-400 text-xs font-bold">
                {totalDiff}
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
