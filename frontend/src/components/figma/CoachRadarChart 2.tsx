import React from 'react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface SchoolData {
  name: string;
  mascot: string;
  logo: string;
  primary_color: string;
  alt_color: string;
  years: string;
  record: string;
}

interface CoachRadarChartProps {
  coachData: any;
  size?: number;
}

export const CoachRadarChart: React.FC<CoachRadarChartProps> = ({ coachData, size = 340 }) => {
  const schools: SchoolData[] = coachData.schools_info || [];
  
  // Calculate win percentage for each school and sort by highest to lowest
  const schoolMetrics = schools.map(school => {
    const parts = school.record.split('-');
    const wins = parseInt(parts[0]);
    const losses = parseInt(parts[1]);
    const total = wins + losses;
    const winPct = total > 0 ? (wins / total) * 100 : 0;
    
    return {
      ...school,
      winPct,
      displayValue: winPct
    };
  }).sort((a, b) => b.winPct - a.winPct); // Sort descending by win percentage

  const center = size / 2;
  const maxRadius = (size / 2) - 70;
  const angleStep = (2 * Math.PI) / schoolMetrics.length;
  
  // Find the highest win percentage to normalize the radius
  const maxWinPct = Math.max(...schoolMetrics.map(s => s.winPct));

  // Calculate polygon points
  const getPoint = (index: number, value: number) => {
    const angle = angleStep * index - Math.PI / 2;
    const radius = (value / maxWinPct) * maxRadius; // Normalize to highest win %
    return {
      x: center + radius * Math.cos(angle),
      y: center + radius * Math.sin(angle)
    };
  };

  // Grid circles
  const gridLevels = [20, 40, 60, 80, 100];

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="absolute inset-0">
        <defs>
          {/* Individual gradients for each school segment */}
          {schoolMetrics.map((school, i) => (
            <linearGradient key={i} id={`gradient-${school.name.replace(/\s/g, '')}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={school.primary_color} stopOpacity="0.6" />
              <stop offset="100%" stopColor={school.alt_color} stopOpacity="0.2" />
            </linearGradient>
          ))}
          
          {/* Glow filters for each school */}
          {schoolMetrics.map((school, i) => (
            <filter key={i} id={`glow-${school.name.replace(/\s/g, '')}`}>
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          ))}
        </defs>

        {/* Background circles (grid) */}
        {gridLevels.map((level, i) => (
          <circle
            key={i}
            cx={center}
            cy={center}
            r={(level / 100) * maxRadius}
            fill="none"
            stroke="rgba(255,255,255,0.03)"
            strokeWidth="1"
            strokeDasharray={i === gridLevels.length - 1 ? "0" : "4 4"}
          />
        ))}

        {/* Axis lines with school colors */}
        {schoolMetrics.map((school, index) => {
          const point = getPoint(index, 100);
          return (
            <line
              key={index}
              x1={center}
              y1={center}
              x2={point.x}
              y2={point.y}
              stroke={school.primary_color}
              strokeWidth="2"
              strokeOpacity="0.2"
            />
          );
        })}

        {/* Individual colored segments - perfect equal wedges */}
        {schoolMetrics.map((school, index) => {
          // Calculate the start and end angles for this wedge
          const startAngle = angleStep * index - Math.PI / 2;
          const endAngle = angleStep * (index + 1) - Math.PI / 2;
          
          // Use school's actual win percentage normalized to the highest win %
          const perfRadius = (school.winPct / maxWinPct) * maxRadius;
          
          // Start point on the arc
          const startPoint = {
            x: center + perfRadius * Math.cos(startAngle),
            y: center + perfRadius * Math.sin(startAngle)
          };
          
          // End point on the arc
          const endPoint = {
            x: center + perfRadius * Math.cos(endAngle),
            y: center + perfRadius * Math.sin(endAngle)
          };
          
          // Calculate midpoint for logo watermark placement
          const midAngle = startAngle + angleStep / 2;
          const logoRadius = perfRadius * 0.65;
          const logoX = center + logoRadius * Math.cos(midAngle);
          const logoY = center + logoRadius * Math.sin(midAngle);
          
          // Determine if we need a large arc flag (for angles > 180 degrees)
          const largeArcFlag = angleStep > Math.PI ? 1 : 0;
          
          return (
            <g key={index}>
              {/* Perfect wedge with smooth rounded arc edge */}
              <path
                d={`
                  M ${center} ${center}
                  L ${startPoint.x} ${startPoint.y}
                  A ${perfRadius} ${perfRadius} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y}
                  Z
                `}
                fill={`url(#gradient-${school.name.replace(/\s/g, '')})`}
                opacity="0.75"
                filter={`url(#glow-${school.name.replace(/\s/g, '')})`}
                style={{
                  filter: `drop-shadow(0 0 8px ${school.primary_color}60)`
                }}
              />
              
              {/* Bold outer arc border */}
              <path
                d={`
                  M ${startPoint.x} ${startPoint.y}
                  A ${perfRadius} ${perfRadius} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y}
                `}
                fill="none"
                stroke={school.primary_color}
                strokeWidth="3"
                opacity="0.8"
                strokeLinecap="round"
              />
              
              {/* Team Logo Watermark in segment */}
              <foreignObject 
                x={logoX - 20} 
                y={logoY - 20} 
                width="40" 
                height="40"
                style={{ pointerEvents: 'none' }}
              >
                <div className="w-full h-full flex items-center justify-center opacity-20">
                  <ImageWithFallback 
                    src={school.logo}
                    alt={school.name}
                    className="w-full h-full object-contain"
                  />
                </div>
              </foreignObject>
              
              {/* Segment border lines - both edges */}
              <line
                x1={center}
                y1={center}
                x2={startPoint.x}
                y2={startPoint.y}
                stroke={school.alt_color}
                strokeWidth="1.5"
                opacity="0.4"
              />
              <line
                x1={center}
                y1={center}
                x2={endPoint.x}
                y2={endPoint.y}
                stroke={school.alt_color}
                strokeWidth="1.5"
                opacity="0.4"
              />
            </g>
          );
        })}

        {/* Center coach headshot */}
        <foreignObject x={center - 30} y={center - 30} width="60" height="60">
          <div className="w-full h-full flex items-center justify-center">
            <ImageWithFallback 
              src={coachData.coach_info?.headshot_url}
              alt={coachData.metadata?.coach}
              className="w-full h-full rounded-full object-cover border-2 border-white/20"
            />
          </div>
        </foreignObject>
      </svg>

      {/* School labels positioned in middle of each quadrant, outside circle */}
      {schoolMetrics.map((school, index) => {
        // Calculate middle angle of this school's segment
        const midAngle = angleStep * index + angleStep / 2 - Math.PI / 2;
        const labelRadius = maxRadius * 1.45; // Position further outside circle
        const labelX = center + labelRadius * Math.cos(midAngle);
        const labelY = center + labelRadius * Math.sin(midAngle);
        
        // Calculate rotation angle for text (convert radians to degrees)
        const rotationDegrees = ((midAngle + Math.PI / 2) * 180) / Math.PI;
        
        return (
          <div
            key={index}
            className="absolute transform -translate-x-1/2 -translate-y-1/2"
            style={{
              left: labelX,
              top: labelY,
              width: '110px',
              transformOrigin: 'center center'
            }}
          >
            <div style={{ transform: `rotate(${rotationDegrees}deg)` }}>
              {/* Win Percentage - with team color glow */}
              <div 
                className="text-2xl font-black mb-1 text-center"
                style={{ 
                  color: school.primary_color,
                  textShadow: `0 0 15px ${school.primary_color}60`
                }}
              >
                {school.winPct.toFixed(1)}%
              </div>
              
              {/* School Name - Subtle gray */}
              <div className="text-[10px] uppercase tracking-wide font-light leading-tight text-center text-gray-500">
                {school.name}
              </div>
              
              {/* Record - More subtle */}
              <div 
                className="text-xs font-light text-center mt-0.5 text-gray-400"
              >
                {school.record}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

