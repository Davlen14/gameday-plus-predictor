import { GlassCard } from './GlassCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { TrendingUp, Shield, Activity } from 'lucide-react';



interface EPAComparisonProps {
  predictionData?: any;
}

export function EPAComparison({ predictionData }: EPAComparisonProps) {
  // Live API data integration
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png", primary_color: "#ce1141" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/275.png", primary_color: "#c4012f" };
  
  // Extract EPA data from API formatted_analysis - needs parsing from the formatted text
  const parseEPAFromFormattedAnalysis = (formattedText: string) => {
    if (!formattedText) return null;
    
    const epaSection = formattedText.match(/🎯 \[7\] EPA COMPARISON[\s\S]*?(?=🎯 \[8\])/);
    if (!epaSection) return null;
    
    const section = epaSection[0];
    
    // Parse Overall EPA values
    const awayOverallMatch = section.match(new RegExp(`${awayTeam.name}:\\s*\\+([0-9.]+)`));
    const homeOverallMatch = section.match(new RegExp(`${homeTeam.name}:\\s*\\+([0-9.]+)`));
    
    // Parse EPA Allowed values  
    const awayAllowedMatch = section.match(new RegExp(`EPA Allowed:[\\s\\S]*?${awayTeam.name}:\\s*\\+([0-9.]+)`));
    const homeAllowedMatch = section.match(new RegExp(`EPA Allowed:[\\s\\S]*?${homeTeam.name}:\\s*\\+([0-9.]+)`));
    
    // Parse Passing EPA values
    const awayPassingMatch = section.match(new RegExp(`Passing EPA:[\\s\\S]*?${awayTeam.name}:\\s*\\+([0-9.]+)`));
    const homePassingMatch = section.match(new RegExp(`Passing EPA:[\\s\\S]*?${homeTeam.name}:\\s*\\+([0-9.]+)`));
    
    // Parse Rushing EPA values  
    const awayRushingMatch = section.match(new RegExp(`Rushing EPA:[\\s\\S]*?${awayTeam.name}:\\s*\\+([0-9.]+)`));
    const homeRushingMatch = section.match(new RegExp(`Rushing EPA:[\\s\\S]*?${homeTeam.name}:\\s*\\+([0-9.]+)`));
    
    return {
      awayOverallEPA: awayOverallMatch ? parseFloat(awayOverallMatch[1]) : 0.200,
      homeOverallEPA: homeOverallMatch ? parseFloat(homeOverallMatch[1]) : 0.150,
      awayEPAAllowed: awayAllowedMatch ? parseFloat(awayAllowedMatch[1]) : 0.100,
      homeEPAAllowed: homeAllowedMatch ? parseFloat(homeAllowedMatch[1]) : 0.120,
      awayPassingEPA: awayPassingMatch ? parseFloat(awayPassingMatch[1]) : 0.300,
      homePassingEPA: homePassingMatch ? parseFloat(homePassingMatch[1]) : 0.250,
      awayRushingEPA: awayRushingMatch ? parseFloat(awayRushingMatch[1]) : 0.080,
      homeRushingEPA: homeRushingMatch ? parseFloat(homeRushingMatch[1]) : 0.090,
    };
  };
  
  const epaData = parseEPAFromFormattedAnalysis(predictionData?.formatted_analysis) || {
    awayOverallEPA: 0.200,
    homeOverallEPA: 0.150,
    awayEPAAllowed: 0.100,
    homeEPAAllowed: 0.120,
    awayPassingEPA: 0.300,
    homePassingEPA: 0.250,
    awayRushingEPA: 0.080,
    homeRushingEPA: 0.090,
  };
  
  // Calculate differentials and determine advantages
  const overallDiff = epaData.awayOverallEPA - epaData.homeOverallEPA; // -0.123
  const epaAllowedDiff = epaData.homeEPAAllowed - epaData.awayEPAAllowed; // +0.113
  const passingDiff = epaData.awayPassingEPA - epaData.homePassingEPA;
  const rushingDiff = epaData.awayRushingEPA - epaData.homeRushingEPA;
  
  // Dynamic chart data
  const chartData = [
    { 
      name: 'Overall EPA', 
      [homeTeam.name.substring(0, 3)]: epaData.homeOverallEPA, 
      [awayTeam.name.substring(0, 3)]: epaData.awayOverallEPA 
    },
    { 
      name: 'EPA Allowed', 
      [homeTeam.name.substring(0, 3)]: -epaData.homeEPAAllowed, 
      [awayTeam.name.substring(0, 3)]: -epaData.awayEPAAllowed 
    },
    { 
      name: 'Passing EPA', 
      [homeTeam.name.substring(0, 3)]: epaData.homePassingEPA, 
      [awayTeam.name.substring(0, 3)]: epaData.awayPassingEPA 
    },
    { 
      name: 'Rushing EPA', 
      [homeTeam.name.substring(0, 3)]: epaData.homeRushingEPA, 
      [awayTeam.name.substring(0, 3)]: epaData.awayRushingEPA 
    },
  ];
  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-500/20 rounded-lg border border-emerald-500/40">
            <Activity className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-white font-semibold text-lg">EPA Comparison</h3>
            <p className="text-gray-400 text-sm">Expected Points Added per Play</p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/20 rounded-lg border border-emerald-500/40">
          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
          <span className="text-emerald-400 text-xs font-medium">LIVE ANALYTICS</span>
        </div>
      </div>

      {/* Quick EPA Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Overall EPA */}
        <div className="relative overflow-hidden rounded-lg bg-gray-800/40 border border-gray-600/40 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-400 text-sm font-semibold">Overall EPA</span>
            </div>
            <div className="px-2 py-1 bg-emerald-500/20 rounded text-emerald-400 text-xs font-medium">
              {overallDiff > 0 ? `${awayTeam.name.toUpperCase()} EDGE` : `${homeTeam.name.toUpperCase()} EDGE`}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 rounded-lg border" style={{ backgroundColor: `${homeTeam.primary_color}20`, borderColor: `${homeTeam.primary_color}40` }}>
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-5 h-5 object-contain" />
                <span className="text-xs font-medium" style={{ color: homeTeam.primary_color }}>{homeTeam.name.substring(0, 3).toUpperCase()}</span>
              </div>
              <div className="font-bold text-xl font-mono" style={{ color: homeTeam.primary_color }}>+{epaData.homeOverallEPA.toFixed(3)}</div>
            </div>
            <div className="text-center p-3 rounded-lg border" style={{ backgroundColor: `${awayTeam.primary_color}20`, borderColor: `${awayTeam.primary_color}40` }}>
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-5 h-5 object-contain" />
                <span className="text-xs font-medium" style={{ color: awayTeam.primary_color }}>{awayTeam.name.substring(0, 3).toUpperCase()}</span>
              </div>
              <div className="font-bold text-xl font-mono" style={{ color: awayTeam.primary_color }}>+{epaData.awayOverallEPA.toFixed(3)}</div>
            </div>
          </div>
        </div>

        {/* EPA Allowed */}
        <div className="relative overflow-hidden rounded-lg bg-gray-800/40 border border-gray-600/40 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-blue-400" />
              <span className="text-blue-400 text-sm font-semibold">EPA Allowed</span>
            </div>
            <div className="px-2 py-1 bg-emerald-500/20 rounded text-emerald-400 text-xs font-medium">
              {epaData.awayEPAAllowed < epaData.homeEPAAllowed ? `${awayTeam.name.toUpperCase()} EDGE` : `${homeTeam.name.toUpperCase()} EDGE`}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 rounded-lg border" style={{ backgroundColor: `${homeTeam.primary_color}20`, borderColor: `${homeTeam.primary_color}40` }}>
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-5 h-5 object-contain" />
                <span className="text-xs font-medium" style={{ color: homeTeam.primary_color }}>{homeTeam.name.substring(0, 3).toUpperCase()}</span>
              </div>
              <div className="font-bold text-xl font-mono" style={{ color: homeTeam.primary_color }}>+{epaData.homeEPAAllowed.toFixed(3)}</div>
            </div>
            <div className="text-center p-3 rounded-lg border" style={{ backgroundColor: `${awayTeam.primary_color}20`, borderColor: `${awayTeam.primary_color}40` }}>
              <div className="flex items-center justify-center gap-2 mb-2">
                <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-5 h-5 object-contain" />
                <span className="text-xs font-medium" style={{ color: awayTeam.primary_color }}>{awayTeam.name.substring(0, 3).toUpperCase()}</span>
              </div>
              <div className="font-bold text-xl font-mono" style={{ color: awayTeam.primary_color }}>+{epaData.awayEPAAllowed.toFixed(3)}</div>
            </div>
          </div>
        </div>

        {/* Net EPA Edge */}
        <div className="relative overflow-hidden rounded-lg bg-gradient-to-br from-emerald-500/20 to-emerald-500/5 border-2 border-emerald-500/40 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-400 text-sm font-semibold">Net EPA Edge</span>
            </div>
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
          </div>
          <div className="flex items-center justify-center gap-3">
            <ImageWithFallback 
              src={(overallDiff > 0 ? awayTeam : homeTeam).logo} 
              alt={(overallDiff > 0 ? awayTeam : homeTeam).name} 
              className="w-10 h-10 object-contain" 
            />
            <div className="text-center">
              <div className="text-emerald-400 font-bold text-3xl font-mono">+{Math.abs(overallDiff).toFixed(3)}</div>
              <div className="text-emerald-300 text-xs font-medium">per play</div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Passing EPA */}
        <div className="bg-[#2a3140] rounded-lg p-4 border border-[#3a4252]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-blue-400" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="12" r="2"/>
                <path d="M12 2v4m0 4v4m0 4v4" opacity="0.5"/>
              </svg>
              <span className="text-blue-400 font-semibold text-sm">Passing EPA</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-[10px] text-emerald-400">{passingDiff > 0 ? awayTeam.name.substring(0, 3).toUpperCase() : homeTeam.name.substring(0, 3).toUpperCase()}</span>
              <svg className="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
          <div className="space-y-3">
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-gray-400 text-xs">{homeTeam.name} Offense</span>
                <span className="font-bold text-sm font-mono" style={{ color: homeTeam.primary_color }}>+{epaData.homePassingEPA.toFixed(3)}</span>
              </div>
              <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ 
                  background: `linear-gradient(to right, ${homeTeam.primary_color}, ${homeTeam.primary_color})`, 
                  width: `${Math.min(100, (epaData.homePassingEPA / Math.max(epaData.homePassingEPA, epaData.awayPassingEPA)) * 100)}%` 
                }}></div>
              </div>
            </div>
            <div className="pt-2 mt-2 border-t border-[#3a4252]">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-gray-400 text-xs">{awayTeam.name} Offense</span>
                <span className="font-bold text-sm font-mono" style={{ color: awayTeam.primary_color }}>+{epaData.awayPassingEPA.toFixed(3)}</span>
              </div>
              <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ 
                  background: `linear-gradient(to right, ${awayTeam.primary_color}, ${awayTeam.primary_color})`, 
                  width: `${Math.min(100, (epaData.awayPassingEPA / Math.max(epaData.homePassingEPA, epaData.awayPassingEPA)) * 100)}%` 
                }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Rushing EPA */}
        <div className="bg-[#2a3140] rounded-lg p-4 border border-[#3a4252]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              <span className="text-emerald-400 font-semibold text-sm">Rushing EPA</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-[10px] text-emerald-400">{rushingDiff > 0 ? awayTeam.name.substring(0, 3).toUpperCase() : homeTeam.name.substring(0, 3).toUpperCase()}</span>
              <svg className="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
          <div className="space-y-3">
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-gray-400 text-xs">{homeTeam.name} Offense</span>
                <span className="font-bold text-sm font-mono" style={{ color: homeTeam.primary_color }}>+{epaData.homeRushingEPA.toFixed(3)}</span>
              </div>
              <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ 
                  background: `linear-gradient(to right, ${homeTeam.primary_color}, ${homeTeam.primary_color})`, 
                  width: `${Math.min(100, (epaData.homeRushingEPA / Math.max(epaData.homeRushingEPA, epaData.awayRushingEPA)) * 100)}%` 
                }}></div>
              </div>
            </div>
            <div className="pt-2 mt-2 border-t border-[#3a4252]">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-gray-400 text-xs">{awayTeam.name} Offense</span>
                <span className="font-bold text-sm font-mono" style={{ color: awayTeam.primary_color }}>+{epaData.awayRushingEPA.toFixed(3)}</span>
              </div>
              <div className="h-1.5 bg-[#1a1f28] rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ 
                  background: `linear-gradient(to right, ${awayTeam.primary_color}, ${awayTeam.primary_color})`, 
                  width: `${Math.min(100, (epaData.awayRushingEPA / Math.max(epaData.homeRushingEPA, epaData.awayRushingEPA)) * 100)}%` 
                }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Visual Comparison */}
      <div className="mb-4">
        <div className="text-center text-gray-400 text-[10px] mb-3 font-semibold tracking-wider">VISUAL COMPARISON</div>
        <div style={{ height: '300px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3a4252" />
              <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
              <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }} />
              <Legend 
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="rect"
                formatter={(value) => <span style={{ color: '#9ca3af', fontSize: '12px' }}>{value}</span>}
              />
              <Bar dataKey={homeTeam.name.substring(0, 3)} fill={homeTeam.primary_color} radius={[4, 4, 0, 0]} />
              <Bar dataKey={awayTeam.name.substring(0, 3)} fill={awayTeam.primary_color} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex items-start gap-3 p-4 rounded-lg border" style={{ 
          background: `linear-gradient(to right, ${homeTeam.primary_color}20, ${homeTeam.primary_color}05)`, 
          borderColor: `${homeTeam.primary_color}40` 
        }}>
          <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-8 h-8 object-contain mt-0.5" />
          <div className="flex-1">
            <div className="font-semibold text-sm mb-1" style={{ color: homeTeam.primary_color }}>{homeTeam.name} Strength</div>
            <div className="text-gray-300 text-sm">
              {epaData.homePassingEPA > epaData.homeRushingEPA ? "Passing offense focus" : "Rushing offense focus"}
            </div>
          </div>
        </div>
        <div className="flex items-start gap-3 p-4 rounded-lg border" style={{ 
          background: `linear-gradient(to left, ${awayTeam.primary_color}20, ${awayTeam.primary_color}05)`, 
          borderColor: `${awayTeam.primary_color}40` 
        }}>
          <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-8 h-8 object-contain mt-0.5" />
          <div className="flex-1">
            <div className="font-semibold text-sm mb-1" style={{ color: awayTeam.primary_color }}>{awayTeam.name} Strength</div>
            <div className="text-gray-300 text-sm">
              {epaData.awayPassingEPA > epaData.awayRushingEPA ? "Passing offense focus" : "Rushing offense focus"}
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
