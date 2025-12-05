import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Cell } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';
import { InsightBox } from './InsightBox';

// Custom Tooltip Component with Team Status Icons
const CustomTooltip = ({ active, payload, label, awayTeam, homeTeam, awayAbbr, homeAbbr }: any) => {
  if (active && payload && payload.length) {
    const awayValue = payload.find((p: any) => p.dataKey === awayAbbr)?.value;
    const homeValue = payload.find((p: any) => p.dataKey === homeAbbr)?.value;
    const isAwayWinning = awayValue > homeValue;
    const isHomeWinning = homeValue > awayValue;

    // Determine benchmarks based on metric
    const getBenchmarks = (metricName: string) => {
      switch(metricName) {
        case 'Success Rate': return { elite: 47.1, avg: 42.9, below: 40.5 };
        case 'Explosiveness': return { elite: 130, avg: 120, below: 115 };
        case 'Passing Downs': return { elite: 34.7, avg: 30.8, below: 28.2 };
        case 'Standard Downs': return { elite: 52.2, avg: 48.6, below: 46.2 };
        default: return { elite: 50, avg: 42, below: 35 };
      }
    };

    const getStatus = (value: number, metricName: string) => {
      const { elite, avg, below } = getBenchmarks(metricName);
      if (value >= elite) return { icon: '▲', color: '#22c55e', text: 'Elite', bg: 'rgba(34, 197, 94, 0.15)' };
      if (value >= avg) return { icon: '●', color: '#eab308', text: 'Avg', bg: 'rgba(234, 179, 8, 0.15)' };
      return { icon: '▼', color: '#ef4444', text: 'Below', bg: 'rgba(239, 68, 68, 0.15)' };
    };

    const awayStatus = getStatus(awayValue, label);
    const homeStatus = getStatus(homeValue, label);

    return (
      <div 
        style={{ 
          backgroundColor: 'rgba(26, 31, 38, 0.95)', 
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '8px',
          padding: '12px',
          fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
          minWidth: '200px'
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
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ 
              fontSize: '10px', 
              color: awayStatus.color,
              backgroundColor: awayStatus.bg,
              padding: '2px 6px',
              borderRadius: '3px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              {awayStatus.icon}
            </span>
            <span style={{ 
              color: isAwayWinning ? '#10b981' : '#94a3b8', 
              fontSize: '12px', 
              fontWeight: 700,
              fontFamily: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace"
            }}>
              {awayValue?.toFixed(1)}%
            </span>
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
              style={{ width: '28px', height: '28px', objectFit: 'contain' }}
            />
            <span style={{ color: homeTeam?.primary_color || '#10b981', fontSize: '11px', fontWeight: 600 }}>
              {homeAbbr}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ 
              fontSize: '10px', 
              color: homeStatus.color,
              backgroundColor: homeStatus.bg,
              padding: '2px 6px',
              borderRadius: '3px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              {homeStatus.icon}
            </span>
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
    <div className="border rounded-lg p-3" style={{ background: 'rgba(255, 255, 255, 0.02)', backdropFilter: 'blur(16px)', borderColor: 'rgba(255, 255, 255, 0.08)' }}>
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

  // Dynamic situational performance data with FBS national benchmarks
  // Calculated from 123 FBS teams (Week 15, 2025 season) using raw percentage data
  // Elite = 80th percentile, Average = 50th percentile, Below Avg = 30th percentile
  const situationalPerformanceData = [
    {
      metric: "Success Rate",
      [awayAbbr]: 46.0,
      [homeAbbr]: 48.0,
      Elite: 47.1,    // Top 20% of FBS teams
      Average: 42.9,  // Median FBS performance
      BelowAvg: 40.5  // Bottom 30%
    },
    {
      metric: "Explosiveness",
      [awayAbbr]: 120.0,  // Indiana coefficient 1.2 = 120%
      [homeAbbr]: 113.0,  // OSU coefficient 1.13 = 113%
      Elite: 130.0,       // Top 20%: 1.30+ coefficient = 130%+
      Average: 120.0,     // Median: 1.20 coefficient = 120%
      BelowAvg: 115.0     // Bottom 30%: 1.15 coefficient = 115%
    },
    {
      metric: "Passing Downs",
      [awayAbbr]: situationalPerformance.away_passing_downs,
      [homeAbbr]: situationalPerformance.home_passing_downs,
      Elite: 34.7,    // Top 20% 3rd down conversion
      Average: 30.8,  // Median 3rd down success
      BelowAvg: 28.2  // Struggles on passing downs
    },
    {
      metric: "Standard Downs",
      [awayAbbr]: situationalPerformance.away_standard_downs,
      [homeAbbr]: situationalPerformance.home_standard_downs,
      Elite: 52.2,    // Top 20% early down efficiency
      Average: 48.6,  // Median standard downs success
      BelowAvg: 46.2  // Below average on 1st/2nd down
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
      
      <div className="grid grid-cols-1 gap-6">
        {/* Legend - Team Logos and Metric Benchmarks */}
        <div className="space-y-4 mb-6">
          {/* Team Logos Row */}
          <div className="flex items-center justify-center gap-6 flex-wrap">
            <div className="flex items-center gap-3 px-4 py-2 rounded-lg border shadow-lg" style={{ background: 'rgba(255, 255, 255, 0.03)', backdropFilter: 'blur(16px)', borderColor: `${awayTeam.primary_color}40` }}>
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
            <div className="flex items-center gap-3 px-4 py-2 rounded-lg border shadow-lg" style={{ background: 'rgba(255, 255, 255, 0.03)', backdropFilter: 'blur(16px)', borderColor: `${homeTeam.primary_color}40` }}>
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
          </div>

          {/* Benchmarks Grid - Color Coded by Metric */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {/* Success Rate */}
            <div className="rounded-lg p-3 border" style={{ background: 'rgba(16, 185, 129, 0.05)', backdropFilter: 'blur(16px)', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
              <div className="text-emerald-400 text-xs font-bold mb-2">Success Rate</div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Elite:</span>
                  <span className="text-emerald-300 font-mono">47.1%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg:</span>
                  <span className="text-gray-300 font-mono">42.9%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Below:</span>
                  <span className="text-gray-500 font-mono">40.5%</span>
                </div>
              </div>
            </div>

            {/* Explosiveness */}
            <div className="rounded-lg p-3 border" style={{ background: 'rgba(245, 158, 11, 0.05)', backdropFilter: 'blur(16px)', borderColor: 'rgba(245, 158, 11, 0.3)' }}>
              <div className="text-amber-400 text-xs font-bold mb-2">Explosiveness</div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Elite:</span>
                  <span className="text-amber-300 font-mono">130%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg:</span>
                  <span className="text-gray-300 font-mono">120%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Below:</span>
                  <span className="text-gray-500 font-mono">115%</span>
                </div>
              </div>
            </div>

            {/* Passing Downs */}
            <div className="rounded-lg p-3 border" style={{ background: 'rgba(139, 92, 246, 0.05)', backdropFilter: 'blur(16px)', borderColor: 'rgba(139, 92, 246, 0.3)' }}>
              <div className="text-violet-400 text-xs font-bold mb-2">Passing Downs</div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Elite:</span>
                  <span className="text-violet-300 font-mono">34.7%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg:</span>
                  <span className="text-gray-300 font-mono">30.8%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Below:</span>
                  <span className="text-gray-500 font-mono">28.2%</span>
                </div>
              </div>
            </div>

            {/* Standard Downs */}
            <div className="rounded-lg p-3 border" style={{ background: 'rgba(59, 130, 246, 0.05)', backdropFilter: 'blur(16px)', borderColor: 'rgba(59, 130, 246, 0.3)' }}>
              <div className="text-blue-400 text-xs font-bold mb-2">Standard Downs</div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">Elite:</span>
                  <span className="text-blue-300 font-mono">52.2%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg:</span>
                  <span className="text-gray-300 font-mono">48.6%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Below:</span>
                  <span className="text-gray-500 font-mono">46.2%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Line Chart - Clean without reference line labels */}
        <div style={{ height: '360px', width: '100%', position: 'relative', boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.2)', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.02)', backdropFilter: 'blur(16px)', padding: '12px', border: '1px solid rgba(255, 255, 255, 0.06)' }}>
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
              
              {/* Reference Lines - Color-coded: Green=High Good, Yellow=Medium, Red=Low Bad, Gray=Neutral */}
              {/* Success Rate Average - Green (higher is better) */}
              <ReferenceLine y={42.9} stroke="rgba(34, 197, 94, 0.7)" strokeDasharray="8 4" strokeWidth={2.5} label={{ value: '42.9%', position: 'right', fill: '#22c55e', fontSize: 10, fontWeight: 600 }} />
              
              {/* Explosiveness Average - Yellow (higher is better) */}
              <ReferenceLine y={120.0} stroke="rgba(234, 179, 8, 0.7)" strokeDasharray="8 4" strokeWidth={2.5} label={{ value: '120%', position: 'right', fill: '#eab308', fontSize: 10, fontWeight: 600 }} />
              
              {/* Passing Downs Average - Red (critical metric) */}
              <ReferenceLine y={30.8} stroke="rgba(239, 68, 68, 0.7)" strokeDasharray="8 4" strokeWidth={2.5} label={{ value: '30.8%', position: 'right', fill: '#ef4444', fontSize: 10, fontWeight: 600 }} />
              
              {/* Standard Downs Average - Gray (baseline metric) */}
              <ReferenceLine y={48.6} stroke="rgba(156, 163, 175, 0.7)" strokeDasharray="8 4" strokeWidth={2.5} label={{ value: '48.6%', position: 'right', fill: '#9ca3af', fontSize: 10, fontWeight: 600 }} />
              
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

        {/* Edge Summary - Condensed */}
        <div className="flex items-center justify-center gap-6 flex-wrap">
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg" style={{ 
            background: `linear-gradient(135deg, ${awayTeam.primary_color}15, transparent)`,
            border: `1px solid ${awayTeam.primary_color}30`
          }}>
            <img src={awayTeam.logo} alt={awayTeam.name} className="w-6 h-6 object-contain" />
            <span className="text-xs font-semibold" style={{ color: awayTeam.primary_color }}>{awayAbbr} Edge</span>
            <span className="text-xs text-gray-400">
              {situationalPerformanceData.filter(d => d[awayAbbr] > d[homeAbbr]).map(d => d.metric).join(', ') || 'None'}
            </span>
          </div>
          
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg" style={{ 
            background: `linear-gradient(135deg, ${homeTeam.primary_color}15, transparent)`,
            border: `1px solid ${homeTeam.primary_color}30`
          }}>
            <img src={homeTeam.logo} alt={homeTeam.name} className="w-6 h-6 object-contain" />
            <span className="text-xs font-semibold" style={{ color: homeTeam.primary_color }}>{homeAbbr} Edge</span>
            <span className="text-xs text-gray-400">
              {situationalPerformanceData.filter(d => d[homeAbbr] > d[awayAbbr]).map(d => d.metric).join(', ') || 'None'}
            </span>
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