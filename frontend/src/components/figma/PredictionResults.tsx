import { GlassCard } from './GlassCard';
import { CheckCircle2, XCircle, TrendingUp, TrendingDown, BarChart3, Target } from 'lucide-react';

interface PredictionResultsProps {
  predictionData?: {
    final_prediction?: {
      predicted_score?: {
        home_score?: number;
        away_score?: number;
        total?: number;
      };
    };
    ui_components?: {
      prediction_cards?: {
        predicted_spread?: {
          model_spread?: number;
          market_spread?: number;
          edge?: number;
        };
        predicted_total?: {
          model_total?: number;
          market_total?: number;
          edge?: number;
        };
      };
      detailed_analysis?: {
        betting_analysis?: {
          market_spread?: number;
          market_total?: number;
          spread_edge?: number;
          total_edge?: number;
          sportsbooks?: {
            individual_books?: Array<{
              provider?: string;
              name?: string;
              spread?: number;
              overUnder?: number;
              total?: number;
            }>;
          };
        };
      };
      season_records?: {
        home?: {
          games?: Array<{
            week: string;
            opponent: string;
            result: string;
            score: string;
          }>;
        };
        away?: {
          games?: Array<{
            week: string;
            opponent: string;
            result: string;
            score: string;
          }>;
        };
      };
    };
    team_selector?: {
      home_team?: {
        name: string;
        logo: string;
      };
      away_team?: {
        name: string;
        logo: string;
      };
    };
  };
  actualScore?: {
    homeScore: number;
    awayScore: number;
  };
  gameCompleted?: boolean;
}

export function PredictionResults({ predictionData, actualScore: providedActualScore, gameCompleted: providedGameCompleted = false }: PredictionResultsProps) {
  const homeTeam = predictionData?.team_selector?.home_team?.name || 'Home';
  const awayTeam = predictionData?.team_selector?.away_team?.name || 'Away';
  const homeLogo = predictionData?.team_selector?.home_team?.logo || '';
  const awayLogo = predictionData?.team_selector?.away_team?.logo || '';
  
  // Get team colors from season_records
  const homeColor = (predictionData as any)?.season_records?.home?.primary_color || '#60a5fa';
  const awayColor = (predictionData as any)?.season_records?.away?.primary_color || '#60a5fa';

  // Auto-detect if game is completed by checking season records
  const seasonRecords = (predictionData as any)?.season_records || (predictionData as any)?.ui_components?.season_records;
  const homeRecords = seasonRecords?.home?.games || [];
  const awayRecords = seasonRecords?.away?.games || [];
  
  console.log('PredictionResults Debug:', {
    homeTeam,
    awayTeam,
    homeRecordsCount: homeRecords.length,
    awayRecordsCount: awayRecords.length,
    homeRecordsSample: homeRecords[0],
    awayRecordsSample: awayRecords[0]
  });
  
  // Determine if game is completed and extract actual scores
  let gameCompleted = providedGameCompleted;
  let actualScore = providedActualScore;
  
  // Only try to auto-detect if not already provided
  if (!gameCompleted && homeRecords && awayRecords) {
    try {
      // Normalize team names for better matching
      const normalizeTeamName = (name: string) => {
        return name.toLowerCase()
          .replace(/\s+(university|college|the)\s*/gi, '')
          .replace(/[^a-z0-9]/g, '')
          .trim();
      };
      
      const normalizedHomeTeam = normalizeTeamName(homeTeam);
      const normalizedAwayTeam = normalizeTeamName(awayTeam);
      
      console.log('Searching for matchup:', {
        homeTeam: homeTeam,
        awayTeam: awayTeam,
        normalizedHome: normalizedHomeTeam,
        normalizedAway: normalizedAwayTeam
      });
      
      // Find the matchup in season records (look for both teams playing each other)
      const homeMatchup = homeRecords.find((game: any) => {
        const normalizedOpponent = normalizeTeamName(game?.opponent || '');
        const matches = normalizedOpponent === normalizedAwayTeam || 
                       normalizedAwayTeam === normalizedOpponent;
        console.log('Checking home game:', game?.opponent, '→', normalizedOpponent, 'vs', normalizedAwayTeam, '=', matches);
        return game?.opponent && matches && game?.score && game.score.trim() !== '';
      });
      
      const awayMatchup = awayRecords.find((game: any) => {
        const normalizedOpponent = normalizeTeamName(game?.opponent || '');
        const matches = normalizedOpponent === normalizedHomeTeam || 
                       normalizedHomeTeam === normalizedOpponent;
        console.log('Checking away game:', game?.opponent, '→', normalizedOpponent, 'vs', normalizedHomeTeam, '=', matches);
        return game?.opponent && matches && game?.score && game.score.trim() !== '';
      });
      
      if (homeMatchup || awayMatchup) {
        const matchup = homeMatchup || awayMatchup;
        console.log('Found matchup:', matchup);
        
        if (matchup && matchup.score) {
          // Parse score format like "20-17" or "17-20"
          const scoreMatch = matchup.score.match(/(\d+)-(\d+)/);
          if (scoreMatch) {
            const [, score1, score2] = scoreMatch;
            const teamScore = parseInt(score1);
            const oppScore = parseInt(score2);
            
            // If this is home team's record
            if (homeMatchup) {
              actualScore = {
                homeScore: teamScore,
                awayScore: oppScore
              };
            } else {
              // If this is away team's record
              actualScore = {
                homeScore: oppScore,
                awayScore: teamScore
              };
            }
            gameCompleted = true;
            console.log('Game completed! Scores:', actualScore);
          }
        }
      } else {
        console.log('No matchup found between', homeTeam, 'and', awayTeam);
      }
    } catch (error) {
      console.error('Error parsing season records:', error);
    }
  }
  
  // Don't render if game is not completed
  if (!gameCompleted || !actualScore) {
    console.log('❌ Not showing PredictionResults - game not completed:', { gameCompleted, actualScore, homeTeam, awayTeam });
    return null;
  }
  
  console.log('✅ Showing PredictionResults!', { gameCompleted, actualScore });

  const predictedHomeScore = predictionData?.final_prediction?.predicted_score?.home_score || 0;
  const predictedAwayScore = predictionData?.final_prediction?.predicted_score?.away_score || 0;
  
  // Use same data paths as MarketComparison component
  const uiComponents = (predictionData as any)?.ui_components || predictionData;
  const bettingAnalysis = uiComponents?.detailed_analysis?.betting_analysis;
  const predictionCards = uiComponents?.prediction_cards;
  
  const predictedSpread = predictionCards?.predicted_spread?.model_spread || 0;
  const predictedTotal = predictionCards?.predicted_total?.model_total || 0;
  
  // Market data - same as MarketComparison
  const marketSpread = bettingAnalysis?.market_spread || predictionCards?.predicted_spread?.market_spread || 0;
  const marketTotal = bettingAnalysis?.market_total || predictionCards?.predicted_total?.market_total || 0;
  const spreadEdge = Math.abs(bettingAnalysis?.spread_edge || predictionCards?.predicted_spread?.edge || 0);
  const totalEdge = Math.abs(bettingAnalysis?.total_edge || predictionCards?.predicted_total?.edge || 0);
  
  // Sportsbooks data - map provider to name
  const sportsbooksRaw = bettingAnalysis?.sportsbooks?.individual_books || [];
  const sportsbooks = sportsbooksRaw.map((book: any) => ({
    name: book.provider || book.name || 'Unknown',
    spread: book.spread,
    total: book.overUnder || book.total
  }));
  
  // Sportsbook logo mapping
  const sportsbookLogos: Record<string, string> = {
    'DraftKings': '/Draftking.svg',
    'Bovada': '/Bovada-Casino-Logo.svg',
    'ESPN Bet': '/espnbet.svg'
  };

  const actualHomeScore = actualScore.homeScore;
  const actualAwayScore = actualScore.awayScore;
  const actualSpread = actualHomeScore - actualAwayScore;
  const actualTotal = actualHomeScore + actualAwayScore;

  // Calculate accuracy
  const scoreAccuracy = {
    home: Math.abs(predictedHomeScore - actualHomeScore),
    away: Math.abs(predictedAwayScore - actualAwayScore),
  };
  
  const spreadAccuracy = Math.abs(predictedSpread - actualSpread);
  const totalAccuracy = Math.abs(predictedTotal - actualTotal);
  
  const spreadCorrect = Math.sign(predictedSpread) === Math.sign(actualSpread);
  const totalCorrect = Math.abs(totalAccuracy) <= 3; // Within 3 points is good
  
  const overallAccuracy = 100 - Math.min(
    ((scoreAccuracy.home + scoreAccuracy.away + spreadAccuracy + totalAccuracy) / 4) * 2,
    100
  );

  return (
    <GlassCard className="p-6 border-purple-500/40 mt-6">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-white font-bold text-xl flex items-center gap-2">
              <BarChart3 className="w-6 h-6 text-purple-400" />
              Prediction Results
              <span className={`text-sm px-3 py-1 rounded-full ${
                overallAccuracy >= 90 ? 'bg-green-500/20 text-green-400' :
                overallAccuracy >= 75 ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                {overallAccuracy.toFixed(0)}% Accurate
              </span>
            </h3>
            <p className="text-gray-400 text-sm">Model vs Actual Results</p>
          </div>
        </div>

        {/* Score Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Away Team */}
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              {awayLogo && (
                <img src={awayLogo} alt={awayTeam} className="w-12 h-12 object-contain" />
              )}
              <div className="flex-1">
                <p className="text-white font-semibold">{awayTeam}</p>
                <p className="text-gray-400 text-sm">Away Team</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="backdrop-blur-sm rounded-lg p-3 border border-gray-700/50">
                <p className="text-gray-400 text-xs mb-1">Predicted</p>
                <div className="flex items-center gap-2">
                  {awayLogo && <img src={awayLogo} alt={awayTeam} className="w-6 h-6 object-contain" />}
                  <p className="text-2xl font-mono font-bold" style={{ color: awayColor }}>{predictedAwayScore}</p>
                </div>
              </div>
              <div className="backdrop-blur-sm rounded-lg p-3 border border-green-500/30">
                <p className="text-gray-400 text-xs mb-1">Actual</p>
                <div className="flex items-center gap-2">
                  {awayLogo && <img src={awayLogo} alt={awayTeam} className="w-6 h-6 object-contain" />}
                  <p className="text-2xl font-mono text-green-400">{actualAwayScore}</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm">
              {scoreAccuracy.away <= 3 ? (
                <CheckCircle2 className="w-4 h-4 text-green-400" />
              ) : (
                <XCircle className="w-4 h-4 text-red-400" />
              )}
              <span className={scoreAccuracy.away <= 3 ? 'text-green-400' : 'text-red-400'}>
                {scoreAccuracy.away === 0 ? 'Perfect!' : `Off by ${scoreAccuracy.away} pts`}
              </span>
            </div>
          </div>

          {/* Home Team */}
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              {homeLogo && (
                <img src={homeLogo} alt={homeTeam} className="w-12 h-12 object-contain" />
              )}
              <div className="flex-1">
                <p className="text-white font-semibold">{homeTeam}</p>
                <p className="text-gray-400 text-sm">Home Team</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="backdrop-blur-sm rounded-lg p-3 border border-gray-700/50">
                <p className="text-gray-400 text-xs mb-1">Predicted</p>
                <div className="flex items-center gap-2">
                  {homeLogo && <img src={homeLogo} alt={homeTeam} className="w-6 h-6 object-contain" />}
                  <p className="text-2xl font-mono font-bold" style={{ color: homeColor }}>{predictedHomeScore}</p>
                </div>
              </div>
              <div className="backdrop-blur-sm rounded-lg p-3 border border-green-500/30">
                <p className="text-gray-400 text-xs mb-1">Actual</p>
                <div className="flex items-center gap-2">
                  {homeLogo && <img src={homeLogo} alt={homeTeam} className="w-6 h-6 object-contain" />}
                  <p className="text-2xl font-mono text-green-400">{actualHomeScore}</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm">
              {scoreAccuracy.home <= 3 ? (
                <CheckCircle2 className="w-4 h-4 text-green-400" />
              ) : (
                <XCircle className="w-4 h-4 text-red-400" />
              )}
              <span className={scoreAccuracy.home <= 3 ? 'text-green-400' : 'text-red-400'}>
                {scoreAccuracy.home === 0 ? 'Perfect!' : `Off by ${scoreAccuracy.home} pts`}
              </span>
            </div>
          </div>
        </div>

        {/* Model vs Market Comparison */}
        <div className="bg-gradient-to-br from-purple-500/10 to-blue-500/10 rounded-lg p-5 border border-purple-500/30">
          <h4 className="text-purple-400 font-semibold mb-4 flex items-center gap-2">
            <Target className="w-5 h-5" />
            Model vs Market Lines
          </h4>
          
          {/* Sportsbooks Reference */}
          {sportsbooks && sportsbooks.length > 0 && (
            <div className="mb-4 pb-3 border-b border-purple-500/20">
              <p className="text-gray-400 text-xs mb-2">Market consensus from:</p>
              <div className="flex flex-wrap gap-2">
                {sportsbooks.map((book: any, idx: number) => {
                  const bookName = book?.name || 'Unknown';
                  const logoPath = sportsbookLogos[bookName];
                  return (
                    <div key={idx} className="flex items-center gap-2 backdrop-blur-sm rounded px-2 py-1 border border-gray-700/50">
                      {logoPath ? (
                        <img 
                          src={logoPath} 
                          alt={bookName} 
                          className="w-4 h-4 object-contain"
                          onError={(e) => {
                            // Fallback to initials if image fails to load
                            e.currentTarget.style.display = 'none';
                            const parent = e.currentTarget.parentElement;
                            if (parent) {
                              const fallback = document.createElement('div');
                              fallback.className = 'w-4 h-4 bg-gradient-to-br from-blue-500 to-purple-500 rounded flex items-center justify-center text-white text-[8px] font-bold';
                              fallback.textContent = bookName.substring(0, 2).toUpperCase();
                              parent.insertBefore(fallback, e.currentTarget);
                            }
                          }}
                        />
                      ) : (
                        <div className="w-4 h-4 bg-gradient-to-br from-blue-500 to-purple-500 rounded flex items-center justify-center text-white text-[8px] font-bold">
                          {bookName.substring(0, 2).toUpperCase()}
                        </div>
                      )}
                      <span className="text-gray-300 text-xs font-medium">{bookName}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Spread Comparison */}
            <div className="space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-purple-500/20">
                <span className="text-gray-400 text-sm font-medium">Spread</span>
                <span className={`text-xs px-2 py-1 rounded ${
                  Math.abs(spreadEdge) > 3 ? 'bg-green-500/20 text-green-400' : 
                  Math.abs(spreadEdge) > 1 ? 'bg-yellow-500/20 text-yellow-400' : 
                  'bg-gray-500/20 text-gray-400'
                }`}>
                  {Math.abs(spreadEdge).toFixed(1)}pt edge
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Our Model:</span>
                  <span className="text-blue-400 font-mono font-semibold">
                    {predictedSpread > 0 ? '+' : ''}{predictedSpread.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Market:</span>
                  <span className="text-amber-400 font-mono font-semibold">
                    {marketSpread > 0 ? '+' : ''}{marketSpread.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center pt-2 border-t border-purple-500/10">
                  <span className="text-gray-400 text-sm">Actual Result:</span>
                  <span className="text-green-400 font-mono font-semibold">
                    {actualSpread > 0 ? '+' : ''}{actualSpread.toFixed(1)}
                  </span>
                </div>
                <div className="mt-2 text-xs">
                  {Math.abs(predictedSpread - actualSpread) < Math.abs(marketSpread - actualSpread) ? (
                    <div className="flex items-center gap-1 text-green-400">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Model closer to actual ({Math.abs(predictedSpread - actualSpread).toFixed(1)} vs {Math.abs(marketSpread - actualSpread).toFixed(1)} pts off)</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-red-400">
                      <XCircle className="w-3 h-3" />
                      <span>Market closer to actual ({Math.abs(marketSpread - actualSpread).toFixed(1)} vs {Math.abs(predictedSpread - actualSpread).toFixed(1)} pts off)</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Total Comparison */}
            <div className="space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-purple-500/20">
                <span className="text-gray-400 text-sm font-medium">Total</span>
                <span className={`text-xs px-2 py-1 rounded ${
                  Math.abs(totalEdge) > 5 ? 'bg-green-500/20 text-green-400' : 
                  Math.abs(totalEdge) > 2 ? 'bg-yellow-500/20 text-yellow-400' : 
                  'bg-gray-500/20 text-gray-400'
                }`}>
                  {Math.abs(totalEdge).toFixed(1)}pt edge
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Our Model:</span>
                  <span className="text-blue-400 font-mono font-semibold">
                    {predictedTotal.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">Market:</span>
                  <span className="text-amber-400 font-mono font-semibold">
                    {marketTotal.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center pt-2 border-t border-purple-500/10">
                  <span className="text-gray-400 text-sm">Actual Result:</span>
                  <span className="text-green-400 font-mono font-semibold">
                    {actualTotal.toFixed(1)}
                  </span>
                </div>
                <div className="mt-2 text-xs">
                  {Math.abs(predictedTotal - actualTotal) < Math.abs(marketTotal - actualTotal) ? (
                    <div className="flex items-center gap-1 text-green-400">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Model closer to actual ({Math.abs(predictedTotal - actualTotal).toFixed(1)} vs {Math.abs(marketTotal - actualTotal).toFixed(1)} pts off)</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-red-400">
                      <XCircle className="w-3 h-3" />
                      <span>Market closer to actual ({Math.abs(marketTotal - actualTotal).toFixed(1)} vs {Math.abs(predictedTotal - actualTotal).toFixed(1)} pts off)</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Spread & Total Accuracy */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-700/50">
          {/* Spread */}
          <div className="bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-lg p-4 border border-amber-500/30">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-amber-400 font-semibold flex items-center gap-2">
                {spreadCorrect ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                Spread Prediction
              </h4>
              {spreadCorrect ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : (
                <XCircle className="w-5 h-5 text-red-400" />
              )}
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Predicted:</span>
                <span className="text-white font-mono">{predictedSpread > 0 ? '+' : ''}{predictedSpread.toFixed(1)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Actual:</span>
                <span className="text-green-400 font-mono">{actualSpread > 0 ? '+' : ''}{actualSpread.toFixed(1)}</span>
              </div>
              <div className="flex justify-between pt-2 border-t border-amber-500/20">
                <span className="text-gray-400">Difference:</span>
                <span className={spreadAccuracy <= 3 ? 'text-green-400' : 'text-red-400'}>
                  {spreadAccuracy.toFixed(1)} pts
                </span>
              </div>
            </div>
          </div>

          {/* Total */}
          <div className="bg-gradient-to-br from-emerald-500/10 to-green-500/10 rounded-lg p-4 border border-emerald-500/30">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-emerald-400 font-semibold flex items-center gap-2">
                {totalCorrect ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                Total Prediction
              </h4>
              {totalCorrect ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : (
                <XCircle className="w-5 h-5 text-red-400" />
              )}
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Predicted:</span>
                <span className="text-white font-mono">{predictedTotal.toFixed(1)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Actual:</span>
                <span className="text-green-400 font-mono">{actualTotal.toFixed(1)}</span>
              </div>
              <div className="flex justify-between pt-2 border-t border-emerald-500/20">
                <span className="text-gray-400">Difference:</span>
                <span className={totalAccuracy <= 3 ? 'text-green-400' : 'text-red-400'}>
                  {totalAccuracy.toFixed(1)} pts
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Summary */}
        <div className="backdrop-blur-sm rounded-lg p-4 border border-gray-700/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white font-semibold mb-1">Prediction Summary</p>
              <div className="flex items-center gap-2 text-sm">
                {spreadCorrect && totalCorrect ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-green-400" />
                    <span className="text-gray-400">Hit both spread and total!</span>
                  </>
                ) : spreadCorrect ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-green-400" />
                    <span className="text-gray-400">Got the spread right</span>
                  </>
                ) : totalCorrect ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-green-400" />
                    <span className="text-gray-400">Got the total right</span>
                  </>
                ) : (
                  <>
                    <XCircle className="w-4 h-4 text-red-400" />
                    <span className="text-gray-400">Missed spread and total</span>
                  </>
                )}
              </div>
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-purple-400">{overallAccuracy.toFixed(0)}%</p>
              <p className="text-gray-400 text-xs">Overall Accuracy</p>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
