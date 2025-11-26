import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus, Target, Shield, Activity } from 'lucide-react';
import { CONFIG } from '../../config';
import { PlayerPropsModal } from './PlayerPropsModal';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface GameLog {
  week: number;
  opponent: string;
  home_away: string;
  result: string;
  stats: { [key: string]: number };
  defense_rank: number | null;
}

interface PlayerProp {
  player_name: string;
  player_team: string;
  position: string;
  prop_type: string;
  line?: number;
  over_under_line: number;
  confidence: number;
  recommendation: string;
  reasoning: string;
  season_average: number;
  weather_impact: string;
  game_logs: GameLog[];
  trend_analysis: {
    last_3_games_avg: number;
    last_5_games_avg: number;
    season_avg: number;
    vs_good_defenses_avg: number;
    vs_poor_defenses_avg: number;
    home_vs_away_diff: number;
    trend_direction: string;
  };
  defensive_matchup: {
    opponent: string;
    category: string;
    sp_plus_rank: number | null;
    sp_plus_rating: number | null;
  };
  key_insights: string[];
}

interface PlayerPropsData {
  matchup: {
    team1: string;
    team2: string;
  };
  team1_props: PlayerProp[];
  team2_props: PlayerProp[];
  total_props: number;
}

interface PlayerPropsPanelProps {
  predictionData?: any;
}

export function PlayerPropsPanel({ predictionData }: PlayerPropsPanelProps) {
  const [propsData, setPropsData] = useState<PlayerPropsData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProp, setSelectedProp] = useState<PlayerProp | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTeamLogo, setSelectedTeamLogo] = useState<string>('');
  const [selectedTeamColor, setSelectedTeamColor] = useState<string>('#3B82F6');

  useEffect(() => {
    const fetchPlayerProps = async () => {
      // Get team names from team_selector object
      const homeTeamName = predictionData?.team_selector?.home_team?.name;
      const awayTeamName = predictionData?.team_selector?.away_team?.name;
      
      if (!homeTeamName || !awayTeamName) {
        console.log('PlayerProps: No team data found in predictionData');
        return;
      }

      setIsLoading(true);
      try {
        console.log(`PlayerProps: Fetching props for ${homeTeamName} vs ${awayTeamName}`);
        const response = await fetch(
          `${CONFIG.API.BASE_URL}/api/player-props/${encodeURIComponent(homeTeamName)}/${encodeURIComponent(awayTeamName)}`
        );

        if (!response.ok) throw new Error('Failed to fetch player props');

        const data = await response.json();
        console.log('PlayerProps: Received data:', data);
        setPropsData(data);
      } catch (error) {
        console.error('Error fetching player props:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlayerProps();
  }, [predictionData]);

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'improving':
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'declining':
        return <TrendingDown className="w-4 h-4 text-red-400" />;
      default:
        return <Minus className="w-4 h-4 text-gray-400" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 60) return 'text-green-400 bg-green-400/10';
    if (confidence >= 50) return 'text-yellow-400 bg-yellow-400/10';
    return 'text-red-400 bg-red-400/10';
  };

  const formatPropType = (type: string) => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
  };

  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Get team styling info for a player
  const getPlayerTeamStyle = (prop: PlayerProp) => {
    const homeTeam = predictionData?.team_selector?.home_team;
    const awayTeam = predictionData?.team_selector?.away_team;
    
    const isTeam1Player = propsData?.team1_props?.some(p => p.player_name === prop.player_name && p.position === prop.position);
    
    const team = isTeam1Player ? homeTeam : awayTeam;
    
    // Use alt_color if primary is blue/black
    let teamColor = '#3B82F6';
    if (team?.primary_color && isBlueOrBlack(team.primary_color)) {
      teamColor = team.alt_color || team.secondary_color || '#f97316';
    } else if (team?.primary_color) {
      teamColor = team.primary_color;
    } else if (team?.color) {
      teamColor = team.color;
    }
    
    return {
      logo: team?.logo || '',
      color: teamColor,
      name: team?.name || ''
    };
  };

  const openModal = (prop: PlayerProp) => {
    setSelectedProp(prop);
    
    // Determine which team the player belongs to by checking team1_props vs team2_props
    const homeTeam = predictionData?.team_selector?.home_team;
    const awayTeam = predictionData?.team_selector?.away_team;
    
    // Check if this prop is in team1_props or team2_props
    const isTeam1Player = propsData?.team1_props?.some(p => p.player_name === prop.player_name && p.position === prop.position);
    
    const team = isTeam1Player ? homeTeam : awayTeam;
    
    // Use alt_color if primary is blue/black (same logic as cards)
    let teamColor = '#3B82F6';
    if (team?.primary_color && isBlueOrBlack(team.primary_color)) {
      teamColor = team.alt_color || team.secondary_color || '#f97316';
    } else if (team?.primary_color) {
      teamColor = team.primary_color;
    } else if (team?.color) {
      teamColor = team.color;
    }
    
    setSelectedTeamLogo(team?.logo || '');
    setSelectedTeamColor(teamColor);
    setIsModalOpen(true);
  };

  const homeTeamName = predictionData?.team_selector?.home_team?.name;
  const awayTeamName = predictionData?.team_selector?.away_team?.name;

  if (!homeTeamName || !awayTeamName) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="glassmorphism rounded-2xl p-8">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
          <span className="ml-3 text-gray-300">Loading player props...</span>
        </div>
      </div>
    );
  }

  if (!propsData) return null;

  const allProps = [...propsData.team1_props, ...propsData.team2_props];
  const topProps = allProps
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, 8); // Show top 8 props

  return (
    <>
      <div className="glassmorphism rounded-2xl p-8 animate-fade-in">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Target className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Player Props</h2>
              <p className="text-sm text-gray-400">Top betting opportunities</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Total Props</div>
            <div className="text-2xl font-bold text-white">{propsData.total_props}</div>
          </div>
        </div>

        {/* Props Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {topProps.map((prop, index) => {
            const teamStyle = getPlayerTeamStyle(prop);
            return (
              <button
                key={index}
                onClick={() => openModal(prop)}
                className="relative overflow-hidden rounded-xl p-4 text-left transition-all hover:scale-105 border-2 backdrop-blur-sm group"
                style={{
                  borderColor: `${teamStyle.color}50`,
                  background: `linear-gradient(135deg, ${teamStyle.color}25 0%, ${teamStyle.color}10 50%, ${teamStyle.color}05 100%)`,
                  boxShadow: `0 0 20px ${teamStyle.color}15`
                }}
              >
                {/* Team Logo Background */}
                <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-10">
                  <ImageWithFallback 
                    src={teamStyle.logo}
                    alt={teamStyle.name}
                    className="w-16 h-16 object-contain"
                    style={{ filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.5))' }}
                  />
                </div>

                <div className="relative z-10">
                  {/* Player Header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <ImageWithFallback
                          src={teamStyle.logo}
                          alt={teamStyle.name}
                          className="w-6 h-6 object-contain flex-shrink-0"
                          style={{ filter: `drop-shadow(0 0 4px ${teamStyle.color}80)` }}
                        />
                        <div 
                          className="text-sm font-bold truncate font-orbitron"
                          style={{ 
                            color: teamStyle.color,
                            textShadow: `0 0 10px ${teamStyle.color}40`
                          }}
                        >
                          {prop.player_name}
                        </div>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <span 
                          className="text-xs px-2 py-0.5 rounded-full font-orbitron font-semibold"
                          style={{
                            backgroundColor: `${teamStyle.color}20`,
                            color: teamStyle.color,
                            border: `1px solid ${teamStyle.color}40`
                          }}
                        >
                          {prop.position}
                        </span>
                        {getTrendIcon(prop.trend_analysis.trend_direction)}
                      </div>
                    </div>
                    <div className={`text-xs px-2 py-1 rounded-lg font-semibold ${getConfidenceColor(prop.confidence)}`}>
                      {prop.confidence}%
                    </div>
                  </div>

                  {/* Prop Line */}
                  <div className="mb-3">
                    <div className="text-xs text-gray-400 mb-1 font-orbitron">
                      {formatPropType(prop.prop_type)}
                    </div>
                    <div className="flex items-baseline gap-2">
                      <span 
                        className="text-2xl font-bold font-orbitron"
                        style={{ 
                          color: teamStyle.color,
                          textShadow: `0 0 10px ${teamStyle.color}50`
                        }}
                      >
                        {prop.line}
                      </span>
                      <span className={`text-sm font-semibold font-orbitron ${prop.recommendation === 'over' ? 'text-green-400' : 'text-red-400'}`}>
                        {prop.recommendation.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  {/* Quick Stats */}
                  <div className="flex items-center gap-3 text-xs">
                    <div className="flex items-center gap-1">
                      <Activity className="w-3 h-3 text-gray-400" />
                      <span className="text-gray-400 font-orbitron">Avg:</span>
                      <span className="text-white font-medium font-orbitron">{prop.season_average.toFixed(1)}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Shield className="w-3 h-3 text-gray-400" />
                      <span className="text-white font-medium font-orbitron">{prop.defensive_matchup.category}</span>
                    </div>
                  </div>

                  {/* Hover Indicator */}
                  <div 
                    className="mt-3 pt-3 border-t opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ borderColor: `${teamStyle.color}30` }}
                  >
                    <span 
                      className="text-xs font-orbitron font-semibold"
                      style={{ color: teamStyle.color }}
                    >
                      Click for detailed analysis →
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* View All Link */}
        {propsData.total_props > 8 && (
          <div className="mt-6 text-center">
            <button 
              onClick={() => {
                // Show all props by updating the slice to show all
                const allPropsSection = document.getElementById('all-player-props');
                if (allPropsSection) {
                  allPropsSection.scrollIntoView({ behavior: 'smooth' });
                }
              }}
              className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
            >
              View all {propsData.total_props} props →
            </button>
          </div>
        )}
        
        {/* All Props Section - Hidden by default, shown when expanded */}
        <div id="all-player-props" className="mt-8 pt-8 border-t border-white/10">
          <h3 className="text-xl font-bold text-white mb-4 font-orbitron">All Player Props ({propsData.total_props})</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {allProps.map((prop, index) => {
              const teamStyle = getPlayerTeamStyle(prop);
              return (
                <button
                  key={index}
                  onClick={() => openModal(prop)}
                  className="relative overflow-hidden rounded-xl p-4 text-left transition-all hover:scale-105 border-2 backdrop-blur-sm group"
                  style={{
                    borderColor: `${teamStyle.color}50`,
                    background: `linear-gradient(135deg, ${teamStyle.color}25 0%, ${teamStyle.color}10 50%, ${teamStyle.color}05 100%)`,
                    boxShadow: `0 0 20px ${teamStyle.color}15`
                  }}
                >
                  {/* Team Logo Background */}
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-10">
                    <ImageWithFallback 
                      src={teamStyle.logo}
                      alt={teamStyle.name}
                      className="w-16 h-16 object-contain"
                      style={{ filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.5))' }}
                    />
                  </div>

                  <div className="relative z-10">
                    {/* Player Header */}
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <ImageWithFallback
                            src={teamStyle.logo}
                            alt={teamStyle.name}
                            className="w-6 h-6 object-contain flex-shrink-0"
                            style={{ filter: `drop-shadow(0 0 4px ${teamStyle.color}80)` }}
                          />
                          <div 
                            className="text-sm font-bold truncate font-orbitron"
                            style={{ 
                              color: teamStyle.color,
                              textShadow: `0 0 10px ${teamStyle.color}40`
                            }}
                          >
                            {prop.player_name}
                          </div>
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          <span 
                            className="text-xs px-2 py-0.5 rounded-full font-orbitron font-semibold"
                            style={{
                              backgroundColor: `${teamStyle.color}20`,
                              color: teamStyle.color,
                              border: `1px solid ${teamStyle.color}40`
                            }}
                          >
                            {prop.position}
                          </span>
                          {getTrendIcon(prop.trend_analysis.trend_direction)}
                        </div>
                      </div>
                      <div className={`text-xs px-2 py-1 rounded-lg font-semibold ${getConfidenceColor(prop.confidence)}`}>
                        {prop.confidence}%
                      </div>
                    </div>

                    {/* Prop Line */}
                    <div className="mb-3">
                      <div className="text-xs text-gray-400 mb-1 font-orbitron">
                        {formatPropType(prop.prop_type)}
                      </div>
                      <div className="flex items-baseline gap-2">
                        <span 
                          className="text-2xl font-bold font-orbitron"
                          style={{ 
                            color: teamStyle.color,
                            textShadow: `0 0 10px ${teamStyle.color}50`
                          }}
                        >
                          {prop.line}
                        </span>
                        <span className={`text-sm font-semibold font-orbitron ${prop.recommendation === 'over' ? 'text-green-400' : 'text-red-400'}`}>
                          {prop.recommendation.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    {/* Quick Stats */}
                    <div className="flex items-center gap-3 text-xs">
                      <div className="flex items-center gap-1">
                        <Activity className="w-3 h-3 text-gray-400" />
                        <span className="text-gray-400 font-orbitron">Avg:</span>
                        <span className="text-white font-medium font-orbitron">{prop.season_average.toFixed(1)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Shield className="w-3 h-3 text-gray-400" />
                        <span className="text-white font-medium font-orbitron">{prop.defensive_matchup.category}</span>
                      </div>
                    </div>

                    {/* Hover Indicator */}
                    <div 
                      className="mt-3 pt-3 border-t opacity-0 group-hover:opacity-100 transition-opacity"
                      style={{ borderColor: `${teamStyle.color}30` }}
                    >
                      <span 
                        className="text-xs font-orbitron font-semibold"
                        style={{ color: teamStyle.color }}
                      >
                        Click for detailed analysis →
                      </span>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Modal */}
      {selectedProp && (
        <PlayerPropsModal
          prop={selectedProp}
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          teamLogo={selectedTeamLogo}
          teamColor={selectedTeamColor}
        />
      )}
    </>
  );
}
