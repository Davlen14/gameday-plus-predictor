import React from 'react';
import { GlassCard } from './GlassCard';
import { BarChart3 } from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';

// StatComparison Component
const StatComparison = ({ label, awayValue, homeValue, awayLabel, homeLabel, higherBetter, awayTeam, homeTeam }: {
  label: string;
  awayValue: number;
  homeValue: number;
  awayLabel: string;
  homeLabel: string;
  higherBetter: boolean;
  awayTeam: any;
  homeTeam: any;
}) => {
  // Calculate percentages for bar widths
  const total = awayValue + homeValue;
  const awayPercent = (awayValue / total) * 100;
  const homePercent = (homeValue / total) * 100;

  // Determine which team is better
  const awayBetter = higherBetter ? awayValue > homeValue : awayValue < homeValue;
  const homeBetter = higherBetter ? homeValue > awayValue : homeValue < awayValue;

  return (
    <div className="space-y-2">
      {/* Header with label and values */}
      <div className="flex justify-between items-center">
        <span className="text-gray-300 text-sm">{label}</span>
        <div className="flex gap-4 text-xs items-center">
          {/* Color-coded values with team logos */}
          <div className="flex items-center gap-1">
            <ImageWithFallback 
              src={awayTeam.logo} 
              alt={generateTeamAbbr(awayTeam.name)} 
              className="w-4 h-4 object-contain team-logo-3d"
            />
            <span className={`font-mono ${awayBetter ? 'text-emerald-400' : 'text-gray-400'}`}>
              {awayLabel}
            </span>
          </div>
          <span className="text-gray-500">vs</span>
          <div className="flex items-center gap-1">
            <ImageWithFallback 
              src={homeTeam.logo} 
              alt={generateTeamAbbr(homeTeam.name)} 
              className="w-4 h-4 object-contain team-logo-3d"
            />
            <span className={`font-mono ${homeBetter ? 'text-emerald-400' : 'text-gray-400'}`}>
              {homeLabel}
            </span>
          </div>
        </div>
      </div>

      {/* Two-tone progress bar */}
      <div className="flex h-2 rounded-full overflow-hidden bg-gray-800/40">
        {/* Away team bar - extends from left */}
        <div 
          className="transition-all duration-500"
          style={{ 
            width: `${awayPercent}%`,
            backgroundColor: awayBetter ? awayTeam.primary_color : `${awayTeam.primary_color}80`
          }}
        />
        {/* Home team bar - extends from right */}
        <div 
          className="transition-all duration-500"
          style={{ 
            width: `${homePercent}%`,
            backgroundColor: homeBetter ? homeTeam.primary_color : `${homeTeam.primary_color}80`
          }}
        />
      </div>
    </div>
  );
};

interface AdvancedMetricsProps {
  predictionData?: any;
}

export function AdvancedMetrics({ predictionData }: AdvancedMetricsProps) {
  const homeTeam = predictionData?.team_selector?.home_team;
  const awayTeam = predictionData?.team_selector?.away_team;

  if (!homeTeam || !awayTeam) {
    return null; // Return nothing instead of loading message
  }

  // Parse advanced metrics from formatted_analysis section [15] - ADVANCED OFFENSIVE METRICS
  const parseAdvancedMetrics = () => {
    const advancedSection = predictionData?.formatted_analysis ? 
      extractSection(predictionData.formatted_analysis, 15) : null;
    
    // Parse values from the "ADVANCED OFFENSIVE METRICS:" table
    const parseMetric = (metricName: string) => {
      if (!advancedSection) return { away: 0, home: 0 };
      
      // Pattern: "Metric                         Away (TeamName)                   Home (TeamName)                        Advantage"
      // Example: "Offense PPA                    0.178                               0.286                               Home"
      const pattern = new RegExp(`${metricName}\\s+([\\d.]+)%?\\s+([\\d.]+)%?`, 'i');
      const match = advancedSection.match(pattern);
      
      if (match) {
        return {
          away: parseFloat(match[1]),
          home: parseFloat(match[2])
        };
      }
      return { away: 0, home: 0 };
    };
    
    const offensePPA = parseMetric('Offense PPA');
    const successRate = parseMetric('Success Rate');
    const explosiveness = parseMetric('Explosiveness');
    const powerSuccess = parseMetric('Power Success');
    const stuffRate = parseMetric('Stuff Rate');
    const lineYards = parseMetric('Line Yards');
    const secondLevel = parseMetric('Second Level Yards');
    const openField = parseMetric('Open Field Yards');
    
    return [
      { 
        metric: 'PPA', 
        AWAY: offensePPA.away, 
        HOME: offensePPA.home, 
        higherBetter: true, 
        unit: '' 
      },
      { 
        metric: 'Success Rate', 
        AWAY: successRate.away, 
        HOME: successRate.home, 
        higherBetter: true, 
        unit: '%' 
      },
      { 
        metric: 'Explosiveness', 
        AWAY: explosiveness.away, 
        HOME: explosiveness.home, 
        higherBetter: true, 
        unit: '' 
      },
      { 
        metric: 'Power Success', 
        AWAY: powerSuccess.away, 
        HOME: powerSuccess.home, 
        higherBetter: true, 
        unit: '%' 
      },
      { 
        metric: 'Stuff Rate', 
        AWAY: stuffRate.away, 
        HOME: stuffRate.home, 
        higherBetter: false, 
        unit: '%' 
      },
      { 
        metric: 'Line Yards', 
        AWAY: lineYards.away, 
        HOME: lineYards.home, 
        higherBetter: true, 
        unit: '' 
      },
      { 
        metric: 'Second Level', 
        AWAY: secondLevel.away, 
        HOME: secondLevel.home, 
        higherBetter: true, 
        unit: '' 
      },
      { 
        metric: 'Open Field', 
        AWAY: openField.away, 
        HOME: openField.home, 
        higherBetter: true, 
        unit: '' 
      }
    ];
  };

  const offensiveMetrics = parseAdvancedMetrics();

  // Normalize data for radar chart (0-100 scale)
  const radarData = offensiveMetrics.map(metric => {
    const max = Math.max(metric.AWAY, metric.HOME);
    const min = Math.min(metric.AWAY, metric.HOME);
    const range = max - min || 1;
    
    return {
      metric: metric.metric,
      AWAY: ((metric.AWAY - min) / range) * 100,
      HOME: ((metric.HOME - min) / range) * 100,
    };
  });

  const teams = {
    away: { name: awayTeam.name, abbreviation: generateTeamAbbr(awayTeam.name), color: awayTeam.primary_color },
    home: { name: homeTeam.name, abbreviation: generateTeamAbbr(homeTeam.name), color: homeTeam.primary_color }
  };

  // Calculate team advantages
  const awayAdvantages = offensiveMetrics.filter(metric => 
    metric.higherBetter ? metric.AWAY > metric.HOME : metric.AWAY < metric.HOME
  ).map(m => m.metric);

  const homeAdvantages = offensiveMetrics.filter(metric => 
    metric.higherBetter ? metric.HOME > metric.AWAY : metric.HOME < metric.AWAY
  ).map(m => m.metric);

  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          Advanced Offensive Metrics
        </h3>
      </div>

      {/* Main Content - Two Column Layout */}
      <div className="glass-card-light rounded-lg p-5">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Radar Chart */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-gray-300 font-semibold text-lg" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Performance Overview
              </h4>
              {/* Team Logos in Header */}
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <ImageWithFallback 
                    src={awayTeam.logo} 
                    alt={teams.away.name} 
                    className="w-6 h-6 object-contain team-logo-3d"
                  />
                  <span className="text-sm font-mono" style={{color: teams.away.color}}>{teams.away.abbreviation}</span>
                </div>
                <span className="text-gray-500 text-xs">vs</span>
                <div className="flex items-center gap-2">
                  <ImageWithFallback 
                    src={homeTeam.logo} 
                    alt={teams.home.name} 
                    className="w-6 h-6 object-contain team-logo-3d"
                  />
                  <span className="text-sm font-mono" style={{color: teams.home.color}}>{teams.home.abbreviation}</span>
                </div>
              </div>
            </div>
            <div className="h-[500px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(148, 163, 184, 0.2)" />
                  <PolarAngleAxis 
                    dataKey="metric" 
                    stroke="#94a3b8"
                    style={{ fontSize: '11px', fontFamily: 'Orbitron, sans-serif' }}
                  />
                  <Radar 
                    name={teams.away.abbreviation}
                    dataKey="AWAY" 
                    stroke={teams.away.color}
                    fill={teams.away.color} 
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Radar 
                    name={teams.home.abbreviation}
                    dataKey="HOME" 
                    stroke={teams.home.color}
                    fill={teams.home.color} 
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'rgba(37, 43, 54, 0.9)',
                      border: '1px solid rgba(148, 163, 184, 0.2)',
                      borderRadius: '8px',
                      backdropFilter: 'blur(16px)',
                      color: '#e2e8f0'
                    }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Right: Progress Bars + Team Edges */}
          <div className="space-y-4">
            <h4 className="text-gray-300 font-semibold text-lg" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              Detailed Comparison
            </h4>
            
            {/* Progress Bars */}
            <div className="space-y-4">
              {offensiveMetrics.map((metric, index) => (
                <StatComparison
                  key={index}
                  label={metric.metric}
                  awayValue={metric.AWAY}
                  homeValue={metric.HOME}
                  awayLabel={`${metric.AWAY}${metric.unit}`}
                  homeLabel={`${metric.HOME}${metric.unit}`}
                  higherBetter={metric.higherBetter}
                  awayTeam={awayTeam}
                  homeTeam={homeTeam}
                />
              ))}
            </div>

            {/* Team Edge Cards */}
            <div className="mt-6 grid grid-cols-2 gap-3">
              {/* Away Team Edge Card */}
              <div className="glass-card rounded-lg p-3" style={{border: `1px solid ${teams.away.color}30`}}>
                <div className="flex items-center gap-2 mb-2">
                  <ImageWithFallback 
                    src={awayTeam.logo} 
                    alt={teams.away.name} 
                    className="w-5 h-5 object-contain team-logo-3d"
                  />
                  <p className="text-xs text-gray-400" 
                     style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {teams.away.name}
                  </p>
                </div>
                <p className="font-semibold text-xs" 
                   style={{ fontFamily: 'Orbitron, sans-serif', color: teams.away.color }}>
                  {teams.away.abbreviation} Edge
                </p>
                <p className="text-gray-400 text-xs mt-1">
                  {awayAdvantages.length > 0 ? awayAdvantages.slice(0, 3).join(', ') : 'None'}
                </p>
              </div>

              {/* Home Team Edge Card */}
              <div className="glass-card rounded-lg p-3" style={{border: `1px solid ${teams.home.color}30`}}>
                <div className="flex items-center gap-2 mb-2">
                  <ImageWithFallback 
                    src={homeTeam.logo} 
                    alt={teams.home.name} 
                    className="w-5 h-5 object-contain team-logo-3d"
                  />
                  <p className="text-xs text-gray-400" 
                     style={{ fontFamily: 'Orbitron, sans-serif' }}>
                    {teams.home.name}
                  </p>
                </div>
                <p className="font-semibold text-xs" 
                   style={{ fontFamily: 'Orbitron, sans-serif', color: teams.home.color }}>
                  {teams.home.abbreviation} Edge
                </p>
                <p className="text-gray-400 text-xs mt-1">
                  {homeAdvantages.length > 0 ? homeAdvantages.slice(0, 3).join(', ') : 'None'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
