import React, { useMemo, useState, useCallback } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Brush, ReferenceDot, ReferenceArea } from 'recharts';
import { format, parseISO, differenceInHours } from 'date-fns';
import { OddsDataPoint } from '../../hooks/useOddsTimeline';
import { RefreshCw, TrendingDown, TrendingUp, Zap, Target, AlertTriangle, Activity, Flame, Sparkles, TrendingUp as TrendingUpIcon, Info, BarChart3, Clock } from 'lucide-react';

// Sportsbook logo imports
import fanduelLogo from '../../assets/FanduelSports.png';
import caesarsLogo from '../../assets/caesars.png';
import draftKingsLogo from '../../assets/Draftking.svg';
import betmgmLogo from '../../assets/MGM.png';
import fanaticsLogo from '../../assets/fanatics.png';
import bovadaLogo from '../../assets/Bovada-Casino-Logo.svg';

interface OddsTimelineChartProps {
  data: OddsDataPoint[];
  lastUpdated: string;
  isLoading: boolean;
  error: string | null;
  onRefresh?: () => void;
  awayTeam?: string;
  homeTeam?: string;
}

/**
 * Sportsbook ID to name mapping
 */
const SPORTSBOOK_NAMES: Record<number, string> = {
  15: 'FanDuel',
  68: 'Caesars',
  69: 'DraftKings',
  71: 'BetMGM',
  75: 'Fanatics',
  79: 'Fanatics',
  30: 'Bovada',
};

/**
 * Sportsbook logos mapping
 */
const SPORTSBOOK_LOGOS: Record<number, string> = {
  15: fanduelLogo,
  68: caesarsLogo,
  69: draftKingsLogo,
  71: betmgmLogo,
  75: fanaticsLogo,
  30: bovadaLogo,
};

/**
 * Chart colors for different sportsbooks
 */
const BOOK_COLORS: Record<number, string> = {
  15: '#2563eb', // FanDuel - Blue
  68: '#7c3aed', // Caesars - Purple
  69: '#dc2626', // DraftKings - Red
  71: '#059669', // BetMGM - Green
  75: '#ea580c', // Fanatics - Orange
  79: '#ea580c', // Fanatics - Orange (alt ID)
  30: '#ca8a04', // Bovada - Yellow
};

/**
 * Custom tooltip for the chart with enhanced interactivity
 */
const CustomTooltip = ({ active, payload, label, visibleBooks }: any) => {
  if (!active || !payload || !payload.length) return null;

  // Filter by visible books
  const visiblePayload = payload.filter((p: any) => visibleBooks[p.name] !== false);

  return (
    <div className="bg-slate-900/95 border border-white/20 rounded-lg p-4 shadow-2xl backdrop-blur-sm min-w-[200px]">
      <p className="text-white text-xs font-bold mb-3 border-b border-white/10 pb-2">
        {format(parseISO(label), 'MMM dd, h:mm a')}
      </p>
      {visiblePayload.map((entry: any, index: number) => (
        <div key={index} className="flex items-center justify-between gap-4 text-xs mb-1.5">
          <div className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full shadow-lg"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-slate-300 font-medium">{entry.name}</span>
          </div>
          <span className="text-white font-bold text-sm">{entry.value > 0 ? '+' : ''}{entry.value}</span>
        </div>
      ))}
    </div>
  );
};

/**
 * Custom Legend with Sportsbook Logos and Toggle Functionality
 */
const CustomLegend = ({ payload, visibleBooks, onToggleBook }: any) => {
  if (!payload || !payload.length) return null;

  // Sportsbook logos mapping
  const bookLogos: {[key: string]: string} = {
    'FanDuel': fanduelLogo,
    'DraftKings': draftKingsLogo,
    'BetMGM': betmgmLogo,
    'Caesars': caesarsLogo,
    'Fanatics': fanaticsLogo,
    'Bovada': bovadaLogo,
  };

  // Deduplicate by bookName
  const uniquePayload = payload.filter((entry: any, index: number, self: any[]) =>
    self.findIndex((e: any) => e.value === entry.value) === index
  );

  return (
    <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
      {uniquePayload.map((entry: any, index: number) => {
        const bookName = entry.value;
        const logo = bookLogos[bookName];
        const isVisible = visibleBooks[bookName] !== false;
        
        return (
          <div 
            key={index} 
            className="flex items-center gap-3 cursor-pointer select-none hover:scale-105 transition-transform"
            onClick={() => onToggleBook(bookName)}
            style={{ opacity: isVisible ? 1 : 0.3 }}
          >
            {logo && (
              <img 
                src={logo} 
                alt={bookName}
                style={{
                  height: '24px',
                  width: 'auto',
                  objectFit: 'contain',
                  filter: isVisible 
                    ? 'drop-shadow(0 2px 4px rgba(0,0,0,0.3)) drop-shadow(0 0 8px rgba(255,255,255,0.1))'
                    : 'grayscale(100%) drop-shadow(0 2px 4px rgba(0,0,0,0.3))',
                  transform: 'translateZ(0)',
                }}
              />
            )}
            <div className="flex items-center gap-1.5">
              <div
                className="w-3 h-0.5"
                style={{ 
                  backgroundColor: isVisible ? entry.color : 'rgba(148, 163, 184, 0.3)',
                  transition: 'background-color 0.2s'
                }}
              />
              <span style={{
                color: isVisible ? 'rgba(148, 163, 184, 0.7)' : 'rgba(148, 163, 184, 0.3)',
                fontSize: '12px',
                fontWeight: '500',
                letterSpacing: '0.01em',
                textDecoration: isVisible ? 'none' : 'line-through'
              }}>
                {bookName}
              </span>
            </div>
          </div>
        );
      })}
      <div className="w-full text-center mt-2">
        <p className="text-xs text-slate-500 italic flex items-center justify-center gap-1.5">
          <Info className="w-3 h-3" />
          Click sportsbooks to toggle visibility
        </p>
      </div>
    </div>
  );
};

/**
 * Modernized Odds Timeline Chart Component
 *
 * Features:
 * - Brush/range selector for zooming
 * - Toggle sportsbooks on/off
 * - Predictive best bet indicator
 * - Line movement velocity color-coding
 * - Smart annotations for significant movements
 * - Divergence alerts
 * - Time-based filtering
 * - Hover crosshair with all values
 * - Value opportunities timeline
 */
export const OddsTimelineChart: React.FC<OddsTimelineChartProps> = ({
  data,
  lastUpdated,
  isLoading,
  error,
  onRefresh,
  awayTeam = 'Away',
  homeTeam = 'Home',
}) => {
  // State for interactive features
  const [visibleBooks, setVisibleBooks] = useState<Record<string, boolean>>({});
  const [timeFilter, setTimeFilter] = useState<'all' | '24h' | '7d' | 'custom'>('all');
  const [hoveredPoint, setHoveredPoint] = useState<any>(null);
  const [showAnnotations, setShowAnnotations] = useState(true);
  const [brushDomain, setBrushDomain] = useState<[number, number] | null>(null);

  /**
   * Toggle sportsbook visibility
   */
  const toggleBook = useCallback((bookName: string) => {
    setVisibleBooks(prev => ({
      ...prev,
      [bookName]: prev[bookName] === false ? true : false
    }));
  }, []);

  /**
   * Transform data for Recharts with time filtering
   */
  const chartData = useMemo(() => {
    const grouped = new Map<string, any>();

    data.forEach(item => {
      const timestamp = item.timestamp;

      if (!grouped.has(timestamp)) {
        grouped.set(timestamp, { timestamp });
      }

      const bookName = SPORTSBOOK_NAMES[item.bookId] || `Book ${item.bookId}`;
      grouped.get(timestamp)![bookName] = item.spread;
    });

    const sorted = Array.from(grouped.values()).sort((a, b) =>
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    // Apply time filter
    if (timeFilter !== 'all' && sorted.length > 0) {
      const now = new Date();
      const cutoff = timeFilter === '24h' 
        ? new Date(now.getTime() - 24 * 60 * 60 * 1000)
        : new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      
      return sorted.filter(d => new Date(d.timestamp) >= cutoff);
    }

    return sorted;
  }, [data, timeFilter]);

  /**
   * Get unique sportsbooks in the data
   */
  const sportsbooks = useMemo(() => {
    const books = new Set<number>();
    data.forEach(item => books.add(item.bookId));
    return Array.from(books).sort((a, b) => a - b);
  }, [data]);

  /**
   * Detect significant line movements (rapid changes)
   */
  const significantMovements = useMemo(() => {
    const movements: Array<{ timestamp: string; spread: number; velocity: number; reason: string }> = [];
    
    if (chartData.length < 2) return movements;

    for (let i = 1; i < chartData.length; i++) {
      const prev = chartData[i - 1];
      const curr = chartData[i];
      const timeDiff = differenceInHours(new Date(curr.timestamp), new Date(prev.timestamp)) || 0.1;
      
      // Check each sportsbook for rapid movement
      sportsbooks.forEach(bookId => {
        const bookName = SPORTSBOOK_NAMES[bookId];
        const prevSpread = prev[bookName];
        const currSpread = curr[bookName];
        
        if (prevSpread !== undefined && currSpread !== undefined) {
          const spreadChange = Math.abs(currSpread - prevSpread);
          const velocity = spreadChange / timeDiff; // Points per hour
          
          // Flag movements > 2 points in < 2 hours (velocity > 1)
          if (spreadChange >= 2 && velocity > 1) {
            movements.push({
              timestamp: curr.timestamp,
              spread: currSpread,
              velocity,
              reason: spreadChange >= 3 
                ? 'Sharp money detected'
                : spreadChange >= 2.5
                ? 'Public betting surge'
                : 'Significant movement'
            });
          }
        }
      });
    }
    
    return movements;
  }, [chartData, sportsbooks]);

  /**
   * Calculate best entry point (best value opportunity)
   */
  const bestEntryPoint = useMemo(() => {
    if (chartData.length === 0) return null;

    let bestPoint = null;
    let maxSpread = -Infinity;

    chartData.forEach(point => {
      sportsbooks.forEach(bookId => {
        const bookName = SPORTSBOOK_NAMES[bookId];
        const spread = point[bookName];
        
        if (spread !== undefined && Math.abs(spread) > Math.abs(maxSpread)) {
          maxSpread = spread;
          bestPoint = {
            timestamp: point.timestamp,
            spread,
            bookName
          };
        }
      });
    });

    return bestPoint;
  }, [chartData, sportsbooks]);

  /**
   * Detect market divergence (when sportsbooks disagree significantly)
   */
  const marketDivergence = useMemo(() => {
    const divergencePoints: Array<{ timestamp: string; range: number; spreads: number[] }> = [];
    
    chartData.forEach(point => {
      const spreads = sportsbooks
        .map(bookId => point[SPORTSBOOK_NAMES[bookId]])
        .filter((s): s is number => s !== undefined);
      
      if (spreads.length >= 2) {
        const min = Math.min(...spreads);
        const max = Math.max(...spreads);
        const range = max - min;
        
        if (range >= 3) {
          divergencePoints.push({
            timestamp: point.timestamp,
            range,
            spreads
          });
        }
      }
    });
    
    return divergencePoints;
  }, [chartData, sportsbooks]);

  /**
   * Calculate line movement velocity for color coding
   */
  const lineVelocities = useMemo(() => {
    const velocities: Record<string, number[]> = {};
    
    sportsbooks.forEach(bookId => {
      const bookName = SPORTSBOOK_NAMES[bookId];
      velocities[bookName] = [];
      
      for (let i = 1; i < chartData.length; i++) {
        const prev = chartData[i - 1];
        const curr = chartData[i];
        const timeDiff = differenceInHours(new Date(curr.timestamp), new Date(prev.timestamp)) || 0.1;
        
        const prevSpread = prev[bookName];
        const currSpread = curr[bookName];
        
        if (prevSpread !== undefined && currSpread !== undefined) {
          const velocity = Math.abs(currSpread - prevSpread) / timeDiff;
          velocities[bookName].push(velocity);
        }
      }
    });
    
    return velocities;
  }, [chartData, sportsbooks]);

  /**
   * Calculate spread movement stats
   */
  const stats = useMemo(() => {
    if (data.length === 0) return null;

    const firstPoint = data[0];
    const lastPoint = data[data.length - 1];
    const spreadChange = lastPoint.spread - firstPoint.spread;
    const openingSpread = firstPoint.spread;
    const currentSpread = lastPoint.spread;

    return {
      openingSpread,
      currentSpread,
      spreadChange,
      direction: spreadChange > 0 ? 'up' : spreadChange < 0 ? 'down' : 'flat',
      percentChange: Math.abs((spreadChange / openingSpread) * 100).toFixed(1),
    };
  }, [data]);

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-6 text-center">
        <p className="text-red-300 text-sm">{error}</p>
        {onRefresh && (
          <button
            onClick={onRefresh}
            className="mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 rounded-lg text-red-200 text-sm transition-colors"
          >
            Try Again
          </button>
        )}
      </div>
    );
  }

  if (data.length === 0 && !isLoading) {
    return (
      <div className="bg-slate-800/50 border border-white/10 rounded-xl p-6 text-center">
        <p className="text-slate-400 text-sm">
          No historical odds data available for this game
        </p>
      </div>
    );
  }

  return (
    <div style={{
      background: 'transparent',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: '0',
      padding: '20px'
    }}>
      {/* Header with stats and controls */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '24px',
        paddingBottom: '16px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <h3 style={{
            fontSize: '11px',
            fontWeight: '500',
            color: '#999',
            margin: '0',
            textTransform: 'uppercase',
            letterSpacing: '1.2px'
          }}>
            <span className="flex items-center gap-2">
              <BarChart3 className="w-3.5 h-3.5" />
              Interactive Spread Movement Timeline
            </span>
          </h3>
          <p style={{
            color: 'rgba(148, 163, 184, 0.6)',
            fontSize: '11px',
            fontWeight: '400',
            margin: '0'
          }}>
            {homeTeam} vs {awayTeam}
          </p>
        </div>

        <div className="flex items-center gap-6">
          {/* Time Filter Buttons */}
          <div className="flex items-center gap-2">
            {(['all', '7d', '24h'] as const).map(filter => (
              <button
                key={filter}
                onClick={() => setTimeFilter(filter)}
                style={{
                  padding: '6px 12px',
                  fontSize: '11px',
                  fontWeight: '600',
                  borderRadius: '6px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  background: timeFilter === filter 
                    ? 'rgba(59, 130, 246, 0.2)' 
                    : 'transparent',
                  color: timeFilter === filter 
                    ? 'rgba(96, 165, 250, 1)' 
                    : 'rgba(148, 163, 184, 0.7)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em'
                }}
                className="hover:bg-white/5"
              >
                {filter === 'all' ? 'All' : filter === '7d' ? 'Week' : '24h'}
              </button>
            ))}
          </div>

          {/* Annotations Toggle */}
          <button
            onClick={() => setShowAnnotations(!showAnnotations)}
            style={{
              padding: '6px 12px',
              fontSize: '11px',
              fontWeight: '600',
              borderRadius: '6px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              background: showAnnotations 
                ? 'rgba(34, 197, 94, 0.2)' 
                : 'transparent',
              color: showAnnotations 
                ? 'rgba(74, 222, 128, 1)' 
                : 'rgba(148, 163, 184, 0.7)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
            className="hover:bg-white/5"
            title="Toggle movement alerts"
          >
            <Zap className="w-3 h-3" />
            Alerts
          </button>

          {stats && (
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p style={{
                  color: 'rgba(148, 163, 184, 0.6)',
                  fontSize: '11px',
                  fontWeight: '500',
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase'
                }}>Opening</p>
                <p style={{
                  color: 'rgba(226, 232, 240, 0.9)',
                  fontSize: '16px',
                  fontWeight: '600',
                  letterSpacing: '-0.01em'
                }}>
                  {stats.openingSpread > 0 ? '+' : ''}{stats.openingSpread}
                </p>
              </div>

              <div className="flex items-center gap-1.5">
                {stats.direction === 'up' && <TrendingUp className="w-4 h-4" style={{ color: 'rgba(34, 197, 94, 0.8)' }} />}
                {stats.direction === 'down' && <TrendingDown className="w-4 h-4" style={{ color: 'rgba(239, 68, 68, 0.8)' }} />}
                <span style={{
                  fontSize: '13px',
                  fontWeight: '600',
                  color: stats.direction === 'up' ? 'rgba(34, 197, 94, 0.8)' :
                          stats.direction === 'down' ? 'rgba(239, 68, 68, 0.8)' :
                          'rgba(148, 163, 184, 0.7)'
                }}>
                  {stats.spreadChange > 0 ? '+' : ''}{stats.spreadChange.toFixed(1)}
                </span>
              </div>

              <div className="text-left">
                <p style={{
                  color: 'rgba(148, 163, 184, 0.6)',
                  fontSize: '11px',
                  fontWeight: '500',
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase'
                }}>Current</p>
                <p style={{
                  color: 'rgba(226, 232, 240, 0.9)',
                  fontSize: '16px',
                  fontWeight: '600',
                  letterSpacing: '-0.01em'
                }}>
                  {stats.currentSpread > 0 ? '+' : ''}{stats.currentSpread}
                </p>
              </div>
            </div>
          )}

          {onRefresh && (
            <button
              onClick={onRefresh}
              disabled={isLoading}
              style={{
                padding: '8px',
                background: 'transparent',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                opacity: isLoading ? 0.5 : 1,
              }}
              className="hover:bg-white/5"
              title="Refresh data"
            >
              <RefreshCw 
                className={isLoading ? 'animate-spin' : ''}
                style={{
                  width: '18px',
                  height: '18px',
                  color: 'rgba(148, 163, 184, 0.7)',
                  filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.2))'
                }}
              />
            </button>
          )}
        </div>
      </div>

      {/* Smart Insights Panel */}
      {(bestEntryPoint || marketDivergence.length > 0 || significantMovements.length > 0) && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Best Entry Point */}
          {bestEntryPoint && (
            <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-green-500/20 rounded-lg p-4 hover:scale-105 transition-transform">
              <div className="flex items-center gap-2 mb-2">
                <Target className="w-4 h-4 text-green-400" />
                <span className="text-xs font-bold text-green-400 uppercase tracking-wide">Best Entry Point</span>
              </div>
              <p className="text-white text-lg font-bold">{bestEntryPoint.spread > 0 ? '+' : ''}{bestEntryPoint.spread}</p>
              <p className="text-slate-400 text-xs mt-1">{bestEntryPoint.bookName}</p>
              <p className="text-slate-500 text-xs">{format(parseISO(bestEntryPoint.timestamp), 'MMM dd, h:mm a')}</p>
            </div>
          )}

          {/* Market Divergence Alert */}
          {marketDivergence.length > 0 && (
            <div className="bg-gradient-to-br from-amber-500/10 to-orange-500/5 border border-amber-500/20 rounded-lg p-4 hover:scale-105 transition-transform">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span className="text-xs font-bold text-amber-400 uppercase tracking-wide">Market Uncertainty</span>
              </div>
              <p className="text-white text-lg font-bold">{marketDivergence.length} divergence{marketDivergence.length > 1 ? 's' : ''}</p>
              <p className="text-slate-400 text-xs mt-1">Books disagree by ≥3 pts</p>
              <p className="text-slate-500 text-xs">Max range: {Math.max(...marketDivergence.map(d => d.range)).toFixed(1)} pts</p>
            </div>
          )}

          {/* Line Movement Velocity */}
          {significantMovements.length > 0 && (
            <div className="bg-gradient-to-br from-red-500/10 to-pink-500/5 border border-red-500/20 rounded-lg p-4 hover:scale-105 transition-transform">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-4 h-4 text-red-400" />
                <span className="text-xs font-bold text-red-400 uppercase tracking-wide">Rapid Movements</span>
              </div>
              <p className="text-white text-lg font-bold">{significantMovements.length} alert{significantMovements.length > 1 ? 's' : ''}</p>
              <p className="text-slate-400 text-xs mt-1">Significant line changes</p>
              <p className="text-slate-500 text-xs flex items-center gap-1.5">
                {significantMovements[significantMovements.length - 1]?.reason.includes('Sharp') && <Flame className="w-3 h-3" />}
                {significantMovements[significantMovements.length - 1]?.reason.includes('Public') && <Sparkles className="w-3 h-3" />}
                {significantMovements[significantMovements.length - 1]?.reason.includes('Significant') && <TrendingUpIcon className="w-3 h-3" />}
                {significantMovements[significantMovements.length - 1]?.reason}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Interactive Chart */}
      <div className="relative bg-slate-900/30 backdrop-blur-sm border border-white/5 rounded-xl p-6 shadow-2xl shadow-black/20">
        <ResponsiveContainer width="100%" height={450}>
          <LineChart 
            data={chartData}
            onMouseMove={(e: any) => {
              if (e && e.activePayload) {
                setHoveredPoint(e.activePayload[0]?.payload);
              }
            }}
            onMouseLeave={() => setHoveredPoint(null)}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
            
            <XAxis
              dataKey="timestamp"
              stroke="rgba(255, 255, 255, 0.4)"
              tick={{ fill: 'rgba(255, 255, 255, 0.6)', fontSize: 11 }}
              tickFormatter={(value) => format(parseISO(value), 'MM/dd HH:mm')}
            />

            <YAxis
              stroke="rgba(255, 255, 255, 0.4)"
              tick={{ fill: 'rgba(255, 255, 255, 0.6)', fontSize: 11 }}
              domain={['auto', 'auto']}
              tickFormatter={(value) => `${value > 0 ? '+' : ''}${value}`}
            />

            <Tooltip 
              content={<CustomTooltip visibleBooks={visibleBooks} />} 
              cursor={{ 
                stroke: 'rgba(96, 165, 250, 0.5)', 
                strokeWidth: 2, 
                strokeDasharray: '5 5' 
              }}
              animationDuration={200}
            />

            <Legend
              content={<CustomLegend visibleBooks={visibleBooks} onToggleBook={toggleBook} />}
              wrapperStyle={{ paddingTop: '20px' }}
            />

            {/* Brush for zoom/range selection */}
            {chartData.length > 10 && (
              <Brush
                dataKey="timestamp"
                height={35}
                stroke="rgba(96, 165, 250, 0.8)"
                fill="rgba(15, 23, 42, 0.9)"
                tickFormatter={(value) => format(parseISO(value), 'MM/dd')}
                onChange={(range: any) => {
                  if (range && range.startIndex !== undefined && range.endIndex !== undefined) {
                    setBrushDomain([range.startIndex, range.endIndex]);
                  }
                }}
                travellerWidth={12}
                gap={2}
                padding={{ top: 5, bottom: 5 }}
                alwaysShowText={false}
              />
            )}

            {/* Reference areas for market divergence */}
            {showAnnotations && marketDivergence.map((div, idx) => {
              const dataIndex = chartData.findIndex(d => d.timestamp === div.timestamp);
              if (dataIndex === -1) return null;
              
              return (
                <ReferenceArea
                  key={`divergence-${idx}`}
                  x1={chartData[Math.max(0, dataIndex - 1)]?.timestamp}
                  x2={chartData[Math.min(chartData.length - 1, dataIndex + 1)]?.timestamp}
                  fill="rgba(251, 191, 36, 0.1)"
                  stroke="rgba(251, 191, 36, 0.3)"
                  strokeDasharray="3 3"
                />
              );
            })}

            {/* Best entry point marker */}
            {showAnnotations && bestEntryPoint && (
              <ReferenceDot
                x={bestEntryPoint.timestamp}
                y={bestEntryPoint.spread}
                r={8}
                fill="rgba(34, 197, 94, 0.6)"
                stroke="rgba(34, 197, 94, 1)"
                strokeWidth={2}
              />
            )}

            {/* Significant movement markers */}
            {showAnnotations && significantMovements.slice(0, 10).map((mov, idx) => (
              <ReferenceDot
                key={`movement-${idx}`}
                x={mov.timestamp}
                y={mov.spread}
                r={6}
                fill="rgba(239, 68, 68, 0.6)"
                stroke="rgba(239, 68, 68, 1)"
                strokeWidth={2}
              />
            ))}

            {/* Sportsbook lines with velocity-based color coding */}
            {sportsbooks.map(bookId => {
              const bookName = SPORTSBOOK_NAMES[bookId] || `Book ${bookId}`;
              const color = BOOK_COLORS[bookId] || '#94a3b8';
              const isVisible = visibleBooks[bookName] !== false;
              
              if (!isVisible) return null;

              // Calculate average velocity for this book
              const velocities = lineVelocities[bookName] || [];
              const avgVelocity = velocities.length > 0 
                ? velocities.reduce((a, b) => a + b, 0) / velocities.length 
                : 0;
              
              // Color code based on velocity: fast = hot (red tint), stable = cool (blue tint)
              const velocityColor = avgVelocity > 1 
                ? `rgba(239, 68, 68, 0.8)` // Fast moving - red
                : avgVelocity > 0.5 
                ? color // Normal
                : `rgba(59, 130, 246, 0.8)`; // Stable - blue
              
              return (
                <Line
                  key={bookId}
                  type="monotone"
                  dataKey={bookName}
                  stroke={velocityColor}
                  strokeWidth={2.5}
                  dot={{ 
                    fill: velocityColor, 
                    r: 3,
                    strokeWidth: 0 
                  }}
                  activeDot={{ 
                    r: 8, 
                    fill: velocityColor, 
                    stroke: '#fff', 
                    strokeWidth: 2,
                    filter: 'drop-shadow(0 0 8px rgba(96, 165, 250, 0.6))'
                  }}
                  connectNulls
                  animationDuration={1000}
                  animationEasing="ease-in-out"
                />
              );
            })}
          </LineChart>
        </ResponsiveContainer>

        {/* Hover crosshair info panel */}
        {hoveredPoint && (
          <div className="absolute top-6 left-6 bg-slate-900/95 border border-white/20 rounded-lg p-3 shadow-2xl backdrop-blur-sm z-10 animate-fadeIn">
            <p className="text-white text-xs font-bold mb-1 flex items-center gap-2">
              <Activity className="w-3 h-3" />
              All Books at {format(parseISO(hoveredPoint.timestamp), 'h:mm a')}
            </p>
            <div className="space-y-0.5">
              {sportsbooks.map(bookId => {
                const bookName = SPORTSBOOK_NAMES[bookId];
                const value = hoveredPoint[bookName];
                if (value === undefined || visibleBooks[bookName] === false) return null;
                
                return (
                  <div key={bookId} className="flex items-center justify-between gap-3 text-xs">
                    <span className="text-slate-400">{bookName}</span>
                    <span className="text-white font-bold">{value > 0 ? '+' : ''}{value}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Footer with live status */}
      <div className="flex items-center justify-between text-xs text-slate-400 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span>Live data • Updates every 3 minutes</span>
        </div>
        <div className="flex items-center gap-4">
          {chartData.length > 0 && (
            <span className="text-slate-500 flex items-center gap-1">
              <BarChart3 className="w-3 h-3" />
              {chartData.length} data points
            </span>
          )}
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            Last updated: {format(parseISO(lastUpdated), 'h:mm a')}
          </span>
        </div>
      </div>
    </div>
  );
};
