import { GlassCard } from './GlassCard';
import { BarChart3, TrendingUp, Shield, Target, Clock, Trophy, Check, Zap, Activity, ArrowUp } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';

// Horizontal Bar Chart for Advanced Offensive Metrics
const HorizontalBarChart = ({ data, awayTeam, homeTeam }: { 
  data: Array<{ metric: string; away: number; home: number; advantage: string }>;
  awayTeam: any;
  homeTeam: any;
}) => {
  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get display colors
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam.primary_color || '#f97316');

  const awayAbbr = generateTeamAbbr(awayTeam.name);
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  
  return (
    <div className="space-y-6">
      {data.map((item, index) => {
        const maxVal = Math.max(item.away, item.home);
        const awayPercent = (item.away / maxVal) * 100;
        const homePercent = (item.home / maxVal) * 100;
        
        return (
          <div key={index} className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-white font-medium text-sm">{item.metric}</span>
              <div className="flex items-center gap-4 text-xs">
                <span className="font-mono font-bold" style={{ color: awayTeamColor }}>{item.away}</span>
                <span className="text-slate-400">vs</span>
                <span className="font-mono font-bold" style={{ color: homeTeamColor }}>{item.home}</span>
              </div>
            </div>
            
            <div className="space-y-2">
              {/* Away Team Bar */}
              <div className="flex items-center gap-3">
                <ImageWithFallback 
                  src={awayTeam.logo} 
                  alt={awayAbbr} 
                  className="w-5 h-5 object-contain"
                />
                <div className="flex-1 bg-slate-800/50 rounded-full h-2 overflow-hidden">
                  <div 
                    className="h-full transition-all duration-1000 ease-out"
                    style={{ 
                      width: `${awayPercent}%`,
                      background: `linear-gradient(to right, ${awayTeamColor}, ${awayTeamColor}80)`
                    }}
                  />
                </div>
              </div>
              
              {/* Home Team Bar */}
              <div className="flex items-center gap-3">
                <ImageWithFallback 
                  src={homeTeam.logo} 
                  alt={homeAbbr} 
                  className="w-5 h-5 object-contain"
                />
                <div className="flex-1 bg-slate-800/50 rounded-full h-2 overflow-hidden">
                  <div 
                    className="h-full transition-all duration-1000 ease-out"
                    style={{ 
                      width: `${homePercent}%`,
                      background: `linear-gradient(to right, ${homeTeamColor}, ${homeTeamColor}80)`
                    }}
                  />
                </div>
              </div>
            </div>
            
            {item.advantage !== 'Even' && (
              <div className="text-center">
                <span 
                  className="text-xs font-bold px-2 py-1 rounded-full border"
                  style={{
                    backgroundColor: `${item.advantage === awayTeam.name ? awayTeamColor : homeTeamColor}20`,
                    color: item.advantage === awayTeam.name ? awayTeamColor : homeTeamColor,
                    borderColor: `${item.advantage === awayTeam.name ? awayTeamColor : homeTeamColor}30`
                  }}
                >
                  {item.advantage} leads
                </span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

// Circular Progress Chart for Defense
const CircularProgressChart = ({ data, awayTeam, homeTeam }: { 
  data: Array<{ metric: string; away: number; home: number; advantage: string }>;
  awayTeam: any;
  homeTeam: any;
}) => {
  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get display colors
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam.primary_color || '#f97316');
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {data.map((item, index) => {
        const maxVal = Math.max(Math.abs(item.away), Math.abs(item.home));
        const awayPercent = Math.abs(item.away) / maxVal * 100;
        const homePercent = Math.abs(item.home) / maxVal * 100;
        
        return (
          <div key={index} className="text-center space-y-3">
            <h4 className="text-white text-sm font-medium">{item.metric}</h4>
            
            {/* Dual Circle Progress */}
            <div className="flex justify-center gap-4">
              {/* Away Team Circle */}
              <div className="relative w-16 h-16">
                <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="28" stroke="#374151" strokeWidth="4" fill="transparent" />
                  <circle 
                    cx="32" cy="32" r="28" 
                    stroke={awayTeamColor} 
                    strokeWidth="4" 
                    fill="transparent"
                    strokeDasharray={`${awayPercent * 1.76} 176`}
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <ImageWithFallback 
                    src={awayTeam.logo} 
                    alt={generateTeamAbbr(awayTeam.name)} 
                    className="w-6 h-6 object-contain"
                  />
                </div>
              </div>
              
              {/* Home Team Circle */}
              <div className="relative w-16 h-16">
                <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="28" stroke="#374151" strokeWidth="4" fill="transparent" />
                  <circle 
                    cx="32" cy="32" r="28" 
                    stroke={homeTeamColor} 
                    strokeWidth="4" 
                    fill="transparent"
                    strokeDasharray={`${homePercent * 1.76} 176`}
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <ImageWithFallback 
                    src={homeTeam.logo} 
                    alt={generateTeamAbbr(homeTeam.name)} 
                    className="w-6 h-6 object-contain"
                  />
                </div>
              </div>
            </div>
            
            {/* Values */}
            <div className="flex justify-center gap-4 text-xs">
              <span className="font-mono font-bold" style={{ color: awayTeamColor }}>{item.away}</span>
              <span className="font-mono font-bold" style={{ color: homeTeamColor }}>{item.home}</span>
            </div>
            
            {item.advantage !== 'Even' && (
              <div className="text-xs font-bold" style={{ 
                color: item.advantage === awayTeam.name ? awayTeamColor : homeTeamColor 
              }}>
                {item.advantage === awayTeam.name ? generateTeamAbbr(awayTeam.name) : generateTeamAbbr(homeTeam.name)} +
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

// Radar Chart Style for Game Control
const RadarStyleChart = ({ data, awayTeam, homeTeam }: { 
  data: Array<{ metric: string; away: string; home: string; advantage: string }>;
  awayTeam: any;
  homeTeam: any;
}) => {
  const parseValue = (val: string): number => {
    if (val.includes('%')) return parseFloat(val.replace('%', ''));
    if (val.includes(':')) {
      const [min, sec] = val.split(':').map(Number);
      return min + sec / 60;
    }
    if (val.startsWith('+')) return parseFloat(val.substring(1));
    return parseFloat(val.replace(/,/g, '')) || 0;
  };

  return (
    <div className="space-y-8">
      {data.map((item, index) => {
        const awayVal = parseValue(item.away);
        const homeVal = parseValue(item.home);
        const total = awayVal + homeVal;
        const awayPercent = total > 0 ? (awayVal / total) * 100 : 50;
        const homePercent = total > 0 ? (homeVal / total) * 100 : 50;
        
        return (
          <div key={index} className="relative">
            <div className="text-center mb-4">
              <h4 className="text-white text-lg font-bold mb-2">{item.metric}</h4>
              <div className="flex justify-center items-center gap-8">
                <div className="text-center">
                  <ImageWithFallback 
                    src={awayTeam.logo} 
                    alt={generateTeamAbbr(awayTeam.name)} 
                    className="w-8 h-8 object-contain mx-auto mb-2"
                  />
                  <span className="font-mono text-xl font-bold" style={{ color: awayTeam.primary_color }}>{item.away}</span>
                </div>
                
                <div className="text-center">
                  <ImageWithFallback 
                    src={homeTeam.logo} 
                    alt={generateTeamAbbr(homeTeam.name)} 
                    className="w-8 h-8 object-contain mx-auto mb-2"
                  />
                  <span className="font-mono text-xl font-bold" style={{ color: homeTeam.primary_color }}>{item.home}</span>
                </div>
              </div>
            </div>
            
            {/* Proportional comparison bar */}
            <div className="relative h-12 bg-slate-800/50 rounded-full overflow-hidden border-2 border-slate-600/30 shadow-xl">
              <div className="absolute inset-0 flex">
                <div 
                  className="h-full flex items-center justify-center transition-all duration-1500 ease-out"
                  style={{ 
                    width: `${awayPercent}%`,
                    background: `linear-gradient(to right, ${awayTeam.primary_color}, ${awayTeam.primary_color}, ${awayTeam.primary_color}80)`
                  }}
                >
                  <div className="flex items-center gap-2 text-white font-bold text-sm">
                    <ImageWithFallback 
                      src={awayTeam.logo} 
                      alt={generateTeamAbbr(awayTeam.name)} 
                      className="w-6 h-6 object-contain drop-shadow-lg"
                    />
                    <span className="drop-shadow-sm">{awayPercent.toFixed(1)}%</span>
                  </div>
                </div>
                <div 
                  className="h-full flex items-center justify-center transition-all duration-1500 ease-out"
                  style={{ 
                    width: `${homePercent}%`,
                    background: `linear-gradient(to left, ${homeTeam.primary_color}, ${homeTeam.primary_color}, ${homeTeam.primary_color}80)`
                  }}
                >
                  <div className="flex items-center gap-2 text-white font-bold text-sm">
                    <span className="drop-shadow-sm">{homePercent.toFixed(1)}%</span>
                    <ImageWithFallback 
                      src={homeTeam.logo} 
                      alt={generateTeamAbbr(homeTeam.name)} 
                      className="w-6 h-6 object-contain drop-shadow-lg"
                    />
                  </div>
                </div>
              </div>
              
              {/* Animated glow effect for the leading team */}
              <div 
                className="absolute inset-0 rounded-full transition-all duration-1000"
                style={{
                  boxShadow: awayPercent > homePercent 
                    ? `0 0 20px ${awayTeam.primary_color}40` 
                    : `0 0 20px ${homeTeam.primary_color}40`
                }}
              />
            </div>
            
            {item.advantage !== 'Even' && (
              <div className="text-center mt-3">
                <span 
                  className="inline-flex items-center gap-2 text-sm font-bold px-4 py-2 rounded-full border"
                  style={{
                    backgroundColor: `${item.advantage === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color}20`,
                    color: item.advantage === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color,
                    borderColor: `${item.advantage === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color}30`
                  }}
                >
                  <ArrowUp className="w-4 h-4" />
                  {item.advantage} advantage
                </span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

interface ComprehensiveTeamStatsProps {
  predictionData?: any;
}

export function ComprehensiveTeamStats({ predictionData }: ComprehensiveTeamStatsProps) {
  const homeTeam = predictionData?.team_selector?.home_team;
  const awayTeam = predictionData?.team_selector?.away_team;

  if (!homeTeam || !awayTeam) {
    return null;
  }

  const awayAbbr = generateTeamAbbr(awayTeam.name);
  const homeAbbr = generateTeamAbbr(homeTeam.name);

  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get display colors - use alt_color if primary is blue/black
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam.primary_color || '#f97316');

  // Parse advanced offensive metrics from section [15] - ADVANCED OFFENSIVE METRICS
  const parseAdvancedOffensive = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 15) : null;
    
    if (!section) {
      return [
        { metric: 'Offense PPA', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Success Rate', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Explosiveness', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Power Success', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Stuff Rate', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Line Yards', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Second Level Yards', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Open Field Yards', away: 0, home: 0, advantage: 'Even' },
      ];
    }

    // Helper to parse metric rows
    const parseMetric = (metricName: string) => {
      // Pattern: "Metric                         Away (TeamName)                   Home (TeamName)                        Advantage"
      // Example: "Offense PPA                    0.178                               0.286                               Home"
      const pattern = new RegExp(`${metricName}\\s+([\\d.]+)%?\\s+([\\d.]+)%?\\s+(\\w+)`, 'i');
      const match = section.match(pattern);
      
      if (match) {
        const advantageRaw = match[3].trim();
        // Map "Home" or "Away" to actual team names
        const advantage = advantageRaw === 'Home' ? homeTeam.name : 
                         advantageRaw === 'Away' ? awayTeam.name : 
                         'Even';
        return {
          metric: metricName,
          away: parseFloat(match[1]),
          home: parseFloat(match[2]),
          advantage
        };
      }
      return { metric: metricName, away: 0, home: 0, advantage: 'Even' };
    };

    return [
      parseMetric('Offense PPA'),
      parseMetric('Success Rate'),
      parseMetric('Explosiveness'),
      parseMetric('Power Success'),
      parseMetric('Stuff Rate'),
      parseMetric('Line Yards'),
      parseMetric('Second Level Yards'),
      parseMetric('Open Field Yards'),
    ];
  };

  // Data for Advanced Offensive Metrics - Horizontal Bar Chart
  const advancedOffensiveData = parseAdvancedOffensive();

  // Parse defensive metrics from section [15] - DEFENSIVE STATISTICS & ADVANCED DEFENSIVE METRICS
  const parseDefensiveData = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 15) : null;
    
    if (!section) {
      return [
        { metric: 'Sacks', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Interceptions', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Tackles for Loss', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Fumbles Recovered', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Defense PPA', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Defense Success Rate', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Defense Explosiveness', away: 0, home: 0, advantage: 'Even' },
        { metric: 'Defense Havoc Total', away: 0, home: 0, advantage: 'Even' },
      ];
    }

    // Helper to parse defensive metric rows
    const parseMetric = (metricName: string) => {
      // Pattern: "Metric                         Away (TeamName)                   Home (TeamName)                        Advantage"
      // Example: "Sacks                          14                                  12                                  Away"
      const pattern = new RegExp(`${metricName}\\s+([\\d.\\-]+)%?\\s+([\\d.\\-]+)%?\\s+(\\w+)`, 'i');
      const match = section.match(pattern);
      
      if (match) {
        const advantageRaw = match[3].trim();
        // Map "Home" or "Away" to actual team names
        const advantage = advantageRaw === 'Home' ? homeTeam.name : 
                         advantageRaw === 'Away' ? awayTeam.name : 
                         'Even';
        return {
          metric: metricName,
          away: parseFloat(match[1]),
          home: parseFloat(match[2]),
          advantage
        };
      }
      return { metric: metricName, away: 0, home: 0, advantage: 'Even' };
    };

    return [
      parseMetric('Sacks'),
      parseMetric('Interceptions'),
      parseMetric('Tackles for Loss'),
      parseMetric('Fumbles Recovered'),
      parseMetric('Defense PPA'),
      parseMetric('Defense Success Rate'),
      parseMetric('Defense Explosiveness'),
      parseMetric('Defense Havoc Total'),
    ];
  };

  // Data for Defensive Statistics - Circular Progress
  const defensiveData = parseDefensiveData();

  // Parse game control metrics from section [15]
  const parseGameControl = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 15) : null;
    
    if (!section) {
      return [
        { metric: 'Possession Time', away: '0:00', home: '0:00', advantage: 'Even' },
        { metric: 'Turnover Margin', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Penalty Yards', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Games Played', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Drives Per Game', away: '0', home: '0', advantage: 'Even' },
      ];
    }

    // Helper to parse game control rows
    const parseRow = (metricName: string) => {
      // Pattern: "Metric                         Away (TeamName)                   Home (TeamName)                        Advantage"
      // Example: "Possession Time                158:46                              164:59                              Home"
      // Example: "Drives Per Game                10.0                                9.3                                 Away"
      const pattern = new RegExp(`${metricName}\\s+([\\d:+\\-.]+)\\s+([\\d:+\\-.]+)\\s+(\\w+)`, 'i');
      const match = section.match(pattern);
      
      if (match) {
        const advantageRaw = match[3].trim();
        // Map "Home" or "Away" to actual team names
        const advantage = advantageRaw === 'Home' ? homeTeam.name : 
                         advantageRaw === 'Away' ? awayTeam.name : 
                         'Even';
        return {
          metric: metricName,
          away: match[1].trim(),
          home: match[2].trim(),
          advantage
        };
      }
      return { metric: metricName, away: '0', home: '0', advantage: 'Even' };
    };

    return [
      parseRow('Possession Time'),
      parseRow('Turnover Margin'),
      parseRow('Penalty Yards'),
      parseRow('Games Played'),
      parseRow('Drives Per Game'),
    ];
  };

  // Data for Game Control Metrics - Radar Style
  const gameControlData = parseGameControl();

  return (
    <div className="space-y-8">
      {/* Advanced Offensive Metrics - Horizontal Bar Chart */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl border shadow-xl backdrop-blur-sm" style={{ 
              background: `linear-gradient(to bottom right, ${awayTeam.primary_color}20, ${homeTeam.primary_color}20)`,
              borderColor: `${awayTeam.primary_color}40`
            }}>
              <Activity className="w-8 h-8" style={{ color: awayTeam.primary_color }} />
            </div>
            <div>
              <h3 className="text-white font-bold text-2xl tracking-wide" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Advanced Offensive Metrics
              </h3>
              <p className="text-slate-300 text-sm">Elite performance analytics with horizontal comparison</p>
            </div>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="text-center">
              <ImageWithFallback 
                src={awayTeam.logo} 
                alt={awayAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: awayTeam.primary_color }}>
                {awayAbbr} leads {advancedOffensiveData.filter(d => d.advantage === awayTeam.name).length}
              </span>
            </div>
            <div className="text-center">
              <ImageWithFallback 
                src={homeTeam.logo} 
                alt={homeAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: homeTeam.primary_color }}>
                {homeAbbr} leads {advancedOffensiveData.filter(d => d.advantage === homeTeam.name).length}
              </span>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-slate-900/60 to-slate-800/40 rounded-2xl p-8 border border-white/10 backdrop-blur-md">
          <HorizontalBarChart data={advancedOffensiveData} awayTeam={awayTeam} homeTeam={homeTeam} />
        </div>
      </GlassCard>

      {/* Defensive Statistics - Circular Progress */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl border shadow-xl backdrop-blur-sm" style={{
              background: 'linear-gradient(to bottom right, rgb(239 68 68 / 0.2), rgb(249 115 22 / 0.2))',
              borderColor: 'rgb(239 68 68 / 0.4)'
            }}>
              <Shield className="w-8 h-8 text-red-400" />
            </div>
            <div>
              <h3 className="text-white font-bold text-2xl tracking-wide" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Defensive Statistics
              </h3>
              <p className="text-slate-300 text-sm">Defensive dominance with circular progress visualization</p>
            </div>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="text-center">
              <ImageWithFallback 
                src={awayTeam.logo} 
                alt={awayAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: awayTeamColor }}>
                {awayAbbr} leads {defensiveData.filter(d => d.advantage === awayTeam.name).length}
              </span>
            </div>
            <div className="text-center">
              <ImageWithFallback 
                src={homeTeam.logo} 
                alt={homeAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: homeTeamColor }}>
                {homeAbbr} leads {defensiveData.filter(d => d.advantage === homeTeam.name).length}
              </span>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-slate-900/60 to-slate-800/40 rounded-2xl p-8 border border-white/10 backdrop-blur-md">
          <CircularProgressChart data={defensiveData} awayTeam={awayTeam} homeTeam={homeTeam} />
        </div>
      </GlassCard>

      {/* Game Control Metrics - Radar Style */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl border shadow-xl backdrop-blur-sm" style={{
              background: 'linear-gradient(to bottom right, rgb(16 185 129 / 0.2), rgb(20 184 166 / 0.2))',
              borderColor: 'rgb(16 185 129 / 0.4)'
            }}>
              <Clock className="w-8 h-8 text-emerald-400" />
            </div>
            <div>
              <h3 className="text-white font-bold text-2xl tracking-wide" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Game Control Metrics
              </h3>
              <p className="text-slate-300 text-sm">Tempo and possession analytics with radar-style visualization</p>
            </div>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="text-center">
              <ImageWithFallback 
                src={awayTeam.logo} 
                alt={awayAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: awayTeam.primary_color }}>
                {awayAbbr} leads {gameControlData.filter(d => d.advantage === awayTeam.name).length}
              </span>
            </div>
            <div className="text-center">
              <ImageWithFallback 
                src={homeTeam.logo} 
                alt={homeAbbr} 
                className="w-12 h-12 object-contain mx-auto mb-2"
              />
              <span className="font-bold text-sm" style={{ color: homeTeam.primary_color }}>
                {homeAbbr} leads {gameControlData.filter(d => d.advantage === homeTeam.name).length}
              </span>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-slate-900/60 to-slate-800/40 rounded-2xl p-8 border border-white/10 backdrop-blur-md">
          <RadarStyleChart data={gameControlData} awayTeam={awayTeam} homeTeam={homeTeam} />
        </div>
      </GlassCard>
    </div>
  );
}


