import React, { useState } from 'react';
import './FieldVisualization.css';

interface Player {
  name: string;
  number: string;
  position: string;
  image?: string;
  stats: {
    primary: { label: string; value: string | number };
    secondary: { label: string; value: string | number };
    tertiary: { label: string; value: string | number };
  };
}

interface Play {
  id: string;
  quarter: number;
  time: string;
  down: string;
  distance: number;
  yardLine: string;
  description: string;
  yards: number;
  playType: 'run' | 'pass' | 'penalty' | 'punt' | 'fieldGoal' | 'touchdown' | 'interception';
  player?: {
    name: string;
    number: string;
    image?: string;
  };
}

interface DriveStats {
  plays: number;
  yards: number;
  timeOfPossession: string;
  thirdDowns?: string;
  redZone?: boolean;
  result?: 'touchdown' | 'fieldGoal' | 'punt' | 'turnover' | 'inProgress';
}

interface FieldVisualizationProps {
  possession: {
    team: string;
    logo?: string;
  };
  fieldPosition: {
    yardLine: number;
    down: number;
    distance: number;
  };
  homeTeam: {
    name: string;
    abbr?: string;
    color: string;
    logo?: string;
  };
  awayTeam: {
    name: string;
    abbr?: string;
    color: string;
    logo?: string;
  };
  situation?: string;
  recentPlays?: Play[];
  keyPlayers?: Player[];
  driveStats?: DriveStats;
  quarter?: number;
  score?: { home: number; away: number };
}

const FieldVisualizationModern: React.FC<FieldVisualizationProps> = ({
  possession,
  fieldPosition,
  homeTeam,
  awayTeam,
  situation,
  recentPlays = [],
  keyPlayers = [],
  driveStats,
  quarter = 4,
  score
}) => {
  const [selectedPlay, setSelectedPlay] = useState<string | null>(null);

  const getOrdinalSuffix = (num: number): string => {
    const j = num % 10;
    const k = num % 100;
    if (j === 1 && k !== 11) return num + 'st';
    if (j === 2 && k !== 12) return num + 'nd';
    if (j === 3 && k !== 13) return num + 'rd';
    return num + 'th';
  };

  const getPlayTypeColor = (playType: string): string => {
    switch (playType) {
      case 'touchdown': return 'from-green-500/20 to-green-600/20 border-green-400';
      case 'pass': return 'from-blue-500/20 to-blue-600/20 border-blue-400';
      case 'run': return 'from-orange-500/20 to-orange-600/20 border-orange-400';
      case 'penalty': return 'from-yellow-500/20 to-yellow-600/20 border-yellow-400';
      case 'interception': return 'from-red-500/20 to-red-600/20 border-red-400';
      case 'punt': return 'from-gray-500/20 to-gray-600/20 border-gray-400';
      default: return 'from-gray-500/20 to-gray-600/20 border-gray-400';
    }
  };

  const getPlayTypeIcon = (playType: string): string => {
    switch (playType) {
      case 'touchdown': return '🏈';
      case 'pass': return '➡️';
      case 'run': return '🏃';
      case 'penalty': return '⚠️';
      case 'interception': return '🔄';
      case 'punt': return '⬆️';
      case 'fieldGoal': return '🎯';
      default: return '•';
    }
  };

  // Calculate ball position percentage
  const ballPosition = ((fieldPosition.yardLine) / 100) * 100;
  const isHomeTeamPossession = possession.team === homeTeam.name;

  return (
    <div className="w-full space-y-6">
      {/* Header with Score and Quarter */}
      {score && (
        <div className="flex items-center justify-between bg-gradient-to-r from-gray-900/40 via-gray-800/40 to-gray-900/40 backdrop-blur-xl rounded-2xl border border-white/10 p-4 shadow-2xl">
          <div className="flex items-center gap-4">
            {awayTeam.logo && (
              <img src={awayTeam.logo} alt={awayTeam.name} className="w-12 h-12 object-contain" />
            )}
            <div>
              <div className="text-white/60 text-xs font-medium">{awayTeam.name}</div>
              <div className="text-white text-3xl font-bold">{score.away}</div>
            </div>
          </div>
          
          <div className="text-center px-6">
            <div className="text-white/60 text-xs font-medium mb-1">QUARTER</div>
            <div className="text-white text-2xl font-bold">{getOrdinalSuffix(quarter)}</div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-white/60 text-xs font-medium">{homeTeam.name}</div>
              <div className="text-white text-3xl font-bold">{score.home}</div>
            </div>
            {homeTeam.logo && (
              <img src={homeTeam.logo} alt={homeTeam.name} className="w-12 h-12 object-contain" />
            )}
          </div>
        </div>
      )}

      {/* Main Field Visualization with Drive Stats */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Sidebar - Key Players */}
        {keyPlayers.length > 0 && (
          <div className="lg:col-span-1 space-y-4">
            <h3 className="text-white font-semibold text-lg mb-4">Key Players</h3>
            {keyPlayers.map((player, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-br from-gray-900/40 to-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 p-4 shadow-2xl hover:border-white/30 transition-all duration-300 hover:scale-[1.02]"
              >
                <div className="flex items-center gap-4">
                  {player.image ? (
                    <img 
                      src={player.image} 
                      alt={player.name}
                      className="w-16 h-16 rounded-full object-cover border-2 border-white/20"
                    />
                  ) : (
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-white/20 flex items-center justify-center">
                      <span className="text-white text-xl font-bold">#{player.number}</span>
                    </div>
                  )}
                  <div className="flex-1">
                    <div className="text-white font-bold text-sm">{player.name}</div>
                    <div className="text-white/60 text-xs">{player.position} • #{player.number}</div>
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-2 mt-4 pt-4 border-t border-white/10">
                  <div className="text-center">
                    <div className="text-white text-lg font-bold">{player.stats.primary.value}</div>
                    <div className="text-white/60 text-xs">{player.stats.primary.label}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-white text-lg font-bold">{player.stats.secondary.value}</div>
                    <div className="text-white/60 text-xs">{player.stats.secondary.label}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-white text-lg font-bold">{player.stats.tertiary.value}</div>
                    <div className="text-white/60 text-xs">{player.stats.tertiary.label}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Center - Football Field */}
        <div className={keyPlayers.length > 0 ? "lg:col-span-2" : "lg:col-span-3"}>
          <div className="bg-gradient-to-br from-gray-900/40 to-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 p-6 shadow-2xl">
            {/* Current Drive Stats */}
            {driveStats && (
              <div className="mb-6 grid grid-cols-4 gap-4">
                <div className="text-center bg-white/5 rounded-lg p-3 backdrop-blur-sm">
                  <div className="text-white text-2xl font-bold">{driveStats.plays}</div>
                  <div className="text-white/60 text-xs">Plays</div>
                </div>
                <div className="text-center bg-white/5 rounded-lg p-3 backdrop-blur-sm">
                  <div className="text-white text-2xl font-bold">{driveStats.yards}</div>
                  <div className="text-white/60 text-xs">Yards</div>
                </div>
                <div className="text-center bg-white/5 rounded-lg p-3 backdrop-blur-sm">
                  <div className="text-white text-xl font-bold">{driveStats.timeOfPossession}</div>
                  <div className="text-white/60 text-xs">Time</div>
                </div>
                {driveStats.thirdDowns && (
                  <div className="text-center bg-white/5 rounded-lg p-3 backdrop-blur-sm">
                    <div className="text-white text-xl font-bold">{driveStats.thirdDowns}</div>
                    <div className="text-white/60 text-xs">3rd Down</div>
                  </div>
                )}
              </div>
            )}

            {/* Field Visualization */}
            <div className="relative h-40 mb-6">
              {/* Away Team Endzone */}
              <div 
                className="absolute left-0 top-0 w-[10%] h-full rounded-l-xl flex items-center justify-center overflow-hidden"
                style={{
                  background: `linear-gradient(135deg, ${awayTeam.color}40, ${awayTeam.color}20)`,
                  borderRight: `2px solid ${awayTeam.color}80`
                }}
              >
                {awayTeam.logo && (
                  <img 
                    src={awayTeam.logo} 
                    alt={awayTeam.name}
                    className="w-8 h-8 object-contain opacity-60"
                  />
                )}
              </div>

              {/* Field */}
              <div className="absolute left-[10%] right-[10%] top-0 h-full bg-gradient-to-r from-green-900/40 via-green-800/40 to-green-900/40 border-y-2 border-white/20">
                {/* Yard Lines */}
                {[10, 20, 30, 40, 50, 40, 30, 20, 10].map((yard, idx) => (
                  <div
                    key={idx}
                    className="absolute top-0 bottom-0 border-l border-white/20"
                    style={{ left: `${(idx + 1) * 10}%` }}
                  >
                    <div className="text-white/40 text-xs font-mono absolute top-1/2 -translate-y-1/2 -translate-x-1/2 bg-black/20 px-1 rounded">
                      {yard}
                    </div>
                  </div>
                ))}

                {/* Ball Position */}
                <div
                  className="absolute top-0 bottom-0 w-1 bg-gradient-to-b from-yellow-400 to-orange-500 shadow-lg shadow-yellow-500/50 transition-all duration-500"
                  style={{ left: `${ballPosition}%` }}
                >
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 border-2 border-white shadow-xl flex items-center justify-center">
                    {possession.logo ? (
                      <img src={possession.logo} alt="" className="w-5 h-5 object-contain" />
                    ) : (
                      <div className="w-3 h-3 bg-white rounded-full"></div>
                    )}
                  </div>
                </div>
              </div>

              {/* Home Team Endzone */}
              <div 
                className="absolute right-0 top-0 w-[10%] h-full rounded-r-xl flex items-center justify-center overflow-hidden"
                style={{
                  background: `linear-gradient(135deg, ${homeTeam.color}40, ${homeTeam.color}20)`,
                  borderLeft: `2px solid ${homeTeam.color}80`
                }}
              >
                {homeTeam.logo && (
                  <img 
                    src={homeTeam.logo} 
                    alt={homeTeam.name}
                    className="w-8 h-8 object-contain opacity-60"
                  />
                )}
              </div>
            </div>

            {/* Down and Distance */}
            <div className="text-center">
              <div className="inline-flex items-center gap-4 bg-white/5 backdrop-blur-sm rounded-xl px-6 py-3 border border-white/10">
                <div>
                  <span className="text-white text-2xl font-bold">{getOrdinalSuffix(fieldPosition.down)}</span>
                  <span className="text-white/60 text-lg"> & </span>
                  <span className="text-white text-2xl font-bold">{fieldPosition.distance}</span>
                </div>
                <div className="text-white/60">•</div>
                <div className="text-white/80 text-sm font-medium">
                  Ball on {possession.team === awayTeam.name ? awayTeam.abbr || awayTeam.name : homeTeam.abbr || homeTeam.name} {fieldPosition.yardLine}
                </div>
              </div>
            </div>
          </div>

          {/* Recent Plays Timeline */}
          {recentPlays.length > 0 && (
            <div className="mt-6 bg-gradient-to-br from-gray-900/40 to-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 p-6 shadow-2xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-white font-semibold text-lg">Recent Plays</h3>
                <div className="text-white/60 text-sm">{recentPlays.length} plays</div>
              </div>
              
              <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
                {recentPlays.map((play) => (
                  <div
                    key={play.id}
                    onClick={() => setSelectedPlay(selectedPlay === play.id ? null : play.id)}
                    className={`bg-gradient-to-r ${getPlayTypeColor(play.playType)} backdrop-blur-sm rounded-xl p-4 border transition-all duration-300 cursor-pointer hover:scale-[1.02] ${
                      selectedPlay === play.id ? 'ring-2 ring-white/30' : ''
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      {/* Play Icon */}
                      <div className="text-2xl">{getPlayTypeIcon(play.playType)}</div>
                      
                      {/* Play Info */}
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <div className="text-white/80 text-xs font-medium">
                            Q{play.quarter} • {play.time} • {play.down} & {play.distance} at {play.yardLine}
                          </div>
                          <div className={`text-lg font-bold ${play.yards > 0 ? 'text-green-400' : play.yards < 0 ? 'text-red-400' : 'text-white/60'}`}>
                            {play.yards > 0 ? '+' : ''}{play.yards} yds
                          </div>
                        </div>
                        
                        <div className="text-white text-sm">{play.description}</div>
                        
                        {/* Player Info (expanded) */}
                        {selectedPlay === play.id && play.player && (
                          <div className="mt-3 pt-3 border-t border-white/10 flex items-center gap-3">
                            {play.player.image ? (
                              <img 
                                src={play.player.image} 
                                alt={play.player.name}
                                className="w-10 h-10 rounded-full object-cover border-2 border-white/20"
                              />
                            ) : (
                              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center border-2 border-white/20">
                                <span className="text-white text-xs font-bold">#{play.player.number}</span>
                              </div>
                            )}
                            <div>
                              <div className="text-white font-medium text-sm">{play.player.name}</div>
                              <div className="text-white/60 text-xs">#{play.player.number}</div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FieldVisualizationModern;
