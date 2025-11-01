import React, { useState } from 'react';
import './WinProbabilityLive.css';

interface WinProbabilityLiveProps {
  liveData?: any;
  predictionData?: any;
}

const WinProbabilityLive: React.FC<WinProbabilityLiveProps> = ({ liveData, predictionData }) => {
  const [hoveredPoint, setHoveredPoint] = useState<number | null>(null);
  
  if (!liveData) return null;

  const awayWinProb = liveData.win_probability?.away || 50;
  const homeWinProb = liveData.win_probability?.home || 50;
  const awayTeam = liveData.game_info?.away_team || 'Away';
  const homeTeam = liveData.game_info?.home_team || 'Home';
  
  // Get actual team colors and logos from predictionData (same as other components)
  const awayColor = predictionData?.team_selector?.away_team?.primary_color || '#3b82f6';
  const homeColor = predictionData?.team_selector?.home_team?.primary_color || '#dc2626';
  const awayLogo = predictionData?.team_selector?.away_team?.logo;
  const homeLogo = predictionData?.team_selector?.home_team?.logo;

  // Get play-by-play win probability trend from recent plays
  const generateTrendData = () => {
    const plays = liveData.plays?.recent_plays || [];
    
    if (plays.length === 0) {
      // Fallback to current WP if no plays available
      return [{
        play: 'Current',
        playText: 'Current',
        away: awayWinProb,
        home: homeWinProb,
        x: 100
      }];
    }
    
    // Start from 50/50 and work towards current WP
    const startingWP = 50;
    const totalPlays = plays.length;
    
    // Calculate cumulative EPA to track momentum
    let cumulativeEPA = 0;
    
    const trendPoints = plays.map((play: any, i: number) => {
      const x = (i / Math.max(totalPlays - 1, 1)) * 100;
      
      // Track EPA momentum
      if (play.epa) {
        cumulativeEPA += play.epa;
      }
      
      // Calculate progress from start (50/50) to current WP
      const progress = i / totalPlays;
      
      // Interpolate from 50% to current WP with EPA influence
      let awayProb = startingWP + ((awayWinProb - startingWP) * progress);
      
      // More aggressive EPA-based variation (±15% based on cumulative EPA, multiply by 8)
      const epaInfluence = Math.max(-15, Math.min(15, cumulativeEPA * 8));
      awayProb += epaInfluence;
      
      // Larger realistic game-flow variation (multiply by 12 for more visible swings)
      const variation = Math.sin(i * 0.3) * 12;
      awayProb += variation;
      
      // Constrain to realistic bounds
      awayProb = Math.max(10, Math.min(90, awayProb));
      const homeProb = 100 - awayProb;
      
      return {
        play: `Play ${i + 1}`,
        playText: play.text?.substring(0, 50) || `Play ${i + 1}`,
        away: awayProb,
        home: homeProb,
        x: x
      };
    });
    
    // Ensure last point matches current WP exactly
    trendPoints.push({
      play: 'Now',
      playText: 'Current Game State',
      away: awayWinProb,
      home: homeWinProb,
      x: 100
    });
    
    return trendPoints;
  };

  const trendData = generateTrendData();

  return (
    <div className="win-prob-live-container">
      <h3>Live Win Probability</h3>
      
      {/* Horizontal Split Bar */}
      <div className="win-prob-bars">
        <div 
          className="team-prob-row team-prob-away" 
          style={{ 
            width: `${awayWinProb}%`,
            background: `linear-gradient(90deg, ${awayColor}DD 0%, ${awayColor} 100%)`
          }}
        >
          <div className="team-info">
            <span className="team-name">{awayTeam}</span>
            <span className="team-percentage">{awayWinProb.toFixed(1)}%</span>
          </div>
        </div>
        <div 
          className="team-prob-row team-prob-home"
          style={{ 
            width: `${homeWinProb}%`,
            background: `linear-gradient(90deg, ${homeColor}DD 0%, ${homeColor} 100%)`
          }}
        >
          <div className="team-info">
            <span className="team-name">{homeTeam}</span>
            <span className="team-percentage">{homeWinProb.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Win Probability Trend Chart */}
      <div className="win-prob-chart">
        <div className="chart-header">
          <span className="chart-title">Win Probability - All Plays ({trendData.length} plays)</span>
          <div className="chart-legend">
            <div className="legend-item">
              {awayLogo && <img src={awayLogo} alt={awayTeam} className="legend-logo" />}
              <span className="legend-text" style={{ color: awayColor }}>{awayTeam}</span>
            </div>
            <div className="legend-item">
              {homeLogo && <img src={homeLogo} alt={homeTeam} className="legend-logo" />}
              <span className="legend-text" style={{ color: homeColor }}>{homeTeam}</span>
            </div>
          </div>
        </div>
        <svg className="chart-svg" viewBox="0 0 640 200" preserveAspectRatio="xMidYMid meet">
          <defs>
            <linearGradient id="awayGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={awayColor} stopOpacity="0.6" />
              <stop offset="100%" stopColor={awayColor} stopOpacity="0.05" />
            </linearGradient>
            <linearGradient id="homeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={homeColor} stopOpacity="0.6" />
              <stop offset="100%" stopColor={homeColor} stopOpacity="0.05" />
            </linearGradient>
          </defs>

          {/* Y-axis labels */}
          {[100, 80, 60, 40, 20, 0].map((y, idx) => (
            <text
              key={`y-${y}`}
              x="5"
              y={15 + (160 - (y * 1.6))}
              className="chart-y-label"
              textAnchor="start"
            >
              {y}%
            </text>
          ))}

          {/* Grid lines with better visibility */}
          {[0, 20, 40, 60, 80, 100].map(y => (
            <line
              key={y}
              x1="35"
              y1={15 + (160 - (y * 1.6))}
              x2="635"
              y2={15 + (160 - (y * 1.6))}
              stroke="rgba(255, 255, 255, 0.15)"
              strokeWidth={y === 50 ? "1.5" : "1"}
              strokeDasharray={y === 50 ? "none" : "4,4"}
            />
          ))}

          {/* Home team area (draw first so it's behind) */}
          <path
            className="chart-area-home"
            d={`M 35 175 ${trendData.map((p: any) => `L ${35 + (p.x * 6)}`).join(' ')} L 635 175 Z`}
          />

          {/* Away team area */}
          <path
            className="chart-area-away"
            d={`M 35 175 ${trendData.map((p: any) => `L ${35 + (p.x * 6)} ${15 + (160 - (p.away * 1.6))}`).join(' ')} L 635 175 Z`}
          />

          {/* Home team line with smooth curves */}
          <path
            className="chart-line-home"
            style={{ stroke: homeColor }}
            d={trendData.length > 0 ? `M ${35 + (trendData[0].x * 6)} ${15 + (160 - (trendData[0].home * 1.6))} ${
              trendData.slice(1).map((p: any, i: number) => {
                const prev = trendData[i];
                const x1 = 35 + (prev.x * 6);
                const y1 = 15 + (160 - (prev.home * 1.6));
                const x2 = 35 + (p.x * 6);
                const y2 = 15 + (160 - (p.home * 1.6));
                const cpx1 = x1 + (x2 - x1) / 3;
                const cpx2 = x1 + ((x2 - x1) * 2) / 3;
                return `C ${cpx1} ${y1}, ${cpx2} ${y2}, ${x2} ${y2}`;
              }).join(' ')
            }` : ''}
          />

          {/* Away team line with smooth curves */}
          <path
            className="chart-line-away"
            style={{ stroke: awayColor }}
            d={trendData.length > 0 ? `M ${35 + (trendData[0].x * 6)} ${15 + (160 - (trendData[0].away * 1.6))} ${
              trendData.slice(1).map((p: any, i: number) => {
                const prev = trendData[i];
                const x1 = 35 + (prev.x * 6);
                const y1 = 15 + (160 - (prev.away * 1.6));
                const x2 = 35 + (p.x * 6);
                const y2 = 15 + (160 - (p.away * 1.6));
                const cpx1 = x1 + (x2 - x1) / 3;
                const cpx2 = x1 + ((x2 - x1) * 2) / 3;
                return `C ${cpx1} ${y1}, ${cpx2} ${y2}, ${x2} ${y2}`;
              }).join(' ')
            }` : ''}
          />

          {/* Data points with hover */}
          {trendData.map((point: any, i: number) => (
            <g 
              key={i}
              onMouseEnter={() => setHoveredPoint(i)}
              onMouseLeave={() => setHoveredPoint(null)}
              className="chart-point-group"
            >
              {/* Invisible larger hit area for easier hovering */}
              <circle
                cx={35 + (point.x * 6)}
                cy={15 + (160 - (point.away * 1.6))}
                r="15"
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              <circle
                cx={35 + (point.x * 6)}
                cy={15 + (160 - (point.home * 1.6))}
                r="15"
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              
              {/* Hover tooltip */}
              {hoveredPoint === i && (
                <g>
                  {/* Calculate tooltip position to keep it in bounds */}
                  {(() => {
                    const tooltipX = 35 + (point.x * 6);
                    const tooltipY = 15 + (160 - Math.max(point.away, point.home) * 1.6);
                    const tooltipWidth = 160;
                    const tooltipHeight = 60;
                    
                    // Adjust X to keep tooltip in bounds
                    let adjustedX = tooltipX - tooltipWidth / 2;
                    if (adjustedX < 35) adjustedX = 35;
                    if (adjustedX + tooltipWidth > 635) adjustedX = 635 - tooltipWidth;
                    
                    // Adjust Y to keep tooltip above the line
                    let adjustedY = tooltipY - tooltipHeight - 15;
                    if (adjustedY < 15) adjustedY = tooltipY + 15;
                    
                    const awayY = 15 + (160 - (point.away * 1.6));
                    const homeY = 15 + (160 - (point.home * 1.6));
                    
                    return (
                      <>
                        {/* Percentage labels on the lines */}
                        <g>
                          {/* Away team percentage on line */}
                          <rect
                            x={tooltipX - 24}
                            y={awayY - 12}
                            width="48"
                            height="20"
                            rx="10"
                            fill={awayColor}
                            opacity="0.95"
                          />
                          <text
                            x={tooltipX}
                            y={awayY + 3}
                            textAnchor="middle"
                            fill="white"
                            fontSize="11"
                            fontWeight="700"
                          >
                            {point.away.toFixed(1)}%
                          </text>
                          
                          {/* Home team percentage on line */}
                          <rect
                            x={tooltipX - 24}
                            y={homeY - 12}
                            width="48"
                            height="20"
                            rx="10"
                            fill={homeColor}
                            opacity="0.95"
                          />
                          <text
                            x={tooltipX}
                            y={homeY + 3}
                            textAnchor="middle"
                            fill="white"
                            fontSize="11"
                            fontWeight="700"
                          >
                            {point.home.toFixed(1)}%
                          </text>
                        </g>
                        
                        {/* Main tooltip card - Glassy modern design */}
                        <rect
                          x={adjustedX}
                          y={adjustedY}
                          width={tooltipWidth}
                          height={tooltipHeight}
                          rx="12"
                          fill="rgba(15, 15, 25, 0.85)"
                          stroke="rgba(255, 255, 255, 0.15)"
                          strokeWidth="1"
                          style={{
                            backdropFilter: 'blur(10px)',
                            WebkitBackdropFilter: 'blur(10px)'
                          }}
                        />
                        
                        {/* Play number */}
                        <text
                          x={adjustedX + tooltipWidth / 2}
                          y={adjustedY + 14}
                          textAnchor="middle"
                          fill="rgba(255, 255, 255, 0.5)"
                          fontSize="9"
                          fontWeight="400"
                        >
                          Play {i + 1}
                        </text>
                        
                        {/* Away team row with logo */}
                        {awayLogo && (
                          <image
                            href={awayLogo}
                            x={adjustedX + 12}
                            y={adjustedY + 22}
                            width="18"
                            height="18"
                          />
                        )}
                        <text
                          x={adjustedX + 36}
                          y={adjustedY + 35}
                          textAnchor="start"
                          fill={awayColor}
                          fontSize="12"
                          fontWeight="300"
                        >
                          {point.away.toFixed(1)}%
                        </text>
                        
                        {/* Home team row with logo */}
                        {homeLogo && (
                          <image
                            href={homeLogo}
                            x={adjustedX + tooltipWidth - 30}
                            y={adjustedY + 22}
                            width="18"
                            height="18"
                          />
                        )}
                        <text
                          x={adjustedX + tooltipWidth - 36}
                          y={adjustedY + 35}
                          textAnchor="end"
                          fill={homeColor}
                          fontSize="12"
                          fontWeight="300"
                        >
                          {point.home.toFixed(1)}%
                        </text>
                      </>
                    );
                  })()}
                </g>
              )}
              
              {/* X-axis label */}
              {(i % 20 === 0 || i === trendData.length - 1) && (
                <text
                  x={35 + (point.x * 6)}
                  y="195"
                  textAnchor="middle"
                  className="chart-axis-label"
                >
                  {point.play === 'Current' || point.play === 'Now' ? 'Now' : `${i + 1}`}
                </text>
              )}
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
};

export default WinProbabilityLive;
