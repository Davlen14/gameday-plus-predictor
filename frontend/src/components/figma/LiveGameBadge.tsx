import React from 'react';
import './LiveGameBadge.css';

interface LiveGameBadgeProps {
  period: number;
  clock: string;
}

export const LiveGameBadge: React.FC<LiveGameBadgeProps> = ({ period, clock }) => {
  return (
    <div className="live-badge-container">
      <div className="live-badge">
        <span className="pulse-dot" />
        <span className="live-text">LIVE</span>
        <span className="game-time">Q{period} - {clock}</span>
      </div>
    </div>
  );
};

export default LiveGameBadge;
