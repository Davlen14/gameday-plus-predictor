import { GlassCard } from './GlassCard';
import { Sliders } from 'lucide-react';

const weights = [
  { name: 'Opponent-Adjusted Metrics', value: 50, color: 'bg-blue-500' },
  { name: 'Market Consensus', value: 20, color: 'bg-purple-500' },
  { name: 'Composite Ratings (Talent)', value: 15, color: 'bg-green-500' },
  { name: 'Key Player Impact', value: 10, color: 'bg-amber-500' },
  { name: 'Contextual Factors', value: 5, color: 'bg-red-500' }
];

interface WeightsBreakdownProps {
  predictionData?: any;
}

export function WeightsBreakdown({ predictionData }: WeightsBreakdownProps) {
  return (
    <GlassCard className="p-4 sm:p-6">
      <div className="flex items-center gap-2 mb-3 sm:mb-4">
        <Sliders className="w-4 h-4 sm:w-5 sm:h-5 text-gray-300" />
        <h3 className="text-white font-semibold text-sm sm:text-base">Model Weights Breakdown</h3>
      </div>
      <div className="space-y-3 sm:space-y-4">
        {weights.map((weight) => (
          <div key={weight.name}>
            <div className="flex justify-between items-center mb-1.5 sm:mb-2 gap-2">
              <span className="text-gray-300 text-xs sm:text-sm truncate">{weight.name}</span>
              <span className="text-white font-bold text-sm sm:text-base whitespace-nowrap">{weight.value}%</span>
            </div>
            <div className="relative h-2 bg-gray-800/40 rounded-full overflow-hidden border border-gray-400/15">
              <div 
                className={`absolute inset-y-0 left-0 rounded-full transition-all duration-500 ${weight.color}`}
                style={{ width: `${weight.value}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}
