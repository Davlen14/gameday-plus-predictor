import React, { useState, useEffect } from 'react';
import { Users, ArrowLeft, Trophy, TrendingUp, Target, Award, Home, Plane, Calendar, Star, BarChart3, Zap, Radar } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { CoachRadarChart } from './CoachRadarChart';
import { CoachSpiralTimeline } from './CoachSpiralTimeline';
import { CoachSunburst } from './CoachSunburst';
import laneKiffinData from '../../data/lane_kiffin_master.json';
import jamesFranklinData from '../../data/james_franklin_master.json';
import coachRankings from '../../data/coaches_advanced_rankings.json';

interface CoachAnalysisPageProps {
  onBack: () => void;
}

interface CoachData {
  metadata: any;
  current_team: {
    name: string;
    mascot: string;
    primary_color: string;
    alt_color: string;
    logo: string;
  };
  coach_info: {
    headshot_url: string;
  };
  schools_info: Array<{
    name: string;
    mascot: string;
    abbreviation: string;
    conference: string;
    primary_color: string;
    alt_color: string;
    logo: string;
    years: string;
    record: string;
  }>;
  summary: {
    career_record: string;
    career_win_pct: number;
    total_seasons: number;
    schools_coached: number;
    total_games: number;
  };
  career_stats: {
    by_school: any;
    splits: {
      home: string;
      away: string;
      neutral: string;
    };
    vs_ranked: {
      overall: string;
      vs_top5?: string;
      vs_top10?: string;
      vs_top_25?: string;
    };
  };
}

export const CoachAnalysisPage: React.FC<CoachAnalysisPageProps> = ({ onBack }) => {
  const [selectedView, setSelectedView] = useState<'overview' | 'kiffin' | 'franklin'>('overview');

  // Digital color coding for performance
  const getPerformanceColor = (winPct: number) => {
    if (winPct >= 65) return '#10b981'; // Digital green
    if (winPct >= 50) return '#f59e0b'; // Digital yellow
    return '#ef4444'; // Digital red
  };

  // Parse record and get color based on win percentage
  const getRecordColor = (record: string) => {
    const parts = record.split('-');
    if (parts.length >= 2) {
      const wins = parseInt(parts[0]);
      const losses = parseInt(parts[1]);
      const total = wins + losses;
      if (total > 0) {
        const winPct = (wins / total) * 100;
        return getPerformanceColor(winPct);
      }
    }
    return '#9ca3af'; // Gray for N/A
  };

  // Comparison Bar Component
  const ComparisonBar = ({ 
    label, 
    coach1Value, 
    coach2Value, 
    max, 
    inverse = false,
    coach1Color,
    coach2Color 
  }: { 
    label: string; 
    coach1Value: number; 
    coach2Value: number; 
    max: number; 
    inverse?: boolean;
    coach1Color: string;
    coach2Color: string;
  }) => {
    const coach1Pct = Math.min((coach1Value / max) * 100, 100);
    const coach2Pct = Math.min((coach2Value / max) * 100, 100);
    
    const winner = inverse ? 
      (coach1Value < coach2Value ? 'coach1' : 'coach2') :
      (coach1Value > coach2Value ? 'coach1' : 'coach2');
    
    return (
      <div className="mb-4">
        <div className="text-xs text-gray-400 mb-2 font-medium tracking-wide uppercase">{label}</div>
        <div className="flex items-center gap-4">
          <div className={`text-base font-light min-w-[60px] text-right ${winner === 'coach1' ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(5,150,105,0.6)]' : 'text-white'}`}>
            {coach1Value.toFixed(1)}
          </div>
          
          <div className="flex-1 flex gap-2">
            <div className="flex-1 bg-gray-800/30 rounded-full h-4 overflow-hidden relative">
              <div 
                className="h-full transition-all duration-1000"
                style={{
                  width: `${coach1Pct}%`,
                  background: winner === 'coach1' ? 'linear-gradient(90deg, #10b981, #34d399)' : `linear-gradient(90deg, ${coach1Color}, ${coach1Color}cc)`,
                  boxShadow: winner === 'coach1' ? '0 0 15px rgba(5,150,105,0.6)' : `0 0 10px ${coach1Color}40`
                }}
              />
            </div>
            <div className="flex-1 bg-gray-800/30 rounded-full h-4 overflow-hidden relative">
              <div 
                className="h-full transition-all duration-1000"
                style={{
                  width: `${coach2Pct}%`,
                  background: winner === 'coach2' ? 'linear-gradient(90deg, #10b981, #34d399)' : `linear-gradient(90deg, ${coach2Color}, ${coach2Color}cc)`,
                  boxShadow: winner === 'coach2' ? '0 0 15px rgba(5,150,105,0.6)' : `0 0 10px ${coach2Color}40`
                }}
              />
            </div>
          </div>
          
          <div className={`text-base font-light min-w-[60px] text-left ${winner === 'coach2' ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(5,150,105,0.6)]' : 'text-white'}`}>
            {coach2Value.toFixed(1)}
          </div>
        </div>
      </div>
    );
  };

  const CoachCard = ({ coachData }: { coachData: CoachData }) => {
    const team = coachData.current_team;
    const coach = coachData.metadata.coach;
    
    return (
      <div 
        className="relative backdrop-blur-2xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl bg-gradient-to-br from-white/[0.03] to-transparent hover:scale-[1.02] transition-all duration-500 cursor-pointer"
      >
        {/* Team Color Header Accent */}
        <div 
          className="absolute top-0 left-0 right-0 h-1"
          style={{ background: `linear-gradient(90deg, ${team.primary_color}, ${team.alt_color})` }}
        />

        {/* Content */}
        <div className="p-8">
          {/* Coach Photo & Info */}
          <div className="flex items-center gap-6 mb-6">
            <div 
              className="relative w-28 h-28 rounded-full overflow-hidden border-4"
              style={{ 
                borderColor: team.primary_color,
                boxShadow: `0 0 30px ${team.primary_color}40, 0 0 60px ${team.primary_color}20`
              }}
            >
              <img 
                src={coachData.coach_info.headshot_url}
                alt={coach}
                className="w-full h-full object-cover"
                style={{ filter: 'brightness(1.1) contrast(1.15)' }}
              />
            </div>
            
            <div className="flex-1">
              <h3 className="text-2xl font-light text-white mb-2 tracking-tight">{coach}</h3>
              <p 
                className="text-base font-normal mb-1"
                style={{ color: team.alt_color }}
              >
                {team.name} {team.mascot}
              </p>
              <p 
                className="text-sm font-medium text-gray-400"
              >
                {team.mascot} • {coachData.metadata.era}
              </p>
            </div>

            {/* Team Logo */}
            <div className="w-20 h-20">
              <img 
                src={team.logo}
                alt={team.name}
                className="w-full h-full object-contain opacity-90"
              />
            </div>
          </div>

          {/* Career Stats Grid */}
          <div className="grid grid-cols-3 gap-4">
            <div 
              className="p-4 rounded-lg border border-white/10"
              style={{ background: `${team.primary_color}10` }}
            >
              <div className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">Career Record</div>
              <div 
                className="text-2xl font-black"
                style={{ color: team.alt_color }}
              >
                {coachData.summary.career_record}
              </div>
            </div>
            
            <div 
              className="p-4 rounded-lg border border-white/10"
              style={{ background: `${team.primary_color}10` }}
            >
              <div className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">Win Percentage</div>
              <div 
                className="text-2xl font-black"
                style={{ color: team.alt_color }}
              >
                {coachData.summary.career_win_pct.toFixed(1)}%
              </div>
            </div>
            
            <div 
              className="p-4 rounded-lg border border-white/10"
              style={{ background: `${team.primary_color}10` }}
            >
              <div className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">Seasons</div>
              <div 
                className="text-2xl font-black"
                style={{ color: team.alt_color }}
              >
                {coachData.summary.total_seasons}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen relative overflow-hidden" style={{
      background: `
        linear-gradient(135deg, #050506 0%, #0a0a0b 25%, #060607 50%, #080809 75%, #050506 100%),
        radial-gradient(ellipse at top left, rgba(12, 12, 14, 0.3), transparent 50%),
        radial-gradient(ellipse at bottom right, rgba(10, 10, 12, 0.3), transparent 50%),
        linear-gradient(180deg, #070708 0%, #030304 100%)
      `,
      backgroundBlendMode: 'normal, screen, screen, normal'
    }}>
      {/* Lighting Effects - Uniform darkness */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800/20 via-slate-900/40 to-transparent pointer-events-none" />
      
      {/* Grid Pattern Background */}
      <div 
        className="absolute inset-0 opacity-[0.015]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px'
        }}
      />

      {/* Ambient Glow Effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl" />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Subtle Back Button */}
        <button
          onClick={onBack}
          className="group mb-8 px-3 py-1.5 backdrop-blur-md border border-white/10 hover:border-white/20 rounded-lg transition-all duration-300 hover:bg-white/5 flex items-center gap-1.5 text-sm"
        >
          <ArrowLeft className="h-3.5 w-3.5 text-slate-400 group-hover:text-slate-300 transition-colors" />
          <span className="text-slate-400 group-hover:text-slate-300 transition-colors">Back</span>
        </button>

        {/* Main Content Card */}
        <div className="max-w-7xl mx-auto">
          <div className="relative backdrop-blur-2xl border border-white/10 rounded-3xl p-12 md:p-16 shadow-2xl bg-gradient-to-br from-white/[0.03] to-white/[0.01]">
            {/* Floating Icon with Glow - Silver Theme */}
            <div className="flex justify-center mb-12">
              <div className="relative">
                <div className="absolute inset-0 bg-slate-400/20 rounded-full blur-2xl animate-pulse" />
                <div className="relative p-8 bg-gradient-to-br from-slate-500/10 to-slate-600/10 rounded-full border border-slate-400/20 shadow-xl">
                  <Users className="h-20 w-20 text-slate-300" strokeWidth={1.5} />
                </div>
              </div>
            </div>

            {/* Title with Enhanced Gradient - Matching Main App */}
            <h1 className="text-4xl md:text-5xl font-light mb-6 text-center tracking-tight">
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
                ELITE COACHING PROFILES
              </span>
            </h1>

            {/* Description */}
            <div className="text-center space-y-3 text-slate-300 mb-14 max-w-2xl mx-auto">
              <p className="text-lg font-light leading-relaxed text-gray-400">
                Comprehensive multi-school coaching analysis
              </p>
              <p className="text-lg opacity-60 font-light">
                Explore complete career trajectories and performance metrics
              </p>
            </div>

            {/* Coach Cards Grid */}
            <div className="grid md:grid-cols-2 gap-8 mb-12">
              <CoachCard coachData={laneKiffinData as CoachData} />
              <CoachCard coachData={jamesFranklinData as CoachData} />
            </div>

            {/* Head-to-Head Comparison Section */}
            <div className="mb-12">
              <h2 className="text-2xl font-light text-white mb-6 flex items-center gap-3 tracking-tight">
                <TrendingUp className="w-7 h-7 text-emerald-400" />
                Head-to-Head Comparison
              </h2>
              
              <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-8 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                {/* Dual Watermark Logos */}
                <div className="absolute top-0 left-0 w-40 h-40 opacity-5 overflow-hidden">
                  <ImageWithFallback 
                    src={(laneKiffinData as any).current_team.logo}
                    alt={(laneKiffinData as any).current_team.name}
                    className="w-full h-full object-contain scale-150"
                  />
                </div>
                <div className="absolute top-0 right-0 w-40 h-40 opacity-5 overflow-hidden">
                  <ImageWithFallback 
                    src={(jamesFranklinData as any).current_team.logo}
                    alt={(jamesFranklinData as any).current_team.name}
                    className="w-full h-full object-contain scale-150"
                  />
                </div>

                <div className="relative z-10">
                <ComparisonBar
                  label="Career Win Percentage"
                  coach1Value={(laneKiffinData as CoachData).summary.career_win_pct}
                  coach2Value={(jamesFranklinData as CoachData).summary.career_win_pct}
                  max={100}
                  coach1Color={(laneKiffinData as CoachData).current_team.alt_color}
                  coach2Color={(jamesFranklinData as CoachData).current_team.alt_color}
                />
                
                <ComparisonBar
                  label="Total Career Wins"
                  coach1Value={parseInt((laneKiffinData as CoachData).summary.career_record.split('-')[0])}
                  coach2Value={parseInt((jamesFranklinData as CoachData).summary.career_record.split('-')[0])}
                  max={150}
                  coach1Color={(laneKiffinData as CoachData).current_team.alt_color}
                  coach2Color={(jamesFranklinData as CoachData).current_team.alt_color}
                />
                
                <ComparisonBar
                  label="Total Seasons"
                  coach1Value={(laneKiffinData as CoachData).summary.total_seasons}
                  coach2Value={(jamesFranklinData as CoachData).summary.total_seasons}
                  max={20}
                  coach1Color={(laneKiffinData as CoachData).current_team.alt_color}
                  coach2Color={(jamesFranklinData as CoachData).current_team.alt_color}
                />
                
                <ComparisonBar
                  label="Schools Coached"
                  coach1Value={(laneKiffinData as CoachData).summary.schools_coached}
                  coach2Value={(jamesFranklinData as CoachData).summary.schools_coached}
                  max={5}
                  coach1Color={(laneKiffinData as CoachData).current_team.alt_color}
                  coach2Color={(jamesFranklinData as CoachData).current_team.alt_color}
                />
                
                <ComparisonBar
                  label="Total Games Coached"
                  coach1Value={(laneKiffinData as CoachData).summary.total_games}
                  coach2Value={(jamesFranklinData as CoachData).summary.total_games}
                  max={250}
                  coach1Color={(laneKiffinData as CoachData).current_team.alt_color}
                  coach2Color={(jamesFranklinData as CoachData).current_team.alt_color}
                />
                </div>
              </div>
            </div>

            {/* Career Splits Comparison */}
            <div className="mb-12">
              <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
                <BarChart3 className="w-8 h-8 text-emerald-400" />
                Performance Splits
              </h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Lane Kiffin Splits */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  {/* Watermark Logo */}
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(laneKiffinData as any).current_team.logo}
                      alt={(laneKiffinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-4">
                      <ImageWithFallback 
                        src={(laneKiffinData as any).coach_info.headshot_url}
                        alt={(laneKiffinData as any).metadata.coach}
                        className="w-10 h-10 rounded-full object-cover border-2"
                        style={{ borderColor: (laneKiffinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold flex items-center gap-2"
                        style={{ color: (laneKiffinData as CoachData).current_team.primary_color }}
                      >
                        {(laneKiffinData as CoachData).metadata.coach}
                      </h3>
                    </div>
                  
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Home className="w-4 h-4 text-emerald-400" />
                          <span className="text-gray-300">Home Games</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((laneKiffinData as CoachData).career_stats.splits.home) }}>{(laneKiffinData as CoachData).career_stats.splits.home}</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Plane className="w-4 h-4 text-blue-400" />
                          <span className="text-gray-300">Away Games</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((laneKiffinData as CoachData).career_stats.splits.away) }}>{(laneKiffinData as CoachData).career_stats.splits.away}</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Target className="w-4 h-4 text-purple-400" />
                          <span className="text-gray-300">Neutral Site</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((laneKiffinData as CoachData).career_stats.splits.neutral) }}>{(laneKiffinData as CoachData).career_stats.splits.neutral}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* James Franklin Splits */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  {/* Watermark Logo */}
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(jamesFranklinData as any).current_team.logo}
                      alt={(jamesFranklinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-4">
                      <ImageWithFallback 
                        src={(jamesFranklinData as any).coach_info.headshot_url}
                        alt={(jamesFranklinData as any).metadata.coach}
                        className="w-10 h-10 rounded-full object-cover border-2"
                        style={{ borderColor: (jamesFranklinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold flex items-center gap-2"
                        style={{ color: (jamesFranklinData as CoachData).current_team.primary_color }}
                      >
                        {(jamesFranklinData as CoachData).metadata.coach}
                      </h3>
                    </div>
                  
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Home className="w-4 h-4 text-emerald-400" />
                          <span className="text-gray-300">Home Games</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((jamesFranklinData as CoachData).career_stats.splits.home) }}>{(jamesFranklinData as CoachData).career_stats.splits.home}</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Plane className="w-4 h-4 text-blue-400" />
                          <span className="text-gray-300">Away Games</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((jamesFranklinData as CoachData).career_stats.splits.away) }}>{(jamesFranklinData as CoachData).career_stats.splits.away}</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
                        <div className="flex items-center gap-2">
                          <Target className="w-4 h-4 text-purple-400" />
                          <span className="text-gray-300">Neutral Site</span>
                        </div>
                        <span className="text-sm font-light" style={{ color: getRecordColor((jamesFranklinData as CoachData).career_stats.splits.neutral) }}>{(jamesFranklinData as CoachData).career_stats.splits.neutral}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Vs Ranked Teams */}
            <div className="mb-12">
              <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
                <Star className="w-8 h-8 text-yellow-400" />
                Performance vs Ranked Opponents
              </h2>
              
              <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-8 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                {/* Dual Watermark Logos */}
                <div className="absolute top-0 left-0 w-40 h-40 opacity-5 overflow-hidden">
                  <ImageWithFallback 
                    src={(laneKiffinData as any).current_team.logo}
                    alt={(laneKiffinData as any).current_team.name}
                    className="w-full h-full object-contain scale-150"
                  />
                </div>
                <div className="absolute top-0 right-0 w-40 h-40 opacity-5 overflow-hidden">
                  <ImageWithFallback 
                    src={(jamesFranklinData as any).current_team.logo}
                    alt={(jamesFranklinData as any).current_team.name}
                    className="w-full h-full object-contain scale-150"
                  />
                </div>

                <div className="relative z-10">
                  <div className="grid md:grid-cols-2 gap-8 mb-6">
                    <div className="text-center">
                      <div className="flex items-center justify-center gap-3 mb-3">
                        <ImageWithFallback 
                          src={(laneKiffinData as any).coach_info.headshot_url}
                          alt={(laneKiffinData as any).metadata.coach}
                          className="w-10 h-10 rounded-full object-cover border-2"
                          style={{ borderColor: (laneKiffinData as any).current_team.primary_color }}
                        />
                        <h3 
                          className="text-xl font-bold"
                          style={{ color: (laneKiffinData as CoachData).current_team.primary_color }}
                        >
                          {(laneKiffinData as CoachData).metadata.coach}
                        </h3>
                      </div>
                      <div className="text-3xl font-light mb-2" style={{ color: getRecordColor((laneKiffinData as CoachData).career_stats.vs_ranked.overall) }}>
                        {(laneKiffinData as CoachData).career_stats.vs_ranked.overall}
                      </div>
                      <div className="text-sm text-gray-400">vs Ranked Teams</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="flex items-center justify-center gap-3 mb-3">
                        <ImageWithFallback 
                          src={(jamesFranklinData as any).coach_info.headshot_url}
                          alt={(jamesFranklinData as any).metadata.coach}
                          className="w-10 h-10 rounded-full object-cover border-2"
                          style={{ borderColor: (jamesFranklinData as any).current_team.primary_color }}
                        />
                        <h3 
                          className="text-xl font-bold"
                          style={{ color: (jamesFranklinData as CoachData).current_team.primary_color }}
                        >
                          {(jamesFranklinData as CoachData).metadata.coach}
                        </h3>
                      </div>
                      <div className="text-3xl font-light mb-2" style={{ color: getRecordColor((jamesFranklinData as CoachData).career_stats.vs_ranked.overall) }}>
                        {(jamesFranklinData as CoachData).career_stats.vs_ranked.overall}
                      </div>
                      <div className="text-sm text-gray-400">vs Ranked Teams</div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="p-4 rounded-lg bg-white/5">
                      <div className="text-sm text-gray-400 mb-1">vs Top 10</div>
                      <div className="text-base font-light" style={{ color: getRecordColor((laneKiffinData as any).career_stats.vs_ranked.vs_top10 || 'N/A') }}>{(laneKiffinData as any).career_stats.vs_ranked.vs_top10 || 'N/A'}</div>
                    </div>
                    <div className="p-4 rounded-lg bg-white/5">
                      <div className="text-sm text-gray-400 mb-1">vs Top 10</div>
                      <div className="text-base font-light" style={{ color: getRecordColor((jamesFranklinData as any).career_stats.vs_ranked.vs_top10 || 'N/A') }}>{(jamesFranklinData as any).career_stats.vs_ranked.vs_top10 || 'N/A'}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Radar Charts */}
            <div className="mb-12">
              <h2 className="text-2xl font-light text-white mb-6 flex items-center gap-3 tracking-tight">
                <Radar className="w-7 h-7 text-cyan-400" />
                Performance Analytics
              </h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Lane Kiffin Radar */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(laneKiffinData as any).current_team.logo}
                      alt={(laneKiffinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-6">
                      <ImageWithFallback 
                        src={(laneKiffinData as any).coach_info.headshot_url}
                        alt={(laneKiffinData as any).metadata.coach}
                        className="w-12 h-12 rounded-full object-cover border-2"
                        style={{ borderColor: (laneKiffinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold"
                        style={{ color: (laneKiffinData as any).current_team.primary_color }}
                      >
                        {(laneKiffinData as any).metadata.coach}
                      </h3>
                    </div>

                    <div className="flex justify-center">
                      <CoachRadarChart 
                        coachData={laneKiffinData}
                        size={360}
                      />
                    </div>
                  </div>
                </div>

                {/* James Franklin Radar */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(jamesFranklinData as any).current_team.logo}
                      alt={(jamesFranklinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-6">
                      <ImageWithFallback 
                        src={(jamesFranklinData as any).coach_info.headshot_url}
                        alt={(jamesFranklinData as any).metadata.coach}
                        className="w-12 h-12 rounded-full object-cover border-2"
                        style={{ borderColor: (jamesFranklinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold"
                        style={{ color: (jamesFranklinData as any).current_team.primary_color }}
                      >
                        {(jamesFranklinData as any).metadata.coach}
                      </h3>
                    </div>

                    <div className="flex justify-center">
                      <CoachRadarChart 
                        coachData={jamesFranklinData}
                        size={360}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Interactive Career Timelines */}
            <div className="mb-12">
              <h2 className="text-2xl font-light text-white mb-6 flex items-center gap-3 tracking-tight">
                <Calendar className="w-7 h-7 text-purple-400" />
                Career Sunburst Visualization
              </h2>
              
              <div className="space-y-8">
                {/* Lane Kiffin Sunburst */}
                <CoachSunburst coachData={laneKiffinData} />
                
                {/* James Franklin Sunburst */}
                <CoachSunburst coachData={jamesFranklinData} />
              </div>
            </div>

            {/* Multi-School Experience */}
            <div className="mb-12">
              <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
                <Trophy className="w-8 h-8 text-amber-400" />
                Coaching Career Journey
              </h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Lane Kiffin Schools */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  {/* Watermark Logo */}
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(laneKiffinData as any).current_team.logo}
                      alt={(laneKiffinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-4">
                      <ImageWithFallback 
                        src={(laneKiffinData as any).coach_info.headshot_url}
                        alt={(laneKiffinData as any).metadata.coach}
                        className="w-12 h-12 rounded-full object-cover border-2"
                        style={{ borderColor: (laneKiffinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold"
                        style={{ color: (laneKiffinData as any).current_team.primary_color }}
                      >
                        {(laneKiffinData as any).metadata.coach}
                      </h3>
                    </div>
                  
                    <div className="space-y-3">
                      {(laneKiffinData as any).schools_info?.map((school: any, index: number) => (
                      <div 
                        key={index} 
                        className="p-4 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-all duration-300"
                      >
                        <div className="flex items-center gap-4 mb-2">
                          <img 
                            src={school.logo}
                            alt={school.name}
                            className="w-12 h-12 object-contain"
                          />
                          <div className="flex-1">
                            <div className="flex justify-between items-center mb-1">
                              <span className="font-bold text-white text-lg">{school.name} {school.mascot}</span>
                              <span className="text-sm text-gray-400">{school.years}</span>
                            </div>
                            <div className="text-xs text-gray-400 mb-1">{school.conference}</div>
                            <div 
                              className="text-sm font-light"
                              style={{ color: getRecordColor(school.record) }}
                            >
                              {school.record}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    </div>
                  </div>
                </div>

                {/* James Franklin Schools */}
                <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
                  {/* Watermark Logo */}
                  <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
                    <ImageWithFallback 
                      src={(jamesFranklinData as any).current_team.logo}
                      alt={(jamesFranklinData as any).current_team.name}
                      className="w-full h-full object-contain scale-150"
                    />
                  </div>

                  <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-4">
                      <ImageWithFallback 
                        src={(jamesFranklinData as any).coach_info.headshot_url}
                        alt={(jamesFranklinData as any).metadata.coach}
                        className="w-12 h-12 rounded-full object-cover border-2"
                        style={{ borderColor: (jamesFranklinData as any).current_team.primary_color }}
                      />
                      <h3 
                        className="text-xl font-bold"
                        style={{ color: (jamesFranklinData as any).current_team.primary_color }}
                      >
                        {(jamesFranklinData as any).metadata.coach}
                      </h3>
                    </div>
                  
                    <div className="space-y-3">
                      {(jamesFranklinData as any).schools_info?.map((school: any, index: number) => (
                      <div 
                        key={index} 
                        className="p-4 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-all duration-300"
                      >
                        <div className="flex items-center gap-4 mb-2">
                          <img 
                            src={school.logo}
                            alt={school.name}
                            className="w-12 h-12 object-contain"
                          />
                          <div className="flex-1">
                            <div className="flex justify-between items-center mb-1">
                              <span className="font-bold text-white text-lg">{school.name} {school.mascot}</span>
                              <span className="text-sm text-gray-400">{school.years}</span>
                            </div>
                            <div className="text-xs text-gray-400 mb-1">{school.conference}</div>
                            <div 
                              className="text-sm font-light"
                              style={{ color: getRecordColor(school.record) }}
                            >
                              {school.record}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Coming Soon Section - Silver Theme */}
            <div className="mt-16 text-center">
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <div className="absolute inset-0 bg-slate-400/20 rounded-full blur-xl" />
                  <div className="relative px-8 py-3 bg-gradient-to-r from-slate-500/5 to-slate-600/5 border border-slate-400/20 rounded-full backdrop-blur-sm">
                    <span className="text-slate-300 font-bold text-base tracking-wider">MORE FEATURES COMING SOON</span>
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto">
                {[
                  'Interactive career timelines',
                  'Head-to-head comparisons',
                  'Historical performance trends',
                  'Advanced ranking system'
                ].map((feature, index) => (
                  <div 
                    key={index}
                    className="group p-5 backdrop-blur-xl border border-white/10 rounded-2xl bg-gradient-to-br from-white/[0.03] to-transparent hover:from-slate-500/5 hover:border-slate-400/20 transition-all duration-500 hover:scale-[1.02]"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-1.5 h-1.5 bg-slate-400 rounded-full group-hover:scale-125 transition-transform duration-300" />
                      <span className="text-slate-200 font-light text-lg group-hover:text-white transition-colors">{feature}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
