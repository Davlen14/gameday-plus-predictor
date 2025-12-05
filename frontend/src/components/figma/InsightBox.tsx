import { useState } from 'react';
import { LightbulbIcon, TrendingUp, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';

interface InsightBoxProps {
  title?: string;
  whatItMeans: string;
  whyItMatters: string;
  whoHasEdge: {
    team: string;
    reason: string;
    magnitude?: 'small' | 'moderate' | 'significant' | 'major';
  };
  keyDifferences?: string[];
  type?: 'info' | 'advantage' | 'warning';
}

export function InsightBox({ 
  title = "What This Means",
  whatItMeans, 
  whyItMatters, 
  whoHasEdge,
  keyDifferences,
  type = 'info'
}: InsightBoxProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const magnitudeColors = {
    small: { bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-400', label: 'Slight Edge' },
    moderate: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-400', label: 'Moderate Edge' },
    significant: { bg: 'bg-amber-500/10', border: 'border-amber-500/30', text: 'text-amber-400', label: 'Significant Edge' },
    major: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400', label: 'Major Edge' }
  };

  const magnitude = whoHasEdge.magnitude || 'moderate';
  const colors = magnitudeColors[magnitude];

  return (
    <div className="mt-6 space-y-4">
      {/* Header - Clickable to expand/collapse */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between w-full gap-2 border-b border-white/10 pb-2 hover:border-white/20 transition-colors"
      >
        <div className="flex items-center gap-2">
          <LightbulbIcon className="w-5 h-5 text-yellow-400" />
          <h4 className="text-white font-semibold text-lg">{title}</h4>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        )}
      </button>

      {/* Collapsible Content */}
      {isExpanded && (
        <div className="space-y-4 animate-in slide-in-from-top-2 duration-200">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* What It Means */}
            <div className="backdrop-blur-sm border border-slate-600/40 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <AlertCircle className="w-4 h-4 text-blue-400" />
                <span className="text-blue-400 font-semibold text-sm">What It Means</span>
              </div>
              <p className="text-gray-300 text-sm leading-relaxed">{whatItMeans}</p>
            </div>

            {/* Why It Matters */}
            <div className="backdrop-blur-sm border border-slate-600/40 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <span className="text-emerald-400 font-semibold text-sm">Why It Matters</span>
              </div>
              <p className="text-gray-300 text-sm leading-relaxed">{whyItMatters}</p>
            </div>
          </div>

          {/* Who Has The Edge */}
          <div className={`${colors.bg} border ${colors.border} rounded-lg p-5`}>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <svg className={`w-5 h-5 ${colors.text}`} viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" />
                </svg>
                <span className={`${colors.text} font-bold text-sm`}>ADVANTAGE: {whoHasEdge.team.toUpperCase()}</span>
              </div>
              <div className={`px-3 py-1 ${colors.bg} border ${colors.border} rounded-full`}>
                <span className={`${colors.text} text-xs font-semibold`}>{colors.label.toUpperCase()}</span>
              </div>
            </div>
            <p className="text-gray-300 text-sm mb-3">{whoHasEdge.reason}</p>

            {/* Key Differences */}
            {keyDifferences && keyDifferences.length > 0 && (
              <div className="mt-4 pt-4 border-t border-white/10">
                <div className="text-gray-400 font-semibold text-xs mb-2 uppercase tracking-wider">Key Differences</div>
                <ul className="space-y-2">
                  {keyDifferences.map((diff, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className={`${colors.text} mt-0.5`}>•</span>
                      <span>{diff}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
