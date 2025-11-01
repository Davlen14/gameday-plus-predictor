import React, { useState } from 'react';
import { Activity } from 'lucide-react';
import './LivePlaysFeed.css';

interface Play {
  id: string;
  period: number;
  clock: string;
  team: string;
  down?: number;
  distance?: number;
  yards_to_goal?: number;
  yards_gained?: number;
  play_type: string;
  play_text: string;
  home_score: number;
  away_score: number;
  epa?: number;
  success?: boolean;
}

interface LivePlaysFeedProps {
  plays: Play[];
  limit?: number;
  showEPA?: boolean;
  predictionData?: any;
}

export const LivePlaysFeed: React.FC<LivePlaysFeedProps> = ({ 
  plays, 
  limit,
  showEPA = true,
  predictionData
}) => {
  const [selectedQuarter, setSelectedQuarter] = useState<number | 'all'>('all');
  
  // Get team colors
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;
  
  const getTeamColor = (teamName: string) => {
    if (teamName === awayTeam?.name || teamName === awayTeam?.school) {
      return awayTeam?.primary_color || '#3b82f6';
    } else if (teamName === homeTeam?.name || teamName === homeTeam?.school) {
      return homeTeam?.primary_color || '#dc2626';
    }
    return 'rgba(255, 255, 255, 0.9)';
  };
  
  const getTeamLogo = (teamName: string) => {
    if (teamName === awayTeam?.name || teamName === awayTeam?.school) {
      return awayTeam?.logo;
    } else if (teamName === homeTeam?.name || teamName === homeTeam?.school) {
      return homeTeam?.logo;
    }
    return null;
  };
  
  // Group plays by quarter
  const quarters = Array.from(new Set(plays.map(p => p.period))).sort((a, b) => a - b);
  
  // Filter plays based on selected quarter
  const filteredPlays = selectedQuarter === 'all' 
    ? plays 
    : plays.filter(p => p.period === selectedQuarter);
  
  return (
    <div className="live-plays-container">
      <div className="plays-header">
        <h3><Activity className="inline-block w-5 h-5 mr-2" /> All Plays</h3>
        <div className="quarter-filter">
          <button 
            className={`quarter-btn ${selectedQuarter === 'all' ? 'active' : ''}`}
            onClick={() => setSelectedQuarter('all')}
          >
            All
          </button>
          {quarters.map(q => (
            <button 
              key={q}
              className={`quarter-btn ${selectedQuarter === q ? 'active' : ''}`}
              onClick={() => setSelectedQuarter(q)}
            >
              Q{q}
            </button>
          ))}
        </div>
      </div>
      
      <div className="plays-list">
        {filteredPlays.map((play, idx) => (
          <div 
            key={play.id || idx} 
            className={`play-item ${play.success ? 'play-success' : 'play-failure'}`}
            style={{
              backgroundImage: `linear-gradient(135deg, ${getTeamColor(play.team)}15 0%, ${getTeamColor(play.team)}05 100%)`,
              backdropFilter: 'blur(10px)',
              WebkitBackdropFilter: 'blur(10px)'
            }}
          >
            {getTeamLogo(play.team) && (
              <img 
                src={getTeamLogo(play.team)!} 
                alt={play.team}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '70px',
                  height: '70px',
                  objectFit: 'contain',
                  opacity: 0.08,
                  pointerEvents: 'none'
                }}
              />
            )}
            <div className="play-header-row">
              <div className="play-meta">
                <span className="play-quarter">Q{play.period}</span>
                <span className="play-clock">{play.clock}</span>
                <span className="play-team" style={{ color: getTeamColor(play.team) }}>{play.team}</span>
              </div>
              
              <div className="play-score">
                {play.home_score} - {play.away_score}
              </div>
            </div>
            
            <div className="play-description">
              {play.down && play.distance && (
                <span className="play-situation">
                  {play.down}
                  {play.down === 1 ? 'st' : play.down === 2 ? 'nd' : play.down === 3 ? 'rd' : 'th'}
                  {' & '}{play.distance}
                  {play.yards_to_goal && ` at ${play.yards_to_goal}`}
                  {' - '}
                </span>
              )}
              <span className="play-text">
                {play.play_text.length > 120 
                  ? `${play.play_text.substring(0, 120)}...` 
                  : play.play_text}
              </span>
            </div>
            
            <div className="play-stats-row">
              {play.yards_gained !== undefined && play.yards_gained !== null && (
                <span className={`yards-gained ${play.yards_gained > 0 ? 'positive' : play.yards_gained < 0 ? 'negative' : 'neutral'}`}>
                  {play.yards_gained > 0 ? '+' : ''}{play.yards_gained} yds
                </span>
              )}
              
              {showEPA && play.epa !== undefined && play.epa !== null && (
                <span className={`epa-value ${play.epa > 0 ? 'epa-positive' : play.epa < 0 ? 'epa-negative' : 'epa-neutral'}`}>
                  EPA: {play.epa.toFixed(2)}
                </span>
              )}
              
              {play.success !== undefined && (
                <span className={`success-indicator ${play.success ? 'success-yes' : 'success-no'}`}>
                  {play.success ? '✓ Success' : '✗ Failed'}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {plays.length === 0 && (
        <div className="no-plays">
          <p>No plays available yet</p>
        </div>
      )}
      
      <div className="plays-footer">
        <span className="plays-count">
          {selectedQuarter === 'all' 
            ? `Showing all ${plays.length} plays` 
            : `Showing ${filteredPlays.length} plays from Q${selectedQuarter}`
          }
        </span>
      </div>
    </div>
  );
};

export default LivePlaysFeed;
