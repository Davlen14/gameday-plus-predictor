import { GlassCard } from './GlassCard';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

// Sportsbook SVGs from public folder
const BovadaLogo = '/Bovada-Casino-Logo.svg';
const ESPNBetLogo = '/espnbet.svg';
const DraftKingsLogo = '/Draftking.svg';

interface LineMovementProps {
  predictionData?: any;
}

export function LineMovement({ predictionData }: LineMovementProps) {
  // Get the individual_books array from the sportsbooks object
  const sportsbooksData = predictionData?.detailed_analysis?.betting_analysis?.sportsbooks;
  const sportsbooks = sportsbooksData?.individual_books || [];

  // Calculate line movement for each book
  const lineMovements = sportsbooks.map((book: any) => {
    const spreadOpen = book.spreadOpen;
    const spreadCurrent = book.spread;
    const movement = spreadOpen && spreadCurrent ? spreadCurrent - spreadOpen : 0;
    
    const totalOpen = book.overUnderOpen;
    const totalCurrent = book.overUnder;
    const totalMovement = totalOpen && totalCurrent ? totalCurrent - totalOpen : 0;

    return {
      provider: book.provider,
      spread: {
        open: spreadOpen,
        current: spreadCurrent,
        movement: movement,
        direction: movement > 0 ? 'up' : movement < 0 ? 'down' : 'none'
      },
      total: {
        open: totalOpen,
        current: totalCurrent,
        movement: totalMovement,
        direction: totalMovement > 0 ? 'up' : totalMovement < 0 ? 'down' : 'none'
      }
    };
  });

  if (lineMovements.length === 0) {
    return null;
  }

  const getMovementIcon = (direction: string) => {
    switch (direction) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-400" />;
      default:
        return <Minus className="w-4 h-4 text-gray-400" />;
    }
  };

  const getMovementColor = (direction: string) => {
    switch (direction) {
      case 'up':
        return 'text-green-400';
      case 'down':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  return (
    <GlassCard glowColor="from-amber-500/10 to-orange-500/10" className="p-6 border-orange-500/20">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-amber-500/20 border border-orange-500/30">
          <TrendingUp className="w-5 h-5 text-amber-400" />
        </div>
        <h2 className="text-xl font-bold text-white">Line Movement Analysis</h2>
      </div>

      <div className="space-y-4">
        {/* Spread Movement */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-3">Spread Movement</h3>
          <div className="space-y-2">
            {lineMovements.map((book: any, idx: number) => {
              const logo = book.provider === 'DraftKings' ? DraftKingsLogo :
                          book.provider === 'ESPN Bet' ? ESPNBetLogo :
                          book.provider === 'Bovada' ? BovadaLogo :
                          DraftKingsLogo;
              
              return (
              <div key={idx} className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <img src={logo} alt={book.provider} className="w-8 h-8 object-contain" />
                    <span className="text-sm font-medium text-white">{book.provider}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getMovementIcon(book.spread.direction)}
                    <span className={`text-sm font-bold ${getMovementColor(book.spread.direction)}`}>
                      {book.spread.movement > 0 ? '+' : ''}{book.spread.movement.toFixed(1)}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <div className="text-gray-400">
                    Open: <span className="text-white font-medium">{book.spread.open?.toFixed(1) || 'N/A'}</span>
                  </div>
                  <div className="text-gray-400">
                    Current: <span className="text-amber-400 font-medium">{book.spread.current?.toFixed(1) || 'N/A'}</span>
                  </div>
                </div>
              </div>
              );
            })}
          </div>
        </div>

        {/* Total Movement */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-3">Total (Over/Under) Movement</h3>
          <div className="space-y-2">
            {lineMovements.map((book: any, idx: number) => {
              const logo = book.provider === 'DraftKings' ? DraftKingsLogo :
                          book.provider === 'ESPN Bet' ? ESPNBetLogo :
                          book.provider === 'Bovada' ? BovadaLogo :
                          DraftKingsLogo;
              
              return (
              <div key={idx} className="backdrop-blur-sm border border-gray-600/40 rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <img src={logo} alt={book.provider} className="w-8 h-8 object-contain" />
                    <span className="text-sm font-medium text-white">{book.provider}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getMovementIcon(book.total.direction)}
                    <span className={`text-sm font-bold ${getMovementColor(book.total.direction)}`}>
                      {book.total.movement > 0 ? '+' : ''}{book.total.movement.toFixed(1)}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <div className="text-gray-400">
                    Open: <span className="text-white font-medium">{book.total.open?.toFixed(1) || 'N/A'}</span>
                  </div>
                  <div className="text-gray-400">
                    Current: <span className="text-amber-400 font-medium">{book.total.current?.toFixed(1) || 'N/A'}</span>
                  </div>
                </div>
              </div>
              );
            })}
          </div>
        </div>

        {/* Movement Summary */}
        <div className="mt-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg">
          <div className="text-sm text-amber-200">
            <span className="font-semibold">Sharp Money Analysis:</span> Line movement indicates where professional bettors are placing their money. Significant movement (2+ points) typically signals sharp action.
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
