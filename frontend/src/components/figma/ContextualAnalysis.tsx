import { GlassCard } from './GlassCard';
import { Sun, TrendingUp, Calendar } from 'lucide-react';
import { useAppStore } from '../../store';

interface ContextualAnalysisProps {
  predictionData?: any;
}

export function ContextualAnalysis({ predictionData: propPredictionData }: ContextualAnalysisProps) {
  // GET REAL API DATA
  const { predictionData: storePredictionData } = useAppStore();
  const predictionData = propPredictionData || storePredictionData;
  
  // EXTRACT WEATHER DATA (from contextual_analysis section)
  const weather = predictionData?.contextual_analysis?.weather || {};
  const temperature = weather.temperature || 72.0;
  const windSpeed = weather.wind_speed || 7.0;
  const precipitation = weather.precipitation || 0.0;
  const weatherFactor = weather.weather_factor || 0.0;
  
  // EXTRACT TEAM INFO (dynamic based on actual prediction)
  const homeTeam = predictionData?.team_selector?.home_team?.name || 'Home Team';
  const awayTeam = predictionData?.team_selector?.away_team?.name || 'Away Team';
  
  // EXTRACT POLL DATA (from contextual_analysis section)
  const rankings = predictionData?.contextual_analysis?.rankings || {};
  const homeRank = rankings.home_rank ? `#${rankings.home_rank}` : 'NR';
  const awayRank = rankings.away_rank ? `#${rankings.away_rank}` : 'NR';
  
  // Calculate poll points from rankings (estimated)
  const getRankingPoints = (rank: string | number | null): number => {
    if (!rank || rank === 'Unranked' || rank === null) return 0;
    const rankNum = typeof rank === 'string' ? parseInt(rank.replace('#', '')) : rank;
    if (rankNum <= 5) return 1500 - (rankNum * 200);
    if (rankNum <= 10) return 1000 - ((rankNum - 5) * 100);
    if (rankNum <= 15) return 500 - ((rankNum - 10) * 50);
    if (rankNum <= 25) return 250 - ((rankNum - 15) * 10);
    return 0;
  };
  
  const homePollPoints = getRankingPoints(homeRank);
  const awayPollPoints = getRankingPoints(awayRank);
  const pollAdvantage = homePollPoints - awayPollPoints;
  
  // EXTRACT BYE WEEK DATA (from contextual_analysis section)
  const byeAnalysis = predictionData?.contextual_analysis?.bye_week_analysis || {};
  const homeByeWeeks = byeAnalysis.home_bye_weeks || [];
  const awayByeWeeks = byeAnalysis.away_bye_weeks || [];
  const byeAdvantage = parseFloat(byeAnalysis.bye_advantage?.replace(' points', '')) || 0.0;
  
  const homeByeStatus = homeByeWeeks.length > 0 ? `Bye: Week ${homeByeWeeks.join(', ')}` : 'No bye weeks yet';
  const awayByeStatus = awayByeWeeks.length > 0 ? `Bye: Week ${awayByeWeeks.join(', ')}` : 'No bye weeks yet';
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Weather Conditions */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sun className="w-5 h-5 text-orange-400" />
          <h3 className="text-white font-semibold">Weather Conditions</h3>
        </div>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-300 text-sm">Temperature</span>
            <span className="text-lg font-bold text-orange-400">{temperature.toFixed(1)}°F</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-300 text-sm">Wind Speed</span>
            <span className="text-lg font-bold text-blue-400">{windSpeed.toFixed(1)} mph</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-300 text-sm">Precipitation</span>
            <span className="text-lg font-bold text-gray-400 font-mono">{precipitation.toFixed(1)} in</span>
          </div>
          <div className="mt-4 p-3 bg-emerald-500/20 border border-emerald-400/40 rounded-lg backdrop-blur-sm">
            <p className="text-emerald-400 font-semibold font-mono drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">Weather Factor: {weatherFactor.toFixed(1)}</p>
            <p className="text-gray-300 text-xs mt-1">
              {Math.abs(weatherFactor) < 0.1 ? 'Ideal playing conditions' : 
               weatherFactor > 0 ? 'Favorable weather' : 'Challenging conditions'}
            </p>
          </div>
        </div>
      </GlassCard>

      {/* Poll Rankings */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-amber-400" />
          <h3 className="text-white font-semibold">Poll Rankings</h3>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">{awayTeam}</p>
            <p className="text-blue-400 text-3xl font-mono drop-shadow-[0_0_10px_rgba(59,130,246,0.3)]">{awayRank}</p>
            <p className="text-gray-400 text-xs mt-1 font-mono">{awayPollPoints} poll points</p>
          </div>
          <div className="bg-amber-500/20 rounded-lg p-4 border border-amber-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">{homeTeam}</p>
            <p className="text-amber-400 text-3xl font-mono drop-shadow-[0_0_10px_rgba(245,158,11,0.3)]">{homeRank}</p>
            <p className="text-gray-400 text-xs mt-1 font-mono">{homePollPoints} poll points</p>
          </div>
        </div>
        <div className="mt-4 p-3 bg-red-500/20 border border-red-500/40 rounded-lg backdrop-blur-sm">
          <p className="text-red-400 font-semibold font-mono drop-shadow-[0_0_10px_rgba(239,68,68,0.3)]">Poll Advantage: {pollAdvantage.toFixed(0)} pts</p>
          <p className="text-gray-300 text-sm mt-1">
            {Math.abs(pollAdvantage) < 50 ? 'Close poll standing' :
             pollAdvantage > 0 ? `Favors ${homeTeam}` : `Favors ${awayTeam}`}
          </p>
        </div>
      </GlassCard>

      {/* Bye Week Analysis */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-5 h-5 text-cyan-400" />
          <h3 className="text-white font-semibold">Bye Week Analysis</h3>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-slate-500/20 rounded-lg p-4 border border-gray-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">{awayTeam}</p>
            <p className="text-gray-400 text-lg font-mono">{awayByeStatus}</p>
          </div>
          <div className="bg-emerald-500/20 rounded-lg p-4 border border-emerald-400/40 backdrop-blur-sm">
            <p className="text-gray-300 text-sm mb-2">{homeTeam}</p>
            <p className="text-emerald-400 text-lg font-mono drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">{homeByeStatus}</p>
            <p className="text-gray-400 text-xs mt-1">
              {homeByeStatus.includes('Bye') ? 'Rest advantage' : 'No rest advantage'}
            </p>
          </div>
        </div>
        <div className="mt-4 p-3 bg-red-500/20 border border-red-500/40 rounded-lg backdrop-blur-sm">
          <p className="text-red-400 font-semibold font-mono drop-shadow-[0_0_10px_rgba(239,68,68,0.3)]">Bye Advantage: {byeAdvantage.toFixed(1)} pts</p>
          <p className="text-gray-300 text-sm mt-1">
            {Math.abs(byeAdvantage) < 0.1 ? 'No bye advantage' :
             byeAdvantage > 0 ? `Favors ${homeTeam}` : `Favors ${awayTeam}`}
          </p>
        </div>
      </GlassCard>
    </div>
  );
}
