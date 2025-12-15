import React, { useState, useEffect } from 'react';
import { GlassCard } from './GlassCard';
import { ImageWithFallback } from './figma/ImageWithFallback';
import {
  TrendingUp,
  Target,
  Activity,
  Zap,
  MapPin,
  BarChart3,
  Shield,
  Clock,
  ArrowRight,
  Flame,
  TrendingDown,
  Minus,
  Crosshair,
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie
} from 'recharts';

interface DriveEfficiencyGameFlowProps {
  predictionData?: any;
}

export const DriveEfficiencyGameFlow: React.FC<DriveEfficiencyGameFlowProps> = ({
  predictionData,
}) => {
  const [advancedMetrics, setAdvancedMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  // Extract team data from team_selector
  const awayTeam = predictionData?.team_selector?.away_team || { name: 'Away', abbreviation: 'AWAY', logo: '', primary_color: '#ef4444' };
  const homeTeam = predictionData?.team_selector?.home_team || { name: 'Home', abbreviation: 'HOME', logo: '', primary_color: '#3b82f6' };

  const homeAbbr = homeTeam.abbreviation || homeTeam.name?.substring(0, 4).toUpperCase() || 'HOME';
  const awayAbbr = awayTeam.abbreviation || awayTeam.name?.substring(0, 4).toUpperCase() || 'AWAY';

  // Helper function to detect blue or black colors (same as ComprehensiveStats)
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get display colors (same logic as ComprehensiveStats)
  const awayTeamColor = (awayTeam.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam.primary_color || '#f97316');

  // Fetch advanced drive analytics
  useEffect(() => {
    if (homeTeam.name && awayTeam.name) {
      fetch(`http://localhost:5002/advanced-drive-analytics/${homeTeam.name}/${awayTeam.name}`)
        .then(res => res.json())
        .then(data => {
          setAdvancedMetrics(data);
          setLoading(false);
        })
        .catch(err => {
          console.error('Failed to fetch advanced drive analytics:', err);
          setLoading(false);
        });
    }
  }, [homeTeam.name, awayTeam.name]);

  // Sample data structure - replace with actual data from predictionData
  const quarterlyPerformance = {
    away: { Q1: 62.1, Q2: 43.2, Q3: 55.3, Q4: 29.6 },
    home: { Q1: 57.6, Q2: 53.3, Q3: 40, Q4: 50 },
  };

  // Calculate play style indicators
  const calculatePlayStyle = (quarters: { Q1: number; Q2: number; Q3: number; Q4: number }) => {
    const q1 = quarters.Q1;
    const q2 = quarters.Q2;
    const q3 = quarters.Q3;
    const q4 = quarters.Q4;
    
    const firstHalf = (q1 + q2) / 2;
    const secondHalf = (q3 + q4) / 2;
    const differential = secondHalf - firstHalf;
    
    // Determine style
    let style = '';
    let IconComponent: any = null;
    let color = '';
    
    if (differential > 10) {
      style = 'Strong Finisher';
      IconComponent = Flame;
      color = 'text-orange-400';
    } else if (differential < -10) {
      style = 'Fast Starter';
      IconComponent = Zap;
      color = 'text-yellow-400';
    } else if (Math.max(q1, q2, q3, q4) - Math.min(q1, q2, q3, q4) < 10) {
      style = 'Consistent';
      IconComponent = Minus;
      color = 'text-green-400';
    } else {
      style = 'Momentum Shifter';
      IconComponent = TrendingUp;
      color = 'text-blue-400';
    }
    
    return { style, IconComponent, color, firstHalf, secondHalf, differential };
  };

  const homeStyle = calculatePlayStyle(quarterlyPerformance.home);
  const awayStyle = calculatePlayStyle(quarterlyPerformance.away);

  const fieldPositionScoring = {
    away: {
      'Own 1-20': { drives: 25, scoring: 20 },
      'Own 21-40': { drives: 39, scoring: 66.7 },
      'Own 41-Mid': { drives: 9, scoring: 33.3 },
      'Opp Territory': { drives: 59, scoring: 50.8 },
    },
    home: {
      'Own 1-20': { drives: 22, scoring: 50 },
      'Own 21-40': { drives: 37, scoring: 54.1 },
      'Own 41-Mid': { drives: 7, scoring: 85.7 },
      'Opp Territory': { drives: 60, scoring: 43.3 },
    },
  };

  const driveOutcomes = {
    away: {
      touchdowns: 37.1,
      fieldGoals: 10.6,
      punts: 29.5,
      turnovers: 9.8,
      powerSuccess: 47.7,
    },
    home: {
      touchdowns: 38.9,
      fieldGoals: 10.3,
      punts: 27,
      turnovers: 7.9,
      powerSuccess: 49.2,
    },
  };

  const gameControlMetrics = {
    away: {
      possessionTime: '402:05',
      possessionPercent: 50.3,
      turnoverMargin: -1,
      turnoverPercent: -14.3,
      penaltyYards: 491,
      penaltyPercent: 47.9,
      gamesPlayed: 12,
      gamesPercent: 50.0,
      drivesPerGame: 10.2,
      drivesPercent: 50.2,
    },
    home: {
      possessionTime: '398:03',
      possessionPercent: 49.7,
      turnoverMargin: 8,
      turnoverPercent: 114.3,
      penaltyYards: 535,
      penaltyPercent: 52.1,
      gamesPlayed: 12,
      gamesPercent: 50.0,
      drivesPerGame: 10.1,
      drivesPercent: 49.8,
    },
  };

  // Count advantages for game control
  const awayAdvantages = [
    gameControlMetrics.away.possessionPercent > gameControlMetrics.home.possessionPercent,
    gameControlMetrics.away.turnoverMargin > gameControlMetrics.home.turnoverMargin,
    gameControlMetrics.away.penaltyYards < gameControlMetrics.home.penaltyYards,
    gameControlMetrics.away.drivesPerGame > gameControlMetrics.home.drivesPerGame,
  ].filter(Boolean).length;

  const homeAdvantages = 4 - awayAdvantages;

  // Prepare chart data
  const quarterChartData = [
    { quarter: 'Q1', [awayTeam.name]: quarterlyPerformance.away.Q1, [homeTeam.name]: quarterlyPerformance.home.Q1 },
    { quarter: 'Q2', [awayTeam.name]: quarterlyPerformance.away.Q2, [homeTeam.name]: quarterlyPerformance.home.Q2 },
    { quarter: 'Q3', [awayTeam.name]: quarterlyPerformance.away.Q3, [homeTeam.name]: quarterlyPerformance.home.Q3 },
    { quarter: 'Q4', [awayTeam.name]: quarterlyPerformance.away.Q4, [homeTeam.name]: quarterlyPerformance.home.Q4 },
  ];

  const fieldPositionChartData = [
    { zone: '1-20', [awayTeam.name]: fieldPositionScoring.away['Own 1-20'].scoring, [homeTeam.name]: fieldPositionScoring.home['Own 1-20'].scoring },
    { zone: '21-40', [awayTeam.name]: fieldPositionScoring.away['Own 21-40'].scoring, [homeTeam.name]: fieldPositionScoring.home['Own 21-40'].scoring },
    { zone: '41-Mid', [awayTeam.name]: fieldPositionScoring.away['Own 41-Mid'].scoring, [homeTeam.name]: fieldPositionScoring.home['Own 41-Mid'].scoring },
    { zone: 'Opp Territory', [awayTeam.name]: fieldPositionScoring.away['Opp Territory'].scoring, [homeTeam.name]: fieldPositionScoring.home['Opp Territory'].scoring },
  ];

  const radarChartData = [
    { metric: 'TD%', [awayTeam.name]: driveOutcomes.away.touchdowns, [homeTeam.name]: driveOutcomes.home.touchdowns },
    { metric: 'FG%', [awayTeam.name]: driveOutcomes.away.fieldGoals, [homeTeam.name]: driveOutcomes.home.fieldGoals },
    { metric: 'POWER', [awayTeam.name]: driveOutcomes.away.powerSuccess, [homeTeam.name]: driveOutcomes.home.powerSuccess },
    { metric: 'PUNT', [awayTeam.name]: driveOutcomes.away.punts, [homeTeam.name]: driveOutcomes.home.punts },
    { metric: 'TO%', [awayTeam.name]: driveOutcomes.away.turnovers, [homeTeam.name]: driveOutcomes.home.turnovers },
  ];

  return (
    <GlassCard className="p-6 border-slate-500/40">
      {/* Tactical Header */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-700/50">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-slate-800/60 border border-slate-600/40">
            <Crosshair className="w-5 h-5 text-cyan-400 animate-pulse" />
          </div>
          <div>
            <h3 className="text-white font-bold text-lg uppercase tracking-wider">Tactical Drive Analytics</h3>
            <p className="text-slate-400 text-xs uppercase tracking-widest font-mono">Efficiency Velocity & Zone Mastery</p>
          </div>
        </div>
        <div className="flex gap-4">
          <div className="text-center px-3 py-2 bg-slate-900/50 rounded border border-slate-700">
            <div className="text-xs text-slate-500 uppercase font-mono">Unit A</div>
            <div className="font-bold text-sm" style={{ color: awayTeamColor }}>{awayAbbr}</div>
          </div>
          <div className="text-center px-3 py-2 bg-slate-900/50 rounded border border-slate-700">
            <div className="text-xs text-slate-500 uppercase font-mono">Unit B</div>
            <div className="font-bold text-sm" style={{ color: homeTeamColor }}>{homeAbbr}</div>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
        
        {/* Quarter Performance - Sharp Line Chart */}
        <div className="lg:col-span-8 border border-white/10 rounded-lg p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h4 className="text-white font-bold uppercase tracking-wider flex items-center gap-2 text-sm">
                <Activity className="w-4 h-4 text-cyan-400" />
                Efficiency Velocity
              </h4>
              <p className="text-xs text-slate-500 font-mono mt-1">Quarter-by-Quarter Scoring %</p>
            </div>
            <div className="text-right font-mono text-xs">
              <div className="text-slate-500">MAX VARIANCE</div>
              <div className="text-cyan-400 font-bold">
                {Math.max(...quarterChartData.map(d => Math.abs(d[awayTeam.name] - d[homeTeam.name]))).toFixed(1)}%
              </div>
            </div>
          </div>
          
          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={quarterChartData}>
                <defs>
                  <linearGradient id="awayGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={awayTeamColor} stopOpacity={0.1} />
                    <stop offset="100%" stopColor={awayTeamColor} stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="homeGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={homeTeamColor} stopOpacity={0.1} />
                    <stop offset="100%" stopColor={homeTeamColor} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
                <XAxis 
                  dataKey="quarter" 
                  stroke="#666" 
                  style={{ fontSize: '12px', fontFamily: 'monospace' }}
                />
                <YAxis 
                  stroke="#666" 
                  style={{ fontSize: '12px', fontFamily: 'monospace' }}
                  domain={[0, 100]}
                  tickFormatter={(val) => `${val}%`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.95)',
                    border: '1px solid #333',
                    borderRadius: '4px',
                    fontFamily: 'monospace'
                  }}
                  labelStyle={{ color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  formatter={(value: any) => `${value}%`}
                />
                <Legend 
                  wrapperStyle={{ fontFamily: 'monospace', fontSize: '11px' }}
                />
                <Line
                  type="monotone"
                  dataKey={awayTeam.name}
                  stroke={awayTeamColor}
                  strokeWidth={2}
                  dot={{ r: 4, fill: '#000', stroke: awayTeamColor, strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                  fill="url(#awayGradient)"
                />
                <Line
                  type="monotone"
                  dataKey={homeTeam.name}
                  stroke={homeTeamColor}
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={{ r: 4, fill: '#000', stroke: homeTeamColor, strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                  fill="url(#homeGradient)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Quarter Deltas */}
          <div className="mt-4 grid grid-cols-4 gap-2 bg-slate-900/50 p-3 border border-slate-800 rounded">
            {quarterChartData.map((data, idx) => {
              const delta = data[awayTeam.name] - data[homeTeam.name];
              const leader = delta > 0 ? awayTeam.name : homeTeam.name;
              return (
                <div key={idx} className="text-center border-r border-slate-800 last:border-r-0">
                  <div className="text-[10px] text-slate-500 uppercase font-mono">{data.quarter}</div>
                  <div className={`font-mono text-xs font-bold ${delta > 0 ? 'text-cyan-400' : 'text-orange-400'}`}>
                    {Math.abs(delta).toFixed(1)}%
                  </div>
                  <div className="text-[9px] text-slate-600">{leader.split(' ').pop()}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Metrics Column */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* Ball Security Index */}
          <div className="border border-white/10 rounded-lg p-5">
            <h4 className="text-xs font-bold uppercase text-slate-400 mb-4 border-b border-slate-800 pb-2 font-mono">
              Ball Security Index
            </h4>
            <div className="flex items-center justify-between mb-4">
              <div className="text-center">
                <div className="text-3xl font-bold font-mono" style={{ color: awayTeamColor, textShadow: `0 0 8px ${awayTeamColor}` }}>
                  {driveOutcomes.away.turnovers.toFixed(1)}<span className="text-sm">%</span>
                </div>
                <div className="text-[10px] uppercase tracking-widest mt-1 text-slate-500">{awayAbbr} Risk</div>
              </div>
              <div className="text-slate-600 text-xl font-thin">VS</div>
              <div className="text-center">
                <div className="text-3xl font-bold font-mono" style={{ color: homeTeamColor, textShadow: `0 0 8px ${homeTeamColor}` }}>
                  {driveOutcomes.home.turnovers.toFixed(1)}<span className="text-sm">%</span>
                </div>
                <div className="text-[10px] uppercase tracking-widest mt-1 text-slate-500">{homeAbbr} Risk</div>
              </div>
            </div>
            <div className="font-mono text-xs text-center border border-dashed border-slate-700 p-2 rounded" style={{
              background: driveOutcomes.away.turnovers < driveOutcomes.home.turnovers 
                ? 'rgba(0, 255, 136, 0.05)' 
                : 'rgba(255, 170, 0, 0.05)',
              color: driveOutcomes.away.turnovers < driveOutcomes.home.turnovers ? '#00ff88' : '#ffaa00',
              borderColor: driveOutcomes.away.turnovers < driveOutcomes.home.turnovers ? '#00ff88' : '#ffaa00'
            }}>
              <Shield className="w-3 h-3 inline mr-1" />
              {driveOutcomes.away.turnovers < driveOutcomes.home.turnovers ? awayAbbr : homeAbbr} ADVANTAGE
            </div>
          </div>

          {/* Power Success Bars */}
          <div className="border border-white/10 rounded-lg p-5">
            <h4 className="text-xs font-bold uppercase text-slate-400 mb-4 border-b border-slate-800 pb-2 font-mono">
              Power Success Rate
            </h4>
            
            <div className="mb-4">
              <div className="flex justify-between text-xs mb-2 font-mono">
                <span className="text-slate-400">{awayAbbr}</span>
                <span className="text-white font-bold">{driveOutcomes.away.powerSuccess.toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-slate-900 w-full relative border border-slate-800">
                <div 
                  style={{ width: `${driveOutcomes.away.powerSuccess}%`, backgroundColor: awayTeamColor, boxShadow: `0 0 10px ${awayTeamColor}` }}
                  className="h-full transition-all duration-500"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-2 font-mono">
                <span className="text-slate-400">{homeAbbr}</span>
                <span className="text-white font-bold">{driveOutcomes.home.powerSuccess.toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-slate-900 w-full relative border border-slate-800">
                <div 
                  style={{ width: `${driveOutcomes.home.powerSuccess}%`, backgroundColor: homeTeamColor, boxShadow: `0 0 10px ${homeTeamColor}` }}
                  className="h-full transition-all duration-500 opacity-80"
                />
              </div>
            </div>
          </div>

          {/* TD vs FG Split */}
          <div className="border border-white/10 rounded-lg p-5 flex-grow flex flex-col justify-center">
            <h4 className="text-xs font-bold uppercase text-slate-400 mb-3 font-mono">TD/FG Split</h4>
            <div className="grid grid-cols-2 gap-3">
              <div className="text-center p-2 bg-slate-900/50 border border-slate-800 rounded">
                <div className="text-[10px] text-slate-500 uppercase">TDs</div>
                <div className="text-lg font-bold font-mono" style={{ color: awayTeamColor }}>
                  {driveOutcomes.away.touchdowns.toFixed(1)}%
                </div>
              </div>
              <div className="text-center p-2 bg-slate-900/50 border border-slate-800 rounded">
                <div className="text-[10px] text-slate-500 uppercase">TDs</div>
                <div className="text-lg font-bold font-mono" style={{ color: homeTeamColor }}>
                  {driveOutcomes.home.touchdowns.toFixed(1)}%
                </div>
              </div>
              <div className="text-center p-2 bg-slate-900/50 border border-slate-800 rounded">
                <div className="text-[10px] text-slate-500 uppercase">FGs</div>
                <div className="text-sm font-bold font-mono text-cyan-400">
                  {driveOutcomes.away.fieldGoals.toFixed(1)}%
                </div>
              </div>
              <div className="text-center p-2 bg-slate-900/50 border border-slate-800 rounded">
                <div className="text-[10px] text-slate-500 uppercase">FGs</div>
                <div className="text-sm font-bold font-mono text-orange-400">
                  {driveOutcomes.home.fieldGoals.toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Field Position & Radar Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-7 gap-6 mb-6">
        
        {/* Field Position Histogram */}
        <div className="lg:col-span-4 border border-white/10 rounded-lg p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h4 className="text-white font-bold uppercase tracking-wider flex items-center gap-2 text-sm">
                <Target className="w-4 h-4 text-cyan-400" />
                Zone Mastery
              </h4>
              <p className="text-xs text-slate-500 font-mono mt-1">Scoring Probability by Field Position</p>
            </div>
          </div>
          
          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={fieldPositionChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
                <XAxis 
                  dataKey="zone" 
                  stroke="#666" 
                  style={{ fontSize: '10px', fontFamily: 'monospace' }}
                  angle={-20}
                  textAnchor="end"
                  height={60}
                />
                <YAxis 
                  stroke="#666" 
                  style={{ fontSize: '12px', fontFamily: 'monospace' }}
                  tickFormatter={(val) => `${val}%`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.95)',
                    border: '1px solid #333',
                    borderRadius: '4px',
                    fontFamily: 'monospace'
                  }}
                  formatter={(value: any) => `${value}%`}
                />
                <Bar 
                  dataKey={awayTeam.name} 
                  fill={awayTeamColor} 
                  opacity={0.9}
                  radius={[4, 4, 0, 0]}
                />
                <Bar 
                  dataKey={homeTeam.name} 
                  fill="transparent" 
                  stroke={homeTeamColor}
                  strokeWidth={2}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Drive Outcome Radar */}
        <div className="lg:col-span-3 border border-white/10 rounded-lg p-6">
          <div className="mb-6">
            <h4 className="text-white font-bold uppercase tracking-wider flex items-center gap-2 text-sm">
              <Crosshair className="w-4 h-4 text-cyan-400" />
              Outcome Profile
            </h4>
            <p className="text-xs text-slate-500 font-mono mt-1">Drive Result Distribution</p>
          </div>
          
          <div className="h-[280px] w-full flex justify-center items-center relative">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarChartData}>
                <PolarGrid stroke="#444" strokeWidth={1} />
                <PolarAngleAxis 
                  dataKey="metric" 
                  tick={{ fill: '#94a3b8', fontSize: 11, fontFamily: 'monospace' }}
                  stroke="#64748b"
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]} 
                  tick={{ fill: '#64748b', fontSize: 10 }}
                  stroke="#475569"
                  axisLine={{ stroke: '#475569' }}
                />
                <Radar
                  name={awayTeam.name}
                  dataKey={awayTeam.name}
                  stroke={awayTeamColor}
                  fill={awayTeamColor}
                  fillOpacity={0.25}
                  strokeWidth={2.5}
                />
                <Radar
                  name={homeTeam.name}
                  dataKey={homeTeam.name}
                  stroke={homeTeamColor}
                  fill={homeTeamColor}
                  fillOpacity={0.25}
                  strokeWidth={2.5}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(148, 163, 184, 0.2)',
                    borderRadius: '8px',
                    fontFamily: 'monospace',
                    color: '#e2e8f0'
                  }}
                  labelStyle={{ color: '#f1f5f9' }}
                />
              </RadarChart>
            </ResponsiveContainer>
            {/* Decorative circle overlay */}
            <div className="absolute inset-0 rounded-full border border-dashed border-slate-600/30 w-[180px] h-[180px] m-auto pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Advanced Drive Analytics Section */}
      {advancedMetrics && (
        <>
          <div className="mt-6 grid lg:grid-cols-3 gap-4">
            {/* Red Zone Efficiency */}
            <div className="border border-white/10 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <Target className="w-3.5 h-3.5 text-slate-500" />
                <h3 className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Red Zone Efficiency</h3>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-white/10">
                  <span className="text-[10px] text-slate-500 font-mono">{awayAbbr}</span>
                  <div className="text-right">
                    <span className="text-lg font-mono text-slate-300">{advancedMetrics.away_metrics.red_zone_efficiency.toFixed(1)}</span>
                    <p className="text-[9px] text-slate-600 font-mono">
                      {advancedMetrics.away_metrics.red_zone_scores}/{advancedMetrics.away_metrics.red_zone_attempts}
                    </p>
                  </div>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-[10px] text-slate-500 font-mono">{homeAbbr}</span>
                  <div className="text-right">
                    <span className="text-lg font-mono text-slate-300">{advancedMetrics.home_metrics.red_zone_efficiency.toFixed(1)}</span>
                    <p className="text-[9px] text-slate-600 font-mono">
                      {advancedMetrics.home_metrics.red_zone_scores}/{advancedMetrics.home_metrics.red_zone_attempts}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Drive Style Distribution */}
            <div className="border border-white/10 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <Activity className="w-3.5 h-3.5 text-slate-500" />
                <h3 className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Drive Styles</h3>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-[9px] text-slate-600 font-mono mb-3 uppercase">{awayAbbr}</p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between py-1.5 border-b border-white/10">
                      <span className="text-[10px] text-slate-500 font-mono">Explosive</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.away_metrics.explosive_pct.toFixed(1)}</span>
                    </div>
                    <div className="flex items-center justify-between py-1.5 border-b border-white/10">
                      <span className="text-[10px] text-slate-500 font-mono">Methodical</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.away_metrics.methodical_pct.toFixed(1)}</span>
                    </div>
                    <div className="flex items-center justify-between py-1.5">
                      <span className="text-[10px] text-slate-500 font-mono">Quick Strike</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.away_metrics.quick_strike_pct.toFixed(1)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <p className="text-[9px] text-slate-600 font-mono mb-3 uppercase">{homeAbbr}</p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between py-1.5 border-b border-white/10">
                      <span className="text-[10px] text-slate-500 font-mono">Explosive</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.home_metrics.explosive_pct.toFixed(1)}</span>
                    </div>
                    <div className="flex items-center justify-between py-1.5 border-b border-white/10">
                      <span className="text-[10px] text-slate-500 font-mono">Methodical</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.home_metrics.methodical_pct.toFixed(1)}</span>
                    </div>
                    <div className="flex items-center justify-between py-1.5">
                      <span className="text-[10px] text-slate-500 font-mono">Quick Strike</span>
                      <span className="text-sm font-mono text-slate-300">{advancedMetrics.home_metrics.quick_strike_pct.toFixed(1)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Three & Out Rate */}
            <div className="border border-white/10 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <TrendingDown className="w-3.5 h-3.5 text-slate-500" />
                <h3 className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Three & Out Rate</h3>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-white/10">
                  <span className="text-[10px] text-slate-500 font-mono">{awayAbbr}</span>
                  <span className="text-lg font-mono text-slate-300">
                    {advancedMetrics.away_metrics.three_and_out_pct.toFixed(1)}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-white/10">
                  <span className="text-[10px] text-slate-500 font-mono">{homeAbbr}</span>
                  <span className="text-lg font-mono text-slate-300">
                    {advancedMetrics.home_metrics.three_and_out_pct.toFixed(1)}
                  </span>
                </div>
                <div className="pt-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] text-slate-600 font-mono uppercase">Advantage</span>
                    <span className="text-xs font-mono text-slate-400">
                      {advancedMetrics.away_metrics.three_and_out_pct < advancedMetrics.home_metrics.three_and_out_pct ? awayAbbr : homeAbbr} -{Math.abs(advancedMetrics.home_metrics.three_and_out_pct - advancedMetrics.away_metrics.three_and_out_pct).toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quarter-by-Quarter Predictions */}
          <div className="mt-6 border border-white/10 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <Crosshair className="w-4 h-4 text-slate-400" />
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400">Quarter-by-Quarter Analysis</h3>
              <div className="ml-auto flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <div className="w-1.5 h-1.5 rounded-full bg-slate-600" />
                <span>Game Flow Predictions</span>
              </div>
            </div>
            
            {/* Scoring Efficiency Line Chart */}
            <div className="mb-6 rounded-xl p-4 border border-white/10">
              <h4 className="text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-4">Scoring Efficiency by Quarter</h4>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={(() => {
                  const quarters = Object.keys(advancedMetrics.quarter_predictions).filter(q => !q.includes('5')); // Filter out overtime
                  return quarters.map(quarter => ({
                    quarter,
                    [awayTeam.name]: advancedMetrics.quarter_predictions[quarter].away_scoring_pct,
                    [homeTeam.name]: advancedMetrics.quarter_predictions[quarter].home_scoring_pct
                  }));
                })()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
                  <XAxis 
                    dataKey="quarter" 
                    tick={{ fill: '#94a3b8', fontSize: 12, fontFamily: 'monospace' }}
                    stroke="#475569"
                  />
                  <YAxis 
                    tick={{ fill: '#94a3b8', fontSize: 11, fontFamily: 'monospace' }}
                    stroke="#475569"
                    label={{ value: 'Scoring %', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(15, 23, 42, 0.95)',
                      border: '1px solid rgba(148, 163, 184, 0.2)',
                      borderRadius: '8px',
                      fontFamily: 'monospace',
                      color: '#e2e8f0'
                    }}
                    labelStyle={{ color: '#f1f5f9' }}
                    formatter={(value: any) => `${value.toFixed(1)}%`}
                  />
                  <Legend 
                    wrapperStyle={{ fontFamily: 'monospace', fontSize: '11px' }}
                    iconType="line"
                  />
                  <Line
                    type="monotone"
                    dataKey={awayTeam.name}
                    stroke={awayTeamColor}
                    strokeWidth={3}
                    dot={{ fill: awayTeamColor, r: 5, strokeWidth: 2, stroke: '#0f172a' }}
                    activeDot={{ r: 7, strokeWidth: 2 }}
                  />
                  <Line
                    type="monotone"
                    dataKey={homeTeam.name}
                    stroke={homeTeamColor}
                    strokeWidth={3}
                    dot={{ fill: homeTeamColor, r: 5, strokeWidth: 2, stroke: '#0f172a' }}
                    activeDot={{ r: 7, strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Quarter Advantage Bar Chart */}
            <div className="mb-6 rounded-xl p-4 border border-white/10">
              <h4 className="text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-4">Quarter Advantage Differential</h4>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={(() => {
                  const quarters = Object.keys(advancedMetrics.quarter_predictions).filter(q => !q.includes('5'));
                  return quarters.map(quarter => {
                    const data = advancedMetrics.quarter_predictions[quarter];
                    const diff = data.home_scoring_pct - data.away_scoring_pct;
                    return {
                      quarter,
                      differential: diff,
                      fill: Math.abs(diff) < 5 ? '#64748b' : (diff > 0 ? homeTeamColor : awayTeamColor)
                    };
                  });
                })()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
                  <XAxis 
                    dataKey="quarter" 
                    tick={{ fill: '#94a3b8', fontSize: 12, fontFamily: 'monospace' }}
                    stroke="#475569"
                  />
                  <YAxis 
                    tick={{ fill: '#94a3b8', fontSize: 11, fontFamily: 'monospace' }}
                    stroke="#475569"
                    label={{ value: 'Advantage %', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }}
                    domain={[-30, 30]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(15, 23, 42, 0.95)',
                      border: '1px solid rgba(148, 163, 184, 0.2)',
                      borderRadius: '8px',
                      fontFamily: 'monospace',
                      color: '#e2e8f0'
                    }}
                    formatter={(value: any) => {
                      const team = value > 0 ? homeTeam.name : awayTeam.name;
                      return [`${Math.abs(value).toFixed(1)}% ${team} advantage`, 'Differential'];
                    }}
                  />
                  <Bar dataKey="differential" radius={[4, 4, 0, 0]}>
                    {(() => {
                      const quarters = Object.keys(advancedMetrics.quarter_predictions).filter(q => !q.includes('5'));
                      return quarters.map((quarter, index) => {
                        const data = advancedMetrics.quarter_predictions[quarter];
                        const diff = data.home_scoring_pct - data.away_scoring_pct;
                        const fill = Math.abs(diff) < 5 ? '#64748b' : (diff > 0 ? homeTeamColor : awayTeamColor);
                        return <Cell key={`cell-${index}`} fill={fill} />;
                      });
                    })()}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="flex items-center justify-center gap-4 mt-3 text-[10px] font-mono">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded" style={{ backgroundColor: awayTeamColor }} />
                  <span className="text-slate-400">{awayAbbr} Edge</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded bg-slate-600" />
                  <span className="text-slate-400">Even</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded" style={{ backgroundColor: homeTeamColor }} />
                  <span className="text-slate-400">{homeAbbr} Edge</span>
                </div>
              </div>
            </div>

            {/* Quarter Detail Cards */}
            <div className="grid lg:grid-cols-4 gap-4">
              {Object.entries(advancedMetrics.quarter_predictions).filter(([q]) => !q.includes('5')).map(([quarter, data]: [string, any]) => (
                <div key={quarter} className="border border-white/10 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-sm font-mono text-slate-300">{quarter}</h4>
                    <div className="px-2 py-0.5 rounded text-[9px] font-mono uppercase text-slate-500 border border-white/10">
                      {data.confidence}
                    </div>
                  </div>
                  
                  {/* Team Comparison */}
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-slate-500 font-mono">{awayAbbr}</span>
                      <span className="text-lg font-mono text-slate-300">
                        {data.away_scoring_pct.toFixed(1)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-slate-500 font-mono">{homeAbbr}</span>
                      <span className="text-lg font-mono text-slate-300">
                        {data.home_scoring_pct.toFixed(1)}
                      </span>
                    </div>
                  </div>
                  
                  {/* Edge Indicator */}
                  <div className="mb-3 pb-3 border-b border-white/10">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-slate-500 font-mono uppercase">Edge</span>
                      <span className="text-xs font-mono text-slate-400">
                        {data.edge === 'Even' ? 'Even' : `${data.edge === awayTeam.name ? awayAbbr : homeAbbr} +${Math.abs(data.home_scoring_pct - data.away_scoring_pct).toFixed(1)}`}
                      </span>
                    </div>
                  </div>
                  
                  {/* Analysis Text */}
                  <div>
                    <p className="text-[10px] text-slate-500 leading-relaxed font-mono">
                      {data.analysis}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* OLD CHART.JS CONTENT REMOVED - NOW USING RECHARTS ABOVE */}
    </GlassCard>
  );
};


