import React from 'react';

interface PowerRankingData {
  rank: number;
  team: string;
  conference: string;
  overall_score: number;
  offensive_score: number;
  defensive_score: number;
  total_metrics_analyzed: number;
}

interface OverallPowerRankingsProps {
  homeTeam: string;
  awayTeam: string;
  homeData?: PowerRankingData;
  awayData?: PowerRankingData;
}

const OverallPowerRankings: React.FC<OverallPowerRankingsProps> = ({
  homeTeam,
  awayTeam,
  homeData,
  awayData,
}) => {
  if (!homeData || !awayData) {
    return (
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h3 className="text-xl font-bold text-white mb-4">Overall Power Rankings</h3>
        <p className="text-gray-300">Power rankings not available</p>
      </div>
    );
  }

  const calculateDifferential = (away: number, home: number) => {
    const diff = away - home;
    return {
      value: Math.abs(diff),
      advantage: diff > 0 ? 'away' : diff < 0 ? 'home' : 'even' as 'away' | 'home' | 'even'
    };
  };

  const overallDiff = calculateDifferential(awayData.overall_score, homeData.overall_score);
  const offenseDiff = calculateDifferential(awayData.offensive_score, homeData.offensive_score);
  const defenseDiff = calculateDifferential(awayData.defensive_score, homeData.defensive_score);
  const rankDiff = calculateDifferential(homeData.rank, awayData.rank); // Lower rank = better

  const getMatchQuality = () => {
    const scoreDiff = Math.abs(awayData.overall_score - homeData.overall_score);
    if (scoreDiff > 20) return { level: 'Heavy Mismatch', color: 'text-red-400' };
    if (scoreDiff > 10) return { level: 'Clear Favorite', color: 'text-orange-400' };
    if (scoreDiff > 5) return { level: 'Moderate Advantage', color: 'text-yellow-400' };
    return { level: 'Even Matchup', color: 'text-green-400' };
  };

  const matchQuality = getMatchQuality();

  const renderScoreBar = (score: number, maxScore: number = 100) => {
    const percentage = (score / maxScore) * 100;
    let colorClass = 'bg-red-500';
    if (percentage >= 70) colorClass = 'bg-green-500';
    else if (percentage >= 50) colorClass = 'bg-yellow-500';
    else if (percentage >= 30) colorClass = 'bg-orange-500';

    return (
      <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
        <div 
          className={`${colorClass} h-full transition-all duration-500 ease-out`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
    );
  };

  return (
    <div className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 backdrop-blur-xl rounded-2xl p-8 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h3 className="text-3xl font-bold text-white flex items-center gap-3">
          <span className="text-4xl">🏆</span>
          Overall Power Rankings
        </h3>
        <div className={`text-lg font-bold ${matchQuality.color} px-4 py-2 bg-white/10 rounded-xl`}>
          {matchQuality.level}
        </div>
      </div>

      {/* Team Names & Ranks */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-6 mb-8 pb-6 border-b-2 border-white/30">
        <div className="text-right">
          <div className="text-2xl font-bold text-white mb-1">{awayTeam}</div>
          <div className="text-sm text-gray-400 mb-2">{awayData.conference}</div>
          <div className="inline-block bg-blue-500/20 px-4 py-2 rounded-lg">
            <div className="text-xs text-gray-400">National Rank</div>
            <div className="text-3xl font-bold text-blue-400">#{awayData.rank}</div>
          </div>
        </div>

        <div className="text-center px-4">
          <div className="text-xs text-gray-400 mb-2">Rank Differential</div>
          <div className={`text-2xl font-bold px-4 py-2 rounded-lg ${
            rankDiff.advantage === 'away' 
              ? 'bg-blue-500/20 text-blue-400' 
              : rankDiff.advantage === 'home'
              ? 'bg-purple-500/20 text-purple-400'
              : 'bg-gray-500/20 text-gray-400'
          }`}>
            {rankDiff.value}
          </div>
        </div>

        <div className="text-left">
          <div className="text-2xl font-bold text-white mb-1">{homeTeam}</div>
          <div className="text-sm text-gray-400 mb-2">{homeData.conference}</div>
          <div className="inline-block bg-purple-500/20 px-4 py-2 rounded-lg">
            <div className="text-xs text-gray-400">National Rank</div>
            <div className="text-3xl font-bold text-purple-400">#{homeData.rank}</div>
          </div>
        </div>
      </div>

      {/* Overall Score Comparison */}
      <div className="mb-8">
        <div className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
          <span>⭐</span> Overall Power Score
        </div>
        
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-6 mb-4">
          <div className="text-right">
            <div className="text-4xl font-bold text-blue-400 mb-2">{awayData.overall_score.toFixed(2)}</div>
            {renderScoreBar(awayData.overall_score)}
          </div>

          <div className={`px-6 py-3 rounded-xl ${
            overallDiff.advantage === 'away' 
              ? 'bg-blue-500/30 text-blue-300' 
              : overallDiff.advantage === 'home'
              ? 'bg-purple-500/30 text-purple-300'
              : 'bg-gray-500/30 text-gray-300'
          }`}>
            <div className="text-xs mb-1">Differential</div>
            <div className="text-2xl font-bold">{overallDiff.value.toFixed(2)}</div>
          </div>

          <div className="text-left">
            <div className="text-4xl font-bold text-purple-400 mb-2">{homeData.overall_score.toFixed(2)}</div>
            {renderScoreBar(homeData.overall_score)}
          </div>
        </div>
      </div>

      {/* Offensive Score */}
      <div className="mb-6">
        <div className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
          <span>⚡</span> Offensive Power
        </div>
        
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-6">
          <div className="text-right">
            <div className="text-2xl font-bold text-green-400 mb-2">{awayData.offensive_score.toFixed(2)}</div>
            {renderScoreBar(awayData.offensive_score)}
          </div>

          <div className={`px-4 py-2 rounded-lg ${
            offenseDiff.advantage === 'away' 
              ? 'bg-green-500/20 text-green-400' 
              : offenseDiff.advantage === 'home'
              ? 'bg-green-500/20 text-green-400'
              : 'bg-gray-500/20 text-gray-400'
          }`}>
            <div className="text-lg font-bold">{offenseDiff.advantage === 'away' ? '+' : offenseDiff.advantage === 'home' ? '-' : ''}{offenseDiff.value.toFixed(2)}</div>
          </div>

          <div className="text-left">
            <div className="text-2xl font-bold text-green-400 mb-2">{homeData.offensive_score.toFixed(2)}</div>
            {renderScoreBar(homeData.offensive_score)}
          </div>
        </div>
      </div>

      {/* Defensive Score */}
      <div className="mb-6">
        <div className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
          <span>🛡️</span> Defensive Power
        </div>
        
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-6">
          <div className="text-right">
            <div className="text-2xl font-bold text-red-400 mb-2">{awayData.defensive_score.toFixed(2)}</div>
            {renderScoreBar(awayData.defensive_score)}
          </div>

          <div className={`px-4 py-2 rounded-lg ${
            defenseDiff.advantage === 'away' 
              ? 'bg-red-500/20 text-red-400' 
              : defenseDiff.advantage === 'home'
              ? 'bg-red-500/20 text-red-400'
              : 'bg-gray-500/20 text-gray-400'
          }`}>
            <div className="text-lg font-bold">{defenseDiff.advantage === 'away' ? '+' : defenseDiff.advantage === 'home' ? '-' : ''}{defenseDiff.value.toFixed(2)}</div>
          </div>

          <div className="text-left">
            <div className="text-2xl font-bold text-red-400 mb-2">{homeData.defensive_score.toFixed(2)}</div>
            {renderScoreBar(homeData.defensive_score)}
          </div>
        </div>
      </div>

      {/* Meta Information */}
      <div className="mt-8 pt-6 border-t border-white/20 grid grid-cols-2 gap-4 text-sm">
        <div className="bg-white/5 rounded-lg p-4">
          <div className="text-gray-400 mb-1">Total Metrics Analyzed</div>
          <div className="text-2xl font-bold text-white">{awayData.total_metrics_analyzed}</div>
        </div>
        <div className="bg-white/5 rounded-lg p-4">
          <div className="text-gray-400 mb-1">Data Coverage</div>
          <div className="text-2xl font-bold text-white">167 Stats/Team</div>
        </div>
      </div>

      {/* Advantage Summary */}
      <div className="mt-6 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-white/10">
        <div className="text-sm font-semibold text-white mb-3">Match Analysis</div>
        <div className="grid grid-cols-3 gap-4 text-center text-sm">
          <div>
            <div className="text-gray-400 mb-1">Overall Edge</div>
            <div className={`font-bold ${overallDiff.advantage === 'away' ? 'text-blue-400' : overallDiff.advantage === 'home' ? 'text-purple-400' : 'text-gray-400'}`}>
              {overallDiff.advantage === 'away' ? awayTeam : overallDiff.advantage === 'home' ? homeTeam : 'Even'}
            </div>
          </div>
          <div>
            <div className="text-gray-400 mb-1">Offensive Edge</div>
            <div className={`font-bold ${offenseDiff.advantage === 'away' ? 'text-blue-400' : offenseDiff.advantage === 'home' ? 'text-purple-400' : 'text-gray-400'}`}>
              {offenseDiff.advantage === 'away' ? awayTeam : offenseDiff.advantage === 'home' ? homeTeam : 'Even'}
            </div>
          </div>
          <div>
            <div className="text-gray-400 mb-1">Defensive Edge</div>
            <div className={`font-bold ${defenseDiff.advantage === 'away' ? 'text-blue-400' : defenseDiff.advantage === 'home' ? 'text-purple-400' : 'text-gray-400'}`}>
              {defenseDiff.advantage === 'away' ? awayTeam : defenseDiff.advantage === 'home' ? homeTeam : 'Even'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OverallPowerRankings;
