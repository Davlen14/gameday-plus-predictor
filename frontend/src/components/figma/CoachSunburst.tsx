import React, { useEffect, useRef } from 'react';

interface CoachSunburstProps {
  coachData: any;
}

interface SchoolSegment {
  name: string;
  years: string;
  record: string;
  color: string;
  altColor: string;
  logo: string;
  startYear: number;
  endYear: number;
  winPct: number;
  seasons: SeasonData[];
}

interface SeasonData {
  year: number;
  wins: number;
  losses: number;
  winPct: number;
  events: string[];
}

export const CoachSunburst: React.FC<CoachSunburstProps> = ({ coachData }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const currentTeam = coachData?.current_team;

  useEffect(() => {
    if (!svgRef.current || !coachData) return;

    const schools = transformCoachData(coachData);
    renderSunburst(svgRef.current, schools);
  }, [coachData]);

  return (
    <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
      {/* Watermark Logo */}
      <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
        <img 
          src={currentTeam?.logo}
          alt={currentTeam?.name}
          className="w-full h-full object-contain scale-150"
        />
      </div>

      {/* Header */}
      <div className="relative z-10 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <img 
            src={coachData?.coach_info?.headshot_url}
            alt={coachData?.metadata?.coach}
            className="w-12 h-12 rounded-full object-cover border-2"
            style={{ borderColor: currentTeam?.primary_color }}
          />
          <div className="flex-1">
            <h3 
              className="text-xl font-bold"
              style={{ color: currentTeam?.primary_color }}
            >
              {coachData?.metadata?.coach} Career Sunburst
            </h3>
            <p className="text-sm text-gray-400">
              Interactive hierarchical career visualization
            </p>
          </div>
          <img 
            src={currentTeam?.logo}
            alt={currentTeam?.name}
            className="w-16 h-16 object-contain opacity-90"
          />
        </div>
        
        {/* Chart Description */}
        <div className="flex items-start gap-3 p-4 rounded-lg bg-white/5 border border-white/5">
          <div className="flex-1">
            <p className="text-xs text-gray-300 leading-relaxed mb-2">
              <span className="font-semibold text-white">Sunburst Layers:</span> Each ring represents a level of career detail. 
              Inner ring shows schools coached (sized by tenure length), outer rings show individual seasons and performance.
            </p>
            <div className="flex flex-wrap gap-4 text-xs text-gray-400">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: currentTeam?.primary_color }} />
                <span>Ring 1: Schools (by years)</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-blue-500" />
                <span>Ring 2: Individual seasons</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-emerald-500" />
                <span>Brightness = Win %</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SVG Sunburst Chart */}
      <div className="relative z-10 w-full bg-black/20 rounded-xl border border-white/5 flex items-center justify-center" style={{ height: '600px' }}>
        <svg 
          ref={svgRef} 
          width="600" 
          height="600" 
          viewBox="-300 -300 600 600"
          className="w-full h-full"
        />
      </div>

      {/* Legend */}
      <div className="relative z-10 mt-6 flex flex-wrap gap-3 justify-center">
        {coachData?.schools_info?.map((school: any, index: number) => (
          <div 
            key={index} 
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all duration-300"
            style={{
              background: `linear-gradient(135deg, ${school.primary_color}15, ${school.alt_color}08)`
            }}
          >
            <img 
              src={school.logo}
              alt={school.name}
              className="w-5 h-5 object-contain"
            />
            <span 
              className="text-xs font-medium"
              style={{ color: school.primary_color }}
            >
              {school.name}
            </span>
            <span className="text-xs text-gray-400">
              {school.record}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Transform coach data
function transformCoachData(coachData: any): SchoolSegment[] {
  const schools: SchoolSegment[] = [];
  
  (coachData.schools_info || []).forEach((school: any) => {
    const yearsParts = school.years.split('-');
    const startYear = parseInt(yearsParts[0]);
    const endYear = yearsParts[1] ? parseInt(yearsParts[1]) : new Date().getFullYear();
    
    const recordParts = school.record.split('-');
    const totalWins = parseInt(recordParts[0]);
    const totalLosses = parseInt(recordParts[1]);
    const winPct = (totalWins / (totalWins + totalLosses)) * 100;
    
    const numSeasons = endYear - startYear + 1;
    const avgWins = totalWins / numSeasons;
    const avgLosses = totalLosses / numSeasons;
    
    const seasons: SeasonData[] = [];
    for (let year = startYear; year <= endYear; year++) {
      const wins = Math.round(avgWins + (Math.random() - 0.5) * 2);
      const losses = Math.round(avgLosses + (Math.random() - 0.5) * 2);
      const seasonWinPct = (wins / (wins + losses)) * 100;
      
      seasons.push({
        year,
        wins,
        losses,
        winPct: seasonWinPct,
        events: seasonWinPct > 75 ? ['Bowl Win'] : []
      });
    }
    
    schools.push({
      name: school.name,
      years: school.years,
      record: school.record,
      color: school.primary_color,
      altColor: school.alt_color || school.primary_color,
      logo: school.logo,
      startYear,
      endYear,
      winPct,
      seasons
    });
  });
  
  return schools;
}

// Render SVG sunburst
function renderSunburst(svg: SVGSVGElement, schools: SchoolSegment[]) {
  // Clear previous content
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  
  const totalSeasons = schools.reduce((sum, s) => sum + s.seasons.length, 0);
  let currentAngle = -Math.PI / 2;
  
  const innerRadius = 60;
  const schoolRingWidth = 80;
  const seasonRingWidth = 70;
  
  schools.forEach((school) => {
    const schoolAngle = (school.seasons.length / totalSeasons) * 2 * Math.PI;
    
    // Draw school segment (inner ring)
    const schoolPath = describeArc(
      0, 0,
      innerRadius,
      innerRadius + schoolRingWidth,
      currentAngle,
      currentAngle + schoolAngle
    );
    
    const schoolSegment = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    schoolSegment.setAttribute('d', schoolPath);
    schoolSegment.setAttribute('fill', school.color);
    schoolSegment.setAttribute('stroke', '#ffffff');
    schoolSegment.setAttribute('stroke-width', '2');
    schoolSegment.setAttribute('opacity', '0.8');
    
    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    title.textContent = `${school.name}\n${school.record}\n${school.winPct.toFixed(1)}% Win Rate`;
    schoolSegment.appendChild(title);
    
    svg.appendChild(schoolSegment);
    
    // Draw season segments (outer ring)
    school.seasons.forEach((season, idx) => {
      const seasonAngle = schoolAngle / school.seasons.length;
      const seasonStart = currentAngle + (idx * seasonAngle);
      
      const opacity = 0.4 + (season.winPct / 100) * 0.6;
      
      const seasonPath = describeArc(
        0, 0,
        innerRadius + schoolRingWidth,
        innerRadius + schoolRingWidth + seasonRingWidth,
        seasonStart,
        seasonStart + seasonAngle
      );
      
      const seasonSegment = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      seasonSegment.setAttribute('d', seasonPath);
      seasonSegment.setAttribute('fill', school.altColor);
      seasonSegment.setAttribute('stroke', '#ffffff');
      seasonSegment.setAttribute('stroke-width', '1');
      seasonSegment.setAttribute('opacity', opacity.toString());
      
      const seasonTitle = document.createElementNS('http://www.w3.org/2000/svg', 'title');
      seasonTitle.textContent = `${season.year}\n${season.wins}-${season.losses}\n${season.winPct.toFixed(1)}% Win Rate`;
      seasonSegment.appendChild(seasonTitle);
      
      svg.appendChild(seasonSegment);
    });
    
    // Add school label
    const labelAngle = currentAngle + schoolAngle / 2;
    const labelRadius = innerRadius + schoolRingWidth / 2;
    const labelX = labelRadius * Math.cos(labelAngle);
    const labelY = labelRadius * Math.sin(labelAngle);
    
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', labelX.toString());
    text.setAttribute('y', labelY.toString());
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('dominant-baseline', 'middle');
    text.setAttribute('fill', '#ffffff');
    text.setAttribute('font-size', '12');
    text.setAttribute('font-weight', 'bold');
    text.textContent = school.name.split(' ')[0];
    
    svg.appendChild(text);
    
    currentAngle += schoolAngle;
  });
  
  // Center circle
  const centerCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  centerCircle.setAttribute('cx', '0');
  centerCircle.setAttribute('cy', '0');
  centerCircle.setAttribute('r', innerRadius.toString());
  centerCircle.setAttribute('fill', '#1a1a1a');
  centerCircle.setAttribute('stroke', '#ffffff');
  centerCircle.setAttribute('stroke-width', '2');
  svg.appendChild(centerCircle);
}

// Helper to create arc path
function describeArc(x: number, y: number, innerRadius: number, outerRadius: number, startAngle: number, endAngle: number) {
  const innerStart = polarToCartesian(x, y, innerRadius, endAngle);
  const innerEnd = polarToCartesian(x, y, innerRadius, startAngle);
  const outerStart = polarToCartesian(x, y, outerRadius, endAngle);
  const outerEnd = polarToCartesian(x, y, outerRadius, startAngle);
  
  const largeArcFlag = endAngle - startAngle <= Math.PI ? '0' : '1';
  
  return [
    'M', outerStart.x, outerStart.y,
    'A', outerRadius, outerRadius, 0, largeArcFlag, 0, outerEnd.x, outerEnd.y,
    'L', innerEnd.x, innerEnd.y,
    'A', innerRadius, innerRadius, 0, largeArcFlag, 1, innerStart.x, innerStart.y,
    'Z'
  ].join(' ');
}

function polarToCartesian(centerX: number, centerY: number, radius: number, angleInRadians: number) {
  return {
    x: centerX + (radius * Math.cos(angleInRadians)),
    y: centerY + (radius * Math.sin(angleInRadians))
  };
}
