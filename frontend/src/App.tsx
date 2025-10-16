import { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import { CONFIG } from './config';
import { TeamSelector } from './components/figma/TeamSelector';
import { Header } from './components/figma/Header';
import { PredictionCards } from './components/figma/PredictionCards';
import { ConfidenceSection } from './components/figma/ConfidenceSection';
import { MarketComparison } from './components/figma/MarketComparison';
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

export default function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [predictionData, setPredictionData] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (homeTeam: string, awayTeam: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
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
      // Pass the complete data structure including formatted_analysis
      setPredictionData(data.ui_components ? { ...data.ui_components, formatted_analysis: data.formatted_analysis } : data);
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
        {/* Clean Dark Gradient Background */}
        <div className="absolute inset-0" style={{
          background: 'linear-gradient(90deg, hsla(240, 5%, 10%, 1) 0%, hsla(240, 5%, 15%, 1) 50%, hsla(240, 5%, 8%, 1) 100%)'
        }}></div>
        
        {/* Content */}
        <div className="relative z-10 p-4 md:p-8 lg:p-12 text-white">
          <div className="max-w-[1600px] mx-auto space-y-6">
          
          {/* Modern Header */}
          <div className="relative text-center mb-12">
            {/* Theme Toggle - Top Right */}
            <div className="absolute top-0 right-0">
              <button 
                onClick={() => setDarkMode(!darkMode)}
                className="p-4 bg-slate-900/70 backdrop-blur-xl border border-white/20 hover:border-white/40 rounded-xl transition-all duration-300 hover:scale-105 hover:bg-slate-800/80 shadow-lg hover:shadow-xl"
                aria-label="Toggle theme"
              >
                {darkMode ? (
                  <Sun className="h-6 w-6 text-yellow-400 drop-shadow-sm" />
                ) : (
                  <Moon className="h-6 w-6 text-slate-300 drop-shadow-sm" />
                )}
              </button>
            </div>

            {/* Main Title */}
            <h1 className="text-5xl md:text-7xl font-bold mb-4">
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
          
          {/* Header */}
          <Header predictionData={predictionData} isLoading={isLoading} />
          
          {/* 🎯 SECTION 1: CORE PREDICTIONS */}
          {/* Prediction Cards - Main Results */}
          <PredictionCards predictionData={predictionData} isLoading={isLoading} error={error || undefined} />
          
          {/* Final Prediction Summary - Move up for immediate visibility */}
          <FinalPredictionSummary predictionData={predictionData} />
          
          {/* 📈 MARKET ANALYSIS - RIGHT AFTER PREDICTIONS */}
          {/* Market Comparison - Sportsbook lines and value analysis */}
          <MarketComparison predictionData={predictionData} />
          
          {/* Confidence & Market - COMMENTED OUT FOR NOW */}
          {/* <ConfidenceSection predictionData={predictionData} isLoading={isLoading} error={error || undefined} /> */}
          
          {/* 🎲 PROBABILITY & PERFORMANCE */}
          {/* Win Probability - Standalone Section */}
          <WinProbability predictionData={predictionData} />
          
          {/* Situational Performance - Standalone Section */}
          <SituationalPerformance predictionData={predictionData} />
          
          {/* 🌤️ CONTEXTUAL FACTORS */}
          {/* Weather, Poll & Bye Week Analysis */}
          <ContextualAnalysis predictionData={predictionData} />
          
          {/* AP Poll Rankings */}
          <APPollRankings predictionData={predictionData} />
          
          {/* Media Information */}
          <MediaInformation predictionData={predictionData} />
          
          {/* 🏈 SECTION 3: ADVANCED ANALYTICS */}
          {/* EPA Comparison - Core advanced metric */}
          <EPAComparison predictionData={predictionData} />
          
          {/* Comprehensive Differential Analysis */}
          <DifferentialAnalysis predictionData={predictionData} />
          
          {/* Advanced Metrics */}
          <AdvancedMetrics predictionData={predictionData} />
          
          {/* Field Position Metrics */}
          <FieldPositionMetrics predictionData={predictionData} />
          
          {/* Drive Efficiency & Game Flow */}
          <DriveEfficiency predictionData={predictionData} />
          
          {/* Comprehensive Ratings Comparison - Advanced Rating Systems */}
          <ComprehensiveRatingsComparison predictionData={predictionData} />
          
          {/* 👥 SECTION 4: TEAM & PLAYER ANALYSIS */}
          {/* Key Player Impact */}
          <KeyPlayerImpact predictionData={predictionData} />
          
          {/* Comprehensive Team Statistics */}
          <ComprehensiveTeamStats predictionData={predictionData} />
          
          {/* Season Records */}
          <SeasonRecords predictionData={predictionData} />
          
          {/* Coaching Staff Comparison */}
          <CoachingComparison predictionData={predictionData} />
          
          {/* Extended Defensive Analytics & Season Summary */}
          <ExtendedDefensiveAnalytics predictionData={predictionData} />
          
          {/* 🔧 SECTION 5: MODEL TRANSPARENCY */}
          {/* Model Weights Breakdown */}
          <WeightsBreakdown predictionData={predictionData} />
          
          {/* Weighted Component Breakdown */}
          <ComponentBreakdown predictionData={predictionData} />
          
          {/* Glossary */}
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