import React from 'react';
import { GlassCard } from './GlassCard';
import { Trophy, Target, TrendingUp, Users, Award, Medal, ShieldCheck, BarChart3, Activity, CheckCircle } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';
import { getCoachHeadshot } from '../../services/coachService';

interface CoachingComparisonProps {
 coach1Data?: any;
 coach2Data?: any;
 predictionData?: any;
}

// Mock coaching data
const mockCoachingData = {
 coach1: {
 name: 'Ryan Day',
 team: 'Ohio State',
 logo: 'https://a.espncdn.com/i/teamlogos/ncaa/500/194.png',
 color: '#ce1141',
 vsRanked: { wins: 25, losses: 9, total: 34, percentage: 73.5 },
 vsTop10: { wins: 17, losses: 8, total: 25, percentage: 68.0 },
 vsTop5: { wins: 8, losses: 6, total: 14, percentage: 57.1 },
 conferenceVsRanked: {
 'ACC': { wins: 1, losses: 1, total: 2 },
 'Big Ten': { wins: 16, losses: 5, total: 21 },
 'Big 12': { wins: 2, losses: 0, total: 2 },
 'SEC': { wins: 3, losses: 3, total: 6 }
 }
 },
 coach2: {
 name: 'Bret Bielema',
 team: 'Illinois',
 logo: 'https://a.espncdn.com/i/teamlogos/ncaa/500/356.png',
 color: '#ff5f05',
 vsRanked: { wins: 23, losses: 45, total: 68, percentage: 33.8 },
 vsTop10: { wins: 7, losses: 24, total: 31, percentage: 22.6 },
 vsTop5: { wins: 1, losses: 9, total: 10, percentage: 10.0 },
 conferenceVsRanked: {
 'ACC': { wins: 1, losses: 1, total: 2 },
 'Big Ten': { wins: 11, losses: 19, total: 30 },
 'Big 12': { wins: 2, losses: 2, total: 4 },
 'SEC': { wins: 8, losses: 23, total: 31 }
 }
 }
};

// Performance Indicator Component
const PerformanceIndicator = ({ 
 percentage, 
 threshold = 50, 
 label 
}: { 
 percentage: number, 
 threshold?: number, 
 label: string 
}) => {
 const isElite = percentage >= threshold;
 return (
 <div className="flex items-center gap-2">
 <div className={`w-2 h-2 rounded-full ${isElite ? 'bg-emerald-400' : 'bg-slate-500'}`} />
 <span className={`text-sm font-semibold tracking-tight ${isElite ? 'text-emerald-400' : 'text-slate-400'}`}>
 {label}
 </span>
 </div>
 );
};

// Team Header Component
const TeamHeader = ({ coach, isElite }: { coach: any, isElite: boolean }) => {
 // Determine elite status based on rankings and win percentage
 const isTopTier = coach.overallRank <= 5 || coach.winPctRank <= 5;
 const isEliteRank = coach.overallRank <= 10 || coach.winPctRank <= 10;
 const isUndefeated2025 = coach.currentSeasonRecord && coach.currentSeasonRecord.split('-')[1] === '0';
 
 return (
 <div className={`relative flex flex-col gap-4 p-6 rounded-xl border ${
 isElite 
 ? 'bg-gradient-to-br from-slate-900/90 to-slate-800/90 border-emerald-500/30'
 : 'bg-gradient-to-br from-slate-900/90 to-slate-800/90 border-slate-700/30'
 }`} style={{
 backgroundColor: `${coach.color}08`,
 borderColor: `${coach.color}30`,
 boxShadow: isElite ? `0 8px 32px ${coach.color}15` : '0 4px 16px rgba(0,0,0,0.2)'
 }}>
 {/* Elite Status Badges */}
 {isTopTier && (
 <div className="absolute -top-3 -right-3 flex items-center gap-1">
 <div className="bg-gradient-to-br from-amber-400 to-amber-600 text-slate-900 px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xl border border-amber-300/50">
 <Medal className="w-3.5 h-3.5" />
 Elite Tier
 </div>
 </div>
 )}
 
 {isUndefeated2025 && (
 <div className="absolute -top-3 -left-3">
 <div className="bg-gradient-to-br from-emerald-400 to-emerald-600 text-slate-900 px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xl border border-emerald-300/50">
 <ShieldCheck className="w-3.5 h-3.5" />
 Undefeated
 </div>
 </div>
 )}

 {/* Coach Info with Headshot */}
 <div className="flex items-center gap-4">
 {/* Coach Headshot */}
 <div className="relative">
 <div className="relative w-20 h-20 rounded-xl overflow-hidden border-2" style={{
 borderColor: `${coach.color}40`,
 boxShadow: `0 8px 24px ${coach.color}30, 0 0 0 1px ${coach.color}20`
 }}>
 <ImageWithFallback 
 src={getCoachHeadshot(coach.team) || coach.logo}
 alt={coach.name}
 className="w-full h-full object-cover"
 style={{
 filter: 'brightness(1.05) contrast(1.1)'
 }}
 />
 {/* Gradient overlay */}
 <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent" />
 </div>
 {isElite && (
 <div className="absolute -bottom-1.5 -right-1.5">
 <div className="bg-emerald-500 rounded-full p-1.5 border-2 border-slate-900 shadow-lg">
 <ShieldCheck className="w-3.5 h-3.5 text-white" />
 </div>
 </div>
 )}
 </div>
 
 {/* Team Logo */}
 <div className="relative">
 <div className="p-2.5 rounded-lg border" style={{
 backgroundColor: `${coach.color}12`,
 borderColor: `${coach.color}25`,
 boxShadow: `0 4px 16px ${coach.color}20`
 }}>
 {coach.logo && (
 <ImageWithFallback 
 src={coach.logo}
 alt={coach.team}
 className="w-10 h-10 object-contain"
 style={{
 filter: `drop-shadow(0 2px 4px ${coach.color}40)`
 }}
 />
 )}
 </div>
 </div>
 
 <div className="flex-1">
 <h5 className="font-bold text-white text-lg tracking-tight">{coach.name}</h5>
 <p className="text-sm font-medium mt-0.5" style={{ color: coach.color }}>{coach.team}</p>
 {coach.conference && (
 <p className="text-xs text-slate-400 mt-1 font-medium">{coach.conference}</p>
 )}
 </div>
 </div>

 {/* Career Stats */}
 <div className="grid grid-cols-2 gap-3">
 <div className="rounded-lg p-3 bg-slate-950/50 border border-slate-700/30 hover:border-slate-600/50 transition-colors">
 <div className="text-xs text-slate-400 mb-1.5 font-semibold uppercase tracking-wider">Career</div>
 <div className="font-bold text-white text-base">{coach.careerRecord}</div>
 <div className="text-xs font-semibold mt-1" style={{ color: coach.color }}>{coach.careerWinPct}%</div>
 </div>
 <div className="rounded-lg p-3 bg-slate-950/50 border border-slate-700/30 hover:border-slate-600/50 transition-colors">
 <div className="text-xs text-slate-400 mb-1.5 font-semibold uppercase tracking-wider">2025 Season</div>
 <div className="font-bold text-white text-base">{coach.currentSeasonRecord}</div>
 <div className="text-xs text-slate-400 font-semibold mt-1">{coach.currentSeasonGames} games</div>
 </div>
 </div>

 {/* National Rankings */}
 <div className="rounded-lg p-3 bg-slate-950/70 border border-slate-700/30">
 <div className="text-xs text-slate-400 mb-2 flex items-center gap-1.5 font-semibold uppercase tracking-wider">
 <Award className="w-3.5 h-3.5" />
 National Rankings
 </div>
 <div className="space-y-1.5">
 <div className="flex items-center justify-between text-xs">
 <span className="text-slate-400 font-medium">Overall:</span>
 <span className="font-bold text-white text-sm">#{coach.overallRank}</span>
 </div>
 <div className="flex items-center justify-between text-xs">
 <span className="text-slate-400 font-medium">Win %:</span>
 <span className="font-bold text-white text-sm">#{coach.winPctRank}</span>
 </div>
 <div className="flex items-center justify-between text-xs">
 <span className="text-slate-400 font-medium">Total Wins:</span>
 <span className="font-bold text-white text-sm">{coach.totalWins} (#{coach.totalWinsRank})</span>
 </div>
 </div>
 </div>
 </div>
 );
};

// Performance Comparison Row
const PerformanceRow = ({ 
 label, 
 coach1Data, 
 coach2Data, 
 icon: Icon,
 coach1Color,
 coach2Color 
}: { 
 label: string, 
 coach1Data: any, 
 coach2Data: any, 
 icon: any,
 coach1Color: string,
 coach2Color: string
}) => {
 const coach1Better = coach1Data.percentage > coach2Data.percentage;
 
 return (
 <tr className="border-b border-gray-700/30 hover:bg-white/5 transition-colors">
 <td className="py-3 sm:py-4 px-2 sm:px-4">
 <div className="flex items-center gap-1 sm:gap-2 text-gray-300 font-medium text-xs sm:text-sm">
 <Icon className="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" />
 <span className="truncate">{label}</span>
 </div>
 </td>
 <td className="py-3 sm:py-4 px-2 sm:px-4 text-center">
 <div className={`space-y-1 ${coach1Better ? 'text-green-400' : 'text-white'}`}>
 <div className="font-bold text-base sm:text-lg">{coach1Data.percentage}%</div>
 <div className="text-xs text-gray-400">
 {coach1Data.wins}-{coach1Data.losses}-0 <span className="hidden sm:inline">({coach1Data.total} games)</span>
 </div>
 {coach1Better && <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mx-auto mt-1" />}
 </div>
 </td>
 <td className="py-3 sm:py-4 px-2 sm:px-4 text-center">
 <div className={`space-y-1 ${!coach1Better ? 'text-green-400' : 'text-white'}`}>
 <div className="font-bold text-base sm:text-lg">{coach2Data.percentage}%</div>
 <div className="text-xs text-gray-400">
 {coach2Data.wins}-{coach2Data.losses}-0 <span className="hidden sm:inline">({coach2Data.total} games)</span>
 </div>
 {!coach1Better && <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mx-auto mt-1" />}
 </div>
 </td>
 </tr>
 );
};

export function CoachingComparison({ coach1Data, coach2Data, predictionData }: CoachingComparisonProps) {
 // Get dynamic team data from predictionData
 const awayTeam = predictionData?.team_selector?.away_team;
 const homeTeam = predictionData?.team_selector?.home_team;

 if (!awayTeam || !homeTeam) {
 return null;
 }

 // Helper to parse record strings like "26-9-0" to extract wins, losses, and percentage
 const parseRecordString = (record: string) => {
 const match = record.match(/(\d+)-(\d+)-\d+/);
 if (match) {
 const wins = parseInt(match[1]);
 const losses = parseInt(match[2]);
 const total = wins + losses;
 const percentage = total > 0 ? parseFloat(((wins / total) * 100).toFixed(1)) : 0;
 return { wins, losses, total, percentage };
 }
 return { wins: 0, losses: 0, total: 0, percentage: 0 };
 };

 // Parse coaching data from structured coaching_data object (not text parsing)
 const parseCoachingData = (team: any, isAway: boolean) => {
 const coachingData = isAway 
 ? predictionData?.coaching_data?.away 
 : predictionData?.coaching_data?.home;
 
 if (!coachingData) {
 return {
 name: team.coach || 'Head Coach',
 team: team.name,
 logo: team.logo,
 color: team.primary_color,
 conference: team.conference || 'N/A',
 careerRecord: '0-0',
 careerWinPct: 0,
 currentSeasonRecord: '0-0',
 currentSeasonGames: 0,
 totalWins: 0,
 overallRank: 999,
 winPctRank: 999,
 totalWinsRank: 999,
 current2025Rank: 999,
 vsRanked: { wins: 0, losses: 0, total: 0, percentage: 0 },
 vsTop10: { wins: 0, losses: 0, total: 0, percentage: 0 },
 vsTop5: { wins: 0, losses: 0, total: 0, percentage: 0 },
 conferenceVsRanked: {
 'ACC': { wins: 0, losses: 0, total: 0 },
 'Big Ten': { wins: 0, losses: 0, total: 0 },
 'Big 12': { wins: 0, losses: 0, total: 0 },
 'SEC': { wins: 0, losses: 0, total: 0 }
 }
 };
 }

 // Build career record from career_wins and career_losses
 const careerWins = coachingData.career_wins || 0;
 const careerLosses = coachingData.career_losses || 0;
 const careerRecord = `${careerWins}-${careerLosses}`;
 const careerWinPct = (coachingData.career_win_pct || 0) * 100; // Backend sends as decimal
 const totalWins = careerWins;

 // Parse current season record properly
 const currentSeasonRecord = coachingData.current_2025_record || '0-0';
 const seasonParts = currentSeasonRecord.split('-');
 const currentSeasonGames = seasonParts.length >= 2 
 ? parseInt(seasonParts[0]) + parseInt(seasonParts[1]) 
 : 0;

 // Extract vs ranked data
 const vsRanked = parseRecordString(coachingData.vs_ranked_record || '0-0-0');
 const vsTop10 = parseRecordString(coachingData.vs_top10_record || '0-0-0');
 const vsTop5 = parseRecordString(coachingData.vs_top5_record || '0-0-0');

 // Extract conference records
 const conferenceVsRanked = {
 'ACC': parseRecordString(coachingData.vs_ranked_acc_record || '0-0-0'),
 'Big Ten': parseRecordString(coachingData.vs_ranked_big_ten_record || '0-0-0'),
 'Big 12': parseRecordString(coachingData.vs_ranked_big_12_record || '0-0-0'),
 'SEC': parseRecordString(coachingData.vs_ranked_sec_record || '0-0-0')
 };

 return {
 name: coachingData.coach_name || team.coach || 'Head Coach',
 team: team.name,
 logo: team.logo,
 color: team.primary_color,
 conference: team.conference || 'N/A',
 careerRecord,
 careerWinPct: parseFloat(careerWinPct.toFixed(1)),
 currentSeasonRecord,
 currentSeasonGames,
 totalWins,
 overallRank: coachingData.overall_rank || 999,
 winPctRank: coachingData.win_pct_rank || 999,
 totalWinsRank: coachingData.total_wins_rank || 999,
 current2025Rank: coachingData.current_2025_rank || 999,
 vsRanked,
 vsTop10,
 vsTop5,
 conferenceVsRanked
 };
 };

 const coach1 = parseCoachingData(awayTeam, true);
 const coach2 = parseCoachingData(homeTeam, false);
 
 const coach1IsElite = coach1.vsRanked.percentage > 65;
 const coach2IsElite = coach2.vsRanked.percentage > 65;

 return (
 <GlassCard className="p-4 sm:p-6">
 <div className="flex items-center gap-2 sm:gap-3 mb-6 sm:mb-8">
 <div className="p-2 rounded-xl border border-slate-700/40 backdrop-blur-sm">
 <Users className="w-5 h-5 sm:w-6 sm:h-6 text-slate-300" />
 </div>
 <div>
 <h3 className="text-white font-bold text-base sm:text-lg tracking-tight">
 Elite Coaching Analysis
 </h3>
 <p className="text-xs text-slate-400 font-medium mt-0.5">Head-to-Head vs Ranked Performance</p>
 </div>
 </div>

 {/* Coach Headers */}
 <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 mb-6 sm:mb-8">
 <TeamHeader coach={coach1} isElite={coach1IsElite} />
 <TeamHeader coach={coach2} isElite={coach2IsElite} />
 </div>

 {/* Career Achievements & Experience Comparison */}
 <div className="mb-6 sm:mb-8">
 <h4 className="text-slate-300 font-bold mb-4 flex items-center gap-2 text-sm tracking-tight">
 <div className="p-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20">
 <Award className="w-4 h-4 text-purple-400" />
 </div>
 Career Achievements & Rankings
 </h4>
 
 <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
 {/* Coach 1 Career Stats */}
 <div className="rounded-xl p-4 border backdrop-blur-sm" style={{
 borderColor: `${coach1.color}20`,
 background: `linear-gradient(135deg, ${coach1.color}08, rgba(15, 23, 42, 0.6))`,
 backdropFilter: 'blur(16px)',
 boxShadow: `0 4px 16px ${coach1.color}10`
 }}>
 <div className="flex items-center gap-2.5 mb-3">
 {/* Coach Headshot */}
 <div className="relative w-12 h-12 rounded-lg overflow-hidden border" style={{
 borderColor: `${coach1.color}40`,
 boxShadow: `0 4px 12px ${coach1.color}25`
 }}>
 <ImageWithFallback 
 src={getCoachHeadshot(coach1.team) || coach1.logo}
 alt={coach1.name}
 className="w-full h-full object-cover"
 style={{
 filter: 'brightness(1.05)'
 }}
 />
 <div className="absolute inset-0 bg-gradient-to-t from-slate-900/40 via-transparent to-transparent" />
 </div>
 {/* Team Logo */}
 <div className="p-1.5 rounded border opacity-80" style={{
 backgroundColor: `${coach1.color}15`,
 borderColor: `${coach1.color}30`
 }}>
 {coach1.logo && (
 <ImageWithFallback 
 src={coach1.logo}
 alt={coach1.team}
 className="w-5 h-5 object-contain"
 />
 )}
 </div>
 <div>
 <h5 className="font-bold text-white text-sm tracking-tight">{coach1.name}</h5>
 <p className="text-xs text-slate-400 font-medium">{coach1.conference}</p>
 </div>
 </div>
 
 <div className="space-y-2.5">
 {/* Experience Meter */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: `${coach1.color}15`
 }}>
 <div className="flex justify-between items-center mb-2">
 <span className="text-xs text-slate-400 font-semibold">Experience</span>
 <span className="text-sm font-bold text-white">{coach1.totalWins} Wins</span>
 </div>
 <div className="w-full backdrop-blur-sm rounded-full h-2 mb-2 border border-slate-700/30">
 <div 
 className="h-2 rounded-full transition-all duration-500"
 style={{ 
 width: `${Math.min((coach1.totalWins / 150) * 100, 100)}%`,
 background: `linear-gradient(90deg, ${coach1.color}60, ${coach1.color})`
 }}
 />
 </div>
 <div className="flex justify-between text-xs">
 <span className="text-slate-500 font-medium">Milestone</span>
 <span className="font-bold" style={{ color: coach1.color }}>
 {coach1.totalWins >= 150 ? 'Elite (150+)' : 
 coach1.totalWins >= 100 ? 'Veteran (100+)' : 
 coach1.totalWins >= 50 ? 'Experienced (50+)' : 
 'Rising Star'}
 </span>
 </div>
 </div>

 {/* Career Record */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: `${coach1.color}15`
 }}>
 <div className="flex justify-between items-center">
 <span className="text-xs text-slate-400 font-semibold">Career</span>
 <div className="text-right">
 <div className="text-base font-bold text-white tracking-tight">{coach1.careerRecord}</div>
 <div className="text-xs font-bold mt-0.5" style={{ color: coach1.color }}>{coach1.careerWinPct}%</div>
 </div>
 </div>
 </div>

 {/* National Rankings Grid */}
 <div className="grid grid-cols-2 gap-2">
 <div className="p-2.5 rounded-lg border bg-slate-950/70 text-center" style={{
 borderColor: `${coach1.color}15`
 }}>
 <div className="text-xs text-slate-500 mb-1 font-semibold">Overall</div>
 <div className="text-xl font-bold text-white tracking-tight">#{coach1.overallRank}</div>
 {coach1.overallRank <= 5 && (
 <div className="mt-1">
 <Medal className="w-3.5 h-3.5 text-amber-400 mx-auto" />
 </div>
 )}
 </div>
 <div className="p-2.5 rounded-lg border bg-slate-950/70 text-center" style={{
 borderColor: `${coach1.color}15`
 }}>
 <div className="text-xs text-slate-500 mb-1 font-semibold">Win %</div>
 <div className="text-xl font-bold text-white tracking-tight">#{coach1.winPctRank}</div>
 {coach1.winPctRank <= 5 && (
 <div className="mt-1">
 <Trophy className="w-3.5 h-3.5 text-amber-400 mx-auto" />
 </div>
 )}
 </div>
 </div>

 {/* 2025 Season Performance */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: coach1.currentSeasonRecord.split('-')[1] === '0' ? `${coach1.color}30` : `${coach1.color}15`,
 background: coach1.currentSeasonRecord.split('-')[1] === '0' ? `linear-gradient(135deg, ${coach1.color}15, rgba(16, 185, 129, 0.05))` : undefined
 }}>
 <div className="flex items-center justify-between mb-1.5">
 <div className="flex items-center gap-1.5">
 <Activity className="w-3.5 h-3.5 text-blue-400" />
 <span className="text-xs text-slate-400 font-semibold">2025 Season</span>
 </div>
 {coach1.currentSeasonRecord.split('-')[1] === '0' && (
 <div className="bg-emerald-500/20 border border-emerald-500/40 px-1.5 py-0.5 rounded">
 <span className="text-xs font-bold text-emerald-400">Undefeated</span>
 </div>
 )}
 </div>
 <div className="flex justify-between items-center">
 <span className="text-base font-bold text-white tracking-tight">{coach1.currentSeasonRecord}</span>
 <span className="text-xs text-slate-400 font-semibold">Rank #{coach1.current2025Rank}</span>
 </div>
 </div>
 </div>
 </div>

 {/* Coach 2 Career Stats */}
 <div className="rounded-xl p-4 border backdrop-blur-sm" style={{
 borderColor: `${coach2.color}20`,
 background: `linear-gradient(135deg, ${coach2.color}08, rgba(15, 23, 42, 0.6))`,
 backdropFilter: 'blur(16px)',
 boxShadow: `0 4px 16px ${coach2.color}10`
 }}>
 <div className="flex items-center gap-2.5 mb-3">
 {/* Coach Headshot */}
 <div className="relative w-12 h-12 rounded-lg overflow-hidden border" style={{
 borderColor: `${coach2.color}40`,
 boxShadow: `0 4px 12px ${coach2.color}25`
 }}>
 <ImageWithFallback 
 src={getCoachHeadshot(coach2.team) || coach2.logo}
 alt={coach2.name}
 className="w-full h-full object-cover"
 style={{
 filter: 'brightness(1.05)'
 }}
 />
 <div className="absolute inset-0 bg-gradient-to-t from-slate-900/40 via-transparent to-transparent" />
 </div>
 {/* Team Logo */}
 <div className="p-1.5 rounded border opacity-80" style={{
 backgroundColor: `${coach2.color}15`,
 borderColor: `${coach2.color}30`
 }}>
 {coach2.logo && (
 <ImageWithFallback 
 src={coach2.logo}
 alt={coach2.team}
 className="w-5 h-5 object-contain"
 />
 )}
 </div>
 <div>
 <h5 className="font-bold text-white text-sm tracking-tight">{coach2.name}</h5>
 <p className="text-xs text-slate-400 font-medium">{coach2.conference}</p>
 </div>
 </div>
 
 <div className="space-y-2.5">
 {/* Experience Meter */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: `${coach2.color}15`
 }}>
 <div className="flex justify-between items-center mb-2">
 <span className="text-xs text-slate-400 font-semibold">Experience</span>
 <span className="text-sm font-bold text-white">{coach2.totalWins} Wins</span>
 </div>
 <div className="w-full backdrop-blur-sm rounded-full h-2 mb-2 border border-slate-700/30">
 <div 
 className="h-2 rounded-full transition-all duration-500"
 style={{ 
 width: `${Math.min((coach2.totalWins / 150) * 100, 100)}%`,
 background: `linear-gradient(90deg, ${coach2.color}60, ${coach2.color})`
 }}
 />
 </div>
 <div className="flex justify-between text-xs">
 <span className="text-slate-500 font-medium">Milestone</span>
 <span className="font-bold" style={{ color: coach2.color }}>
 {coach2.totalWins >= 150 ? 'Elite (150+)' : 
 coach2.totalWins >= 100 ? 'Veteran (100+)' : 
 coach2.totalWins >= 50 ? 'Experienced (50+)' : 
 'Rising Star'}
 </span>
 </div>
 </div>

 {/* Career Record */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: `${coach2.color}15`
 }}>
 <div className="flex justify-between items-center">
 <span className="text-xs text-slate-400 font-semibold">Career</span>
 <div className="text-right">
 <div className="text-base font-bold text-white tracking-tight">{coach2.careerRecord}</div>
 <div className="text-xs font-bold mt-0.5" style={{ color: coach2.color }}>{coach2.careerWinPct}%</div>
 </div>
 </div>
 </div>

 {/* National Rankings Grid */}
 <div className="grid grid-cols-2 gap-2">
 <div className="p-2.5 rounded-lg border bg-slate-950/70 text-center" style={{
 borderColor: `${coach2.color}15`
 }}>
 <div className="text-xs text-slate-500 mb-1 font-semibold">Overall</div>
 <div className="text-xl font-bold text-white tracking-tight">#{coach2.overallRank}</div>
 {coach2.overallRank <= 5 && (
 <div className="mt-1">
 <Medal className="w-3.5 h-3.5 text-amber-400 mx-auto" />
 </div>
 )}
 </div>
 <div className="p-2.5 rounded-lg border bg-slate-950/70 text-center" style={{
 borderColor: `${coach2.color}15`
 }}>
 <div className="text-xs text-slate-500 mb-1 font-semibold">Win %</div>
 <div className="text-xl font-bold text-white tracking-tight">#{coach2.winPctRank}</div>
 {coach2.winPctRank <= 5 && (
 <div className="mt-1">
 <Trophy className="w-3.5 h-3.5 text-amber-400 mx-auto" />
 </div>
 )}
 </div>
 </div>

 {/* 2025 Season Performance */}
 <div className="p-2.5 rounded-lg border bg-slate-950/70" style={{
 borderColor: coach2.currentSeasonRecord.split('-')[1] === '0' ? `${coach2.color}30` : `${coach2.color}15`,
 background: coach2.currentSeasonRecord.split('-')[1] === '0' ? `linear-gradient(135deg, ${coach2.color}15, rgba(16, 185, 129, 0.05))` : undefined
 }}>
 <div className="flex items-center justify-between mb-1.5">
 <div className="flex items-center gap-1.5">
 <Activity className="w-3.5 h-3.5 text-blue-400" />
 <span className="text-xs text-slate-400 font-semibold">2025 Season</span>
 </div>
 {coach2.currentSeasonRecord.split('-')[1] === '0' && (
 <div className="bg-emerald-500/20 border border-emerald-500/40 px-1.5 py-0.5 rounded">
 <span className="text-xs font-bold text-emerald-400">Undefeated</span>
 </div>
 )}
 </div>
 <div className="flex justify-between items-center">
 <span className="text-base font-bold text-white tracking-tight">{coach2.currentSeasonRecord}</span>
 <span className="text-xs text-slate-400 font-semibold">Rank #{coach2.current2025Rank}</span>
 </div>
 </div>
 </div>
 </div>
 </div>
 </div>

 {/* Big Game Performance Summary */}
 <div className="mb-6 sm:mb-8">
 <h4 className="text-gray-300 font-semibold mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
 <Trophy className="w-3 h-3 sm:w-4 sm:h-4 text-yellow-400" />
 Big Game Performance Summary
 </h4>
 
 <div className="rounded-xl p-4 sm:p-6 border shadow-xl" style={{
 background: `linear-gradient(to bottom right, ${coach1.color}10, ${coach2.color}10, ${coach1.color}08)`,
 borderColor: `${coach1.color}20`,
 backdropFilter: 'blur(16px) saturate(180%)',
 WebkitBackdropFilter: 'blur(16px) saturate(180%)'
 }}>
 <div className="overflow-x-auto -mx-2 sm:mx-0">
 <table className="w-full min-w-[580px]">
 <thead>
 <tr className="border-b border-gray-600/40">
 <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-medium text-xs sm:text-sm">Performance Level</th>
 <th className="text-center py-2 sm:py-3 px-2 sm:px-4 font-medium text-xs sm:text-sm">
 <div className="flex items-center justify-center gap-1 sm:gap-2">
 {coach1.logo && (
 <ImageWithFallback 
 src={coach1.logo}
 alt={coach1.team}
 className="w-5 h-5 sm:w-6 sm:h-6 object-contain opacity-90"
 />
 )}
 <span style={{ color: coach1.color }} className="truncate max-w-[80px] sm:max-w-none">{coach1.name}</span>
 </div>
 </th>
 <th className="text-center py-2 sm:py-3 px-2 sm:px-4 font-medium text-xs sm:text-sm">
 <div className="flex items-center justify-center gap-1 sm:gap-2">
 {coach2.logo && (
 <ImageWithFallback 
 src={coach2.logo}
 alt={coach2.team}
 className="w-5 h-5 sm:w-6 sm:h-6 object-contain opacity-90"
 />
 )}
 <span style={{ color: coach2.color }} className="truncate max-w-[80px] sm:max-w-none">{coach2.name}</span>
 </div>
 </th>
 </tr>
 </thead>
 <tbody>
 <PerformanceRow
 label="vs Top 5 Teams"
 coach1Data={coach1.vsTop5}
 coach2Data={coach2.vsTop5}
 coach1Color={coach1.color}
 coach2Color={coach2.color}
 icon={Trophy}
 />
 <PerformanceRow
 label="vs Top 10 Teams"
 coach1Data={coach1.vsTop10}
 coach2Data={coach2.vsTop10}
 coach1Color={coach1.color}
 coach2Color={coach2.color}
 icon={Target}
 />
 <PerformanceRow
 label="vs All Ranked"
 coach1Data={coach1.vsRanked}
 coach2Data={coach2.vsRanked}
 coach1Color={coach1.color}
 coach2Color={coach2.color}
 icon={TrendingUp}
 />
 </tbody>
 </table>
 </div>
 </div>
 </div>

 {/* Conference vs Ranked Breakdown */}
 <div className="mb-8">
 <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
 <Target className="w-4 h-4 text-blue-400" />
 Conference vs Ranked Breakdown
 </h4>
 
 <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
 {/* Coach 1 Conference Performance */}
 <div className="rounded-xl p-6 border shadow-lg" style={{
 background: `linear-gradient(to bottom right, ${coach1.color}20, ${coach1.color}10)`,
 borderColor: `${coach1.color}30`,
 backdropFilter: 'blur(12px) saturate(160%)',
 WebkitBackdropFilter: 'blur(12px) saturate(160%)'
 }}>
 <div className="flex items-center gap-3 mb-4">
 {/* Coach Headshot */}
 <div className="relative w-10 h-10 rounded-lg overflow-hidden border" style={{
 borderColor: `${coach1.color}40`,
 boxShadow: `0 4px 12px ${coach1.color}25`
 }}>
 <ImageWithFallback 
 src={getCoachHeadshot(coach1.team) || coach1.logo}
 alt={coach1.name}
 className="w-full h-full object-cover"
 style={{ filter: 'brightness(1.05)' }}
 />
 <div className="absolute inset-0 bg-gradient-to-t from-slate-900/30 via-transparent to-transparent" />
 </div>
 {/* Team Logo */}
 {coach1.logo && (
 <ImageWithFallback 
 src={coach1.logo}
 alt={coach1.team}
 className="w-7 h-7 object-contain opacity-90"
 style={{ filter: `drop-shadow(0 0 4px ${coach1.color}40)` }}
 />
 )}
 <h5 className="font-semibold text-white">{coach1.name} vs Ranked</h5>
 </div>
 <div className="space-y-3">
 {Object.entries(coach1.conferenceVsRanked).map(([conference, data]: [string, any]) => (
 <div key={conference} className="flex justify-between items-center p-3 rounded-lg border border-white/5" style={{
 background: `${coach1.color}15`,
 backdropFilter: 'blur(4px)',
 WebkitBackdropFilter: 'blur(4px)'
 }}>
 <span className="text-gray-300 font-medium">vs Ranked {conference}</span>
 <div className="text-right">
 <div className="text-white font-semibold">
 {data.wins}-{data.losses}-0
 </div>
 <div className="text-xs text-gray-400">
 {data.total} games
 </div>
 {data.total > 0 && data.wins/data.total >= 0.6 && (
 <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mx-auto mt-1" />
 )}
 </div>
 </div>
 ))}
 </div>
 </div>

 {/* Coach 2 Conference Performance */}
 <div className="rounded-xl p-6 border shadow-lg" style={{
 background: `linear-gradient(to bottom right, ${coach2.color}20, ${coach2.color}10)`,
 borderColor: `${coach2.color}30`,
 backdropFilter: 'blur(12px) saturate(160%)',
 WebkitBackdropFilter: 'blur(12px) saturate(160%)'
 }}>
 <div className="flex items-center gap-3 mb-4">
 {/* Coach Headshot */}
 <div className="relative w-10 h-10 rounded-lg overflow-hidden border" style={{
 borderColor: `${coach2.color}40`,
 boxShadow: `0 4px 12px ${coach2.color}25`
 }}>
 <ImageWithFallback 
 src={getCoachHeadshot(coach2.team) || coach2.logo}
 alt={coach2.name}
 className="w-full h-full object-cover"
 style={{ filter: 'brightness(1.05)' }}
 />
 <div className="absolute inset-0 bg-gradient-to-t from-slate-900/30 via-transparent to-transparent" />
 </div>
 {/* Team Logo */}
 {coach2.logo && (
 <ImageWithFallback 
 src={coach2.logo}
 alt={coach2.team}
 className="w-7 h-7 object-contain opacity-90"
 style={{ filter: `drop-shadow(0 0 4px ${coach2.color}40)` }}
 />
 )}
 <h5 className="font-semibold text-white">{coach2.name} vs Ranked</h5>
 </div>
 <div className="space-y-3">
 {Object.entries(coach2.conferenceVsRanked).map(([conference, data]: [string, any]) => (
 <div key={conference} className="flex justify-between items-center p-3 rounded-lg border border-white/5" style={{
 background: `${coach2.color}15`,
 backdropFilter: 'blur(4px)',
 WebkitBackdropFilter: 'blur(4px)'
 }}>
 <span className="text-gray-300 font-medium">vs Ranked {conference}</span>
 <div className="text-right">
 <div className="text-white font-semibold">
 {data.wins}-{data.losses}-0
 </div>
 <div className="text-xs text-gray-400">
 {data.total} games
 </div>
 {data.total > 0 && data.wins/data.total >= 0.6 && (
 <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mx-auto mt-1" />
 )}
 </div>
 </div>
 ))}
 </div>
 </div>
 </div>
 </div>

 {/* Elite Performance Analysis */}
 <div>
 <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
 <TrendingUp className="w-4 h-4 text-green-400" />
 Elite Performance Analysis
 </h4>
 
 <div className="rounded-xl p-6 border shadow-2xl" style={{
 background: `linear-gradient(to bottom right, ${coach1.color}12, ${coach2.color}12, ${coach1.color}08)`,
 borderColor: `${coach1.color}25`,
 backdropFilter: 'blur(20px) saturate(200%)',
 WebkitBackdropFilter: 'blur(20px) saturate(200%)'
 }}>
 <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
 {/* Performance Metrics */}
 {[
 { label: 'vs Top 5 Elite', threshold: 50, coach1: coach1.vsTop5.percentage, coach2: coach2.vsTop5.percentage },
 { label: 'vs Top 10 Strong', threshold: 45, coach1: coach1.vsTop10.percentage, coach2: coach2.vsTop10.percentage },
 { label: 'vs Ranked Consistent', threshold: 40, coach1: coach1.vsRanked.percentage, coach2: coach2.vsRanked.percentage }
 ].map((metric, index) => (
 <div key={index} className="rounded-lg p-4 shadow-lg border border-gray-400/15" style={{
 background: `linear-gradient(135deg, ${coach1.color}18, ${coach2.color}15)`,
 backdropFilter: 'blur(8px) saturate(140%)',
 WebkitBackdropFilter: 'blur(8px) saturate(140%)'
 }}>
 <h6 className="text-gray-300 font-medium mb-3 text-center">{metric.label}</h6>
 <div className="space-y-3">
 <div className="flex items-center justify-between">
 <div className="flex items-center gap-2">
 {coach1.logo && (
 <ImageWithFallback 
 src={coach1.logo}
 alt={coach1.team}
 className="w-4 h-4 object-contain opacity-90"
 />
 )}
 <span className="text-xs text-gray-400">{coach1.name}</span>
 </div>
 <div className="flex items-center gap-2">
 <span className={`font-bold ${metric.coach1 >= metric.threshold ? 'text-emerald-400' : 'text-slate-500'}`}>
 {metric.coach1}%
 </span>
 {metric.coach1 >= metric.threshold && <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />}
 </div>
 </div>
 <div className="flex items-center justify-between">
 <div className="flex items-center gap-2">
 {coach2.logo && (
 <ImageWithFallback 
 src={coach2.logo}
 alt={coach2.team}
 className="w-4 h-4 object-contain opacity-90"
 />
 )}
 <span className="text-xs text-gray-400">{coach2.name}</span>
 </div>
 <div className="flex items-center gap-2">
 <span className={`font-bold ${metric.coach2 >= metric.threshold ? 'text-emerald-400' : 'text-slate-500'}`}>
 {metric.coach2}%
 </span>
 {metric.coach2 >= metric.threshold && <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />}
 </div>
 </div>
 </div>
 </div>
 ))}
 </div>
 </div>
 </div>
 </GlassCard>
 );
}