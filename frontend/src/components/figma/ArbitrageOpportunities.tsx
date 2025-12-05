import { GlassCard } from './GlassCard';
import { DollarSign, TrendingUp, Calculator, AlertTriangle, Shield, Target } from 'lucide-react';
import { useState } from 'react';

interface ArbitrageOpportunitiesProps {
  predictionData?: any;
}

export function ArbitrageOpportunities({ predictionData }: ArbitrageOpportunitiesProps) {
  const [selectedOpportunity, setSelectedOpportunity] = useState<number | null>(null);
  const arbitrageData = predictionData?.arbitrage_analysis || {};
  const opportunities = arbitrageData.opportunities || [];
  const marketEfficiency = arbitrageData.market_efficiency || 100;
  const bestMargin = arbitrageData.best_margin || 0;

  if (opportunities.length === 0) {
    return (
      <GlassCard glowColor="from-emerald-500/10 to-cyan-500/10" className="p-6 border-cyan-500/20">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-lg bg-emerald-500/20 border border-cyan-500/30">
            <DollarSign className="w-5 h-5 text-emerald-400" />
          </div>
          <h2 className="text-xl font-bold text-white">Arbitrage Opportunities</h2>
        </div>
        <div className="text-center py-8">
          <Shield className="w-12 h-12 text-gray-500 mx-auto mb-3 opacity-50" />
          <p className="text-gray-400">No arbitrage opportunities detected at this time</p>
          <p className="text-sm text-gray-500 mt-2">Market efficiency: {marketEfficiency.toFixed(1)}%</p>
        </div>
      </GlassCard>
    );
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400 bg-green-500/20 border-green-500/30';
      case 'medium': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
      case 'high': return 'text-red-400 bg-red-500/20 border-red-500/30';
      default: return 'text-gray-400 bg-gray-500/20 border-gray-500/30';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'pure_arbitrage': return <Shield className="w-5 h-5" />;
      case 'middle': return <Target className="w-5 h-5" />;
      case 'model_edge': return <TrendingUp className="w-5 h-5" />;
      default: return <DollarSign className="w-5 h-5" />;
    }
  };

  const getTypeName = (type: string) => {
    switch (type) {
      case 'pure_arbitrage': return 'Pure Arbitrage';
      case 'middle': return 'Middle Opportunity';
      case 'model_edge': return 'Model Edge Play';
      case 'hedge': return 'Hedge Calculator';
      default: return type;
    }
  };

  return (
    <GlassCard glowColor="from-emerald-500/10 to-cyan-500/10" className="p-6 border-cyan-500/20">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-emerald-500/20 border border-cyan-500/30">
            <DollarSign className="w-5 h-5 text-emerald-400" />
          </div>
          <h2 className="text-xl font-bold text-white">Arbitrage Intelligence</h2>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-gray-400">Best Margin</div>
            <div className="text-lg font-bold text-emerald-400">{bestMargin.toFixed(1)}%</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-400">Market Efficiency</div>
            <div className="text-lg font-bold text-cyan-400">{marketEfficiency.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* Opportunities Grid */}
      <div className="space-y-4">
        {opportunities.map((opp: any, idx: number) => (
          <div
            key={idx}
            className={`
              relative overflow-hidden rounded-xl border transition-all duration-300 cursor-pointer
              ${selectedOpportunity === idx 
                ? 'bg-emerald-500/10 border-emerald-500/50 shadow-lg shadow-emerald-500/20' 
                : 'backdrop-blur-sm border-gray-600/40 hover:border-emerald-500/30'
              }
            `}
            onClick={() => setSelectedOpportunity(selectedOpportunity === idx ? null : idx)}
          >
            {/* Glowing edge effect */}
            <div className={`
              absolute inset-0 bg-gradient-to-r from-emerald-500/0 via-emerald-500/10 to-cyan-500/0 
              ${selectedOpportunity === idx ? 'opacity-100' : 'opacity-0'}
              transition-opacity duration-300
            `} />

            <div className="relative p-4">
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-400">
                    {getTypeIcon(opp.opportunity_type)}
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-white">
                      {getTypeName(opp.opportunity_type)}
                    </div>
                    <div className="text-xs text-gray-400">
                      Confidence: {opp.confidence.toFixed(0)}%
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`px-3 py-1 rounded-full border text-xs font-semibold ${getRiskColor(opp.risk_level)}`}>
                    {opp.risk_level.toUpperCase()}
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-400">Expected Return</div>
                    <div className="text-lg font-bold text-emerald-400">
                      {opp.profit_margin > 0 ? '+' : ''}{opp.profit_margin.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Explanation */}
              <div className="mb-3 p-3 bg-gray-900/50 border border-gray-700/50 rounded-lg">
                <p className="text-sm text-gray-300">{opp.explanation}</p>
              </div>

              {/* Bets Required */}
              {selectedOpportunity === idx && (
                <div className="mt-4 space-y-2 animate-in fade-in duration-300">
                  <div className="text-xs font-semibold text-emerald-400 mb-2 flex items-center gap-2">
                    <Calculator className="w-4 h-4" />
                    Required Bets
                  </div>
                  {opp.bets.map((bet: any, betIdx: number) => (
                    <div
                      key={betIdx}
                      className="bg-gray-900/60 border border-emerald-500/20 rounded-lg p-3"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <div className="text-sm font-semibold text-white">
                            {bet.sportsbook}
                          </div>
                          <div className="text-xs text-gray-400">
                            {bet.team || bet.bet_type} {bet.spread ? `${bet.spread > 0 ? '+' : ''}${bet.spread.toFixed(1)}` : ''}
                            {bet.total ? `${bet.total.toFixed(1)}` : ''}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-gray-400">Stake</div>
                          <div className="text-sm font-bold text-emerald-400">{bet.stake}</div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <div className="text-gray-500">
                          Odds: <span className="text-gray-300">{bet.odds}</span>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* Action Button */}
                  <button className="w-full mt-3 px-4 py-2 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white font-semibold rounded-lg transition-all duration-300 shadow-lg shadow-emerald-500/20">
                    Calculate Exact Stakes
                  </button>
                </div>
              )}

              {/* Click to expand indicator */}
              {selectedOpportunity !== idx && (
                <div className="mt-2 text-center">
                  <div className="text-xs text-gray-500 flex items-center justify-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    Click to see bet details
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-emerald-500/10 to-emerald-500/5 border border-emerald-500/30 rounded-lg p-3">
          <div className="text-xs text-emerald-400 mb-1">Total Opportunities</div>
          <div className="text-2xl font-bold text-white">{opportunities.length}</div>
        </div>
        <div className="bg-gradient-to-br from-cyan-500/10 to-cyan-500/5 border border-cyan-500/30 rounded-lg p-3">
          <div className="text-xs text-cyan-400 mb-1">Pure Arbitrage</div>
          <div className="text-2xl font-bold text-white">
            {opportunities.filter((o: any) => o.opportunity_type === 'pure_arbitrage').length}
          </div>
        </div>
        <div className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 border border-purple-500/30 rounded-lg p-3">
          <div className="text-xs text-purple-400 mb-1">Middle Plays</div>
          <div className="text-2xl font-bold text-white">
            {opportunities.filter((o: any) => o.opportunity_type === 'middle').length}
          </div>
        </div>
      </div>

      {/* Educational Note */}
      <div className="mt-4 p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-lg">
        <div className="flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-cyan-400 mt-0.5 flex-shrink-0" />
          <div className="text-xs text-cyan-200">
            <span className="font-semibold">Arbitrage Notice:</span> Pure arbitrage opportunities guarantee profit by betting both sides across different sportsbooks. Middle opportunities profit if the final result lands in a specific range. Model edges represent high-confidence plays based on advanced analytics.
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
