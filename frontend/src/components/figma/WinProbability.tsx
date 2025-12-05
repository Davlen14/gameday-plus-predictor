import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';
import { TrendingUp, TrendingDown, Target, Zap, Shield } from 'lucide-react';

interface WinProbabilityProps {
  predictionData?: any;
}

export function WinProbability({ predictionData }: WinProbabilityProps) {
  const [animatedAwayProb, setAnimatedAwayProb] = useState(0);
  const [animatedHomeProb, setAnimatedHomeProb] = useState(0);

  // Use the correct data structure from the original component
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "", primary_color: "#6366f1", alt_color: "#4f46e5" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "", primary_color: "#10b981", alt_color: "#059669" };
  const awayProb = predictionData?.prediction_cards?.win_probability?.away_team_prob || 50.0;
  const homeProb = predictionData?.prediction_cards?.win_probability?.home_team_prob || 50.0;
  const favoredTeam = predictionData?.prediction_cards?.win_probability?.favored_team || awayTeam.name;
  
  // Get confidence from prediction data
  const confidence = predictionData?.confidence?.overall_confidence || 85.2;

  // Animate probabilities on mount - MUST be called before any returns
  useEffect(() => {
    if (!predictionData) return;
    
    const duration = 1500;
    const steps = 60;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      
      setAnimatedAwayProb(awayProb * easeOutQuart);
      setAnimatedHomeProb(homeProb * easeOutQuart);

      if (currentStep >= steps) {
        clearInterval(timer);
        setAnimatedAwayProb(awayProb);
        setAnimatedHomeProb(homeProb);
      }
    }, stepDuration);

    return () => clearInterval(timer);
  }, [awayProb, homeProb, predictionData]);

  // Early return AFTER all hooks
  if (!predictionData) {
    return (
      <GlassCard className="p-8">
        <div className="flex items-center gap-2 mb-6">
          <Target className="w-5 h-5 text-cyan-400" />
          <h3 className="text-white font-semibold text-lg">Win Probability Analysis</h3>
        </div>
        <div className="text-gray-400 text-center py-8">
          Select teams to see win probability analysis
        </div>
      </GlassCard>
    );
  }

  // Calculate key factors for win probability
  const probDifference = Math.abs(homeProb - awayProb);
  const isFavorite = (team: string) => favoredTeam === team;
  const getFavoriteMargin = () => probDifference.toFixed(1);
  
  // Determine confidence level
  const getConfidenceLevel = () => {
    if (confidence >= 85) return { text: "Very High", color: "emerald", icon: Zap };
    if (confidence >= 75) return { text: "High", color: "green", icon: TrendingUp };
    if (confidence >= 65) return { text: "Moderate", color: "yellow", icon: Target };
    return { text: "Low", color: "orange", icon: Shield };
  };

  const confidenceLevel = getConfidenceLevel();
  const ConfidenceIcon = confidenceLevel.icon;

  // Dynamic win probability data for pie chart
  const pieData = [
    { name: awayTeam.name, value: animatedAwayProb, color: awayTeam.primary_color || '#6366f1' },
    { name: homeTeam.name, value: animatedHomeProb, color: homeTeam.primary_color || '#10b981' }
  ];

  // Generate reasons for win probability
  const getWinProbabilityReasons = (team: any, prob: number, isHome: boolean) => {
    const reasons = [];
    
    if (isFavorite(team.name)) {
      if (prob > 75) {
        reasons.push({
          icon: Zap,
          text: `Strong favorite with ${getFavoriteMargin()}% edge`,
          color: team.primary_color
        });
      } else if (prob > 60) {
        reasons.push({
          icon: TrendingUp,
          text: `Moderate favorite with ${getFavoriteMargin()}% advantage`,
          color: team.primary_color
        });
      } else {
        reasons.push({
          icon: Target,
          text: `Slight favorite by ${getFavoriteMargin()}%`,
          color: team.primary_color
        });
      }
    } else {
      reasons.push({
        icon: TrendingDown,
        text: `Underdog trailing by ${getFavoriteMargin()}%`,
        color: team.primary_color
      });
    }

    // Add home field advantage for home team
    if (isHome) {
      reasons.push({
        icon: Shield,
        text: "Home field advantage included",
        color: team.primary_color
      });
    }

    // Add model confidence factor
    if (confidence > 80) {
      reasons.push({
        icon: ConfidenceIcon,
        text: `${confidenceLevel.text} model confidence (${confidence.toFixed(1)}%)`,
        color: team.primary_color
      });
    }

    return reasons;
  };

  const awayReasons = getWinProbabilityReasons(awayTeam, awayProb, false);
  const homeReasons = getWinProbabilityReasons(homeTeam, homeProb, true);

  return (
    <GlassCard className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Target className="w-5 h-5 text-cyan-400" />
          <h3 className="text-white font-semibold text-lg">Win Probability Analysis</h3>
        </div>
        <div 
          className="px-3 py-1 rounded-full border transition-all duration-300"
          style={{
            backgroundColor: confidenceLevel.color === 'emerald' ? 'rgba(16, 185, 129, 0.2)' :
                            confidenceLevel.color === 'yellow' ? 'rgba(234, 179, 8, 0.2)' :
                            'rgba(239, 68, 68, 0.2)',
            borderColor: confidenceLevel.color === 'emerald' ? 'rgba(16, 185, 129, 0.4)' :
                        confidenceLevel.color === 'yellow' ? 'rgba(234, 179, 8, 0.4)' :
                        'rgba(239, 68, 68, 0.4)'
          }}
        >
          <span 
            className="text-xs font-semibold"
            style={{
              color: confidenceLevel.color === 'emerald' ? '#10b981' :
                    confidenceLevel.color === 'yellow' ? '#eab308' :
                    '#ef4444'
            }}
          >
            {confidenceLevel.text} Confidence
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Away Team Card */}
        <div className="space-y-4">
          <div 
            className="relative overflow-hidden rounded-xl p-6 border-2 transition-all duration-500 hover:scale-105" 
            style={{ 
              borderColor: isFavorite(awayTeam.name) ? `${awayTeam.primary_color}60` : `${awayTeam.primary_color}30`,
              background: `linear-gradient(135deg, ${awayTeam.primary_color}20, ${awayTeam.primary_color}05)`,
              boxShadow: isFavorite(awayTeam.name) ? `0 0 30px ${awayTeam.primary_color}40` : 'none'
            }}
          >
            {isFavorite(awayTeam.name) && (
              <div className="absolute top-2 right-2 px-2 py-1 rounded-full bg-yellow-500/20 border border-yellow-400/40">
                <span className="text-yellow-400 text-[10px] font-bold">FAVORITE</span>
              </div>
            )}
            
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-12 h-12 object-contain" />
              <div className="flex-1">
                <div className="font-bold text-sm" style={{ color: awayTeam.primary_color }}>{awayTeam.name}</div>
                <div className="text-gray-400 text-xs">Away Team</div>
              </div>
            </div>
            
            <div className="mb-4">
              <div className="flex items-baseline gap-1 mb-2">
                <span className="font-bold text-5xl font-mono" style={{ color: awayTeam.primary_color }}>
                  {animatedAwayProb.toFixed(1)}
                </span>
                <span className="text-2xl" style={{ color: awayTeam.primary_color }}>%</span>
              </div>
              
              {/* Animated Progress Bar */}
              <div className="h-2 backdrop-blur-sm rounded-full overflow-hidden relative">
                <div 
                  className="h-full rounded-full transition-all duration-1500 ease-out relative overflow-hidden" 
                  style={{ 
                    width: `${animatedAwayProb}%`,
                    background: `linear-gradient(90deg, ${awayTeam.primary_color}, ${awayTeam.alt_color || awayTeam.primary_color})`
                  }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                </div>
              </div>
            </div>

            {/* Reasons */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-300 mb-2">Why this probability:</div>
              {awayReasons.map((reason, idx) => {
                const Icon = reason.icon;
                return (
                  <div key={idx} className="flex items-start gap-2 text-xs">
                    <Icon className="w-3 h-3 mt-0.5 flex-shrink-0" style={{ color: reason.color }} />
                    <span className="text-gray-300 leading-tight">{reason.text}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Dynamic Circular Chart */}
        <div className="flex items-center justify-center">
          <div className="relative" style={{ height: '380px', width: '100%' }}>
            {/* Outer glow rings - Multiple layers for depth */}
            <div className="absolute inset-0 flex items-center justify-center">
              {/* Outer pulsing glow */}
              <div 
                className="absolute rounded-full animate-pulse opacity-15"
                style={{ 
                  width: '360px',
                  height: '360px',
                  background: `radial-gradient(circle, ${favoredTeam === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color}50, transparent 70%)`,
                  filter: 'blur(40px)'
                }}
              ></div>
              
              {/* Middle rotating glow */}
              <div 
                className="absolute rounded-full animate-spin-slow opacity-20"
                style={{ 
                  width: '340px',
                  height: '340px',
                  background: `conic-gradient(from 0deg, transparent, ${favoredTeam === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color}60, transparent)`,
                  filter: 'blur(30px)'
                }}
              ></div>
              
              {/* Inner sharp glow */}
              <div 
                className="absolute rounded-full opacity-25"
                style={{ 
                  width: '320px',
                  height: '320px',
                  background: `radial-gradient(circle, ${favoredTeam === awayTeam.name ? awayTeam.primary_color : homeTeam.primary_color}40, transparent 60%)`,
                  filter: 'blur(20px)'
                }}
              ></div>
            </div>

            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={160}
                  innerRadius={110}
                  fill="#8884d8"
                  dataKey="value"
                  strokeWidth={0}
                  stroke="transparent"
                  animationDuration={1500}
                  animationEasing="ease-out"
                >
                  {pieData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={entry.color}
                      style={{
                        filter: `drop-shadow(0 0 20px ${entry.color}80) drop-shadow(0 0 40px ${entry.color}40)`,
                      }}
                    />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            
            {/* Center Content - Favored Team - HOLOGRAPHIC 3D LOGO */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="relative text-center">
                {favoredTeam === awayTeam.name ? (
                  <>
                    {/* Multi-layer 3D Holographic Effect */}
                    <div className="relative w-40 h-40 flex items-center justify-center">
                      {/* Outer Glow Ring - Rotating */}
                      <div 
                        className="absolute inset-0 rounded-full opacity-40 animate-spin-slow"
                        style={{ 
                          background: `conic-gradient(from 0deg, ${awayTeam.primary_color}00, ${awayTeam.primary_color}ff, ${awayTeam.primary_color}00)`,
                          filter: 'blur(20px)'
                        }}
                      ></div>
                      
                      {/* Middle Glow - Pulsing */}
                      <div 
                        className="absolute inset-4 rounded-full opacity-60 animate-pulse-slow"
                        style={{ 
                          background: `radial-gradient(circle, ${awayTeam.primary_color}80, transparent 70%)`,
                          filter: 'blur(15px)'
                        }}
                      ></div>
                      
                      {/* Inner Shimmer Effect */}
                      <div 
                        className="absolute inset-8 rounded-full opacity-30"
                        style={{ 
                          background: `linear-gradient(135deg, ${awayTeam.primary_color}ff, transparent, ${awayTeam.primary_color}80)`,
                          animation: 'shimmer-rotate 4s linear infinite',
                          filter: 'blur(8px)'
                        }}
                      ></div>
                      
                      {/* Holographic Glass Effect Background */}
                      <div 
                        className="absolute inset-10 rounded-full"
                        style={{ 
                          background: `radial-gradient(circle at 30% 30%, ${awayTeam.primary_color}40, ${awayTeam.primary_color}10)`,
                          backdropFilter: 'blur(10px)',
                          border: `1px solid ${awayTeam.primary_color}20`,
                          boxShadow: `
                            inset 0 0 20px ${awayTeam.primary_color}30,
                            0 0 40px ${awayTeam.primary_color}40,
                            0 0 60px ${awayTeam.primary_color}20
                          `
                        }}
                      ></div>
                      
                      {/* Logo with 3D Transform */}
                      <div className="relative z-10" style={{
                        transform: 'perspective(1000px) rotateX(5deg)',
                        filter: `drop-shadow(0 10px 20px ${awayTeam.primary_color}60) drop-shadow(0 0 30px ${awayTeam.primary_color}40)`
                      }}>
                        <ImageWithFallback 
                          src={awayTeam.logo} 
                          alt="Favorite" 
                          className="w-32 h-32 object-contain animate-float"
                          style={{
                            filter: `brightness(1.2) saturate(1.3)`,
                          }}
                        />
                      </div>
                      
                      {/* Light Reflection Effect */}
                      <div 
                        className="absolute top-8 left-8 w-16 h-16 rounded-full opacity-40"
                        style={{ 
                          background: `radial-gradient(circle at 30% 30%, white, transparent 60%)`,
                          filter: 'blur(10px)'
                        }}
                      ></div>
                    </div>
                    
                    {/* Edge Label with Holographic Style */}
                    <div 
                      className="mt-4 relative"
                      style={{ 
                        filter: `drop-shadow(0 0 10px ${awayTeam.primary_color}80)`
                      }}
                    >
                      <div
                        className="inline-block px-5 py-2 rounded-full relative overflow-hidden"
                        style={{ 
                          background: `linear-gradient(135deg, ${awayTeam.primary_color}30, ${awayTeam.primary_color}10)`,
                          backdropFilter: 'blur(20px)',
                          border: `1px solid ${awayTeam.primary_color}40`,
                          boxShadow: `
                            inset 0 1px 1px ${awayTeam.primary_color}60,
                            0 0 20px ${awayTeam.primary_color}40,
                            0 4px 15px ${awayTeam.primary_color}30
                          `
                        }}
                      >
                        {/* Shimmer overlay */}
                        <div 
                          className="absolute inset-0 opacity-30"
                          style={{
                            background: `linear-gradient(90deg, transparent, ${awayTeam.primary_color}60, transparent)`,
                            animation: 'shimmer 3s infinite'
                          }}
                        ></div>
                        <span 
                          className="font-bold text-base whitespace-nowrap relative z-10" 
                          style={{ 
                            color: awayTeam.primary_color,
                            textShadow: `0 0 10px ${awayTeam.primary_color}80, 0 2px 4px rgba(0,0,0,0.5)`
                          }}
                        >
                          {getFavoriteMargin()}% Edge
                        </span>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    {/* Multi-layer 3D Holographic Effect */}
                    <div className="relative w-40 h-40 flex items-center justify-center">
                      {/* Outer Glow Ring - Rotating */}
                      <div 
                        className="absolute inset-0 rounded-full opacity-40 animate-spin-slow"
                        style={{ 
                          background: `conic-gradient(from 0deg, ${homeTeam.primary_color}00, ${homeTeam.primary_color}ff, ${homeTeam.primary_color}00)`,
                          filter: 'blur(20px)'
                        }}
                      ></div>
                      
                      {/* Middle Glow - Pulsing */}
                      <div 
                        className="absolute inset-4 rounded-full opacity-60 animate-pulse-slow"
                        style={{ 
                          background: `radial-gradient(circle, ${homeTeam.primary_color}80, transparent 70%)`,
                          filter: 'blur(15px)'
                        }}
                      ></div>
                      
                      {/* Inner Shimmer Effect */}
                      <div 
                        className="absolute inset-8 rounded-full opacity-30"
                        style={{ 
                          background: `linear-gradient(135deg, ${homeTeam.primary_color}ff, transparent, ${homeTeam.primary_color}80)`,
                          animation: 'shimmer-rotate 4s linear infinite',
                          filter: 'blur(8px)'
                        }}
                      ></div>
                      
                      {/* Holographic Glass Effect Background */}
                      <div 
                        className="absolute inset-10 rounded-full"
                        style={{ 
                          background: `radial-gradient(circle at 30% 30%, ${homeTeam.primary_color}40, ${homeTeam.primary_color}10)`,
                          backdropFilter: 'blur(10px)',
                          border: `1px solid ${homeTeam.primary_color}20`,
                          boxShadow: `
                            inset 0 0 20px ${homeTeam.primary_color}30,
                            0 0 40px ${homeTeam.primary_color}40,
                            0 0 60px ${homeTeam.primary_color}20
                          `
                        }}
                      ></div>
                      
                      {/* Logo with 3D Transform */}
                      <div className="relative z-10" style={{
                        transform: 'perspective(1000px) rotateX(5deg)',
                        filter: `drop-shadow(0 10px 20px ${homeTeam.primary_color}60) drop-shadow(0 0 30px ${homeTeam.primary_color}40)`
                      }}>
                        <ImageWithFallback 
                          src={homeTeam.logo} 
                          alt="Favorite" 
                          className="w-32 h-32 object-contain animate-float"
                          style={{
                            filter: `brightness(1.2) saturate(1.3)`,
                          }}
                        />
                      </div>
                      
                      {/* Light Reflection Effect */}
                      <div 
                        className="absolute top-8 left-8 w-16 h-16 rounded-full opacity-40"
                        style={{ 
                          background: `radial-gradient(circle at 30% 30%, white, transparent 60%)`,
                          filter: 'blur(10px)'
                        }}
                      ></div>
                    </div>
                    
                    {/* Edge Label with Holographic Style */}
                    <div 
                      className="mt-4 relative"
                      style={{ 
                        filter: `drop-shadow(0 0 10px ${homeTeam.primary_color}80)`
                      }}
                    >
                      <div
                        className="inline-block px-5 py-2 rounded-full relative overflow-hidden"
                        style={{ 
                          background: `linear-gradient(135deg, ${homeTeam.primary_color}30, ${homeTeam.primary_color}10)`,
                          backdropFilter: 'blur(20px)',
                          border: `1px solid ${homeTeam.primary_color}40`,
                          boxShadow: `
                            inset 0 1px 1px ${homeTeam.primary_color}60,
                            0 0 20px ${homeTeam.primary_color}40,
                            0 4px 15px ${homeTeam.primary_color}30
                          `
                        }}
                      >
                        {/* Shimmer overlay */}
                        <div 
                          className="absolute inset-0 opacity-30"
                          style={{
                            background: `linear-gradient(90deg, transparent, ${homeTeam.primary_color}60, transparent)`,
                            animation: 'shimmer 3s infinite'
                          }}
                        ></div>
                        <span 
                          className="font-bold text-base whitespace-nowrap relative z-10" 
                          style={{ 
                            color: homeTeam.primary_color,
                            textShadow: `0 0 10px ${homeTeam.primary_color}80, 0 2px 4px rgba(0,0,0,0.5)`
                          }}
                        >
                          {getFavoriteMargin()}% Edge
                        </span>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Home Team Card */}
        <div className="space-y-4">
          <div 
            className="relative overflow-hidden rounded-xl p-6 border-2 transition-all duration-500 hover:scale-105" 
            style={{ 
              borderColor: isFavorite(homeTeam.name) ? `${homeTeam.primary_color}60` : `${homeTeam.primary_color}30`,
              background: `linear-gradient(135deg, ${homeTeam.primary_color}20, ${homeTeam.primary_color}05)`,
              boxShadow: isFavorite(homeTeam.name) ? `0 0 30px ${homeTeam.primary_color}40` : 'none'
            }}
          >
            {isFavorite(homeTeam.name) && (
              <div className="absolute top-2 right-2 px-2 py-1 rounded-full bg-yellow-500/20 border border-yellow-400/40">
                <span className="text-yellow-400 text-[10px] font-bold">FAVORITE</span>
              </div>
            )}
            
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-12 h-12 object-contain" />
              <div className="flex-1">
                <div className="font-bold text-sm" style={{ color: homeTeam.primary_color }}>{homeTeam.name}</div>
                <div className="text-gray-400 text-xs">Home Team</div>
              </div>
            </div>
            
            <div className="mb-4">
              <div className="flex items-baseline gap-1 mb-2">
                <span className="font-bold text-5xl font-mono" style={{ color: homeTeam.primary_color }}>
                  {animatedHomeProb.toFixed(1)}
                </span>
                <span className="text-2xl" style={{ color: homeTeam.primary_color }}>%</span>
              </div>
              
              {/* Animated Progress Bar */}
              <div className="h-2 backdrop-blur-sm rounded-full overflow-hidden relative">
                <div 
                  className="h-full rounded-full transition-all duration-1500 ease-out relative overflow-hidden" 
                  style={{ 
                    width: `${animatedHomeProb}%`,
                    background: `linear-gradient(90deg, ${homeTeam.primary_color}, ${homeTeam.alt_color || homeTeam.primary_color})`
                  }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                </div>
              </div>
            </div>

            {/* Reasons */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-300 mb-2">Why this probability:</div>
              {homeReasons.map((reason, idx) => {
                const Icon = reason.icon;
                return (
                  <div key={idx} className="flex items-start gap-2 text-xs">
                    <Icon className="w-3 h-3 mt-0.5 flex-shrink-0" style={{ color: reason.color }} />
                    <span className="text-gray-300 leading-tight">{reason.text}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}