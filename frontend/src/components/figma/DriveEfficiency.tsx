import React from 'react';
import { GlassCard } from './GlassCard';
import { Zap, Target, TrendingUp, Clock, CheckCircle, BarChart3 } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { extractSection } from '../../utils/teamUtils';

interface DriveEfficiencyProps {
  team1Data?: any;
  team2Data?: any;
  predictionData?: any;
}

// Mock data for demonstration
const mockQuarterData = {
  team1: [
    { quarter: '1st', drives: 9, scoringPct: 89, avgYards: 72.7 },
    { quarter: '2nd', drives: 5, scoringPct: 100, avgYards: 74.4 },
    { quarter: '3rd', drives: 10, scoringPct: 100, avgYards: 68.1 },
    { quarter: '4th', drives: 3, scoringPct: 100, avgYards: 73.3 }
  ],
  team2: [
    { quarter: '1st', drives: 8, scoringPct: 100, avgYards: 65.1 },
    { quarter: '2nd', drives: 8, scoringPct: 88, avgYards: 68.4 },
    { quarter: '3rd', drives: 11, scoringPct: 91, avgYards: 65.3 },
    { quarter: '4th', drives: 7, scoringPct: 71, avgYards: 69.4 }
  ]
};

const mockFieldPositionData = {
  team1: [
    { zone: 'Own 1-20', drives: 1, scoringPct: 100.0 },
    { zone: 'Own 21-40', drives: 12, scoringPct: 41.7 },
    { zone: 'Own 41-Mid', drives: 3, scoringPct: 66.7 },
    { zone: 'Opp Territory', drives: 45, scoringPct: 57.8 }
  ],
  team2: [
    { zone: 'Own 1-20', drives: 6, scoringPct: 50.0 },
    { zone: 'Own 21-40', drives: 28, scoringPct: 46.4 },
    { zone: 'Own 41-Mid', drives: 1, scoringPct: 100.0 },
    { zone: 'Opp Territory', drives: 44, scoringPct: 54.5 }
  ]
};

const mockDriveOutcomes = {
  team1: { touchdowns: 50.9, fieldGoals: 10.9, punts: 25.5, turnovers: 5.5, totalScoring: 61.8 },
  team2: { touchdowns: 39.4, fieldGoals: 15.5, punts: 29.6, turnovers: 9.9, totalScoring: 54.9 }
};

// Ultra-Dynamic Octagonal Multi-Team Spider Chart with 3D Elements
const MultiTeamSpiderChart = ({ 
  team1Data, 
  team2Data, 
  team1Color, 
  team2Color, 
  team1Label, 
  team2Label,
  team1Logo,
  team2Logo,
  categories 
}: { 
  team1Data: number[], 
  team2Data: number[], 
  team1Color: string, 
  team2Color: string, 
  team1Label: string,
  team2Label: string,
  team1Logo: string,
  team2Logo: string,
  categories: string[]
}) => {
  const size = 520; // Wider chart that fits in card
  const center = size / 2;
  const radius = 170; // Larger radius to use more card space
  
  // Create octagonal structure (8 points)
  const octagonPoints = 8;
  const angleStep = (2 * Math.PI) / octagonPoints;
  
  // Map quarters to octagon positions (spread across 8 points)
  const quarterPositions = [0, 2, 4, 6]; // Q1, Q2, Q3, Q4 at primary positions
  
  // Tooltip state with benchmarks
  const [tooltip, setTooltip] = React.useState<{
    visible: boolean;
    x: number;
    y: number;
    quarter: string;
    quarterIndex: number;
    benchmarks: {
      elite: number;
      average: number;
      poor: number;
    };
  }>({
    visible: false,
    x: 0,
    y: 0,
    quarter: '',
    quarterIndex: 0,
    benchmarks: { elite: 0, average: 0, poor: 0 }
  });

  // College football quarter benchmarks
  const quarterBenchmarks = {
    'Q1': { elite: 75, average: 62, poor: 48 },
    'Q2': { elite: 85, average: 72, poor: 58 },
    'Q3': { elite: 78, average: 65, poor: 52 },
    'Q4': { elite: 88, average: 75, poor: 62 }
  };
  
  // Tooltip functions
  const showTooltip = (e: React.MouseEvent, quarter: string, quarterIndex: number) => {
    const benchmarks = quarterBenchmarks[quarter as keyof typeof quarterBenchmarks];
    setTooltip({
      visible: true,
      x: e.clientX,
      y: e.clientY - 10,
      quarter,
      quarterIndex,
      benchmarks
    });
  };
  
  const hideTooltip = () => {
    setTooltip(prev => ({ ...prev, visible: false }));
  };
  
  // Calculate team performance points using octagonal positions
  const team1Points = team1Data.map((value, index) => {
    const octagonIndex = quarterPositions[index];
    const angle = octagonIndex * angleStep - Math.PI / 2;
    const r = (value / 100) * radius;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return { x, y, value, angle, octagonIndex };
  });

  const team2Points = team2Data.map((value, index) => {
    const octagonIndex = quarterPositions[index];
    const angle = octagonIndex * angleStep - Math.PI / 2;
    const r = (value / 100) * radius;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return { x, y, value, angle, octagonIndex };
  });

  // Create octagonal frame points for structure
  const octagonFramePoints = Array.from({ length: octagonPoints }, (_, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const x = center + radius * Math.cos(angle);
    const y = center + radius * Math.sin(angle);
    return { x, y, angle };
  });

  // Create SVG path data for team areas
  const team1PathData = team1Points.map((point, index) => 
    `${index === 0 ? 'M' : 'L'} ${point.x},${point.y}`
  ).join(' ') + ' Z';

  const team2PathData = team2Points.map((point, index) => 
    `${index === 0 ? 'M' : 'L'} ${point.x},${point.y}`
  ).join(' ') + ' Z';

  // Quarter-specific reference lines based on college football scoring patterns
  // Q1: 22-24% of points, Q2: 27-29% (peak), Q3: 23-25%, Q4: 26-28% (peak)
  const getQuarterBenchmarks = (quarterIndex: number) => {
    const benchmarks = [
      // Q1 - Teams feeling each other out, methodical start
      { elite: 75, average: 62, belowAvg: 48 },
      // Q2 - Peak scoring efficiency, rhythm established, two-minute drills
      { elite: 85, average: 72, belowAvg: 58 },
      // Q3 - Halftime adjustments, slight dip in efficiency
      { elite: 78, average: 65, belowAvg: 52 },
      // Q4 - Peak urgency, fatigue on defense, highest scoring
      { elite: 88, average: 75, belowAvg: 62 }
    ];
    return benchmarks[quarterIndex] || benchmarks[0];
  };

  const referenceLines = [
    { 
      label: 'Elite', 
      data: categories.map((_, i) => getQuarterBenchmarks(i).elite),
      color: '#10b981', 
      opacity: 0.6 
    },
    { 
      label: 'Average', 
      data: categories.map((_, i) => getQuarterBenchmarks(i).average),
      color: '#f59e0b', 
      opacity: 0.5 
    },
    { 
      label: 'Below Avg', 
      data: categories.map((_, i) => getQuarterBenchmarks(i).belowAvg),
      color: '#ef4444', 
      opacity: 0.4 
    }
  ];

  return (
    <div className="relative overflow-hidden rounded-xl bg-[#252b36] border border-[#3a4252] p-6">
      {/* Dynamic Tooltip */}
      {tooltip.visible && (
        <div 
          className="fixed z-50 bg-[#1a1f28] border-2 border-[#3a4252] rounded-xl p-4 shadow-2xl backdrop-blur-sm"
          style={{
            left: tooltip.x,
            top: tooltip.y,
            transform: 'translate(-50%, -100%)',
            pointerEvents: 'none'
          }}
        >
          <div className="flex items-center gap-3 mb-3">
            <div className="flex gap-2">
              <ImageWithFallback src={team1Logo} className="w-6 h-6" />
              <ImageWithFallback src={team2Logo} className="w-6 h-6" />
            </div>
            <h4 className="text-white font-bold text-sm">{tooltip.quarter} Benchmarks</h4>
          </div>
          
          <div className="space-y-2">
            {referenceLines.map((ref, refIndex) => (
              <div key={refIndex} className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-0.5 rounded"
                    style={{ backgroundColor: ref.color }}
                  ></div>
                  <span className="text-xs font-medium text-slate-300">{ref.label}</span>
                </div>
                <span 
                  className="text-xs font-bold"
                  style={{ color: ref.color }}
                >
                  {ref.data[tooltip.quarterIndex]}%
                </span>
              </div>
            ))}
          </div>
          
          <div className="mt-3 pt-3 border-t border-[#3a4252]">
            <div className="text-[10px] text-slate-400">
              College Football {tooltip.quarter} Averages
            </div>
          </div>
        </div>
      )}
      {/* Performance Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-6">
        {categories.map((category, index) => {
          const team1Value = team1Data[index];
          const team2Value = team2Data[index];
          const winner = team1Value > team2Value ? 'team1' : 'team2';
          
          return (
            <div key={category} className="bg-[#2a3140] rounded-lg p-2 border border-[#3a4252]">
              {/* Header */}
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-slate-400 text-[9px] font-semibold">{category}</span>
                <ImageWithFallback 
                  src={winner === 'team1' ? team1Logo : team2Logo} 
                  className="w-3 h-3" 
                />
              </div>
              
              {/* Values */}
              <div className="flex items-baseline gap-1 mb-1">
                <span className={`${
                  winner === 'team1' ? 'text-emerald-400 font-bold' : 'text-slate-300'
                } text-xs font-mono`}>
                  {team1Value}%
                </span>
                <span className="text-slate-500 text-[9px]">vs</span>
                <span className={`${
                  winner === 'team2' ? 'text-emerald-400 font-bold' : 'text-slate-300'
                } text-xs font-mono`}>
                  {team2Value}%
                </span>
              </div>
              
              {/* Progress Bar */}
              <div className="h-1 bg-[#1a1f28] rounded-full overflow-hidden">
                <div 
                  className={`h-full rounded-full ${
                    winner === 'team1' 
                      ? `bg-gradient-to-r from-[${team1Color}] to-[${team2Color}]/60` 
                      : `bg-gradient-to-r from-[${team1Color}]/60 to-[${team2Color}]`
                  }`} 
                  style={{ width: '95%' }} 
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend System */}
      <div className="flex items-center justify-center gap-3 mb-4 flex-wrap text-[10px]">
        {/* Team Legends */}
        <div className={`flex items-center gap-1.5 px-2 py-1 bg-[#2a3140] rounded border border-[${team1Color}]/30`}>
          <div className={`w-3 h-0.5 bg-[${team1Color}]`}></div>
          <ImageWithFallback src={team1Logo} className="w-3 h-3" />
          <span className={`font-bold`} style={{ color: team1Color }}>{team1Label}</span>
        </div>
        
        <div className={`flex items-center gap-1.5 px-2 py-1 bg-[#2a3140] rounded border border-[${team2Color}]/30`}>
          <div className={`w-3 h-0.5 bg-[${team2Color}]`}></div>
          <ImageWithFallback src={team2Logo} className="w-3 h-3" />
          <span className={`font-bold`} style={{ color: team2Color }}>{team2Label}</span>
        </div>
        
        {/* Separator */}
        <div className="h-3 w-px bg-[#3a4252]"></div>
        
        {/* Reference Lines Legend */}
        {referenceLines.map((ref) => (
          <div key={ref.label} className="flex items-center gap-1">
            <svg width="16" height="2">
              <line 
                x1="0" y1="1" x2="16" y2="1" 
                stroke={ref.color} 
                strokeWidth="2" 
                strokeDasharray="3 2"
                opacity={ref.opacity}
              />
            </svg>
            <span className={`font-semibold`} style={{ color: ref.color }}>{ref.label}</span>
          </div>
        ))}
      </div>

      {/* Ultra-Dynamic Octagonal Chart */}
      <div className="flex justify-center relative p-4">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="drop-shadow-2xl overflow-visible">
          <defs>
            {/* Advanced 3D Glow Filters */}
            <filter id="glow-team1" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feOffset in="coloredBlur" dx="2" dy="2" result="offsetBlur"/>
              <feMerge>
                <feMergeNode in="offsetBlur"/>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            <filter id="glow-team2" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feOffset in="coloredBlur" dx="2" dy="2" result="offsetBlur"/>
              <feMerge>
                <feMergeNode in="offsetBlur"/>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            
            {/* 3D Logo Shadow Filter */}
            <filter id="logo-3d" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="3" dy="3" stdDeviation="2" floodColor="#000000" floodOpacity="0.6"/>
              <feDropShadow dx="1" dy="1" stdDeviation="1" floodColor={team1Color} floodOpacity="0.3"/>
            </filter>
            
            {/* Dynamic Pulsing Animation */}
            <filter id="pulse-glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            
            {/* Ultra-Dynamic Gradients */}
            <radialGradient id="team1-ultra" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor={team1Color} stopOpacity="0.35" />
              <stop offset="50%" stopColor={team1Color} stopOpacity="0.15" />
              <stop offset="100%" stopColor={team1Color} stopOpacity="0.02" />
            </radialGradient>
            <radialGradient id="team2-ultra" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor={team2Color} stopOpacity="0.35" />
              <stop offset="50%" stopColor={team2Color} stopOpacity="0.15" />
              <stop offset="100%" stopColor={team2Color} stopOpacity="0.02" />
            </radialGradient>
            
            {/* Octagonal Pattern */}
            <pattern id="octagon-pattern" patternUnits="userSpaceOnUse" width="20" height="20">
              <circle cx="10" cy="10" r="1" fill="#3a4252" opacity="0.3"/>
            </pattern>
          </defs>
          
          {/* Octagonal Grid System - Dynamic & Modern */}
          {[25, 50, 75, 100].map((percentage, index) => {
            const r = (percentage / 100) * radius;
            const octagonPath = octagonFramePoints.map((point, i) => {
              const x = center + r * Math.cos(point.angle);
              const y = center + r * Math.sin(point.angle);
              return `${i === 0 ? 'M' : 'L'} ${x},${y}`;
            }).join(' ') + ' Z';
            
            return (
              <path
                key={percentage}
                d={octagonPath}
                fill={percentage === 100 ? "url(#octagon-pattern)" : "none"}
                stroke="#3a4252"
                strokeWidth={percentage === 100 ? 3 : 1.5}
                opacity={0.2 + index * 0.2}
                className={percentage === 100 ? "animate-pulse" : ""}
                style={{ animationDuration: '3s' }}
              />
            );
          })}
          
          {/* Dynamic Axis Lines to Octagon Vertices */}
          {octagonFramePoints.map((point, index) => (
            <line
              key={`axis-${index}`}
              x1={center}
              y1={center}
              x2={point.x}
              y2={point.y}
              stroke="#3a4252"
              strokeWidth={quarterPositions.includes(index) ? "2" : "1"}
              opacity={quarterPositions.includes(index) ? "0.6" : "0.3"}
              className={quarterPositions.includes(index) ? "animate-pulse" : ""}
              style={{ animationDuration: '4s', animationDelay: `${index * 0.1}s` }}
            />
          ))}
          
          {/* Quarter-Specific Reference Performance Lines (Dashed) */}
          {referenceLines.map((ref, refIndex) => {
            const refPoints = categories.map((_, index) => {
              const angle = index * angleStep - Math.PI / 2;
              const r = (ref.data[index] / 100) * radius;
              const x = center + r * Math.cos(angle);
              const y = center + r * Math.sin(angle);
              return { x, y };
            });
            
            const refPath = refPoints.map((point, index) => 
              `${index === 0 ? 'M' : 'L'} ${point.x},${point.y}`
            ).join(' ') + ' Z';
            
            return (
              <path
                key={`ref-${refIndex}`}
                d={refPath}
                fill="none"
                stroke={ref.color}
                strokeWidth="1.5"
                strokeDasharray="4 4"
                opacity={ref.opacity}
              />
            );
          })}
          
          {/* Team Performance Areas - Ultra Transparent */}
          <path
            d={team1PathData}
            fill="url(#team1-ultra)"
            stroke={team1Color}
            strokeWidth="2.5"
            fillOpacity="0.15"
            filter="url(#glow-team1)"
          />
          
          <path
            d={team2PathData}
            fill="url(#team2-ultra)"
            stroke={team2Color}
            strokeWidth="2.5"
            fillOpacity="0.15"
            filter="url(#glow-team2)"
          />
          
          {/* Dynamic 3D Team Logos at Chart Center */}
          <g transform={`translate(${center-25}, ${center-35})`}>
            <image
              href={team1Logo}
              width="24"
              height="24"
              filter="url(#logo-3d)"
              className="animate-pulse"
              style={{ animationDuration: '2s' }}
            />
            <text
              x="12"
              y="35"
              textAnchor="middle"
              className="text-[10px] font-bold"
              style={{ fill: team1Color, filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.8))' }}
            >
              {team1Label}
            </text>
          </g>
          
          <g transform={`translate(${center+5}, ${center-35})`}>
            <image
              href={team2Logo}
              width="24"
              height="24"
              filter="url(#logo-3d)"
              className="animate-pulse"
              style={{ animationDuration: '2s', animationDelay: '0.5s' }}
            />
            <text
              x="12"
              y="35"
              textAnchor="middle"
              className="text-[10px] font-bold"
              style={{ fill: team2Color, filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.8))' }}
            >
              {team2Label}
            </text>
          </g>

          {/* Enhanced Data Points - Larger with 3D Effect */}
          {team1Points.map((point, index) => (
            <g key={`team1-dot-${index}`}>
              {/* Outer glow ring */}
              <circle
                cx={point.x}
                cy={point.y}
                r="8"
                fill="none"
                stroke={team1Color}
                strokeWidth="1"
                opacity="0.3"
                className="animate-ping"
                style={{ animationDuration: '3s', animationDelay: `${index * 0.2}s` }}
              />
              {/* Main data point */}
              <circle
                cx={point.x}
                cy={point.y}
                r="6"
                fill={team1Color}
                stroke="#1a1f28"
                strokeWidth="3"
                filter="url(#glow-team1)"
              />
              {/* Team logo on data point */}
              <image
                href={team1Logo}
                x={point.x - 8}
                y={point.y - 8}
                width="16"
                height="16"
                filter="url(#pulse-glow)"
                opacity="0.8"
              />
              {/* Team 1 Value Label - Enhanced */}
              <text
                x={point.x}
                y={point.y - 18}
                textAnchor="middle"
                className="text-sm font-bold fill-white"
                style={{ 
                  filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.9))',
                  fontSize: '13px'
                }}
              >
                {point.value}%
              </text>
            </g>
          ))}
          
          {team2Points.map((point, index) => (
            <g key={`team2-dot-${index}`}>
              {/* Outer glow ring */}
              <circle
                cx={point.x}
                cy={point.y}
                r="8"
                fill="none"
                stroke={team2Color}
                strokeWidth="1"
                opacity="0.3"
                className="animate-ping"
                style={{ animationDuration: '3s', animationDelay: `${index * 0.2 + 0.1}s` }}
              />
              {/* Main data point */}
              <circle
                cx={point.x}
                cy={point.y}
                r="6"
                fill={team2Color}
                stroke="#1a1f28"
                strokeWidth="3"
                filter="url(#glow-team2)"
              />
              {/* Team logo on data point */}
              <image
                href={team2Logo}
                x={point.x - 8}
                y={point.y - 8}
                width="16"
                height="16"
                filter="url(#pulse-glow)"
                opacity="0.8"
              />
              {/* Team 2 Value Label - Enhanced */}
              <text
                x={point.x}
                y={point.y + 25}
                textAnchor="middle"
                className="text-sm font-bold fill-white"
                style={{ 
                  filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.9))',
                  fontSize: '13px'
                }}
              >
                {point.value}%
              </text>
            </g>
          ))}
          
          {/* Dynamic Quarter Labels - Enhanced Typography */}
          {categories.map((category, index) => {
            const octagonIndex = quarterPositions[index];
            const angle = octagonIndex * angleStep - Math.PI / 2;
            const labelRadius = radius + 50; // Increased proportionally with chart size
            const x = center + labelRadius * Math.cos(angle);
            const y = center + labelRadius * Math.sin(angle);
            
            return (
              <g key={`quarter-${index}`}>
                {/* Quarter background badge */}
                <circle
                  cx={x}
                  cy={y}
                  r="20"
                  fill="#2a3140"
                  stroke="#3a4252"
                  strokeWidth="2"
                  filter="url(#pulse-glow)"
                  className="animate-pulse"
                  style={{ animationDuration: '4s', animationDelay: `${index * 0.3}s` }}
                />
                {/* Quarter text */}
                <text
                  x={x}
                  y={y + 2}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="text-sm font-bold fill-slate-200"
                  style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.8))' }}
                >
                  {category}
                </text>
              </g>
            );
          })}
          
          {/* Interactive Hover Areas for Tooltips */}
          {categories.map((category, index) => {
            const octagonIndex = quarterPositions[index];
            const angle = octagonIndex * angleStep - Math.PI / 2;
            const hoverRadius = radius + 35; // Increased proportionally with chart size
            const x = center + hoverRadius * Math.cos(angle);
            const y = center + hoverRadius * Math.sin(angle);
            
            return (
              <g key={`hover-area-${index}`}>
                <circle
                  cx={x}
                  cy={y}
                  r="25"
                  fill="transparent"
                  className="hover-trigger cursor-pointer"
                  onMouseEnter={(e) => showTooltip(e, category, index)}
                  onMouseLeave={hideTooltip}
                />
              </g>
            );
          })}
        </svg>
      </div>

      {/* Dynamic 3D Team Edge Summary Cards */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="relative overflow-hidden flex items-center justify-center gap-4 p-6 bg-gradient-to-r from-slate-900/80 via-slate-800/60 to-slate-900/80 rounded-xl border-2 border-slate-600/50 backdrop-blur-sm shadow-2xl">
          {/* Team 1 Side */}
          <div className="flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-transparent via-slate-900/40 to-transparent rounded-lg border border-slate-600/30">
            <div className="relative">
              <ImageWithFallback 
                src={team1Logo} 
                className="w-12 h-12 drop-shadow-lg" 
                style={{ 
                  filter: 'drop-shadow(3px 3px 6px rgba(0,0,0,0.5)) drop-shadow(0px 0px 8px rgba(255,255,255,0.2))',
                  transform: 'perspective(100px) rotateY(-5deg)'
                }}
              />
              <div 
                className="absolute inset-0 w-12 h-12 rounded-full blur-md opacity-40"
                style={{ backgroundColor: team1Color }}
              ></div>
            </div>
            <div className="font-bold text-lg" style={{ color: team1Color }}>
              {team1Label} Edge
            </div>
          </div>

          {/* VS Divider */}
          <div className="text-slate-400 font-bold text-xl px-4">VS</div>

          {/* Team 2 Side */}
          <div className="flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-transparent via-slate-900/40 to-transparent rounded-lg border border-slate-600/30">
            <div className="relative">
              <ImageWithFallback 
                src={team2Logo} 
                className="w-12 h-12 drop-shadow-lg" 
                style={{ 
                  filter: 'drop-shadow(3px 3px 6px rgba(0,0,0,0.5)) drop-shadow(0px 0px 8px rgba(255,255,255,0.2))',
                  transform: 'perspective(100px) rotateY(5deg)'
                }}
              />
              <div 
                className="absolute inset-0 w-12 h-12 rounded-full blur-md opacity-40"
                style={{ backgroundColor: team2Color }}
              ></div>
            </div>
            <div className="font-bold text-lg" style={{ color: team2Color }}>
              {team2Label} Edge
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Tooltip Component */}
      {tooltip.visible && (
        <div
          className="fixed z-50 pointer-events-none"
          style={{
            left: `${tooltip.x + 10}px`,
            top: `${tooltip.y - 10}px`,
            transform: 'translate(0, -100%)'
          }}
        >
          <div className="bg-gradient-to-br from-slate-900/95 to-slate-800/95 rounded-lg p-4 border border-slate-600/50 backdrop-blur-md shadow-2xl max-w-xs">
            <div className="flex items-center gap-3 mb-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span className="text-white font-bold text-sm">{tooltip.quarter} Benchmarks</span>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ImageWithFallback 
                    src="https://a.espncdn.com/i/teamlogos/ncaa/500/333.png"
                    alt="Top 25"
                    className="w-5 h-5 object-contain opacity-80"
                  />
                  <span className="text-slate-300 text-xs">Elite Programs</span>
                </div>
                <span className="text-green-400 font-semibold text-sm">{tooltip.benchmarks.elite}%</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ImageWithFallback 
                    src="https://a.espncdn.com/i/teamlogos/ncaa/500/2005.png"
                    alt="FBS Average"
                    className="w-5 h-5 object-contain opacity-80"
                  />
                  <span className="text-slate-300 text-xs">FBS Average</span>
                </div>
                <span className="text-blue-400 font-semibold text-sm">{tooltip.benchmarks.average}%</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ImageWithFallback 
                    src="https://a.espncdn.com/i/teamlogos/ncaa/500/2084.png"
                    alt="Bottom Tier"
                    className="w-5 h-5 object-contain opacity-80"
                  />
                  <span className="text-slate-300 text-xs">Lower Tier</span>
                </div>
                <span className="text-orange-400 font-semibold text-sm">{tooltip.benchmarks.poor}%</span>
              </div>
            </div>
            
            <div className="mt-3 pt-2 border-t border-slate-600/30">
              <p className="text-slate-400 text-xs leading-relaxed">
                College football scoring efficiency varies significantly by quarter, with teams typically performing stronger in Q2 and Q4.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Modern Spider Chart Component
const SpiderChart = ({ 
  data, 
  color, 
  label, 
  categories,
  teamLogo 
}: { 
  data: number[], 
  color: string, 
  label: string,
  categories: string[],
  teamLogo: string
}) => {
  const size = 240;
  const center = size / 2;
  const radius = 85;
  const angleStep = (2 * Math.PI) / data.length;
  
  const points = data.map((value, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = (value / 100) * radius;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return { x, y, value };
  });

  const pathData = points.map((point, index) => 
    `${index === 0 ? 'M' : 'L'} ${point.x},${point.y}`
  ).join(' ') + ' Z';

  return (
    <div className="flex flex-col items-center p-4">
      <div className="relative">
        <svg width={size} height={size} className="mb-3">
          <defs>
            <radialGradient id={`gradient-${label}`} cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor={color} stopOpacity="0.4" />
              <stop offset="100%" stopColor={color} stopOpacity="0.1" />
            </radialGradient>
            <filter id={`glow-${label}`}>
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          {/* Grid circles with glow effect */}
          {[25, 50, 75, 100].map((percentage, index) => (
            <circle
              key={percentage}
              cx={center}
              cy={center}
              r={(percentage / 100) * radius}
              fill="none"
              stroke={`rgba(255,255,255,${0.05 + index * 0.05})`}
              strokeWidth="1"
              className="animate-pulse"
              style={{ animationDelay: `${index * 0.2}s` }}
            />
          ))}
          
          {/* Grid lines to vertices */}
          {data.map((_, index) => {
            const angle = index * angleStep - Math.PI / 2;
            const x = center + radius * Math.cos(angle);
            const y = center + radius * Math.sin(angle);
            return (
              <line
                key={index}
                x1={center}
                y1={center}
                x2={x}
                y2={y}
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="1"
              />
            );
          })}
          
          {/* Data area with gradient */}
          <path
            d={pathData}
            fill={`url(#gradient-${label})`}
            stroke={color}
            strokeWidth="2.5"
            opacity="0.9"
            filter={`url(#glow-${label})`}
          />
          
          {/* Data points with glow */}
          {points.map((point, index) => (
            <g key={index}>
              <circle
                cx={point.x}
                cy={point.y}
                r="6"
                fill={color}
                stroke="rgba(255,255,255,0.8)"
                strokeWidth="2"
                filter={`url(#glow-${label})`}
              />
              <text
                x={point.x}
                y={point.y - 12}
                textAnchor="middle"
                className="text-xs font-semibold fill-white"
                style={{ filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.8))' }}
              >
                {point.value}%
              </text>
            </g>
          ))}
          
          {/* Category labels */}
          {categories.map((category, index) => {
            const angle = index * angleStep - Math.PI / 2;
            const labelRadius = radius + 25;
            const x = center + labelRadius * Math.cos(angle);
            const y = center + labelRadius * Math.sin(angle);
            return (
              <text
                key={index}
                x={x}
                y={y}
                textAnchor="middle"
                dominantBaseline="middle"
                className="text-xs font-medium fill-slate-300"
              >
                {category}
              </text>
            );
          })}
        </svg>
      </div>
      <div className="flex items-center gap-2 bg-gradient-to-r from-slate-500/20 to-gray-500/20 px-4 py-2 rounded-full border border-slate-500/40">
        <ImageWithFallback 
          src={teamLogo}
          alt={label}
          className="w-6 h-6 object-contain opacity-90"
        />
        <span className="text-sm font-bold text-white">{label}</span>
      </div>
    </div>
  );
};

export function DriveEfficiency({ team1Data, team2Data, predictionData }: DriveEfficiencyProps) {
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;

  // Parse drive analytics from section [17]
  const parseDriveData = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 17) : null;
    
    if (!section || !awayTeam || !homeTeam) {
      return {
        quarterData: mockQuarterData,
        fieldPositionData: mockFieldPositionData,
        driveOutcomes: mockDriveOutcomes
      };
    }

    // Parse Quarter-by-Quarter Performance
    // Pattern: "1st Quarter     4 drives (75% scoring, 77.0 yds)      10 drives (90% scoring, 72.2 yds)      Home"
    const parseQuarterData = () => {
      const quarters = ['1st', '2nd', '3rd', '4th'];
      const awayData: any[] = [];
      const homeData: any[] = [];

      quarters.forEach(quarter => {
        const pattern = new RegExp(`${quarter} Quarter\\s+(\\d+) drives \\((\\d+)% scoring, ([\\d.]+) yds\\)\\s+(\\d+) drives \\((\\d+)% scoring, ([\\d.]+) yds\\)`, 'i');
        const match = section.match(pattern);
        
        if (match) {
          awayData.push({
            quarter,
            drives: parseInt(match[1]),
            scoringPct: parseInt(match[2]),
            avgYards: parseFloat(match[3])
          });
          homeData.push({
            quarter,
            drives: parseInt(match[4]),
            scoringPct: parseInt(match[5]),
            avgYards: parseFloat(match[6])
          });
        }
      });

      return { team1: awayData.length === 4 ? awayData : mockQuarterData.team1, 
               team2: homeData.length === 4 ? homeData : mockQuarterData.team2 };
    };

    // Parse Field Position Mastery
    // Pattern: "Own 1-20             8 drives (37.5% scoring)           5 drives (40.0% scoring)"
    const parseFieldPositionData = () => {
      const zones = ['Own 1-20', 'Own 21-40', 'Own 41-Mid', 'Opp Territory'];
      const awayData: any[] = [];
      const homeData: any[] = [];

      zones.forEach(zone => {
        const pattern = new RegExp(`${zone.replace(/[-]/g, '\\-')}\\s+(\\d+) drives \\(([\\d.]+)% scoring\\)\\s+(\\d+) drives \\(([\\d.]+)% scoring\\)`, 'i');
        const match = section.match(pattern);
        
        if (match) {
          awayData.push({
            zone,
            drives: parseInt(match[1]),
            scoringPct: parseFloat(match[2])
          });
          homeData.push({
            zone,
            drives: parseInt(match[3]),
            scoringPct: parseFloat(match[4])
          });
        }
      });

      return { team1: awayData.length === 4 ? awayData : mockFieldPositionData.team1,
               team2: homeData.length === 4 ? homeData : mockFieldPositionData.team2 };
    };

    // Parse Drive Outcomes
    // Pattern: "Touchdowns           17 (27.9%)                34 (58.6%)                Home"
    const parseDriveOutcomes = () => {
      const parseOutcome = (metric: string) => {
        const pattern = new RegExp(`${metric}\\s+\\d+ \\(([\\d.]+)%\\)\\s+\\d+ \\(([\\d.]+)%\\)`, 'i');
        const match = section.match(pattern);
        return match ? { away: parseFloat(match[1]), home: parseFloat(match[2]) } : null;
      };

      const touchdowns = parseOutcome('Touchdowns');
      const fieldGoals = parseOutcome('Field Goals');
      const punts = parseOutcome('Punts');
      const turnovers = parseOutcome('Turnovers');
      
      // Parse total scoring percentage
      const scoringPattern = /TOTAL SCORING %\s+([\d.]+)%\s+([\d.]+)%/i;
      const scoringMatch = section.match(scoringPattern);

      if (touchdowns && fieldGoals && punts && turnovers && scoringMatch) {
        return {
          team1: {
            touchdowns: touchdowns.away,
            fieldGoals: fieldGoals.away,
            punts: punts.away,
            turnovers: turnovers.away,
            totalScoring: parseFloat(scoringMatch[1])
          },
          team2: {
            touchdowns: touchdowns.home,
            fieldGoals: fieldGoals.home,
            punts: punts.home,
            turnovers: turnovers.home,
            totalScoring: parseFloat(scoringMatch[2])
          }
        };
      }

      return mockDriveOutcomes;
    };

    return {
      quarterData: parseQuarterData(),
      fieldPositionData: parseFieldPositionData(),
      driveOutcomes: parseDriveOutcomes()
    };
  };

  const { quarterData, fieldPositionData, driveOutcomes } = parseDriveData();

  // Extract scoring percentages for spider charts
  const team1QuarterScoring = quarterData.team1.map(q => q.scoringPct);
  const team2QuarterScoring = quarterData.team2.map(q => q.scoringPct);
  
  const team1FieldPositionScoring = fieldPositionData.team1.map(fp => fp.scoringPct);
  const team2FieldPositionScoring = fieldPositionData.team2.map(fp => fp.scoringPct);

  const quarterCategories = ['Q1', 'Q2', 'Q3', 'Q4'];
  const fieldPositionCategories = ['Own 1-20', 'Own 21-40', 'Own 41-Mid', 'Opp Territory'];
  
  // Use team data from predictionData or fallback to defaults
  const team1Logo = awayTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png";
  const team2Logo = homeTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png";
  const team1Name = awayTeam?.name || "Ohio State";
  const team2Name = homeTeam?.name || "Illinois";
  const team1Color = awayTeam?.primary_color || "#ce1141";
  const team2Color = homeTeam?.primary_color || "#ff5f05";

  return (
    <GlassCard glowColor="from-slate-500/20 to-gray-500/20" className="p-3 border-slate-500/40">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-lg bg-slate-500/20 border border-slate-500/40">
          <Zap className="w-4 h-4 text-green-400" />
        </div>
        <h3 className="text-white font-semibold text-sm">Drive Efficiency & Game Flow Analytics</h3>
      </div>

      {/* Quarter Performance Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Quarter-by-Quarter Performance - Mirroring Field Position Design */}
        <div className="bg-gradient-to-br from-slate-800/40 to-slate-900/40 rounded-xl p-4 border border-slate-600/30">
          <h4 className="text-slate-300 font-semibold mb-4 flex items-center gap-2 text-sm">
            <BarChart3 className="w-3 h-3 text-green-400" />
            Quarter-by-Quarter Performance
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Team 1 Bar Chart */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback 
                  src={team1Logo}
                  alt={team1Name}
                  className="w-6 h-6 object-contain"
                />
                <h5 className="font-semibold" style={{ color: team1Color }}>{team1Name}</h5>
              </div>
              {quarterCategories.map((category, index) => (
                <div key={category} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-300 font-medium">{category}</span>
                    <span className="font-bold" style={{ color: team1Color }}>
                      {team1QuarterScoring[index]}%
                    </span>
                  </div>
                  <div className="relative h-8 bg-slate-700/30 rounded-lg overflow-hidden border border-slate-600/30">
                    <div 
                      className="absolute inset-y-0 left-0 rounded-lg transition-all duration-500 ease-out"
                      style={{ 
                        width: `${team1QuarterScoring[index]}%`,
                        background: `linear-gradient(to right, ${team1Color}80, ${team1Color})`,
                        boxShadow: `0 0 10px ${team1Color}40`
                      }}
                    />
                    <div className="absolute inset-0 flex items-center px-3">
                      <span className="text-white text-xs font-bold drop-shadow-lg z-10">
                        {team1QuarterScoring[index]}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Team 2 Bar Chart */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback 
                  src={team2Logo}
                  alt={team2Name}
                  className="w-6 h-6 object-contain"
                />
                <h5 className="font-semibold" style={{ color: team2Color }}>{team2Name}</h5>
              </div>
              {quarterCategories.map((category, index) => (
                <div key={category} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-300 font-medium">{category}</span>
                    <span className="font-bold" style={{ color: team2Color }}>
                      {team2QuarterScoring[index]}%
                    </span>
                  </div>
                  <div className="relative h-8 bg-slate-700/30 rounded-lg overflow-hidden border border-slate-600/30">
                    <div 
                      className="absolute inset-y-0 left-0 rounded-lg transition-all duration-500 ease-out"
                      style={{ 
                        width: `${team2QuarterScoring[index]}%`,
                        background: `linear-gradient(to right, ${team2Color}80, ${team2Color})`,
                        boxShadow: `0 0 10px ${team2Color}40`
                      }}
                    />
                    <div className="absolute inset-0 flex items-center px-3">
                      <span className="text-white text-xs font-bold drop-shadow-lg z-10">
                        {team2QuarterScoring[index]}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Field Position Mastery */}
        <div className="bg-gradient-to-br from-slate-800/40 to-slate-900/40 rounded-xl p-4 border border-slate-600/30">
          <h4 className="text-slate-300 font-semibold mb-4 flex items-center gap-2 text-sm">
            <Target className="w-3 h-3 text-green-400" />
            Field Position Scoring Mastery
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Team 1 Bar Chart */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback 
                  src={team1Logo}
                  alt={team1Name}
                  className="w-6 h-6 object-contain"
                />
                <h5 className="font-semibold" style={{ color: team1Color }}>{team1Name}</h5>
              </div>
              {fieldPositionCategories.map((category, index) => (
                <div key={category} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-300 font-medium">{category}</span>
                    <span className="font-bold" style={{ color: team1Color }}>
                      {team1FieldPositionScoring[index]}%
                    </span>
                  </div>
                  <div className="relative h-8 bg-slate-700/30 rounded-lg overflow-hidden border border-slate-600/30">
                    <div 
                      className="absolute inset-y-0 left-0 rounded-lg transition-all duration-500 ease-out"
                      style={{ 
                        width: `${team1FieldPositionScoring[index]}%`,
                        background: `linear-gradient(to right, ${team1Color}80, ${team1Color})`,
                        boxShadow: `0 0 10px ${team1Color}40`
                      }}
                    />
                    <div className="absolute inset-0 flex items-center px-3">
                      <span className="text-white text-xs font-bold drop-shadow-lg z-10">
                        {team1FieldPositionScoring[index]}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Team 2 Bar Chart */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 mb-4">
                <ImageWithFallback 
                  src={team2Logo}
                  alt={team2Name}
                  className="w-6 h-6 object-contain"
                />
                <h5 className="font-semibold" style={{ color: team2Color }}>{team2Name}</h5>
              </div>
              {fieldPositionCategories.map((category, index) => (
                <div key={category} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-300 font-medium">{category}</span>
                    <span className="font-bold" style={{ color: team2Color }}>
                      {team2FieldPositionScoring[index]}%
                    </span>
                  </div>
                  <div className="relative h-8 bg-slate-700/30 rounded-lg overflow-hidden border border-slate-600/30">
                    <div 
                      className="absolute inset-y-0 left-0 rounded-lg transition-all duration-500 ease-out"
                      style={{ 
                        width: `${team2FieldPositionScoring[index]}%`,
                        background: `linear-gradient(to right, ${team2Color}80, ${team2Color})`,
                        boxShadow: `0 0 10px ${team2Color}40`
                      }}
                    />
                    <div className="absolute inset-0 flex items-center px-3">
                      <span className="text-white text-xs font-bold drop-shadow-lg z-10">
                        {team2FieldPositionScoring[index]}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>



      {/* Field Position Analysis */}
      <div className="mb-6">
        <h4 className="text-slate-300 font-semibold mb-3 flex items-center gap-2 text-sm">
          <Target className="w-3 h-3 text-green-400" />
          Field Position Mastery Analysis
        </h4>
        
        <div className="overflow-x-auto">
          <table className="w-full bg-gradient-to-br from-slate-800/20 to-slate-900/20 rounded-lg">
            <thead>
              <tr className="border-b border-slate-600/40">
                <th className="text-left py-4 px-4 text-slate-300 font-medium">Field Position</th>
                <th className="text-center py-4 px-4 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team1Logo}
                      alt={team1Name}
                      className="w-6 h-6 object-contain opacity-90"
                    />
                    <span style={{ color: team1Color }}>{team1Name}</span>
                  </div>
                </th>
                <th className="text-center py-4 px-4 font-medium">
                  <div className="flex items-center justify-center gap-2">
                    <ImageWithFallback 
                      src={team2Logo}
                      alt={team2Name}
                      className="w-6 h-6 object-contain opacity-90"
                    />
                    <span style={{ color: team2Color }}>{team2Name}</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              {fieldPositionData.team1.map((position, index) => (
                <tr key={position.zone} className="border-b border-slate-700/30 hover:bg-slate-800/20 transition-colors">
                  <td className="py-3 px-4 text-slate-300 font-medium">{position.zone}</td>
                  <td className="py-3 px-4 text-center">
                    <div className="text-white font-semibold">{position.drives} drives</div>
                    <div className="text-sm text-green-400">{position.scoringPct}% scoring</div>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <div className="text-white font-semibold">{fieldPositionData.team2[index].drives} drives</div>
                    <div className="text-sm text-green-400">{fieldPositionData.team2[index].scoringPct}% scoring</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Drive Outcome Breakdown - Modern Spacious Design */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 rounded-xl border border-white/20 shadow-2xl backdrop-blur-xl bg-gradient-to-br from-white/10 to-white/5" style={{ 
              boxShadow: `0 0 20px ${team1Color}30`
            }}>
              <Zap className="w-6 h-6" style={{ color: team1Color }} />
            </div>
            <div>
              <h3 className="text-white font-bold text-xl tracking-wide" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Drive Outcome Breakdown
              </h3>
              <p className="text-slate-400 text-sm mt-1">Power Success, Success Rate, Explosiveness & Efficiency</p>
            </div>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="text-center px-4 py-3 rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-transparent backdrop-blur-xl">
              <ImageWithFallback 
                src={team1Logo} 
                alt={team1Name} 
                className="w-10 h-10 object-contain mx-auto mb-2 drop-shadow-lg"
              />
              <span className="font-bold text-sm tracking-wide" style={{ color: team1Color }}>
                {team1Name.split(' ').pop()} Edge
              </span>
            </div>
            <div className="text-center px-4 py-3 rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-transparent backdrop-blur-xl">
              <ImageWithFallback 
                src={team2Logo} 
                alt={team2Name} 
                className="w-10 h-10 object-contain mx-auto mb-2 drop-shadow-lg"
              />
              <span className="font-bold text-sm tracking-wide" style={{ color: team2Color }}>
                {team2Name.split(' ').pop()} Edge
              </span>
            </div>
          </div>
        </div>
        
        <div className="rounded-2xl p-8 backdrop-blur-xl shadow-2xl" style={{ background: 'rgba(0, 0, 0, 0.2)' }}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Team 1 */}
            <div 
              className="rounded-2xl p-6 shadow-2xl backdrop-blur-xl border-2 transition-all hover:shadow-[0_0_30px_rgba(0,0,0,0.3)]"
              style={{ 
                background: 'rgba(0, 0, 0, 0.2)',
                borderColor: team1Color,
                boxShadow: `0 0 20px ${team1Color}40, inset 0 0 60px ${team1Color}15`
              }}
            >
              <div 
                className="flex items-center gap-3 mb-6 pb-4 border-b-2"
                style={{ borderColor: `${team1Color}40` }}
              >
                <ImageWithFallback 
                  src={team1Logo}
                  alt={team1Name}
                  className="w-10 h-10 object-contain opacity-95 drop-shadow-2xl"
                />
                <h5 className="font-bold text-xl tracking-wide" style={{ color: team1Color }}>{team1Name}</h5>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Touchdowns</span>
                  <span className="text-green-400 font-bold text-lg">{driveOutcomes.team1.touchdowns}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Field Goals</span>
                  <span className="text-blue-400 font-bold text-lg">{driveOutcomes.team1.fieldGoals}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Punts</span>
                  <span className="text-yellow-400 font-bold text-lg">{driveOutcomes.team1.punts}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Turnovers</span>
                  <span className="text-red-400 font-bold text-lg">{driveOutcomes.team1.turnovers}%</span>
                </div>
                <div className="border-t border-white/10 mt-2 pt-4 flex justify-between items-center py-4 px-5 bg-gradient-to-r from-slate-900/60 to-slate-800/40 rounded-xl backdrop-blur-xl">
                  <span className="text-white font-bold text-base tracking-wide">Power Success</span>
                  <span className="text-green-400 font-bold text-2xl">{driveOutcomes.team1.totalScoring}%</span>
                </div>
              </div>
            </div>

            {/* Team 2 */}
            <div 
              className="rounded-2xl p-6 shadow-2xl backdrop-blur-xl border-2 transition-all hover:shadow-[0_0_30px_rgba(0,0,0,0.3)]"
              style={{ 
                background: 'rgba(0, 0, 0, 0.2)',
                borderColor: team2Color,
                boxShadow: `0 0 20px ${team2Color}40, inset 0 0 60px ${team2Color}15`
              }}
            >
              <div 
                className="flex items-center gap-3 mb-6 pb-4 border-b-2"
                style={{ borderColor: `${team2Color}40` }}
              >
                <ImageWithFallback 
                  src={team2Logo}
                  alt={team2Name}
                  className="w-10 h-10 object-contain opacity-95 drop-shadow-2xl"
                />
                <h5 className="font-bold text-xl tracking-wide" style={{ color: team2Color }}>{team2Name}</h5>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Touchdowns</span>
                  <span className="text-green-400 font-bold text-lg">{driveOutcomes.team2.touchdowns}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Field Goals</span>
                  <span className="text-blue-400 font-bold text-lg">{driveOutcomes.team2.fieldGoals}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Punts</span>
                  <span className="text-yellow-400 font-bold text-lg">{driveOutcomes.team2.punts}%</span>
                </div>
                <div className="flex justify-between items-center py-3 px-4 bg-gradient-to-r from-slate-800/40 to-transparent rounded-xl border border-slate-600/20 backdrop-blur-sm hover:border-white/20 transition-all">
                  <span className="text-slate-200 font-semibold text-base">Turnovers</span>
                  <span className="text-red-400 font-bold text-lg">{driveOutcomes.team2.turnovers}%</span>
                </div>
                <div className="border-t border-white/10 mt-2 pt-4 flex justify-between items-center py-4 px-5 bg-gradient-to-r from-slate-900/60 to-slate-800/40 rounded-xl backdrop-blur-xl">
                  <span className="text-white font-bold text-base tracking-wide">Power Success</span>
                  <span className="text-green-400 font-bold text-2xl">{driveOutcomes.team2.totalScoring}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}