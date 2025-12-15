import React, { useEffect, useRef, useState } from 'react';
import './FieldVisualization.css';

interface FieldVisualizationProps {
  possession: {
    team: string;
    logo?: string;
  };
  fieldPosition: {
    yardLine: number;
    down: number;
    distance: number;
  };
  homeTeam: { 
    name: string; 
    abbr?: string;
    color: string;
    logo?: string;
  };
  awayTeam: { 
    name: string; 
    abbr?: string;
    color: string;
    logo?: string;
  };
  situation?: string;
  playData?: {
    play_type?: string;
    yards_gained?: number;
    start_yard_line?: number;
    end_yard_line?: number;
  };
}

const getOrdinalSuffix = (num: number): string => {
  const j = num % 10;
  const k = num % 100;
  if (j === 1 && k !== 11) return `${num}st`;
  if (j === 2 && k !== 12) return `${num}nd`;
  if (j === 3 && k !== 13) return `${num}rd`;
  return `${num}th`;
};

export const FieldVisualization: React.FC<FieldVisualizationProps> = ({
  possession,
  fieldPosition,
  homeTeam,
  awayTeam,
  situation,
  playData
}) => {
  const [animatedPosition, setAnimatedPosition] = useState(fieldPosition.yardLine);
  const [isAnimating, setIsAnimating] = useState(false);
  const [ballTrajectory, setBallTrajectory] = useState<number[]>([]);
  const animationRef = useRef<number | null>(null);
  const previousYardLine = useRef(fieldPosition.yardLine);

  // Animate ball movement when yard line changes
  useEffect(() => {
    const startYard = previousYardLine.current;
    const endYard = playData?.end_yard_line ?? fieldPosition.yardLine;
    
    // Only animate if there's actual movement
    if (startYard !== endYard && Math.abs(startYard - endYard) > 0) {
      setIsAnimating(true);
      const distance = Math.abs(endYard - startYard);
      const duration = Math.min(1500, 500 + distance * 30); // Dynamic duration based on distance
      const startTime = Date.now();
      
      // Generate parabolic trajectory points for 3D effect
      const generateTrajectory = () => {
        const points: number[] = [];
        for (let t = 0; t <= 1; t += 0.05) {
          // Parabolic height calculation (peaks at midpoint)
          const height = 4 * distance * t * (1 - t); // Max height proportional to distance
          const position = startYard + (endYard - startYard) * t;
          points.push(position);
        }
        return points;
      };
      
      setBallTrajectory(generateTrajectory());
      
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease-out animation for smooth deceleration
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const currentYard = startYard + (endYard - startYard) * easeProgress;
        
        setAnimatedPosition(currentYard);
        
        if (progress < 1) {
          animationRef.current = requestAnimationFrame(animate);
        } else {
          setIsAnimating(false);
          setBallTrajectory([]);
          previousYardLine.current = endYard;
        }
      };
      
      animationRef.current = requestAnimationFrame(animate);
      
      return () => {
        if (animationRef.current) {
          cancelAnimationFrame(animationRef.current);
        }
      };
    } else {
      // No animation needed, just update position
      setAnimatedPosition(endYard);
      previousYardLine.current = endYard;
    }
  }, [fieldPosition.yardLine, playData]);

  // Calculate ball position percentage (0-100)
  const ballPositionPercent = (animatedPosition / 100) * 100;
  
  // Determine which team has possession
  const isPossessionHome = possession.team.toLowerCase().includes(homeTeam.name.toLowerCase()) ||
                           homeTeam.name.toLowerCase().includes(possession.team.toLowerCase());
  
  const possessionColor = isPossessionHome ? homeTeam.color : awayTeam.color;
  const possessionLogo = isPossessionHome ? homeTeam.logo : awayTeam.logo;
  
  return (
    <div 
      className="field-visualization-container"
      style={{
        boxShadow: `0 8px 32px 0 ${possessionColor}30, 0 0 0 1px ${possessionColor}20`
      }}
    >
      <div className="field-header">
        <h3>Field Position</h3>
      </div>
      
      <div className="field-wrapper">
        {/* Away Team Endzone (Left) */}
        <div 
          className="endzone endzone-away"
          style={{ 
            background: `linear-gradient(135deg, ${awayTeam.color}40 0%, ${awayTeam.color}20 100%)`,
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            border: `1px solid ${awayTeam.color}50`,
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          {awayTeam.logo && (
            <img 
              src={awayTeam.logo} 
              alt={awayTeam.name}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '60px',
                height: '60px',
                objectFit: 'contain',
                opacity: 0.15,
                filter: 'brightness(1.5)',
                pointerEvents: 'none'
              }}
            />
          )}
          <div className="endzone-content">
            {awayTeam.logo && <img src={awayTeam.logo} alt={awayTeam.name} className="endzone-logo" />}
            <span className="endzone-text" style={{ color: awayTeam.color, textShadow: `0 2px 8px ${awayTeam.color}80` }}>
              {awayTeam.abbr || awayTeam.name.substring(0, 3).toUpperCase()}
            </span>
          </div>
        </div>
        
        {/* Football Field */}
        <div className="field">
          {/* Home Team Logo at 50 yard line */}
          {homeTeam.logo && (
            <img 
              src={homeTeam.logo} 
              alt={homeTeam.name}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '220px',
                height: '220px',
                objectFit: 'contain',
                opacity: 0.12,
                filter: 'brightness(1.3)',
                pointerEvents: 'none',
                zIndex: 1
              }}
            />
          )}
          
          {/* Yard lines */}
          <div className="yard-markers">
            {[10, 20, 30, 40, 50, 40, 30, 20, 10].map((yard, idx) => (
              <div key={idx} className="yard-marker">
                <span className="yard-number">{yard}</span>
              </div>
            ))}
          </div>
          
          {/* Ball Position */}
          <div 
            className="ball-position"
            style={{ left: `${ballPositionPercent}%` }}
          >
            {/* 3D Ball Trajectory Arc (visible during animation) */}
            {isAnimating && ballTrajectory.length > 0 && (
              <svg
                style={{
                  position: 'absolute',
                  top: '-80px',
                  left: '-200px',
                  width: '400px',
                  height: '160px',
                  pointerEvents: 'none',
                  zIndex: 10,
                  overflow: 'visible'
                }}
              >
                <defs>
                  <linearGradient id="ballTrailGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor={possessionColor} stopOpacity="0.1" />
                    <stop offset="50%" stopColor={possessionColor} stopOpacity="0.4" />
                    <stop offset="100%" stopColor={possessionColor} stopOpacity="0.8" />
                  </linearGradient>
                  <filter id="ballGlow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
                {/* Draw parabolic arc */}
                <path
                  d={(() => {
                    const startYard = previousYardLine.current;
                    const endYard = playData?.end_yard_line ?? fieldPosition.yardLine;
                    const distance = Math.abs(endYard - startYard);
                    const points = ballTrajectory.map((_, idx) => {
                      const t = idx / (ballTrajectory.length - 1);
                      const x = 200 + (t - 0.5) * 300; // Centered arc
                      const y = 140 - (4 * distance * t * (1 - t) * 3); // Parabolic height
                      return `${x},${y}`;
                    });
                    return `M ${points.join(' L ')}`;
                  })()}
                  stroke="url(#ballTrailGradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                  filter="url(#ballGlow)"
                  opacity="0.7"
                />
              </svg>
            )}

            <div 
              className="ball-marker"
              style={{
                background: 'transparent',
                boxShadow: 'none',
                width: '64px',
                height: '64px',
                transform: isAnimating ? 'scale(1.2) rotateY(360deg)' : 'scale(1)',
                transition: isAnimating ? 'transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)' : 'none',
                filter: isAnimating ? `drop-shadow(0 8px 24px ${possessionColor}90) brightness(1.3)` : 'none'
              }}
            >
              {possessionLogo ? (
                <img 
                  src={possessionLogo} 
                  alt={possession.team} 
                  style={{
                    width: '64px',
                    height: '64px',
                    objectFit: 'contain',
                    filter: `drop-shadow(0 4px 12px ${possessionColor}80) brightness(1.1)`,
                    opacity: 0.95,
                    animation: isAnimating ? 'ballSpin 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)' : 'none'
                  }}
                />
              ) : (
                <span 
                  className="football-icon"
                  style={{
                    animation: isAnimating ? 'ballSpin 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)' : 'none'
                  }}
                >
                  🏈
                </span>
              )}
            </div>
            
            {/* Pulsing ground indicator */}
            {isAnimating && (
              <div
                style={{
                  position: 'absolute',
                  bottom: '-8px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '40px',
                  height: '8px',
                  background: `radial-gradient(ellipse, ${possessionColor}60 0%, transparent 70%)`,
                  borderRadius: '50%',
                  animation: 'groundPulse 0.6s ease-in-out infinite'
                }}
              />
            )}
          </div>
          
          {/* Hash marks (decorative) */}
          <div className="hash-marks" />
        </div>
        
        {/* Home Team Endzone (Right) */}
        <div 
          className="endzone endzone-home"
          style={{ 
            background: `linear-gradient(135deg, ${homeTeam.color}40 0%, ${homeTeam.color}20 100%)`,
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            border: `1px solid ${homeTeam.color}50`,
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          {homeTeam.logo && (
            <img 
              src={homeTeam.logo} 
              alt={homeTeam.name}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '60px',
                height: '60px',
                objectFit: 'contain',
                opacity: 0.15,
                filter: 'brightness(1.5)',
                pointerEvents: 'none'
              }}
            />
          )}
          <div className="endzone-content">
            {homeTeam.logo && <img src={homeTeam.logo} alt={homeTeam.name} className="endzone-logo" />}
            <span className="endzone-text" style={{ color: homeTeam.color, textShadow: `0 2px 8px ${homeTeam.color}80` }}>
              {homeTeam.abbr || homeTeam.name.substring(0, 3).toUpperCase()}
            </span>
          </div>
        </div>
      </div>
      
      {/* Game Situation */}
      <div className="field-info">
        <div className="down-distance">
          <span className="down-text">
            {getOrdinalSuffix(fieldPosition.down)} & {fieldPosition.distance}
          </span>
          {situation && (
            <span className="situation-text">{situation}</span>
          )}
        </div>
        
        <div className="possession-indicator">
          <span className="possession-label">Possession:</span>
          <span className="possession-team" style={{ 
            color: isPossessionHome ? homeTeam.color : awayTeam.color 
          }}>
            {possession.team}
          </span>
        </div>
      </div>
    </div>
  );
};

export default FieldVisualization;
