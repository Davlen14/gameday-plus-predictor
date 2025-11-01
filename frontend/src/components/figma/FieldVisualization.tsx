import React from 'react';
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
  situation
}) => {
  // Calculate ball position percentage (0-100)
  const ballPositionPercent = (fieldPosition.yardLine / 100) * 100;
  
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
            <div 
              className="ball-marker"
              style={{
                background: 'transparent',
                boxShadow: 'none',
                width: '64px',
                height: '64px'
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
                    opacity: 0.95
                  }}
                />
              ) : (
                <span className="football-icon">🏈</span>
              )}
            </div>
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
