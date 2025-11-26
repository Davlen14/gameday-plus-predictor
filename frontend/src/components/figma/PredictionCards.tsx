import { GlassCard } from './GlassCard';
import { Loader2 } from 'lucide-react';

interface PredictionCardsProps {
  predictionData?: {
    prediction_cards?: {
      win_probability?: {
        away_team_prob?: number;
        home_team_prob?: number;
        favored_team?: string;
      };
      predicted_spread?: {
        model_spread?: number;
        model_spread_display?: string;
        market_spread?: number;
        edge?: number;
      };
      predicted_total?: {
        model_total?: number;
        market_total?: number;
        edge?: number;
      };
    };
    detailed_analysis?: {
      betting_analysis?: {
        market_spread?: number;
        market_total?: number;
        spread_edge?: number;
        total_edge?: number;
      };
    };
  };
  isLoading?: boolean;
  error?: string;
}

export function PredictionCards({ predictionData, isLoading, error }: PredictionCardsProps) {
  // Demo data for Ohio State vs Illinois
  const demoData = {
    win_probability: {
      home_team_prob: 91.9,
      away_team_prob: 8.1,
      favored_team: "Ohio State"
    },
    predicted_spread: {
      model_spread: -21.5,
      model_spread_display: "Ohio State -21.5",
      market_spread: -19.5,
      edge: 2.0
    },
    predicted_total: {
      model_total: 55.5,
      market_total: 52.5,
      edge: 3.0
    }
  };

  // Use live data if available, otherwise use demo data
  const cardsData = predictionData?.prediction_cards || demoData;
  
  // Get betting analysis for market data
  const bettingAnalysis = predictionData?.detailed_analysis?.betting_analysis;

  // Show loading state
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[1, 2, 3].map(i => (
          <GlassCard key={i} className="p-6 border-gray-500/40">
            <div className="space-y-3 animate-pulse">
              <div className="flex items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              </div>
              <div className="text-center text-gray-400">Loading prediction...</div>
            </div>
          </GlassCard>
        ))}
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <GlassCard className="p-6 border-red-500/40 col-span-full">
          <div className="text-center text-red-400">
            Error: {error}
          </div>
        </GlassCard>
      </div>
    );
  }

  // Extract data from the new API structure
  const homeWinProb = cardsData.win_probability?.home_team_prob || 0;
  const awayWinProb = cardsData.win_probability?.away_team_prob || 0;
  const favoredTeam = cardsData.win_probability?.favored_team || (homeWinProb > awayWinProb ? "Home" : "Away");
  const favoredProb = Math.max(homeWinProb, awayWinProb);
  
  const spread = cardsData.predicted_spread?.model_spread || 0;
  const spreadDisplay = cardsData.predicted_spread?.model_spread_display || 
                       (spread > 0 ? `Home +${spread.toFixed(1)}` : `Home ${spread.toFixed(1)}`);
  
  const total = cardsData.predicted_total?.model_total || 0;
  // Use betting analysis market data if available, otherwise fall back to prediction_cards
  const marketSpread = bettingAnalysis?.market_spread || cardsData.predicted_spread?.market_spread;
  const marketTotal = bettingAnalysis?.market_total || cardsData.predicted_total?.market_total;
  const spreadEdge = bettingAnalysis?.spread_edge || cardsData.predicted_spread?.edge;
  const totalEdge = bettingAnalysis?.total_edge || cardsData.predicted_total?.edge;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
      {/* Win Probability - Real Data from Your Model */}
      <GlassCard glowColor="from-red-500/20 to-rose-500/20" className="p-4 sm:p-6 border-red-500/40 shadow-xl shadow-red-500/50">
        <div className="space-y-2 sm:space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-300 text-xs sm:text-sm">Win Probability</h3>
            <div className="w-2 h-2 sm:w-3 sm:h-3 rounded-full bg-red-500/20 border border-red-500/40 shadow-lg animate-pulse"></div>
          </div>
          <div className="text-red-400 drop-shadow-[0_0_10px_rgba(239,68,68,0.3)]">
            <span className="text-3xl sm:text-4xl md:text-5xl font-mono tracking-tight">{favoredProb.toFixed(1)}%</span>
          </div>
          <div className="space-y-1">
            <p className="text-gray-400 text-xs sm:text-sm font-mono truncate">{favoredTeam} favored</p>
            <div className="flex justify-between text-xs text-gray-500">
              <span>Home: {homeWinProb.toFixed(1)}%</span>
              <span>Away: {awayWinProb.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* Predicted Spread - Real Data from Your Model */}
      <GlassCard glowColor="from-amber-500/20 to-yellow-500/20" className="p-4 sm:p-6 border-amber-500/40 shadow-xl shadow-amber-500/50">
        <div className="space-y-2 sm:space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-300 text-xs sm:text-sm">Predicted Spread</h3>
            <div className="w-2 h-2 sm:w-3 sm:h-3 rounded-full bg-amber-500/20 border border-amber-500/40 shadow-lg animate-pulse"></div>
          </div>
          <div className="text-amber-400 drop-shadow-[0_0_10px_rgba(245,158,11,0.3)]">
            <span className="text-2xl sm:text-3xl md:text-4xl font-mono tracking-tight truncate block">{spreadDisplay}</span>
          </div>
          <div className="space-y-1">
            <p className="text-gray-400 text-xs sm:text-sm font-mono">Wins by: {Math.abs(spread).toFixed(1)} pts</p>
            {marketSpread && (
              <div className="flex justify-between text-xs text-gray-500">
                <span>Market: {marketSpread.toFixed(1)}</span>
                {spreadEdge && (
                  <span className="text-green-400">Edge: {spreadEdge.toFixed(1)}pt</span>
                )}
              </div>
            )}
          </div>
        </div>
      </GlassCard>

      {/* Predicted Total - Real Data from Your Model */}
      <GlassCard glowColor="from-emerald-500/20 to-green-500/20" className="p-4 sm:p-6 border-emerald-500/40 shadow-xl shadow-emerald-500/50">
        <div className="space-y-2 sm:space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-300 text-xs sm:text-sm">Predicted Total</h3>
            <div className="w-2 h-2 sm:w-3 sm:h-3 rounded-full bg-emerald-500/20 border border-emerald-500/40 shadow-lg animate-pulse"></div>
          </div>
          <div className="text-emerald-400 drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">
            <span className="text-3xl sm:text-4xl font-mono tracking-tight">{total.toFixed(1)}</span>
          </div>
          <div className="space-y-1">
            <p className="text-gray-400 text-xs sm:text-sm font-mono">Model: {total.toFixed(1)}</p>
            {marketTotal && (
              <div className="flex justify-between text-xs text-gray-500">
                <span>Market: {marketTotal.toFixed(1)}</span>
                {totalEdge && (
                  <span className="text-green-400">Edge: {totalEdge > 0 ? '+' : ''}{totalEdge.toFixed(1)}</span>
                )}
              </div>
            )}
          </div>
        </div>
      </GlassCard>
    </div>
  );
}
