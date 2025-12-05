import { ClearGlassCard } from './ClearGlassCard';
import { Target, Award, CheckCircle2, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

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
    <ClearGlassCard className="p-4 sm:p-6 border-gray-500/40">
    <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
        <div className="p-1.5 sm:p-2 rounded-lg border border-gray-500/40">
          <Target className="w-4 h-4 sm:w-5 sm:h-5 text-gray-400" />
        </div>
        <h3 className="text-white font-semibold text-sm sm:text-base">Final Prediction Summary</h3>
      </div>
      
      {/* Score Prediction */}
      <div className="mb-4 sm:mb-6">
        <div className="border border-gray-500/30 rounded-lg p-4 sm:p-6 text-center">
          <h4 className="text-lg sm:text-xl font-bold text-gray-300 mb-3 sm:mb-4">Final Score Prediction</h4>
          <div className="grid grid-cols-3 gap-2 sm:gap-4 items-center">
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 sm:gap-2 mb-2">
                <ImageWithFallback 
                  src={awayTeam?.logo || ''} 
                  alt={awayTeam?.name || 'Away Team'} 
                  className="w-12 h-12 sm:w-16 sm:h-16 object-contain drop-shadow-lg transform hover:scale-105 transition-transform duration-300 filter brightness-110" 
                />
                {awayWins && <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(5,150,105,0.9),0_0_20px_rgba(5,150,105,0.5)]"></div>}
              </div>
              <div className={`text-2xl sm:text-3xl font-bold mb-1 ${awayWins ? 'text-emerald-400 drop-shadow-[0_0_10px_rgba(5,150,105,0.8)]' : 'text-gray-400'}`}>{awayScore}</div>
              <div className="text-xs sm:text-sm text-gray-300 truncate">{awayTeam?.name || 'Away Team'}</div>
            </div>
            <div className="text-center">
              <div className="text-xl sm:text-2xl font-bold text-gray-400 mb-1">vs</div>
              <div className="text-xs sm:text-sm text-emerald-400 font-semibold drop-shadow-[0_0_6px_rgba(5,150,105,0.7)]">Total: {Math.round(total)}</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 sm:gap-2 mb-2">
                <ImageWithFallback 
                  src={homeTeam?.logo || ''} 
                  alt={homeTeam?.name || 'Home Team'} 
                  className="w-12 h-12 sm:w-16 sm:h-16 object-contain drop-shadow-lg transform hover:scale-105 transition-transform duration-300 filter brightness-110" 
                />
                {homeWins && <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(5,150,105,0.9),0_0_20px_rgba(5,150,105,0.5)]"></div>}
              </div>
              <div className={`text-2xl sm:text-3xl font-bold mb-1 ${homeWins ? 'text-emerald-400 drop-shadow-[0_0_10px_rgba(5,150,105,0.8)]' : 'text-gray-400'}`}>{homeScore}</div>
              <div className="text-xs sm:text-sm text-gray-300 truncate">{homeTeam?.name || 'Home Team'}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Factors */}
      {keyFactors.length > 0 && (
        <div className="mb-4 sm:mb-6">
          <h4 className="text-gray-300 font-medium mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
            <Award className="w-3 h-3 sm:w-4 sm:h-4" />
            Key Factors
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 sm:gap-3">
            {keyFactors.map((factor: string, idx: number) => (
              <div key={idx} className="p-3 sm:p-4 rounded-lg border border-gray-500/30">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="w-3 h-3 sm:w-4 sm:h-4 text-emerald-500 mt-0.5 flex-shrink-0 drop-shadow-[0_0_6px_rgba(5,150,105,0.7)]" />
                  <span className="text-xs sm:text-sm text-gray-200">{factor}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Win Probability Analysis */}
      <div className="mb-4 sm:mb-6">
        <h4 className="text-gray-300 font-medium mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
          <Target className="w-3 h-3 sm:w-4 sm:h-4" />
          Win Probability Analysis
        </h4>
        
        {/* Probability Cards with Watermarks */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Away Team Card */}
          <div 
            className="relative rounded-xl p-4 sm:p-5 overflow-hidden border-2 shadow-xl"
            style={{
              background: `linear-gradient(135deg, ${awayTeam?.primary_color || '#6366f1'}15 0%, ${awayTeam?.primary_color || '#6366f1'}08 100%)`,
              borderColor: awayWins ? '#10b981' : `${awayTeam?.primary_color || '#6366f1'}40`
            }}
          >
            {/* Watermark Logo */}
            <div className="absolute top-0 right-0 w-32 h-32 sm:w-40 sm:h-40 opacity-5 overflow-hidden">
              <ImageWithFallback 
                src={awayTeam?.logo || ''} 
                alt={awayTeam?.name || 'Away Team'} 
                className="w-full h-full object-contain scale-150"
              />
            </div>
            
            {/* Edge Indicator */}
            {awayWins && (
              <div className="absolute top-3 right-3 flex items-center gap-1 bg-gradient-to-r from-emerald-700 via-emerald-600 to-emerald-700 text-white px-2.5 py-1 rounded-md text-xs font-bold shadow-[0_0_20px_rgba(5,150,105,0.6),inset_0_1px_1px_rgba(16,185,129,0.3)] border border-emerald-500/50">
                <ArrowRight className="w-3 h-3 drop-shadow-[0_0_4px_rgba(255,255,255,0.8)]" />
                EDGE
              </div>
            )}
            
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <ImageWithFallback 
                  src={awayTeam?.logo || ''} 
                  alt={awayTeam?.name || 'Away Team'} 
                  className="w-10 h-10 sm:w-12 sm:h-12 object-contain drop-shadow-lg"
                />
                <div>
                  <div className="font-bold text-sm sm:text-base text-white">{awayTeam?.name || 'Away Team'}</div>
                  <div className="text-xs text-gray-300">Away Team</div>
                </div>
              </div>
              
              <div className="text-4xl sm:text-5xl font-black mb-2" style={{ color: awayTeam?.primary_color || '#6366f1' }}>
                51.7%
              </div>
              
              <div className="space-y-1.5 text-xs">
                <div className="flex items-center gap-1.5 text-gray-200">
                  <TrendingUp className="w-3.5 h-3.5" style={{ color: awayTeam?.primary_color || '#6366f1' }} />
                  <span>Slight favorite by 3.4%</span>
                </div>
                <div className="flex items-center gap-1.5 text-gray-200">
                  <Target className="w-3.5 h-3.5" style={{ color: awayTeam?.primary_color || '#6366f1' }} />
                  <span>High model confidence</span>
                </div>
              </div>
            </div>
          </div>

          {/* Visual Pie Chart */}
          <div className="relative flex flex-col items-center justify-center">
            {/* Percentage Labels Above Chart */}
            <div className="flex items-center justify-between w-full px-8 mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl sm:text-3xl font-black" style={{ color: awayTeam?.primary_color || '#6366f1' }}>
                  51.7%
                </span>
                <div 
                  className="w-4 h-4 rounded-sm"
                  style={{ 
                    background: `repeating-linear-gradient(45deg, ${awayTeam?.primary_color || '#6366f1'}, ${awayTeam?.primary_color || '#6366f1'} 2px, transparent 2px, transparent 4px)`
                  }}
                ></div>
                <span className="text-xs text-gray-400 uppercase tracking-wider">{awayTeam?.school || 'Away'}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-400 uppercase tracking-wider">{homeTeam?.school || 'Home'}</span>
                <div 
                  className="w-4 h-4 rounded-sm"
                  style={{ backgroundColor: homeTeam?.primary_color || '#10b981' }}
                ></div>
                <span className="text-2xl sm:text-3xl font-black" style={{ color: homeTeam?.primary_color || '#10b981' }}>
                  48.3%
                </span>
              </div>
            </div>

            <div className="relative">
              <ResponsiveContainer width={200} height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: awayTeam?.name || 'Away', value: 51.7 },
                      { name: homeTeam?.name || 'Home', value: 48.3 }
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={95}
                    paddingAngle={0}
                    dataKey="value"
                    startAngle={90}
                    endAngle={450}
                  >
                    <Cell 
                      fill="url(#awayPattern)"
                      stroke={awayTeam?.primary_color || '#6366f1'}
                      strokeWidth={0}
                    />
                    <Cell 
                      fill={homeTeam?.primary_color || '#10b981'}
                      stroke={homeTeam?.primary_color || '#10b981'}
                      strokeWidth={0}
                    />
                  </Pie>
                  <defs>
                    <pattern id="awayPattern" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
                      <line x1="0" y1="0" x2="0" y2="8" stroke={awayTeam?.primary_color || '#6366f1'} strokeWidth="4"/>
                    </pattern>
                  </defs>
                </PieChart>
              </ResponsiveContainer>
              
              {/* Center Logos */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="flex items-center gap-3">
                  <ImageWithFallback 
                    src={awayTeam?.logo || ''} 
                    alt={awayTeam?.name || 'Away Team'} 
                    className="w-16 h-16 object-contain drop-shadow-xl"
                  />
                  <div className="w-px h-16 bg-gray-600"></div>
                  <ImageWithFallback 
                    src={homeTeam?.logo || ''} 
                    alt={homeTeam?.name || 'Home Team'} 
                    className="w-16 h-16 object-contain drop-shadow-xl"
                  />
                </div>
              </div>
            </div>

            {/* Attribution */}
            <div className="text-gray-400 text-xs mt-2">
              According to Model Analytics
            </div>
          </div>

          {/* Home Team Card */}
          <div 
            className="relative rounded-xl p-4 sm:p-5 overflow-hidden border-2 shadow-xl"
            style={{
              background: `linear-gradient(135deg, ${homeTeam?.primary_color || '#10b981'}15 0%, ${homeTeam?.primary_color || '#10b981'}08 100%)`,
              borderColor: homeWins ? '#10b981' : `${homeTeam?.primary_color || '#10b981'}40`
            }}
          >
            {/* Watermark Logo */}
            <div className="absolute top-0 right-0 w-32 h-32 sm:w-40 sm:h-40 opacity-5 overflow-hidden">
              <ImageWithFallback 
                src={homeTeam?.logo || ''} 
                alt={homeTeam?.name || 'Home Team'} 
                className="w-full h-full object-contain scale-150"
              />
            </div>
            
            {/* Edge Indicator */}
            {homeWins && (
              <div className="absolute top-3 right-3 flex items-center gap-1 bg-gradient-to-r from-emerald-700 via-emerald-600 to-emerald-700 text-white px-2.5 py-1 rounded-md text-xs font-bold shadow-[0_0_20px_rgba(5,150,105,0.6),inset_0_1px_1px_rgba(16,185,129,0.3)] border border-emerald-500/50">
                <ArrowRight className="w-3 h-3 drop-shadow-[0_0_4px_rgba(255,255,255,0.8)]" />
                EDGE
              </div>
            )}
            
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <ImageWithFallback 
                  src={homeTeam?.logo || ''} 
                  alt={homeTeam?.name || 'Home Team'} 
                  className="w-10 h-10 sm:w-12 sm:h-12 object-contain drop-shadow-lg"
                />
                <div>
                  <div className="font-bold text-sm sm:text-base text-white">{homeTeam?.name || 'Home Team'}</div>
                  <div className="text-xs text-gray-300">Home Team</div>
                </div>
              </div>
              
              <div className="text-4xl sm:text-5xl font-black mb-2" style={{ color: homeTeam?.primary_color || '#10b981' }}>
                48.3%
              </div>
              
              <div className="space-y-1.5 text-xs">
                <div className="flex items-center gap-1.5 text-gray-200">
                  <TrendingDown className="w-3.5 h-3.5" style={{ color: homeTeam?.primary_color || '#10b981' }} />
                  <span>Underdog trailing by 3.4%</span>
                </div>
                <div className="flex items-center gap-1.5 text-gray-200">
                  <Target className="w-3.5 h-3.5" style={{ color: homeTeam?.primary_color || '#10b981' }} />
                  <span>Home field advantage</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* High Confidence Badge */}
        <div className="mt-4 text-center">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-950/80 via-emerald-900/90 to-emerald-950/80 border border-emerald-600/60 rounded-lg px-4 py-2.5 shadow-[0_0_25px_rgba(5,150,105,0.4),inset_0_1px_1px_rgba(16,185,129,0.2)]">
            <div className="flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_rgba(5,150,105,1),0_0_20px_rgba(5,150,105,0.5)]"></div>
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_rgba(5,150,105,1),0_0_20px_rgba(5,150,105,0.5)]" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_rgba(5,150,105,1),0_0_20px_rgba(5,150,105,0.5)]" style={{ animationDelay: '0.4s' }}></div>
            </div>
            <span className="text-emerald-400 font-bold text-sm tracking-wide uppercase drop-shadow-[0_0_8px_rgba(5,150,105,0.8)]">High Confidence</span>
            <div className="w-px h-5 bg-gradient-to-b from-emerald-600/40 via-emerald-500/60 to-emerald-600/40 shadow-[0_0_4px_rgba(5,150,105,0.6)]"></div>
            <span className="text-emerald-300 font-mono font-semibold text-sm drop-shadow-[0_0_6px_rgba(5,150,105,0.7)]">80.8%</span>
            <span className="text-gray-400 text-xs">Certainty</span>
          </div>
        </div>
      </div>

      {/* Overall Confidence */}
      <div className="text-center">
        <div className="border border-gray-600/40 rounded-lg p-6">
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
      <div className="mt-4 sm:mt-6 text-center">
        <div className="inline-flex items-center gap-1.5 sm:gap-2 bg-gradient-to-r from-emerald-950/80 via-emerald-900/90 to-emerald-950/80 border border-emerald-600/60 rounded-full px-4 sm:px-6 py-2 sm:py-3 shadow-[0_0_30px_rgba(5,150,105,0.4),inset_0_1px_1px_rgba(16,185,129,0.2)]">
          <CheckCircle2 className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 drop-shadow-[0_0_8px_rgba(5,150,105,0.9)]" />
          <span className="text-emerald-400 font-semibold text-xs sm:text-base drop-shadow-[0_0_8px_rgba(5,150,105,0.8)]">
            <span className="hidden sm:inline">COMPREHENSIVE ANALYSIS COMPLETE!</span>
            <span className="sm:hidden">ANALYSIS COMPLETE!</span>
          </span>
        </div>
      </div>
    </ClearGlassCard>
  );
}

function ConfidenceItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center">
      <div className="font-mono font-semibold text-gray-300 text-sm sm:text-base">{value}</div>
      <div className="text-gray-400 text-xs sm:text-sm">{label}</div>
    </div>
  );
}