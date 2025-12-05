import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Cell } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';
import { InsightBox } from './InsightBox';

// Custom Tooltip Component with Team Logos (same as original)
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
              style={{ width: '28px', height: '28px', objectFit: 'contain' }}
            />
            <span style={{ color: awayTeam?.primary_color || '#6366f1', fontSize: '11px', fontWeight: 600 }}>
              {awayAbbr}
            </span>
          </div>
          <span style={{ 
            color: isAwayWinning ? '#10b981' : '#94a3b8', 
            fontSize: '12px', 
            fontWeight: 700,
            fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace"
          }}>
            {awayValue?.toFixed(1)}%
          </span>
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
              style={{ width: '28px', height: '28px', objectFit: 'contain' }}
            />
            <span style={{ color: homeTeam?.primary_color || '#10b981', fontSize: '11px', fontWeight: 600 }}>
              {homeAbbr}
            </span>
          </div>
          <span style={{ 
            color: isHomeWinning ? '#10b981' : '#94a3b8', 
            fontSize: '12px', 
            fontWeight: 700,
            fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace"
          }}>
            {homeValue?.toFixed(1)}%
          </span>
        </div>
      </div>
    );
  }
  return null;
};

// Custom Dot Component - Logos positioned precisely on line data points
const CustomDot = (props: any) => {
  const { cx, cy, payload, dataKey, awayTeam, homeTeam, awayAbbr, homeAbbr } = props;
  
  if (!payload || typeof cx !== 'number' || typeof cy !== 'number') return null;
  
  const awayValue = payload[awayAbbr];
  const homeValue = payload[homeAbbr];
  
  // Determine which team has the upper hand
  if (awayValue === undefined || homeValue === undefined) return null;
  
  const awayHasUpperHand = awayValue > homeValue;
  const homeHasUpperHand = homeValue > awayValue;
  
  // Only show logo if this is the winning team's line
  let shouldShowLogo = false;
  let team = null;
  
  if (awayHasUpperHand && dataKey === awayAbbr) {
    shouldShowLogo = true;
    team = awayTeam;
  } else if (homeHasUpperHand && dataKey === homeAbbr) {
    shouldShowLogo = true;
    team = homeTeam;
  }
  
  // If it's not the winning team's line or no clear winner, don't show logo
  if (!shouldShowLogo || !team?.logo) return null;
  
  return (
    <image 
      x={cx - 18} 
      y={cy - 18} 
      width={36} 
      height={36} 
      href={team.logo}
      style={{ 
        filter: `drop-shadow(0px 3px 6px ${team.primary_color}80) drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.6))`,
        transform: 'perspective(100px) rotateX(5deg)',
        pointerEvents: 'none'
      }}
    />
  );
};

interface SituationalPerformanceProps {
  predictionData?: any;
}

// Performance Card Component
const PerformanceCard = ({ title, awayValue, homeValue, winner, awayTeam, homeTeam, awayAbbr, homeAbbr }: any) => {
  const isAwayWinner = winner === awayAbbr;
  const isHomeWinner = winner === homeAbbr;

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-3">
      <div className="text-xs text-gray-400 mb-2 font-medium">{title}</div>
      <div className="space-y-2">
        <div className={`flex items-center justify-between p-2 rounded ${isAwayWinner ? 'bg-emerald-900/30 border border-emerald-500/30' : 'bg-slate-700/30'}`}>
          <div className="flex items-center gap-2">
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-6 h-6 object-contain" />
            <span className="text-xs text-gray-300">{awayAbbr}</span>
          </div>
          <span className={`text-xs font-semibold ${isAwayWinner ? 'text-emerald-400' : 'text-gray-400'}`}>
            {awayValue}
          </span>
        </div>
        <div className={`flex items-center justify-between p-2 rounded ${isHomeWinner ? 'bg-emerald-900/30 border border-emerald-500/30' : 'bg-slate-700/30'}`}>
          <div className="flex items-center gap-2">
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-6 h-6 object-contain" />
            <span className="text-xs text-gray-300">{homeAbbr}</span>
          </div>
          <span className={`text-xs font-semibold ${isHomeWinner ? 'text-emerald-400' : 'text-gray-400'}`}>
            {homeValue}
          </span>
        </div>
      </div>
    </div>
  );
};

export function SituationalPerformance({ predictionData }: SituationalPerformanceProps) {
  if (!predictionData) {
    return (
      <GlassCard className="p-8">
        <div className="flex items-center gap-2 mb-6">
          <svg className="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
          <h3 className="text-white font-semibold text-lg">Situational Performance</h3>
        </div>
        <div className="text-gray-400 text-center py-8">
          Select teams to see situational performance analysis
        </div>
      </GlassCard>
    );
  }

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

  // Dynamic situational performance data with the correct structure
  const situationalPerformanceData = [
    {
      metric: "Success Rate",
      [awayAbbr]: 46.0,
      [homeAbbr]: 48.0,
      Elite: 50,
      Average: 42.5,
      BelowAvg: 39
    },
    {
      metric: "Explosiveness",
      [awayAbbr]: 15.0,
      [homeAbbr]: 13.0,
      Elite: 17,
      Average: 13,
      BelowAvg: 10.5
    },
    {
      metric: "Passing Downs",
      [awayAbbr]: situationalPerformance.away_passing_downs,
      [homeAbbr]: situationalPerformance.home_passing_downs,
      Elite: 41,
      Average: 34.5,
      BelowAvg: 31
    },
    {
      metric: "Standard Downs",
      [awayAbbr]: situationalPerformance.away_standard_downs,
      [homeAbbr]: situationalPerformance.home_standard_downs,
      Elite: 56.5,
      Average: 49,
      BelowAvg: 44
    }
  ];

  // Radar chart data
  const radarData = situationalPerformanceData.map(item => ({
    metric: item.metric,
    [awayAbbr]: item[awayAbbr],
    [homeAbbr]: item[homeAbbr]
  }));

  return (
    <GlassCard className="p-8">
      <div className="flex items-center gap-2 mb-6">
        <svg className="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        <h3 className="text-white font-semibold text-lg">Situational Performance</h3>
      </div>
      
      <div className="grid grid-cols-1 gap-8">
        {/* Performance Indicators Grid */}
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

        {/* Legend - Floating without container */}
        <div className="flex items-center justify-center gap-6 mb-6 flex-wrap">
          <div className="flex items-center gap-3 px-4 py-2 bg-[#2a3140] rounded-lg border shadow-lg" style={{ borderColor: `${awayTeam.primary_color}40` }}>
            <div className="relative">
              <img 
                src={awayTeam.logo} 
                alt={awayTeam.name} 
                className="w-10 h-10 object-contain"
                style={{ 
                  filter: `drop-shadow(0px 4px 8px ${awayTeam.primary_color}60) drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.4))`,
                  transform: 'perspective(100px) rotateX(10deg) rotateY(-5deg)'
                }}
              />
            </div>
            <span className="font-bold text-sm" style={{ color: awayTeam.primary_color }}>{awayAbbr}</span>
          </div>
          <div className="flex items-center gap-3 px-4 py-2 bg-[#2a3140] rounded-lg border shadow-lg" style={{ borderColor: `${homeTeam.primary_color}40` }}>
            <div className="relative">
              <img 
                src={homeTeam.logo} 
                alt={homeTeam.name} 
                className="w-10 h-10 object-contain"
                style={{ 
                  filter: `drop-shadow(0px 4px 8px ${homeTeam.primary_color}60) drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.4))`,
                  transform: 'perspective(100px) rotateX(10deg) rotateY(5deg)'
                }}
              />
            </div>
            <span className="font-bold text-sm" style={{ color: homeTeam.primary_color }}>{homeAbbr}</span>
          </div>
          <div className="h-8 w-px bg-[#3a4252]"></div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-1 bg-emerald-500 rounded-full" style={{ borderTop: '3px dashed rgba(16, 185, 129, 0.8)' }}></div>
            <span className="text-emerald-400 text-sm font-bold tracking-wide">Elite</span>
            <span className="text-emerald-300 text-xs ml-1">(49%+)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-1 bg-amber-500 rounded-full" style={{ borderTop: '3px dashed rgba(245, 158, 11, 0.8)' }}></div>
            <span className="text-amber-400 text-sm font-bold tracking-wide">Average</span>
            <span className="text-amber-300 text-xs ml-1">(42.5%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-1 bg-red-500 rounded-full" style={{ borderTop: '3px dashed rgba(239, 68, 68, 0.7)' }}></div>
            <span className="text-red-400 text-sm font-bold tracking-wide">Below Avg</span>
            <span className="text-red-300 text-xs ml-1">(39%)</span>
          </div>
        </div>

        {/* Enhanced Line Chart - Clean without reference line labels */}
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
              
              {/* Reference Lines - Thicker and more visible */}
              <ReferenceLine 
                y={39} 
                stroke="rgba(239, 68, 68, 0.8)" 
                strokeDasharray="8 4" 
                strokeWidth={3}
              />
              <ReferenceLine 
                y={42.5} 
                stroke="rgba(245, 158, 11, 0.9)" 
                strokeDasharray="8 4" 
                strokeWidth={3}
              />
              <ReferenceLine 
                y={49} 
                stroke="rgba(16, 185, 129, 0.8)" 
                strokeDasharray="8 4" 
                strokeWidth={3}
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

        {/* Edge Summary - Enhanced with 3D logos */}
        <div className="grid grid-cols-2 gap-3">
          {/* Away Team Edges */}
          <div className="flex items-start gap-3 p-4 rounded-lg border" style={{ 
            background: `linear-gradient(to right, ${awayTeam.primary_color}10, transparent)`,
            borderColor: `${awayTeam.primary_color}20`
          }}>
            <div className="relative">
              <img 
                src={awayTeam.logo} 
                alt={awayTeam.name} 
                className="w-8 h-8 object-contain"
                style={{ 
                  filter: `drop-shadow(0px 4px 8px ${awayTeam.primary_color}60) drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.4)) drop-shadow(0px 1px 2px rgba(255, 255, 255, 0.2))`,
                  transform: 'perspective(150px) rotateX(12deg) rotateY(-8deg) translateZ(5px)'
                }}
              />
            </div>
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
          <div className="flex items-start gap-3 p-4 rounded-lg border" style={{ 
            background: `linear-gradient(to left, ${homeTeam.primary_color}10, transparent)`,
            borderColor: `${homeTeam.primary_color}20`
          }}>
            <div className="relative">
              <img 
                src={homeTeam.logo} 
                alt={homeTeam.name} 
                className="w-8 h-8 object-contain"
                style={{ 
                  filter: `drop-shadow(0px 4px 8px ${homeTeam.primary_color}60) drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.4)) drop-shadow(0px 1px 2px rgba(255, 255, 255, 0.2))`,
                  transform: 'perspective(150px) rotateX(12deg) rotateY(8deg) translateZ(5px)'
                }}
              />
            </div>
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

      {/* Insight Box */}
      <InsightBox
        whatItMeans="Situational performance shows how teams perform in critical moments: 3rd downs (sustaining drives), red zone (scoring TDs vs FGs), and goal-to-go (punch-it-in ability). These situations determine game outcomes more than total yardage."
        whyItMatters="Teams that convert 3rd downs control the clock and wear down defenses. Red zone efficiency (50%+ TD rate) is the difference between 28-point and 21-point performances. Goal-to-go success rate predicts short-yardage dominance."
        whoHasEdge={{
          team: situationalPerformanceData.reduce((max, curr) => 
            (curr[awayAbbr] > curr[homeAbbr] ? awayAbbr : homeAbbr) === awayAbbr ? awayTeam.name : homeTeam.name
          , awayTeam.name),
          reason: `${awayTeam.name} shows ${situationalPerformanceData.filter(d => d[awayAbbr] > d[homeAbbr]).length} category advantages vs ${homeTeam.name}'s ${situationalPerformanceData.filter(d => d[homeAbbr] > d[awayAbbr]).length}. Biggest gap: ${Math.max(...situationalPerformanceData.map(d => Math.abs(d[awayAbbr] - d[homeAbbr]))).toFixed(1)}% in ${situationalPerformanceData.find(d => Math.abs(d[awayAbbr] - d[homeAbbr]) === Math.max(...situationalPerformanceData.map(m => Math.abs(m[awayAbbr] - m[homeAbbr]))))?.metric || 'key metric'}.`,
          magnitude: situationalPerformanceData.filter(d => Math.abs(d[awayAbbr] - d[homeAbbr]) > 15).length > 1 ? 'major' : 
                     situationalPerformanceData.filter(d => Math.abs(d[awayAbbr] - d[homeAbbr]) > 10).length > 0 ? 'significant' : 
                     situationalPerformanceData.filter(d => Math.abs(d[awayAbbr] - d[homeAbbr]) > 5).length > 0 ? 'moderate' : 'small'
        }}
        keyDifferences={[
          `Success Rate: ${situationalPerformanceData[0][awayAbbr].toFixed(1)}% vs ${situationalPerformanceData[0][homeAbbr].toFixed(1)}% (${Math.abs(situationalPerformanceData[0][awayAbbr] - situationalPerformanceData[0][homeAbbr]).toFixed(1)}% gap)`,
          `Explosiveness: ${situationalPerformanceData[1][awayAbbr].toFixed(1)}% vs ${situationalPerformanceData[1][homeAbbr].toFixed(1)}% (${Math.abs(situationalPerformanceData[1][awayAbbr] - situationalPerformanceData[1][homeAbbr]).toFixed(1)}% gap)`,
          `Passing Downs: ${situationalPerformanceData[2][awayAbbr].toFixed(1)}% vs ${situationalPerformanceData[2][homeAbbr].toFixed(1)}% (critical 3rd down conversion)`
        ]}
      />
    </GlassCard>
  );
}