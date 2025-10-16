import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Check } from 'lucide-react';

// Custom Tooltip Component with Team Logos
const CustomTooltip = ({ active, payload, label, awayTeam, homeTeam, awayAbbr, homeAbbr }: any) => {
  if (active && payload && payload.length) {
    const awayValue = payload.find((p: any) => p.dataKey === awayAbbr)?.value;
    const homeValue = payload.find((p: any) => p.dataKey === homeAbbr)?.value;
    const isAwayWinning = awayValue > homeValue;
    const isHomeWinning = homeValue > awayValue;

    return (
      <div 
        style={{ 
          backgroundColor: 'rgba(26, 31, 38, 0.95)', 
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '8px',
          padding: '12px',
          fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
          minWidth: '180px'
        }}
      >
        <p style={{ 
          color: '#e2e8f0', 
          fontSize: '12px', 
          fontWeight: 600, 
          marginBottom: '8px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          paddingBottom: '6px'
        }}>
          {label}
        </p>
        
        {/* Away Team */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          marginBottom: '6px',
          padding: '4px',
          backgroundColor: isAwayWinning ? 'rgba(16, 185, 129, 0.1)' : 'transparent',
          borderRadius: '4px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <img 
              src={awayTeam?.logo || ''} 
              alt={awayTeam?.name || 'Away'}
              style={{ width: '20px', height: '20px', objectFit: 'contain' }}
            />
            <span style={{ color: awayTeam?.primary_color || '#6366f1', fontSize: '11px', fontWeight: 600 }}>{awayAbbr}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ color: '#cbd5e1', fontSize: '13px', fontWeight: 700 }}>{awayValue}%</span>
            {isAwayWinning && (
              <Check style={{ width: '14px', height: '14px', color: '#10b981', strokeWidth: 3 }} />
            )}
          </div>
        </div>

        {/* Home Team */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          padding: '4px',
          backgroundColor: isHomeWinning ? 'rgba(16, 185, 129, 0.1)' : 'transparent',
          borderRadius: '4px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <img 
              src={homeTeam?.logo || ''} 
              alt={homeTeam?.name || 'Home'}
              style={{ width: '20px', height: '20px', objectFit: 'contain' }}
            />
            <span style={{ color: homeTeam?.primary_color || '#10b981', fontSize: '11px', fontWeight: 600 }}>{homeAbbr}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ color: '#cbd5e1', fontSize: '13px', fontWeight: 700 }}>{homeValue}%</span>
            {isHomeWinning && (
              <Check style={{ width: '14px', height: '14px', color: '#10b981', strokeWidth: 3 }} />
            )}
          </div>
        </div>
      </div>
    );
  }

  return null;
};

// Custom Dot Component for Team Logos
const CustomDot = (props: any) => {
  const { cx, cy, payload, dataKey, awayTeam, homeTeam, awayAbbr, homeAbbr } = props;
  
  if (!awayTeam || !homeTeam) return null;
  
  // Determine which team has the advantage for this metric
  const awayValue = payload[awayAbbr];
  const homeValue = payload[homeAbbr];
  
  // Only show logo on the line of the winning team
  const isAwayWinning = awayValue > homeValue;
  const isHomeWinning = homeValue > awayValue;
  
  // Away team line
  if (dataKey === awayAbbr && isAwayWinning) {
    return (
      <image
        x={cx - 16}
        y={cy - 16}
        width={32}
        height={32}
        href={awayTeam.logo}
        style={{ filter: `drop-shadow(0px 6px 16px ${awayTeam.primary_color}80)` }}
      />
    );
  }
  
  // Home team line
  if (dataKey === homeAbbr && isHomeWinning) {
    return (
      <image
        x={cx - 16}
        y={cy - 16}
        width={32}
        height={32}
        href={homeTeam.logo}
        style={{ filter: `drop-shadow(0px 6px 16px ${homeTeam.primary_color}80)` }}
      />
    );
  }
  
  // Don't render anything if this team is not winning
  return null;
};



interface WinProbabilitySectionProps {
  predictionData?: any;
}

export function WinProbabilitySection({ predictionData }: WinProbabilitySectionProps) {
  // Parse formatted analysis for situational performance and confidence
  const parseFormattedAnalysis = () => {
    if (!predictionData?.formatted_analysis) {
      return {
        confidence: 85.0,
        situationalPerformance: {
          away_passing_downs: 30.0,
          home_passing_downs: 28.0,
          away_standard_downs: 45.0,
          home_standard_downs: 47.0
        }
      };
    }

    const analysis = predictionData.formatted_analysis;
    
    // Extract model confidence
    const confidenceMatch = analysis.match(/Model Confidence:\s*(\d+\.?\d*)%/);
    const confidence = confidenceMatch ? parseFloat(confidenceMatch[1]) : 85.0;

    // Extract situational performance from section [9]
    const passingDownsAwayMatch = analysis.match(new RegExp(`${predictionData.team_selector?.away_team?.name || 'Away'}\\s+Passing Downs:\\s*([0-9.]+)`));
    const passingDownsHomeMatch = analysis.match(new RegExp(`${predictionData.team_selector?.home_team?.name || 'Home'}\\s+Passing Downs:\\s*([0-9.]+)`));
    const standardDownsAwayMatch = analysis.match(new RegExp(`${predictionData.team_selector?.away_team?.name || 'Away'}\\s+Standard Downs:\\s*([0-9.]+)`));
    const standardDownsHomeMatch = analysis.match(new RegExp(`${predictionData.team_selector?.home_team?.name || 'Home'}\\s+Standard Downs:\\s*([0-9.]+)`));

    return {
      confidence,
      situationalPerformance: {
        away_passing_downs: passingDownsAwayMatch ? parseFloat(passingDownsAwayMatch[1]) * 100 : 30.0,
        home_passing_downs: passingDownsHomeMatch ? parseFloat(passingDownsHomeMatch[1]) * 100 : 28.0,
        away_standard_downs: standardDownsAwayMatch ? parseFloat(standardDownsAwayMatch[1]) * 100 : 45.0,
        home_standard_downs: standardDownsHomeMatch ? parseFloat(standardDownsHomeMatch[1]) * 100 : 47.0
      }
    };
  };

  const { confidence, situationalPerformance } = parseFormattedAnalysis();

  // Use prediction data if available, otherwise fall back to generic data
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "", primary_color: "#6366f1", alt_color: "#4f46e5" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "", primary_color: "#10b981", alt_color: "#059669" };
  const awayProb = predictionData?.prediction_cards?.win_probability?.away_team_prob || 50.0;
  const homeProb = predictionData?.prediction_cards?.win_probability?.home_team_prob || 50.0;
  const favoredTeam = predictionData?.prediction_cards?.win_probability?.favored_team || awayTeam.name;
  
  // Generate abbreviations from team names with special handling
  const generateAbbr = (teamName: string) => {
    // Special cases for common team names
    const specialCases: { [key: string]: string } = {
      'USC': 'USC',
      'UCLA': 'UCLA',
      'TCU': 'TCU',
      'SMU': 'SMU',
      'BYU': 'BYU',
      'LSU': 'LSU',
      'ECU': 'ECU',
      'UCF': 'UCF',
      'Notre Dame': 'ND',
      'Texas A&M': 'A&M',
      'Virginia Tech': 'VT',
      'Georgia Tech': 'GT',
      'Florida State': 'FSU',
      'Arizona State': 'ASU',
      'Michigan State': 'MSU',
      'Ohio State': 'OSU',
      'Penn State': 'PSU',
      'Oklahoma State': 'OKST',
      'Iowa State': 'ISU',
      'Kansas State': 'KSU',
      'Mississippi State': 'MSST',
      'South Carolina': 'SC',
      'North Carolina': 'UNC',
      'NC State': 'NCST'
    };

    if (specialCases[teamName]) {
      return specialCases[teamName];
    }

    // For other teams, use first letter of each word, max 4 characters
    return teamName.split(' ').map((word: string) => word.charAt(0)).join('').substring(0, 4);
  };

  const awayAbbr = generateAbbr(awayTeam.name);
  const homeAbbr = generateAbbr(homeTeam.name);

  // Dynamic win probability data for pie chart
  const winProbData = [
    { name: awayTeam.name, value: awayProb, color: awayTeam.primary_color || '#6366f1' },
    { name: homeTeam.name, value: homeProb, color: homeTeam.primary_color || '#10b981' }
  ];

  // Dynamic situational performance data
  const situationalPerformanceData = [
    { 
      metric: 'Success Rate', 
      [awayAbbr]: 46.0, 
      [homeAbbr]: 48.0, 
      Elite: 50, 
      Average: 42.5, 
      BelowAvg: 39 
    },
    { 
      metric: 'Explosiveness', 
      [awayAbbr]: 15.0, 
      [homeAbbr]: 13.0, 
      Elite: 17, 
      Average: 13, 
      BelowAvg: 10.5 
    },
    { 
      metric: 'Passing Downs', 
      [awayAbbr]: situationalPerformance.away_passing_downs, 
      [homeAbbr]: situationalPerformance.home_passing_downs, 
      Elite: 41, 
      Average: 34.5, 
      BelowAvg: 31 
    },
    { 
      metric: 'Standard Downs', 
      [awayAbbr]: situationalPerformance.away_standard_downs, 
      [homeAbbr]: situationalPerformance.home_standard_downs, 
      Elite: 56.5, 
      Average: 49, 
      BelowAvg: 44 
    },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Win Probability Chart */}
      <div className="relative overflow-visible rounded-xl bg-[#252b36] border border-[#3a4252] p-6">
        <div className="flex items-center gap-2 mb-6">
          <svg className="w-5 h-5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
          <h3 className="text-white font-semibold">Win Probability</h3>
        </div>

        {/* Probability Cards */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div 
            className="relative overflow-hidden rounded-lg p-4 border bg-gradient-to-br" 
            style={{ 
              borderColor: `${awayTeam.primary_color}30`,
              background: `linear-gradient(to bottom right, ${awayTeam.primary_color}15, ${awayTeam.primary_color}05)`
            }}
          >
            <div className="flex items-center gap-2 mb-2">
              <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-8 h-8 object-contain" />
              <div className="flex-1">
                <div className="font-semibold text-xs" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</div>
                <div className="text-gray-400 text-[10px]">Away</div>
              </div>
            </div>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="font-bold text-3xl font-mono" style={{ color: awayTeam.primary_color }}>{awayProb.toFixed(1)}</span>
              <span className="text-lg" style={{ color: awayTeam.primary_color }}>%</span>
            </div>
            <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full" 
                style={{ 
                  width: `${awayProb}%`,
                  background: `linear-gradient(to right, ${awayTeam.primary_color}, ${awayTeam.primary_color})`
                }}
              ></div>
            </div>
          </div>

          <div 
            className="relative overflow-hidden rounded-lg p-4 border bg-gradient-to-br"
            style={{ 
              borderColor: `${homeTeam.primary_color}30`,
              background: `linear-gradient(to bottom right, ${homeTeam.primary_color}15, ${homeTeam.primary_color}05)`
            }}
          >
            <div className="flex items-center gap-2 mb-2">
              <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-8 h-8 object-contain" />
              <div className="flex-1">
                <div className="font-semibold text-xs" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</div>
                <div className="text-gray-400 text-[10px]">Home</div>
              </div>
            </div>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="font-bold text-3xl font-mono" style={{ color: homeTeam.primary_color }}>{homeProb.toFixed(1)}</span>
              <span className="text-lg" style={{ color: homeTeam.primary_color }}>%</span>
            </div>
            <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full" 
                style={{ 
                  width: `${homeProb}%`,
                  background: `linear-gradient(to right, ${homeTeam.primary_color}, ${homeTeam.primary_color})`
                }}
              ></div>
            </div>
          </div>
        </div>

        {/* Pie Chart - Bigger and Wider */}
        <div className="relative" style={{ height: '380px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={winProbData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={160}
                innerRadius={105}
                fill="#8884d8"
                dataKey="value"
                strokeWidth={0}
              >
                {winProbData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          {/* Center Logo - Favored Team */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="relative">
              {favoredTeam === awayTeam.name ? (
                <>
                  <ImageWithFallback 
                    src={awayTeam.logo} 
                    alt="Favorite" 
                    className="w-24 h-24 object-contain"
                  />
                  <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 backdrop-blur-sm border rounded-full px-4 py-1.5"
                       style={{ 
                         backgroundColor: `${awayTeam.primary_color}20`, 
                         borderColor: `${awayTeam.primary_color}40` 
                       }}>
                    <span className="font-bold text-sm whitespace-nowrap" style={{ color: awayTeam.primary_color }}>Favorite</span>
                  </div>
                </>
              ) : (
                <>
                  <ImageWithFallback 
                    src={homeTeam.logo} 
                    alt="Favorite" 
                    className="w-24 h-24 object-contain"
                  />
                  <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 backdrop-blur-sm border rounded-full px-4 py-1.5"
                       style={{ 
                         backgroundColor: `${homeTeam.primary_color}20`, 
                         borderColor: `${homeTeam.primary_color}40` 
                       }}>
                    <span className="font-bold text-sm whitespace-nowrap" style={{ color: homeTeam.primary_color }}>Favorite</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Model Confidence - Dynamic */}
        <div className="mt-6 p-4 bg-gradient-to-r from-emerald-500/10 via-transparent to-emerald-500/10 rounded-lg border border-emerald-500/20">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span className="text-gray-300 text-sm font-semibold">Model Confidence</span>
            </div>
            <div className="flex items-baseline gap-1">
              <span className="text-emerald-400 font-bold text-2xl font-mono">{confidence.toFixed(1)}</span>
              <span className="text-emerald-400 text-base">%</span>
            </div>
          </div>
          <div className="text-xs text-gray-400">
            {confidence >= 90 ? 'Very high' : confidence >= 80 ? 'High' : confidence >= 70 ? 'Moderate' : 'Low'} confidence prediction based on comprehensive analysis
          </div>
        </div>
      </div>

      {/* Situational Performance Chart */}
      <div className="relative overflow-hidden rounded-xl bg-[#252b36] border border-[#3a4252] p-6">
        <div className="flex items-center gap-2 mb-6">
          <svg className="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
          <h3 className="text-white font-semibold">Situational Performance</h3>
        </div>
        
        {/* Performance Indicators */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-6">
          {situationalPerformanceData.map((data) => {
            const awayValue = Number(data[awayAbbr]) || 0;
            const homeValue = Number(data[homeAbbr]) || 0;
            const winner = awayValue > homeValue ? awayAbbr : homeAbbr;
            return (
              <PerformanceCard 
                key={data.metric}
                title={data.metric} 
                awayValue={`${awayValue.toFixed(1)}%`} 
                homeValue={`${homeValue.toFixed(1)}%`} 
                winner={winner}
                awayTeam={awayTeam}
                homeTeam={homeTeam}
                awayAbbr={awayAbbr}
                homeAbbr={homeAbbr}
              />
            );
          })}
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-4 mb-4 flex-wrap">
          <div className="flex items-center gap-2 px-2 py-1 bg-[#2a3140] rounded border" style={{ borderColor: `${awayTeam.primary_color}30` }}>
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-4 h-4 object-contain" />
            <span className="font-bold text-[10px]" style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
          </div>
          <div className="flex items-center gap-2 px-2 py-1 bg-[#2a3140] rounded border" style={{ borderColor: `${homeTeam.primary_color}30` }}>
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-4 h-4 object-contain" />
            <span className="font-bold text-[10px]" style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
          </div>
          <div className="h-4 w-px bg-[#3a4252]"></div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-emerald-500" style={{ borderTop: '2px dashed rgba(16, 185, 129, 0.7)' }}></div>
            <span className="text-emerald-400 text-[10px] font-semibold">Elite</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-amber-500" style={{ borderTop: '2px dashed rgba(245, 158, 11, 0.7)' }}></div>
            <span className="text-amber-400 text-[10px] font-semibold">Average</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-red-500" style={{ borderTop: '2px dashed rgba(239, 68, 68, 0.6)' }}></div>
            <span className="text-red-400 text-[10px] font-semibold">Below Avg</span>
          </div>
        </div>

        {/* Enhanced Line Chart - Mirroring Chart.js Version */}
        <div style={{ height: '380px', width: '100%', position: 'relative', boxShadow: '0px 4px 15px rgba(0, 0, 0, 0.3)', borderRadius: '12px', background: 'rgba(37, 43, 54, 0.5)', backdropFilter: 'blur(10px)', padding: '15px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart 
              data={situationalPerformanceData} 
              margin={{ top: 10, right: 10, left: 5, bottom: 10 }}
            >
              {/* Grid with subtle styling */}
              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="rgba(255, 255, 255, 0.08)" 
                strokeWidth={1}
              />
              
              {/* X-Axis Configuration */}
              <XAxis 
                dataKey="metric" 
                tick={{ 
                  fill: '#94a3b8', 
                  fontSize: 9,
                  fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
                  fontWeight: 600
                }}
                axisLine={false}
                tickLine={false}
                interval={0}
                angle={0}
                textAnchor="middle"
                height={40}
              />
              
              {/* Y-Axis Configuration */}
              <YAxis 
                domain={[0, 100]}
                ticks={[0, 20, 40, 60, 80, 100]}
                tick={{ 
                  fill: '#94a3b8', 
                  fontSize: 9,
                  fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
                  fontWeight: 600
                }}
                tickFormatter={(value) => `${value}%`}
                axisLine={false}
                tickLine={false}
                width={40}
              />
              
              {/* Custom Tooltip */}
              <Tooltip content={<CustomTooltip awayTeam={awayTeam} homeTeam={homeTeam} awayAbbr={awayAbbr} homeAbbr={homeAbbr} />} />
              
              {/* Reference Lines - Thresholds with Apple-style shadows */}
              <ReferenceLine 
                y={39} 
                stroke="rgba(239, 68, 68, 0.8)" 
                strokeDasharray="10 5" 
                strokeWidth={3}
                label={{ 
                  value: 'Below Avg', 
                  position: 'right',
                  fill: '#ef4444',
                  fontSize: 10,
                  fontWeight: 600
                }}
                style={{
                  filter: 'drop-shadow(0px 2px 4px rgba(239, 68, 68, 0.4))'
                }}
              />
              <ReferenceLine 
                y={42.5} 
                stroke="rgba(245, 158, 11, 0.9)" 
                strokeDasharray="10 5" 
                strokeWidth={3}
                label={{ 
                  value: 'League Avg', 
                  position: 'right',
                  fill: '#f59e0b',
                  fontSize: 10,
                  fontWeight: 600
                }}
                style={{
                  filter: 'drop-shadow(0px 2px 4px rgba(245, 158, 11, 0.5))'
                }}
              />
              <ReferenceLine 
                y={49} 
                stroke="rgba(16, 185, 129, 0.9)" 
                strokeDasharray="10 5" 
                strokeWidth={3}
                label={{ 
                  value: 'Elite', 
                  position: 'right',
                  fill: '#10b981',
                  fontSize: 10,
                  fontWeight: 600
                }}
                style={{
                  filter: 'drop-shadow(0px 2px 4px rgba(16, 185, 129, 0.5))'
                }}
              />
              
              {/* Team Lines with Enhanced Styling and Logo Dots */}
              <Line 
                type="monotone" 
                dataKey={awayAbbr} 
                stroke={awayTeam.primary_color || '#6366f1'} 
                strokeWidth={5} 
                dot={<CustomDot awayTeam={awayTeam} homeTeam={homeTeam} awayAbbr={awayAbbr} homeAbbr={homeAbbr} />}
                fill={`${awayTeam.primary_color || '#6366f1'}10`}
                fillOpacity={1}
                activeDot={false}
                style={{
                  filter: `drop-shadow(0px 8px 20px ${awayTeam.primary_color || '#6366f1'}80)`
                }}
                isAnimationActive={true}
              />
              <Line 
                type="monotone" 
                dataKey={homeAbbr} 
                stroke={homeTeam.primary_color || '#10b981'} 
                strokeWidth={5} 
                dot={<CustomDot awayTeam={awayTeam} homeTeam={homeTeam} awayAbbr={awayAbbr} homeAbbr={homeAbbr} />}
                fill={`${homeTeam.primary_color || '#10b981'}10`}
                fillOpacity={1}
                activeDot={false}
                style={{
                  filter: `drop-shadow(0px 8px 20px ${homeTeam.primary_color || '#10b981'}80)`
                }}
                isAnimationActive={true}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Edge Summary */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          {/* Away Team Edges */}
          <div className="flex items-start gap-2 p-4 rounded-lg border" style={{ 
            background: `linear-gradient(to right, ${awayTeam.primary_color}10, transparent)`,
            borderColor: `${awayTeam.primary_color}20`
          }}>
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-6 h-6 object-contain" />
            <div className="flex-1">
              <div className="font-semibold text-sm mb-2" style={{ color: awayTeam.primary_color }}>
                {awayTeam.name} Edge
              </div>
              <div className="text-gray-400 text-xs">
                {situationalPerformanceData
                  .filter(d => d[awayAbbr] > d[homeAbbr])
                  .map(d => d.metric)
                  .join(', ') || 'None identified'}
              </div>
            </div>
          </div>
          
          {/* Home Team Edges */}
          <div className="flex items-start gap-2 p-4 rounded-lg border" style={{ 
            background: `linear-gradient(to left, ${homeTeam.primary_color}10, transparent)`,
            borderColor: `${homeTeam.primary_color}20`
          }}>
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-6 h-6 object-contain" />
            <div className="flex-1">
              <div className="font-semibold text-sm mb-2" style={{ color: homeTeam.primary_color }}>
                {homeTeam.name} Edge
              </div>
              <div className="text-gray-400 text-xs">
                {situationalPerformanceData
                  .filter(d => d[homeAbbr] > d[awayAbbr])
                  .map(d => d.metric)
                  .join(', ') || 'None identified'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function PerformanceCard({ 
  title, 
  awayValue, 
  homeValue, 
  winner, 
  awayTeam, 
  homeTeam,
  awayAbbr,
  homeAbbr
}: { 
  title: string; 
  awayValue: string; 
  homeValue: string; 
  winner: string; 
  awayTeam: any; 
  homeTeam: any; 
  awayAbbr: string;
  homeAbbr: string;
}) {
  const isAwayWinner = winner === awayAbbr;
  const winnerLogo = isAwayWinner ? awayTeam?.logo : homeTeam?.logo;
  const winnerColor = isAwayWinner ? awayTeam?.primary_color : homeTeam?.primary_color;
  
  return (
    <div className="bg-[#2a3140] rounded-lg p-3 border border-[#3a4252]">
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-400 text-[10px] font-semibold">{title}</span>
        <ImageWithFallback 
          src={winnerLogo || ''} 
          alt={winner} 
          className="w-6 h-6 object-contain drop-shadow-lg" 
          style={{
            filter: `drop-shadow(0 2px 6px ${winnerColor}99)`
          }}
        />
      </div>
      <div className="flex items-baseline gap-1.5 mb-1">
        <span className={`${isAwayWinner ? 'text-emerald-400 font-bold' : 'text-gray-300'} text-sm font-mono`}>{awayValue}</span>
        <span className="text-gray-500 text-[10px]">vs</span>
        <span className={`${!isAwayWinner ? 'text-emerald-400 font-bold' : 'text-gray-300'} text-sm font-mono`}>{homeValue}</span>
      </div>
      <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
        <div 
          className="h-full rounded-full bg-gradient-to-r" 
          style={{ 
            width: '95%',
            backgroundImage: isAwayWinner 
              ? `linear-gradient(to right, ${awayTeam?.primary_color}, ${homeTeam?.primary_color}60)` 
              : `linear-gradient(to right, ${awayTeam?.primary_color}60, ${homeTeam?.primary_color})`
          }}
        ></div>
      </div>
    </div>
  );
}
