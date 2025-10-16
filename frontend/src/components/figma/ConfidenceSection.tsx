import { GlassCard } from './GlassCard';
import { Target, Crosshair } from 'lucide-react';

interface ConfidenceSectionProps {
  predictionData?: {
    confidence?: {
      overall_confidence?: number;
      breakdown?: {
        base_data_quality?: number;
        consistency_factor?: number;
        differential_strength?: number;
        trend_factor?: number;
        weather_calendar?: number;
      };
      calibration?: {
        raw_probability?: number;
        calibrated_probability?: number;
        adjustment?: number;
      };
    };
  };
  isLoading?: boolean;
  error?: string;
}

export function ConfidenceSection({ predictionData, isLoading, error }: ConfidenceSectionProps) {
  // Demo data for Ohio State vs Illinois
  const demoData = {
    overall_confidence: 85.2,
    breakdown: {
      base_data_quality: 0.90,
      consistency_factor: 0.06,
      differential_strength: 0.15,
      trend_factor: 0.05,
      weather_calendar: 0.05
    },
    calibration: {
      raw_probability: 91.9,
      calibrated_probability: 91.9,
      adjustment: 0.0
    }
  };

  // Use live data if available, otherwise use demo data
  const confidenceData = predictionData?.confidence || demoData;
  const confidence = confidenceData.overall_confidence || 85.2;
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <GlassCard className="p-6 border-gray-500/40">
          <div className="space-y-4 animate-pulse">
            <div className="h-4 bg-gray-700 rounded w-3/4"></div>
            <div className="h-8 bg-gray-700 rounded w-1/2"></div>
            <div className="h-3 bg-gray-700 rounded"></div>
          </div>
        </GlassCard>
        <GlassCard className="p-6 border-gray-500/40">
          <div className="space-y-4 animate-pulse">
            <div className="h-4 bg-gray-700 rounded w-3/4"></div>
            <div className="h-20 bg-gray-700 rounded"></div>
          </div>
        </GlassCard>
      </div>
    );
  }

  if (error) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <GlassCard className="p-6 border-red-500/40 col-span-full">
          <div className="text-center text-red-400">
            Error loading confidence data: {error}
          </div>
        </GlassCard>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Confidence Indicator */}
      <GlassCard className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            <h3 className="text-white font-semibold">Model Confidence</h3>
          </div>
          <span className="text-2xl font-mono text-emerald-400 drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">{confidence}%</span>
        </div>
        <div className="relative h-3 bg-gray-800/40 rounded-full overflow-hidden border border-emerald-500/30">
          <div 
            className="absolute inset-y-0 left-0 bg-emerald-500 rounded-full transition-all duration-1000 ease-out shadow-lg shadow-emerald-500/50"
            style={{ width: `${confidence}%` }}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-400/30 to-transparent animate-pulse"></div>
          </div>
        </div>
        <div className="mt-4 space-y-2">
          <MetricRow 
            label="Base Data Quality" 
            value={confidenceData.breakdown?.base_data_quality?.toFixed(2) || "0.90"} 
          />
          <MetricRow 
            label="Consistency Factor" 
            value={`+${confidenceData.breakdown?.consistency_factor?.toFixed(2) || "0.06"}`} 
            positive 
          />
          <MetricRow 
            label="Differential Strength" 
            value={`+${confidenceData.breakdown?.differential_strength?.toFixed(2) || "0.15"}`} 
            positive 
          />
          <MetricRow 
            label="Trend Factor" 
            value={`+${confidenceData.breakdown?.trend_factor?.toFixed(2) || "0.05"}`} 
            positive 
          />
          <div className="border-t border-gray-400/15 pt-2">
            <MetricRow 
              label="Weather/Calendar" 
              value={`+${confidenceData.breakdown?.weather_calendar?.toFixed(2) || "0.05"}`} 
              positive 
            />
          </div>
          <div className="border-t border-emerald-500/30 pt-2">
            <MetricRow 
              label="TOTAL CONFIDENCE" 
              value={(confidence / 100).toFixed(2)} 
              positive 
              bold 
            />
          </div>
        </div>
        <p className="text-gray-400 text-sm mt-3">Based on historical performance and current matchup analysis</p>
      </GlassCard>

      {/* Probability Calibration */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Crosshair className="w-5 h-5 text-cyan-400" />
          <h3 className="text-white font-semibold">Probability Calibration (Platt Scaling)</h3>
        </div>
        <div className="space-y-4">
          <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">Raw Probability</p>
            <p className="text-blue-400 text-3xl font-mono drop-shadow-[0_0_10px_rgba(59,130,246,0.3)]">
              {(confidenceData.calibration?.raw_probability || 91.9).toFixed(1)}%
            </p>
            <p className="text-gray-400 text-xs mt-1">Before calibration</p>
          </div>
          <div className="flex items-center justify-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </div>
          <div className="bg-emerald-500/20 rounded-lg p-4 border border-emerald-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">Calibrated Probability</p>
            <p className="text-emerald-400 text-3xl font-mono drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">
              {(confidenceData.calibration?.calibrated_probability || 91.9).toFixed(1)}%
            </p>
            <p className="text-gray-400 text-xs mt-1">After Platt Scaling</p>
          </div>
          <div className="bg-gray-800/40 rounded-lg p-3 border border-gray-400/15 backdrop-blur-sm">
            <p className="text-gray-300 text-sm font-semibold">Calibration Adjustment</p>
            <p className="text-white text-lg font-mono">
              {(confidenceData.calibration?.adjustment || 0) > 0 ? '+' : ''}
              {(confidenceData.calibration?.adjustment || 0).toFixed(1)} percentage points
            </p>
          </div>
          <p className="text-gray-400 text-xs">Platt Scaling transforms raw probabilities to calibrated estimates based on historical accuracy</p>
        </div>
      </GlassCard>
    </div>
  );
}

function MetricRow({ label, value, positive = false, bold = false }: { label: string; value: string; positive?: boolean; bold?: boolean }) {
  return (
    <div className="flex justify-between items-center text-sm">
      <span className={`${bold ? 'text-white' : 'text-gray-300'}`}>{label}</span>
      <span className={`font-mono ${bold ? 'font-bold' : ''} ${positive ? 'text-emerald-400' : 'text-gray-100'}`}>{value}</span>
    </div>
  );
}
