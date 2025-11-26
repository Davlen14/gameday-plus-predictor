import React from 'react';

const RivalryHistoryCard = ({ rivalryData }) => {
  if (!rivalryData) {
    console.log('RivalryHistoryCard: No rivalry data provided');
    return null;
  }

  console.log('RivalryHistoryCard: Received rivalry data:', rivalryData);
  const { name, trophy, established, stats, recent_games } = rivalryData;
  
  if (!stats) {
    console.log('RivalryHistoryCard: No stats in rivalry data');
    return null;
  }

  return (
    <div className="rivalry-history-card glass-card p-6 rounded-2xl mb-6">
      {/* Header */}
      <div className="rivalry-header mb-6">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-3xl font-bold text-white flex items-center gap-3">
            <span className="text-4xl">🏆</span>
            {name}
          </h2>
          {established && (
            <span className="text-sm text-white/60">
              Est. {established}
            </span>
          )}
        </div>
        {trophy && (
          <p className="text-lg text-emerald-400 font-semibold">
            {trophy}
          </p>
        )}
      </div>

      {/* Series Statistics */}
      <div className="series-stats grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="stat-box glass-card-light p-4 rounded-xl text-center">
          <div className="text-2xl font-bold text-white">
            {stats.total_games}
          </div>
          <div className="text-sm text-white/70">Total Games</div>
        </div>
        
        <div className="stat-box glass-card-light p-4 rounded-xl text-center">
          <div className="text-2xl font-bold text-emerald-400">
            {stats.team1_wins}-{stats.team2_wins}
          </div>
          <div className="text-sm text-white/70">Series Record</div>
        </div>
        
        <div className="stat-box glass-card-light p-4 rounded-xl text-center">
          <div className="text-2xl font-bold text-blue-400">
            {stats.ranked_matchups}
          </div>
          <div className="text-sm text-white/70">Ranked Matchups</div>
        </div>
        
        <div className="stat-box glass-card-light p-4 rounded-xl text-center">
          <div className="text-2xl font-bold text-purple-400">
            {stats.top10_matchups}
          </div>
          <div className="text-sm text-white/70">Top 10 Clashes</div>
        </div>
      </div>

      {/* Additional Stats */}
      <div className="additional-stats grid grid-cols-2 gap-4 mb-6">
        <div className="glass-card-light p-4 rounded-xl">
          <div className="text-sm text-white/70 mb-1">Points Per Game</div>
          <div className="text-lg font-semibold text-white">
            {(stats.team1_points / stats.total_games).toFixed(1)} - {(stats.team2_points / stats.total_games).toFixed(1)}
          </div>
        </div>
        
        <div className="glass-card-light p-4 rounded-xl">
          <div className="text-sm text-white/70 mb-1">Home/Away Wins</div>
          <div className="text-lg font-semibold text-white">
            {stats.home_wins} Home / {stats.away_wins} Away
          </div>
        </div>
      </div>

      {/* Notable Games */}
      {(stats.closest_game || stats.biggest_blowout) && (
        <div className="notable-games grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {stats.closest_game && (
            <div className="glass-card-light p-4 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">🔥</span>
                <span className="text-sm font-semibold text-white/70">Closest Game</span>
              </div>
              <div className="text-white">
                <div className="font-bold">{stats.closest_game.season} Week {stats.closest_game.week}</div>
                <div className="text-sm">
                  {stats.closest_game.homeTeam} {stats.closest_game.homePoints} - {stats.closest_game.awayTeam} {stats.closest_game.awayPoints}
                </div>
                <div className="text-xs text-emerald-400 mt-1">
                  {Math.abs(stats.closest_game.homePoints - stats.closest_game.awayPoints)} point margin
                </div>
              </div>
            </div>
          )}
          
          {stats.biggest_blowout && (
            <div className="glass-card-light p-4 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">💥</span>
                <span className="text-sm font-semibold text-white/70">Biggest Blowout</span>
              </div>
              <div className="text-white">
                <div className="font-bold">{stats.biggest_blowout.season} Week {stats.biggest_blowout.week}</div>
                <div className="text-sm">
                  {stats.biggest_blowout.homeTeam} {stats.biggest_blowout.homePoints} - {stats.biggest_blowout.awayTeam} {stats.biggest_blowout.awayPoints}
                </div>
                <div className="text-xs text-red-400 mt-1">
                  {Math.abs(stats.biggest_blowout.homePoints - stats.biggest_blowout.awayPoints)} point margin
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Last 10 Meetings */}
      <div className="recent-games">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>📅</span>
          Last 10 Meetings
        </h3>
        
        <div className="games-list space-y-2">
          {recent_games.slice().reverse().map((game, idx) => {
            const homeWon = game.homePoints > game.awayPoints;
            
            return (
              <div 
                key={idx} 
                className="game-item glass-card-light p-3 rounded-lg flex items-center justify-between hover:bg-white/10 transition-all"
              >
                <div className="flex items-center gap-3 flex-1">
                  <div className="text-xs font-semibold text-white/60 w-16">
                    {game.season}
                  </div>
                  <div className="text-xs text-white/50 w-16">
                    Week {game.week}
                  </div>
                  <div className="flex-1 flex items-center justify-between">
                    <div className={`font-semibold ${homeWon ? 'text-emerald-400' : 'text-white/70'}`}>
                      {game.homeTeam} {game.homePoints}
                    </div>
                    <div className="text-white/40 mx-2">-</div>
                    <div className={`font-semibold ${!homeWon ? 'text-emerald-400' : 'text-white/70'}`}>
                      {game.awayPoints} {game.awayTeam}
                    </div>
                  </div>
                </div>
                
                {/* Weather indicator */}
                {game.weather?.temperature && (
                  <div className="text-xs text-white/50 ml-4">
                    {game.weather.temperature}°F
                  </div>
                )}
                
                {/* Spread indicator */}
                {game.lines?.[0]?.spread && (
                  <div className="text-xs text-blue-400 ml-2">
                    {game.lines[0].spread > 0 ? '+' : ''}{game.lines[0].spread}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Fun Fact Section */}
      <div className="fun-facts glass-card-light p-4 rounded-xl mt-6">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-2xl">💡</span>
          <span className="text-sm font-semibold text-white/70">Rivalry Insights</span>
        </div>
        
        <div className="space-y-2 text-sm text-white/80">
          <div>
            • Home team wins <span className="text-emerald-400 font-semibold">
              {((stats.home_wins / stats.total_games) * 100).toFixed(1)}%
            </span> of the time
          </div>
          <div>
            • Average scoring: <span className="text-blue-400 font-semibold">
              {((stats.team1_points + stats.team2_points) / stats.total_games).toFixed(1)} total points
            </span>
          </div>
          {stats.ranked_matchups > 0 && (
            <div>
              • <span className="text-purple-400 font-semibold">
                {((stats.ranked_matchups / stats.total_games) * 100).toFixed(0)}%
              </span> of games featured ranked teams
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RivalryHistoryCard;
