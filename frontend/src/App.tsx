import { useState, useEffect, useRef } from 'react';
import { BarChart3, TrendingUp, Users } from 'lucide-react';
import { CONFIG } from './config';
import fbsData from './fbs.json';
import { EVPlusPage } from './components/figma/EVPlusPage';
import { CoachAnalysisPage } from './components/figma/CoachAnalysisPage';
import { TeamSelector } from './components/figma/TeamSelector';
import { Header } from './components/figma/Header';
import { PredictionResults } from './components/figma/PredictionResults';
import { PredictionCards } from './components/figma/PredictionCards';
import { PredictionLoader } from './components/figma/PredictionLoader';
import { ConfidenceSection } from './components/figma/ConfidenceSection';
import { CompactMarketAnalysis } from './components/figma/CompactMarketAnalysis';
import { ArbitrageOpportunities } from './components/figma/ArbitrageOpportunities';
import { ArbitrageCalculator } from './components/figma/ArbitrageCalculator';
import { MediaInformation } from './components/figma/MediaInformation';
import { EPAComparison } from './components/figma/EPAComparison';
import { DifferentialAnalysis } from './components/figma/DifferentialAnalysis';
import { WinProbability } from './components/figma/WinProbability';
import { SituationalPerformance } from './components/figma/SituationalPerformance';
import { FieldPositionMetrics } from './components/figma/FieldPositionMetrics';
import { AdvancedMetrics } from './components/figma/AdvancedMetrics';
import { WeightsBreakdown } from './components/figma/WeightsBreakdown';
import { ComponentBreakdown } from './components/figma/ComponentBreakdown';
import { ComprehensiveTeamStats } from './components/figma/ComprehensiveStats';
import { CoachingComparison } from './components/figma/CoachingComparison';
import CoachesComparison from './components/CoachesComparison';
import { DriveEfficiency } from './components/figma/DriveEfficiency';
import { DriveEfficiencyGameFlow } from './components/figma/DriveEfficiencyGameFlow';
import { ExtendedDefensiveAnalytics } from './components/figma/ExtendedDefensiveAnalytics';
import ComprehensiveRatingsComparison from './components/figma/ComprehensiveRatingsComparison';
import { SeasonRecords } from './components/figma/SeasonRecords';
import { FinalPredictionSummary } from './components/figma/FinalPredictionSummary';
import { GameSummaryRationale } from './components/figma/GameSummaryRationale';
import { Glossary } from './components/figma/Glossary';
import { EnhancedTeamStats } from './components/figma/EnhancedTeamStats';
import LiveGameBadge from './components/figma/LiveGameBadge';
import FieldVisualization from './components/figma/FieldVisualization';
import WinProbabilityLive from './components/figma/WinProbabilityLive';
import LivePlaysFeed from './components/figma/LivePlaysFeed';
import ComprehensiveMetricsDashboard from './components/figma/ComprehensiveMetricsDashboard';
import { PlayerPropsPanel } from './components/figma/PlayerPropsPanel';
import { CommonOpponents } from './components/figma/CommonOpponents';
import { KeyPlayerImpact } from './components/figma/KeyPlayerImpact';

interface Team {
  id: number;
  school: string;
  mascot: string;
  abbreviation: string;
  conference: string;
  primary_color: string;
  alt_color: string;
  logos: string[];
}

const teams: Team[] = fbsData as Team[];

export default function App() {
  const [currentPage, setCurrentPage] = useState<'main' | 'evplus' | 'coach'>('main');
  const [predictionData, setPredictionData] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [liveData, setLiveData] = useState<any | null>(null);
  const [replayMode, setReplayMode] = useState<boolean>(false);
  const [replayPlayIndex, setReplayPlayIndex] = useState<number>(0);
  const [replayQuarter, setReplayQuarter] = useState<number>(0); // 0 = all quarters
  const [replaySpeed, setReplaySpeed] = useState<number>(1); // 1x, 2x, 4x
  const [selectedTeams, setSelectedTeams] = useState<{ home: string; away: string } | null>(null);
  const [currentMatchup, setCurrentMatchup] = useState<{ home: string; away: string } | null>(null);
  const [insightMode, setInsightMode] = useState(false);
  const [batchMode, setBatchMode] = useState(false);
  const [batchPredictions, setBatchPredictions] = useState<any[]>([]);
  const [batchLoading, setBatchLoading] = useState(false);
  const intervalRef = useRef<number | null>(null);
  const gameSummaryRef = useRef<HTMLDivElement | null>(null);
  
  // Fetch live game data from ESPN API
  const fetchLiveData = async (homeTeam: string, awayTeam: string) => {
    try {
      const response = await fetch(
        `${CONFIG.API.BASE_URL}/api/live-game?home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`
      );
      
      if (!response.ok) {
        console.error('Live data fetch failed');
        setLiveData(null);
        return;
      }
      
      const data = await response.json();
      
      // Set live data for both live and finished games (for replay functionality)
      if (data.game_info?.is_live || data.game_info?.status === 'final' || data.game_info?.status === 'post') {
        console.log('Game data received:', data);
        setLiveData(data);
      } else {
        console.log('Game not available');
        setLiveData(null);
      }
    } catch (error) {
      console.error('Error fetching live data:', error);
      setLiveData(null);
    }
  };
  
  // Auto-refresh effect for live data
  useEffect(() => {
    // Clear any existing interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    // Only start polling if we have teams selected
    if (selectedTeams) {
      // Initial fetch
      fetchLiveData(selectedTeams.home, selectedTeams.away);
      
      // Set up polling every 15 seconds for live games
      intervalRef.current = window.setInterval(() => {
        fetchLiveData(selectedTeams.home, selectedTeams.away);
      }, 15000);
    }
    
    // Cleanup on unmount or when teams change
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [selectedTeams]);

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

  const handleQuickInsight = async () => {
    // Check if we already have prediction data for the current matchup
    const hasMatchingPrediction = predictionData && 
                                   selectedTeams?.home === currentMatchup?.home && 
                                   selectedTeams?.away === currentMatchup?.away;
    
    // Only run prediction if we don't have data for current matchup
    if (!hasMatchingPrediction && currentMatchup) {
      await handlePrediction(currentMatchup.home, currentMatchup.away);
    }
    
    // Enable insight mode to show only the Game Summary & Rationale
    setInsightMode(true);
  };

  const handleBatchPredictions = async () => {
    setBatchLoading(true);
    setBatchMode(true);
    setInsightMode(false);
    
    try {
      // Fetch current week games
      const gamesResponse = await fetch('/Currentweekgames.json');
      const gamesData = await gamesResponse.json();
      const games = gamesData.games?.all || [];
      
      // Limit to top 10 games to avoid overwhelming the system
      const gamesToPredict = games.slice(0, 10);
      
      const predictions = [];
      
      for (const game of gamesToPredict) {
        try {
          const response = await fetch(`${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              home_team: game.homeTeam.name,
              away_team: game.awayTeam.name
            })
          });
          
          if (response.ok) {
            const data = await response.json();
            predictions.push({
              homeTeam: game.homeTeam.name,
              awayTeam: game.awayTeam.name,
              data: data.ui_components ? { 
                ...data.ui_components, 
                formatted_analysis: data.formatted_analysis,
                rivalry_history: data.rivalry_history 
              } : data
            });
          }
        } catch (err) {
          console.error(`Failed to predict ${game.awayTeam.name} @ ${game.homeTeam.name}:`, err);
        }
      }
      
      setBatchPredictions(predictions);
    } catch (error) {
      console.error('Batch prediction error:', error);
    } finally {
      setBatchLoading(false);
    }
  };

  // Handle page navigation
  if (currentPage === 'evplus') {
    return <EVPlusPage onBack={() => setCurrentPage('main')} />;
  }

  if (currentPage === 'coach') {
    return <CoachAnalysisPage onBack={() => setCurrentPage('main')} />;
  }

  return (
    <div className="dark">
      {/* Modern Team Logos Loading Animation */}
      {isLoading && selectedTeams && (
        <PredictionLoader
          awayTeam={{
            name: selectedTeams.away,
            logo: teams.find(t => t.school === selectedTeams.away)?.logos[1] || '',
            color: teams.find(t => t.school === selectedTeams.away)?.primary_color || '#3b82f6'
          }}
          homeTeam={{
            name: selectedTeams.home,
            logo: teams.find(t => t.school === selectedTeams.home)?.logos[1] || '',
            color: teams.find(t => t.school === selectedTeams.home)?.primary_color || '#8b5cf6'
          }}
        />
      )}

      {/* Modern Textured Background - Exact Mirror of week14.html */}
      <div className="min-h-screen relative overflow-hidden" style={{
        background: `
          linear-gradient(135deg, #050506 0%, #0a0a0b 25%, #060607 50%, #080809 75%, #050506 100%),
          radial-gradient(ellipse at top left, rgba(12, 12, 14, 0.3), transparent 50%),
          radial-gradient(ellipse at bottom right, rgba(10, 10, 12, 0.3), transparent 50%),
          linear-gradient(180deg, #070708 0%, #030304 100%)
        `,
        WebkitFontSmoothing: 'antialiased',
        MozOsxFontSmoothing: 'grayscale',
        textRendering: 'optimizeLegibility'
      }}>
        
        {/* Layered Texture Pattern - Exact from week14.html body::before */}
        <div className="absolute inset-0 pointer-events-none" style={{
          backgroundImage: `
            repeating-linear-gradient(0deg, transparent, transparent 0.5px, rgba(255, 255, 255, 0.025) 0.5px, rgba(255, 255, 255, 0.025) 1px),
            repeating-linear-gradient(90deg, transparent, transparent 0.5px, rgba(255, 255, 255, 0.025) 0.5px, rgba(255, 255, 255, 0.025) 1px),
            repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.02) 0px, rgba(255, 255, 255, 0.02) 0.5px, transparent 0.5px, transparent 4px),
            repeating-linear-gradient(-45deg, rgba(255, 255, 255, 0.02) 0px, rgba(255, 255, 255, 0.02) 0.5px, transparent 0.5px, transparent 4px),
            repeating-linear-gradient(30deg, rgba(204, 0, 28, 0.035) 0px, rgba(204, 0, 28, 0.035) 1px, transparent 1px, transparent 16px),
            repeating-linear-gradient(-30deg, rgba(161, 0, 20, 0.035) 0px, rgba(161, 0, 20, 0.035) 1px, transparent 1px, transparent 16px),
            radial-gradient(ellipse at 25% 15%, rgba(204, 0, 28, 0.12) 0%, rgba(161, 0, 20, 0.08) 30%, transparent 60%),
            radial-gradient(ellipse at 75% 85%, rgba(115, 0, 13, 0.12) 0%, rgba(161, 0, 20, 0.08) 30%, transparent 60%),
            radial-gradient(circle at 50% 30%, rgba(255, 255, 255, 0.06) 0%, transparent 35%),
            radial-gradient(circle at 80% 70%, rgba(204, 0, 28, 0.06) 0%, transparent 25%)
          `,
          backgroundSize: '1px 1px, 1px 1px, 4px 4px, 4px 4px, 16px 16px, 16px 16px, 800px 800px, 700px 700px, 400px 400px, 300px 300px',
          zIndex: 0,
          opacity: 1
        }}></div>
        
        {/* Lighting Effects - Uniform darkness */}
        <div className="absolute inset-0 pointer-events-none" style={{
          background: `
            linear-gradient(180deg, transparent 0%, transparent 75%, rgba(0, 0, 0, 0.25) 100%),
            linear-gradient(135deg, transparent 0%, transparent 70%, rgba(0, 0, 0, 0.08) 100%),
            radial-gradient(ellipse at 80% 80%, rgba(0, 0, 0, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, transparent 0%, rgba(0, 0, 0, 0.18) 100%)
          `,
          zIndex: 0
        }}></div>
        
        {/* Content */}
        <div className="relative z-10 px-3 py-4 sm:px-4 sm:py-6 md:p-8 lg:p-12 text-white">
          <div className="max-w-[1600px] mx-auto space-y-4 sm:space-y-6">
          
          {/* Modern Header */}
          <div className="relative text-center mb-8 sm:mb-12">
            {/* Theme Toggle & Week 14 Recap - Top Right */}
            <div className="absolute top-0 right-0 flex items-center gap-2">
              {/* Week 14 Recap Button */}
              <a
                href="/week14.html"
                target="_blank"
                rel="noopener noreferrer"
                className="group p-2 sm:p-3 md:p-4 backdrop-blur-sm backdrop-blur-xl border border-red-500/30 hover:border-red-500/50 rounded-lg sm:rounded-xl transition-all duration-300 hover:scale-105 hover:bg-red-900/30 shadow-lg hover:shadow-xl"
                aria-label="Week 14 Recap"
              >
                <svg 
                  className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-red-400 group-hover:text-red-300 transition-colors duration-300" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </a>
              
              {/* EV+ Button */}
              <button 
                onClick={() => setCurrentPage('evplus')}
                className="p-2 sm:p-3 md:p-4 backdrop-blur-sm backdrop-blur-xl border border-white/20 hover:border-green-400/40 rounded-lg sm:rounded-xl transition-all duration-300 hover:scale-105 hover:bg-green-500/10 shadow-lg hover:shadow-xl"
                aria-label="EV+ Betting Tools"
                title="EV+ Betting Tools"
              >
                <TrendingUp className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-green-400 drop-shadow-sm" />
              </button>

              {/* Coach Analysis Button */}
              <button 
                onClick={() => setCurrentPage('coach')}
                className="p-2 sm:p-3 md:p-4 backdrop-blur-sm backdrop-blur-xl border border-white/20 hover:border-blue-400/40 rounded-lg sm:rounded-xl transition-all duration-300 hover:scale-105 hover:bg-blue-500/10 shadow-lg hover:shadow-xl"
                aria-label="Coach Analysis"
                title="Coach Analysis"
              >
                <Users className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-blue-400 drop-shadow-sm" />
              </button>

              {/* CFP Charts Button */}
              <a
                href="/CoolerVisuals.html"
                target="_blank"
                rel="noopener noreferrer"
                className="group p-2 sm:p-3 md:p-4 backdrop-blur-sm backdrop-blur-xl border border-yellow-500/30 hover:border-yellow-500/50 rounded-lg sm:rounded-xl transition-all duration-300 hover:scale-105 hover:bg-yellow-900/30 shadow-lg hover:shadow-xl"
                aria-label="CFP Charts"
                title="CFP Charts & Metrics Dashboard"
              >
                <img 
                  src="/CFP.png" 
                  alt="CFP" 
                  className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 object-contain group-hover:scale-110 transition-transform duration-300"
                />
              </a>
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
                <span className="text-slate-300 backdrop-blur-sm backdrop-blur-sm border border-white/20 px-4 py-2 rounded-full shadow-lg">
                  v 0.2.1
                </span>
                <div className="flex items-center gap-3 text-slate-300 backdrop-blur-sm backdrop-blur-sm border border-emerald-500/30 px-4 py-2 rounded-full shadow-lg">
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

          {/* ========================================================================= */}
          {/* 🎯 TIER 1: HERO & INSTANT DECISION (0-30 seconds) */}
          {/* First impression - what bettors need immediately */}
          {/* ========================================================================= */}
          
          {/* 1-2. Team Selector - Select matchup */}
          <TeamSelector 
            onPrediction={handlePrediction}
            isLoading={isLoading}
            onQuickInsight={handleQuickInsight}
            onMatchupChange={(away, home) => {
              setCurrentMatchup({ home: home.school, away: away.school });
            }}
          />
          
          {/* Batch Predictions Button */}
          <div className="mb-6 flex justify-center">
            <button
              onClick={handleBatchPredictions}
              disabled={batchLoading}
              className="group relative overflow-hidden rounded-xl shadow-lg hover:shadow-xl 
                       transform hover:scale-[1.02] transition-all duration-300 ease-out
                       disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                background: `linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15))`,
                border: `1px solid rgba(59, 130, 246, 0.3)`,
              }}
            >
              <div className="relative px-8 py-3 flex items-center justify-center gap-2">
                <BarChart3 
                  className="w-5 h-5 text-blue-400 group-hover:text-blue-300 transition-colors duration-300" 
                  strokeWidth={2}
                />
                <span className="text-base font-semibold text-blue-100 group-hover:text-white transition-colors duration-300">
                  {batchLoading ? 'Loading All Predictions...' : 'Get All Predictions'}
                </span>
              </div>
              <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
            </button>
          </div>
          
          {/* Batch Predictions Mode - Show all game insights */}
          {batchMode && batchPredictions.length > 0 ? (
            <>
              {/* Exit Batch Mode Button */}
              <div className="mb-6 flex justify-center">
                <button
                  onClick={() => {
                    setBatchMode(false);
                    setBatchPredictions([]);
                  }}
                  className="px-6 py-3 bg-gradient-to-r from-blue-500/20 to-purple-500/20 
                           hover:from-blue-500/30 hover:to-purple-500/30
                           border border-blue-400/30 hover:border-blue-400/50
                           rounded-xl text-white font-semibold transition-all duration-300
                           shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
                >
                  ← Back to Single Game
                </button>
              </div>
              
              {/* Display all predictions */}
              <div className="space-y-8">
                {batchPredictions.map((prediction, index) => (
                  <div key={index}>
                    <h2 className="text-2xl font-bold text-white mb-4 text-center">
                      {prediction.awayTeam} @ {prediction.homeTeam}
                    </h2>
                    <GameSummaryRationale predictionData={prediction.data} />
                  </div>
                ))}
              </div>
            </>
          ) : insightMode && predictionData ? (
            <>
              {/* Exit Insight Mode Button */}
              <div className="mb-6 flex justify-center">
                <button
                  onClick={() => setInsightMode(false)}
                  className="px-6 py-3 bg-gradient-to-r from-purple-500/20 to-blue-500/20 
                           hover:from-purple-500/30 hover:to-blue-500/30
                           border border-purple-400/30 hover:border-purple-400/50
                           rounded-xl text-white font-semibold transition-all duration-300
                           shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
                >
                  ← Back to Full Analysis
                </button>
              </div>
              
              <GameSummaryRationale predictionData={predictionData} />
            </>
          ) : (
            <>
              {/* 3-6. Header - Selected Teams, Game Details, Rivalry Banner */}
              <Header predictionData={predictionData} isLoading={isLoading} />
              
              {/* Rivalry History - Shows if this is a rivalry game */}
              {predictionData?.rivalry_history && (
                <>
  
                </>
              )}
              
              {/* 7-11. Win Probability, Final Score, Confidence, Spread vs Market, Recommended Bets */}
              <PredictionCards predictionData={predictionData} isLoading={isLoading} error={error || undefined} />
          
          {/* ============================================================================================================= */}
          {/* 🔴 LIVE GAME SECTION - Only shows when game is in progress */}
          {/* Shows real-time field position, score, and plays right after win probability */}
          {/* ============================================================================================================= */}
          
          {liveData && (liveData.game_info?.is_live || replayMode || liveData.game_info?.status === 'post' || liveData.game_info?.status === 'final') && (
            <>
              {/* Show Start Replay button for finished games */}
              {!replayMode && !liveData.game_info?.is_live && (liveData.game_info?.status === 'final' || liveData.game_info?.status === 'post') && (
                <div style={{
                  background: 'rgba(15, 23, 42, 0.4)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  padding: '28px',
                  marginBottom: '24px',
                  border: '1px solid rgba(148, 163, 184, 0.2)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05) inset',
                  textAlign: 'center'
                }}>
                  <div style={{ marginBottom: '20px' }}>
                    <h3 style={{ margin: '0 0 10px 0', fontSize: '20px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.95)', letterSpacing: '-0.01em' }}>
                      Game Complete
                    </h3>
                    <p style={{ margin: 0, fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)', fontWeight: 400 }}>
                      Review all {liveData.plays?.length || 0} plays with interactive field visualization
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      setReplayMode(true);
                      setReplayPlayIndex(0);
                      setReplayQuarter(0);
                    }}
                    style={{
                      background: 'rgba(59, 130, 246, 0.15)',
                      border: '1px solid rgba(59, 130, 246, 0.3)',
                      borderRadius: '12px',
                      padding: '14px 32px',
                      color: 'rgba(255, 255, 255, 0.95)',
                      cursor: 'pointer',
                      fontSize: '15px',
                      fontWeight: 600,
                      boxShadow: '0 4px 16px rgba(59, 130, 246, 0.2)',
                      transition: 'all 0.2s ease',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '10px'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(59, 130, 246, 0.25)';
                      e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.boxShadow = '0 6px 24px rgba(59, 130, 246, 0.3)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(59, 130, 246, 0.15)';
                      e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = '0 4px 16px rgba(59, 130, 246, 0.2)';
                    }}
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    Start Game Replay
                  </button>
                </div>
              )}
              
              {!replayMode && liveData.game_info?.is_live && (
                <LiveGameBadge 
                  period={liveData.game_state.period}
                  clock={liveData.game_state.clock}
                />
              )}
              
              {replayMode && (
                <div style={{
                  background: 'rgba(15, 23, 42, 0.4)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  padding: '24px',
                  marginBottom: '24px',
                  border: '1px solid rgba(148, 163, 184, 0.2)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05) inset'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
                    <h3 style={{ margin: 0, fontSize: '18px', fontWeight: 600, color: 'rgba(255, 255, 255, 0.95)', letterSpacing: '-0.01em' }}>
                      Game Replay
                    </h3>
                    <button
                      onClick={() => {
                        setReplayMode(false);
                        setReplayPlayIndex(0);
                        setReplayQuarter(0);
                      }}
                      style={{
                        background: 'rgba(239, 68, 68, 0.15)',
                        border: '1px solid rgba(239, 68, 68, 0.3)',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        color: 'rgba(255, 255, 255, 0.9)',
                        cursor: 'pointer',
                        fontSize: '13px',
                        fontWeight: 600,
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(239, 68, 68, 0.25)';
                        e.currentTarget.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(239, 68, 68, 0.15)';
                        e.currentTarget.style.borderColor = 'rgba(239, 68, 68, 0.3)';
                      }}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                      Exit
                    </button>
                  </div>
                  
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '20px' }}>
                    <div style={{ flex: 1, minWidth: '200px' }}>
                      <label style={{ display: 'block', fontSize: '11px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                        Quarter
                      </label>
                      <select
                        value={replayQuarter}
                        onChange={(e) => {
                          setReplayQuarter(parseInt(e.target.value));
                          setReplayPlayIndex(0);
                        }}
                        style={{
                          width: '100%',
                          background: 'rgba(15, 23, 42, 0.6)',
                          border: '1px solid rgba(148, 163, 184, 0.2)',
                          borderRadius: '10px',
                          padding: '12px 14px',
                          color: 'rgba(255, 255, 255, 0.95)',
                          fontSize: '14px',
                          fontWeight: 500,
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          outline: 'none'
                        }}
                        onFocus={(e) => {
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                          e.currentTarget.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                        }}
                        onBlur={(e) => {
                          e.currentTarget.style.borderColor = 'rgba(148, 163, 184, 0.2)';
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                      >
                        <option value={0}>All Quarters</option>
                        <option value={1}>1st Quarter</option>
                        <option value={2}>2nd Quarter</option>
                        <option value={3}>3rd Quarter</option>
                        <option value={4}>4th Quarter</option>
                      </select>
                    </div>
                    
                    <div style={{ flex: 1, minWidth: '200px' }}>
                      <label style={{ display: 'block', fontSize: '11px', color: 'rgba(255, 255, 255, 0.6)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                        Speed
                      </label>
                      <select
                        value={replaySpeed}
                        onChange={(e) => setReplaySpeed(parseFloat(e.target.value))}
                        style={{
                          width: '100%',
                          background: 'rgba(15, 23, 42, 0.6)',
                          border: '1px solid rgba(148, 163, 184, 0.2)',
                          borderRadius: '10px',
                          padding: '12px 14px',
                          color: 'rgba(255, 255, 255, 0.95)',
                          fontSize: '14px',
                          fontWeight: 500,
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          outline: 'none'
                        }}
                        onFocus={(e) => {
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                          e.currentTarget.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                        }}
                        onBlur={(e) => {
                          e.currentTarget.style.borderColor = 'rgba(148, 163, 184, 0.2)';
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                      >
                        <option value={0.5}>0.5x</option>
                        <option value={1}>1.0x</option>
                        <option value={2}>2.0x</option>
                        <option value={4}>4.0x</option>
                      </select>
                    </div>
                  </div>
                  
                  <div style={{ 
                    display: 'flex', 
                    gap: '12px', 
                    alignItems: 'center',
                    background: 'rgba(15, 23, 42, 0.4)',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid rgba(148, 163, 184, 0.15)'
                  }}>
                    <button
                      onClick={() => setReplayPlayIndex(Math.max(0, replayPlayIndex - 1))}
                      disabled={replayPlayIndex === 0}
                      style={{
                        background: replayPlayIndex === 0 ? 'rgba(148, 163, 184, 0.1)' : 'rgba(59, 130, 246, 0.15)',
                        border: `1px solid ${replayPlayIndex === 0 ? 'rgba(148, 163, 184, 0.2)' : 'rgba(59, 130, 246, 0.3)'}`,
                        borderRadius: '10px',
                        padding: '12px 18px',
                        color: replayPlayIndex === 0 ? 'rgba(255, 255, 255, 0.4)' : 'rgba(255, 255, 255, 0.9)',
                        cursor: replayPlayIndex === 0 ? 'not-allowed' : 'pointer',
                        fontSize: '14px',
                        fontWeight: 600,
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                      onMouseEnter={(e) => {
                        if (replayPlayIndex !== 0) {
                          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.25)';
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (replayPlayIndex !== 0) {
                          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.15)';
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                        }
                      }}
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <polygon points="19 20 9 12 19 4 19 20"></polygon>
                        <line x1="5" y1="19" x2="5" y2="5"></line>
                      </svg>
                      Previous
                    </button>
                    
                    <div style={{
                      flex: 1,
                      textAlign: 'center',
                      fontSize: '14px',
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 600,
                      background: 'rgba(59, 130, 246, 0.1)',
                      padding: '12px 20px',
                      borderRadius: '10px',
                      border: '1px solid rgba(59, 130, 246, 0.2)'
                    }}>
                      Play {replayPlayIndex + 1} of {(() => {
                        if (!liveData?.plays) return 0;
                        if (replayQuarter === 0) return liveData.plays.length;
                        return liveData.plays.filter((p: any) => p.period === replayQuarter).length;
                      })()}
                    </div>
                    
                    <button
                      onClick={() => {
                        const maxPlays = (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length;
                        })();
                        setReplayPlayIndex(Math.min(maxPlays - 1, replayPlayIndex + 1));
                      }}
                      disabled={!liveData?.plays || replayPlayIndex >= (() => {
                        if (!liveData?.plays) return 0;
                        if (replayQuarter === 0) return liveData.plays.length - 1;
                        return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                      })()}
                      style={{
                        background: (!liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })()) ? 'rgba(148, 163, 184, 0.1)' : 'rgba(59, 130, 246, 0.15)',
                        border: `1px solid ${(!liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })()) ? 'rgba(148, 163, 184, 0.2)' : 'rgba(59, 130, 246, 0.3)'}`,
                        borderRadius: '10px',
                        padding: '12px 18px',
                        color: (!liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })()) ? 'rgba(255, 255, 255, 0.4)' : 'rgba(255, 255, 255, 0.9)',
                        cursor: (!liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })()) ? 'not-allowed' : 'pointer',
                        fontSize: '14px',
                        fontWeight: 600,
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}
                      onMouseEnter={(e) => {
                        const isDisabled = !liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })();
                        if (!isDisabled) {
                          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.25)';
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                        }
                      }}
                      onMouseLeave={(e) => {
                        const isDisabled = !liveData?.plays || replayPlayIndex >= (() => {
                          if (!liveData?.plays) return 0;
                          if (replayQuarter === 0) return liveData.plays.length - 1;
                          return liveData.plays.filter((p: any) => p.period === replayQuarter).length - 1;
                        })();
                        if (!isDisabled) {
                          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.15)';
                          e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                        }
                      }}
                    >
                      Next
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <polygon points="5 4 15 12 5 20 5 4"></polygon>
                        <line x1="19" y1="5" x2="19" y2="19"></line>
                      </svg>
                    </button>
                  </div>
                </div>
              )}
              
              <FieldVisualization
                possession={{
                  team: (() => {
                    if (replayMode && liveData?.plays?.length) {
                      const filteredPlays = replayQuarter === 0
                        ? liveData.plays 
                        : liveData.plays.filter((p: any) => p.period === replayQuarter);
                      const currentPlay = filteredPlays[replayPlayIndex];
                      return currentPlay?.offense === 'home' ? liveData.game_info.home_team : liveData.game_info.away_team;
                    }
                    return liveData.game_state.possession === 'home'
                      ? liveData.game_info.home_team 
                      : liveData.game_info.away_team;
                  })(),
                  logo: (() => {
                    if (replayMode && liveData?.plays?.length) {
                      const filteredPlays = replayQuarter === 0
                        ? liveData.plays 
                        : liveData.plays.filter((p: any) => p.period === replayQuarter);
                      const currentPlay = filteredPlays[replayPlayIndex];
                      return currentPlay?.offense === 'home' ? liveData.game_info.home_logo : liveData.game_info.away_logo;
                    }
                    return liveData.game_state.possession === 'home'
                      ? liveData.game_info.home_logo
                      : liveData.game_info.away_logo;
                  })()
                }}
                fieldPosition={{
                  yardLine: (() => {
                    if (replayMode && liveData?.plays?.length) {
                      const filteredPlays = replayQuarter === 0
                        ? liveData.plays 
                        : liveData.plays.filter((p: any) => p.period === replayQuarter);
                      const currentPlay = filteredPlays[replayPlayIndex];
                      return currentPlay?.yard_line || 50;
                    }
                    return liveData.field_position?.yard_line || 50;
                  })(),
                  down: (() => {
                    if (replayMode && liveData?.plays?.length) {
                      const filteredPlays = replayQuarter === 0
                        ? liveData.plays 
                        : liveData.plays.filter((p: any) => p.period === replayQuarter);
                      const currentPlay = filteredPlays[replayPlayIndex];
                      return currentPlay?.down || 1;
                    }
                    return liveData.field_position?.down || 1;
                  })(),
                  distance: (() => {
                    if (replayMode && liveData?.plays?.length) {
                      const filteredPlays = replayQuarter === 0
                        ? liveData.plays 
                        : liveData.plays.filter((p: any) => p.period === replayQuarter);
                      const currentPlay = filteredPlays[replayPlayIndex];
                      return currentPlay?.distance || 10;
                    }
                    return liveData.field_position?.distance || 10;
                  })()
                }}
                playData={(() => {
                  if (replayMode && liveData?.plays?.length) {
                    const filteredPlays = replayQuarter === 0
                      ? liveData.plays 
                      : liveData.plays.filter((p: any) => p.period === replayQuarter);
                    const currentPlay = filteredPlays[replayPlayIndex];
                    const prevPlay = replayPlayIndex > 0 ? filteredPlays[replayPlayIndex - 1] : null;
                    return {
                      play_type: currentPlay?.play_type,
                      yards_gained: currentPlay?.yards_gained,
                      start_yard_line: prevPlay?.yard_line || currentPlay?.yard_line,
                      end_yard_line: currentPlay?.yard_line
                    };
                  }
                  return undefined;
                })()}
                homeTeam={{
                  name: liveData.game_info.home_team,
                  abbr: liveData.game_info.home_abbr,
                  color: liveData.game_info.home_color || '#1a7a42',
                  logo: liveData.game_info.home_logo
                }}
                awayTeam={{
                  name: liveData.game_info.away_team,
                  abbr: liveData.game_info.away_abbr,
                  color: liveData.game_info.away_color || '#0d5c2f',
                  logo: liveData.game_info.away_logo
                }}
                situation={liveData.game_state.situation}
              />              <WinProbabilityLive
                liveData={liveData}
                predictionData={predictionData}
              />
              
              <LivePlaysFeed
                plays={(() => {
                  if (replayMode && liveData?.plays?.length) {
                    const filteredPlays = replayQuarter === 0 
                      ? liveData.plays 
                      : liveData.plays.filter((p: any) => p.period === replayQuarter);
                    return filteredPlays;
                  }
                  return liveData.recent_plays || liveData.plays || [];
                })()}
                showEPA={true}
                predictionData={predictionData}
              />
            </>
          )}
          
          {/* Final Summary with Predicted Score & Key Factors */}
          <FinalPredictionSummary predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 📊 TIER 2: CRITICAL BETTING INTEL (30 sec - 2 min) */}
          {/* Core data that influences betting decisions */}
          {/* ========================================================================= */}
          
          {/* 12-15. Compact Market Analysis (ATS Performance, Market Comparison, Line Movement) */}
          <CompactMarketAnalysis predictionData={predictionData} />
          
          {/* 16. Elite vs Ranked Performance (Coaching Comparison) */}
          <CoachingComparison predictionData={predictionData} />
          
          {/* 16b. Comprehensive Coaches Head-to-Head Analysis */}
          <CoachesComparison predictionData={predictionData} />
          
          {/* 17. Key Player Impact Analysis */}
          <KeyPlayerImpact predictionData={predictionData} />
          
          {/* 18. Player Props (Top 8-10 opportunities) - HIDDEN */}
          {/* <PlayerPropsPanel predictionData={predictionData} /> */}
          
          {/* ========================================================================= */}
          {/* 🧠 TIER 3: ADVANCED ANALYTICS (2-5 minutes) */}
          {/* Deep performance analysis for serious bettors */}
          {/* ========================================================================= */}
          
          {/* 19. EPA Comparison */}
          <EPAComparison predictionData={predictionData} />
          
          {/* 21. Comprehensive Differential Analysis */}
          <DifferentialAnalysis predictionData={predictionData} />
          
          {/* 22-23. Advanced Offensive Metrics & Situational Performance */}
          <AdvancedMetrics predictionData={predictionData} />
          
          {/* 24. Situational Performance */}
          <SituationalPerformance predictionData={predictionData} />
          
          {/* 25. Field Position Metrics */}
          <FieldPositionMetrics predictionData={predictionData} />
          
          {/* 26. Drive Efficiency & Game Flow Analytics (Combined) */}
          <DriveEfficiencyGameFlow predictionData={predictionData} />
          
          {/* 27-28. Defensive Statistics & Game Control Metrics */}
          <ExtendedDefensiveAnalytics predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 📈 TIER 4: CONTEXTUAL BACKGROUND (5+ minutes) */}
          {/* Historical and seasonal context */}
          {/* ========================================================================= */}
          
          {/* 29. 2025 Season Records */}
          <SeasonRecords predictionData={predictionData} />
          
          {/* 30. Common Opponents Analysis - 2025 Season */}
          <CommonOpponents predictionData={predictionData} />
          
          {/* 31. Extended Team Statistics */}
          <ComprehensiveTeamStats predictionData={predictionData} />
          
          {/* Enhanced Team Stats */}
          <EnhancedTeamStats predictionData={predictionData} />
          
          {/* ========================================================================= */}
          {/* 📊 TIER 5: ADVANCED RATINGS & RANKINGS (Deep dive) */}
          {/* For analytics enthusiasts */}
          {/* ========================================================================= */}
          
          {/* 35-37. Team Ratings, Power Rankings, Match Quality */}
          <ComprehensiveRatingsComparison predictionData={predictionData} />
          
          {/* 167-Metric Power Rankings Dashboard */}
          <ComprehensiveMetricsDashboard 
            predictionData={predictionData} 

          />
          
          {/* ========================================================================= */}
          {/* 🛠️ TIER 6: SPECIALIZED TOOLS (Advanced users) */}
          {/* Professional betting tools */}
          {/* ========================================================================= */}
          
          {/* COMMENTED OUT: Arbitrage components - temporarily hidden */}
          {/* 38. Arbitrage Intelligence */}
          {/* <ArbitrageOpportunities predictionData={predictionData} /> */}
          
          {/* 40. Arbitrage Calculator */}
          {/* <ArbitrageCalculator predictionData={predictionData} /> */}

          {predictionData && (
            <PredictionResults 
              predictionData={predictionData}
            />
          )}
          
          {/* ========================================================================= */}
          {/* 📖 TIER 6 CONTINUED: REFERENCE - Terms & Definitions */}
          {/* ========================================================================= */}
          
          {/* 41. Metrics Glossary - Educational resource */}
          <Glossary predictionData={predictionData} />
            </>
          )}
          
          {/* ========================================================================= */}
          {/* 📱 FOOTER */}
          {/* ========================================================================= */}
          
          {/* Footer */}
          <div className="text-center text-slate-400 text-sm py-8">
            <div className="backdrop-blur-xl backdrop-blur-sm border border-white/10 rounded-lg p-4 shadow-lg">
              <p>Analytics Dashboard • Data-Driven Predictions • For Educational Purposes Only</p>
            </div>
          </div>
          
          </div>
        </div>
      </div>
    </div>
  );
}