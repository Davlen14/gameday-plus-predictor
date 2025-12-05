import React from 'react';

const RivalryHistoryCard = ({ rivalryData, predictionData }) => {
  if (!rivalryData) return null;

  const { name, trophy, established, stats, recent_games } = rivalryData;
  
  if (!stats) return null;

  // Get team data directly from predictionData (same as ATS component)
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "", color: "#374151", alt_color: "#6B7280" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "", color: "#374151", alt_color: "#6B7280" };

  // Helper function to detect if color is too dark (same as ATS)
  const isBlueOrBlack = (color) => {
    if (!color) return false;
    const hex = color.replace('#', '').toLowerCase();
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    const isDark = (r + g + b) < 180;
    const isBlueish = b > r && b > g;
    return isDark || isBlueish;
  };

  const awayColor = isBlueOrBlack(awayTeam.color) ? (awayTeam.alt_color || '#3B82F6') : awayTeam.color;
  const homeColor = isBlueOrBlack(homeTeam.color) ? (homeTeam.alt_color || '#10B981') : homeTeam.color;

  return (
    <div className="relative bg-[#1a1d24]/40 backdrop-blur-sm border border-gray-800/50 rounded-lg p-6 mb-6">
      {/* Header */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-1">
          {name}
        </h3>
        {trophy && (
          <p className="text-sm text-gray-400">
            {trophy}
          </p>
        )}
      </div>

      {/* Season Label */}
      <div className="text-center mb-4">
        <span className="text-xs font-semibold text-gray-400 tracking-wider">
          ALL-TIME SERIES
        </span>
      </div>

      {/* Season Label */}
      <div className="text-center mb-4">
        <span className="text-xs font-semibold text-gray-400 tracking-wider">
          ALL-TIME SERIES
        </span>
      </div>

      {/* Team Stats Grid */}
      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* Away Team */}
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            {awayTeam.logo && (
              <img 
                src={awayTeam.logo} 
                alt={awayTeam.name}
                className="w-12 h-12 object-contain"
              />
            )}
            <div>
              <div className="text-sm font-semibold text-white">{awayTeam.name}</div>
              <div className="text-xs text-gray-500">Away Team</div>
            </div>
          </div>
          
          <div 
            className="bg-[#0f1117]/60 backdrop-blur-sm border rounded p-4"
            style={{ borderColor: `${awayColor}40` }}
          >
            <div className="text-xs text-gray-400 mb-1">Series Record</div>
            <div className="text-2xl font-bold" style={{ color: awayColor }}>
              {stats.team1_wins}-{stats.team2_wins}
            </div>
            <div className="text-xs text-gray-500 mt-2">Win Rate</div>
            <div className="text-sm font-semibold text-white mt-1">
              {(stats.team1_wins / stats.total_games * 100).toFixed(1)}%
            </div>
            {stats.team1_wins > stats.team2_wins && (
              <div className="mt-2 flex items-center gap-1">
                <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                </svg>
                <span className="text-xs font-semibold text-green-500">LEADS SERIES</span>
              </div>
            )}
          </div>

          <div 
            className="bg-[#0f1117]/60 backdrop-blur-sm border rounded p-4"
            style={{ borderColor: `${awayColor}30` }}
          >
            <div className="text-xs text-gray-400 mb-1">Avg Points/Game</div>
            <div className="text-2xl font-bold text-white">
              {(stats.team1_points / stats.total_games).toFixed(1)}
            </div>
          </div>
        </div>

        {/* Home Team */}
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            {homeTeam.logo && (
              <img 
                src={homeTeam.logo} 
                alt={homeTeam.name}
                className="w-12 h-12 object-contain"
              />
            )}
            <div>
              <div className="text-sm font-semibold text-white">{homeTeam.name}</div>
              <div className="text-xs text-gray-500">Home Team</div>
            </div>
          </div>
          
          <div 
            className="bg-[#0f1117]/60 backdrop-blur-sm border rounded p-4"
            style={{ borderColor: `${homeColor}40` }}
          >
            <div className="text-xs text-gray-400 mb-1">Series Record</div>
            <div className="text-2xl font-bold" style={{ color: homeColor }}>
              {stats.team2_wins}-{stats.team1_wins}
            </div>
            <div className="text-xs text-gray-500 mt-2">Win Rate</div>
            <div className="text-sm font-semibold text-white mt-1">
              {(stats.team2_wins / stats.total_games * 100).toFixed(1)}%
            </div>
            {stats.team2_wins > stats.team1_wins && (
              <div className="mt-2 flex items-center gap-1">
                <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                </svg>
                <span className="text-xs font-semibold text-green-500">LEADS SERIES</span>
              </div>
            )}
          </div>

          <div 
            className="bg-[#0f1117]/60 backdrop-blur-sm border rounded p-4"
            style={{ borderColor: `${homeColor}30` }}
          >
            <div className="text-xs text-gray-400 mb-1">Avg Points/Game</div>
            <div className="text-2xl font-bold text-white">
              {(stats.team2_points / stats.total_games).toFixed(1)}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Games */}
      {recent_games && recent_games.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-white mb-3">
            Recent Matchups (Last {Math.min(recent_games.length, 10)})
          </h4>
          <div className="space-y-2">
            {recent_games.slice(0, 10).map((game, index) => {
              const awayWon = game.awayPoints > game.homePoints;
              const homeWon = game.homePoints > game.awayPoints;
              
              // Match game teams with current prediction teams
              const isHomeTeamMatch = game.homeTeam.toLowerCase().includes(homeTeam.name.toLowerCase()) || 
                                     homeTeam.name.toLowerCase().includes(game.homeTeam.toLowerCase());
              const isAwayTeamMatch = game.awayTeam.toLowerCase().includes(awayTeam.name.toLowerCase()) || 
                                     awayTeam.name.toLowerCase().includes(game.awayTeam.toLowerCase());
              
              const gameHomeTeam = isHomeTeamMatch ? homeTeam : (isAwayTeamMatch ? awayTeam : { name: game.homeTeam, logo: '', color: homeColor });
              const gameAwayTeam = isAwayTeamMatch ? awayTeam : (isHomeTeamMatch ? homeTeam : { name: game.awayTeam, logo: '', color: awayColor });

              return (
                <div 
                  key={index} 
                  className="bg-[#0f1117]/60 backdrop-blur-sm border border-gray-800/50 rounded p-3"
                >
                  <div className="flex items-center justify-between mb-2">
                    {/* Away Team */}
                    <div className="flex items-center gap-2 flex-1">
                      {gameAwayTeam.logo && (
                        <img 
                          src={gameAwayTeam.logo} 
                          alt={game.awayTeam}
                          className="w-6 h-6 object-contain"
                        />
                      )}
                      <span className={`text-sm ${awayWon ? 'font-semibold text-white' : 'text-gray-400'}`}>
                        {game.awayTeam}
                      </span>
                      {awayWon && (
                        <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <span className={`text-lg font-bold ${awayWon ? 'text-white' : 'text-gray-500'}`}>
                        {game.awayPoints}
                      </span>
                      <span className="text-gray-600">-</span>
                      <span className={`text-lg font-bold ${homeWon ? 'text-white' : 'text-gray-500'}`}>
                        {game.homePoints}
                      </span>
                    </div>

                    {/* Home Team */}
                    <div className="flex items-center gap-2 flex-1 justify-end">
                      {homeWon && (
                        <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                        </svg>
                      )}
                      <span className={`text-sm ${homeWon ? 'font-semibold text-white' : 'text-gray-400'}`}>
                        {game.homeTeam}
                      </span>
                      {gameHomeTeam.logo && (
                        <img 
                          src={gameHomeTeam.logo} 
                          alt={game.homeTeam}
                          className="w-6 h-6 object-contain"
                        />
                      )}
                    </div>
                  </div>

                  {/* Game Info */}
                  <div className="text-xs text-gray-500">
                    {game.season} Season • Week {game.week}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Rivalry Intelligence */}
      <div className="bg-[#0f1117]/60 backdrop-blur-sm border border-gray-800/50 rounded p-4">
        <h4 className="text-sm font-semibold text-white mb-3">
          Rivalry Intelligence
        </h4>
        <div className="text-sm text-gray-300 leading-relaxed">
          <span style={{ color: stats.team1_wins > stats.team2_wins ? awayColor : homeColor, fontWeight: 600 }}>
            {stats.team1_wins > stats.team2_wins ? awayTeam.name : homeTeam.name}
          </span> leads the series {Math.max(stats.team1_wins, stats.team2_wins)}-{Math.min(stats.team1_wins, stats.team2_wins)} over {stats.total_games} all-time matchups. 
          The home team has won {((stats.home_wins / stats.total_games) * 100).toFixed(1)}% of games in this rivalry. 
          Average combined score is {((stats.team1_points + stats.team2_points) / stats.total_games).toFixed(1)} points per game.
        </div>
      </div>

      {/* What is this section */}
      <div className="mt-4 pt-4 border-t border-gray-800">
        <p className="text-xs text-gray-400 leading-relaxed">
          <span className="font-semibold text-gray-300">What is Rivalry History?</span> Historic rivalry matchups show head-to-head performance between traditional opponents. Series records and recent trends can indicate psychological advantages and competitive patterns that may influence current game outcomes.
        </p>
      </div>
    </div>
  );
};

export default RivalryHistoryCard;
