import { GlassCard } from './GlassCard';
import { BarChart3, TrendingUp, Shield, Target, Clock, Trophy, Check, Zap, Activity, ArrowUp, CheckCircle, Skull, Grid } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';
import { useState } from 'react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip,
  CartesianGrid, Cell, ReferenceLine, Legend
} from 'recharts';

// Debug Data Display Component
const DebugDataDisplay = ({ title, data, show }: { title: string; data: any; show: boolean }) => {
  if (!show) return null;
  
  return (
    <div className="mt-4 p-4 bg-yellow-500/10 border-2 border-yellow-500 rounded-lg">
      <h4 className="text-yellow-500 font-bold mb-2">🔍 DEBUG: {title}</h4>
      {!data || Object.keys(data).length === 0 ? (
        <p className="text-red-500 font-bold">⚠️ NO DATA FOUND - Check path!</p>
      ) : (
        <div className="overflow-auto max-h-96">
          <table className="w-full text-xs text-left">
            <thead>
              <tr className="border-b border-yellow-500/30">
                <th className="p-2 text-yellow-400">Key</th>
                <th className="p-2 text-yellow-400">Value</th>
                <th className="p-2 text-yellow-400">Type</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data || {}).map(([key, value]) => (
                <tr key={key} className="border-b border-yellow-500/10 hover:bg-yellow-500/5">
                  <td className="p-2 font-mono text-yellow-300">{key}</td>
                  <td className="p-2 font-mono text-white">
                    {typeof value === 'object' ? JSON.stringify(value).substring(0, 100) + '...' : String(value)}
                  </td>
                  <td className="p-2 text-gray-400">{typeof value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// Modern Section Title Component
const SectionTitle = ({ icon: Icon, title, subtitle }: { icon: any, title: string, subtitle?: string }) => (
  <div className="flex items-center gap-3 mb-6">
    <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
      <Icon size={24} />
    </div>
    <div>
      <h3 className="text-xl font-bold text-white tracking-wide">{title}</h3>
      {subtitle && <p className="text-sm text-slate-400">{subtitle}</p>}
    </div>
  </div>
);

// Modern Win Probability Hero Card
const WinProbabilityHero = ({ awayTeam, homeTeam, winProb }: { 
  awayTeam: any, 
  homeTeam: any, 
  winProb: { away: number, home: number }
}) => {
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#06b6d4') 
    : (awayTeam.primary_color || '#06b6d4');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#f97316') 
    : (homeTeam.primary_color || '#f97316');

  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 p-8 flex flex-col justify-center">
      <div className="absolute top-0 right-0 p-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16"></div>
      <div className="absolute bottom-0 left-0 p-32 bg-orange-500/10 rounded-full blur-3xl -ml-16 -mb-16"></div>
      
      <div className="relative z-10 flex items-center justify-between gap-8 text-center">
        <div className="flex-1">
          <div className="flex items-center justify-center gap-2 mb-2">
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-12 h-12 object-contain" />
            <h2 className="text-3xl font-black text-white">{awayTeam.name}</h2>
          </div>
          <div className="text-5xl font-bold" style={{ color: awayTeamColor }}>{winProb.away}%</div>
          <p className="text-sm font-mono mt-2" style={{ color: `${awayTeamColor}99` }}>WIN PROBABILITY</p>
        </div>
        
        <div className="flex flex-col items-center">
          <span className="text-2xl font-bold text-slate-500">VS</span>
          <div className="h-1 w-12 bg-slate-700 my-4 rounded-full"></div>
        </div>

        <div className="flex-1">
          <div className="flex items-center justify-center gap-2 mb-2">
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-12 h-12 object-contain" />
            <h2 className="text-3xl font-black text-white">{homeTeam.name}</h2>
          </div>
          <div className="text-5xl font-bold" style={{ color: homeTeamColor }}>{winProb.home}%</div>
          <p className="text-sm font-mono mt-2" style={{ color: `${homeTeamColor}99` }}>WIN PROBABILITY</p>
        </div>
      </div>
      
      {/* Progress Bar */}
      <div className="mt-8 relative h-3 bg-slate-800 rounded-full overflow-hidden flex">
        <div 
          style={{ width: `${winProb.away}%`, backgroundColor: awayTeamColor }} 
          className="shadow-[0_0_15px_rgba(6,182,212,0.6)]"
        ></div>
        <div 
          style={{ width: `${winProb.home}%`, backgroundColor: homeTeamColor }} 
          className="shadow-[0_0_15px_rgba(249,115,22,0.6)]"
        ></div>
      </div>
    </div>
  );
};

// Team Identity DNA Radar Chart
const TeamIdentityRadar = ({ awayTeam, homeTeam, radarData }: { 
  awayTeam: any, 
  homeTeam: any, 
  radarData: any[]
}) => {
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#06b6d4') 
    : (awayTeam.primary_color || '#06b6d4');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#f97316') 
    : (homeTeam.primary_color || '#f97316');

  return (
    <GlassCard glowColor="from-blue-500/20 to-purple-500/20" className="p-6">
      <SectionTitle icon={Grid} title="Team Identity DNA" subtitle="Shape of the offense compared." />
      <div className="h-[350px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart outerRadius={120} data={radarData}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
            <Radar
              name={awayTeam.name}
              dataKey="away"
              stroke={awayTeamColor}
              strokeWidth={3}
              fill={awayTeamColor}
              fillOpacity={0.2}
            />
            <Radar
              name={homeTeam.name}
              dataKey="home"
              stroke={homeTeamColor}
              strokeWidth={3}
              fill={homeTeamColor}
              fillOpacity={0.2}
            />
            <RechartsTooltip 
              contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f1f5f9' }}
              itemStyle={{ color: '#e2e8f0' }}
              formatter={(value: any, name: string, props: any) => {
                const realKey = name === awayTeam.name ? 'realAway' : 'realHome';
                return [props.payload[realKey], name];
              }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex justify-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: awayTeamColor }}></div>
          <span className="text-sm text-slate-300">{awayTeam.name}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: homeTeamColor }}></div>
          <span className="text-sm text-slate-300">{homeTeam.name}</span>
        </div>
      </div>
    </GlassCard>
  );
};

// Field Tilt PPA Chart
const FieldTiltChart = ({ awayTeam, homeTeam, ppaData }: { 
  awayTeam: any, 
  homeTeam: any, 
  ppaData: any[]
}) => {
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#06b6d4') 
    : (awayTeam.primary_color || '#06b6d4');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#f97316') 
    : (homeTeam.primary_color || '#f97316');

  return (
    <GlassCard glowColor="from-emerald-500/20 to-teal-500/20" className="p-6">
      <SectionTitle icon={TrendingUp} title="Field Tilt (PPA)" subtitle="Who moves the chains more efficiently?" />
      <div className="h-[350px] w-full flex flex-col justify-center gap-4">
        {ppaData.map((item, idx) => {
          const maxVal = Math.max(Math.abs(item.away), Math.abs(item.home));
          const total = Math.abs(item.away) + Math.abs(item.home);
          const awayPct = total > 0 ? (Math.abs(item.away) / total) * 100 : 50;
          
          return (
            <div key={idx} className="group">
              <div className="flex justify-between text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">
                <span>{item.away.toFixed(2)}</span>
                <span className="text-white group-hover:text-blue-400 transition-colors">{item.category}</span>
                <span>{item.home.toFixed(2)}</span>
              </div>
              <div className="h-4 w-full bg-slate-900 rounded-full flex overflow-hidden relative">
                <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-700 z-10"></div>
                
                <div 
                  style={{ 
                    width: `${awayPct}%`,
                    background: `linear-gradient(to right, transparent, ${awayTeamColor})`
                  }} 
                  className="hover:opacity-80 transition-all duration-500 border-r border-slate-900"
                ></div>
                <div 
                  style={{ 
                    width: `${100 - awayPct}%`,
                    background: `linear-gradient(to left, transparent, ${homeTeamColor})`
                  }} 
                  className="hover:opacity-80 transition-all duration-500"
                ></div>
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-4 p-3 bg-slate-900/50 rounded-lg border border-slate-800 text-xs text-center text-slate-400">
        Larger bar = Higher Predicted Points Added (PPA) per play.
      </div>
    </GlassCard>
  );
};

// Havoc Meter Chart
const HavocMeterChart = ({ awayTeam, homeTeam, havocData }: { 
  awayTeam: any, 
  homeTeam: any, 
  havocData: any[]
}) => {
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#06b6d4') 
    : (awayTeam.primary_color || '#06b6d4');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#f97316') 
    : (homeTeam.primary_color || '#f97316');

  return (
    <GlassCard glowColor="from-red-500/20 to-pink-500/20" className="p-6">
      <SectionTitle icon={Skull} title="The Havoc Meter" subtitle="Defensive disruption plays (Sacks, TFLs, INTs)." />
      
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={havocData} layout="vertical" margin={{ left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
            <XAxis type="number" stroke="#94a3b8" />
            <YAxis dataKey="name" type="category" stroke="#e2e8f0" width={60} />
            <RechartsTooltip 
              cursor={{fill: '#334155', opacity: 0.2}}
              contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }}
            />
            <Bar dataKey="away" name={awayTeam.name} fill={awayTeamColor} radius={[0, 4, 4, 0]} barSize={20} />
            <Bar dataKey="home" name={homeTeam.name} fill={homeTeamColor} radius={[0, 4, 4, 0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </GlassCard>
  );
};

// Trenches Chart
const TrenchesChart = ({ awayTeam, homeTeam, trenchesData, powerSuccess, stuffRate }: { 
  awayTeam: any, 
  homeTeam: any, 
  trenchesData: any[],
  powerSuccess: { away: number, home: number },
  stuffRate: { away: number, home: number }
}) => {
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#06b6d4') 
    : (awayTeam.primary_color || '#06b6d4');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#f97316') 
    : (homeTeam.primary_color || '#f97316');

  return (
    <GlassCard glowColor="from-amber-500/20 to-yellow-500/20" className="p-6">
      <SectionTitle icon={Shield} title="Trench Warfare" subtitle="Yards gained by O-Line vs D-Line." />
      
      <div className="grid grid-cols-3 gap-4 mb-6">
        {trenchesData.map((d, i) => (
          <div key={i} className="flex flex-col items-center p-3 bg-slate-900 rounded-lg border border-slate-800">
            <span className="text-xs text-slate-500 mb-2 text-center h-8 flex items-center">{d.name}</span>
            <div className="flex items-end gap-2 h-20">
              <div className="flex flex-col items-center">
                <div style={{height: `${Math.min(d.away * 15, 75)}px`, backgroundColor: awayTeamColor}} className="w-4 rounded-t-sm"></div>
                <span className="text-xs font-bold mt-1" style={{ color: awayTeamColor }}>{d.away.toFixed(1)}</span>
              </div>
              <div className="flex flex-col items-center">
                <div style={{height: `${Math.min(d.home * 15, 75)}px`, backgroundColor: homeTeamColor}} className="w-4 rounded-t-sm"></div>
                <span className="text-xs font-bold mt-1" style={{ color: homeTeamColor }}>{d.home.toFixed(1)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center p-3 bg-slate-900 rounded border border-slate-700">
          <span className="text-slate-400 text-sm">Power Success Rate</span>
          <div className="flex gap-4">
            <span className="font-bold" style={{ color: awayTeamColor }}>{(powerSuccess.away * 100).toFixed(1)}%</span>
            <span className="text-slate-600">vs</span>
            <span className="font-bold" style={{ color: homeTeamColor }}>{(powerSuccess.home * 100).toFixed(1)}%</span>
          </div>
        </div>
        <div className="flex justify-between items-center p-3 bg-slate-900 rounded border border-slate-700">
          <span className="text-slate-400 text-sm">Stuff Rate</span>
          <div className="flex gap-4">
            <span className="font-bold" style={{ color: awayTeamColor }}>{(stuffRate.away * 100).toFixed(1)}%</span>
            <span className="text-slate-600">vs</span>
            <span className="font-bold" style={{ color: homeTeamColor }}>{(stuffRate.home * 100).toFixed(1)}%</span>
          </div>
        </div>
      </div>
    </GlassCard>
  );
};

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
                <div className="flex-1 backdrop-blur-sm rounded-full h-2 overflow-hidden">
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
                <div className="flex-1 backdrop-blur-sm rounded-full h-2 overflow-hidden">
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
            <div className="relative h-12 backdrop-blur-sm rounded-full overflow-hidden border-2 border-slate-600/30 shadow-xl">
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
  const [debugMode, setDebugMode] = useState(false);
  const homeTeam = predictionData?.team_selector?.home_team;
  const awayTeam = predictionData?.team_selector?.away_team;

  // 🔍 DEBUG FUNCTION - Click button to see data structure
  const debugData = () => {
    console.log('🔍 === COMPREHENSIVE STATS DEBUG ===');
    console.log('Full predictionData:', predictionData);
    console.log('team_statistics path:', predictionData?.team_statistics);
    console.log('Home stats:', predictionData?.team_statistics?.home);
    console.log('Away stats:', predictionData?.team_statistics?.away);
    console.log('Sample home values:', {
      off_ppa: predictionData?.team_statistics?.home?.off_ppa,
      sacks: predictionData?.team_statistics?.home?.sacks,
      possession_time: predictionData?.team_statistics?.home?.possession_time
    });
    alert('Check browser console (F12) for full data dump!');
  };

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

  // Parse advanced offensive metrics from structured team statistics
  const parseAdvancedOffensive = () => {
    const awayStats = predictionData?.team_statistics?.away;
    const homeStats = predictionData?.team_statistics?.home;
    
    if (!awayStats || !homeStats) {
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

    // Helper to determine advantage
    const getAdvantage = (awayVal: number, homeVal: number, lowerIsBetter: boolean = false) => {
      if (lowerIsBetter) {
        return awayVal < homeVal ? awayTeam.name : homeVal < awayVal ? homeTeam.name : 'Even';
      }
      return awayVal > homeVal ? awayTeam.name : homeVal > awayVal ? homeTeam.name : 'Even';
    };

    return [
      // Overall Offense
      { metric: 'Offense PPA', away: awayStats.off_ppa || 0, home: homeStats.off_ppa || 0, advantage: getAdvantage(awayStats.off_ppa || 0, homeStats.off_ppa || 0) },
      { metric: 'PPA Rank', away: awayStats.off_ppa_rank || 0, home: homeStats.off_ppa_rank || 0, advantage: getAdvantage(awayStats.off_ppa_rank || 0, homeStats.off_ppa_rank || 0, true) },
      { metric: 'Success Rate', away: awayStats.off_success_rate || 0, home: homeStats.off_success_rate || 0, advantage: getAdvantage(awayStats.off_success_rate || 0, homeStats.off_success_rate || 0) },
      { metric: 'Explosiveness', away: awayStats.off_explosiveness || 0, home: homeStats.off_explosiveness || 0, advantage: getAdvantage(awayStats.off_explosiveness || 0, homeStats.off_explosiveness || 0) },
      { metric: 'Total Plays', away: awayStats.off_plays || 0, home: homeStats.off_plays || 0, advantage: getAdvantage(awayStats.off_plays || 0, homeStats.off_plays || 0) },
      { metric: 'Drives', away: awayStats.off_drives || 0, home: homeStats.off_drives || 0, advantage: getAdvantage(awayStats.off_drives || 0, homeStats.off_drives || 0) },
      
      // Rushing
      { metric: 'Rush PPA', away: awayStats.off_rush_ppa || 0, home: homeStats.off_rush_ppa || 0, advantage: getAdvantage(awayStats.off_rush_ppa || 0, homeStats.off_rush_ppa || 0) },
      { metric: 'Rush Success Rate', away: awayStats.off_rush_success_rate || 0, home: homeStats.off_rush_success_rate || 0, advantage: getAdvantage(awayStats.off_rush_success_rate || 0, homeStats.off_rush_success_rate || 0) },
      { metric: 'Rush Explosiveness', away: awayStats.off_rush_explosiveness || 0, home: homeStats.off_rush_explosiveness || 0, advantage: getAdvantage(awayStats.off_rush_explosiveness || 0, homeStats.off_rush_explosiveness || 0) },
      { metric: 'Rush Rate', away: awayStats.off_rush_rate || 0, home: homeStats.off_rush_rate || 0, advantage: getAdvantage(awayStats.off_rush_rate || 0, homeStats.off_rush_rate || 0) },
      { metric: 'Power Success', away: awayStats.off_power_success || 0, home: homeStats.off_power_success || 0, advantage: getAdvantage(awayStats.off_power_success || 0, homeStats.off_power_success || 0) },
      { metric: 'Stuff Rate', away: awayStats.off_stuff_rate || 0, home: homeStats.off_stuff_rate || 0, advantage: getAdvantage(awayStats.off_stuff_rate || 0, homeStats.off_stuff_rate || 0, true) },
      { metric: 'Line Yards', away: awayStats.off_line_yards || 0, home: homeStats.off_line_yards || 0, advantage: getAdvantage(awayStats.off_line_yards || 0, homeStats.off_line_yards || 0) },
      { metric: 'Line Yards Total', away: awayStats.off_line_yards_total || 0, home: homeStats.off_line_yards_total || 0, advantage: getAdvantage(awayStats.off_line_yards_total || 0, homeStats.off_line_yards_total || 0) },
      { metric: 'Second Level Yards', away: awayStats.off_second_level_yards || 0, home: homeStats.off_second_level_yards || 0, advantage: getAdvantage(awayStats.off_second_level_yards || 0, homeStats.off_second_level_yards || 0) },
      { metric: 'Second Level Yards Total', away: awayStats.off_second_level_yards_total || 0, home: homeStats.off_second_level_yards_total || 0, advantage: getAdvantage(awayStats.off_second_level_yards_total || 0, homeStats.off_second_level_yards_total || 0) },
      { metric: 'Open Field Yards', away: awayStats.off_open_field_yards || 0, home: homeStats.off_open_field_yards || 0, advantage: getAdvantage(awayStats.off_open_field_yards || 0, homeStats.off_open_field_yards || 0) },
      { metric: 'Open Field Yards Total', away: awayStats.off_open_field_yards_total || 0, home: homeStats.off_open_field_yards_total || 0, advantage: getAdvantage(awayStats.off_open_field_yards_total || 0, homeStats.off_open_field_yards_total || 0) },
      
      // Passing
      { metric: 'Pass PPA', away: awayStats.off_pass_ppa || 0, home: homeStats.off_pass_ppa || 0, advantage: getAdvantage(awayStats.off_pass_ppa || 0, homeStats.off_pass_ppa || 0) },
      { metric: 'Pass Success Rate', away: awayStats.off_pass_success_rate || 0, home: homeStats.off_pass_success_rate || 0, advantage: getAdvantage(awayStats.off_pass_success_rate || 0, homeStats.off_pass_success_rate || 0) },
      { metric: 'Pass Explosiveness', away: awayStats.off_pass_explosiveness || 0, home: homeStats.off_pass_explosiveness || 0, advantage: getAdvantage(awayStats.off_pass_explosiveness || 0, homeStats.off_pass_explosiveness || 0) },
      { metric: 'Pass Rate', away: awayStats.off_pass_rate || 0, home: homeStats.off_pass_rate || 0, advantage: getAdvantage(awayStats.off_pass_rate || 0, homeStats.off_pass_rate || 0) },
      
      // Standard Down
      { metric: 'Std Down PPA', away: awayStats.off_std_ppa || 0, home: homeStats.off_std_ppa || 0, advantage: getAdvantage(awayStats.off_std_ppa || 0, homeStats.off_std_ppa || 0) },
      { metric: 'Std Down Success Rate', away: awayStats.off_std_success_rate || 0, home: homeStats.off_std_success_rate || 0, advantage: getAdvantage(awayStats.off_std_success_rate || 0, homeStats.off_std_success_rate || 0) },
      { metric: 'Std Down Explosiveness', away: awayStats.off_std_explosiveness || 0, home: homeStats.off_std_explosiveness || 0, advantage: getAdvantage(awayStats.off_std_explosiveness || 0, homeStats.off_std_explosiveness || 0) },
      { metric: 'Std Down Rate', away: awayStats.off_std_rate || 0, home: homeStats.off_std_rate || 0, advantage: getAdvantage(awayStats.off_std_rate || 0, homeStats.off_std_rate || 0) },
      
      // Passing Down
      { metric: 'Pass Down PPA', away: awayStats.off_pass_down_ppa || 0, home: homeStats.off_pass_down_ppa || 0, advantage: getAdvantage(awayStats.off_pass_down_ppa || 0, homeStats.off_pass_down_ppa || 0) },
      { metric: 'Pass Down Success Rate', away: awayStats.off_pass_down_success_rate || 0, home: homeStats.off_pass_down_success_rate || 0, advantage: getAdvantage(awayStats.off_pass_down_success_rate || 0, homeStats.off_pass_down_success_rate || 0) },
      { metric: 'Pass Down Explosiveness', away: awayStats.off_pass_down_explosiveness || 0, home: homeStats.off_pass_down_explosiveness || 0, advantage: getAdvantage(awayStats.off_pass_down_explosiveness || 0, homeStats.off_pass_down_explosiveness || 0) },
      { metric: 'Pass Down Rate', away: awayStats.off_pass_down_rate || 0, home: homeStats.off_pass_down_rate || 0, advantage: getAdvantage(awayStats.off_pass_down_rate || 0, homeStats.off_pass_down_rate || 0) },
      
      // Field Position & Opportunities
      { metric: 'Avg Start Field Pos', away: awayStats.off_field_pos_avg_start || 0, home: homeStats.off_field_pos_avg_start || 0, advantage: getAdvantage(awayStats.off_field_pos_avg_start || 0, homeStats.off_field_pos_avg_start || 0) },
      { metric: 'Avg Predicted Points', away: awayStats.off_field_pos_avg_predicted_points || 0, home: homeStats.off_field_pos_avg_predicted_points || 0, advantage: getAdvantage(awayStats.off_field_pos_avg_predicted_points || 0, homeStats.off_field_pos_avg_predicted_points || 0) },
      { metric: 'Points Per Opportunity', away: awayStats.off_points_per_opportunity || 0, home: homeStats.off_points_per_opportunity || 0, advantage: getAdvantage(awayStats.off_points_per_opportunity || 0, homeStats.off_points_per_opportunity || 0) },
      { metric: 'Total Opportunities', away: awayStats.off_total_opportunities || 0, home: homeStats.off_total_opportunities || 0, advantage: getAdvantage(awayStats.off_total_opportunities || 0, homeStats.off_total_opportunities || 0) },
      
      // Havoc
      { metric: 'Havoc Total', away: awayStats.off_havoc_total || 0, home: homeStats.off_havoc_total || 0, advantage: getAdvantage(awayStats.off_havoc_total || 0, homeStats.off_havoc_total || 0) },
      { metric: 'Havoc Front Seven', away: awayStats.off_havoc_front_seven || 0, home: homeStats.off_havoc_front_seven || 0, advantage: getAdvantage(awayStats.off_havoc_front_seven || 0, homeStats.off_havoc_front_seven || 0) },
      { metric: 'Havoc DB', away: awayStats.off_havoc_db || 0, home: homeStats.off_havoc_db || 0, advantage: getAdvantage(awayStats.off_havoc_db || 0, homeStats.off_havoc_db || 0) },
    ];
  };

  // Data for Advanced Offensive Metrics - Horizontal Bar Chart
  const advancedOffensiveData = parseAdvancedOffensive();

  // Parse defensive metrics from structured team statistics
  const parseDefensiveData = () => {
    const awayStats = predictionData?.team_statistics?.away;
    const homeStats = predictionData?.team_statistics?.home;
    
    if (!awayStats || !homeStats) {
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

    // Helper to determine advantage (lower is better for defense)
    const getAdvantage = (awayVal: number, homeVal: number, lowerIsBetter: boolean = true) => {
      if (lowerIsBetter) {
        return awayVal < homeVal ? awayTeam.name : homeVal < awayVal ? homeTeam.name : 'Even';
      }
      return awayVal > homeVal ? awayTeam.name : homeVal > awayVal ? homeTeam.name : 'Even';
    };

    return [
      // Traditional Stats
      { metric: 'Sacks', away: awayStats.sacks || 0, home: homeStats.sacks || 0, advantage: getAdvantage(awayStats.sacks || 0, homeStats.sacks || 0, false) },
      { metric: 'Interceptions', away: awayStats.interceptions || 0, home: homeStats.interceptions || 0, advantage: getAdvantage(awayStats.interceptions || 0, homeStats.interceptions || 0, false) },
      { metric: 'Tackles for Loss', away: awayStats.tackles_for_loss || 0, home: homeStats.tackles_for_loss || 0, advantage: getAdvantage(awayStats.tackles_for_loss || 0, homeStats.tackles_for_loss || 0, false) },
      { metric: 'Fumbles Recovered', away: awayStats.fumbles_recovered || 0, home: homeStats.fumbles_recovered || 0, advantage: getAdvantage(awayStats.fumbles_recovered || 0, homeStats.fumbles_recovered || 0, false) },
      
      // Overall Defense
      { metric: 'Defense PPA', away: awayStats.def_ppa || 0, home: homeStats.def_ppa || 0, advantage: getAdvantage(awayStats.def_ppa || 0, homeStats.def_ppa || 0) },
      { metric: 'PPA Rank', away: awayStats.def_ppa_rank || 0, home: homeStats.def_ppa_rank || 0, advantage: getAdvantage(awayStats.def_ppa_rank || 0, homeStats.def_ppa_rank || 0) },
      { metric: 'Defense Success Rate', away: awayStats.def_success_rate || 0, home: homeStats.def_success_rate || 0, advantage: getAdvantage(awayStats.def_success_rate || 0, homeStats.def_success_rate || 0) },
      { metric: 'Defense Explosiveness', away: awayStats.def_explosiveness || 0, home: homeStats.def_explosiveness || 0, advantage: getAdvantage(awayStats.def_explosiveness || 0, homeStats.def_explosiveness || 0) },
      { metric: 'Defense Plays', away: awayStats.def_plays || 0, home: homeStats.def_plays || 0, advantage: getAdvantage(awayStats.def_plays || 0, homeStats.def_plays || 0) },
      { metric: 'Defense Drives', away: awayStats.def_drives || 0, home: homeStats.def_drives || 0, advantage: getAdvantage(awayStats.def_drives || 0, homeStats.def_drives || 0) },
      
      // Rush Defense
      { metric: 'Def Rush PPA', away: awayStats.def_rush_ppa || 0, home: homeStats.def_rush_ppa || 0, advantage: getAdvantage(awayStats.def_rush_ppa || 0, homeStats.def_rush_ppa || 0) },
      { metric: 'Def Rush Success Rate', away: awayStats.def_rush_success_rate || 0, home: homeStats.def_rush_success_rate || 0, advantage: getAdvantage(awayStats.def_rush_success_rate || 0, homeStats.def_rush_success_rate || 0) },
      { metric: 'Def Rush Explosiveness', away: awayStats.def_rush_explosiveness || 0, home: homeStats.def_rush_explosiveness || 0, advantage: getAdvantage(awayStats.def_rush_explosiveness || 0, homeStats.def_rush_explosiveness || 0) },
      { metric: 'Def Rush Rate', away: awayStats.def_rush_rate || 0, home: homeStats.def_rush_rate || 0, advantage: getAdvantage(awayStats.def_rush_rate || 0, homeStats.def_rush_rate || 0) },
      { metric: 'Def Power Success', away: awayStats.def_power_success || 0, home: homeStats.def_power_success || 0, advantage: getAdvantage(awayStats.def_power_success || 0, homeStats.def_power_success || 0) },
      { metric: 'Def Stuff Rate', away: awayStats.def_stuff_rate || 0, home: homeStats.def_stuff_rate || 0, advantage: getAdvantage(awayStats.def_stuff_rate || 0, homeStats.def_stuff_rate || 0, false) },
      { metric: 'Def Line Yards', away: awayStats.def_line_yards || 0, home: homeStats.def_line_yards || 0, advantage: getAdvantage(awayStats.def_line_yards || 0, homeStats.def_line_yards || 0) },
      { metric: 'Def Line Yards Total', away: awayStats.def_line_yards_total || 0, home: homeStats.def_line_yards_total || 0, advantage: getAdvantage(awayStats.def_line_yards_total || 0, homeStats.def_line_yards_total || 0) },
      { metric: 'Def Second Level Yards', away: awayStats.def_second_level_yards || 0, home: homeStats.def_second_level_yards || 0, advantage: getAdvantage(awayStats.def_second_level_yards || 0, homeStats.def_second_level_yards || 0) },
      { metric: 'Def Second Level Yards Total', away: awayStats.def_second_level_yards_total || 0, home: homeStats.def_second_level_yards_total || 0, advantage: getAdvantage(awayStats.def_second_level_yards_total || 0, homeStats.def_second_level_yards_total || 0) },
      { metric: 'Def Open Field Yards', away: awayStats.def_open_field_yards || 0, home: homeStats.def_open_field_yards || 0, advantage: getAdvantage(awayStats.def_open_field_yards || 0, homeStats.def_open_field_yards || 0) },
      { metric: 'Def Open Field Yards Total', away: awayStats.def_open_field_yards_total || 0, home: homeStats.def_open_field_yards_total || 0, advantage: getAdvantage(awayStats.def_open_field_yards_total || 0, homeStats.def_open_field_yards_total || 0) },
      
      // Pass Defense
      { metric: 'Def Pass PPA', away: awayStats.def_pass_ppa || 0, home: homeStats.def_pass_ppa || 0, advantage: getAdvantage(awayStats.def_pass_ppa || 0, homeStats.def_pass_ppa || 0) },
      { metric: 'Def Pass Success Rate', away: awayStats.def_pass_success_rate || 0, home: homeStats.def_pass_success_rate || 0, advantage: getAdvantage(awayStats.def_pass_success_rate || 0, homeStats.def_pass_success_rate || 0) },
      { metric: 'Def Pass Explosiveness', away: awayStats.def_pass_explosiveness || 0, home: homeStats.def_pass_explosiveness || 0, advantage: getAdvantage(awayStats.def_pass_explosiveness || 0, homeStats.def_pass_explosiveness || 0) },
      { metric: 'Def Pass Rate', away: awayStats.def_pass_rate || 0, home: homeStats.def_pass_rate || 0, advantage: getAdvantage(awayStats.def_pass_rate || 0, homeStats.def_pass_rate || 0) },
      
      // Standard Down Defense
      { metric: 'Def Std Down PPA', away: awayStats.def_std_ppa || 0, home: homeStats.def_std_ppa || 0, advantage: getAdvantage(awayStats.def_std_ppa || 0, homeStats.def_std_ppa || 0) },
      { metric: 'Def Std Down Success Rate', away: awayStats.def_std_success_rate || 0, home: homeStats.def_std_success_rate || 0, advantage: getAdvantage(awayStats.def_std_success_rate || 0, homeStats.def_std_success_rate || 0) },
      { metric: 'Def Std Down Explosiveness', away: awayStats.def_std_explosiveness || 0, home: homeStats.def_std_explosiveness || 0, advantage: getAdvantage(awayStats.def_std_explosiveness || 0, homeStats.def_std_explosiveness || 0) },
      { metric: 'Def Std Down Rate', away: awayStats.def_std_rate || 0, home: homeStats.def_std_rate || 0, advantage: getAdvantage(awayStats.def_std_rate || 0, homeStats.def_std_rate || 0) },
      
      // Passing Down Defense
      { metric: 'Def Pass Down PPA', away: awayStats.def_pass_down_ppa || 0, home: homeStats.def_pass_down_ppa || 0, advantage: getAdvantage(awayStats.def_pass_down_ppa || 0, homeStats.def_pass_down_ppa || 0) },
      { metric: 'Def Pass Down Success Rate', away: awayStats.def_pass_down_success_rate || 0, home: homeStats.def_pass_down_success_rate || 0, advantage: getAdvantage(awayStats.def_pass_down_success_rate || 0, homeStats.def_pass_down_success_rate || 0) },
      { metric: 'Def Pass Down Explosiveness', away: awayStats.def_pass_down_explosiveness || 0, home: homeStats.def_pass_down_explosiveness || 0, advantage: getAdvantage(awayStats.def_pass_down_explosiveness || 0, homeStats.def_pass_down_explosiveness || 0) },
      { metric: 'Def Pass Down Rate', away: awayStats.def_pass_down_rate || 0, home: homeStats.def_pass_down_rate || 0, advantage: getAdvantage(awayStats.def_pass_down_rate || 0, homeStats.def_pass_down_rate || 0) },
      
      // Field Position & Opportunities Defense
      { metric: 'Def Avg Start Field Pos', away: awayStats.def_field_pos_avg_start || 0, home: homeStats.def_field_pos_avg_start || 0, advantage: getAdvantage(awayStats.def_field_pos_avg_start || 0, homeStats.def_field_pos_avg_start || 0, false) },
      { metric: 'Def Avg Predicted Points', away: awayStats.def_field_pos_avg_predicted_points || 0, home: homeStats.def_field_pos_avg_predicted_points || 0, advantage: getAdvantage(awayStats.def_field_pos_avg_predicted_points || 0, homeStats.def_field_pos_avg_predicted_points || 0) },
      { metric: 'Def Points Per Opportunity', away: awayStats.def_points_per_opportunity || 0, home: homeStats.def_points_per_opportunity || 0, advantage: getAdvantage(awayStats.def_points_per_opportunity || 0, homeStats.def_points_per_opportunity || 0) },
      { metric: 'Def Total Opportunities', away: awayStats.def_total_opportunities || 0, home: homeStats.def_total_opportunities || 0, advantage: getAdvantage(awayStats.def_total_opportunities || 0, homeStats.def_total_opportunities || 0) },
      
      // Havoc
      { metric: 'Defense Havoc Total', away: awayStats.def_havoc_total || 0, home: homeStats.def_havoc_total || 0, advantage: getAdvantage(awayStats.def_havoc_total || 0, homeStats.def_havoc_total || 0, false) },
      { metric: 'Def Havoc Front Seven', away: awayStats.def_havoc_front_seven || 0, home: homeStats.def_havoc_front_seven || 0, advantage: getAdvantage(awayStats.def_havoc_front_seven || 0, homeStats.def_havoc_front_seven || 0, false) },
      { metric: 'Def Havoc DB', away: awayStats.def_havoc_db || 0, home: homeStats.def_havoc_db || 0, advantage: getAdvantage(awayStats.def_havoc_db || 0, homeStats.def_havoc_db || 0, false) },
    ];
  };

  // Data for Defensive Statistics - Circular Progress
  const defensiveData = parseDefensiveData();

  // Parse game control metrics from structured team statistics
  const parseGameControl = () => {
    const awayStats = predictionData?.team_statistics?.away;
    const homeStats = predictionData?.team_statistics?.home;
    
    if (!awayStats || !homeStats) {
      return [
        { metric: 'Possession Time', away: '0:00', home: '0:00', advantage: 'Even' },
        { metric: 'Turnover Margin', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Penalty Yards', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Games Played', away: '0', home: '0', advantage: 'Even' },
        { metric: 'Drives Per Game', away: '0', home: '0', advantage: 'Even' },
      ];
    }

    // Format possession time from seconds to MM:SS
    const formatPossessionTime = (seconds: number) => {
      if (!seconds) return '0:00';
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    // Calculate drives per game - data is already in team stats!
    const awayOffDrives = awayStats.off_drives || 0;
    const homeOffDrives = homeStats.off_drives || 0;
    const awayGamesPlayed = awayStats.games_played || 1;
    const homeGamesPlayed = homeStats.games_played || 1;
    
    const awayDrivesPerGame = (awayOffDrives / awayGamesPlayed).toFixed(1);
    const homeDrivesPerGame = (homeOffDrives / homeGamesPlayed).toFixed(1);

    // Safe getters with default values
    const awayPossTime = awayStats.possession_time || 0;
    const homePossTime = homeStats.possession_time || 0;
    const awayTOMargin = awayStats.turnover_margin || 0;
    const homeTOMargin = homeStats.turnover_margin || 0;
    const awayPenaltyYards = awayStats.penalty_yards || 0;
    const homePenaltyYards = homeStats.penalty_yards || 0;

    // Determine advantages
    const possAdvantage = awayPossTime > homePossTime ? awayTeam.name : 
                         homePossTime > awayPossTime ? homeTeam.name : 'Even';
    const toAdvantage = awayTOMargin > homeTOMargin ? awayTeam.name :
                       homeTOMargin > awayTOMargin ? homeTeam.name : 'Even';
    const penaltyAdvantage = awayPenaltyYards < homePenaltyYards ? awayTeam.name :
                            homePenaltyYards < awayPenaltyYards ? homeTeam.name : 'Even';
    const drivesAdvantage = parseFloat(awayDrivesPerGame) > parseFloat(homeDrivesPerGame) ? awayTeam.name :
                           parseFloat(homeDrivesPerGame) > parseFloat(awayDrivesPerGame) ? homeTeam.name : 'Even';

    return [
      { 
        metric: 'Possession Time', 
        away: formatPossessionTime(awayPossTime), 
        home: formatPossessionTime(homePossTime), 
        advantage: possAdvantage 
      },
      { 
        metric: 'Turnover Margin', 
        away: awayTOMargin > 0 ? `+${awayTOMargin}` : awayTOMargin.toString(), 
        home: homeTOMargin > 0 ? `+${homeTOMargin}` : homeTOMargin.toString(), 
        advantage: toAdvantage 
      },
      { 
        metric: 'Penalty Yards', 
        away: awayPenaltyYards.toString(), 
        home: homePenaltyYards.toString(), 
        advantage: penaltyAdvantage 
      },
      { 
        metric: 'Games Played', 
        away: awayGamesPlayed.toString(), 
        home: homeGamesPlayed.toString(), 
        advantage: 'Even' 
      },
      { 
        metric: 'Drives Per Game', 
        away: awayDrivesPerGame, 
        home: homeDrivesPerGame, 
        advantage: drivesAdvantage 
      },
    ];
  };

  // Data for Game Control Metrics - Radar Style
  const gameControlData = parseGameControl();

  // Parse team info & ratings
  const parseTeamInfo = () => {
    const awayStats = predictionData?.team_statistics?.away;
    const homeStats = predictionData?.team_statistics?.home;
    
    if (!awayStats || !homeStats) return [];

    const getAdvantage = (awayVal: number, homeVal: number, lowerIsBetter: boolean = false) => {
      if (lowerIsBetter) {
        return awayVal < homeVal ? awayTeam.name : homeVal < awayVal ? homeTeam.name : 'Even';
      }
      return awayVal > homeVal ? awayTeam.name : homeVal > awayVal ? homeTeam.name : 'Even';
    };

    return [
      // Record
      { metric: 'Wins', away: awayStats.wins || 0, home: homeStats.wins || 0, advantage: getAdvantage(awayStats.wins || 0, homeStats.wins || 0) },
      { metric: 'Losses', away: awayStats.losses || 0, home: homeStats.losses || 0, advantage: getAdvantage(awayStats.losses || 0, homeStats.losses || 0, true) },
      { metric: 'Home Wins', away: awayStats.home_wins || 0, home: homeStats.home_wins || 0, advantage: getAdvantage(awayStats.home_wins || 0, homeStats.home_wins || 0) },
      { metric: 'Home Losses', away: awayStats.home_losses || 0, home: homeStats.home_losses || 0, advantage: getAdvantage(awayStats.home_losses || 0, homeStats.home_losses || 0, true) },
      { metric: 'Away Wins', away: awayStats.away_wins || 0, home: homeStats.away_wins || 0, advantage: getAdvantage(awayStats.away_wins || 0, homeStats.away_wins || 0) },
      { metric: 'Away Losses', away: awayStats.away_losses || 0, home: homeStats.away_losses || 0, advantage: getAdvantage(awayStats.away_losses || 0, homeStats.away_losses || 0, true) },
      { metric: 'Conference Wins', away: awayStats.conference_wins || 0, home: homeStats.conference_wins || 0, advantage: getAdvantage(awayStats.conference_wins || 0, homeStats.conference_wins || 0) },
      { metric: 'Conference Losses', away: awayStats.conference_losses || 0, home: homeStats.conference_losses || 0, advantage: getAdvantage(awayStats.conference_losses || 0, homeStats.conference_losses || 0, true) },
      
      // FPI
      { metric: 'FPI Rating', away: awayStats.fpi || 0, home: homeStats.fpi || 0, advantage: getAdvantage(awayStats.fpi || 0, homeStats.fpi || 0) },
      { metric: 'FPI Ranking', away: awayStats.fpi_ranking || 0, home: homeStats.fpi_ranking || 0, advantage: getAdvantage(awayStats.fpi_ranking || 0, homeStats.fpi_ranking || 0, true) },
      { metric: 'FPI Offense Efficiency', away: awayStats.fpi_offense_efficiency || 0, home: homeStats.fpi_offense_efficiency || 0, advantage: getAdvantage(awayStats.fpi_offense_efficiency || 0, homeStats.fpi_offense_efficiency || 0) },
      { metric: 'FPI Offense Rank', away: awayStats.fpi_offense_efficiency_rank || 0, home: homeStats.fpi_offense_efficiency_rank || 0, advantage: getAdvantage(awayStats.fpi_offense_efficiency_rank || 0, homeStats.fpi_offense_efficiency_rank || 0, true) },
      { metric: 'FPI Defense Efficiency', away: awayStats.fpi_defense_efficiency || 0, home: homeStats.fpi_defense_efficiency || 0, advantage: getAdvantage(awayStats.fpi_defense_efficiency || 0, homeStats.fpi_defense_efficiency || 0) },
      { metric: 'FPI Defense Rank', away: awayStats.fpi_defense_efficiency_rank || 0, home: homeStats.fpi_defense_efficiency_rank || 0, advantage: getAdvantage(awayStats.fpi_defense_efficiency_rank || 0, homeStats.fpi_defense_efficiency_rank || 0, true) },
      { metric: 'FPI Special Teams', away: awayStats.fpi_special_teams_efficiency || 0, home: homeStats.fpi_special_teams_efficiency || 0, advantage: getAdvantage(awayStats.fpi_special_teams_efficiency || 0, homeStats.fpi_special_teams_efficiency || 0) },
      { metric: 'FPI Overall Efficiency', away: awayStats.fpi_overall_efficiency || 0, home: homeStats.fpi_overall_efficiency || 0, advantage: getAdvantage(awayStats.fpi_overall_efficiency || 0, homeStats.fpi_overall_efficiency || 0) },
      { metric: 'FPI Game Control', away: awayStats.fpi_game_control || 0, home: homeStats.fpi_game_control || 0, advantage: getAdvantage(awayStats.fpi_game_control || 0, homeStats.fpi_game_control || 0) },
      { metric: 'FPI Avg Win Probability', away: awayStats.fpi_avg_win_probability || 0, home: homeStats.fpi_avg_win_probability || 0, advantage: getAdvantage(awayStats.fpi_avg_win_probability || 0, homeStats.fpi_avg_win_probability || 0) },
      { metric: 'FPI Strength of Record', away: awayStats.fpi_strength_of_record || 0, home: homeStats.fpi_strength_of_record || 0, advantage: getAdvantage(awayStats.fpi_strength_of_record || 0, homeStats.fpi_strength_of_record || 0) },
      { metric: 'FPI Strength of Schedule', away: awayStats.fpi_strength_of_schedule || 0, home: homeStats.fpi_strength_of_schedule || 0, advantage: getAdvantage(awayStats.fpi_strength_of_schedule || 0, homeStats.fpi_strength_of_schedule || 0, true) },
      
      // SP+ Ratings
      { metric: 'SP+ Rating', away: awayStats.sp_rating || 0, home: homeStats.sp_rating || 0, advantage: getAdvantage(awayStats.sp_rating || 0, homeStats.sp_rating || 0) },
      { metric: 'SP+ Ranking', away: awayStats.sp_ranking || 0, home: homeStats.sp_ranking || 0, advantage: getAdvantage(awayStats.sp_ranking || 0, homeStats.sp_ranking || 0, true) },
      { metric: 'SP+ Offense', away: awayStats.sp_offense || 0, home: homeStats.sp_offense || 0, advantage: getAdvantage(awayStats.sp_offense || 0, homeStats.sp_offense || 0) },
      { metric: 'SP+ Offense Rank', away: awayStats.sp_offense_rank || 0, home: homeStats.sp_offense_rank || 0, advantage: getAdvantage(awayStats.sp_offense_rank || 0, homeStats.sp_offense_rank || 0, true) },
      { metric: 'SP+ Defense', away: awayStats.sp_defense || 0, home: homeStats.sp_defense || 0, advantage: getAdvantage(awayStats.sp_defense || 0, homeStats.sp_defense || 0) },
      { metric: 'SP+ Defense Rank', away: awayStats.sp_defense_rank || 0, home: homeStats.sp_defense_rank || 0, advantage: getAdvantage(awayStats.sp_defense_rank || 0, homeStats.sp_defense_rank || 0, true) },
      { metric: 'SP+ Special Teams', away: awayStats.sp_special_teams || 0, home: homeStats.sp_special_teams || 0, advantage: getAdvantage(awayStats.sp_special_teams || 0, homeStats.sp_special_teams || 0) },
      
      // Recruiting & Talent
      { metric: 'Recruiting Rank', away: awayStats.recruiting_rank || 0, home: homeStats.recruiting_rank || 0, advantage: getAdvantage(awayStats.recruiting_rank || 0, homeStats.recruiting_rank || 0, true) },
      { metric: 'Recruiting Points', away: awayStats.recruiting_points || 0, home: homeStats.recruiting_points || 0, advantage: getAdvantage(awayStats.recruiting_points || 0, homeStats.recruiting_points || 0) },
      { metric: 'Recruiting Points Rank', away: awayStats.recruiting_points_rank || 0, home: homeStats.recruiting_points_rank || 0, advantage: getAdvantage(awayStats.recruiting_points_rank || 0, homeStats.recruiting_points_rank || 0, true) },
      { metric: 'Talent Composite', away: awayStats.talent_composite || 0, home: homeStats.talent_composite || 0, advantage: getAdvantage(awayStats.talent_composite || 0, homeStats.talent_composite || 0) },
      { metric: 'Talent Composite Rank', away: awayStats.talent_composite_rank || 0, home: homeStats.talent_composite_rank || 0, advantage: getAdvantage(awayStats.talent_composite_rank || 0, homeStats.talent_composite_rank || 0, true) },
      
      // Turnovers
      { metric: 'Turnovers', away: awayStats.turnovers || 0, home: homeStats.turnovers || 0, advantage: getAdvantage(awayStats.turnovers || 0, homeStats.turnovers || 0, true) },
      { metric: 'Turnovers Opponent', away: awayStats.turnovers_opponent || 0, home: homeStats.turnovers_opponent || 0, advantage: getAdvantage(awayStats.turnovers_opponent || 0, homeStats.turnovers_opponent || 0) },
      { metric: 'Fumbles Lost', away: awayStats.fumbles_lost || 0, home: homeStats.fumbles_lost || 0, advantage: getAdvantage(awayStats.fumbles_lost || 0, homeStats.fumbles_lost || 0, true) },
    ];
  };

  const teamInfoData = parseTeamInfo();

  // Prepare data for modern charts
  const awayStats = predictionData?.team_statistics?.away;
  const homeStats = predictionData?.team_statistics?.home;

  // Calculate win probability based on key metrics (simple weighted average)
  const calculateWinProb = () => {
    if (!awayStats || !homeStats) return { away: 50, home: 50 };
    
    // Weight factors: PPA (50%), Success Rate (20%), Explosiveness (15%), Power (15%)
    const awayScore = (awayStats.off_ppa || 0) * 50 + (awayStats.off_success_rate || 0) * 20 + 
                      (awayStats.off_explosiveness || 0) * 15 + (awayStats.off_power_success || 0) * 15;
    const homeScore = (homeStats.off_ppa || 0) * 50 + (homeStats.off_success_rate || 0) * 20 + 
                      (homeStats.off_explosiveness || 0) * 15 + (homeStats.off_power_success || 0) * 15;
    
    const total = awayScore + homeScore;
    if (total === 0) return { away: 50, home: 50 };
    
    return {
      away: Math.round((awayScore / total) * 100),
      home: Math.round((homeScore / total) * 100)
    };
  };

  // Radar data - normalized to 0-100 scale
  const normalizeToRadar = (val: number, max: number = 1) => Math.min(Math.round((val / max) * 100), 100);
  
  const radarChartData = [
    { 
      subject: 'Success Rate', 
      away: normalizeToRadar(awayStats?.off_success_rate || 0, 1), 
      home: normalizeToRadar(homeStats?.off_success_rate || 0, 1),
      realAway: `${((awayStats?.off_success_rate || 0) * 100).toFixed(1)}%`,
      realHome: `${((homeStats?.off_success_rate || 0) * 100).toFixed(1)}%`
    },
    { 
      subject: 'Explosiveness', 
      away: normalizeToRadar(awayStats?.off_explosiveness || 0, 3), 
      home: normalizeToRadar(homeStats?.off_explosiveness || 0, 3),
      realAway: (awayStats?.off_explosiveness || 0).toFixed(2),
      realHome: (homeStats?.off_explosiveness || 0).toFixed(2)
    },
    { 
      subject: 'PPA (Eff)', 
      away: normalizeToRadar((awayStats?.off_ppa || 0) + 0.5, 1), 
      home: normalizeToRadar((homeStats?.off_ppa || 0) + 0.5, 1),
      realAway: (awayStats?.off_ppa || 0).toFixed(2),
      realHome: (homeStats?.off_ppa || 0).toFixed(2)
    },
    { 
      subject: 'Power', 
      away: normalizeToRadar(awayStats?.off_power_success || 0, 1), 
      home: normalizeToRadar(homeStats?.off_power_success || 0, 1),
      realAway: `${((awayStats?.off_power_success || 0) * 100).toFixed(1)}%`,
      realHome: `${((homeStats?.off_power_success || 0) * 100).toFixed(1)}%`
    },
    { 
      subject: 'Finishing', 
      away: normalizeToRadar(awayStats?.off_points_per_opportunity || 0, 6), 
      home: normalizeToRadar(homeStats?.off_points_per_opportunity || 0, 6),
      realAway: `${(awayStats?.off_points_per_opportunity || 0).toFixed(1)} Pts/Opp`,
      realHome: `${(homeStats?.off_points_per_opportunity || 0).toFixed(1)} Pts/Opp`
    },
    { 
      subject: 'Stuff Rate', 
      away: 100 - normalizeToRadar(awayStats?.off_stuff_rate || 0, 1), 
      home: 100 - normalizeToRadar(homeStats?.off_stuff_rate || 0, 1),
      realAway: `${((awayStats?.off_stuff_rate || 0) * 100).toFixed(1)}%`,
      realHome: `${((homeStats?.off_stuff_rate || 0) * 100).toFixed(1)}%`
    },
  ];

  // PPA Field Tilt data
  const ppaChartData = [
    { category: 'Overall Offense', away: Math.abs(awayStats?.off_ppa || 0), home: Math.abs(homeStats?.off_ppa || 0) },
    { category: 'Passing', away: Math.abs(awayStats?.off_pass_ppa || 0), home: Math.abs(homeStats?.off_pass_ppa || 0) },
    { category: 'Rushing', away: Math.abs(awayStats?.off_rush_ppa || 0), home: Math.abs(homeStats?.off_rush_ppa || 0) },
    { category: 'Standard Down', away: Math.abs(awayStats?.off_std_ppa || 0), home: Math.abs(homeStats?.off_std_ppa || 0) },
    { category: 'Passing Down', away: Math.abs(awayStats?.off_pass_down_ppa || 0), home: Math.abs(homeStats?.off_pass_down_ppa || 0) },
  ];

  // Havoc/Chaos data
  const havocChartData = [
    { name: 'Sacks', away: awayStats?.sacks || 0, home: homeStats?.sacks || 0 },
    { name: 'TFLs', away: awayStats?.tackles_for_loss || 0, home: homeStats?.tackles_for_loss || 0 },
    { name: 'INTs', away: awayStats?.interceptions || 0, home: homeStats?.interceptions || 0 },
    { name: 'Fumbles', away: awayStats?.fumbles_recovered || 0, home: homeStats?.fumbles_recovered || 0 },
  ];

  // Trenches data
  const trenchesChartData = [
    { name: 'Line Yards', away: awayStats?.off_line_yards || 0, home: homeStats?.off_line_yards || 0 },
    { name: 'Second Lvl Yds', away: awayStats?.off_second_level_yards || 0, home: homeStats?.off_second_level_yards || 0 },
    { name: 'Open Field Yds', away: awayStats?.off_open_field_yards || 0, home: homeStats?.off_open_field_yards || 0 },
  ];

  const winProb = calculateWinProb();

  return (
    <div className="space-y-8">
      {/* MODERN CHARTS SECTION */}
      <section className="space-y-6">
        {/* Win Probability Hero */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <WinProbabilityHero awayTeam={awayTeam} homeTeam={homeTeam} winProb={winProb} />
          </div>
          <GlassCard glowColor="from-yellow-500/20 to-amber-500/20" className="p-6 flex flex-col justify-center items-center text-center">
            <Trophy size={48} className="text-yellow-400 mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">Matchup Insight</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              {winProb.away > winProb.home ? (
                <>
                  <span className="text-cyan-400 font-bold">{awayTeam.name}</span> has the efficiency edge with {winProb.away}% win probability based on PPA, success rate, and explosiveness metrics.
                </>
              ) : (
                <>
                  <span className="text-orange-400 font-bold">{homeTeam.name}</span> dominates with {winProb.home}% win probability, showcasing superior offensive efficiency and execution.
                </>
              )}
            </p>
          </GlassCard>
        </div>

        {/* Row 2: Team DNA & Field Tilt */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TeamIdentityRadar awayTeam={awayTeam} homeTeam={homeTeam} radarData={radarChartData} />
          <FieldTiltChart awayTeam={awayTeam} homeTeam={homeTeam} ppaData={ppaChartData} />
        </div>

        {/* Row 3: Havoc & Trenches */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <HavocMeterChart awayTeam={awayTeam} homeTeam={homeTeam} havocData={havocChartData} />
          <TrenchesChart 
            awayTeam={awayTeam} 
            homeTeam={homeTeam} 
            trenchesData={trenchesChartData}
            powerSuccess={{ away: awayStats?.off_power_success || 0, home: homeStats?.off_power_success || 0 }}
            stuffRate={{ away: awayStats?.off_stuff_rate || 0, home: homeStats?.off_stuff_rate || 0 }}
          />
        </div>
      </section>
      
      {/* 🔍 PATH EXPLORER - Show data structure */}
      {debugMode && (
        <div className="p-6 bg-red-500/10 border-2 border-red-500 rounded-lg">
          <h3 className="text-red-500 font-bold text-xl mb-4">🔍 DATA PATH EXPLORER</h3>
          <div className="space-y-2 text-sm font-mono">
            <div className="p-2 bg-black/30 rounded">
              <span className="text-gray-400">predictionData exists:</span>{' '}
              <span className={predictionData ? 'text-green-400' : 'text-red-400'}>
                {predictionData ? '✅ YES' : '❌ NO'}
              </span>
            </div>
            <div className="p-2 bg-black/30 rounded">
              <span className="text-gray-400">predictionData.team_statistics:</span>{' '}
              <span className={predictionData?.team_statistics ? 'text-green-400' : 'text-red-400'}>
                {predictionData?.team_statistics ? '✅ EXISTS' : '❌ MISSING'}
              </span>
            </div>
            <div className="p-2 bg-black/30 rounded">
              <span className="text-gray-400">predictionData.team_statistics.home:</span>{' '}
              <span className={predictionData?.team_statistics?.home ? 'text-green-400' : 'text-red-400'}>
                {predictionData?.team_statistics?.home ? '✅ EXISTS' : '❌ MISSING'}
              </span>
            </div>
            <div className="p-2 bg-black/30 rounded">
              <span className="text-gray-400">predictionData.team_statistics.away:</span>{' '}
              <span className={predictionData?.team_statistics?.away ? 'text-green-400' : 'text-red-400'}>
                {predictionData?.team_statistics?.away ? '✅ EXISTS' : '❌ MISSING'}
              </span>
            </div>
            <div className="p-2 bg-black/30 rounded">
              <span className="text-gray-400">Keys in predictionData:</span>{' '}
              <span className="text-blue-400">{predictionData ? Object.keys(predictionData).join(', ') : 'N/A'}</span>
            </div>
          </div>
        </div>
      )}

      {/* Combined Performance Dashboard */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-center mb-8">
          <div className="text-center">
            <h3 className="text-gray-400 font-bold text-3xl tracking-wide mb-2" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              Complete Performance Analysis
            </h3>
            <p className="text-slate-400 text-sm">Comprehensive offensive and defensive metrics comparison</p>
          </div>
        </div>

        {/* Modern Radial Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Offensive Radial Chart */}
          <div className="backdrop-blur-xl rounded-2xl p-6 border border-white/5 relative overflow-hidden" style={{
            background: 'linear-gradient(135deg, rgba(30, 58, 138, 0.1), rgba(17, 24, 39, 0.2))',
            boxShadow: '0 8px 32px rgba(59, 130, 246, 0.15)'
          }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl border shadow-xl backdrop-blur-sm" style={{ 
                background: `linear-gradient(135deg, rgb(59 130 246 / 0.3), rgb(37 99 235 / 0.2))`,
                borderColor: `rgb(59 130 246 / 0.5)`,
                boxShadow: '0 8px 32px rgba(59, 130, 246, 0.2)'
              }}>
                <Activity className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h4 className="text-gray-400 text-lg font-bold" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  Offensive Metrics
                </h4>
              </div>
            </div>

            <div className="relative flex items-center justify-center" style={{ minHeight: '450px' }}>
              <svg viewBox="0 0 400 400" className="w-full max-w-md">
                {advancedOffensiveData.map((data, index) => {
                  const awayVal = typeof data.away === 'number' ? data.away : parseFloat(data.away) || 0;
                  const homeVal = typeof data.home === 'number' ? data.home : parseFloat(data.home) || 0;
                  const maxVal = Math.max(awayVal, homeVal);
                  
                  // Calculate angles for radial positioning
                  const totalMetrics = advancedOffensiveData.length;
                  const angleStep = (2 * Math.PI) / totalMetrics;
                  const startAngle = (index * angleStep) - (Math.PI / 2); // Start from top
                  const endAngle = startAngle + angleStep - 0.05; // Small gap between arcs
                  
                  // Arc parameters
                  const centerX = 200;
                  const centerY = 200;
                  const innerRadius = 80;
                  const arcThickness = 20;
                  
                  // Away team arc (outer)
                  const awayRadius = innerRadius + arcThickness * 2 + 10;
                  const awayArcLength = (awayVal / (maxVal || 1)) * (endAngle - startAngle);
                  const awayEndAngle = startAngle + awayArcLength;
                  
                  // Home team arc (inner)
                  const homeRadius = innerRadius + arcThickness;
                  const homeArcLength = (homeVal / (maxVal || 1)) * (endAngle - startAngle);
                  const homeEndAngle = startAngle + homeArcLength;
                  
                  const createArcPath = (r: number, start: number, end: number, thickness: number) => {
                    const innerR = r - thickness;
                    const x1 = centerX + r * Math.cos(start);
                    const y1 = centerY + r * Math.sin(start);
                    const x2 = centerX + r * Math.cos(end);
                    const y2 = centerY + r * Math.sin(end);
                    const x3 = centerX + innerR * Math.cos(end);
                    const y3 = centerY + innerR * Math.sin(end);
                    const x4 = centerX + innerR * Math.cos(start);
                    const y4 = centerY + innerR * Math.sin(start);
                    
                    const largeArc = (end - start) > Math.PI ? 1 : 0;
                    
                    return `M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} L ${x3} ${y3} A ${innerR} ${innerR} 0 ${largeArc} 0 ${x4} ${y4} Z`;
                  };
                  
                  // Label positioning
                  const labelAngle = startAngle + (endAngle - startAngle) / 2;
                  const labelRadius = awayRadius + 30;
                  const labelX = centerX + labelRadius * Math.cos(labelAngle);
                  const labelY = centerY + labelRadius * Math.sin(labelAngle);
                  
                  return (
                    <g key={index}>
                      {/* Away team arc */}
                      <path
                        d={createArcPath(awayRadius, startAngle, awayEndAngle, arcThickness)}
                        fill={awayTeam.primary_color}
                        opacity="0.8"
                        className="transition-all duration-500 hover:opacity-100"
                      >
                        <title>{`${awayTeam.name}: ${awayVal.toFixed(1)}`}</title>
                      </path>
                      
                      {/* Home team arc */}
                      <path
                        d={createArcPath(homeRadius, startAngle, homeEndAngle, arcThickness)}
                        fill={homeTeam.primary_color}
                        opacity="0.8"
                        className="transition-all duration-500 hover:opacity-100"
                      >
                        <title>{`${homeTeam.name}: ${homeVal.toFixed(1)}`}</title>
                      </path>
                      
                      {/* Metric label */}
                      <text
                        x={labelX}
                        y={labelY}
                        textAnchor="middle"
                        fill="white"
                        fontSize="10"
                        fontWeight="600"
                        className="pointer-events-none"
                      >
                        {data.metric}
                      </text>
                    </g>
                  );
                })}
                
                {/* Center legend */}
                <g>
                  <circle cx="200" cy="180" r="5" fill={awayTeam.primary_color} />
                  <text x="210" y="185" fill="white" fontSize="12" fontWeight="500">
                    {awayAbbr}
                  </text>
                  <circle cx="200" cy="210" r="5" fill={homeTeam.primary_color} />
                  <text x="210" y="215" fill="white" fontSize="12" fontWeight="500">
                    {homeAbbr}
                  </text>
                </g>
              </svg>
            </div>
            
            {/* 🔍 DEBUG: Offensive Stats Data */}
            <DebugDataDisplay 
              title="Offensive Metrics - Away Team" 
              data={predictionData?.team_statistics?.away}
              show={debugMode}
            />
            <DebugDataDisplay 
              title="Offensive Metrics - Home Team" 
              data={predictionData?.team_statistics?.home}
              show={debugMode}
            />
          </div>

          {/* Defensive Radial Chart */}
          <div className="backdrop-blur-xl rounded-2xl p-6 border border-white/5 relative overflow-hidden" style={{
            background: 'linear-gradient(135deg, rgba(153, 27, 27, 0.1), rgba(17, 24, 39, 0.2))',
            boxShadow: '0 8px 32px rgba(239, 68, 68, 0.15)'
          }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl border shadow-xl backdrop-blur-sm" style={{
                background: 'linear-gradient(135deg, rgb(239 68 68 / 0.3), rgb(220 38 38 / 0.2))',
                borderColor: 'rgb(239 68 68 / 0.5)',
                boxShadow: '0 8px 32px rgba(239, 68, 68, 0.2)'
              }}>
                <Shield className="w-6 h-6 text-red-400" />
              </div>
              <div>
                <h4 className="text-gray-400 text-lg font-bold" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  Defensive Metrics
                </h4>
              </div>
            </div>

            <div className="relative flex items-center justify-center" style={{ minHeight: '450px' }}>
              <svg viewBox="0 0 400 400" className="w-full max-w-md">
                {defensiveData.map((data, index) => {
                  const awayVal = typeof data.away === 'number' ? data.away : parseFloat(data.away) || 0;
                  const homeVal = typeof data.home === 'number' ? data.home : parseFloat(data.home) || 0;
                  const maxVal = Math.max(awayVal, homeVal);
                  
                  const totalMetrics = defensiveData.length;
                  const angleStep = (2 * Math.PI) / totalMetrics;
                  const startAngle = (index * angleStep) - (Math.PI / 2);
                  const endAngle = startAngle + angleStep - 0.05;
                  
                  const centerX = 200;
                  const centerY = 200;
                  const innerRadius = 80;
                  const arcThickness = 20;
                  
                  const awayRadius = innerRadius + arcThickness * 2 + 10;
                  const awayArcLength = (awayVal / (maxVal || 1)) * (endAngle - startAngle);
                  const awayEndAngle = startAngle + awayArcLength;
                  
                  const homeRadius = innerRadius + arcThickness;
                  const homeArcLength = (homeVal / (maxVal || 1)) * (endAngle - startAngle);
                  const homeEndAngle = startAngle + homeArcLength;
                  
                  const createArcPath = (r: number, start: number, end: number, thickness: number) => {
                    const innerR = r - thickness;
                    const x1 = centerX + r * Math.cos(start);
                    const y1 = centerY + r * Math.sin(start);
                    const x2 = centerX + r * Math.cos(end);
                    const y2 = centerY + r * Math.sin(end);
                    const x3 = centerX + innerR * Math.cos(end);
                    const y3 = centerY + innerR * Math.sin(end);
                    const x4 = centerX + innerR * Math.cos(start);
                    const y4 = centerY + innerR * Math.sin(start);
                    
                    const largeArc = (end - start) > Math.PI ? 1 : 0;
                    
                    return `M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} L ${x3} ${y3} A ${innerR} ${innerR} 0 ${largeArc} 0 ${x4} ${y4} Z`;
                  };
                  
                  const labelAngle = startAngle + (endAngle - startAngle) / 2;
                  const labelRadius = awayRadius + 30;
                  const labelX = centerX + labelRadius * Math.cos(labelAngle);
                  const labelY = centerY + labelRadius * Math.sin(labelAngle);
                  
                  return (
                    <g key={index}>
                      <path
                        d={createArcPath(awayRadius, startAngle, awayEndAngle, arcThickness)}
                        fill={awayTeam.primary_color}
                        opacity="0.8"
                        className="transition-all duration-500 hover:opacity-100"
                      >
                        <title>{`${awayTeam.name}: ${awayVal.toFixed(1)}`}</title>
                      </path>
                      
                      <path
                        d={createArcPath(homeRadius, startAngle, homeEndAngle, arcThickness)}
                        fill={homeTeam.primary_color}
                        opacity="0.8"
                        className="transition-all duration-500 hover:opacity-100"
                      >
                        <title>{`${homeTeam.name}: ${homeVal.toFixed(1)}`}</title>
                      </path>
                      
                      <text
                        x={labelX}
                        y={labelY}
                        textAnchor="middle"
                        fill="white"
                        fontSize="10"
                        fontWeight="600"
                        className="pointer-events-none"
                      >
                        {data.metric}
                      </text>
                    </g>
                  );
                })}
                
                <g>
                  <circle cx="200" cy="180" r="5" fill={awayTeam.primary_color} />
                  <text x="210" y="185" fill="white" fontSize="12" fontWeight="500">
                    {awayAbbr}
                  </text>
                  <circle cx="200" cy="210" r="5" fill={homeTeam.primary_color} />
                  <text x="210" y="215" fill="white" fontSize="12" fontWeight="500">
                    {homeAbbr}
                  </text>
                </g>
              </svg>
            </div>
            
            {/* 🔍 DEBUG: Defensive Stats Data */}
            <DebugDataDisplay 
              title="Defensive Metrics - Away Team" 
              data={predictionData?.team_statistics?.away}
              show={debugMode}
            />
            <DebugDataDisplay 
              title="Defensive Metrics - Home Team" 
              data={predictionData?.team_statistics?.home}
              show={debugMode}
            />
          </div>
        </div>

        {/* MODERN DIVERGING BAR CHARTS - Side by Side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Offensive Metrics */}
          {(() => {
            // Calculate which team has offensive advantage
            const awayOffTotal = advancedOffensiveData.reduce((sum, d) => {
              const val = typeof d.away === 'number' ? d.away : parseFloat(d.away) || 0;
              return sum + val;
            }, 0);
            const homeOffTotal = advancedOffensiveData.reduce((sum, d) => {
              const val = typeof d.home === 'number' ? d.home : parseFloat(d.home) || 0;
              return sum + val;
            }, 0);
            const offLeader = awayOffTotal > homeOffTotal ? awayTeam : homeTeam;
            const offLeaderColor = offLeader.primary_color;
            
            return (
              <div className="relative backdrop-blur-sm bg-white/5 rounded-2xl p-6 border-2 transition-all overflow-hidden" style={{
                borderColor: `${offLeaderColor}50`,
                boxShadow: `0 0 30px ${offLeaderColor}20`
              }}>
                {/* Team Logo Watermark */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none">
                  <ImageWithFallback
                    src={offLeader.logo}
                    alt={offLeader.name}
                    className="w-64 h-64 object-contain"
                    style={{ filter: `drop-shadow(0 0 40px ${offLeaderColor})` }}
                  />
                </div>
                <h5 className="relative text-lg font-bold mb-6 uppercase tracking-wider flex items-center gap-2" style={{ color: offLeaderColor }}>
                  <Activity className="w-5 h-5" />
                  Offensive Battle
                </h5>
            <div className="space-y-3">
              {advancedOffensiveData.map((data, index) => {
                const awayVal = typeof data.away === 'number' ? data.away : parseFloat(data.away) || 0;
                const homeVal = typeof data.home === 'number' ? data.home : parseFloat(data.home) || 0;
                const maxVal = Math.max(Math.abs(awayVal), Math.abs(homeVal)) || 1;
                const awayPercent = (Math.abs(awayVal) / maxVal) * 48; // Increased to 48%
                const homePercent = (Math.abs(homeVal) / maxVal) * 48;
                const awayWins = awayVal > homeVal;
                
                return (
                  <div key={index} className="relative group hover:scale-[1.01] transition-all duration-300">
                    <div className="text-xs text-gray-300 mb-2 font-semibold uppercase tracking-wider text-center">
                      {data.metric}
                    </div>
                    <div className="flex items-center gap-1">
                      {/* Away Team Side */}
                      <div className="flex-1 flex items-center justify-end gap-2">
                        {awayWins && (
                          <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 drop-shadow-[0_0_6px_rgba(5,150,105,0.8)]" />
                        )}
                        <div className={`text-right ${awayWins ? 'text-emerald-400 font-bold' : 'text-gray-500'}`}>
                          <span className="text-sm font-mono">{awayVal.toFixed(1)}</span>
                        </div>
                        <div className="relative h-10 flex items-center justify-end" style={{ width: '48%' }}>
                          <div 
                            className={`h-full rounded-l-lg transition-all duration-700 ease-out relative overflow-hidden ${awayWins ? 'opacity-100' : 'opacity-40'}`}
                            style={{ 
                              width: `${awayPercent}%`,
                              background: `linear-gradient(90deg, transparent, ${awayTeam.primary_color})`,
                              boxShadow: awayWins ? `0 0 20px ${awayTeam.primary_color}80` : 'none'
                            }}
                          >
                            {awayWins && (
                              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                            )}
                          </div>
                          {awayWins && (
                            <div className="absolute -right-1 top-1/2 -translate-y-1/2">
                              <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: awayTeam.primary_color, boxShadow: `0 0 10px ${awayTeam.primary_color}` }}></div>
                            </div>
                          )}
                        </div>
                        <ImageWithFallback
                          src={awayTeam.logo}
                          alt={awayAbbr}
                          className="w-7 h-7 object-contain flex-shrink-0"
                        />
                      </div>
                      
                      {/* Center Divider */}
                      <div className="w-px h-12 bg-gradient-to-b from-transparent via-blue-400 to-transparent"></div>
                      
                      {/* Home Team Side */}
                      <div className="flex-1 flex items-center gap-2">
                        <ImageWithFallback
                          src={homeTeam.logo}
                          alt={homeAbbr}
                          className="w-7 h-7 object-contain flex-shrink-0"
                        />
                        <div className="relative h-10 flex items-center" style={{ width: '48%' }}>
                          <div 
                            className={`h-full rounded-r-lg transition-all duration-700 ease-out relative overflow-hidden ${!awayWins ? 'opacity-100' : 'opacity-40'}`}
                            style={{ 
                              width: `${homePercent}%`,
                              background: `linear-gradient(90deg, ${homeTeam.primary_color}, transparent)`,
                              boxShadow: !awayWins ? `0 0 20px ${homeTeam.primary_color}80` : 'none'
                            }}
                          >
                            {!awayWins && (
                              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                            )}
                          </div>
                          {!awayWins && (
                            <div className="absolute -left-1 top-1/2 -translate-y-1/2">
                              <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: homeTeam.primary_color, boxShadow: `0 0 10px ${homeTeam.primary_color}` }}></div>
                            </div>
                          )}
                        </div>
                        <div className={`text-left ${!awayWins ? 'text-emerald-400 font-bold' : 'text-gray-500'}`}>
                          <span className="text-sm font-mono">{homeVal.toFixed(1)}</span>
                        </div>
                        {!awayWins && (
                          <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 drop-shadow-[0_0_6px_rgba(5,150,105,0.8)]" />
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
              </div>
            );
          })()}

          {/* Defensive Metrics */}
          {(() => {
            // Calculate which team has defensive advantage
            const awayDefTotal = defensiveData.reduce((sum, d) => {
              const val = typeof d.away === 'number' ? d.away : parseFloat(d.away) || 0;
              return sum + val;
            }, 0);
            const homeDefTotal = defensiveData.reduce((sum, d) => {
              const val = typeof d.home === 'number' ? d.home : parseFloat(d.home) || 0;
              return sum + val;
            }, 0);
            const defLeader = awayDefTotal > homeDefTotal ? awayTeam : homeTeam;
            const defLeaderColor = defLeader.primary_color;
            
            return (
              <div className="relative backdrop-blur-sm bg-white/5 rounded-2xl p-6 border-2 transition-all overflow-hidden" style={{
                borderColor: `${defLeaderColor}50`,
                boxShadow: `0 0 30px ${defLeaderColor}20`
              }}>
                {/* Team Logo Watermark */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none">
                  <ImageWithFallback
                    src={defLeader.logo}
                    alt={defLeader.name}
                    className="w-64 h-64 object-contain"
                    style={{ filter: `drop-shadow(0 0 40px ${defLeaderColor})` }}
                  />
                </div>
                <h5 className="relative text-lg font-bold mb-6 uppercase tracking-wider flex items-center gap-2" style={{ color: defLeaderColor }}>
                  <Shield className="w-5 h-5" />
                  Defensive Battle
                </h5>
            <div className="space-y-3">
              {defensiveData.map((data, index) => {
                const awayVal = typeof data.away === 'number' ? data.away : parseFloat(data.away) || 0;
                const homeVal = typeof data.home === 'number' ? data.home : parseFloat(data.home) || 0;
                const maxVal = Math.max(Math.abs(awayVal), Math.abs(homeVal)) || 1;
                const awayPercent = (Math.abs(awayVal) / maxVal) * 48;
                const homePercent = (Math.abs(homeVal) / maxVal) * 48;
                const awayWins = awayVal > homeVal;
                
                return (
                  <div key={index} className="relative group hover:scale-[1.01] transition-all duration-300">
                    <div className="text-xs text-gray-300 mb-2 font-semibold uppercase tracking-wider text-center">
                      {data.metric}
                    </div>
                    <div className="flex items-center gap-1">
                      {/* Away Team Side */}
                      <div className="flex-1 flex items-center justify-end gap-2">
                        {awayWins && (
                          <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 drop-shadow-[0_0_6px_rgba(5,150,105,0.8)]" />
                        )}
                        <div className={`text-right ${awayWins ? 'text-emerald-400 font-bold' : 'text-gray-500'}`}>
                          <span className="text-sm font-mono">{awayVal.toFixed(1)}</span>
                        </div>
                        <div className="relative h-10 flex items-center justify-end" style={{ width: '48%' }}>
                          <div 
                            className={`h-full rounded-l-lg transition-all duration-700 ease-out relative overflow-hidden ${awayWins ? 'opacity-100' : 'opacity-40'}`}
                            style={{ 
                              width: `${awayPercent}%`,
                              background: `linear-gradient(90deg, transparent, ${awayTeam.primary_color})`,
                              boxShadow: awayWins ? `0 0 20px ${awayTeam.primary_color}80` : 'none'
                            }}
                          >
                            {awayWins && (
                              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                            )}
                          </div>
                          {awayWins && (
                            <div className="absolute -right-1 top-1/2 -translate-y-1/2">
                              <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: awayTeam.primary_color, boxShadow: `0 0 10px ${awayTeam.primary_color}` }}></div>
                            </div>
                          )}
                        </div>
                        <ImageWithFallback
                          src={awayTeam.logo}
                          alt={awayAbbr}
                          className="w-7 h-7 object-contain flex-shrink-0"
                        />
                      </div>
                      
                      {/* Center Divider */}
                      <div className="w-px h-12 bg-gradient-to-b from-transparent via-red-400 to-transparent"></div>
                      
                      {/* Home Team Side */}
                      <div className="flex-1 flex items-center gap-2">
                        <ImageWithFallback
                          src={homeTeam.logo}
                          alt={homeAbbr}
                          className="w-7 h-7 object-contain flex-shrink-0"
                        />
                        <div className="relative h-10 flex items-center" style={{ width: '48%' }}>
                          <div 
                            className={`h-full rounded-r-lg transition-all duration-700 ease-out relative overflow-hidden ${!awayWins ? 'opacity-100' : 'opacity-40'}`}
                            style={{ 
                              width: `${homePercent}%`,
                              background: `linear-gradient(90deg, ${homeTeam.primary_color}, transparent)`,
                              boxShadow: !awayWins ? `0 0 20px ${homeTeam.primary_color}80` : 'none'
                            }}
                          >
                            {!awayWins && (
                              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                            )}
                          </div>
                          {!awayWins && (
                            <div className="absolute -left-1 top-1/2 -translate-y-1/2">
                              <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: homeTeam.primary_color, boxShadow: `0 0 10px ${homeTeam.primary_color}` }}></div>
                            </div>
                          )}
                        </div>
                        <div className={`text-left ${!awayWins ? 'text-emerald-400 font-bold' : 'text-gray-500'}`}>
                          <span className="text-sm font-mono">{homeVal.toFixed(1)}</span>
                        </div>
                        {!awayWins && (
                          <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 drop-shadow-[0_0_6px_rgba(5,150,105,0.8)]" />
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
              </div>
            );
          })()}
        </div>
      </GlassCard>

      {/* Game Control Metrics - HIDDEN (duplicate of DriveEfficiencyGameFlow section) */}
      {/* <GlassCard className="p-8">
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
        
        <div className="backdrop-blur-xl rounded-2xl p-8 border border-white/5">
          <RadarStyleChart data={gameControlData} awayTeam={awayTeam} homeTeam={homeTeam} />
        </div>
        
        <DebugDataDisplay 
          title="Game Control - Away Team" 
          data={predictionData?.team_statistics?.away}
          show={debugMode}
        />
        <DebugDataDisplay 
          title="Game Control - Home Team" 
          data={predictionData?.team_statistics?.home}
          show={debugMode}
        />
      </GlassCard> */}

      {/* Team Info & Ratings */}
      {teamInfoData.length > 0 && (
        <GlassCard className="p-8">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <div className="p-4 rounded-xl border shadow-xl backdrop-blur-sm" style={{
                background: 'linear-gradient(to bottom right, rgb(245 158 11 / 0.2), rgb(234 88 12 / 0.2))',
                borderColor: 'rgb(245 158 11 / 0.4)'
              }}>
                <Trophy className="w-8 h-8 text-amber-400" />
              </div>
              <div>
                <h3 className="text-white font-bold text-2xl tracking-wide" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  Team Info & Ratings
                </h3>
                <p className="text-slate-300 text-sm">Complete record, rankings, and advanced ratings</p>
              </div>
            </div>
          </div>
          
          <div className="backdrop-blur-xl rounded-2xl p-8 border border-white/5">
            <HorizontalBarChart data={teamInfoData} awayTeam={awayTeam} homeTeam={homeTeam} />
          </div>
        </GlassCard>
      )}
    </div>
  );
}


