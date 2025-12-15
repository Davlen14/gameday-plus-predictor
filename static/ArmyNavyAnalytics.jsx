import React, { useState, useEffect, useRef } from 'react';
import { 
  Trophy, 
  Target, 
  TrendingUp, 
  Activity, 
  Shield, 
  AlertTriangle, 
  Zap,
  BarChart3,
  ChevronRight,
  Cpu,
  Calendar,
  Clock,
  History,
  Swords,
  Scale,
  Flame,
  Minus,
  Hexagon,
  Radar,
  DollarSign,
  Settings,
  Code,
  FileText,
  TrendingDown,
  RefreshCw,
  MessageSquare,
  X,
  Send,
  Sparkles
} from 'lucide-react';

const apiKey = ""; // API Key injected by environment

const ArmyNavyAnalytics = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [mounted, setMounted] = useState(false);
  
  // AI STATE
  const [showAI, setShowAI] = useState(false);
  const [aiInput, setAiInput] = useState('');
  const [aiHistory, setAiHistory] = useState([
    { role: 'system', text: 'TACTICAL ORACLE ONLINE. NEURAL LINK ESTABLISHED. AWAITING QUERY.' }
  ]);
  const [aiLoading, setAiLoading] = useState(false);
  const chatEndRef = useRef(null);

  // LIVE MARKET STATE
  const [marketData, setMarketData] = useState({
    navyPrice: 0.685, // Defaulting to the provided snapshot
    armyPrice: 0.315, // Defaulting to the provided snapshot
    volume: "2,288",
    loading: true,
    error: null,
    isLive: false
  });

  // OFFICIAL TEAM COLORS
  const COLORS = {
    NAVY: {
      BLUE: '#00205B', // PMS 281 C
      GOLD: '#C5B783', // PMS 4525 C
      ACCENT: '#00B4D8' // Cyan for HUD glow
    },
    ARMY: {
      GOLD: '#D4BF91', // PMS 467 C
      GRAY: '#B2B4B3', // PMS COOL GRAY 5 C
      BLACK: '#1A1A1A',
      ACCENT: '#FFD700' // Bright gold for HUD glow
    }
  };

  useEffect(() => {
    setMounted(true);
    fetchLiveMarketData();
  }, []);

  useEffect(() => {
    if (showAI && chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [aiHistory, showAI]);

  const fetchLiveMarketData = async () => {
    setMarketData(prev => ({ ...prev, loading: true }));
    try {
      const response = await fetch("https://gamma-api.polymarket.com/markets/slug/cfb-army-navy-2025-12-13");
      if (!response.ok) throw new Error("Network response was not ok");
      
      const data = await response.json();
      
      const prices = JSON.parse(data.outcomePrices);
      const outcomes = JSON.parse(data.outcomes);
      
      const armyIndex = outcomes.findIndex(o => o === "Army");
      const navyIndex = outcomes.findIndex(o => o === "Navy");

      const armyPriceVal = parseFloat(prices[armyIndex]);
      const navyPriceVal = parseFloat(prices[navyIndex]);

      setMarketData({
        navyPrice: navyPriceVal,
        armyPrice: armyPriceVal,
        volume: parseFloat(data.volume).toLocaleString(undefined, {maximumFractionDigits: 0}),
        loading: false,
        error: null,
        isLive: true
      });

    } catch (err) {
      console.warn("Live fetch blocked (CORS) - Using Snapshot Data");
      // Fallback to the specific data provided by user
      setMarketData({
        navyPrice: 0.685,
        armyPrice: 0.315,
        volume: "2,288",
        loading: false,
        error: "Live stream restricted - Using latest snapshot",
        isLive: false 
      });
    }
  };

  const handleAISubmit = async (e) => {
    e?.preventDefault();
    if (!aiInput.trim()) return;
    
    const userText = aiInput;
    setAiInput('');
    setAiHistory(prev => [...prev, { role: 'user', text: userText }]);
    setAiLoading(true);

    const systemPrompt = `
      You are RivalryOS, a highly advanced tactical AI for the Army vs Navy football game in the year 2090.
      
      CURRENT TELEMETRY:
      - Predicted Winner: Navy Midshipmen (Probability: ${data.winProb.navy}%)
      - Predicted Score: Navy 21, Army 18
      - Key Navy Advantage: Offensive Efficiency (+10.2%) and TD Production (+59% freq).
      - Key Army Strength: Elite Red Zone Efficiency (100% conversion) and Ball Control.
      - Market Sentiment: Navy trading at ${(marketData.navyPrice * 100).toFixed(1)} cents.
      - Historical Context: Navy leads series +7 wins.
      
      INSTRUCTIONS:
      - Answer the user's query based on this data.
      - Adopt a futuristic, military-analytical persona (e.g., "Affirmative," "Telemetry indicates," "Tactical Assessment").
      - Keep responses concise (under 60 words).
      - Use markdown for emphasis if needed.
    `;

    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ parts: [{ text: userText }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] }
          }),
        }
      );

      if (!response.ok) throw new Error("Neural Link Severed");
      
      const resData = await response.json();
      const aiText = resData.candidates?.[0]?.content?.parts?.[0]?.text || "DATA CORRUPTION DETECTED. RETRY.";
      
      setAiHistory(prev => [...prev, { role: 'ai', text: aiText }]);
    } catch (error) {
      setAiHistory(prev => [...prev, { role: 'ai', text: "ERROR: UPLINK FAILED. OFFLINE MODE ACTIVE." }]);
    } finally {
      setAiLoading(false);
    }
  };

  const data = {
    gameDate: "12.14.2090", // Stylized for futuristic feel
    winner: "NAVY MIDSHIPMEN",
    predictedScore: { navy: 21, army: 18 },
    // Use live data if available, otherwise fallback
    winProb: { 
      navy: (marketData.navyPrice * 100).toFixed(1), 
      army: (marketData.armyPrice * 100).toFixed(1) 
    },
    factors: [
      { label: "Offensive Eff.", navy: 49.1, army: 38.9, diff: "+10.2%", favor: "navy" },
      { label: "TD Production", navy: 41.2, army: 25.9, diff: "+59%", favor: "navy" },
      { label: "Yards / Drive", navy: 41.1, army: 34.3, diff: "+19.8%", favor: "navy" },
      { label: "Series History", navy: "62 W", army: "55 W", diff: "+7 Wins", favor: "navy" }
    ],
    stats: {
      army: { drives: 108, scoreRate: 38.9, tdRate: 25.9, ypd: 34.3, compScore: 131.06 },
      navy: { drives: 114, scoreRate: 49.1, tdRate: 41.2, ypd: 41.1, compScore: 194.21 }
    },
    scenarios: {
      avgScore: { army: 14.2, navy: 15.9 },
      closeGames: { total: 48, armyWins: 21, navyWins: 23, ties: 4, insight: "Dead Heat (< 7 pts)" },
      blowouts: { total: 45, armyWins: 17, navyWins: 28, insight: "Navy Dominates (> 14 pts)" },
    },
    history: {
      team1Wins: 55,
      team2Wins: 62,
      ties: 7,
      recent: [
        { year: 2024, winner: "NAVY", score: "31-13" },
        { year: 2023, winner: "ARMY", score: "17-11" },
        { year: 2022, winner: "ARMY", score: "20-17" },
        { year: 2021, winner: "NAVY", score: "17-13" },
        { year: 2020, winner: "ARMY", score: "15-0" }
      ]
    }
  };

  // Helper to calculate Y position based on percentage (for chart)
  const getNavyY = () => 300 - (marketData.navyPrice * 300) + 40; // Offset for visual padding
  const getArmyY = () => 300 - (marketData.armyPrice * 300) + 40;

  return (
    <div className="min-h-screen bg-[#050505] text-slate-200 font-sans selection:bg-[#00205B] selection:text-[#C5B783] overflow-x-hidden">
      
      {/* --- CYBER BACKGROUND --- */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {/* Navy Glow */}
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full blur-[120px] opacity-20" style={{backgroundColor: COLORS.NAVY.BLUE}}></div>
        {/* Army Glow */}
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full blur-[120px] opacity-20" style={{backgroundColor: COLORS.ARMY.GOLD}}></div>
        {/* Grid Texture */}
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage: 'linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px)', backgroundSize: '40px 40px'}}></div>
        {/* Scanline */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 to-transparent h-screen w-full animate-scan pointer-events-none mix-blend-overlay"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        
        {/* --- HUD HEADER --- */}
        <header className="flex flex-col md:flex-row justify-between items-end mb-12 border-b border-white/10 pb-6 relative">
          <div className="absolute bottom-0 left-0 w-32 h-[2px]" style={{backgroundColor: COLORS.NAVY.BLUE}}></div>
          <div className="absolute bottom-0 right-0 w-32 h-[2px]" style={{backgroundColor: COLORS.ARMY.GOLD}}></div>
          
          <div className="mb-4 md:mb-0">
            <div className="flex items-center space-x-3 mb-2">
              <Hexagon size={24} className="text-white/80 fill-white/10 animate-pulse" />
              <h1 className="text-3xl md:text-5xl font-black tracking-tighter uppercase text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-slate-500 font-mono">
                RIVALRY<span className="text-white/20">OS</span>
              </h1>
            </div>
            <div className="flex items-center space-x-4 text-[10px] uppercase tracking-[0.3em] text-slate-500 font-mono">
              <span>Simulation v.9.0</span>
              <span className="text-slate-700">|</span>
              <span className="flex items-center"><Cpu size={10} className="mr-1"/> Neural Net Active</span>
              <span className="text-slate-700">|</span>
              <span className={`flex items-center ${marketData.loading ? 'text-yellow-500' : (marketData.isLive ? 'text-emerald-500' : 'text-blue-400')}`}>
                 <Activity size={10} className={`mr-1 ${marketData.loading ? 'animate-spin' : ''}`}/> 
                 {marketData.loading ? 'FETCHING LIVE DATA...' : (marketData.isLive ? 'LIVE FEED ACTIVE' : 'SNAPSHOT MODE')}
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-2 bg-white/5 backdrop-blur-md border border-white/10 rounded-full p-1 pl-4">
             <span className="text-xs font-mono text-slate-400 mr-2">{data.gameDate}</span>
             <div className="flex space-x-1">
                <button 
                  onClick={() => setActiveTab('overview')}
                  className={`px-4 py-1.5 text-xs font-bold rounded-full transition-all duration-300 uppercase tracking-wider ${activeTab === 'overview' ? 'bg-white text-black shadow-[0_0_15px_rgba(255,255,255,0.5)]' : 'text-slate-400 hover:text-white hover:bg-white/10'}`}
                >
                  Intel
                </button>
                <button 
                  onClick={() => setActiveTab('deepDive')}
                  className={`px-4 py-1.5 text-xs font-bold rounded-full transition-all duration-300 uppercase tracking-wider ${activeTab === 'deepDive' ? 'bg-[#00205B] text-white shadow-[0_0_15px_rgba(0,32,91,0.5)]' : 'text-slate-400 hover:text-white hover:bg-white/10'}`}
                >
                  Deep Dive
                </button>
                {/* AI BUTTON */}
                <button 
                  onClick={() => setShowAI(true)}
                  className="px-4 py-1.5 text-xs font-bold rounded-full transition-all duration-300 uppercase tracking-wider bg-purple-600/20 text-purple-300 border border-purple-500/50 hover:bg-purple-600 hover:text-white flex items-center shadow-[0_0_15px_rgba(147,51,234,0.3)] ml-2"
                >
                  <Sparkles size={12} className="mr-1" /> ORACLE
                </button>
             </div>
          </div>
        </header>

        {/* --- VIEW: OVERVIEW --- */}
        {activeTab === 'overview' && (
          <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
            
            {/* MATCHUP HUD */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-16 relative">
              {/* Connecting Lines */}
              <div className="hidden lg:block absolute top-1/2 left-[30%] right-[30%] h-px bg-gradient-to-r from-[#00205B] via-white/20 to-[#D4BF91]"></div>
              
              {/* ARMY CARD */}
              <div className="lg:col-span-4 flex flex-col items-center justify-center relative group">
                <div className="relative z-10 bg-[#1a1a1a]/80 backdrop-blur-xl border border-[#D4BF91]/30 p-8 rounded-tr-3xl rounded-bl-3xl w-full max-w-sm hover:border-[#D4BF91] transition-all duration-500">
                   <div className="absolute -top-3 -left-3 text-[#D4BF91] opacity-50"><Scale size={20} /></div>
                   <div className="flex flex-col items-center">
                      <div className="w-24 h-24 mb-6 rounded-full bg-gradient-to-b from-[#D4BF91]/20 to-transparent flex items-center justify-center border border-[#D4BF91]/20 shadow-[0_0_30px_rgba(212,191,145,0.1)]">
                         <img src="https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/349.png" alt="Army" className="w-16 h-16 object-contain" />
                      </div>
                      <h2 className="text-3xl font-black text-white tracking-widest uppercase mb-1">ARMY</h2>
                      <p className="text-[10px] text-[#D4BF91] font-mono tracking-[0.4em] uppercase mb-6">Black Knights</p>
                      
                      <div className="flex items-baseline space-x-2">
                        <span className="text-6xl font-black text-[#B2B4B3]" style={{textShadow: `0 0 20px ${COLORS.ARMY.GRAY}40`}}>{data.predictedScore.army}</span>
                        <span className="text-xs text-slate-500 font-mono uppercase">PTS</span>
                      </div>
                   </div>
                </div>
              </div>

              {/* VS CORE */}
              <div className="lg:col-span-4 flex flex-col items-center justify-center relative z-20">
                 <div className="w-full bg-black/60 backdrop-blur-2xl border-y border-white/10 p-6 relative overflow-hidden">
                    {/* Scanning Line */}
                    <div className="absolute top-0 bottom-0 left-0 w-1 bg-white/20 animate-[ping_3s_linear_infinite]"></div>
                    
                    <div className="text-center">
                      <div className="text-[10px] font-mono text-slate-400 uppercase tracking-widest mb-2">Market Probability</div>
                      <div className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#00205B] via-[#C5B783] to-[#00205B] animate-pulse">
                        {parseFloat(data.winProb.navy) > 50 ? 'NAVY' : 'ARMY'}
                      </div>
                      <div className="mt-4 flex justify-center items-center space-x-4">
                         <div className="text-right">
                            <div className="text-[10px] text-slate-500 uppercase font-mono">Win Prob</div>
                            <div className="text-xl font-bold" style={{color: COLORS.NAVY.GOLD}}>{data.winProb.navy}%</div>
                         </div>
                         <div className="h-8 w-px bg-white/10"></div>
                         <div className="text-left">
                            <div className="text-[10px] text-slate-500 uppercase font-mono">Vol</div>
                            <div className="text-xl font-bold text-white">${marketData.volume}</div>
                         </div>
                      </div>
                    </div>
                 </div>
                 
                 {/* Probability Bar */}
                 <div className="w-full max-w-xs mt-6 h-2 bg-slate-900 rounded-full overflow-hidden flex relative">
                    <div className="h-full transition-all duration-1000 relative" style={{width: `${data.winProb.army}%`, backgroundColor: COLORS.ARMY.GOLD}}></div>
                    <div className="h-full transition-all duration-1000 relative" style={{width: `${data.winProb.navy}%`, backgroundColor: COLORS.NAVY.BLUE}}></div>
                    {/* Center Tick */}
                    <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-black z-10"></div>
                 </div>
                 <div className="flex justify-between w-full max-w-xs mt-2 text-[9px] font-mono text-slate-500 uppercase">
                    <span>Army {data.winProb.army}%</span>
                    <span>Navy {data.winProb.navy}%</span>
                 </div>
              </div>

              {/* NAVY CARD */}
              <div className="lg:col-span-4 flex flex-col items-center justify-center relative group">
                <div className="relative z-10 bg-[#1a1a1a]/80 backdrop-blur-xl border border-[#00205B]/50 p-8 rounded-tl-3xl rounded-br-3xl w-full max-w-sm hover:border-[#00205B] transition-all duration-500">
                   <div className="absolute -top-3 -right-3 text-[#00205B] opacity-80"><Shield size={20} /></div>
                   <div className="flex flex-col items-center">
                      <div className="w-24 h-24 mb-6 rounded-full bg-gradient-to-b from-[#00205B]/40 to-transparent flex items-center justify-center border border-[#00205B]/40 shadow-[0_0_30px_rgba(0,32,91,0.3)]">
                         <img src="https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/2426.png" alt="Navy" className="w-16 h-16 object-contain" />
                      </div>
                      <h2 className="text-3xl font-black text-white tracking-widest uppercase mb-1">NAVY</h2>
                      <p className="text-[10px] text-[#00205B] font-mono tracking-[0.4em] uppercase mb-6 text-shadow-glow">Midshipmen</p>
                      
                      <div className="flex items-baseline space-x-2">
                        <span className="text-6xl font-black text-[#C5B783]" style={{textShadow: `0 0 20px ${COLORS.NAVY.GOLD}40`}}>{data.predictedScore.navy}</span>
                        <span className="text-xs text-slate-500 font-mono uppercase">PTS</span>
                      </div>
                   </div>
                </div>
              </div>
            </div>

            {/* ANALYTICS GRID */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* METRICS MODULE */}
              <div className="lg:col-span-2 space-y-6">
                <div className="flex items-center space-x-2 mb-4 border-l-2 border-[#00205B] pl-4">
                  <h3 className="text-lg font-bold tracking-widest uppercase text-white font-mono">Tactical Telemetry</h3>
                </div>
                
                <div className="grid gap-3">
                  {data.factors.map((factor, idx) => (
                    <div key={idx} className="bg-white/5 border border-white/5 p-4 flex items-center justify-between hover:bg-white/10 transition-colors rounded-r-lg relative overflow-hidden group">
                      {/* Hover Glow */}
                      <div className={`absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity bg-gradient-to-r from-transparent ${factor.favor === 'navy' ? 'via-[#00205B]/10' : 'via-[#D4BF91]/10'} to-transparent`}></div>
                      
                      <div className="flex flex-col z-10">
                        <span className="text-xs text-slate-400 uppercase font-mono tracking-wider mb-1">{factor.label}</span>
                        <div className="flex items-center space-x-2">
                          <span className={`text-lg font-bold ${factor.favor === 'navy' ? 'text-[#C5B783]' : 'text-[#D4BF91]'}`}>
                            {factor.diff}
                          </span>
                          <TrendingUp size={14} className={factor.favor === 'navy' ? 'text-[#00205B]' : 'text-[#D4BF91]'} />
                        </div>
                      </div>

                      {/* Visual Bar */}
                      <div className="w-32 h-1.5 bg-slate-800 rounded-full overflow-hidden flex z-10">
                         {factor.favor === 'navy' ? (
                            <>
                              <div className="w-1/2 bg-slate-800"></div>
                              <div className="w-1/2 bg-[#00205B] shadow-[0_0_10px_#00205B]"></div>
                            </>
                         ) : (
                            <>
                              <div className="w-1/2 bg-[#D4BF91] shadow-[0_0_10px_#D4BF91]"></div>
                              <div className="w-1/2 bg-slate-800"></div>
                            </>
                         )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* TACTICAL BRIEF */}
                <div className="bg-gradient-to-br from-black to-slate-900 border border-white/10 rounded-xl p-6 relative overflow-hidden">
                  <div className="absolute top-0 right-0 p-4 opacity-10"><Radar size={60} /></div>
                  <h4 className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-6">Strategic Assessment</h4>
                  
                  <div className="grid md:grid-cols-2 gap-8">
                    <div className="border-l border-[#D4BF91]/30 pl-4">
                       <h5 className="text-[#D4BF91] font-bold uppercase text-sm mb-3">Army Strategy</h5>
                       <ul className="space-y-2 text-xs text-slate-400 font-mono">
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#D4BF91] mr-2"></div>Run Hvy (6.5:1)</li>
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#D4BF91] mr-2"></div>Red Zone Eff (100%)</li>
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#D4BF91] mr-2"></div>Clock Control</li>
                       </ul>
                    </div>
                    <div className="border-l border-[#00205B]/50 pl-4">
                       <h5 className="text-[#C5B783] font-bold uppercase text-sm mb-3">Navy Strategy</h5>
                       <ul className="space-y-2 text-xs text-slate-400 font-mono">
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#00205B] mr-2"></div>High Scoring (49%)</li>
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#00205B] mr-2"></div>Explosive YPD</li>
                         <li className="flex items-center"><div className="w-1 h-1 bg-[#00205B] mr-2"></div>TD Efficiency</li>
                       </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* COMPOSITE SCORE CARD */}
              <div className="space-y-6">
                 <div className="bg-[#0A0A0A] border border-white/10 rounded-2xl p-6 relative">
                    <div className="flex justify-between items-center mb-6">
                       <span className="text-xs font-mono text-slate-500 uppercase">Composite Index</span>
                       <Activity size={16} className="text-slate-600" />
                    </div>

                    <div className="space-y-6 relative">
                       {/* Vertical Line */}
                       <div className="absolute left-[30px] top-0 bottom-0 w-px bg-white/5"></div>

                       <div className="flex items-center relative z-10">
                          <div className="w-[60px] text-xs font-bold text-[#D4BF91]">ARMY</div>
                          <div className="flex-1 h-10 bg-slate-900 rounded-sm overflow-hidden flex items-center px-1 relative">
                             <div className="h-2 rounded-sm bg-[#D4BF91]" style={{width: `${(data.stats.army.compScore / 250) * 100}%`}}></div>
                             <span className="absolute right-2 text-[10px] text-slate-500 font-mono">{data.stats.army.compScore}</span>
                          </div>
                       </div>
                       
                       <div className="flex items-center relative z-10">
                          <div className="w-[60px] text-xs font-bold text-[#00205B]">NAVY</div>
                          <div className="flex-1 h-10 bg-slate-900 rounded-sm overflow-hidden flex items-center px-1 relative border border-[#00205B]/30">
                             <div className="h-2 rounded-sm bg-[#00205B] shadow-[0_0_15px_#00205B]" style={{width: `${(data.stats.navy.compScore / 250) * 100}%`}}></div>
                             <span className="absolute right-2 text-[10px] text-slate-500 font-mono">{data.stats.navy.compScore}</span>
                          </div>
                       </div>
                    </div>
                    
                    <div className="mt-6 pt-4 border-t border-white/5 text-center">
                       <span className="text-[10px] uppercase tracking-widest text-emerald-500 animate-pulse">Navy Advantage Detected</span>
                    </div>
                 </div>

                 {/* Historical Quick View */}
                 <div className="bg-white/5 rounded-xl p-4 flex justify-between items-center border border-white/5">
                    <div className="text-center">
                       <div className="text-2xl font-black text-[#D4BF91]">{data.history.team1Wins}</div>
                       <div className="text-[8px] uppercase tracking-widest text-slate-500">Army</div>
                    </div>
                    <div className="h-8 w-px bg-white/10"></div>
                    <div className="text-center">
                       <div className="text-2xl font-black text-[#C5B783]">{data.history.team2Wins}</div>
                       <div className="text-[8px] uppercase tracking-widest text-slate-500">Navy</div>
                    </div>
                 </div>
              </div>

            </div>
          </div>
        )}

        {/* --- VIEW: DEEP DIVE --- */}
        {activeTab === 'deepDive' && (
           <div className="animate-in fade-in slide-in-from-right-8 duration-700 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              
              {/* HISTORICAL AVG */}
              <div className="bg-[#0A0A0A] border border-white/10 rounded-xl p-6 relative overflow-hidden group hover:border-white/20 transition-colors">
                 <div className="absolute top-0 left-0 w-1 h-full bg-[#B2B4B3]"></div>
                 <h3 className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-6">Historical Avg Score</h3>
                 
                 <div className="flex items-end justify-center space-x-6 h-40 border-b border-white/5 pb-2">
                    <div className="flex flex-col items-center w-20">
                       <span className="text-lg font-bold text-[#D4BF91] mb-2">{data.scenarios.avgScore.army}</span>
                       <div className="w-full bg-[#D4BF91]/20 border border-[#D4BF91] h-32 relative rounded-t-sm">
                          <div className="absolute bottom-0 w-full bg-[#D4BF91]" style={{height: `${(data.scenarios.avgScore.army / 25) * 100}%`}}></div>
                       </div>
                    </div>
                    <div className="flex flex-col items-center w-20">
                       <span className="text-lg font-bold text-[#00205B] mb-2">{data.scenarios.avgScore.navy}</span>
                       <div className="w-full bg-[#00205B]/20 border border-[#00205B] h-32 relative rounded-t-sm">
                          <div className="absolute bottom-0 w-full bg-[#00205B]" style={{height: `${(data.scenarios.avgScore.navy / 25) * 100}%`}}></div>
                       </div>
                    </div>
                 </div>
                 <div className="mt-4 text-[10px] text-center text-slate-500 font-mono">
                    PROJECTION ALIGNS WITHIN 1.0 PTS
                 </div>
              </div>

              {/* SCENARIO: CLOSE GAMES */}
              <div className="bg-[#0A0A0A] border border-white/10 rounded-xl p-6 relative overflow-hidden">
                 <div className="absolute top-0 right-0 p-3 opacity-20"><Swords size={40} className="text-white"/></div>
                 <h3 className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-1">Scenario: Close Games</h3>
                 <div className="text-[10px] text-slate-600 mb-6 font-mono uppercase">Margin &le; 7 Pts</div>

                 <div className="flex items-center justify-center mb-6">
                    <div className="relative w-32 h-32 rounded-full border border-white/10 flex items-center justify-center">
                       <div className="absolute inset-0 border-t-2 border-[#D4BF91] rounded-full rotate-45"></div>
                       <div className="absolute inset-0 border-b-2 border-[#00205B] rounded-full -rotate-12"></div>
                       <div className="text-center">
                          <div className="text-2xl font-black text-white">50/50</div>
                          <div className="text-[8px] uppercase tracking-widest text-slate-500">SPLIT</div>
                       </div>
                    </div>
                 </div>
                 
                 <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono">
                    <div className="bg-[#D4BF91]/10 p-2 rounded border border-[#D4BF91]/20">
                       <span className="block text-[#D4BF91] font-bold">21 Wins</span>
                       <span className="text-[8px] text-slate-500">ARMY</span>
                    </div>
                    <div className="bg-[#00205B]/10 p-2 rounded border border-[#00205B]/20">
                       <span className="block text-[#00B4D8] font-bold">23 Wins</span>
                       <span className="text-[8px] text-slate-500">NAVY</span>
                    </div>
                 </div>
              </div>

              {/* SCENARIO: BLOWOUTS */}
              <div className="bg-[#0A0A0A] border border-white/10 rounded-xl p-6 relative overflow-hidden">
                 <div className="absolute top-0 right-0 p-3 opacity-20"><Flame size={40} className="text-[#00205B]"/></div>
                 <h3 className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-1">Scenario: Blowouts</h3>
                 <div className="text-[10px] text-slate-600 mb-6 font-mono uppercase">Margin &ge; 14 Pts</div>

                 <div className="space-y-6">
                    <div>
                       <div className="flex justify-between text-xs mb-2">
                          <span className="text-[#00B4D8] font-bold">NAVY</span>
                          <span className="font-mono text-slate-400">63%</span>
                       </div>
                       <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                          <div className="h-full bg-[#00205B] shadow-[0_0_10px_#00205B]" style={{width: '63%'}}></div>
                       </div>
                    </div>
                    <div>
                       <div className="flex justify-between text-xs mb-2">
                          <span className="text-[#D4BF91] font-bold">ARMY</span>
                          <span className="font-mono text-slate-400">37%</span>
                       </div>
                       <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                          <div className="h-full bg-[#D4BF91]" style={{width: '37%'}}></div>
                       </div>
                    </div>
                 </div>
                 
                 <div className="mt-8 p-3 bg-white/5 border-l-2 border-[#00205B] text-[10px] text-slate-400 leading-relaxed font-mono">
                    KEY INSIGHT: Navy dominates high-scoring variances. Army relies on defensive attrition.
                 </div>
              </div>

              {/* RECENT MATCHUPS */}
              <div className="md:col-span-2 lg:col-span-3 bg-gradient-to-r from-[#0A0A0A] to-[#111] border border-white/10 rounded-xl p-6">
                 <h3 className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-6 flex items-center">
                    <History size={14} className="mr-2"/> Last 5 Operations
                 </h3>
                 <div className="flex flex-wrap justify-between gap-4">
                    {data.history.recent.map((game, i) => (
                       <div key={i} className="flex-1 min-w-[120px] bg-black border border-white/5 p-4 rounded text-center relative overflow-hidden group hover:border-white/20 transition-all">
                          <div className={`absolute top-0 left-0 w-full h-1 ${game.winner === 'NAVY' ? 'bg-[#00205B]' : 'bg-[#D4BF91]'}`}></div>
                          <div className="text-xs text-slate-500 font-mono mb-2">{game.year}</div>
                          <div className={`text-lg font-black mb-1 ${game.winner === 'NAVY' ? 'text-white' : 'text-[#D4BF91]'}`}>
                             {game.winner}
                          </div>
                          <div className="text-[10px] text-slate-600 font-mono bg-white/5 rounded px-2 py-1 inline-block">{game.score}</div>
                       </div>
                    ))}
                 </div>
              </div>

              {/* LIVE MARKET VISUALIZATION (MODERN LINE CHART) */}
              <div className="md:col-span-2 lg:col-span-3 bg-[#0A0A0A] border border-white/10 rounded-xl p-6 relative overflow-hidden flex flex-col">
                 <div className="absolute top-0 right-0 w-64 h-64 bg-[#00205B] opacity-5 blur-[100px] rounded-full"></div>

                 <div className="flex justify-between items-center z-10">
                    <div className="flex flex-col">
                       <h3 className="text-xs font-mono text-slate-500 uppercase tracking-widest flex items-center">
                          <Activity size={14} className="mr-2 text-[#00B4D8]"/> Live Prediction Market
                       </h3>
                       <div className="text-[10px] text-slate-600 font-mono mt-1">Source: Polymarket Gamma API</div>
                    </div>
                    <div className="flex items-center space-x-2">
                       <button onClick={fetchLiveMarketData} className="p-1 hover:bg-white/10 rounded transition-colors" title="Refresh Live Data">
                          <RefreshCw size={12} className={`text-slate-400 ${marketData.loading ? 'animate-spin' : ''}`} />
                       </button>
                       <div className={`w-2 h-2 rounded-full animate-pulse ${marketData.isLive ? 'bg-emerald-500' : 'bg-blue-400'}`}></div>
                       <span className={`text-[10px] font-mono uppercase ${marketData.isLive ? 'text-emerald-500' : 'text-blue-400'}`}>
                          {marketData.isLive ? 'Live' : 'Snapshot'}
                       </span>
                    </div>
                 </div>

                 {/* SVG CHART CONTAINER */}
                 <div className="relative h-64 w-full mt-4 select-none z-10">
                    <svg className="w-full h-full" viewBox="0 0 800 300" preserveAspectRatio="none">
                        {/* Gradients */}
                        <defs>
                          <linearGradient id="gradNavy" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" style={{stopColor: COLORS.NAVY.ACCENT, stopOpacity: 0.2}} />
                            <stop offset="100%" style={{stopColor: COLORS.NAVY.ACCENT, stopOpacity: 0}} />
                          </linearGradient>
                          <linearGradient id="gradArmy" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" style={{stopColor: COLORS.ARMY.GOLD, stopOpacity: 0.2}} />
                            <stop offset="100%" style={{stopColor: COLORS.ARMY.GOLD, stopOpacity: 0}} />
                          </linearGradient>
                        </defs>

                        {/* Grid Lines (Dashed) */}
                        <line x1="0" y1="50" x2="800" y2="50" stroke="#333" strokeDasharray="4 4" strokeWidth="1" />
                        <line x1="0" y1="125" x2="800" y2="125" stroke="#333" strokeDasharray="4 4" strokeWidth="1" />
                        <line x1="0" y1="200" x2="800" y2="200" stroke="#333" strokeDasharray="4 4" strokeWidth="1" />
                        <line x1="0" y1="275" x2="800" y2="275" stroke="#333" strokeDasharray="4 4" strokeWidth="1" />

                        {/* NAVY LINE (Cyan - Trending) */}
                        {/* We simulate a visual history leading to the current live point at the end */}
                        <path 
                          d={`M0,130 C200,130 400,${getNavyY() + 20} 600,${getNavyY() - 10} S 750,${getNavyY()} 800,${getNavyY()}`} 
                          fill="none" 
                          stroke={COLORS.NAVY.ACCENT} 
                          strokeWidth="3" 
                          strokeLinecap="round"
                          className="drop-shadow-[0_0_8px_rgba(0,180,216,0.5)] transition-all duration-1000"
                        />
                        <path 
                          d={`M0,130 C200,130 400,${getNavyY() + 20} 600,${getNavyY() - 10} S 750,${getNavyY()} 800,${getNavyY()} V 300 H 0 Z`} 
                          fill="url(#gradNavy)" 
                          stroke="none"
                          className="transition-all duration-1000"
                        />

                        {/* ARMY LINE (Gold - Trending) */}
                        <path 
                          d={`M0,170 C200,170 400,${getArmyY() - 20} 600,${getArmyY() + 10} S 750,${getArmyY()} 800,${getArmyY()}`} 
                          fill="none" 
                          stroke={COLORS.ARMY.GOLD} 
                          strokeWidth="3" 
                          strokeLinecap="round"
                          className="drop-shadow-[0_0_8px_rgba(212,191,145,0.3)] transition-all duration-1000"
                        />
                         <path 
                          d={`M0,170 C200,170 400,${getArmyY() - 20} 600,${getArmyY() + 10} S 750,${getArmyY()} 800,${getArmyY()} V 300 H 0 Z`} 
                          fill="url(#gradArmy)" 
                          stroke="none"
                          className="transition-all duration-1000"
                        />
                        
                        {/* End Points with TEXT LABELS (Replaced Logos) */}
                        {/* Navy Label */}
                        <text x="790" y={getNavyY() - 15} textAnchor="end" fill={COLORS.NAVY.ACCENT} className="text-xs font-bold font-mono tracking-widest uppercase">NAVY</text>
                        <circle cx="800" cy={getNavyY()} r="4" fill={COLORS.NAVY.ACCENT} stroke="#fff" strokeWidth="2" className="transition-all duration-1000"/>

                        {/* Army Label */}
                        <text x="790" y={getArmyY() + 25} textAnchor="end" fill={COLORS.ARMY.GOLD} className="text-xs font-bold font-mono tracking-widest uppercase">ARMY</text>
                        <circle cx="800" cy={getArmyY()} r="4" fill={COLORS.ARMY.GOLD} stroke="#fff" strokeWidth="2" className="transition-all duration-1000"/>
                    </svg>
                    
                    {/* Time Labels (X-Axis) */}
                    <div className="absolute bottom-0 w-full flex justify-between text-[10px] text-slate-600 font-mono pt-2">
                       <span>6:20am</span>
                       <span>6:30am</span>
                       <span>6:40am</span>
                       <span>6:50am</span>
                       <span>7:00am</span>
                    </div>

                    {/* Right Side Labels (Y-Axis Overlay) */}
                    {/* NAVY (HIGHEST) -> GREEN */}
                    <div className="absolute top-[18%] right-0 transform translate-x-2 text-right pointer-events-none pr-10">
                       <div className="flex flex-col items-end">
                          <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider mb-0.5 flex items-center">
                            Navy <TrendingUp size={10} className="ml-1"/>
                          </span>
                          <span className="text-4xl font-black text-emerald-400 leading-none drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]">
                             {(marketData.navyPrice * 100).toFixed(0)}%
                          </span>
                       </div>
                    </div>

                    {/* ARMY (LOWEST) -> RED */}
                    <div className="absolute bottom-[20%] right-0 transform translate-x-2 text-right pointer-events-none pr-10">
                       <div className="flex flex-col items-end">
                          <span className="text-[10px] font-bold text-red-500 uppercase tracking-wider mb-0.5 flex items-center">
                            Army <TrendingDown size={10} className="ml-1"/>
                          </span>
                          <span className="text-4xl font-black text-red-500 leading-none drop-shadow-[0_0_10px_rgba(239,68,68,0.5)]">
                             {(marketData.armyPrice * 100).toFixed(0)}%
                          </span>
                       </div>
                    </div>
                 </div>

                 {/* Bottom Controls */}
                 <div className="flex justify-between items-center mt-6 pt-4 border-t border-white/5 z-10">
                    <div className="flex space-x-6 text-xs font-bold text-slate-500 font-mono">
                        <span className="text-white cursor-pointer border-b border-white pb-1">1H</span>
                        <span className="hover:text-white cursor-pointer transition-colors pb-1">6H</span>
                        <span className="hover:text-white cursor-pointer transition-colors pb-1">1D</span>
                        <span className="hover:text-white cursor-pointer transition-colors pb-1">1W</span>
                        <span className="hover:text-white cursor-pointer transition-colors pb-1">1M</span>
                        <span className="hover:text-white cursor-pointer transition-colors pb-1">ALL</span>
                    </div>
                    <div className="flex space-x-4 text-slate-500">
                        <FileText size={16} className="hover:text-white cursor-pointer transition-colors" />
                        <Code size={16} className="hover:text-white cursor-pointer transition-colors" />
                        <Settings size={16} className="hover:text-white cursor-pointer transition-colors" />
                    </div>
                 </div>
              </div>
           </div>
        )}

      </div>

      {/* --- AI ORACLE MODAL --- */}
      {showAI && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
          <div className="bg-[#0A0A0A] border border-purple-500/30 w-full max-w-2xl rounded-xl shadow-[0_0_50px_rgba(147,51,234,0.15)] flex flex-col overflow-hidden max-h-[80vh] relative">
            
            {/* Header */}
            <div className="bg-black/50 p-4 border-b border-white/10 flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <Sparkles size={16} className="text-purple-400 animate-pulse" />
                <h3 className="text-sm font-bold text-white tracking-widest uppercase font-mono">Tactical Oracle v9.0</h3>
              </div>
              <button 
                onClick={() => setShowAI(false)}
                className="text-slate-500 hover:text-white transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {/* Chat Body */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-sm">
              {aiHistory.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user' 
                      ? 'bg-purple-900/30 border border-purple-500/30 text-purple-100' 
                      : msg.role === 'system'
                      ? 'bg-blue-900/10 border border-blue-500/20 text-blue-400 text-xs text-center w-full'
                      : 'bg-slate-900 border border-white/10 text-slate-300'
                  }`}>
                    {msg.role !== 'system' && (
                      <div className="text-[10px] uppercase opacity-50 mb-1">
                        {msg.role === 'user' ? 'Operator' : 'RivalryOS'}
                      </div>
                    )}
                    {msg.text}
                  </div>
                </div>
              ))}
              {aiLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-900 border border-white/10 text-slate-300 p-3 rounded-lg">
                    <span className="animate-pulse">PROCESSING TELEMETRY...</span>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleAISubmit} className="p-4 border-t border-white/10 bg-black/50">
              <div className="relative">
                <input
                  type="text"
                  value={aiInput}
                  onChange={(e) => setAiInput(e.target.value)}
                  placeholder="Ask for tactical analysis..."
                  className="w-full bg-slate-900/50 border border-white/10 rounded-lg py-3 pl-4 pr-12 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50 transition-colors font-mono text-sm"
                />
                <button 
                  type="submit"
                  disabled={aiLoading || !aiInput.trim()}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-purple-400 hover:text-white disabled:opacity-50 disabled:hover:text-purple-400 transition-colors"
                >
                  <Send size={16} />
                </button>
              </div>
              <div className="mt-2 flex space-x-2 overflow-x-auto pb-1">
                {['How does Navy win?', 'Army\'s key weakness?', 'Predict X-Factor'].map(prompt => (
                  <button
                    key={prompt}
                    type="button"
                    onClick={() => setAiInput(prompt)}
                    className="whitespace-nowrap px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/5 rounded text-[10px] text-slate-400 hover:text-white transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </form>

          </div>
        </div>
      )}

      <style>{`
        @keyframes scan {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100%); }
        }
        .animate-scan {
          animation: scan 4s linear infinite;
        }
        .text-shadow-glow {
          text-shadow: 0 0 10px currentColor;
        }
      `}</style>
    </div>
  );
};

export default ArmyNavyAnalytics;