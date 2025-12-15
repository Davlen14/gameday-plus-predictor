import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  Terminal, Cpu, User, Trophy, Calendar, Target, Star, 
  TrendingUp, Swords, BarChart3, Users, MapPin, Award,
  Shield, Clipboard, DollarSign, Gem, RefreshCw, Flame,
  Info, Film, TrendingDown
} from 'lucide-react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, RadarChart, 
  PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, AreaChart, Area,
  ScatterChart, Scatter, ReferenceLine, Cell, PieChart, Pie, ComposedChart,
  RadialBarChart, RadialBar
} from 'recharts';
import { GlassCard } from './figma/GlassCard';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

// --- UTILITY FUNCTIONS ---
const parseRecord = (rec) => {
  if (!rec) return 0;
  // Handle "10-2" format
  if (typeof rec === 'string' && rec.includes('-')) {
    const [w, l] = rec.split('-').map(Number);
    if (isNaN(w) || isNaN(l) || (w + l) === 0) return 0;
    return (w / (w + l)) * 100;
  }
  return 0;
};

const calculateTrend = (data) => {
  const n = data.length;
  if (n === 0) return { slope: 0, data: [] };

  const processed = data.map((d, idx) => {
    // Handle different data formats
    const pf = d.points_for || d.pf || 0;
    const pa = d.points_against || d.pa || 0;
    
    return {
      ...d,
      w: d.week || idx + 1,
      pf: pf,
      pa: pa,
      diff: pf - pa,
      opp: d.opponent || d.opp || 'Unknown',
      res: d.result || d.res || (pf > pa ? 'W' : 'L')
    };
  });

  const sumX = processed.reduce((acc, d) => acc + d.w, 0);
  const sumY = processed.reduce((acc, d) => acc + d.pf, 0);
  const sumXY = processed.reduce((acc, d) => acc + (d.w * d.pf), 0);
  const sumXX = processed.reduce((acc, d) => acc + (d.w * d.w), 0);

  const denominator = (n * sumXX - sumX * sumX);
  const slope = denominator === 0 ? 0 : (n * sumXY - sumX * sumY) / denominator;
  const intercept = (sumY - slope * sumX) / n;

  return {
    slope,
    data: processed.map(d => ({ ...d, trend: (slope * d.w) + intercept }))
  };
};

// --- BRAND UTILS ---
const getBranding = (coach, fallbackPrimary = '#00d2ff', fallbackSecondary = '#ff00aa') => {
  const colors = coach?.profile?.colors || {};
  const primary = coach?.profile?.team_color || colors.primary || fallbackPrimary;
  const secondary = coach?.profile?.secondary_color || colors.secondary || fallbackSecondary;
  const logo = coach?.profile?.team_logo || coach?.profile?.logo || null;
  return { primary, secondary, logo };
};

// --- TECH PANEL COMPONENT ---
const TechPanel = ({ children, className = "", title, sub, height, brand }) => {
  const borderColor = brand?.primary || '#0ea5e9';
  return (
    <div
      className={`relative backdrop-blur-xl border ${className} group overflow-hidden flex flex-col`}
      style={{ height, borderColor }}
    >
      {/* Watermark */}
      {brand?.logo && (
        <div
          className="absolute inset-0 pointer-events-none opacity-[0.04] mix-blend-screen"
          style={{
            backgroundImage: `url(${brand.logo})`,
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center',
            backgroundSize: '50%'
          }}
        />
      )}
      {/* Corner Markers */}
      <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2" style={{ borderColor }}></div>
      <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2" style={{ borderColor }}></div>
      <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2" style={{ borderColor }}></div>
      <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2" style={{ borderColor }}></div>
      
      <div className="relative z-10 p-4 h-full flex flex-col min-h-0">
        {title && (
          <div className="flex justify-between items-end mb-4 border-b border-white/10 pb-2 bg-gradient-to-r from-white/5 to-transparent shrink-0">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4" style={{ color: borderColor }} />
              <h3 className="text-xs font-mono font-bold uppercase tracking-[0.2em]" style={{ color: borderColor }}>{title}</h3>
            </div>
            {sub && <span className="text-[9px] font-mono text-white/70 uppercase bg-white/10 px-2 py-0.5 rounded">{sub}</span>}
          </div>
        )}
        <div className="flex-1 min-h-0 relative">
          {children}
        </div>
      </div>
    </div>
  );
};

// --- DATA READOUT COMPONENT ---
const DataReadout = ({ label, value, unit, color, size = "xl" }) => (
  <div className="flex flex-col border-l-2 border-slate-800 pl-3">
    <span className="text-[9px] font-mono text-slate-500 uppercase tracking-wider">{label}</span>
    <div className="flex items-baseline gap-1">
      <span className={`text-${size} font-mono font-bold leading-none`} style={color ? { color } : {}}>{value}</span>
      {unit && <span className="text-[10px] text-slate-600">{unit}</span>}
    </div>
  </div>
);

// --- SEASON TREND CHART ---
const SeasonTrendChart = ({ data, color, coachName }) => {
  const { slope, data: chartData } = useMemo(() => calculateTrend(data || []), [data]);
  
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-slate-500 text-sm">
        No game data available
      </div>
    );
  }

  const isProgressing = slope > 0;
  const trendColor = isProgressing ? '#10b981' : '#f43f5e';
  const gradientId = `grad${color.replace('#', '')}${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className="flex flex-col h-full w-full p-2 border border-white/5 relative">
      <div className="absolute top-2 right-2 z-10 flex items-center gap-2 bg-black/40 px-2 py-1 rounded border border-white/10 backdrop-blur-md">
        <span className="text-[8px] text-slate-400 uppercase tracking-wider">Trend</span>
        <div className={`flex items-center text-[10px] font-bold ${isProgressing ? 'text-emerald-400' : 'text-rose-400'}`}>
          {isProgressing ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
          {isProgressing ? 'PROGRESSION' : 'REGRESSION'}
        </div>
      </div>

      <ResponsiveContainer width="100%" height="100%" minHeight={200}>
        <ComposedChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
          <defs>
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.4}/>
              <stop offset="95%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis 
            dataKey="w" 
            axisLine={false} 
            tickLine={false}
            interval={0}
            tick={(props) => {
              const { x, y, payload } = props;
              const game = chartData.find(d => d.w === payload.value);
              if (!game) return null;
              
              return (
                <g transform={`translate(${x},${y})`}>
                  {game.opponent_logo && (
                    <image 
                      x={-8} 
                      y={0} 
                      width={16} 
                      height={16} 
                      href={game.opponent_logo}
                      opacity={0.8}
                    />
                  )}
                  <text 
                    x={0} 
                    y={20} 
                    textAnchor="middle" 
                    fill="#64748b" 
                    fontSize={8}
                    fontFamily="monospace"
                  >
                    W{payload.value}
                  </text>
                </g>
              );
            }}
          />
          <YAxis tick={{ fill: '#64748b', fontSize: 9 }} axisLine={false} tickLine={false} domain={[0, 'auto']} />
          
          <Tooltip 
            cursor={{ stroke: '#ffffff20', strokeWidth: 2 }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const d = payload[0].payload;
                return (
                  <div className="border border-slate-700 p-3 rounded-lg shadow-2xl">
                    <div className="flex items-center gap-2 mb-2">
                      {d.opponent_logo && (
                        <img 
                          src={d.opponent_logo} 
                          alt={d.opp}
                          className="w-8 h-8 object-contain"
                        />
                      )}
                      <div>
                        <div className="text-[10px] text-slate-400">WEEK {d.w}</div>
                        <div className="text-sm font-bold text-white">{d.opp}</div>
                      </div>
                    </div>
                    <div className="text-xs font-bold mb-2" style={{color}}>{d.res} ({d.pf}-{d.pa})</div>
                    <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-[10px]">
                      <span className="text-slate-500">PF:</span>
                      <span className="text-right font-mono" style={{color}}>{d.pf}</span>
                      <span className="text-slate-500">PA:</span>
                      <span className="text-right font-mono text-rose-400">{d.pa}</span>
                      <span className="text-slate-500">Net:</span>
                      <span className={`text-right font-mono font-bold ${d.diff > 0 ? 'text-emerald-400' : 'text-rose-500'}`}>{d.diff > 0 ? '+' : ''}{d.diff}</span>
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />

          <Area 
            type="monotone" 
            dataKey="pf" 
            stroke={color} 
            fill={`url(#${gradientId})`} 
            strokeWidth={2} 
            activeDot={{ r: 4, fill: '#fff' }} 
          />
          <Line 
            type="monotone" 
            dataKey="pa" 
            stroke="#f43f5e" 
            strokeWidth={2} 
            strokeDasharray="3 3" 
            opacity={0.7}
            dot={(props) => {
              const { cx, cy, payload } = props;
              if (!payload.opponent_logo) return null;
              return (
                <image 
                  x={cx - 10} 
                  y={cy - 10} 
                  width={20} 
                  height={20} 
                  href={payload.opponent_logo}
                />
              );
            }}
          />
          <Line type="monotone" dataKey="trend" stroke={trendColor} strokeWidth={2} dot={false} strokeOpacity={0.8} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

const ModernSpiderChart = ({ data, color1 = "#00d2ff", color2 = "#ff00aa", label1 = "Coach 1", label2 = "Coach 2" }) => {
  return (
    <div className="h-[250px] w-full relative">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#1e293b" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 'bold' }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
          <Radar
            name={label1}
            dataKey="A"
            stroke={color1}
            fill={color1}
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Radar
            name={label2}
            dataKey="B"
            stroke={color2}
            fill={color2}
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Legend wrapperStyle={{ fontSize: '10px', paddingTop: '10px' }}/>
          <Tooltip 
            content={({ active, payload, label }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="border border-slate-700 p-2 rounded shadow-xl text-xs">
                    <div className="font-bold text-slate-300 mb-1">{label}</div>
                    {payload.map((p, i) => (
                      <div key={i} style={{ color: p.color }}>
                        {p.name}: {p.value.toFixed(1)}
                      </div>
                    ))}
                  </div>
                );
              }
              return null;
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

const CoachesComparison = ({ predictionData }) => {

  const [coachData, setCoachData] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);



  // Extract team data from team_selector (same pattern as DriveEfficiencyGameFlow)

  const awayTeam = predictionData?.team_selector?.away_team || { name: null };

  const homeTeam = predictionData?.team_selector?.home_team || { name: null };



  // DEBUG: Log everything

  console.log('🏈 CoachesComparison DEBUG:', {

    predictionData_exists: !!predictionData,

    team_selector_exists: !!predictionData?.team_selector,

    homeTeam: homeTeam,

    awayTeam: awayTeam,

    homeTeam_name: homeTeam.name,

    awayTeam_name: awayTeam.name,

    loading,

    coachData_exists: !!coachData,

    error

  });



  useEffect(() => {

    console.log('🔄 CoachesComparison useEffect triggered:', {

      homeTeam_name: homeTeam.name,

      awayTeam_name: awayTeam.name,

      will_fetch: !!(homeTeam.name && awayTeam.name)

    });

    

    if (homeTeam.name && awayTeam.name) {

      fetchCoachComparison(homeTeam.name, awayTeam.name);

    }

  }, [homeTeam.name, awayTeam.name]);



  const fetchCoachComparison = async (homeTeamName, awayTeamName) => {

    console.log('🌐 Fetching coach comparison:', { homeTeamName, awayTeamName });

    setLoading(true);

    setError(null);

    try {

      const url = `http://localhost:5002/api/coaches/comparison?home_team=${encodeURIComponent(homeTeamName)}&away_team=${encodeURIComponent(awayTeamName)}`;

      console.log('📡 Fetch URL:', url);

      const response = await fetch(url);

      console.log('📥 Response status:', response.status, response.ok);

      

      if (!response.ok) {

        const errorText = await response.text();

        console.error('❌ Response not OK:', { status: response.status, errorText });

        throw new Error(`Failed to fetch coach data (${response.status}): ${errorText.substring(0, 200)}`);

      }

      

      const result = await response.json();

      console.log('✅ Coach data received:', result);

      setCoachData(result);

    } catch (err) {

      console.error('❌ Fetch error:', err);

      setError(err.message);

    } finally {

      setLoading(false);

    }

  };

  // Always compute coach references/branding before any conditional returns to keep hook order stable
  const coach1 = coachData?.coach1;
  const coach2 = coachData?.coach2;
  const comparative_analysis = coachData?.comparative_analysis;
  const hypothetical_matchup = coachData?.hypothetical_matchup;
  const brand1 = useMemo(() => getBranding(coach1), [coach1]);
  const brand2 = useMemo(() => getBranding(coach2, '#ff00aa', '#00d2ff'), [coach2]);



  if (!homeTeam.name || !awayTeam.name) {

    console.log('⏹️ CoachesComparison returning null - no teams selected');

    return null;

  }



  if (loading) {

    return (

      <div className="min-h-[400px] bg-[#020305] text-slate-300 font-mono p-2 md:p-6 relative">

        <div className="absolute inset-0 pointer-events-none z-0" 

             style={{ backgroundImage: 'linear-gradient(rgba(0, 255, 255, 0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.02) 1px, transparent 1px)', backgroundSize: '40px 40px' }}>

        </div>

        <div className="relative z-10">

          <TechPanel title="LOADING // COACH_DATA" sub="PROCESS">

            <div className="flex items-center justify-center py-8">

              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>

              <span className="ml-3">Loading coach comparison...</span>

            </div>

          </TechPanel>

        </div>

      </div>

    );

  }



  // Silently hide component if coach data not available (404 error)

  if (error) {

    console.log('⏹️ CoachesComparison hidden - no coach data available for these teams');

    return null;

  }



  if (!coachData) return null;

  return (

    <GlassCard className="min-h-screen text-slate-300 font-mono selection:bg-cyan-500/30 p-2 md:p-6 border-slate-500/40">

      <div className="relative z-10 max-w-[1920px] mx-auto space-y-6">

        {/* --- HEADER --- */}

        <div className="flex flex-col md:flex-row justify-between items-end border-b border-cyan-900/50 pb-4 backdrop-blur-sm p-4 rounded-t-xl">

          <div>

            <h2 className="text-3xl md:text-6xl font-black text-white tracking-tight leading-none">

              Coach <span style={{ color: brand1.primary }}>Pound-for-Pound</span>

            </h2>

          </div>

          <div className="flex gap-8 text-right items-center">

             <div className="hidden md:block">

                <div className="text-[9px] text-slate-500 uppercase tracking-widest mb-1">Target Alpha</div>

                <div className="text-2xl font-black tracking-tight" style={{ color: brand1.primary }}>{coach1?.profile?.coach_name?.toUpperCase() || 'COACH 1'}</div>

                <div className="text-[10px]" style={{ color: brand1.primary, opacity: 0.7 }}>{coach1?.profile?.school?.toUpperCase() || ''}</div>

             </div>

             <div className="hidden md:block h-10 w-[1px] bg-slate-800"></div>

             <div className="hidden md:block">

                <div className="text-[9px] text-slate-500 uppercase tracking-widest mb-1">Target Beta</div>

                <div className="text-2xl font-black tracking-tight" style={{ color: brand2.primary }}>{coach2?.profile?.coach_name?.toUpperCase() || 'COACH 2'}</div>

                <div className="text-[10px]" style={{ color: brand2.primary, opacity: 0.7 }}>{coach2?.profile?.school?.toUpperCase() || ''}</div>

             </div>

          </div>

        </div>



        {/* --- ROW 1: PROFILES & SCORING TRENDS --- */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-[400px]">

          <TechPanel title="TARGET_ALPHA // LOGS" sub={coach1?.profile?.school?.substring(0, 3).toUpperCase() || 'TM1'} brand={brand1}>

            <div className="flex h-full gap-4">

              <div className="w-1/3 flex flex-col gap-4">

                {coach1?.profile?.headshot_url && (

                  <img 

                    src={coach1.profile.headshot_url} 

                    className="w-full h-56 object-cover object-center border border brightness-75 hover:brightness-100 transition-all" 

                    alt={coach1.profile.coach_name}

                  />

                )}

                <div className="grid grid-cols-3 gap-2 text-xs">

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">Record</div>

                    <div className="font-bold">{coach1?.season_2025_detail?.record || 'N/A'}</div>

                  </div>

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">SP+ Overall</div>

                    <div className="font-bold">{coach1?.season_2025_detail?.sp_overall ? coach1.season_2025_detail.sp_overall.toFixed(1) : 'N/A'}</div>

                  </div>

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">Off/Def</div>

                    <div className="font-bold text-[10px]">

                      {coach1?.season_2025_detail?.sp_offense?.toFixed(1) || 'N/A'} / {coach1?.season_2025_detail?.sp_defense?.toFixed(1) || 'N/A'}

                    </div>

                  </div>

                </div>

              </div>

              <div className="w-2/3 h-full flex flex-col">

                <div className="text-[9px] font-mono text-slate-500 mb-1 uppercase tracking-wider text-right">Scoring Trajectory</div>

                <SeasonTrendChart data={coach1?.season_2025_detail?.games || []} color={brand1.primary} coachName={coach1?.profile?.coach_name} />

              </div>

            </div>

          </TechPanel>



          <TechPanel title="TARGET_BETA // LOGS" sub={coach2?.profile?.school?.substring(0, 3).toUpperCase() || 'TM2'} brand={brand2}>

            <div className="flex h-full gap-4 flex-row-reverse text-right">

              <div className="w-1/3 flex flex-col gap-4 items-end">

                {coach2?.profile?.headshot_url && (

                  <img 

                    src={coach2.profile.headshot_url} 

                    className="w-full h-56 object-cover object-center border border brightness-75 hover:brightness-100 transition-all" 

                    alt={coach2.profile.coach_name}

                  />

                )}

                <div className="grid grid-cols-3 gap-2 text-xs text-right">

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">Record</div>

                    <div className="font-bold">{coach2?.season_2025_detail?.record || 'N/A'}</div>

                  </div>

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">SP+ Overall</div>

                    <div className="font-bold">{coach2?.season_2025_detail?.sp_overall ? coach2.season_2025_detail.sp_overall.toFixed(1) : 'N/A'}</div>

                  </div>

                  <div>

                    <div className="text-[9px] text-slate-500 uppercase">Off/Def</div>

                    <div className="font-bold text-[10px]">

                      {coach2?.season_2025_detail?.sp_offense?.toFixed(1) || 'N/A'} / {coach2?.season_2025_detail?.sp_defense?.toFixed(1) || 'N/A'}

                    </div>

                  </div>

                </div>

              </div>

              <div className="w-2/3 h-full flex flex-col">

                <div className="text-[9px] font-mono text-slate-500 mb-1 uppercase tracking-wider text-left">Scoring Trajectory</div>

                <SeasonTrendChart data={coach2?.season_2025_detail?.games || []} color={brand2.primary} coachName={coach2?.profile?.coach_name} />

              </div>

            </div>

          </TechPanel>

        </div>



        {/* All Content - Compact Layout */}

        <div className="space-y-4">

          {/* Overview & Career Stats Combined */}

          <TechPanel title="CAREER_ANALYSIS // OVERVIEW" sub="DATABASE">

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">

              <CompactMetrics coach1={coach1} coach2={coach2} />

              <div className="space-y-3">

                <CompactStints stints={coach1.stints} coachName={coach1.profile?.coach_name} color={brand1.primary} />

                <CompactStints stints={coach2.stints} coachName={coach2.profile?.coach_name} color={brand2.primary} />

              </div>

            </div>

            

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">

              <CareerTreeNetwork coach={coach1} color={brand1.primary} />

              <CareerTreeNetwork coach={coach2} color={brand2.primary} />

            </div>

            

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

              <CareerAchievementsRadial coach={coach1} color={brand1.primary} />

              <CareerAchievementsRadial coach={coach2} color={brand2.primary} />

            </div>

          </TechPanel>



          {/* 2025 Season & Coaching Style Combined */}

          <TechPanel title="2025_SEASON // STYLE_PROFILE" sub="ACTIVE">

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

              <CompactSeason2025Card season={coach1.season_2025_detail} coach={coach1} />

              <CompactSeason2025Card season={coach2.season_2025_detail} coach={coach2} />

            </div>

          </TechPanel>



          {/* Recruiting Section */}

          <TechPanel title="RECRUITING // TALENT_PIPELINE" sub="CLASSES">

            <RecruitingTab coach1={coach1} coach2={coach2} />

          </TechPanel>



          {/* Advanced Metrics Section */}

          <TechPanel title="ADVANCED_METRICS // PERFORMANCE" sub="ANALYTICS">

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

              <CompactPerformanceCard coach={coach1} />

              <CompactPerformanceCard coach={coach2} />

            </div>

          </TechPanel>



          {/* Matchup Prediction Section */}

          <TechPanel title="MATCHUP_PREDICTION // SIMULATION" sub="FORECAST">

            <MatchupPredictionTab matchup={hypothetical_matchup} coach1={coach1} coach2={coach2} />

          </TechPanel>

        </div>

      </div>

    </GlassCard>

  );

};



// --- COMPACT COMPONENTS ---

const CompactMetrics = ({ coach1, coach2 }) => {
  const color1 = coach1.profile?.team_color || '#00d2ff';
  const color2 = coach2.profile?.team_color || '#ff00aa';
  
  // Aggregate situational stats across all schools
  const aggregateSituational = (coach) => {
    if (!coach.situational_by_school || coach.situational_by_school.length === 0) {
      return { vsRanked: 'N/A', vsTop10: 'N/A', home: 'N/A', away: 'N/A', oneScore: 'N/A', blowouts: 'N/A' };
    }
    
    let vsRankedW = 0, vsRankedL = 0, vsTop10W = 0, vsTop10L = 0;
    let homeW = 0, homeL = 0, awayW = 0, awayL = 0;
    let oneScoreW = 0, oneScoreL = 0, blowoutsW = 0, blowoutsL = 0;
    
    coach.situational_by_school.forEach(s => {
      if (s.vs_ranked) { const [w, l] = s.vs_ranked.split('-').map(Number); vsRankedW += w; vsRankedL += l; }
      if (s.vs_top_10) { const [w, l] = s.vs_top_10.split('-').map(Number); vsTop10W += w; vsTop10L += l; }
      if (s.home) { const [w, l] = s.home.split('-').map(Number); homeW += w; homeL += l; }
      if (s.away) { const [w, l] = s.away.split('-').map(Number); awayW += w; awayL += l; }
      if (s.one_score) { const [w, l] = s.one_score.split('-').map(Number); oneScoreW += w; oneScoreL += l; }
      if (s.blowouts) { const [w, l] = s.blowouts.split('-').map(Number); blowoutsW += w; blowoutsL += l; }
    });
    
    return {
      vsRanked: vsRankedW + vsRankedL > 0 ? `${vsRankedW}-${vsRankedL}` : 'N/A',
      vsTop10: vsTop10W + vsTop10L > 0 ? `${vsTop10W}-${vsTop10L}` : 'N/A',
      home: homeW + homeL > 0 ? `${homeW}-${homeL}` : 'N/A',
      away: awayW + awayL > 0 ? `${awayW}-${awayL}` : 'N/A',
      oneScore: oneScoreW + oneScoreL > 0 ? `${oneScoreW}-${oneScoreL}` : 'N/A',
      blowouts: blowoutsW + blowoutsL > 0 ? `${blowoutsW}-${blowoutsL}` : 'N/A'
    };
  };
  
  const sit1 = aggregateSituational(coach1);
  const sit2 = aggregateSituational(coach2);
  
  const metrics = [
    { label: 'Career Win %', c1: (coach1.career_summary?.win_pct * 100).toFixed(1), c2: (coach2.career_summary?.win_pct * 100).toFixed(1), suffix: '%' },
    { label: 'Total Games', c1: coach1.career_summary?.total_games, c2: coach2.career_summary?.total_games },
    { label: 'Seasons', c1: coach1.career_summary?.seasons_coached, c2: coach2.career_summary?.seasons_coached },
    { label: 'Last 10 Games', c1: coach1.career_summary?.last_10_record, c2: coach2.career_summary?.last_10_record },
    { label: 'vs Ranked', c1: sit1.vsRanked, c2: sit2.vsRanked },
    { label: 'vs Top 10', c1: sit1.vsTop10, c2: sit2.vsTop10 },
    { label: 'Close Games (1 Score)', c1: sit1.oneScore, c2: sit2.oneScore },
    { label: 'Blowouts (>14pts)', c1: sit1.blowouts, c2: sit2.blowouts },
    { label: 'Home Record', c1: sit1.home, c2: sit2.home },
    { label: 'Away Record', c1: sit1.away, c2: sit2.away },
  ];

  return (
    <div className="space-y-1">
      <h4 className="text-xs font-bold mb-3 uppercase tracking-wider" style={{ color: color1 }}>Career Analytics</h4>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1">
        {metrics.map((m, idx) => {
          const val1 = parseFloat(m.c1) || 0;
          const val2 = parseFloat(m.c2) || 0;
          return (
            <div key={idx} className="rounded p-1">
              <div className="text-[8px] text-slate-500 mb-0.5 uppercase tracking-wide">{m.label}</div>
              <div className="flex justify-between gap-2">
                <span className="text-[10px] font-mono font-bold" style={{ color: val1 > val2 ? color1 : '#94a3b8' }}>{m.c1}{m.suffix}</span>
                <span className="text-[10px] font-mono font-bold" style={{ color: val2 > val1 ? color2 : '#94a3b8' }}>{m.c2}{m.suffix}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const CompactStints = ({ stints, coachName, color }) => {
  if (!stints || stints.length === 0) return null;
  
  return (
    <div className="rounded p-2">
      <h5 className="text-[9px] font-bold mb-1 uppercase tracking-wider" style={{ color }}>{coachName}</h5>
      <div className="space-y-1">
        {stints.slice(0, 3).map((stint, idx) => (
          <div key={idx} className="text-[9px] text-slate-300 leading-tight">
            <div className="flex justify-between">
              <span className="font-medium">{stint.school}</span>
              <span className="text-slate-500">{stint.start_year}-{stint.end_year}</span>
            </div>
            <div style={{ color }}>{stint.record} ({(stint.win_pct * 100).toFixed(1)}%)</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const CareerTreeNetwork = ({ coach, color }) => {
  const teamColor = coach.profile?.team_color || color;
  const [timelineData, setTimelineData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    // Fetch timeline data from database
    const fetchTimelineData = async () => {
      try {
        setLoading(true);
        setError(null);
        const coachId = coach.profile?.coach_id || coach.id;
        console.log('🎯 Fetching timeline for coach:', coach.profile?.coach_name || 'Unknown', 'ID:', coachId);
        
        if (!coachId) {
          console.warn('⚠️ No coach ID found');
          setError('No coach ID available');
          setTimelineData(null);
          return;
        }
        
        const response = await fetch(`http://localhost:5555/api/coach/${coachId}/timeline`);
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error('❌ API error:', errorText);
          setError(`API Error: ${response.status}`);
          setTimelineData(null);
          return;
        }
        
        const data = await response.json();
        console.log('✅ Timeline data loaded:', data.coach_name, data.career_record, 'Weekly points:', data.weekly?.length);
        setTimelineData(data);
        setError(null);
      } catch (err) {
        console.error('❌ Failed to load timeline data:', err);
        setError(err.message || 'Failed to load timeline');
        setTimelineData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchTimelineData();
  }, [coach.profile?.coach_id, coach.id]);
  
  // Early return after hooks to follow Rules of Hooks
  if (!coach.stints || coach.stints.length === 0) return null;

  if (loading) {
    return (
      <div className="rounded-lg p-4 h-full flex items-center justify-center" style={{ 
        background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%)',
        border: `1px solid ${teamColor}40`
      }}>
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-slate-600 border-t-transparent" style={{ borderTopColor: teamColor }}></div>
          <div className="text-slate-400 text-sm font-mono">Loading career timeline...</div>
        </div>
      </div>
    );
  }

  if (error || !timelineData) {
    // Silently hide if no timeline data - coach likely doesn't have enough game history yet
    return null;
  }

  // Build Highcharts options with modern styling
  const buildChartOptions = () => {
    // Prepare data series with custom properties
    const weeklyWinPct = timelineData.weekly.map(w => [w.x, w.win_pct]);
    const weeklyHomeWinPct = timelineData.weekly.map(w => [w.x, w.home_win_pct]);
    const weeklyConfWinPct = timelineData.weekly.map(w => [w.x, w.conf_win_pct]);
    const weeklyAPRank = timelineData.weekly.map(w => [w.x, w.ap_rank_score]);
    const weeklyMargin = timelineData.weekly.map(w => [w.x, w.avg_margin]);
    const weeklyRankedWins = timelineData.weekly.map(w => [w.x, w.ranked_wins || 0]);
    const yearlyEliteScore = timelineData.yearly.map(y => [y.x, y.elite_score]);
    const yearlyPPG = timelineData.yearly.filter(y => y.ppg).map(y => [y.x, y.ppg]);
    const yearlyPPGAllowed = timelineData.yearly.filter(y => y.ppg_allowed).map(y => [y.x, y.ppg_allowed]);
    
    // Filter and clean flags data - remove fire emojis, replace with clean text
    const cleanFlags = (timelineData.flags || []).map(flag => ({
      ...flag,
      title: flag.title === '🔥' ? 'W' : 
             flag.title === '🏆' ? 'B' : 
             flag.title === '🌟' ? 'S' :
             flag.title === '💎' ? 'U' :
             flag.title === '⭐' ? 'D' :
             flag.title
    }));

    // School data for multi-school coaches
    const schools = [];
    if (coach.stints && coach.stints.length > 0) {
      coach.stints.sort((a, b) => a.start_year - b.start_year).forEach(stint => {
        const logo = `https://a.espncdn.com/i/teamlogos/ncaa/500/${stint.team_id || '0'}.png`;
        schools.push({
          name: stint.school,
          logo: logo,
          color: stint.team_color || teamColor,
          startYear: stint.start_year,
          endYear: stint.end_year,
          record: stint.record
        });
      });
    }

    return {
      chart: {
        backgroundColor: 'rgba(15, 23, 42, 0.4)',
        style: { 
          fontFamily: '"JetBrains Mono", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace' 
        },
        height: 500,
        zoomType: 'x',
        panning: true,
        panKey: 'shift',
        animation: { duration: 800, easing: 'easeOutQuint' },
        events: {
          load: function() {
            drawWatermarks.call(this, schools, coach, teamColor);
          },
          redraw: function() {
            drawWatermarks.call(this, schools, coach, teamColor);
          }
        }
      },
      title: { text: null },
      credits: { enabled: false },
      xAxis: {
        type: 'datetime',
        gridLineColor: 'rgba(255,255,255,0.03)',
        lineColor: 'rgba(148, 163, 184, 0.2)',
        tickColor: 'rgba(148, 163, 184, 0.2)',
        labels: { 
          style: { 
            color: '#94a3b8', 
            fontSize: '10px',
            fontWeight: '500'
          } 
        },
        plotBands: timelineData.plot_bands?.map((band, idx) => ({
          ...band,
          color: schools[idx] ? `${schools[idx].color}15` : `${teamColor}15`,
          borderColor: schools[idx] ? `${schools[idx].color}40` : `${teamColor}40`,
          borderWidth: 1,
          label: {
            ...band.label,
            style: { 
              color: schools[idx] ? schools[idx].color : teamColor,
              fontWeight: 'bold', 
              fontSize: '9px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            },
            y: -5
          }
        })) || [],
        ordinal: false
      },
      yAxis: [
        {
          title: { text: null },
          labels: { 
            align: 'left',
            x: 5,
            format: '{value}%', 
            style: { 
              color: '#e2e8f0', 
              fontSize: '10px',
              fontWeight: '600'
            } 
          },
          gridLineColor: 'rgba(255,255,255,0.04)',
          gridLineDashStyle: 'Dot',
          min: 0,
          max: 100
        },
        {
          title: { text: null },
          labels: { 
            align: 'right',
            x: -5,
            style: { 
              color: '#fbbf24', 
              fontSize: '10px',
              fontWeight: '600'
            } 
          },
          gridLineColor: 'transparent',
          opposite: true,
          min: 0,
          max: 100
        },
        {
          title: { text: null },
          labels: { 
            align: 'right',
            x: -5,
            style: { 
              color: '#34d399', 
              fontSize: '10px',
              fontWeight: '600'
            } 
          },
          gridLineColor: 'transparent',
          opposite: true,
          min: 0
        }
      ],
      tooltip: {
        useHTML: true,
        backgroundColor: 'rgba(15, 23, 42, 0.98)',
        borderColor: teamColor,
        borderWidth: 2,
        borderRadius: 8,
        padding: 12,
        style: { 
          color: '#e2e8f0', 
          fontSize: '11px',
          fontWeight: '500'
        },
        shared: true,
        split: false,
        xDateFormat: '<b>%b %Y</b>',
        shadow: { color: 'rgba(0,0,0,0.5)', offsetX: 0, offsetY: 4, opacity: 0.6, width: 8 }
      },
      legend: {
        enabled: true,
        align: 'left',
        verticalAlign: 'top',
        itemStyle: { 
          color: '#cbd5e1', 
          fontSize: '9px',
          fontWeight: '600',
          textTransform: 'uppercase',
          letterSpacing: '0.5px'
        },
        itemHoverStyle: { color: teamColor },
        itemDistance: 15,
        symbolRadius: 2,
        symbolHeight: 8,
        symbolWidth: 8
      },
      rangeSelector: { enabled: false },
      navigator: { 
        enabled: true,
        height: 35,
        maskFill: `${teamColor}20`,
        outlineColor: 'rgba(148, 163, 184, 0.3)',
        series: { 
          color: teamColor,
          lineWidth: 1.5,
          fillOpacity: 0.2
        },
        xAxis: { 
          labels: { 
            style: { 
              color: '#64748b',
              fontSize: '9px'
            } 
          },
          gridLineColor: 'rgba(255,255,255,0.05)'
        },
        handles: {
          backgroundColor: teamColor,
          borderColor: '#1e293b',
          height: 20,
          width: 8
        }
      },
      scrollbar: { enabled: false },
      series: [
        {
          name: 'Elite Score',
          data: yearlyEliteScore,
          type: 'areaspline',
          color: teamColor,
          fillColor: { 
            linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 }, 
            stops: [
              [0, `${teamColor}CC`], 
              [0.5, `${teamColor}66`],
              [1, `${teamColor}11`]
            ] 
          },
          yAxis: 0,
          tooltip: { 
            valueSuffix: ' pts',
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}</b><br/>'
          },
          marker: { 
            enabled: true, 
            radius: 4,
            fillColor: teamColor,
            lineColor: '#0f172a',
            lineWidth: 2,
            states: {
              hover: {
                radius: 6,
                lineWidth: 3
              }
            }
          },
          lineWidth: 3,
          zIndex: 3,
          shadow: {
            color: `${teamColor}60`,
            offsetX: 0,
            offsetY: 3,
            opacity: 0.5,
            width: 6
          }
        },
        {
          name: 'Win %',
          data: weeklyWinPct,
          type: 'spline',
          color: '#60a5fa',
          yAxis: 0,
          tooltip: { 
            valueSuffix: '%', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}%</b><br/>'
          },
          marker: { 
            enabled: false,
            states: {
              hover: {
                enabled: true,
                radius: 5,
                fillColor: '#60a5fa',
                lineColor: '#1e40af',
                lineWidth: 2
              }
            }
          },
          lineWidth: 2.5,
          zIndex: 2
        },
        {
          name: 'AP Rank',
          data: weeklyAPRank,
          type: 'spline',
          color: '#fbbf24',
          dashStyle: 'ShortDot',
          yAxis: 1,
          tooltip: { 
            valueSuffix: ' pts', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}</b><br/>'
          },
          marker: { enabled: false },
          lineWidth: 2,
          visible: false,
          zIndex: 1
        },
        {
          name: 'Home Win %',
          data: weeklyHomeWinPct,
          type: 'spline',
          color: '#a78bfa',
          yAxis: 0,
          tooltip: { 
            valueSuffix: '%', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}%</b><br/>'
          },
          marker: { enabled: false },
          lineWidth: 1.5,
          visible: false,
          opacity: 0.8
        },
        {
          name: 'Conf Win %',
          data: weeklyConfWinPct,
          type: 'spline',
          color: '#f472b6',
          yAxis: 0,
          tooltip: { 
            valueSuffix: '%', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}%</b><br/>'
          },
          marker: { enabled: false },
          lineWidth: 1.5,
          visible: false,
          opacity: 0.8
        },
        {
          name: 'PPG',
          data: yearlyPPG,
          type: 'spline',
          color: '#34d399',
          yAxis: 2,
          tooltip: { 
            valueSuffix: ' pts', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}</b><br/>'
          },
          marker: { 
            enabled: true, 
            radius: 3,
            symbol: 'diamond',
            fillColor: '#34d399',
            lineColor: '#065f46',
            lineWidth: 1
          },
          lineWidth: 2,
          visible: false
        },
        {
          name: 'Pts Allowed',
          data: yearlyPPGAllowed,
          type: 'spline',
          color: '#f87171',
          yAxis: 2,
          tooltip: { 
            valueSuffix: ' pts', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}</b><br/>'
          },
          marker: { 
            enabled: true, 
            radius: 3,
            symbol: 'diamond',
            fillColor: '#f87171',
            lineColor: '#7f1d1d',
            lineWidth: 1
          },
          lineWidth: 2,
          visible: false
        },
        {
          name: 'Avg Margin',
          data: weeklyMargin,
          type: 'spline',
          color: '#22d3ee',
          yAxis: 2,
          tooltip: { 
            valueSuffix: ' pts', 
            valueDecimals: 1,
            pointFormat: '<span style="color:{point.color}">●</span> {series.name}: <b>{point.y:.1f}</b><br/>'
          },
          marker: { enabled: false },
          lineWidth: 1.5,
          visible: false,
          opacity: 0.8
        },
        {
          type: 'flags',
          name: 'Milestones',
          data: cleanFlags,
          onSeries: 'Elite Score',
          shape: 'circlepin',
          width: 18,
          height: 18,
          color: '#fbbf24',
          fillColor: '#fbbf24',
          lineColor: '#78350f',
          lineWidth: 2,
          style: { 
            color: '#0f172a', 
            fontWeight: 'bold', 
            fontSize: '11px',
            textShadow: '0 1px 2px rgba(0,0,0,0.5)'
          },
          states: { 
            hover: { 
              fillColor: '#fcd34d',
              lineWidth: 3,
              scale: 1.2
            } 
          },
          zIndex: 10
        }
      ]
    };
  };

  // Modern watermark drawing function with glow effects
  const drawWatermarks = function(schools, coach, teamColor) {
    const chart = this;
    if (!chart || !chart.renderer) return;

    // Clear previous watermarks
    if (chart.watermarkElements) {
      chart.watermarkElements.forEach(el => el && el.destroy && el.destroy());
    }
    chart.watermarkElements = [];

    const plotWidth = chart.plotWidth;
    const plotHeight = chart.plotHeight;
    const plotLeft = chart.plotLeft;
    const plotTop = chart.plotTop;

    if (plotWidth < 300) return; // Too small to render

    // Multi-school: logos chronologically positioned with subtle glow
    if (schools.length > 1) {
      const spacing = plotWidth / schools.length;
      schools.forEach((school, idx) => {
        const logoSize = 70;
        const x = plotLeft + (spacing * idx) + (spacing - logoSize) / 2;
        const y = plotTop + (plotHeight - logoSize) / 2;
        const isCurrent = idx === schools.length - 1;

        // Glow background for current school
        if (isCurrent) {
          chart.watermarkElements.push(
            chart.renderer.circle(x + logoSize/2, y + logoSize/2, logoSize * 0.7)
              .attr({ 
                fill: `${school.color}10`,
                stroke: `${school.color}30`,
                'stroke-width': 2,
                zIndex: 0 
              })
              .add()
          );
        }

        chart.watermarkElements.push(
          chart.renderer.image(school.logo, x, y, logoSize, logoSize)
            .attr({ 
              opacity: isCurrent ? 0.15 : 0.06, 
              zIndex: 0 
            })
            .add()
        );

        // School name label
        chart.watermarkElements.push(
          chart.renderer.text(
            school.name.toUpperCase(),
            x + logoSize / 2,
            y + logoSize + 15
          )
          .css({ 
            color: school.color, 
            fontSize: '8px', 
            fontWeight: 'bold',
            opacity: isCurrent ? 0.5 : 0.3,
            textAlign: 'center',
            letterSpacing: '1px'
          })
          .attr({ 
            zIndex: 0,
            'text-anchor': 'middle'
          })
          .add()
        );
      });
    } else if (schools.length === 1) {
      // Single school: centered logo with modern styling
      const logoSize = 120;
      const x = plotLeft + (plotWidth - logoSize) / 2;
      const y = plotTop + (plotHeight - logoSize) / 2;

      // Glow circle background
      chart.watermarkElements.push(
        chart.renderer.circle(x + logoSize/2, y + logoSize/2, logoSize * 0.65)
          .attr({ 
            fill: `${teamColor}08`,
            stroke: `${teamColor}20`,
            'stroke-width': 3,
            zIndex: 0 
          })
          .add()
      );

      // Logo
      chart.watermarkElements.push(
        chart.renderer.image(schools[0].logo, x, y, logoSize, logoSize)
          .attr({ opacity: 0.10, zIndex: 0 })
          .add()
      );

      // Career stats with modern styling
      const coachName = coach.profile?.coach_name || `${coach.first_name || ''} ${coach.last_name || ''}`.trim();
      const record = `${timelineData.career_record} (${timelineData.career_win_pct?.toFixed(1)}%)`;
      
      chart.watermarkElements.push(
        chart.renderer.text(
          `<span style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;">${coachName}</span><br/><span style="font-size:10px;opacity:0.8;">${record}</span>`,
          x + logoSize / 2,
          y + logoSize + 20
        )
        .css({ 
          color: teamColor, 
          fontSize: '10px', 
          opacity: 0.6, 
          textAlign: 'center',
          fontFamily: '"JetBrains Mono", monospace'
        })
        .attr({ 
          zIndex: 0,
          'text-anchor': 'middle'
        })
        .add()
      );
    }
  };

  return (
    <div className="rounded-lg p-4 h-full" style={{ 
      background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%)',
      border: `1px solid ${teamColor}40`,
      boxShadow: `0 0 20px ${teamColor}10`
    }}>
      <div className="flex items-center justify-between mb-3">
        <h5 className="text-xs font-bold uppercase tracking-wider flex items-center gap-2" style={{ 
          color: teamColor,
          textShadow: `0 0 10px ${teamColor}60`,
          fontFamily: '"JetBrains Mono", monospace',
          letterSpacing: '2px'
        }}>
          <BarChart3 size={14} strokeWidth={2.5} />
          Career Analytics
        </h5>
        <div className="flex items-center gap-2 text-xs" style={{ fontFamily: '"JetBrains Mono", monospace' }}>
          <span className="text-slate-500">W-L:</span>
          <span className="font-bold" style={{ color: teamColor }}>{timelineData.career_record}</span>
          <span className="text-slate-500">|</span>
          <span className="font-bold text-slate-300">{timelineData.career_win_pct?.toFixed(1)}%</span>
        </div>
      </div>
      
      <div className="relative h-[500px] mb-2">
        <HighchartsReact
          highcharts={Highcharts}
          constructorType={'stockChart'}
          options={buildChartOptions()}
          ref={chartRef}
        />
      </div>
      
      <div className="flex flex-wrap gap-3 text-xs pt-2 border-t border-slate-700/50" style={{ fontFamily: '"JetBrains Mono", monospace' }}>
        <div className="flex items-center gap-1.5 px-2 py-1 rounded" style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)' }}>
          <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: teamColor, boxShadow: `0 0 8px ${teamColor}80` }}></div>
          <span className="text-slate-300 font-semibold">Elite</span>
        </div>
        <div className="flex items-center gap-1.5 px-2 py-1 rounded" style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)' }}>
          <div className="w-2.5 h-2.5 rounded-full bg-blue-400" style={{ boxShadow: '0 0 8px rgba(96, 165, 250, 0.5)' }}></div>
          <span className="text-slate-300 font-semibold">Win%</span>
        </div>
        <div className="flex items-center gap-1.5 px-2 py-1 rounded" style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)' }}>
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-400" style={{ boxShadow: '0 0 8px rgba(251, 191, 36, 0.5)' }}></div>
          <span className="text-slate-300 font-semibold">Rank</span>
        </div>
        <div className="flex items-center gap-1.5 px-2 py-1 rounded" style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)' }}>
          <span className="text-slate-500 text-xs flex items-center gap-1"><TrendingUp size={10} /> PPG</span>
          <span className="text-slate-500">•</span>
          <span className="text-slate-500 text-xs flex items-center gap-1"><Shield size={10} /> PA</span>
          <span className="text-slate-500">•</span>
          <span className="text-slate-500 text-xs flex items-center gap-1"><Target size={10} /> Margin</span>
        </div>
        {timelineData.max_win_streak > 0 && (
          <div className="flex items-center gap-1.5 px-2 py-1 rounded ml-auto" style={{ 
            backgroundColor: `${teamColor}20`,
            border: `1px solid ${teamColor}40`
          }}>
            <TrendingUp size={12} style={{ color: '#10b981' }} strokeWidth={2.5} />
            <span className="font-bold" style={{ color: teamColor }}>{timelineData.max_win_streak}</span>
            <span className="text-slate-400 text-xs">streak</span>
          </div>
        )}
      </div>
    </div>
  );
};

const CareerAchievementsRadial = ({ coach, color }) => {
  const teamColor = coach.profile?.team_color || color;
  
  // Extract achievement data
  const getBowlWins = () => {
    const rec = coach.career_summary?.bowl_record;
    if (rec && typeof rec === 'string' && rec.includes('-')) {
      return parseInt(rec.split('-')[0]) || 0;
    }
    return 0;
  };

  const getVsRankedWins = () => {
    if (!coach.situational_by_school || !Array.isArray(coach.situational_by_school)) return 0;
    let totalW = 0;
    coach.situational_by_school.forEach(school => {
      const rec = school.vs_ranked;
      if (rec && typeof rec === 'string' && rec.includes('-')) {
        const w = parseInt(rec.split('-')[0]);
        if (!isNaN(w)) totalW += w;
      }
    });
    return totalW;
  };

  const getVsTop10Wins = () => {
    if (!coach.situational_by_school || !Array.isArray(coach.situational_by_school)) return 0;
    let totalW = 0;
    coach.situational_by_school.forEach(school => {
      const rec = school.vs_top_10;
      if (rec && typeof rec === 'string' && rec.includes('-')) {
        const w = parseInt(rec.split('-')[0]);
        if (!isNaN(w)) totalW += w;
      }
    });
    return totalW;
  };

  const getConfChampionships = () => {
    // Look for conference championships in career summary or achievements
    return coach.career_summary?.conference_championships || 0;
  };

  const totalWins = coach.career_summary?.total_wins || 0;
  const bowlWins = getBowlWins();
  const vsRankedWins = getVsRankedWins();
  const vsTop10Wins = getVsTop10Wins();

  const maxValue = Math.max(totalWins, 100);

  const data = [
    {
      name: 'Total Wins',
      value: totalWins,
      fill: '#fbbf24', // Gold
    },
    {
      name: 'vs Ranked',
      value: vsRankedWins,
      fill: '#94a3b8', // Silver
    },
    {
      name: 'vs Top 10',
      value: vsTop10Wins,
      fill: '#c2410c', // Bronze
    },
    {
      name: 'Bowl Wins',
      value: bowlWins,
      fill: teamColor,
    }
  ];

  return (
    <div className="rounded p-3 border border-slate-800 relative overflow-hidden">
      {coach.profile?.team_logo && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none z-0">
          <img src={coach.profile.team_logo} alt="" className="w-48 h-48 object-contain" />
        </div>
      )}
      <h4 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: teamColor }}>{coach.profile?.coach_name} - Career Achievements</h4>
      <div className="rounded p-2">
        <ResponsiveContainer width="100%" height={280}>
          <RadialBarChart 
          cx="50%" 
          cy="50%" 
          innerRadius="20%" 
          outerRadius="90%" 
          data={data} 
          startAngle={90} 
          endAngle={450}
        >
          <PolarGrid gridType="circle" stroke="#1e293b" />
          <RadialBar
            minAngle={15}
            label={{ position: 'insideStart', fill: '#fff', fontSize: 10 }}
            background={{ fill: '#1e293b' }}
            clockWise
            dataKey="value"
          />
          <Legend 
            iconSize={10} 
            layout="horizontal" 
            verticalAlign="bottom" 
            align="center"
            wrapperStyle={{ fontSize: '10px', paddingTop: '10px', color: '#cbd5e1' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#0f172a', 
              border: '1px solid #334155', 
              borderRadius: '8px',
              fontSize: '11px'
            }}
            formatter={(value, name) => [value, name]}
          />
        </RadialBarChart>
      </ResponsiveContainer>
      </div>
    </div>
  );
};

const CompactSeason2025Card = ({ season, coach }) => {
  if (!season) return null;
  const archetype = coach.coaching_archetype_analysis ? coach.coaching_archetype_analysis[Object.keys(coach.coaching_archetype_analysis)[0]] : null;
  
  const teamColor = coach.profile?.team_color || '#00d2ff';
  
  return (
    <div className="rounded p-3 space-y-3 relative overflow-hidden">
      {coach.profile?.team_logo && (
        <div className="absolute top-0 right-0 opacity-[0.04] pointer-events-none">
          <img src={coach.profile.team_logo} alt="" className="w-32 h-32 object-contain" />
        </div>
      )}
      <div className="flex justify-between items-start relative z-10">
        <div>
          <h4 className="text-sm font-bold text-white">{coach.profile?.coach_name}</h4>
          <div className="text-[9px] text-slate-500">{coach.profile?.school}</div>
        </div>
        <div className="text-right">
          <div className="text-lg font-black" style={{ color: teamColor }}>{season.record}</div>
          <div className="text-[8px] text-slate-500">RECORD</div>
        </div>
      </div>
      
      <div className="grid grid-cols-4 gap-2">
        <div className="bg-slate-800/50 rounded p-2 text-center">
          <div className="text-[8px] text-slate-500 mb-1">SP+</div>
          <div className="text-sm font-bold">{season.sp_overall?.toFixed(1)}</div>
        </div>
        <div className="bg-slate-800/50 rounded p-2 text-center">
          <div className="text-[8px] text-slate-500 mb-1">FPI</div>
          <div className="text-sm font-bold">{season.fpi?.toFixed(1)}</div>
        </div>
        <div className="bg-slate-800/50 rounded p-2 text-center">
          <div className="text-[8px] text-slate-500 mb-1">PPG</div>
          <div className="text-sm font-bold text-green-400">{season.points_per_game?.toFixed(1)}</div>
        </div>
        <div className="bg-slate-800/50 rounded p-2 text-center">
          <div className="text-[8px] text-slate-500 mb-1">PAPG</div>
          <div className="text-sm font-bold text-rose-400">{season.points_allowed_pg?.toFixed(1)}</div>
        </div>
      </div>

      {archetype && (
        <div className="border-t border-slate-800 pt-2">
          <div className="text-[9px] text-slate-500 uppercase mb-1">Style Profile</div>
          <div className="grid grid-cols-2 gap-2 text-[9px]">
            {archetype.offensive_identity && (
              <div className="text-slate-300"><span className="text-slate-500">OFF:</span> {archetype.offensive_identity.style}</div>
            )}
            {archetype.defensive_philosophy && (
              <div className="text-slate-300"><span className="text-slate-500">DEF:</span> {archetype.defensive_philosophy.style}</div>
            )}
            {archetype.game_management && (
              <div className="text-slate-300"><span className="text-slate-500">4th:</span> {archetype.game_management.fourth_down_conversion_avg}</div>
            )}
          </div>
        </div>
      )}
      
      {season.key_players_2025 && season.key_players_2025.length > 0 && (
        <div className="border-t border-slate-800 pt-2">
          <div className="text-[9px] text-slate-500 uppercase mb-1">Key Players</div>
          <div className="space-y-1">
            {season.key_players_2025.slice(0, 3).map((player, idx) => (
              <div key={idx} className="flex justify-between text-[9px]">
                <span className="text-white font-medium">{player.name}</span>
                <span className="neutralColor">{player.position}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const CompactPerformanceCard = ({ coach }) => {
  const advanced = coach.advanced_performance_metrics;
  if (!advanced) return <div className="rounded p-3 text-center text-slate-500 text-xs">No performance data</div>;

  const coachKey = Object.keys(advanced)[0];
  const metrics = advanced[coachKey];
  
  // Prepare situational win rate data
  const getSituationalWinPct = (key) => {
    if (!coach.situational_by_school || !Array.isArray(coach.situational_by_school)) return 0;
    let totalW = 0, totalL = 0;
    coach.situational_by_school.forEach(school => {
      const rec = school[key];
      if (rec && typeof rec === 'string' && rec.includes('-')) {
        const [w, l] = rec.split('-').map(Number);
        if (!isNaN(w) && !isNaN(l)) {
          totalW += w;
          totalL += l;
        }
      }
    });
    return totalW + totalL === 0 ? 0 : (totalW / (totalW + totalL)) * 100;
  };

  const situationalData = [
    { category: 'vs Ranked', winPct: getSituationalWinPct('vs_ranked') },
    { category: 'vs Top 10', winPct: getSituationalWinPct('vs_top_10') },
    { category: 'Home', winPct: getSituationalWinPct('home') },
    { category: 'Away', winPct: getSituationalWinPct('away') },
    { category: 'Close Games', winPct: getSituationalWinPct('one_score') },
  ];

  const teamColor = coach.profile?.team_color || '#00d2ff';
  
  return (
    <div className="rounded p-3 space-y-3 relative overflow-hidden">
      {coach.profile?.team_logo && (
        <div className="absolute bottom-0 right-0 opacity-[0.03] pointer-events-none">
          <img src={coach.profile.team_logo} alt="" className="w-40 h-40 object-contain" />
        </div>
      )}
      <h4 className="text-sm font-bold mb-2 relative z-10" style={{ color: teamColor }}>{coach.profile?.coach_name}</h4>

      {/* Situational Win Rate Chart */}
      <div className="rounded p-2 relative z-10">
        <h5 className="text-[9px] font-bold mb-2 uppercase" style={{ color: teamColor }}>Situational Win Rate</h5>
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={situationalData} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis type="number" domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 9 }} stroke="#334155" />
            <YAxis type="category" dataKey="category" tick={{ fill: '#64748b', fontSize: 8 }} stroke="#334155" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px', fontSize: '10px' }}
              formatter={(value) => `${value.toFixed(1)}%`}
            />
            <Bar dataKey="winPct" fill={coach.profile?.team_color || '#10b981'} radius={[0, 4, 4, 0]}>
              {situationalData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.winPct >= 50 ? (coach.profile?.team_color || '#10b981') : '#f59e0b'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {metrics?.signature_wins && metrics.signature_wins.length > 0 && (
        <div className="pt-2 border-t border-slate-800">
          <h5 className="text-[9px] font-bold text-yellow-400 mb-1 uppercase">Top Signature Wins</h5>
          <div className="space-y-1">
            {metrics.signature_wins.slice(0, 2).map((win, idx) => (
              <div key={idx} className="text-[9px] flex justify-between">
                <span className="text-white">{win.opponent}</span>
                <span className="text-slate-400">{win.year}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {metrics?.clutch_performance_metrics && (
        <div className="pt-2 border-t border-slate-800">
          <h5 className="text-[9px] font-bold text-red-400 mb-1 uppercase">Clutch Record</h5>
          <div className="text-[9px] text-slate-300">
            {metrics.clutch_performance_metrics.close_game_wins}
          </div>
        </div>
      )}
    </div>
  );
};

// Overview Tab

const OverviewTab = ({ coach1, coach2, comparative }) => {
  
  const overviewChartData = [
    { subject: 'Win %', A: (coach1.career_summary?.win_pct * 100) || 0, B: (coach2.career_summary?.win_pct * 100) || 0, fullMark: 100 },
    { subject: 'Bowl Win %', A: parseRecord(coach1.career_summary?.bowl_record), B: parseRecord(coach2.career_summary?.bowl_record), fullMark: 100 },
    { subject: 'Conf Win %', A: parseRecord(coach1.career_summary?.conference_record), B: parseRecord(coach2.career_summary?.conference_record), fullMark: 100 },
    { subject: 'Exp (Yrs)', A: Math.min((coach1.career_summary?.seasons_coached || 0) * 3, 100), B: Math.min((coach2.career_summary?.seasons_coached || 0) * 3, 100), fullMark: 100 },
    { subject: 'Recent Form', A: parseRecord(coach1.career_summary?.last_10_record), B: parseRecord(coach2.career_summary?.last_10_record), fullMark: 100 },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ComparisonMetrics coach1={coach1} coach2={coach2} comparative={comparative} />
        <div className="bg-slate-800/50 rounded-lg p-4 flex flex-col items-center justify-center">
           <h4 className="text-sm font-bold text-slate-400 mb-2 w-full text-left">Career Profile</h4>
           <ModernSpiderChart 
              data={overviewChartData} 
              color1={coach1.profile?.team_color || '#00d2ff'}
              color2={coach2.profile?.team_color || '#ff00aa'}
              label1={coach1.profile?.coach_name} 
              label2={coach2.profile?.coach_name}
           />
        </div>
      </div>
      
      {comparative?.philosophy_clash && (

        <div className="bg-slate-800/50 rounded-lg p-4">

          <h4 className="text-lg font-bold text-white mb-3 flex items-center gap-2"><Swords className="w-4 h-4" /> Philosophy Clash</h4>

          <div className="grid grid-cols-2 gap-4 text-sm">

            {Object.entries(comparative.philosophy_clash).map(([key, value]) => (

              <div key={key} className="rounded p-3">

                <div className="neutralColor font-medium mb-1 capitalize">{key.replace(/_/g, ' ')}</div>

                <div className="text-slate-300">{value}</div>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>

  );

};



// Comparison Metrics

const ComparisonMetrics = ({ coach1, coach2, comparative }) => {

  const metrics = [

    { label: 'Win %', coach1: (coach1.career_summary?.win_pct * 100).toFixed(1), coach2: (coach2.career_summary?.win_pct * 100).toFixed(1), suffix: '%' },

    { label: 'Total Games', coach1: coach1.career_summary?.total_games, coach2: coach2.career_summary?.total_games },

    { label: 'Seasons', coach1: coach1.career_summary?.seasons_coached, coach2: coach2.career_summary?.seasons_coached },

    { label: 'Last 10 Record', coach1: coach1.career_summary?.last_10_record, coach2: coach2.career_summary?.last_10_record },

  ];



  return (

    <div className="space-y-3">

      <h4 className="text-lg font-bold text-white mb-3 flex items-center gap-2"><BarChart3 className="w-4 h-4" /> Career Comparison</h4>

      {metrics.map((metric, idx) => (

        <MetricRow key={idx} {...metric} />

      ))}

    </div>

  );

};



const MetricRow = ({ label, coach1, coach2, suffix = '' }) => {

  const val1 = parseFloat(coach1) || 0;

  const val2 = parseFloat(coach2) || 0;

  const better1 = val1 > val2;

  const better2 = val2 > val1;



  return (

    <div className="bg-slate-800/50 rounded-lg p-3">

      <div className="text-slate-400 text-sm mb-2">{label}</div>

      <div className="grid grid-cols-2 gap-4">

        <div className={`text-lg font-bold ${better1 ? 'text-green-400' : 'text-slate-300'}`}>

          {coach1}{suffix}

        </div>

        <div className={`text-lg font-bold ${better2 ? 'text-green-400' : 'text-slate-300'}`}>

          {coach2}{suffix}

        </div>

      </div>

    </div>

  );

};



// Career Stats Tab

const CareerStatsTab = ({ coach1, coach2 }) => {
  
  const getSituationalWinPct = (situational, key) => {
    if (!situational || !Array.isArray(situational)) return 0;
    let totalW = 0;
    let totalL = 0;
    situational.forEach(school => {
      const rec = school[key];
      if (rec && typeof rec === 'string' && rec.includes('-')) {
        const [w, l] = rec.split('-').map(Number);
        if (!isNaN(w) && !isNaN(l)) {
          totalW += w;
          totalL += l;
        }
      }
    });
    if (totalW + totalL === 0) return 0;
    return (totalW / (totalW + totalL)) * 100;
  };

  const situationalChartData = [
    { subject: 'vs Ranked', A: getSituationalWinPct(coach1.situational_by_school, 'vs_ranked'), B: getSituationalWinPct(coach2.situational_by_school, 'vs_ranked'), fullMark: 100 },
    { subject: 'vs Top 10', A: getSituationalWinPct(coach1.situational_by_school, 'vs_top_10'), B: getSituationalWinPct(coach2.situational_by_school, 'vs_top_10'), fullMark: 100 },
    { subject: 'Home', A: getSituationalWinPct(coach1.situational_by_school, 'home'), B: getSituationalWinPct(coach2.situational_by_school, 'home'), fullMark: 100 },
    { subject: 'Away', A: getSituationalWinPct(coach1.situational_by_school, 'away'), B: getSituationalWinPct(coach2.situational_by_school, 'away'), fullMark: 100 },
    { subject: 'Close Games', A: getSituationalWinPct(coach1.situational_by_school, 'one_score'), B: getSituationalWinPct(coach2.situational_by_school, 'one_score'), fullMark: 100 },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StintsSection stints={coach1.stints} coachName={coach1.profile?.coach_name} />
        <StintsSection stints={coach2.stints} coachName={coach2.profile?.coach_name} />
      </div>
      
      <div className="bg-slate-800/50 rounded-lg p-4">
         <h4 className="text-lg font-bold text-white mb-3">Situational Win % Comparison</h4>
         <ModernSpiderChart 
            data={situationalChartData} 
            color1={coach1.profile?.team_color || '#00d2ff'}
            color2={coach2.profile?.team_color || '#ff00aa'}
            label1={coach1.profile?.coach_name} 
            label2={coach2.profile?.coach_name}
         />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SituationalStatsSection situational={coach1.situational_by_school} coachName={coach1.profile?.coach_name} />
        <SituationalStatsSection situational={coach2.situational_by_school} coachName={coach2.profile?.coach_name} />
      </div>
    </div>
  );
};



const StintsSection = ({ stints, coachName }) => {

  if (!stints) return null;



  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">{coachName} - Career Stops</h4>

      <div className="space-y-2">

        {stints.map((stint, idx) => (

          <div key={idx} className="rounded p-3 text-sm">

            <div className="flex justify-between items-start mb-1">

              <span className="font-bold">{stint.school}</span>

              <span className="text-slate-400">{stint.start_year}-{stint.end_year}</span>

            </div>

            <div className="text-slate-300">

              {stint.record} <span className="text-green-400">({(stint.win_pct * 100).toFixed(1)}%)</span>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

};



const SituationalStatsSection = ({ situational, coachName }) => {

  if (!situational) return null;



  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">Situational Performance</h4>

      <div className="space-y-2 text-sm">

        {situational.map((school, idx) => (

          <div key={idx} className="rounded p-3">

            <div className="font-bold mb-2">{school.school}</div>

            <div className="grid grid-cols-2 gap-2 text-xs">

              <div><span className="text-slate-400">vs Ranked:</span> <span className="text-slate-300">{school.vs_ranked}</span></div>

              <div><span className="text-slate-400">vs Top 10:</span> <span className="text-slate-300">{school.vs_top_10}</span></div>

              <div><span className="text-slate-400">Home:</span> <span className="text-slate-300">{school.home}</span></div>

              <div><span className="text-slate-400">Away:</span> <span className="text-slate-300">{school.away}</span></div>

              <div><span className="text-slate-400">Close Games:</span> <span className="text-slate-300">{school.one_score}</span></div>

              <div><span className="text-slate-400">Blowouts:</span> <span className="text-slate-300">{school.blowouts}</span></div>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

};



// Season 2025 Tab

const Season2025Tab = ({ coach1, coach2 }) => {
  
  const seasonChartData = [
    { subject: 'Win %', A: parseRecord(coach1.season_2025_detail?.record), B: parseRecord(coach2.season_2025_detail?.record), fullMark: 100 },
    { subject: 'SP+ Overall', A: (coach1.season_2025_detail?.sp_overall || 0) + 20, B: (coach2.season_2025_detail?.sp_overall || 0) + 20, fullMark: 100 },
    { subject: 'SP+ Off', A: (coach1.season_2025_detail?.sp_offense || 0), B: (coach2.season_2025_detail?.sp_offense || 0), fullMark: 50 },
    { subject: 'SP+ Def', A: 40 - (coach1.season_2025_detail?.sp_defense || 0), B: 40 - (coach2.season_2025_detail?.sp_defense || 0), fullMark: 50 }, // Invert defense (lower is better)
    { subject: 'FPI', A: (coach1.season_2025_detail?.fpi || 0) + 20, B: (coach2.season_2025_detail?.fpi || 0) + 20, fullMark: 100 },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-lg p-4">
         <h4 className="text-lg font-bold text-white mb-3">2025 Season Metrics</h4>
         <ModernSpiderChart 
            data={seasonChartData} 
            color1={coach1.profile?.team_color || '#00d2ff'}
            color2={coach2.profile?.team_color || '#ff00aa'}
            label1={coach1.profile?.coach_name} 
            label2={coach2.profile?.coach_name}
         />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Season2025Card season={coach1.season_2025_detail} coachName={coach1.profile?.coach_name} />
        <Season2025Card season={coach2.season_2025_detail} coachName={coach2.profile?.coach_name} />
      </div>
    </div>
  );
};



const Season2025Card = ({ season, coachName }) => {

  if (!season) return null;



  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">{coachName} - 2025 Season</h4>

      

      <div className="grid grid-cols-2 gap-3 mb-4 text-sm">

        <div className="rounded p-3">

          <div className="text-slate-400 text-xs mb-1">Record</div>

          <div className="text-xl font-bold text-green-400">{season.record}</div>

        </div>

        <div className="rounded p-3">

          <div className="text-slate-400 text-xs mb-1">PPG / PAPG</div>

          <div className="text-lg font-bold text-white">{season.points_per_game?.toFixed(1)} / {season.points_allowed_pg?.toFixed(1)}</div>

        </div>

        <div className="rounded p-3">

          <div className="text-slate-400 text-xs mb-1">SP+ Overall</div>

          <div className="text-lg font-bold">{season.sp_overall?.toFixed(1)}</div>

        </div>

        <div className="rounded p-3">

          <div className="text-slate-400 text-xs mb-1">FPI</div>

          <div className="text-lg font-bold">{season.fpi?.toFixed(1)}</div>

        </div>

      </div>



      {season.key_players_2025 && (

        <div className="mt-4">

          <h5 className="text-sm font-bold text-slate-300 mb-2">Key Players</h5>

          <div className="space-y-2">

            {season.key_players_2025.map((player, idx) => (

              <div key={idx} className="rounded p-2 text-xs">

                <div className="flex justify-between">

                  <span className="font-bold text-white">{player.name}</span>

                  <span className="neutralColor">{player.position}</span>

                </div>

                <div className="text-slate-400 mt-1">

                  {player.passing_yards && `${player.passing_yards} pass yds`}

                  {player.rushing_yards && `${player.rushing_yards} rush yds`}

                  {player.receiving_yards && `${player.receiving_yards} rec yds`}

                </div>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>

  );

};



// Archetype Tab

const ArchetypeTab = ({ coach1, coach2 }) => {
  const getArchetype = (coach) => {
    const school = coach.profile?.school;
    if (!coach.coaching_archetype_analysis) return null;
    const keys = Object.keys(coach.coaching_archetype_analysis);
    if (keys.length > 0) return coach.coaching_archetype_analysis[keys[0]];
    return null;
  };

  const arch1 = getArchetype(coach1);
  const arch2 = getArchetype(coach2);
  
  const getValuation = (arch) => arch?.nil_strategy?.total_valuation || 0;
  const getAvgNil = (arch) => arch?.nil_strategy?.avg_per_player || 0;
  
  const maxVal = Math.max(getValuation(arch1), getValuation(arch2), 1000000);
  const maxAvg = Math.max(getAvgNil(arch1), getAvgNil(arch2), 10000);

  const archChartData = [
    { subject: 'NIL Total', A: (getValuation(arch1) / maxVal) * 100, B: (getValuation(arch2) / maxVal) * 100, fullMark: 100 },
    { subject: 'NIL Avg', A: (getAvgNil(arch1) / maxAvg) * 100, B: (getAvgNil(arch2) / maxAvg) * 100, fullMark: 100 },
    { subject: 'Aggression', A: arch1?.game_management?.aggression_level === 'High' ? 90 : (arch1?.game_management?.aggression_level === 'Medium' ? 50 : 20), B: arch2?.game_management?.aggression_level === 'High' ? 90 : (arch2?.game_management?.aggression_level === 'Medium' ? 50 : 20), fullMark: 100 },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-lg p-4">
         <h4 className="text-lg font-bold text-white mb-3">Archetype & NIL Profile</h4>
         <ModernSpiderChart 
            data={archChartData} 
            color1={coach1.profile?.team_color || '#00d2ff'}
            color2={coach2.profile?.team_color || '#ff00aa'}
            label1={coach1.profile?.coach_name} 
            label2={coach2.profile?.coach_name}
         />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ArchetypeCard archetype={arch1} coachName={coach1.profile?.coach_name} />
        <ArchetypeCard archetype={arch2} coachName={coach2.profile?.coach_name} />
      </div>
    </div>
  );
};



const ArchetypeCard = ({ archetype, coachName }) => {

  if (!archetype) return <div className="bg-slate-800/50 rounded-lg p-4 text-slate-400">No archetype data available</div>;



  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">{coachName}</h4>

      

      {archetype.archetype_summary && (

        <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-lg p-4 mb-4 border border-purple-500/20">

          <div className="text-sm text-slate-300 leading-relaxed">{archetype.archetype_summary}</div>

        </div>

      )}



      <div className="space-y-4 text-sm">

        {archetype.offensive_identity && (

          <div>

            <h5 className="font-bold mb-2 flex items-center gap-2"><Target className="w-4 h-4" /> Offensive Identity</h5>

            <div className="rounded p-3 text-slate-300">

              <div className="mb-2"><span className="text-slate-400">Style:</span> {archetype.offensive_identity.style}</div>

              <div className="text-slate-400 text-xs">{archetype.offensive_identity.philosophy}</div>

            </div>

          </div>

        )}



        {archetype.defensive_philosophy && (

          <div>

            <h5 className="font-bold mb-2 flex items-center gap-2"><Shield className="w-4 h-4" /> Defensive Philosophy</h5>

            <div className="rounded p-3 text-slate-300">

              <div className="mb-2"><span className="text-slate-400">Style:</span> {archetype.defensive_philosophy.style}</div>

            </div>

          </div>

        )}



        {archetype.game_management && (

          <div>

            <h5 className="font-bold text-green-400 mb-2 flex items-center gap-2"><Clipboard className="w-4 h-4" /> Game Management</h5>

            <div className="rounded p-3 text-slate-300">

              <div><span className="text-slate-400">Aggression:</span> {archetype.game_management.aggression_level}</div>

              <div><span className="text-slate-400">4th Down:</span> {archetype.game_management.fourth_down_conversion_avg}</div>

            </div>

          </div>

        )}



        {archetype.nil_strategy && (

          <div>

            <h5 className="font-bold text-yellow-400 mb-2 flex items-center gap-2"><DollarSign className="w-4 h-4" /> NIL Strategy</h5>

            <div className="rounded p-3 text-xs">

              <div className="text-slate-300 mb-1">Total: ${(archetype.nil_strategy.total_valuation / 1000000).toFixed(1)}M</div>

              <div className="text-slate-400">Players: {archetype.nil_strategy.players} • Avg: ${(archetype.nil_strategy.avg_per_player / 1000).toFixed(0)}K</div>

            </div>

          </div>

        )}

      </div>

    </div>

  );

};



// Recruiting Tab

const RecruitingTab = ({ coach1, coach2 }) => {
  // Get team colors
  const team1Color = coach1.profile?.team_color || '#00d2ff';
  const team2Color = coach2.profile?.team_color || '#ff00aa';
  
  // Prepare data for charts
  const prepareRecruitingRankingsData = () => {
    const allYears = new Set();
    coach1.recruiting_classes?.forEach(c => allYears.add(c.year));
    coach2.recruiting_classes?.forEach(c => allYears.add(c.year));
    
    return Array.from(allYears).sort().map(year => {
      const c1 = coach1.recruiting_classes?.find(c => c.year === year);
      const c2 = coach2.recruiting_classes?.find(c => c.year === year);
      return {
        year,
        coach1Rank: c1?.class_rank || null,
        coach2Rank: c2?.class_rank || null
      };
    });
  };

  const prepareTalentData = () => {
    const allYears = new Set();
    coach1.talent_composite?.forEach(t => allYears.add(t.year));
    coach2.talent_composite?.forEach(t => allYears.add(t.year));
    
    return Array.from(allYears).sort().map(year => {
      const t1 = coach1.talent_composite?.find(t => t.year === year);
      const t2 = coach2.talent_composite?.find(t => t.year === year);
      return {
        year,
        coach1Talent: t1?.talent_rating || null,
        coach2Talent: t2?.talent_rating || null
      };
    });
  };

  const preparePortalVolumeData = () => {
    const allYears = new Set();
    coach1.transfer_portal?.forEach(p => allYears.add(p.season));
    coach2.transfer_portal?.forEach(p => allYears.add(p.season));
    
    return Array.from(allYears).sort().map(year => {
      const p1 = coach1.transfer_portal?.find(p => p.season === year);
      const p2 = coach2.transfer_portal?.find(p => p.season === year);
      return {
        year,
        coach1In: p1?.in || 0,
        coach1Out: p1?.out || 0,
        coach2In: p2?.in || 0,
        coach2Out: p2?.out || 0
      };
    });
  };

  const prepareNetPortalData = () => {
    const allYears = new Set();
    coach1.transfer_portal?.forEach(p => allYears.add(p.season));
    coach2.transfer_portal?.forEach(p => allYears.add(p.season));
    
    return Array.from(allYears).sort().map(year => {
      const p1 = coach1.transfer_portal?.find(p => p.season === year);
      const p2 = coach2.transfer_portal?.find(p => p.season === year);
      return {
        year,
        coach1Net: p1?.net || 0,
        coach2Net: p2?.net || 0
      };
    });
  };

  const rankingsData = prepareRecruitingRankingsData();
  const talentData = prepareTalentData();
  const portalVolumeData = preparePortalVolumeData();
  const netPortalData = prepareNetPortalData();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Chart 1: Recruiting Rankings */}
      <div className="rounded-lg p-4 border border-slate-800 relative overflow-hidden">
        {coach1?.profile?.team_logo && (
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none">
            <img src={coach1.profile.team_logo} alt="" className="w-48 h-48 object-contain" />
          </div>
        )}
        <h4 className="text-sm font-bold mb-2 relative z-10" style={{ color: team1Color }}>Recruiting Class Rankings</h4>
        <p className="text-xs text-slate-500 mb-3 relative z-10">Rank # (Lower is better)</p>
        <div className="rounded p-2 relative z-10">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={rankingsData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <YAxis reversed tick={{ fill: '#64748b', fontSize: 10 }} domain={[0, 'auto']} stroke="#334155" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#cbd5e1' }}
              />
            <Legend wrapperStyle={{ fontSize: '10px' }} />
            <Line 
              type="monotone" 
              dataKey="coach1Rank" 
              stroke={team1Color}
              strokeWidth={3}
              name={coach1.profile?.coach_name}
              dot={{ fill: team1Color, r: 5 }}
              connectNulls
            />
            <Line 
              type="monotone" 
              dataKey="coach2Rank" 
              stroke={team2Color}
              strokeWidth={3}
              strokeDasharray="5 5"
              name={coach2.profile?.coach_name}
              dot={{ fill: team2Color, r: 5 }}
              connectNulls
            />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Chart 2: Talent Composite */}
      <div className="rounded-lg p-4 border border-slate-800 relative overflow-hidden">
        {coach2?.profile?.team_logo && (
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] pointer-events-none">
            <img src={coach2.profile.team_logo} alt="" className="w-48 h-48 object-contain" />
          </div>
        )}
        <h4 className="text-sm font-bold mb-2 relative z-10" style={{ color: team2Color }}>Talent Composite Score</h4>
        <p className="text-xs text-slate-500 mb-3 relative z-10">Total Roster Talent Rating</p>
        <div className="rounded p-2 relative z-10">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={talentData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <YAxis tick={{ fill: '#64748b', fontSize: 10 }} domain={[500, 'auto']} stroke="#334155" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#cbd5e1' }}
              />
            <Legend wrapperStyle={{ fontSize: '10px' }} />
            <Bar dataKey="coach1Talent" fill={team1Color} name={coach1.profile?.coach_name} />
            <Bar dataKey="coach2Talent" fill={team2Color} name={coach2.profile?.coach_name} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Chart 3: Portal Volume */}
      <div className="rounded-lg p-4 lg:col-span-2 border border-slate-800 relative overflow-hidden">
        {coach1?.profile?.team_logo && coach2?.profile?.team_logo && (
          <>
            <div className="absolute top-1/2 left-1/4 -translate-x-1/2 -translate-y-1/2 opacity-[0.02] pointer-events-none">
              <img src={coach1.profile.team_logo} alt="" className="w-40 h-40 object-contain" />
            </div>
            <div className="absolute top-1/2 right-1/4 translate-x-1/2 -translate-y-1/2 opacity-[0.02] pointer-events-none">
              <img src={coach2.profile.team_logo} alt="" className="w-40 h-40 object-contain" />
            </div>
          </>
        )}
        <h4 className="text-sm font-bold mb-2 relative z-10" style={{ color: team1Color }}>Transfer Portal Volume</h4>
        <p className="text-xs text-slate-500 mb-3 relative z-10">Comparison of Incoming vs. Outgoing Transfers</p>
        <div className="rounded p-2 relative z-10">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={portalVolumeData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <YAxis tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#cbd5e1' }}
              />
            <Legend wrapperStyle={{ fontSize: '10px' }} />
            <Bar dataKey="coach1In" fill={team1Color} name={`${coach1.profile?.coach_name} (IN)`} />
            <Bar dataKey="coach1Out" fill={`${team1Color}80`} name={`${coach1.profile?.coach_name} (OUT)`} />
            <Bar dataKey="coach2In" fill={team2Color} name={`${coach2.profile?.coach_name} (IN)`} />
            <Bar dataKey="coach2Out" fill={`${team2Color}80`} name={`${coach2.profile?.coach_name} (OUT)`} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Chart 4: Net Portal Balance */}
      <div className="rounded-lg p-4 lg:col-span-2 border border-slate-800 relative overflow-hidden">
        {coach1?.profile?.team_logo && coach2?.profile?.team_logo && (
          <div className="absolute inset-0 flex justify-between items-center opacity-[0.02] pointer-events-none">
            <img src={coach1.profile.team_logo} alt="" className="w-32 h-32 object-contain ml-8" />
            <img src={coach2.profile.team_logo} alt="" className="w-32 h-32 object-contain mr-8" />
          </div>
        )}
        <h4 className="text-sm font-bold mb-2 relative z-10" style={{ color: team1Color }}>Net Transfer Portal Balance</h4>
        <p className="text-xs text-slate-500 mb-3">Net gain/loss of scholarship players via portal</p>
        <div className="rounded p-2">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={netPortalData} layout="vertical" margin={{ top: 5, right: 20, left: 30, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <YAxis type="category" dataKey="year" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#cbd5e1' }}
              />
            <Legend wrapperStyle={{ fontSize: '10px' }} />
            <ReferenceLine x={0} stroke="#64748b" strokeWidth={2} />
            <Bar dataKey="coach1Net" name={coach1.profile?.coach_name}>
              {netPortalData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.coach1Net >= 0 ? '#10b981' : '#ef4444'} />
              ))}
            </Bar>
            <Bar dataKey="coach2Net" name={coach2.profile?.coach_name}>
              {netPortalData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.coach2Net >= 0 ? '#10b981' : '#ef4444'} />
              ))}
            </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};



const RecruitingCard = ({ coach }) => {

  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">{coach.profile?.coach_name}</h4>

      

      {coach.recruiting_classes && (

        <div className="mb-4">

          <h5 className="text-sm font-bold mb-2 flex items-center gap-2"><Star className="w-4 h-4" /> Recruiting Classes</h5>

          <div className="space-y-1 text-xs">

            {coach.recruiting_classes.slice(0, 5).map((cls, idx) => (

              <div key={idx} className="flex justify-between rounded p-2">

                <span className="text-slate-400">{cls.year}</span>

                <span className="font-bold text-white">#{cls.class_rank}</span>

              </div>

            ))}

          </div>

        </div>

      )}



      {coach.talent_composite && (

        <div className="mb-4">

          <h5 className="text-sm font-bold mb-2 flex items-center gap-2"><Gem className="w-4 h-4" /> Talent Composite</h5>

          <div className="space-y-1 text-xs">

            {coach.talent_composite.slice(0, 5).map((talent, idx) => (

              <div key={idx} className="flex justify-between rounded p-2">

                <span className="text-slate-400">{talent.year}</span>

                <span className="font-bold text-white">{talent.talent_rating?.toFixed(1)}</span>

              </div>

            ))}

          </div>

        </div>

      )}



      {coach.transfer_portal && coach.transfer_portal.length > 0 && (

        <div>

          <h5 className="text-sm font-bold text-green-400 mb-2 flex items-center gap-2"><RefreshCw className="w-4 h-4" /> Transfer Portal</h5>

          <div className="space-y-1 text-xs">

            {coach.transfer_portal.slice(0, 3).map((portal, idx) => (

              <div key={idx} className="rounded p-2">

                <div className="flex justify-between mb-1">

                  <span className="text-slate-400">{portal.season}</span>

                  <span className={`font-bold ${portal.net >= 0 ? 'text-green-400' : 'text-red-400'}`}>

                    {portal.net >= 0 ? '+' : ''}{portal.net}

                  </span>

                </div>

                <div className="text-slate-500">In: {portal.in} • Out: {portal.out}</div>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>

  );

};



// Performance Tab

const PerformanceTab = ({ coach1, coach2 }) => {
  
  const getPerformanceMetric = (coach, type) => {
    const advanced = coach.advanced_performance_metrics;
    if (!advanced) return 0;
    const coachKey = Object.keys(advanced)[0];
    const metrics = advanced[coachKey];
    if (!metrics) return 0;

    if (type === 'sig_wins') return (metrics.signature_wins?.length || 0);
    if (type === 'clutch_wins') {
        const val = metrics.clutch_performance_metrics?.close_game_wins;
        if (typeof val === 'string' && val.includes('-')) {
             return parseInt(val.split('-')[0]);
        }
        return parseInt(val) || 0;
    }
    if (type === 'clutch_pct') {
         const wins = metrics.clutch_performance_metrics?.close_game_wins;
         const total = metrics.clutch_performance_metrics?.close_games;
         
         let w = 0;
         if (typeof wins === 'string' && wins.includes('-')) {
             const parts = wins.split('-').map(Number);
             w = parts[0];
         } else {
             w = parseInt(wins) || 0;
         }
         
         const t = parseInt(total) || 1;
         if (t === 0) return 0;
         return (w / t) * 100;
    }
    return 0;
  };

  const perfChartData = [
    { subject: 'Sig Wins', A: Math.min(getPerformanceMetric(coach1, 'sig_wins') * 20, 100), B: Math.min(getPerformanceMetric(coach2, 'sig_wins') * 20, 100), fullMark: 100 },
    { subject: 'Clutch Wins', A: Math.min(getPerformanceMetric(coach1, 'clutch_wins') * 15, 100), B: Math.min(getPerformanceMetric(coach2, 'clutch_wins') * 15, 100), fullMark: 100 },
    { subject: 'Clutch %', A: getPerformanceMetric(coach1, 'clutch_pct'), B: getPerformanceMetric(coach2, 'clutch_pct'), fullMark: 100 },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-lg p-4">
         <h4 className="text-lg font-bold text-white mb-3">Advanced Performance Profile</h4>
         <ModernSpiderChart 
            data={perfChartData} 
            color1={coach1.profile?.team_color || '#00d2ff'}
            color2={coach2.profile?.team_color || '#ff00aa'}
            label1={coach1.profile?.coach_name} 
            label2={coach2.profile?.coach_name}
         />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PerformanceCard coach={coach1} />
        <PerformanceCard coach={coach2} />
      </div>
    </div>
  );
};



const PerformanceCard = ({ coach }) => {

  const advanced = coach.advanced_performance_metrics;

  if (!advanced) return <div className="bg-slate-800/50 rounded-lg p-4 text-slate-400">No performance data available</div>;



  const coachKey = Object.keys(advanced)[0];

  const metrics = advanced[coachKey];



  return (

    <div className="bg-slate-800/50 rounded-lg p-4">

      <h4 className="text-lg font-bold text-white mb-3">{coach.profile?.coach_name}</h4>

      

      {metrics?.signature_wins && (

        <div className="mb-4">

          <h5 className="text-sm font-bold text-yellow-400 mb-2 flex items-center gap-2"><Trophy className="w-4 h-4" /> Signature Wins</h5>

          <div className="space-y-2">

            {metrics.signature_wins.slice(0, 3).map((win, idx) => (

              <div key={idx} className="bg-gradient-to-r from-yellow-900/20 to-orange-900/20 rounded p-3 text-xs border border-yellow-500/20">

                <div className="flex justify-between mb-1">

                  <span className="font-bold text-white">{win.opponent}</span>

                  <span className="text-slate-400">{win.year}</span>

                </div>

                <div className="text-green-400">{win.score}</div>

                <div className="text-slate-400 mt-1 text-xs">{win.context}</div>

              </div>

            ))}

          </div>

        </div>

      )}



      {metrics?.clutch_performance_metrics && (

        <div className="rounded p-3">

          <h5 className="text-sm font-bold text-red-400 mb-2 flex items-center gap-2"><Flame className="w-4 h-4" /> Clutch Performance</h5>

          <div className="text-xs space-y-1">

            <div className="text-slate-300">

              <span className="text-slate-400">Close Games:</span> {metrics.clutch_performance_metrics.close_game_wins}

            </div>

            <div className="text-slate-300">

              <span className="text-slate-400">Record:</span> {metrics.clutch_performance_metrics.close_games} games

            </div>

          </div>

        </div>

      )}

    </div>

  );

};



// Matchup Prediction Tab

const MatchupPredictionTab = ({ matchup, coach1, coach2 }) => {

  if (!matchup) return <div className="text-slate-400">No matchup prediction available</div>;



  return (

    <div className="space-y-6">

      {matchup.head_to_head_never_met && (

        <div className="relative overflow-hidden backdrop-blur-xl border border-blue-500/30 rounded-lg p-4 text-center">

          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-cyan-500/5 pointer-events-none"></div>

          <div className="relative z-10 font-medium flex items-center justify-center gap-2"><Info className="w-4 h-4" /> {matchup.head_to_head_never_met}</div>

        </div>

      )}



      {matchup.prediction_framework && (

        <>

          {/* Advantages */}

          <div className="grid grid-cols-2 gap-6">

            <div className="relative overflow-hidden backdrop-blur-xl rounded-lg p-4 border border-green-500/30">

              <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-500/5 pointer-events-none"></div>

              <h4 className="relative z-10 text-lg font-bold text-green-400 mb-3">{coach1.profile?.school} Advantages</h4>

              <ul className="relative z-10 space-y-2 text-sm">

                {matchup.prediction_framework.ole_miss_advantages?.map((adv, idx) => (

                  <li key={idx} className="flex items-start">

                    <span className="text-green-400 mr-2">✓</span>

                    <span className="text-slate-300">{adv}</span>

                  </li>

                ))}

              </ul>

            </div>

            

            <div className="relative overflow-hidden backdrop-blur-xl rounded-lg p-4 border border-blue-500/30">

              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-cyan-500/5 pointer-events-none"></div>

              <h4 className="relative z-10 text-lg font-bold mb-3">{coach2.profile?.school} Advantages</h4>

              <ul className="relative z-10 space-y-2 text-sm">

                {matchup.prediction_framework.illinois_advantages?.map((adv, idx) => (

                  <li key={idx} className="flex items-start">

                    <span className="neutralColor mr-2">✓</span>

                    <span className="text-slate-300">{adv}</span>

                  </li>

                ))}

              </ul>

            </div>

          </div>



          {/* Game Scenarios */}

          {matchup.prediction_framework.game_script_scenarios && (

            <div className="relative overflow-hidden backdrop-blur-xl rounded-lg p-4 border border-purple-500/30">

              <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 pointer-events-none"></div>

              <h4 className="relative z-10 text-lg font-bold text-white mb-4 flex items-center gap-2"><Film className="w-4 h-4" /> Game Scenarios</h4>

              

              {/* Scenario Probability Chart */}

              <div className="relative z-10 mb-4 rounded p-2">

                <ResponsiveContainer width="100%" height={180}>

                  <BarChart data={matchup.prediction_framework.game_script_scenarios.map(s => ({

                    scenario: s.scenario,

                    probability: parseFloat(s.probability.replace(/[^0-9.-]/g, '')) || 0

                  }))} layout="vertical" margin={{ top: 5, right: 20, left: 100, bottom: 5 }}>

                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

                    <XAxis type="number" domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" label={{ value: 'Probability %', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} />

                    <YAxis type="category" dataKey="scenario" tick={{ fill: '#64748b', fontSize: 10 }} stroke="#334155" />

                    <Tooltip 

                      contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}

                      formatter={(value) => `${value}%`}

                    />

                    <Bar dataKey="probability" radius={[0, 8, 8, 0]}>

                      {matchup.prediction_framework.game_script_scenarios.map((entry, index) => (

                        <Cell key={`cell-${index}`} fill={index === 0 ? '#10b981' : (index === 1 ? '#f59e0b' : '#8b5cf6')} />

                      ))}

                    </Bar>

                  </BarChart>

                </ResponsiveContainer>

              </div>



              <div className="relative z-10 space-y-3">

                {matchup.prediction_framework.game_script_scenarios.map((scenario, idx) => (

                  <div key={idx} className="relative overflow-hidden backdrop-blur-xl rounded-lg p-4 border border-slate-700/30">

                    <div className="flex justify-between items-start mb-2">

                      <span className="font-bold">{scenario.scenario}</span>

                      <span className="text-sm border border-purple-500/30 px-3 py-1 rounded-full text-purple-300">

                        {scenario.probability}

                      </span>

                    </div>

                    <p className="text-slate-300 text-sm mb-2">{scenario.description}</p>

                    <div className="text-green-400 font-mono text-sm">{scenario.score_prediction}</div>

                  </div>

                ))}

              </div>

            </div>

          )}



          {/* Final Prediction */}

          {matchup.prediction_framework.final_prediction && (

            <div className="relative overflow-hidden backdrop-blur-xl rounded-lg p-6 border border-purple-500/30">

              <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 pointer-events-none"></div>

              <h4 className="relative z-10 text-xl font-bold text-white mb-4 flex items-center gap-2">

                <Trophy className="w-5 h-5" />

                Final Prediction

              </h4>

              <div className="relative z-10 space-y-3">

                <div className="text-2xl font-bold text-green-400">

                  {matchup.prediction_framework.final_prediction.winner}

                </div>

                <div className="text-slate-300">

                  <span className="text-slate-400">Confidence:</span> {matchup.prediction_framework.final_prediction.confidence}

                </div>

                <p className="text-slate-300 text-sm leading-relaxed">

                  {matchup.prediction_framework.final_prediction.reasoning}

                </p>

                {matchup.prediction_framework.final_prediction.upset_path_for_illinois && (

                  <div className="mt-4 pt-4 border-t border-slate-700/50">

                    <h5 className="text-sm font-bold text-yellow-400 mb-2 flex items-center gap-2"><Target className="w-4 h-4" /> Upset Path</h5>

                    <p className="text-slate-300 text-xs leading-relaxed">

                      {matchup.prediction_framework.final_prediction.upset_path_for_illinois}

                    </p>

                  </div>

                )}

              </div>

            </div>

          )}

        </>

      )}

    </div>

  );

};



export default CoachesComparison;
