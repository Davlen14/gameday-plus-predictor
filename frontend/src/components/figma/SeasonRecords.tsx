import { GlassCard } from './GlassCard';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Calendar } from 'lucide-react';

interface SeasonRecordsProps {
  predictionData?: any;
}

interface GameResult {
  week: string;
  opponent: string;
  result: 'W' | 'L';
  score: string;
  isAway: boolean;
  opponentLogo: string;
}

interface TeamRecord {
  team: string;
  record: string;
  games: GameResult[];
  logo: string;
  primaryColor: string;
}

export function SeasonRecords({ predictionData }: SeasonRecordsProps) {
  console.log('SeasonRecords - predictionData:', predictionData);
  console.log('SeasonRecords - season_records:', predictionData?.season_records);
  
  if (!predictionData?.season_records) {
    console.log('SeasonRecords - No season_records data found, returning null');
    return null;
  }

  const { away, home } = predictionData.season_records;
  console.log('SeasonRecords - away:', away);
  console.log('SeasonRecords - home:', home);

  if (!away && !home) {
    console.log('SeasonRecords - No away or home data, returning null');
    return null;
  }
  
  console.log('SeasonRecords - Rendering component!');

  // Get team colors for glowColor
  const team1Color = away?.primaryColor || '#6366f1';
  const team2Color = home?.primaryColor || '#8b5cf6';

  return (
    <GlassCard glowColor={`from-[${team1Color}]/20 to-[${team2Color}]/20`} className="p-4 sm:p-6 border-gray-500/40">
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="p-1.5 sm:p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
            <Calendar className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400" />
          </div>
          <h3 className="text-white font-semibold text-sm sm:text-base">2025 Season Records</h3>
        </div>
        
        {/* Team Legend */}
        <div className="flex items-center gap-4">
          {away && (
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={away.logo}
                alt={away.team}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team1Color }}>{away.team}</span>
            </div>
          )}
          {home && (
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={home.logo}
                alt={home.team}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team2Color }}>{home.team}</span>
            </div>
          )}
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Away Team */}
        {away && (
          <div>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={away.logo} alt={away.team} className="w-12 h-12 object-contain" />
              <div>
                <h4 className="text-lg font-semibold text-white">
                  {away.team}
                </h4>
                <p className="text-sm text-gray-400">{away.record}</p>
              </div>
            </div>
            <div className="space-y-2">
              {away.games.map((game: any, idx: number) => (
                <GameResult
                  key={idx}
                  week={game.week}
                  result={game.result}
                  opponent={game.opponent}
                  score={game.score}
                  away={game.isAway}
                  opponentLogo={game.opponentLogo}
                />
              ))}
            </div>
          </div>
        )}
        
        {/* Home Team */}
        {home && (
          <div>
            <div className="flex items-center gap-3 mb-4">
              <ImageWithFallback src={home.logo} alt={home.team} className="w-12 h-12 object-contain" />
              <div>
                <h4 className="text-lg font-semibold text-white">
                  {home.team}
                </h4>
                <p className="text-sm text-gray-400">{home.record}</p>
              </div>
            </div>
            <div className="space-y-2">
              {home.games.map((game: any, idx: number) => (
                <GameResult
                  key={idx}
                  week={game.week}
                  result={game.result}
                  opponent={game.opponent}
                  score={game.score}
                  away={game.isAway}
                  opponentLogo={game.opponentLogo}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </GlassCard>
  );
}

function GameResult({ week, result, opponent, score, away, opponentLogo }: { week: number; result: 'W' | 'L'; opponent: string; score: string; away?: boolean; opponentLogo: string }) {
  const bgColor = result === 'W' 
    ? 'bg-gradient-to-br from-emerald-500/15 to-emerald-500/5 border-emerald-400/40' 
    : 'bg-gradient-to-br from-red-500/15 to-red-500/5 border-red-400/40';
  const textColor = result === 'W' ? 'text-emerald-400' : 'text-red-500';
  
  return (
    <div className={`flex justify-between items-center rounded-lg p-3 backdrop-blur-sm border ${bgColor}`}>
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-400 font-semibold min-w-[45px]">Week {week}</span>
        <span className="text-sm text-gray-300">{away ? '@' : 'vs'}</span>
        <ImageWithFallback src={opponentLogo} alt={opponent} className="w-6 h-6 object-contain" />
        <span className="text-sm text-gray-200 font-medium">{opponent}</span>
      </div>
      <span className={`text-sm font-bold font-mono ${textColor}`}>{result} {score}</span>
    </div>
  );
}
