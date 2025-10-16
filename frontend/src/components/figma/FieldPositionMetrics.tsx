import { GlassCard } from './GlassCard';
import { Grid3x3, Check } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';

interface FieldPositionMetricsProps {
  predictionData?: any;
}

export function FieldPositionMetrics({ predictionData }: FieldPositionMetricsProps) {
  // Parse field position data from API
  const parseFieldPositionData = () => {
    if (!predictionData?.formatted_analysis || !predictionData?.team_selector) {
      return {
        awayTeam: { name: "Away Team", logo: "", primary_color: "#6366f1" },
        homeTeam: { name: "Home Team", logo: "", primary_color: "#10b981" },
        awayStats: { lineYards: 2.5, secondLevel: 1.0, openField: 1.0, highlightYards: 1.5 },
        homeStats: { lineYards: 2.5, secondLevel: 1.0, openField: 1.0, highlightYards: 1.5 }
      };
    }

    const analysis = predictionData.formatted_analysis;
    const awayTeam = predictionData.team_selector.away_team;
    const homeTeam = predictionData.team_selector.home_team;
    const section10 = extractSection(analysis, 10);

    // Parse field position metrics from section [10]
    const awayStats = {
      lineYards: parseTeamValue(section10, awayTeam.name, 'Line Yards') || 2.5,
      secondLevel: parseTeamValue(section10, awayTeam.name, 'Second Level') || 1.0,
      openField: parseTeamValue(section10, awayTeam.name, 'Open Field') || 1.0,
      highlightYards: parseTeamValue(section10, awayTeam.name, 'Highlight') || 1.5
    };

    const homeStats = {
      lineYards: parseTeamValue(section10, homeTeam.name, 'Line Yards') || 2.5,
      secondLevel: parseTeamValue(section10, homeTeam.name, 'Second Level') || 1.0,
      openField: parseTeamValue(section10, homeTeam.name, 'Open Field') || 1.0,
      highlightYards: parseTeamValue(section10, homeTeam.name, 'Highlight') || 1.5
    };

    return { awayTeam, homeTeam, awayStats, homeStats };
  };

  const { awayTeam, homeTeam, awayStats, homeStats } = parseFieldPositionData();
  const awayAbbr = generateTeamAbbr(awayTeam.name);
  const homeAbbr = generateTeamAbbr(homeTeam.name);

  // Calculate zone averages and advantages
  const metrics = [
    { name: 'Line Yards', awayVal: awayStats.lineYards, homeVal: homeStats.lineYards },
    { name: 'Second Level', awayVal: awayStats.secondLevel, homeVal: homeStats.secondLevel },
    { name: 'Open Field', awayVal: awayStats.openField, homeVal: homeStats.openField },
    { name: 'Highlight Yards', awayVal: awayStats.highlightYards, homeVal: homeStats.highlightYards }
  ];

  const awayAdvantages = metrics.filter(m => m.awayVal > m.homeVal).length;
  const homeAdvantages = metrics.filter(m => m.homeVal > m.awayVal).length;
  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <Grid3x3 className="w-5 h-5 text-purple-400" />
          Field Position Metrics
        </h3>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1">
            <ImageWithFallback 
              src={awayTeam.logo} 
              alt={awayTeam.name} 
              className="w-6 h-6 object-contain"
              style={{
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                transform: 'perspective(100px) rotateX(15deg)'
              }}
            />
            <span className="text-sm font-semibold" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</span>
          </div>
          <span className="text-gray-500 text-sm">vs</span>
          <div className="flex items-center gap-1">
            <ImageWithFallback 
              src={homeTeam.logo} 
              alt={homeTeam.name} 
              className="w-6 h-6 object-contain"
              style={{
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                transform: 'perspective(100px) rotateX(15deg)'
              }}
            />
            <span className="text-sm font-semibold" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</span>
          </div>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {metrics.map((metric) => {
          const advantage = metric.awayVal > metric.homeVal ? 'AWAY' : 
                          metric.homeVal > metric.awayVal ? 'HOME' : 'EVEN';
          return (
            <FieldMetric 
              key={metric.name}
              title={metric.name}
              awayValue={metric.awayVal.toFixed(3)}
              homeValue={metric.homeVal.toFixed(3)}
              advantage={advantage}
              awayTeam={awayTeam}
              homeTeam={homeTeam}
              awayAbbr={awayAbbr}
              homeAbbr={homeAbbr}
            />
          );
        })}
      </div>

      {/* Visual Field Representation */}
      <div className="bg-gradient-to-r from-slate-800/40 via-slate-700/40 to-slate-800/40 rounded-lg p-4 border border-gray-400/15">
        <div className="text-center text-gray-400 text-xs mb-3">FIELD ZONES</div>
        <div className="grid grid-cols-4 gap-2">
          <ZoneCard zone="LINE" range="0-4 yds" value={((awayStats.lineYards + homeStats.lineYards) / 2).toFixed(2)} color="gray" />
          <ZoneCard zone="SECOND" range="5-10 yds" value={((awayStats.secondLevel + homeStats.secondLevel) / 2).toFixed(2)} color="purple" />
          <ZoneCard zone="OPEN" range="11-20 yds" value={((awayStats.openField + homeStats.openField) / 2).toFixed(2)} color="cyan" />
          <ZoneCard zone="HIGHLIGHT" range="20+ yds" value={((awayStats.highlightYards + homeStats.highlightYards) / 2).toFixed(2)} color="emerald" />
        </div>
        <div className="mt-4 flex items-center justify-center gap-4 text-xs">
          {awayAdvantages > homeAdvantages ? (
            <div className="flex items-center gap-2">
              <div className="relative">
                <ImageWithFallback 
                  src={awayTeam.logo} 
                  alt={awayTeam.name} 
                  className="w-5 h-5 object-contain"
                  style={{
                    filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                    transform: 'perspective(50px) rotateX(10deg)'
                  }}
                />
                <Check className="absolute -top-1 -right-1 w-3 h-3 text-green-400 bg-green-900/80 rounded-full p-0.5" />
              </div>
              <span className="font-semibold" style={{ color: awayTeam.primary_color }}>
                {awayAbbr} leads {awayAdvantages}/4 zones
              </span>
            </div>
          ) : homeAdvantages > awayAdvantages ? (
            <div className="flex items-center gap-2">
              <div className="relative">
                <ImageWithFallback 
                  src={homeTeam.logo} 
                  alt={homeTeam.name} 
                  className="w-5 h-5 object-contain"
                  style={{
                    filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                    transform: 'perspective(50px) rotateX(10deg)'
                  }}
                />
                <Check className="absolute -top-1 -right-1 w-3 h-3 text-green-400 bg-green-900/80 rounded-full p-0.5" />
              </div>
              <span className="font-semibold" style={{ color: homeTeam.primary_color }}>
                {homeAbbr} leads {homeAdvantages}/4 zones
              </span>
            </div>
          ) : (
            <span className="text-gray-400 font-semibold">Even split - {awayAdvantages}/4 each</span>
          )}
        </div>
      </div>
    </GlassCard>
  );
}

function FieldMetric({ 
  title, 
  awayValue, 
  homeValue, 
  advantage, 
  awayTeam, 
  homeTeam, 
  awayAbbr, 
  homeAbbr 
}: { 
  title: string; 
  awayValue: string; 
  homeValue: string; 
  advantage: 'AWAY' | 'HOME' | 'EVEN'; 
  awayTeam: any; 
  homeTeam: any; 
  awayAbbr: string;
  homeAbbr: string;
}) {
  return (
    <div className="bg-gray-800/40 rounded-lg p-3 border border-gray-400/15 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-400 text-xs">{title}</span>
        {advantage !== 'EVEN' && (
          <div className="relative">
            <ImageWithFallback 
              src={advantage === 'AWAY' ? awayTeam.logo : homeTeam.logo} 
              alt={advantage === 'AWAY' ? awayTeam.name : homeTeam.name} 
              className="w-4 h-4 object-contain"
              style={{
                filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))',
                transform: 'perspective(50px) rotateX(10deg)'
              }}
            />
            <Check className="absolute -top-0.5 -right-0.5 w-2 h-2 text-green-400 bg-green-900/80 rounded-full p-0.5" />
          </div>
        )}
      </div>
      <div className="flex flex-col gap-1">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1">
            <ImageWithFallback 
              src={awayTeam.logo} 
              alt={awayTeam.name} 
              className="w-3 h-3 object-contain"
              style={{
                filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))',
                transform: 'perspective(50px) rotateX(10deg)'
              }}
            />
            <span className={`text-sm font-mono ${advantage === 'AWAY' ? 'text-emerald-400 font-semibold' : 'text-gray-300'}`}>
              {awayValue}
            </span>
          </div>
          <span className="text-gray-500 text-xs">vs</span>
          <div className="flex items-center gap-1">
            <span className={`text-sm font-mono ${advantage === 'HOME' ? 'text-emerald-400 font-semibold' : 'text-gray-300'}`}>
              {homeValue}
            </span>
            <ImageWithFallback 
              src={homeTeam.logo} 
              alt={homeTeam.name} 
              className="w-3 h-3 object-contain"
              style={{
                filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))',
                transform: 'perspective(50px) rotateX(10deg)'
              }}
            />
          </div>
        </div>
        <div className="h-1.5 bg-gray-700/50 rounded-full overflow-hidden">
          <div 
            className="h-full rounded-full" 
            style={{ 
              width: '99.7%',
              background: advantage === 'AWAY' 
                ? `linear-gradient(to right, ${awayTeam.primary_color}70, ${homeTeam.primary_color}30)`
                : advantage === 'HOME'
                ? `linear-gradient(to right, ${awayTeam.primary_color}30, ${homeTeam.primary_color}70)`
                : `linear-gradient(to right, ${awayTeam.primary_color}50, ${homeTeam.primary_color}50)`
            }}
          ></div>
        </div>
      </div>
    </div>
  );
}

function ZoneCard({ zone, range, value, color }: { zone: string; range: string; value: string; color: string }) {
  const colors = {
    blue: 'bg-blue-500/20 border-blue-500/40 text-blue-400',
    purple: 'bg-purple-500/20 border-purple-500/40 text-purple-400',
    cyan: 'bg-cyan-500/20 border-cyan-500/40 text-cyan-400',
    emerald: 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400',
    gray: 'bg-gray-500/20 border-gray-500/40 text-gray-400'
  };

  return (
    <div className="text-center">
      <div className={`${colors[color as keyof typeof colors]} border rounded p-3 mb-2`}>
        <div className={`font-bold text-lg font-mono`}>{value}</div>
        <div className="text-xs mt-1 opacity-75">avg yards</div>
      </div>
      <div className="text-gray-400 text-xs font-semibold">{zone}</div>
      <div className="text-gray-500 text-xs">{range}</div>
    </div>
  );
}
