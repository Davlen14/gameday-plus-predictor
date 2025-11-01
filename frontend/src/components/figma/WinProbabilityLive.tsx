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
        <svg className="chart-svg" viewBox="0 0 700 200" preserveAspectRatio="xMidYMid meet">
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
              x="10"
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
              x1="50"
              y1={15 + (160 - (y * 1.6))}
              x2="690"
              y2={15 + (160 - (y * 1.6))}
              stroke="rgba(255, 255, 255, 0.15)"
              strokeWidth={y === 50 ? "1.5" : "1"}
              strokeDasharray={y === 50 ? "none" : "4,4"}
            />
          ))}

          {/* Home team area (draw first so it's behind) */}
          <path
            className="chart-area-home"
            d={`M 50 175 ${trendData.map((p: any) => `L ${50 + (p.x * 6.4)} ${15 + (160 - (p.home * 1.6))}`).join(' ')} L 690 175 Z`}
          />

          {/* Away team area */}
          <path
            className="chart-area-away"
            d={`M 50 175 ${trendData.map((p: any) => `L ${50 + (p.x * 6.4)} ${15 + (160 - (p.away * 1.6))}`).join(' ')} L 690 175 Z`}
          />

          {/* Home team line with smooth curves */}
          <path
            className="chart-line-home"
            style={{ stroke: homeColor }}
            d={trendData.length > 0 ? `M ${50 + (trendData[0].x * 6.4)} ${15 + (160 - (trendData[0].home * 1.6))} ${
              trendData.slice(1).map((p: any, i: number) => {
                const prev = trendData[i];
                const x1 = 50 + (prev.x * 6.4);
                const y1 = 15 + (160 - (prev.home * 1.6));
                const x2 = 50 + (p.x * 6.4);
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
            d={trendData.length > 0 ? `M ${50 + (trendData[0].x * 6.4)} ${15 + (160 - (trendData[0].away * 1.6))} ${
              trendData.slice(1).map((p: any, i: number) => {
                const prev = trendData[i];
                const x1 = 50 + (prev.x * 6.4);
                const y1 = 15 + (160 - (prev.away * 1.6));
                const x2 = 50 + (p.x * 6.4);
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
                cx={50 + (point.x * 6.4)}
                cy={15 + (160 - (point.away * 1.6))}
                r="15"
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              <circle
                cx={50 + (point.x * 6.4)}
                cy={15 + (160 - (point.home * 1.6))}
                r="15"
                fill="transparent"
                style={{ cursor: 'pointer' }}
              />
              
              {/* Away team point */}
              <circle
                cx={50 + (point.x * 6.4)}
                cy={15 + (160 - (point.away * 1.6))}
                r={hoveredPoint === i ? "6" : "4"}
                fill={awayColor}
                stroke="rgba(255,255,255,0.9)"
                strokeWidth={hoveredPoint === i ? "3" : "2"}
                className="chart-point"
              />
              
              {/* Home team point */}
              <circle
                cx={50 + (point.x * 6.4)}
                cy={15 + (160 - (point.home * 1.6))}
                r={hoveredPoint === i ? "6" : "4"}
                fill={homeColor}
                stroke="rgba(255,255,255,0.9)"
                strokeWidth={hoveredPoint === i ? "3" : "2"}
                className="chart-point"
              />
              
              {/* Hover tooltip */}
              {hoveredPoint === i && (
                <g>
                  {/* Calculate tooltip position to keep it in bounds */}
                  {(() => {
                    const tooltipX = 50 + (point.x * 6.4);
                    const tooltipY = 15 + (160 - Math.max(point.away, point.home) * 1.6);
                    const tooltipWidth = 200;
                    const tooltipHeight = 70;
                    
                    // Adjust X to keep tooltip in bounds
                    let adjustedX = tooltipX - tooltipWidth / 2;
                    if (adjustedX < 50) adjustedX = 50;
                    if (adjustedX + tooltipWidth > 690) adjustedX = 690 - tooltipWidth;
                    
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
                            x={tooltipX - 28}
                            y={awayY - 14}
                            width="56"
                            height="22"
                            rx="11"
                            fill={awayColor}
                            opacity="0.95"
                          />
                          <text
                            x={tooltipX}
                            y={awayY + 4}
                            textAnchor="middle"
                            fill="white"
                            fontSize="13"
                            fontWeight="800"
                          >
                            {point.away.toFixed(1)}%
                          </text>
                          
                          {/* Home team percentage on line */}
                          <rect
                            x={tooltipX - 28}
                            y={homeY - 14}
                            width="56"
                            height="22"
                            rx="11"
                            fill={homeColor}
                            opacity="0.95"
                          />
                          <text
                            x={tooltipX}
                            y={homeY + 4}
                            textAnchor="middle"
                            fill="white"
                            fontSize="13"
                            fontWeight="800"
                          >
                            {point.home.toFixed(1)}%
                          </text>
                        </g>
                        
                        {/* Main tooltip card */}
                        <rect
                          x={adjustedX}
                          y={adjustedY}
                          width={tooltipWidth}
                          height={tooltipHeight}
                          rx="8"
                          fill="rgba(20, 20, 30, 0.98)"
                          stroke="rgba(255, 255, 255, 0.3)"
                          strokeWidth="1.5"
                        />
                        <text
                          x={adjustedX + tooltipWidth / 2}
                          y={adjustedY + 18}
                          textAnchor="middle"
                          fill="rgba(255, 255, 255, 0.9)"
                          fontSize="11"
                          fontWeight="600"
                        >
                          {point.play}
                        </text>
                        <text
                          x={adjustedX + tooltipWidth / 2}
                          y={adjustedY + 36}
                          textAnchor="middle"
                          fill={awayColor}
                          fontSize="13"
                          fontWeight="700"
                        >
                          {awayTeam}: {point.away.toFixed(1)}%
                        </text>
                        <text
                          x={adjustedX + tooltipWidth / 2}
                          y={adjustedY + 54}
                          textAnchor="middle"
                          fill={homeColor}
                          fontSize="13"
                          fontWeight="700"
                        >
                          {homeTeam}: {point.home.toFixed(1)}%
                        </text>
                      </>
                    );
                  })()}
                </g>
              )}
              
              {/* X-axis label */}
              <text
                x={50 + (point.x * 6.4)}
                y="195"
                textAnchor="middle"
                className="chart-axis-label"
              >
                {point.play === 'Current' ? 'Now' : `${i + 1}`}
              </text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
};

export default WinProbabilityLive;
