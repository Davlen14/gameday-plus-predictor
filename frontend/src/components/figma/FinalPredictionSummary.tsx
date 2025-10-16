import { GlassCard } from './GlassCard';
import { Target, Award, CheckCircle2 } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface FinalPredictionSummaryProps {
  predictionData?: any;
}

export function FinalPredictionSummary({ predictionData }: FinalPredictionSummaryProps) {
  // Get data from predictionData (already spread from ui_components)
  const finalPrediction = predictionData?.final_prediction;
  const confidence = predictionData?.confidence;
  const teams = predictionData?.team_selector || predictionData?.header?.teams;
  
  if (!finalPrediction || !confidence || !teams) {
    return null;
  }

  const awayTeam = teams.away_team || teams.away;
  const homeTeam = teams.home_team || teams.home;
  const awayScore = finalPrediction.predicted_score?.away_score || 0;
  const homeScore = finalPrediction.predicted_score?.home_score || 0;
  const total = finalPrediction.predicted_score?.total || 0;
  const overallConfidence = confidence.overall_confidence || 0;
  
  // Remove emojis from key factors
  const removeEmojis = (text: string) => {
    return text.replace(/[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F000}-\u{1F02F}]|[\u{1F0A0}-\u{1F0FF}]|[\u{1F100}-\u{1F64F}]|[\u{1F680}-\u{1F6FF}]|[\u{1F910}-\u{1F96B}]|[\u{1F980}-\u{1F9E0}]|[\u{231A}-\u{23FA}]|[\u{FE00}-\u{FE0F}]|[\u{203C}-\u{3299}]/gu, '').trim();
  };
  
  const keyFactors = (finalPrediction.key_factors || []).map((factor: string) => removeEmojis(factor));
  
  // Determine winner
  const awayWins = awayScore > homeScore;
  const homeWins = homeScore > awayScore;
  
  return (
    <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-6 border-gray-500/40">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
          <Target className="w-5 h-5 text-gray-400" />
        </div>
        <h3 className="text-white font-semibold">Final Prediction Summary</h3>
      </div>
      
      {/* Score Prediction */}
      <div className="mb-6">
        <div className="bg-gradient-to-br from-slate-500/10 to-gray-500/10 border border-gray-500/30 rounded-lg p-6 text-center">
          <h4 className="text-xl font-bold text-gray-300 mb-4">Final Score Prediction</h4>
          <div className="grid grid-cols-3 gap-4 items-center">
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback 
                  src={awayTeam?.logo || ''} 
                  alt={awayTeam?.name || 'Away Team'} 
                  className="w-16 h-16 object-contain drop-shadow-lg transform hover:scale-105 transition-transform duration-300 filter brightness-110" 
                />
                {awayWins && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
              </div>
              <div className={`text-3xl font-bold mb-1 ${awayWins ? 'text-emerald-400' : 'text-gray-400'}`}>{awayScore}</div>
              <div className="text-sm text-gray-300">{awayTeam?.name || 'Away Team'}</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-400 mb-1">vs</div>
              <div className="text-sm text-emerald-400 font-semibold">Total: {Math.round(total)}</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback 
                  src={homeTeam?.logo || ''} 
                  alt={homeTeam?.name || 'Home Team'} 
                  className="w-16 h-16 object-contain drop-shadow-lg transform hover:scale-105 transition-transform duration-300 filter brightness-110" 
                />
                {homeWins && <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]"></div>}
              </div>
              <div className={`text-3xl font-bold mb-1 ${homeWins ? 'text-emerald-400' : 'text-gray-400'}`}>{homeScore}</div>
              <div className="text-sm text-gray-300">{homeTeam?.name || 'Home Team'}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Factors */}
      {keyFactors.length > 0 && (
        <div className="mb-6">
          <h4 className="text-gray-300 font-medium mb-4 flex items-center gap-2">
            <Award className="w-4 h-4" />
            Key Factors
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {keyFactors.map((factor: string, idx: number) => (
              <div key={idx} className="p-4 rounded-lg border bg-slate-500/10 border-gray-500/30">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-gray-200">{factor}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Overall Confidence */}
      <div className="text-center">
        <div className="bg-gray-800/40 border border-gray-600/40 rounded-lg p-6">
          <div className="text-4xl font-bold text-emerald-400 mb-2">{overallConfidence.toFixed(1)}%</div>
          <div className="text-lg font-semibold text-gray-300 mb-3">Overall Confidence</div>
          
          {/* Confidence Bar */}
          <div className="w-full bg-gray-700/40 rounded-full h-3 mb-4">
            <div 
              className="h-3 rounded-full bg-gradient-to-r from-emerald-500 to-green-400 transition-all duration-1000"
              style={{ width: `${overallConfidence}%` }}
            ></div>
          </div>
          
          {confidence.breakdown && (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
              <ConfidenceItem label="Base Data" value={`${confidence.breakdown.base_data_quality}%`} />
              <ConfidenceItem label="Consistency" value={`+${confidence.breakdown.consistency_factor}%`} />
              <ConfidenceItem label="Differential" value={`+${confidence.breakdown.differential_strength}%`} />
              <ConfidenceItem label="Trend" value={`+${confidence.breakdown.trend_factor}%`} />
              <ConfidenceItem label="Weather" value={`+${confidence.breakdown.weather_calendar}%`} />
            </div>
          )}
        </div>
      </div>

      {/* Analysis Complete Badge */}
      <div className="mt-6 text-center">
        <div className="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-500/20 to-green-500/20 border border-emerald-500/40 rounded-full px-6 py-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span className="text-emerald-400 font-semibold">COMPREHENSIVE ANALYSIS COMPLETE!</span>
        </div>
      </div>
    </GlassCard>
  );
}

function ConfidenceItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center">
      <div className="font-mono font-semibold text-gray-300">{value}</div>
      <div className="text-gray-400">{label}</div>
    </div>
  );
}