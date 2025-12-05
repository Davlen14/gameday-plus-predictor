import { GlassCard } from './GlassCard';
import { Calculator, DollarSign, TrendingUp, ArrowRight } from 'lucide-react';
import { useState } from 'react';

interface ArbitrageCalculatorProps {
  predictionData?: any;
}

export function ArbitrageCalculator({ predictionData }: ArbitrageCalculatorProps) {
  const [betAmount, setBetAmount] = useState<number>(1000);
  const [book1Odds, setBook1Odds] = useState<number>(-110);
  const [book2Odds, setBook2Odds] = useState<number>(-110);
  const [showResults, setShowResults] = useState<boolean>(false);

  const hedgeData = predictionData?.arbitrage_analysis?.hedge_calculator || {};
  const scenarios = hedgeData.original_bet_scenarios || [];

  // Calculate arbitrage stakes and profit
  const calculateArbitrage = () => {
    // Convert American odds to decimal
    const decimalOdds1 = book1Odds > 0 ? (book1Odds / 100) + 1 : (100 / Math.abs(book1Odds)) + 1;
    const decimalOdds2 = book2Odds > 0 ? (book2Odds / 100) + 1 : (100 / Math.abs(book2Odds)) + 1;

    // Calculate implied probabilities
    const implied1 = 1 / decimalOdds1;
    const implied2 = 1 / decimalOdds2;
    const totalImplied = implied1 + implied2;

    // Check if arbitrage exists
    const hasArbitrage = totalImplied < 1.0;
    const profitMargin = hasArbitrage ? ((1 / totalImplied - 1) * 100) : 0;

    // Calculate optimal stakes
    const stake1 = betAmount * (implied1 / totalImplied);
    const stake2 = betAmount * (implied2 / totalImplied);

    // Calculate guaranteed profit
    const payout1 = stake1 * decimalOdds1;
    const payout2 = stake2 * decimalOdds2;
    const guaranteedProfit = Math.min(payout1, payout2) - betAmount;

    return {
      hasArbitrage,
      profitMargin,
      stake1,
      stake2,
      payout1,
      payout2,
      guaranteedProfit,
      totalStaked: betAmount
    };
  };

  const results = showResults ? calculateArbitrage() : null;

  return (
    <GlassCard glowColor="from-purple-500/10 to-pink-500/10" className="p-6 border-purple-500/20">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30">
          <Calculator className="w-5 h-5 text-purple-400" />
        </div>
        <h2 className="text-xl font-bold text-white">Arbitrage Calculator</h2>
      </div>

      <div className="space-y-6">
        {/* Input Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Total Investment */}
          <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-4">
            <label className="text-xs font-semibold text-purple-400 mb-2 block">
              Total Investment
            </label>
            <div className="relative">
              <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="number"
                value={betAmount}
                onChange={(e) => setBetAmount(Number(e.target.value))}
                className="w-full pl-9 pr-3 py-2 bg-gray-900/60 border border-purple-500/30 rounded-lg text-white font-semibold focus:outline-none focus:border-purple-500 transition-colors"
                min="1"
                step="100"
              />
            </div>
          </div>

          {/* Book 1 Odds */}
          <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-4">
            <label className="text-xs font-semibold text-cyan-400 mb-2 block">
              Sportsbook 1 Odds
            </label>
            <input
              type="number"
              value={book1Odds}
              onChange={(e) => setBook1Odds(Number(e.target.value))}
              className="w-full px-3 py-2 bg-gray-900/60 border border-cyan-500/30 rounded-lg text-white font-semibold focus:outline-none focus:border-cyan-500 transition-colors"
              step="5"
            />
          </div>

          {/* Book 2 Odds */}
          <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-4">
            <label className="text-xs font-semibold text-emerald-400 mb-2 block">
              Sportsbook 2 Odds
            </label>
            <input
              type="number"
              value={book2Odds}
              onChange={(e) => setBook2Odds(Number(e.target.value))}
              className="w-full px-3 py-2 bg-gray-900/60 border border-emerald-500/30 rounded-lg text-white font-semibold focus:outline-none focus:border-emerald-500 transition-colors"
              step="5"
            />
          </div>
        </div>

        {/* Calculate Button */}
        <button
          onClick={() => setShowResults(true)}
          style={{
            background: 'linear-gradient(135deg, rgb(204, 0, 28) 0%, rgb(161, 0, 20) 25%, rgb(115, 0, 13) 50%, rgb(161, 0, 20) 75%, rgb(204, 0, 28) 100%)'
          }}
          className="w-full px-6 py-3 hover:brightness-110 text-white font-bold rounded-lg transition-all duration-300 shadow-lg shadow-red-900/40 flex items-center justify-center gap-3 group"
        >
          <div className="flex items-center gap-1 opacity-80 group-hover:opacity-100 transition-opacity">
            <span className="text-xs font-semibold">DK</span>
            <span className="text-xs">•</span>
            <span className="text-xs font-semibold">FD</span>
            <span className="text-xs">•</span>
            <span className="text-xs font-semibold">MGM</span>
          </div>
          <Calculator className="w-5 h-5" />
          Calculate Optimal Stakes
        </button>

        {/* Results Section */}
        {showResults && results && (
          <div className="space-y-4 animate-in fade-in duration-500">
            {/* Arbitrage Status */}
            <div className={`
              p-4 rounded-lg border-2 text-center
              ${results.hasArbitrage 
                ? 'bg-emerald-500/10 border-emerald-500/50' 
                : 'bg-red-500/10 border-red-500/50'
              }
            `}>
              <div className="text-2xl font-bold mb-1">
                {results.hasArbitrage ? (
                  <span className="text-emerald-400">✓ Arbitrage Exists!</span>
                ) : (
                  <span className="text-red-400">✗ No Arbitrage</span>
                )}
              </div>
              <div className="text-sm text-gray-300">
                {results.hasArbitrage 
                  ? `Guaranteed ${results.profitMargin.toFixed(2)}% profit margin`
                  : 'Combined implied probability exceeds 100%'
                }
              </div>
            </div>

            {results.hasArbitrage && (
              <>
                {/* Stake Distribution */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gradient-to-br from-cyan-500/10 to-cyan-500/5 border border-cyan-500/30 rounded-lg p-4">
                    <div className="text-xs text-cyan-400 mb-2">Stake on Book 1</div>
                    <div className="text-2xl font-bold text-white mb-1">
                      ${results.stake1.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-400">
                      Potential Payout: ${results.payout1.toFixed(2)}
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-emerald-500/10 to-emerald-500/5 border border-emerald-500/30 rounded-lg p-4">
                    <div className="text-xs text-emerald-400 mb-2">Stake on Book 2</div>
                    <div className="text-2xl font-bold text-white mb-1">
                      ${results.stake2.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-400">
                      Potential Payout: ${results.payout2.toFixed(2)}
                    </div>
                  </div>
                </div>

                {/* Profit Summary */}
                <div className="bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm text-gray-400 mb-1">Guaranteed Profit</div>
                      <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
                        +${results.guaranteedProfit.toFixed(2)}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-400 mb-1">ROI</div>
                      <div className="text-2xl font-bold text-purple-400">
                        {((results.guaranteedProfit / results.totalStaked) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </div>

                {/* Visual Flow */}
                <div className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-4">
                  <div className="flex items-center justify-between text-sm">
                    <div className="text-center flex-1">
                      <div className="text-gray-400 mb-1">Total Investment</div>
                      <div className="text-lg font-bold text-white">${results.totalStaked.toFixed(2)}</div>
                    </div>
                    <ArrowRight className="w-6 h-6 text-purple-400 mx-4" />
                    <div className="text-center flex-1">
                      <div className="text-gray-400 mb-1">Guaranteed Return</div>
                      <div className="text-lg font-bold text-emerald-400">
                        ${(results.totalStaked + results.guaranteedProfit).toFixed(2)}
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* Hedge Scenarios */}
        {scenarios.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-semibold text-purple-400 mb-3 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Common Hedge Scenarios
            </h3>
            <div className="space-y-2">
              {scenarios.map((scenario: any, idx: number) => (
                <div
                  key={idx}
                  className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-3 hover:border-purple-500/30 transition-colors"
                >
                  <div className="text-xs font-semibold text-white mb-1">
                    {scenario.scenario}
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <div>Original: <span className="text-gray-300">{scenario.original}</span></div>
                    <ArrowRight className="w-3 h-3 text-purple-400 mx-2" />
                    <div>Hedge: <span className="text-gray-300">{scenario.hedge_at}</span></div>
                  </div>
                  <div className="text-xs text-emerald-400 mt-1">{scenario.profit_if_hedged}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Educational Note */}
        <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg">
          <div className="text-xs text-purple-200">
            <span className="font-semibold">How it works:</span> Arbitrage betting exploits price differences between sportsbooks. By betting both outcomes at optimal stakes, you guarantee profit regardless of the result. The calculator determines the exact amount to bet on each side to lock in risk-free returns.
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
