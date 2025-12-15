import React from 'react';
import { Users, Trophy, CheckCircle2 } from 'lucide-react';
import { ClearGlassCard } from './ClearGlassCard';

interface CoachingComparisonProps {
  coach1Data?: any;
  coach2Data?: any;
  predictionData?: any;
}

export function CoachingComparison({ coach1Data, coach2Data, predictionData }: CoachingComparisonProps) {
  return (
    <ClearGlassCard className="p-6 sm:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg" style={{ background: 'rgba(148, 163, 184, 0.08)' }}>
          <Users className="w-5 h-5 text-gray-400" />
        </div>
        <div>
          <h3 className="text-white font-semibold text-base">
            Advanced Coaching Analysis
          </h3>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Comprehensive 9-Factor Performance Evaluation
          </p>
        </div>
      </div>

      {/* Coming Soon Message */}
      <div className="text-center py-16">
        <div className="mb-6">
          <div 
            className="w-20 h-20 mx-auto rounded-full flex items-center justify-center mb-4"
            style={{ 
              background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%)',
              border: '2px solid rgba(139, 92, 246, 0.2)'
            }}
          >
            <Trophy className="w-10 h-10 text-purple-400" />
          </div>
          <h4 className="text-2xl font-bold text-white mb-2">Coming Soon</h4>
          <p className="text-gray-400 max-w-md mx-auto">
            Advanced head-to-head coaching analysis is currently being enhanced with new metrics and insights.
          </p>
        </div>
        
        <div className="mt-8 p-4 rounded-lg max-w-2xl mx-auto" style={{ background: 'rgba(15, 23, 42, 0.3)' }}>
          <p className="text-sm text-gray-300 mb-3 font-medium">Features in development:</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>9-Factor Performance Comparison</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Career Timeline Analysis</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Big Game Performance Metrics</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Recruiting & Development Stats</span>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <p className="text-xs text-gray-500">
            Visit the dedicated Coach Analysis page for detailed coaching insights
          </p>
        </div>
      </div>
    </ClearGlassCard>
  );
}
