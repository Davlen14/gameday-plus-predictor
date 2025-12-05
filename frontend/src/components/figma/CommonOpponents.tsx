import { GlassCard } from './GlassCard';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Users, TrendingUp, TrendingDown, Minus, Check, X } from 'lucide-react';

interface CommonOpponentsProps {
  predictionData?: any;
}

interface CommonOpponentGame {
  opponent: string;
  opponentLogo: string;
  awayTeamResult: 'W' | 'L';
  awayTeamScore: string;
  homeTeamResult: 'W' | 'L';
  homeTeamScore: string;
  awayTeamWeek: number;
  homeTeamWeek: number;
  awayPoints: number;
  awayPointsAllowed: number;
  homePoints: number;
  homePointsAllowed: number;
  marginDiff: number;
}

export function CommonOpponents({ predictionData }: CommonOpponentsProps) {
  if (!predictionData?.season_records?.away?.games || !predictionData?.season_records?.home?.games) {
    return null;
  }

  const awayTeam = predictionData.team_selector?.away_team;
  const homeTeam = predictionData.team_selector?.home_team;
  const awayGames = predictionData.season_records.away.games;
  const homeGames = predictionData.season_records.home.games;

  // Find common opponents
  const commonOpponents: CommonOpponentGame[] = [];
  
  awayGames.forEach((awayGame: any) => {
    const homeGame = homeGames.find((hg: any) => 
      hg.opponent.toLowerCase() === awayGame.opponent.toLowerCase()
    );
    
    if (homeGame) {
      // Parse scores to get points and points allowed
      const awayScoreParts = awayGame.score.split('-').map((s: string) => parseInt(s.trim()));
      const homeScoreParts = homeGame.score.split('-').map((s: string) => parseInt(s.trim()));
      
      const awayPoints = awayScoreParts[0] || 0;
      const awayPointsAllowed = awayScoreParts[1] || 0;
      const homePoints = homeScoreParts[0] || 0;
      const homePointsAllowed = homeScoreParts[1] || 0;
      
      // Calculate margin of victory/defeat for each team
      const awayMargin = awayPoints - awayPointsAllowed;
      const homeMargin = homePoints - homePointsAllowed;
      const marginDiff = awayMargin - homeMargin;
      
      commonOpponents.push({
        opponent: awayGame.opponent,
        opponentLogo: awayGame.opponentLogo,
        awayTeamResult: awayGame.result,
        awayTeamScore: awayGame.score,
        homeTeamResult: homeGame.result,
        homeTeamScore: homeGame.score,
        awayTeamWeek: awayGame.week,
        homeTeamWeek: homeGame.week,
        awayPoints,
        awayPointsAllowed,
        homePoints,
        homePointsAllowed,
        marginDiff
      });
    }
  });

  if (commonOpponents.length === 0) {
    return null;
  }

  // Calculate records against common opponents
  const awayWins = commonOpponents.filter(co => co.awayTeamResult === 'W').length;
  const homeWins = commonOpponents.filter(co => co.homeTeamResult === 'W').length;
  
  // Calculate total points scored and allowed vs common opponents
  const awayTotalPoints = commonOpponents.reduce((sum, co) => sum + co.awayPoints, 0);
  const awayTotalAllowed = commonOpponents.reduce((sum, co) => sum + co.awayPointsAllowed, 0);
  const homeTotalPoints = commonOpponents.reduce((sum, co) => sum + co.homePoints, 0);
  const homeTotalAllowed = commonOpponents.reduce((sum, co) => sum + co.homePointsAllowed, 0);
  
  // Calculate average margin of victory
  const awayAvgMargin = commonOpponents.reduce((sum, co) => sum + (co.awayPoints - co.awayPointsAllowed), 0) / commonOpponents.length;
  const homeAvgMargin = commonOpponents.reduce((sum, co) => sum + (co.homePoints - co.homePointsAllowed), 0) / commonOpponents.length;
  
  // Calculate average points per game
  const awayAvgPoints = awayTotalPoints / commonOpponents.length;
  const awayAvgAllowed = awayTotalAllowed / commonOpponents.length;
  const homeAvgPoints = homeTotalPoints / commonOpponents.length;
  const homeAvgAllowed = homeTotalAllowed / commonOpponents.length;

  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color?.toLowerCase() || '';
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get display colors
  const awayTeamColor = (awayTeam?.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#f97316') 
    : (awayTeam?.primary_color || '#3b82f6');
    
  const homeTeamColor = (homeTeam?.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#10b981') 
    : (homeTeam?.primary_color || '#f97316');

  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg border border-cyan-400/30">
            <Users className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-white font-semibold text-xl">Common Opponents</h3>
            <p className="text-sm text-gray-400">2025 Season Head-to-Head Comparison</p>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 rounded-lg border border-white/10">
            <div className="flex items-center justify-center gap-2 mb-1">
              <ImageWithFallback 
                src={awayTeam?.logo} 
                alt={awayTeam?.name} 
                className="w-6 h-6 object-contain"
              />
              <span className="text-xl font-bold" style={{ color: awayTeamColor }}>
                {awayWins}-{commonOpponents.length - awayWins}
              </span>
            </div>
            <span className="text-xs text-gray-400">Record</span>
          </div>
          
          <div className="text-center p-3 rounded-lg border border-white/10">
            <div className="flex items-center justify-center gap-2 mb-1">
              <ImageWithFallback 
                src={awayTeam?.logo} 
                alt={awayTeam?.name} 
                className="w-6 h-6 object-contain"
              />
              <span className="text-xl font-bold text-white">
                {awayAvgMargin >= 0 ? '+' : ''}{awayAvgMargin.toFixed(1)}
              </span>
            </div>
            <span className="text-xs text-gray-400">Avg Margin</span>
          </div>
          
          <div className="text-center p-3 rounded-lg border border-white/10">
            <div className="flex items-center justify-center gap-2 mb-1">
              <ImageWithFallback 
                src={homeTeam?.logo} 
                alt={homeTeam?.name} 
                className="w-6 h-6 object-contain"
              />
              <span className="text-xl font-bold" style={{ color: homeTeamColor }}>
                {homeWins}-{commonOpponents.length - homeWins}
              </span>
            </div>
            <span className="text-xs text-gray-400">Record</span>
          </div>
          
          <div className="text-center p-3 rounded-lg border border-white/10">
            <div className="flex items-center justify-center gap-2 mb-1">
              <ImageWithFallback 
                src={homeTeam?.logo} 
                alt={homeTeam?.name} 
                className="w-6 h-6 object-contain"
              />
              <span className="text-xl font-bold text-white">
                {homeAvgMargin >= 0 ? '+' : ''}{homeAvgMargin.toFixed(1)}
              </span>
            </div>
            <span className="text-xs text-gray-400">Avg Margin</span>
          </div>
        </div>
      </div>

      {/* Performance Comparison Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Away Team Stats */}
        <div className="p-4 rounded-lg border border-white/10">
          <div className="flex items-center gap-2 mb-4">
            <ImageWithFallback 
              src={awayTeam?.logo} 
              alt={awayTeam?.name} 
              className="w-8 h-8 object-contain"
            />
            <h4 className="text-white font-semibold">{awayTeam?.name} vs Common</h4>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Avg Points Scored</span>
              <span className="text-lg font-bold" style={{ color: awayTeamColor }}>{awayAvgPoints.toFixed(1)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Avg Points Allowed</span>
              <span className="text-lg font-bold text-white">{awayAvgAllowed.toFixed(1)}</span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t border-white/10">
              <span className="text-sm text-gray-400">Total Points</span>
              <span className="text-lg font-bold" style={{ color: awayTeamColor }}>{awayTotalPoints}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Total Allowed</span>
              <span className="text-lg font-bold text-white">{awayTotalAllowed}</span>
            </div>
          </div>
        </div>

        {/* Home Team Stats */}
        <div className="p-4 rounded-lg border border-white/10">
          <div className="flex items-center gap-2 mb-4">
            <ImageWithFallback 
              src={homeTeam?.logo} 
              alt={homeTeam?.name} 
              className="w-8 h-8 object-contain"
            />
            <h4 className="text-white font-semibold">{homeTeam?.name} vs Common</h4>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Avg Points Scored</span>
              <span className="text-lg font-bold" style={{ color: homeTeamColor }}>{homeAvgPoints.toFixed(1)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Avg Points Allowed</span>
              <span className="text-lg font-bold text-white">{homeAvgAllowed.toFixed(1)}</span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t border-white/10">
              <span className="text-sm text-gray-400">Total Points</span>
              <span className="text-lg font-bold" style={{ color: homeTeamColor }}>{homeTotalPoints}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Total Allowed</span>
              <span className="text-lg font-bold text-white">{homeTotalAllowed}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Common Opponents List */}
      <div className="space-y-3">
        {commonOpponents.map((co, index) => {
          const awayWon = co.awayTeamResult === 'W';
          const homeWon = co.homeTeamResult === 'W';
          const bothWon = awayWon && homeWon;
          const bothLost = !awayWon && !homeWon;
          const advantage = bothWon ? 'both' : bothLost ? 'none' : awayWon ? 'away' : 'home';

          return (
            <div 
              key={index} 
              className="relative p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              {/* Opponent Header */}
              <div className="flex items-center justify-center gap-3 mb-4 pb-3 border-b border-white/10">
                <ImageWithFallback 
                  src={co.opponentLogo} 
                  alt={co.opponent} 
                  className="w-10 h-10 object-contain"
                />
                <h4 className="text-lg font-bold text-white">{co.opponent}</h4>
              </div>

              {/* Results Grid */}
              <div className="grid grid-cols-2 gap-4">
                {/* Away Team Result */}
                <div 
                  className={`p-3 rounded-lg border transition-all duration-300 ${
                    awayWon 
                      ? 'bg-emerald-500/10 border-emerald-500/40' 
                      : 'bg-red-500/10 border-red-500/40'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <ImageWithFallback 
                      src={awayTeam?.logo} 
                      alt={awayTeam?.name} 
                      className="w-6 h-6 object-contain"
                    />
                    <span className="text-sm font-semibold text-white">
                      {awayTeam?.name}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-400">Week {co.awayTeamWeek}</span>
                    <div className="flex items-center gap-2">
                      {awayWon ? (
                        <Check className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <X className="w-4 h-4 text-red-400" />
                      )}
                      <span 
                        className={`font-mono font-bold ${
                          awayWon ? 'text-emerald-400' : 'text-red-400'
                        }`}
                      >
                        {co.awayTeamResult} {co.awayTeamScore}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Home Team Result */}
                <div 
                  className={`p-3 rounded-lg border transition-all duration-300 ${
                    homeWon 
                      ? 'bg-emerald-500/10 border-emerald-500/40' 
                      : 'bg-red-500/10 border-red-500/40'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <ImageWithFallback 
                      src={homeTeam?.logo} 
                      alt={homeTeam?.name} 
                      className="w-6 h-6 object-contain"
                    />
                    <span className="text-sm font-semibold text-white">
                      {homeTeam?.name}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-400">Week {co.homeTeamWeek}</span>
                    <div className="flex items-center gap-2">
                      {homeWon ? (
                        <Check className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <X className="w-4 h-4 text-red-400" />
                      )}
                      <span 
                        className={`font-mono font-bold ${
                          homeWon ? 'text-emerald-400' : 'text-red-400'
                        }`}
                      >
                        {co.homeTeamResult} {co.homeTeamScore}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Advantage Indicator */}
              <div className="mt-3 pt-3 border-t border-white/10">
                <div className="flex items-center justify-between">
                  {advantage === 'both' ? (
                    <span className="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                      <Minus className="w-3 h-3" />
                      Both teams won
                    </span>
                  ) : advantage === 'none' ? (
                    <span className="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full bg-slate-500/20 text-slate-400 border border-slate-500/30">
                      <Minus className="w-3 h-3" />
                      Both teams lost
                    </span>
                  ) : advantage === 'away' ? (
                    <span 
                      className="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full border"
                      style={{
                        backgroundColor: `${awayTeamColor}20`,
                        color: awayTeamColor,
                        borderColor: `${awayTeamColor}30`
                      }}
                    >
                      <TrendingUp className="w-3 h-3" />
                      {awayTeam?.name} advantage
                    </span>
                  ) : (
                    <span 
                      className="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full border"
                      style={{
                        backgroundColor: `${homeTeamColor}20`,
                        color: homeTeamColor,
                        borderColor: `${homeTeamColor}30`
                      }}
                    >
                      <TrendingUp className="w-3 h-3" />
                      {homeTeam?.name} advantage
                    </span>
                  )}
                  
                  {/* Margin Differential */}
                  <div className="text-right">
                    <div className="text-xs text-gray-400 mb-1">Margin Diff</div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold" style={{ color: awayTeamColor }}>
                        {co.awayPoints - co.awayPointsAllowed >= 0 ? '+' : ''}{co.awayPoints - co.awayPointsAllowed}
                      </span>
                      <span className="text-xs text-gray-500">vs</span>
                      <span className="text-xs font-bold" style={{ color: homeTeamColor }}>
                        {co.homePoints - co.homePointsAllowed >= 0 ? '+' : ''}{co.homePoints - co.homePointsAllowed}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Overall Analysis */}
      <div className="mt-6 p-4 rounded-lg border border-cyan-500/30">
        <div className="flex items-center gap-3 mb-3">
          <TrendingUp className="w-5 h-5 text-cyan-400" />
          <h4 className="text-white font-semibold">Common Opponent Analysis</h4>
        </div>
        
        <div className="space-y-3 text-sm text-gray-300">
          <p>
            {awayWins > homeWins ? (
              <>
                <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam?.name}</span>
                {' '}performed better with a {awayWins}-{commonOpponents.length - awayWins} record 
                compared to <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam?.name}'s</span> {homeWins}-{commonOpponents.length - homeWins} record.
              </>
            ) : homeWins > awayWins ? (
              <>
                <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam?.name}</span>
                {' '}performed better with a {homeWins}-{commonOpponents.length - homeWins} record 
                compared to <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam?.name}'s</span> {awayWins}-{commonOpponents.length - awayWins} record.
              </>
            ) : (
              <>
                Both teams have identical {awayWins}-{commonOpponents.length - awayWins} records against common opponents.
              </>
            )}
          </p>
          
          <p>
            <span style={{ color: awayTeamColor }} className="font-bold">{awayTeam?.name}</span>
            {' '}averaged <span className="font-bold text-white">{awayAvgPoints.toFixed(1)}</span> points 
            while allowing <span className="font-bold text-white">{awayAvgAllowed.toFixed(1)}</span> points 
            (margin: <span className={`font-bold ${awayAvgMargin >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {awayAvgMargin >= 0 ? '+' : ''}{awayAvgMargin.toFixed(1)}
            </span>).
          </p>
          
          <p>
            <span style={{ color: homeTeamColor }} className="font-bold">{homeTeam?.name}</span>
            {' '}averaged <span className="font-bold text-white">{homeAvgPoints.toFixed(1)}</span> points 
            while allowing <span className="font-bold text-white">{homeAvgAllowed.toFixed(1)}</span> points 
            (margin: <span className={`font-bold ${homeAvgMargin >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {homeAvgMargin >= 0 ? '+' : ''}{homeAvgMargin.toFixed(1)}
            </span>).
          </p>
          
          {Math.abs(awayAvgMargin - homeAvgMargin) > 7 && (
            <p className="pt-2 border-t border-cyan-500/30 text-cyan-300 font-semibold">
              {awayAvgMargin > homeAvgMargin ? (
                <>
                  <span style={{ color: awayTeamColor }}>{awayTeam?.name}</span> dominated common opponents 
                  by an average of {(awayAvgMargin - homeAvgMargin).toFixed(1)} more points per game.
                </>
              ) : (
                <>
                  <span style={{ color: homeTeamColor }}>{homeTeam?.name}</span> dominated common opponents 
                  by an average of {(homeAvgMargin - awayAvgMargin).toFixed(1)} more points per game.
                </>
              )}
            </p>
          )}
        </div>
      </div>
    </GlassCard>
  );
}
