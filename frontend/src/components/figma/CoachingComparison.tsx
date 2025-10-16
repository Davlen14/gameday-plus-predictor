import React from 'react';
import { GlassCard } from './GlassCard';
import { Trophy, Target, TrendingUp, Users, CheckCircle, XCircle } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { generateTeamAbbr, extractSection, parseTeamValue } from '../../utils/teamUtils';

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
      {isElite ? (
        <CheckCircle className="w-4 h-4 text-green-400" />
      ) : (
        <XCircle className="w-4 h-4 text-red-400" />
      )}
      <span className={`text-sm font-medium ${isElite ? 'text-green-400' : 'text-red-400'}`}>
        {label}
      </span>
    </div>
  );
};

// Team Header Component
const TeamHeader = ({ coach, isElite }: { coach: any, isElite: boolean }) => (
  <div className={`flex items-center justify-center gap-3 p-4 rounded-lg border ${
    isElite 
      ? 'bg-gradient-to-br from-green-900/30 to-emerald-800/30 border-green-500/40' 
      : 'bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-gray-600/30'
  }`} style={{
    backgroundColor: `${coach.color}10`,
    borderColor: `${coach.color}40`
  }}>
    <div className="relative">
      <ImageWithFallback 
        src={coach.logo}
        alt={coach.team}
        className="w-10 h-10 object-contain opacity-90"
        style={{
          filter: `drop-shadow(0 4px 8px rgba(0,0,0,0.3)) drop-shadow(0 0 8px ${coach.color}40)`
        }}
      />
      {isElite && (
        <div className="absolute -top-1 -right-1">
          <CheckCircle className="w-5 h-5 text-green-400 bg-gray-900 rounded-full" />
        </div>
      )}
    </div>
    <div>
      <h5 className="font-bold text-white">{coach.name}</h5>
      <p className="text-xs" style={{ color: coach.color }}>{coach.team}</p>
    </div>
  </div>
);

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
    <tr className="border-b border-gray-700/30 hover:bg-gray-800/20 transition-colors">
      <td className="py-4 px-4">
        <div className="flex items-center gap-2 text-gray-300 font-medium">
          <Icon className="w-4 h-4" />
          {label}
        </div>
      </td>
      <td className="py-4 px-4 text-center">
        <div className={`space-y-1 ${coach1Better ? 'text-green-400' : 'text-white'}`}>
          <div className="font-bold text-lg">{coach1Data.percentage}%</div>
          <div className="text-xs text-gray-400">
            {coach1Data.wins}-{coach1Data.losses}-0 ({coach1Data.total} games)
          </div>
          {coach1Better && <CheckCircle className="w-4 h-4 text-green-400 mx-auto" />}
        </div>
      </td>
      <td className="py-4 px-4 text-center">
        <div className={`space-y-1 ${!coach1Better ? 'text-green-400' : 'text-white'}`}>
          <div className="font-bold text-lg">{coach2Data.percentage}%</div>
          <div className="text-xs text-gray-400">
            {coach2Data.wins}-{coach2Data.losses}-0 ({coach2Data.total} games)
          </div>
          {!coach1Better && <CheckCircle className="w-4 h-4 text-green-400 mx-auto" />}
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

  // Parse coaching data from section [16] - ELITE COACHING STAFF COMPARISON & VS RANKED PERFORMANCE
  const parseCoachingData = (team: any, isAway: boolean) => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 16) : null;
    
    if (!section) {
      return {
        name: team.coach || 'Head Coach',
        team: team.name,
        logo: team.logo,
        color: team.primary_color,
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

    // Helper to parse record strings like "11-16-0 (40.7%)" or "4-8-0 (12 games)"
    const parseRecord = (text: string, pattern: RegExp) => {
      const match = text.match(pattern);
      if (match) {
        const wins = parseInt(match[1]);
        const losses = parseInt(match[2]);
        const total = wins + losses;
        const percentage = total > 0 ? parseFloat(((wins / total) * 100).toFixed(1)) : 0;
        return { wins, losses, total, percentage };
      }
      return { wins: 0, losses: 0, total: 0, percentage: 0 };
    };

    // Get coach name from the section - format: "Coach Name                Jeff Brohm                          Mario Cristobal"
    const coachNameLine = section.match(/Coach Name\s+([A-Za-z\s]+?)\s{2,}([A-Za-z\s]+?)\s+/);
    const coachName = coachNameLine 
      ? (isAway ? coachNameLine[1].trim() : coachNameLine[2].trim())
      : (team.coach || 'Head Coach');

    // Parse vs Ranked Teams - pattern: "11-16-0 (40.7%)" or "11-18-0 (37.9%)"
    const vsRankedPattern = isAway
      ? /Vs Ranked Teams\s+(\d+)-(\d+)-\d+\s*\([\d.]+%\)/
      : /Vs Ranked Teams\s+\d+-\d+-\d+\s*\([\d.]+%\)\s+(\d+)-(\d+)-\d+\s*\([\d.]+%\)/;
    const vsRanked = parseRecord(section, vsRankedPattern);

    // Parse vs Top 10 - pattern: "4-8-0 (12 games)" or "4-7-0 (11 games)"
    const vsTop10Pattern = isAway
      ? /Vs Top 10 Teams\s+(\d+)-(\d+)-\d+/
      : /Vs Top 10 Teams\s+\d+-\d+-\d+.*?(\d+)-(\d+)-\d+/;
    const vsTop10 = parseRecord(section, vsTop10Pattern);

    // Parse vs Top 5 - pattern: "3-4-0 (7 games)" or "2-3-0 (5 games)"
    const vsTop5Pattern = isAway
      ? /Vs Top 5 Teams\s+(\d+)-(\d+)-\d+/
      : /Vs Top 5 Teams\s+\d+-\d+-\d+.*?(\d+)-(\d+)-\d+/;
    const vsTop5 = parseRecord(section, vsTop5Pattern);

    // Parse conference records
    const parseConferenceRecord = (conf: string) => {
      const confPattern = isAway
        ? new RegExp(`vs Ranked ${conf}\\s+(\\d+)-(\\d+)-\\d+`)
        : new RegExp(`vs Ranked ${conf}\\s+\\d+-\\d+-\\d+.*?(\\d+)-(\\d+)-\\d+`);
      const match = section.match(confPattern);
      if (match) {
        const wins = parseInt(match[1]);
        const losses = parseInt(match[2]);
        return { wins, losses, total: wins + losses };
      }
      return { wins: 0, losses: 0, total: 0 };
    };

    return {
      name: coachName,
      team: team.name,
      logo: team.logo,
      color: team.primary_color,
      vsRanked,
      vsTop10,
      vsTop5,
      conferenceVsRanked: {
        'ACC': parseConferenceRecord('ACC'),
        'Big Ten': parseConferenceRecord('Big Ten'),
        'Big 12': parseConferenceRecord('Big 12'),
        'SEC': parseConferenceRecord('SEC')
      }
    };
  };

  const coach1 = parseCoachingData(awayTeam, true);
  const coach2 = parseCoachingData(homeTeam, false);
  
  const coach1IsElite = coach1.vsRanked.percentage > 65;
  const coach2IsElite = coach2.vsRanked.percentage > 65;

  return (
    <div className="rounded-xl border backdrop-blur-md shadow-lg p-6" style={{
      background: `linear-gradient(135deg, ${coach1.color}08, ${coach2.color}05, ${coach1.color}06)`,
      borderColor: `${coach1.color}40`,
      boxShadow: `0 0 20px ${coach1.color}15`
    }}>
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg border" style={{
          background: `linear-gradient(135deg, ${coach1.color}20, ${coach2.color}15)`,
          borderColor: `${coach1.color}40`
        }}>
          <Users className="w-5 h-5" style={{ color: `${coach1.color}` }} />
        </div>
        <h3 className="text-white font-semibold">Elite vs Ranked Performance Analysis</h3>
      </div>

      {/* Coach Headers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <TeamHeader coach={coach1} isElite={coach1IsElite} />
        <TeamHeader coach={coach2} isElite={coach2IsElite} />
      </div>

      {/* Big Game Performance Summary */}
      <div className="mb-8">
        <h4 className="text-gray-300 font-semibold mb-4 flex items-center gap-2">
          <Trophy className="w-4 h-4 text-yellow-400" />
          Big Game Performance Summary
        </h4>
        
        <div className="rounded-xl p-6 border backdrop-blur-lg shadow-xl" style={{
          background: `linear-gradient(to bottom right, ${coach1.color}10, ${coach2.color}10, ${coach1.color}08)`,
          borderColor: `${coach1.color}20`,
          backdropFilter: 'blur(16px) saturate(180%)',
          WebkitBackdropFilter: 'blur(16px) saturate(180%)'
        }}>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-600/40">
                  <th className="text-left py-3 px-4 text-gray-300 font-medium">Performance Level</th>
                  <th className="text-center py-3 px-4 font-medium">
                    <div className="flex items-center justify-center gap-2">
                      <ImageWithFallback 
                        src={coach1.logo}
                        alt={coach1.team}
                        className="w-6 h-6 object-contain opacity-90"
                      />
                      <span style={{ color: coach1.color }}>{coach1.name}</span>
                    </div>
                  </th>
                  <th className="text-center py-3 px-4 font-medium">
                    <div className="flex items-center justify-center gap-2">
                      <ImageWithFallback 
                        src={coach2.logo}
                        alt={coach2.team}
                        className="w-6 h-6 object-contain opacity-90"
                      />
                      <span style={{ color: coach2.color }}>{coach2.name}</span>
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
          <div className="rounded-xl p-6 border backdrop-blur-lg shadow-lg" style={{
            background: `linear-gradient(to bottom right, ${coach1.color}20, ${coach1.color}10)`,
            borderColor: `${coach1.color}30`,
            backdropFilter: 'blur(12px) saturate(160%)',
            WebkitBackdropFilter: 'blur(12px) saturate(160%)'
          }}>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback 
                src={coach1.logo}
                alt={coach1.team}
                className="w-8 h-8 object-contain opacity-90"
                style={{ filter: `drop-shadow(0 0 4px ${coach1.color}40)` }}
              />
              <h5 className="font-semibold text-white">{coach1.name} vs Ranked</h5>
            </div>
            <div className="space-y-3">
              {Object.entries(coach1.conferenceVsRanked).map(([conference, data]: [string, any]) => (
                <div key={conference} className="flex justify-between items-center p-3 rounded-lg backdrop-blur-sm border border-white/5" style={{
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
                      <CheckCircle className="w-4 h-4 text-green-400 mx-auto mt-1" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Coach 2 Conference Performance */}
          <div className="rounded-xl p-6 border backdrop-blur-lg shadow-lg" style={{
            background: `linear-gradient(to bottom right, ${coach2.color}20, ${coach2.color}10)`,
            borderColor: `${coach2.color}30`,
            backdropFilter: 'blur(12px) saturate(160%)',
            WebkitBackdropFilter: 'blur(12px) saturate(160%)'
          }}>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback 
                src={coach2.logo}
                alt={coach2.team}
                className="w-8 h-8 object-contain opacity-90"
                style={{ filter: `drop-shadow(0 0 4px ${coach2.color}40)` }}
              />
              <h5 className="font-semibold text-white">{coach2.name} vs Ranked</h5>
            </div>
            <div className="space-y-3">
              {Object.entries(coach2.conferenceVsRanked).map(([conference, data]: [string, any]) => (
                <div key={conference} className="flex justify-between items-center p-3 rounded-lg backdrop-blur-sm border border-white/5" style={{
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
                      <CheckCircle className="w-4 h-4 text-green-400 mx-auto mt-1" />
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
        
        <div className="rounded-xl p-6 border backdrop-blur-xl shadow-2xl" style={{
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
              <div key={index} className="rounded-lg p-4 backdrop-blur-md shadow-lg border border-gray-400/15" style={{
                background: `linear-gradient(135deg, ${coach1.color}18, ${coach2.color}15)`,
                backdropFilter: 'blur(8px) saturate(140%)',
                WebkitBackdropFilter: 'blur(8px) saturate(140%)'
              }}>
                <h6 className="text-gray-300 font-medium mb-3 text-center">{metric.label}</h6>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <ImageWithFallback 
                        src={coach1.logo}
                        alt={coach1.team}
                        className="w-4 h-4 object-contain opacity-90"
                      />
                      <span className="text-xs text-gray-400">{coach1.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`font-bold ${metric.coach1 >= metric.threshold ? 'text-green-400' : 'text-red-400'}`}>
                        {metric.coach1}%
                      </span>
                      {metric.coach1 >= metric.threshold && <CheckCircle className="w-4 h-4 text-green-400" />}
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <ImageWithFallback 
                        src={coach2.logo}
                        alt={coach2.team}
                        className="w-4 h-4 object-contain opacity-90"
                      />
                      <span className="text-xs text-gray-400">{coach2.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`font-bold ${metric.coach2 >= metric.threshold ? 'text-green-400' : 'text-red-400'}`}>
                        {metric.coach2}%
                      </span>
                      {metric.coach2 >= metric.threshold && <CheckCircle className="w-4 h-4 text-green-400" />}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}