import { useState, useEffect, useRef } from 'react';
import { Moon, Sun } from 'lucide-react';
import { CONFIG } from './config';
import { TeamSelector } from './components/figma/TeamSelector';
import { Header } from './components/figma/Header';
import { PredictionResults } from './components/figma/PredictionResults';
import { PredictionCards } from './components/figma/PredictionCards';
import { ConfidenceSection } from './components/figma/ConfidenceSection';
import { MarketComparison } from './components/figma/MarketComparison';
import { LineMovement } from './components/figma/LineMovement';
import { ArbitrageOpportunities } from './components/figma/ArbitrageOpportunities';
import { ArbitrageCalculator } from './components/figma/ArbitrageCalculator';
import { ContextualAnalysis } from './components/figma/ContextualAnalysis';
import { MediaInformation } from './components/figma/MediaInformation';
import { EPAComparison } from './components/figma/EPAComparison';
import { DifferentialAnalysis } from './components/figma/DifferentialAnalysis';
import { WinProbability } from './components/figma/WinProbability';
import { SituationalPerformance } from './components/figma/SituationalPerformance';
import { FieldPositionMetrics } from './components/figma/FieldPositionMetrics';
import { KeyPlayerImpact } from './components/figma/KeyPlayerImpact';
import { AdvancedMetrics } from './components/figma/AdvancedMetrics';
import { WeightsBreakdown } from './components/figma/WeightsBreakdown';
import { ComponentBreakdown } from './components/figma/ComponentBreakdown';
import { ComprehensiveTeamStats } from './components/figma/ComprehensiveStats';
import { CoachingComparison } from './components/figma/CoachingComparison';
import { DriveEfficiency } from './components/figma/DriveEfficiency';
import { ExtendedDefensiveAnalytics } from './components/figma/ExtendedDefensiveAnalytics';
import ComprehensiveRatingsComparison from './components/figma/ComprehensiveRatingsComparison';
import { APPollRankings } from './components/figma/APPollRankings';
import { SeasonRecords } from './components/figma/SeasonRecords';
import { FinalPredictionSummary } from './components/figma/FinalPredictionSummary';
import { Glossary } from './components/figma/Glossary';
import { EnhancedTeamStats } from './components/figma/EnhancedTeamStats';
import LiveGameBadge from './components/figma/LiveGameBadge';
import FieldVisualization from './components/figma/FieldVisualization';
import WinProbabilityLive from './components/figma/WinProbabilityLive';
import LivePlaysFeed from './components/figma/LivePlaysFeed';
import ComprehensiveMetricsDashboard from './components/figma/ComprehensiveMetricsDashboard';
import { ATSComparison } from './components/figma/ATSComparison';
import { PlayerPropsPanel } from './components/figma/PlayerPropsPanel';
import RivalryHistoryCard from './components/RivalryHistoryCard';

// Import comprehensive power rankings data
import powerRankingsData from './data/comprehensive_power_rankings.json';

export default function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [predictionData, setPredictionData] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [liveData, setLiveData] = useState<any | null>(null);
  const [selectedTeams, setSelectedTeams] = useState<{ home: string; away: string } | null>(null);
  const intervalRef = useRef<number | null>(null);
  
  // Fetch live game data
  const fetchLiveData = async (homeTeam: string, awayTeam: string) => {
    try {
      const response = await fetch(
        `${CONFIG.API.BASE_URL}/api/live-game?home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`
      );
      
      if (!response.ok) {
        console.error('Live data fetch failed');
        return;
      }
      
      const data = await response.json();
      
      // Only set live data if game is actually live
      if (data.game_info?.is_live) {
        setLiveData(data);
      } else {
        setLiveData(null);
      }
    } catch (error) {
      console.error('Error fetching live data:', error);
    }
  };
  
  // Auto-refresh effect for live data
  useEffect(() => {
    // Clear any existing interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    // Only start polling if we have teams selected and live data is active
    if (selectedTeams && liveData?.game_info?.is_live) {
      // Initial fetch
      fetchLiveData(selectedTeams.home, selectedTeams.away);
      
      // Set up polling every 30 seconds
      intervalRef.current = window.setInterval(() => {
        fetchLiveData(selectedTeams.home, selectedTeams.away);
      }, 30000);
    }
    
    // Cleanup on unmount or when dependencies change
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [selectedTeams, liveData?.game_info?.is_live]);

  const handlePrediction = async (homeTeam: string, awayTeam: string) => {
    setIsLoading(true);
    setError(null);
    setSelectedTeams({ home: homeTeam, away: awayTeam });
    
    try {
      // Fetch prediction data
      const response = await fetch(`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          home_team: homeTeam,
          away_team: awayTeam
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch prediction');
      }

      const data = await response.json();
      // Pass the complete data structure including formatted_analysis and rivalry_history
      setPredictionData(data.ui_components ? { 
        ...data.ui_components, 
        formatted_analysis: data.formatted_analysis,
        rivalry_history: data.rivalry_history 
      } : data);
      
      // Also check for live game data
      await fetchLiveData(homeTeam, awayTeam);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      {/* Premium Glass Background */}
      <div className="min-h-screen relative overflow-hidden">
        {/* Premium Textured Background */}
        <div className="absolute inset-0" style={{
          background: `
            radial-gradient(circle at 25% 25%, hsla(210, 15%, 25%, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, hsla(220, 20%, 30%, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 100%, hsla(200, 12%, 20%, 0.06) 0%, transparent 70%),
            linear-gradient(135deg, hsla(0, 0%, 8%, 1) 0%, hsla(210, 8%, 12%, 1) 25%, hsla(220, 6%, 15%, 1) 50%, hsla(200, 7%, 10%, 1) 75%, hsla(0, 0%, 6%, 1) 100%)
          `,
          backgroundSize: '400px 400px, 600px 600px, 800px 800px, 100% 100%'
        }}></div>
        
        {/* Subtle Noise Texture Overlay */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
            backgroundSize: '180px 180px'
          }}
        ></div>
        
        {/* Content */}
        <div className="relative z-10 px-3 py-4 sm:px-4 sm:py-6 md:p-8 lg:p-12 text-white">
          <div className="max-w-[1600px] mx-auto space-y-4 sm:space-y-6">
          
          {/* Modern Header */}
          <div className="relative text-center mb-8 sm:mb-12">
            {/* Theme Toggle - Top Right */}
            <div className="absolute top-0 right-0">
              <button 
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 sm:p-3 md:p-4 bg-slate-900/70 backdrop-blur-xl border border-white/20 hover:border-white/40 rounded-lg sm:rounded-xl transition-all duration-300 hover:scale-105 hover:bg-slate-800/80 shadow-lg hover:shadow-xl"
                aria-label="Toggle theme"
              >
                {darkMode ? (
                  <Sun className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-yellow-400 drop-shadow-sm" />
                ) : (
                  <Moon className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-slate-300 drop-shadow-sm" />
                )}
              </button>
            </div>

            {/* Main Title */}
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-7xl font-bold mb-3 sm:mb-4 px-2 sm:px-0">
              <span 
                className="italic"
                style={{
                  fontFamily: 'var(--font-orbitron)',
                  background: 'linear-gradient(45deg, #C0C0C0, #E5E5E5, #A9A9A9, #D3D3D3, #808080, #BEBEBE, #C0C0C0)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}
              >
                GAMEDAY+
              </span>
              
              {/* Version and Status */}
              <div className="flex items-center justify-center gap-4 mt-4 text-sm font-mono">
                <span className="text-slate-300 bg-slate-900/70 backdrop-blur-sm border border-white/20 px-4 py-2 rounded-full shadow-lg">
                  v 0.2.1
                </span>
                <div className="flex items-center gap-3 text-slate-300 bg-slate-900/70 backdrop-blur-sm border border-emerald-500/30 px-4 py-2 rounded-full shadow-lg">
                  <div className="relative">
                    <div 
                      className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.6)]"
                      style={{
                        animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
                      }}
                    ></div>
                    <div 
                      className="absolute inset-0 w-3 h-3 bg-emerald-300 rounded-full animate-ping"
                      style={{
                        animation: 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite'
                      }}
                    ></div>
                  </div>
                  <span className="text-sm tracking-wider uppercase text-emerald-300 font-semibold">LIVE</span>
                </div>
              </div>
            </h1>
          </div>

          {/* Team Selector */}
          <TeamSelector 
            onPrediction={handlePrediction}
            isLoading={isLoading}
          />
          
          {/* Header - Game Info & Teams */}
          <Header predictionData={predictionData} isLoading={isLoading} />
          
          {/* Rivalry History - Shows if this is a rivalry game */}
          {predictionData?.rivalry_history && (
            <>
              {console.log('App.tsx: Rendering RivalryHistoryCard with data:', predictionData.rivalry_history)}
              <RivalryHistoryCard rivalryData={predictionData.rivalry_history} />
            </>
          )}
          
          {/* Prediction Results - Shows after game is complete */}
          {predictionData && (
            <PredictionResults 
              predictionData={predictionData}
            />
          )}
          
          {/* 🔴 LIVE GAME SECTION - Only shows when game is in progress */}
          {liveData?.game_info?.is_live && (
            <>
              <LiveGameBadge 
                period={liveData.game_state.period}
                clock={liveData.game_state.clock}
              />
              
              <FieldVisualization
                possession={{
                  team: liveData.game_state.possession === 'home' 
                    ? liveData.game_info.home_team 
                    : liveData.game_info.away_team,
                  logo: liveData.game_state.possession === 'home'
                    ? predictionData?.team_selector?.home_team?.logo
                    : predictionData?.team_selector?.away_team?.logo
                }}
                fieldPosition={{
                  yardLine: liveData.field_position?.yard_line || 50,
                  down: parseInt(liveData.game_state.situation?.match(/(\d+)(?:st|nd|rd|th)/)?.[1] || '1'),
                  distance: parseInt(liveData.game_state.situation?.match(/& (\d+)/)?.[1] || '10')
                }}
                homeTeam={{
                  name: liveData.game_info.home_team,
                  abbr: liveData.game_info.home_team.substring(0, 3).toUpperCase(),
                  color: predictionData?.team_selector?.home_team?.primary_color || '#1a7a42',
                  logo: predictionData?.team_selector?.home_team?.logo
                }}
                awayTeam={{
                  name: liveData.game_info.away_team,
                  abbr: liveData.game_info.away_team.substring(0, 3).toUpperCase(),
                  color: predictionData?.team_selector?.away_team?.primary_color || '#0d5c2f',
                  logo: predictionData?.team_selector?.away_team?.logo
                }}
                situation={liveData.game_state.situation}
              />
              
              <WinProbabilityLive
                liveData={liveData}
                predictionData={predictionData}
              />
              
              <LivePlaysFeed
                plays={liveData.plays?.recent_plays || []}
                showEPA={true}
                predictionData={predictionData}
              />
            </>
          )}
          
          {/* ========================================================================= */}
          {/* 🎯 THE VERDICT: What You Need to Know First */}
          {/* ========================================================================= */}
          
          {/* Main Prediction Results - Win%, Spread, Total */}
          <PredictionCards predictionData={predictionData} isLoading={isLoading} error={error || undefined} />
          
          {/* Final Summary with Predicted Score & Key Factors */}
          <FinalPredictionSummary predictionData={predictionData} />
          
          {/* Confidence Score - HOW SURE IS THE MODEL? */}
          {/* <ConfidenceSection predictionData={predictionData} isLoading={isLoading} error={error || undefined} /> */}
          
          {/* ========================================================================= */}
          {/* 💰 VALUE HUNTING: Where's the Edge? */}
          {/* ========================================================================= */}
          
          {/* ATS Comparison - Against The Spread Performance */}
          <ATSComparison predictionData={predictionData} />
          
          {/* Player Props - Top betting opportunities */}
          <PlayerPropsPanel predictionData={predictionData} />
          
          {/* Market Comparison - Model vs Vegas Lines */}
          <MarketComparison predictionData={predictionData} />
          
          {/* Line Movement - How the market is reacting */}
          <LineMovement predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 🧠 THE BRAIN: What Drives This Prediction? */}
          {/* ========================================================================= */}
          
          {/* Model Weights - See what matters most in this matchup */}
          {/* <WeightsBreakdown predictionData={predictionData} /> */}
          
          {/* Component Breakdown - How each factor contributed */}
          {/* <ComponentBreakdown predictionData={predictionData} /> */}
          
          {/* ========================================================================= */}
          {/* 👥 GAME CHANGERS: Player Impact */}
          {/* ========================================================================= */}
          
          {/* Key Player Impact - QBs, WRs who move the needle */}
          <KeyPlayerImpact predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 📊 ADVANCED ANALYTICS: The Deep Dive */}
          {/* ========================================================================= */}
          
          {/* EPA Comparison - Most important efficiency metric */}
          <EPAComparison predictionData={predictionData} />
          
          {/* Win Probability Distribution */}
          <WinProbability predictionData={predictionData} />
          
          {/* Comprehensive Differential Analysis - Side-by-side comparison */}
          <DifferentialAnalysis predictionData={predictionData} />
          
          {/* Advanced Metrics - Success rate, explosiveness, etc */}
          <AdvancedMetrics predictionData={predictionData} />
          
          {/* Situational Performance - 3rd down, red zone, etc */}
          <SituationalPerformance predictionData={predictionData} />
          
          {/* Field Position Metrics - Starting field position advantage */}
          <FieldPositionMetrics predictionData={predictionData} />
          
          {/* Drive Efficiency - Scoring drives, explosive plays, methodical drives */}
          <DriveEfficiency predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 🏆 TEAM PROFILES: Who Are These Teams? */}
          {/* ========================================================================= */}
          
          {/* Season Records - Game-by-game results */}
          <SeasonRecords predictionData={predictionData} />
          
          {/* Comprehensive Team Statistics - Full statistical profile */}
          <ComprehensiveTeamStats predictionData={predictionData} />
          
          {/* Enhanced Team Stats - Offense, efficiency, special teams */}
          <EnhancedTeamStats predictionData={predictionData} />
          
          {/* Extended Defensive Analytics - Defensive deep dive */}
          <ExtendedDefensiveAnalytics predictionData={predictionData} />
          
          {/* Coaching Comparison - Experience, records, recruiting */}
          <CoachingComparison predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 🌍 CONTEXT MATTERS: External Factors */}
          {/* ========================================================================= */}
          
          {/* Weather, Bye Weeks, Injuries */}
          <ContextualAnalysis predictionData={predictionData} />
          
          {/* AP Poll Rankings */}
          <APPollRankings predictionData={predictionData} />
          
          {/* Media Information - Network, time, excitement index */}
          {/* <MediaInformation predictionData={predictionData} /> */}
          
          {/* ========================================================================= */}
          {/* 🎯 RATINGS UNIVERSE: Every System's Take */}
          {/* ========================================================================= */}
          
          {/* Comprehensive Ratings - FPI, SP+, SRS, etc */}
          <ComprehensiveRatingsComparison predictionData={predictionData} />
          
          {/* 167-Metric Power Rankings Dashboard */}
          <ComprehensiveMetricsDashboard 
            predictionData={predictionData} 
            powerRankingsData={powerRankingsData}
          />
          
          {/* ========================================================================= */}
          {/* 💸 ARBITRAGE: Advanced Betting Strategies */}
          {/* ========================================================================= */}
          
          {/* Arbitrage Intelligence - Profit opportunities */}
          <ArbitrageOpportunities predictionData={predictionData} />
          
          {/* Arbitrage Calculator - Calculate optimal stakes */}
          <ArbitrageCalculator predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 📖 REFERENCE: Terms & Definitions */}
          {/* ========================================================================= */}
          
          {/* Glossary - What does EPA mean? What's success rate? */}
          <Glossary predictionData={predictionData} />
          
          {/* Footer */}
          <div className="text-center text-slate-400 text-sm py-8">
            <div className="bg-slate-900/60 backdrop-blur-sm border border-white/10 rounded-lg p-4 shadow-lg">
              <p>Analytics Dashboard • Data-Driven Predictions • For Educational Purposes Only</p>
            </div>
          </div>
          
          </div>
        </div>
      </div>
    </div>
  );
}