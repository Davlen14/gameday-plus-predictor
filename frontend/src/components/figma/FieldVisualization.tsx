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
  
  return (
    <div className="field-visualization-container">
      <div className="field-header">
        <h3>Field Position</h3>
      </div>
      
      <div className="field-wrapper">
        {/* Away Team Endzone (Left) */}
        <div 
          className="endzone endzone-away"
          style={{ backgroundColor: awayTeam.color }}
        >
          <div className="endzone-content">
            {awayTeam.logo && <img src={awayTeam.logo} alt={awayTeam.name} className="endzone-logo" />}
            <span className="endzone-text">{awayTeam.abbr || awayTeam.name.substring(0, 3).toUpperCase()}</span>
          </div>
        </div>
        
        {/* Football Field */}
        <div className="field">
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
            <div className="ball-marker">
              {possession.logo ? (
                <img src={possession.logo} alt={possession.team} className="ball-team-logo" />
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
          style={{ backgroundColor: homeTeam.color }}
        >
          <div className="endzone-content">
            {homeTeam.logo && <img src={homeTeam.logo} alt={homeTeam.name} className="endzone-logo" />}
            <span className="endzone-text">{homeTeam.abbr || homeTeam.name.substring(0, 3).toUpperCase()}</span>
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
