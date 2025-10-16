import { GlassCard } from './GlassCard';
import { Calculator, TrendingUp, TrendingDown, Settings } from 'lucide-react';

interface ComponentBreakdownProps {
  predictionData?: any;
}

export function ComponentBreakdown({ predictionData }: ComponentBreakdownProps) {
  return (
    <GlassCard className="p-6">
      <div className="flex items-center gap-2 mb-6">
        <Settings className="w-5 h-5 text-cyan-400" />
        <h3 className="text-white font-semibold">Weighted Component Breakdown</h3>
      </div>
      
      {/* Component 1: Opponent-Adjusted */}
      <div className="mb-4 bg-blue-500/20 rounded-lg p-4 border border-blue-400/40 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-blue-400 font-semibold">[1/5] Opponent-Adjusted Metrics (50%)</h4>
          <span className="text-blue-400 font-bold text-xl font-mono drop-shadow-[0_0_10px_rgba(59,130,246,0.3)]">-0.316</span>
        </div>
        <div className="space-y-1 text-sm text-gray-300">
          <p className="font-mono">• Advanced Metrics Diff: <span className="text-gray-200">-0.132</span></p>
          <p className="font-mono">• Temporal Performance Diff: <span className="text-gray-200">-2.618</span></p>
          <p className="font-mono">• SoS Adjustment: <span className="text-gray-200">-0.152</span></p>
          <p className="font-semibold text-blue-300 mt-2 font-mono">→ Final Component: -0.631 × 50% = -0.316</p>
        </div>
      </div>

      {/* Component 2: Market Consensus */}
      <div className="mb-4 bg-purple-500/20 rounded-lg p-4 border border-purple-400/40 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-purple-400 font-semibold">[2/5] Market Consensus (20%)</h4>
          <span className="text-purple-400 font-bold text-xl font-mono drop-shadow-[0_0_10px_rgba(168,85,247,0.3)]">+0.290</span>
        </div>
        <div className="space-y-1 text-sm text-gray-300">
          <p className="font-mono">• Consensus Spread: <span className="text-gray-200">+14.5</span></p>
          <p className="font-mono">• Consensus Total: <span className="text-gray-200">50.7</span></p>
          <p className="font-mono">• Market Signal: <span className="text-gray-200">1.450</span></p>
          <p className="font-semibold text-purple-300 mt-2 font-mono">→ Signal: 1.450 × 20% = +0.290</p>
        </div>
      </div>

      {/* Component 3: Composite Ratings */}
      <div className="mb-4 bg-emerald-500/20 rounded-lg p-4 border border-emerald-400/40 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-emerald-400 font-semibold">[3/5] Composite Ratings - Talent (15%)</h4>
          <span className="text-emerald-400 font-bold text-xl font-mono drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">-15.244</span>
        </div>
        <div className="space-y-1 text-sm text-gray-300">
          <p className="font-mono">• FPI Differential: <span className="text-gray-200">-14.54</span></p>
          <p className="font-mono">• ELO Differential: <span className="text-gray-200">-4.93</span></p>
          <p className="font-mono">• Talent Diff: <span className="text-gray-200">-311.56</span></p>
          <p className="font-semibold text-emerald-300 mt-2 font-mono">→ Score: -101.629 × 15% = -15.244</p>
        </div>
      </div>

      {/* Final Calculation */}
      <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 rounded-lg p-6 border border-cyan-500/30 backdrop-blur-sm shadow-lg shadow-cyan-500/10">
        <div className="flex items-center gap-2 mb-4">
          <svg className="w-5 h-5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
          </svg>
          <h4 className="font-bold text-white text-lg">Final Calculation</h4>
        </div>
        <div className="space-y-2 text-sm mb-4">
          <CalcRow label="Opponent-Adjusted (50%)" value="-0.316" />
          <CalcRow label="Market Consensus (20%)" value="+0.290" />
          <CalcRow label="Composite Ratings (15%)" value="-15.244" />
          <CalcRow label="Key Player Impact (10%)" value="-0.004" />
          <div className="border-b border-cyan-500/30 pb-3">
            <CalcRow label="Contextual Factors (5%)" value="-0.020" />
          </div>
          <div className="flex justify-between items-center pt-3">
            <span className="text-white font-semibold">RAW DIFFERENTIAL:</span>
            <span className="text-2xl font-bold font-mono text-red-400 drop-shadow-[0_0_10px_rgba(239,68,68,0.3)]">-15.293</span>
          </div>
        </div>
        <div className="space-y-2 text-sm border-t-2 border-cyan-500/30 pt-4">
          <div className="flex justify-between items-center text-emerald-400">
            <span>+ Home Field Advantage:</span>
            <span className="font-mono font-semibold">+2.5</span>
          </div>
          <div className="flex justify-between items-center text-emerald-400">
            <span>+ Conference Bonus:</span>
            <span className="font-mono font-semibold">+1.0</span>
          </div>
          <div className="flex justify-between items-center text-gray-400 border-b border-cyan-500/30 pb-3">
            <span>- Weather Penalty:</span>
            <span className="font-mono font-semibold">-0.0</span>
          </div>
          <div className="flex justify-between items-center pt-3">
            <span className="text-white font-bold text-lg">ADJUSTED DIFFERENTIAL:</span>
            <span className="text-3xl font-bold font-mono text-cyan-400 drop-shadow-[0_0_10px_rgba(6,182,212,0.3)]">-11.793</span>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}

function CalcRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-gray-300">{label}:</span>
      <span className="font-bold font-mono text-gray-200">{value}</span>
    </div>
  );
}
