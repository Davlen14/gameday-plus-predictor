import { useState, useRef, useMemo, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { GlassCard } from './GlassCard';
import { Search, ChevronDown, ArrowLeftRight, X, Zap, Brain } from 'lucide-react';
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { useClickOutside } from "../../hooks/useClickOutside";
import { useAppStore } from "../../store";
import { usePostseasonGames } from '../../hooks/usePostseasonGames';
import fbsData from "../../fbs.json";

interface Team {
  id: number;
  school: string;
  mascot: string;
  abbreviation: string;
  conference: string;
  primary_color: string;
  alt_color: string;
  logos: string[];
}

// Transform FBS data to our team format
const teams: Team[] = fbsData;

// Modern Portal Modal Component - Matches Glossary styling
const PortalModal = ({ 
  children, 
  isOpen, 
  onClose 
}: { 
  children: React.ReactNode; 
  isOpen: boolean;
  onClose?: () => void;
}) => {
  if (!isOpen) return null;
  
  return createPortal(
    <div 
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-2 sm:p-4"
      onClick={(e) => {
        // Only close if clicking the backdrop, not the modal content
        if (e.target === e.currentTarget) {
          onClose?.();
        }
      }}
      style={{
        zIndex: 999999,
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        width: '100vw',
        height: '100vh'
      }}
    >
      {children}
    </div>,
    document.body
  );
};

interface TeamSelectorProps {
  onPrediction: (homeTeam: string, awayTeam: string) => void;
  isLoading?: boolean;
  selectedTeams?: { home: string; away: string } | null;
  onMatchupChange?: (awayTeam: Team, homeTeam: Team) => void;
  onQuickInsight?: () => void;
}

export function TeamSelector({ onPrediction, isLoading, selectedTeams, onMatchupChange, onQuickInsight }: TeamSelectorProps) {
  // Fetch postseason games from database
  const { games: postseasonGames, isLoading: gamesLoading, error: gamesError } = usePostseasonGames();
  
  // Default to CFP Quarterfinal: Miami @ Ohio State (Cotton Bowl - Neutral Site)
  const defaultAwayTeam = teams.find(t => t.school === 'Miami') || teams[0];
  const defaultHomeTeam = teams.find(t => t.school === 'Ohio State') || teams[1];
  
  const [awayTeam, setAwayTeam] = useState<Team>(defaultAwayTeam);
  const [homeTeam, setHomeTeam] = useState<Team>(defaultHomeTeam);
  const [showAwayDropdown, setShowAwayDropdown] = useState(false);
  const [showHomeDropdown, setShowHomeDropdown] = useState(false);
  const [awaySearch, setAwaySearch] = useState('');
  const [homeSearch, setHomeSearch] = useState('');

  // Use the loading state from props instead of store
  const predictionLoading = isLoading || false;

  const awayDropdownRef = useRef<HTMLDivElement>(null);
  const homeDropdownRef = useRef<HTMLDivElement>(null);

  // Custom click outside handlers that ignore Portal modal clicks
  useEffect(() => {
    const handleAwayClickOutside = (event: MouseEvent) => {
      const target = event.target as Element;
      const awayEl = awayDropdownRef?.current;
      
      // Don't close if clicking inside the dropdown ref or inside a Portal modal
      if (!awayEl || awayEl.contains(target) || target.closest('[data-portal-modal]')) {
        return;
      }
      
      if (showAwayDropdown) {
        setShowAwayDropdown(false);
        setAwaySearch('');
      }
    };

    if (showAwayDropdown) {
      document.addEventListener('mousedown', handleAwayClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleAwayClickOutside);
    };
  }, [showAwayDropdown]);

  useEffect(() => {
    const handleHomeClickOutside = (event: MouseEvent) => {
      const target = event.target as Element;
      const homeEl = homeDropdownRef?.current;
      
      // Don't close if clicking inside the dropdown ref or inside a Portal modal
      if (!homeEl || homeEl.contains(target) || target.closest('[data-portal-modal]')) {
        return;
      }
      
      if (showHomeDropdown) {
        setShowHomeDropdown(false);
        setHomeSearch('');
      }
    };

    if (showHomeDropdown) {
      document.addEventListener('mousedown', handleHomeClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleHomeClickOutside);
    };
  }, [showHomeDropdown]);

  const filteredAwayTeams = useMemo(() => {
    return teams.filter(team => 
      team.school.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(awaySearch.toLowerCase())
    );
  }, [awaySearch]);

  const filteredHomeTeams = useMemo(() => {
    return teams.filter(team => 
      team.school.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(homeSearch.toLowerCase())
    );
  }, [homeSearch]);

  const handleAwayTeamSelect = (team: Team) => {

    setAwayTeam(team);
    setShowAwayDropdown(false);
    setAwaySearch('');
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(team, homeTeam);
  };

  const handleHomeTeamSelect = (team: Team) => {

    setHomeTeam(team);
    setShowHomeDropdown(false);
    setHomeSearch('');
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(awayTeam, team);
  };

  const handleSwapTeams = () => {
    const temp = awayTeam;
    setAwayTeam(homeTeam);
    setHomeTeam(temp);
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(homeTeam, temp);
  };

  // Map postseason games from database to quick select format
  const week16Games = useMemo(() => {
    return postseasonGames.map(game => {
      // Check if it's a CFP quarterfinal game (week 1 postseason at major bowl venues)
      const isCFPQuarterfinal = game.seasonType === 'postseason' && 
        game.week === 1 && 
        (game.venue?.includes('Cotton Bowl') || 
         game.venue?.includes('Rose Bowl') || 
         game.venue?.includes('Sugar Bowl') || 
         game.venue?.includes('Orange Bowl'));
      
      return {
        away: game.away.team,
        home: game.home.team,
        label: isCFPQuarterfinal 
          ? `CFP: ${game.away.team} @ ${game.home.team}` 
          : `${game.away.team} @ ${game.home.team}${game.venue ? ` - ${game.venue}` : ''}`,
        spread: game.betting.spread,
        overUnder: game.betting.overUnder,
        homeMoneyline: game.betting.homeMoneyline,
        awayMoneyline: game.betting.awayMoneyline
      };
    });
  }, [postseasonGames]);

  const handleQuickGameSelect = (game: { 
    away: string; 
    home: string; 
    label: string;
    spread?: number | null;
    overUnder?: number | null;
    homeMoneyline?: number | null;
    awayMoneyline?: number | null;
  }) => {
    // More precise matching - exact school name matching with priority for exact matches
    const awayTeamMatch = teams.find(t => {
      const schoolName = t.school.toLowerCase();
      const searchName = game.away.toLowerCase();
      // Exact match first
      return schoolName === searchName;
    }) || teams.find(t => {
      const schoolName = t.school.toLowerCase();
      const searchName = game.away.toLowerCase();
      // Then partial matches with special cases
      return searchName.includes(schoolName) ||
             (searchName.includes('ole miss') && schoolName.includes('ole miss')) ||
             (searchName === 'utah' && schoolName === 'utah') || // Exact Utah, not Utah State
             (searchName === 'usc' && schoolName === 'usc') ||
             (searchName === 'notre dame' && schoolName === 'notre dame') ||
             (searchName === 'byu' && schoolName === 'byu');
    });
    
    const homeTeamMatch = teams.find(t => {
      const schoolName = t.school.toLowerCase();
      const searchName = game.home.toLowerCase();
      // Exact match first
      return schoolName === searchName;
    }) || teams.find(t => {
      const schoolName = t.school.toLowerCase();
      const searchName = game.home.toLowerCase();
      // Then partial matches with special cases
      return searchName.includes(schoolName) ||
             (searchName.includes('vanderbilt') && schoolName.includes('vanderbilt')) ||
             (searchName === 'utah' && schoolName === 'utah') || // Exact Utah, not Utah State
             (searchName === 'usc' && schoolName === 'usc') ||
             (searchName === 'notre dame' && schoolName === 'notre dame') ||
             (searchName === 'byu' && schoolName === 'byu');
    });
    
    if (awayTeamMatch && homeTeamMatch) {
      setAwayTeam(awayTeamMatch);
      setHomeTeam(homeTeamMatch);
      onMatchupChange?.(awayTeamMatch, homeTeamMatch);
    } else {
      console.warn('Could not find team match:', {
        away: game.away,
        awayFound: !!awayTeamMatch,
        home: game.home,
        homeFound: !!homeTeamMatch
      });
    }
  };

  // Separate CFP games from other bowl games
  const cfpGames = useMemo(() => {
    return week16Games.filter(game => 
      game.label.toLowerCase().includes('cfp') || 
      game.label.toLowerCase().includes('playoff')
    );
  }, [week16Games]);

  const bowlGames = useMemo(() => {
    return week16Games.filter(game => 
      !game.label.toLowerCase().includes('cfp') && 
      !game.label.toLowerCase().includes('playoff')
    );
  }, [week16Games]);

  return (
    <GlassCard className="p-6">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-white font-semibold text-xl">Select Matchup</h2>
          <div className="text-gray-400 text-sm">Choose teams to analyze</div>
        </div>

        {/* CFP Premier Games Section */}
        {cfpGames.length > 0 && (
          <div className="mb-2">
            <div className="flex items-center gap-2 mb-3">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30">
                <span className="text-xl">🏆</span>
                <h3 className="text-white font-bold text-sm uppercase tracking-wider">College Football Playoff</h3>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {cfpGames.map((game, idx) => {
                const awayTeamData = teams.find(t => {
                  const schoolName = t.school.toLowerCase();
                  const searchName = game.away.toLowerCase();
                  return schoolName === searchName;
                }) || teams.find(t => {
                  const schoolName = t.school.toLowerCase();
                  const searchName = game.away.toLowerCase();
                  return searchName.includes(schoolName);
                });
                
                const homeTeamData = teams.find(t => {
                  const schoolName = t.school.toLowerCase();
                  const searchName = game.home.toLowerCase();
                  return schoolName === searchName;
                }) || teams.find(t => {
                  const schoolName = t.school.toLowerCase();
                  const searchName = game.home.toLowerCase();
                  return searchName.includes(schoolName);
                });
                
                return (
                  <button
                    key={`cfp-${idx}`}
                    onClick={() => handleQuickGameSelect(game)}
                    disabled={predictionLoading}
                    className="group relative px-4 py-4 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden transform hover:scale-110 hover:shadow-2xl"
                    style={{
                      background: `linear-gradient(135deg, 
                        ${awayTeamData?.primary_color || '#1e293b'}35 0%, 
                        rgba(15, 23, 42, 0.9) 50%,
                        ${homeTeamData?.primary_color || '#1e293b'}35 100%)`,
                      border: `2px solid ${awayTeamData?.primary_color || '#f59e0b'}50`,
                      boxShadow: `0 8px 32px ${awayTeamData?.primary_color || '#f59e0b'}25`
                    }}
                  >
                    {/* Championship glow effect */}
                    <div 
                      className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-xl"
                      style={{
                        background: `linear-gradient(135deg, 
                          ${awayTeamData?.primary_color || '#fbbf24'}80, 
                          ${homeTeamData?.primary_color || '#f59e0b'}80)`,
                        filter: 'blur(20px)',
                        transform: 'scale(1.1)',
                        zIndex: -1
                      }}
                    ></div>
                    
                    {/* Team Logos with enhanced styling */}
                    <div className="flex items-center justify-center gap-2 mb-2 relative z-10">
                      {awayTeamData && (
                        <div className="relative">
                          <div 
                            className="absolute inset-0 rounded-full opacity-40 group-hover:opacity-70 transition-opacity"
                            style={{ 
                              backgroundColor: awayTeamData.primary_color || '#f59e0b',
                              filter: 'blur(12px)',
                              transform: 'scale(1.3)'
                            }}
                          ></div>
                          <ImageWithFallback
                            src={awayTeamData.logos[1] || awayTeamData.logos[0]}
                            alt={awayTeamData.school}
                            className="w-12 h-12 object-contain transform group-hover:scale-125 transition-all duration-300 relative z-10"
                            style={{
                              filter: 'drop-shadow(0 3px 16px rgba(0,0,0,0.6)) drop-shadow(0 0 12px rgba(255,215,0,0.4))'
                            }}
                          />
                        </div>
                      )}
                      <span className="text-yellow-400 text-sm font-bold px-1">@</span>
                      {homeTeamData && (
                        <div className="relative">
                          <div 
                            className="absolute inset-0 rounded-full opacity-40 group-hover:opacity-70 transition-opacity"
                            style={{ 
                              backgroundColor: homeTeamData.primary_color || '#f59e0b',
                              filter: 'blur(12px)',
                              transform: 'scale(1.3)'
                            }}
                          ></div>
                          <ImageWithFallback
                            src={homeTeamData.logos[1] || homeTeamData.logos[0]}
                            alt={homeTeamData.school}
                            className="w-12 h-12 object-contain transform group-hover:scale-125 transition-all duration-300 relative z-10"
                            style={{
                              filter: 'drop-shadow(0 3px 16px rgba(0,0,0,0.6)) drop-shadow(0 0 12px rgba(255,215,0,0.4))'
                            }}
                          />
                        </div>
                      )}
                    </div>
                    
                    {/* Label with CFP styling */}
                    <div 
                      className="text-xs font-bold leading-tight text-center group-hover:text-yellow-300 transition-all duration-300 relative z-10"
                      style={{
                        color: '#fde047',
                        textShadow: '0 2px 4px rgba(0,0,0,0.9)'
                      }}
                    >
                      {game.label}
                    </div>
                    
                    {/* Betting Lines */}
                    {(game.spread !== undefined || game.overUnder) && (
                      <div className="mt-2 text-[10px] text-gray-200/90 text-center relative z-10 space-y-0.5">
                        {game.spread !== null && game.spread !== undefined && (
                          <div className="flex items-center justify-center gap-1">
                            <span className="font-semibold">{game.spread > 0 ? `${game.away} -${Math.abs(game.spread)}` : `${game.home} -${Math.abs(game.spread)}`}</span>
                          </div>
                        )}
                        {game.overUnder && (
                          <div className="flex items-center justify-center gap-1">
                            <span className="font-semibold">O/U {game.overUnder}</span>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* Golden shimmer effect on hover */}
                    <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-yellow-400/30 to-transparent"></div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Bowl Games Quick Select */}
        {bowlGames.length > 0 && (
          <div className="mb-2">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-5 h-5 text-blue-400" />
              <h3 className="text-white font-semibold text-sm">Bowl Games</h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 max-h-64 overflow-y-auto">
              {bowlGames.map((game, idx) => {
              const awayTeamData = teams.find(t => {
                const schoolName = t.school.toLowerCase();
                const searchName = game.away.toLowerCase();
                // Exact match first
                return schoolName === searchName;
              }) || teams.find(t => {
                const schoolName = t.school.toLowerCase();
                const searchName = game.away.toLowerCase();
                // Then partial matches with special cases
                return searchName.includes(schoolName) ||
                       (searchName.includes('ole miss') && schoolName.includes('ole miss')) ||
                       (searchName === 'utah' && schoolName === 'utah') || // Exact Utah, not Utah State
                       (searchName === 'usc' && schoolName === 'usc') ||
                       (searchName === 'notre dame' && schoolName === 'notre dame') ||
                       (searchName === 'byu' && schoolName === 'byu');
              });
              
              const homeTeamData = teams.find(t => {
                const schoolName = t.school.toLowerCase();
                const searchName = game.home.toLowerCase();
                // Exact match first
                return schoolName === searchName;
              }) || teams.find(t => {
                const schoolName = t.school.toLowerCase();
                const searchName = game.home.toLowerCase();
                // Then partial matches with special cases
                return searchName.includes(schoolName) ||
                       (searchName.includes('vanderbilt') && schoolName.includes('vanderbilt')) ||
                       (searchName === 'utah' && schoolName === 'utah') || // Exact Utah, not Utah State
                       (searchName === 'usc' && schoolName === 'usc') ||
                       (searchName === 'notre dame' && schoolName === 'notre dame') ||
                       (searchName === 'byu' && schoolName === 'byu');
              });
              
              return (
                <button
                  key={idx}
                  onClick={() => handleQuickGameSelect(game)}
                  disabled={predictionLoading}
                  className="group relative px-3 py-3 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden transform hover:scale-105 hover:shadow-xl"
                  style={{
                    background: `linear-gradient(135deg, 
                      ${awayTeamData?.primary_color || '#1e293b'}25 0%, 
                      rgba(15, 23, 42, 0.8) 50%,
                      ${homeTeamData?.primary_color || '#1e293b'}25 100%)`,
                    border: `1px solid ${awayTeamData?.primary_color || '#475569'}40`,
                    boxShadow: `0 4px 20px ${awayTeamData?.primary_color || '#000000'}15`
                  }}
                >
                  {/* Animated gradient border on hover */}
                  <div 
                    className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-lg"
                    style={{
                      background: `linear-gradient(135deg, 
                        ${awayTeamData?.primary_color || '#60a5fa'}60, 
                        ${homeTeamData?.primary_color || '#a78bfa'}60)`,
                      filter: 'blur(15px)',
                      transform: 'scale(1.05)',
                      zIndex: -1
                    }}
                  ></div>
                  
                  {/* Team Logos */}
                  <div className="flex items-center justify-center gap-2 mb-2 relative z-10">
                    {awayTeamData && (
                      <div className="relative">
                        <div 
                          className="absolute inset-0 rounded-full opacity-30 group-hover:opacity-50 transition-opacity"
                          style={{ 
                            backgroundColor: awayTeamData.primary_color || '#475569',
                            filter: 'blur(8px)',
                            transform: 'scale(1.2)'
                          }}
                        ></div>
                        <ImageWithFallback
                          src={awayTeamData.logos[1] || awayTeamData.logos[0]}
                          alt={awayTeamData.school}
                          className="w-9 h-9 object-contain transform group-hover:scale-125 transition-all duration-300 relative z-10"
                          style={{
                            filter: 'drop-shadow(0 2px 12px rgba(0,0,0,0.5)) drop-shadow(0 0 8px rgba(255,255,255,0.3))'
                          }}
                        />
                      </div>
                    )}
                    <span className="text-gray-300 text-xs font-bold px-1">@</span>
                    {homeTeamData && (
                      <div className="relative">
                        <div 
                          className="absolute inset-0 rounded-full opacity-30 group-hover:opacity-50 transition-opacity"
                          style={{ 
                            backgroundColor: homeTeamData.primary_color || '#475569',
                            filter: 'blur(8px)',
                            transform: 'scale(1.2)'
                          }}
                        ></div>
                        <ImageWithFallback
                          src={homeTeamData.logos[1] || homeTeamData.logos[0]}
                          alt={homeTeamData.school}
                          className="w-9 h-9 object-contain transform group-hover:scale-125 transition-all duration-300 relative z-10"
                          style={{
                            filter: 'drop-shadow(0 2px 12px rgba(0,0,0,0.5)) drop-shadow(0 0 8px rgba(255,255,255,0.3))'
                          }}
                        />
                      </div>
                    )}
                  </div>
                  
                  {/* Label with enhanced styling */}
                  <div 
                    className="text-[10px] font-semibold leading-tight text-center group-hover:text-white transition-all duration-300 relative z-10"
                    style={{
                      color: '#e2e8f0',
                      textShadow: '0 1px 3px rgba(0,0,0,0.8)'
                    }}
                  >
                    {game.label}
                  </div>
                  
                  {/* Betting Lines */}
                  {(game.spread !== undefined || game.overUnder) && (
                    <div className="mt-1 text-[9px] text-gray-300/80 text-center relative z-10 space-y-0.5">
                      {game.spread !== null && game.spread !== undefined && (
                        <div className="flex items-center justify-center gap-1">
                          <span>{game.spread > 0 ? `${game.away} -${Math.abs(game.spread)}` : `${game.home} -${Math.abs(game.spread)}`}</span>
                        </div>
                      )}
                      {game.overUnder && (
                        <div className="flex items-center justify-center gap-1">
                          <span>O/U {game.overUnder}</span>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Shimmer effect on hover */}
                  <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                </button>
              );
            })}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          {/* Away Team Selector */}
          <div className="relative" ref={awayDropdownRef}>
            <label className="text-gray-400 text-xs mb-2 block">Away Team</label>
            <button
              onClick={() => {
                setShowAwayDropdown(!showAwayDropdown);
                setShowHomeDropdown(false);
              }}
              className="w-full flex items-center justify-between p-4 backdrop-blur-sm border border-gray-400/20 hover:border-gray-400/30 rounded-xl transition-all duration-300 group"
              style={{ backdropFilter: 'none' }}
            >
              <div className="flex items-center gap-3">
                <ImageWithFallback
                  src={awayTeam.logos[1] || awayTeam.logos[0]}
                  alt={awayTeam.school}
                  className="w-8 h-8 object-contain"
                />
                <div className="text-left">
                  <div className="text-white font-medium">{awayTeam.school}</div>
                  <div className="text-gray-400 text-sm">{awayTeam.conference}</div>
                </div>
              </div>
              <ChevronDown className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
            </button>

            {/* Modern Portal Modal for Away Team */}
            <PortalModal isOpen={showAwayDropdown} onClose={() => setShowAwayDropdown(false)}>
              <div 
                data-portal-modal="true"
                className="backdrop-blur-2xl border-2 border-white/20 rounded-lg shadow-2xl w-full max-w-[95vw] sm:max-w-4xl h-[90vh] sm:h-[85vh] flex flex-col animate-in fade-in zoom-in-95 duration-200"
                onClick={(e) => e.stopPropagation()}
                style={{ 
                  boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)', 
                  zIndex: 1000000,
                  position: 'relative',
                  maxWidth: '1400px',
                  maxHeight: '900px'
                }}
              >
                <div className="p-4 sm:p-6 border-b border-white/10 flex-shrink-0">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <h3 className="text-white font-semibold text-xl sm:text-2xl">Select Away Team</h3>
                    <button 
                      onClick={() => setShowAwayDropdown(false)}
                      className="text-slate-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/10"
                    >
                      <X className="w-6 h-6" />
                    </button>
                  </div>
                  
                  {/* Postseason Games Quick Select Inside Dropdown */}
                  <div className="mb-4 p-4 rounded-lg backdrop-blur-sm border border-white/10" style={{
                    background: 'rgba(255, 255, 255, 0.02)'
                  }}>
                    <h4 className="text-white font-medium flex items-center gap-2 mb-3">
                      <Zap className="w-5 h-5 text-yellow-400" />
                      <span className="text-sm sm:text-base">2025 Postseason Bowl Games & CFP</span>
                    </h4>
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-2 max-h-48 sm:max-h-64 overflow-y-auto">
                      {week16Games.map((game, idx) => {
                        const awayTeamData = teams.find(t => t.school.toLowerCase() === game.away.toLowerCase()) || 
                          teams.find(t => t.school.toLowerCase().includes(game.away.toLowerCase()));
                        const homeTeamData = teams.find(t => t.school.toLowerCase() === game.home.toLowerCase()) || 
                          teams.find(t => t.school.toLowerCase().includes(game.home.toLowerCase()));
                        
                        return (
                          <button
                            key={idx}
                            onClick={() => {
                              handleQuickGameSelect(game);
                              setShowAwayDropdown(false);
                              setShowHomeDropdown(false);
                            }}
                            className="group relative p-2 rounded-lg backdrop-blur-sm transition-all duration-300 overflow-hidden hover:scale-105 hover:shadow-lg border border-white/10 hover:border-white/20"
                            style={{
                              background: `linear-gradient(135deg, ${awayTeamData?.primary_color || '#1e293b'}15, ${homeTeamData?.primary_color || '#1e293b'}15)`
                            }}
                          >
                            <div className="flex items-center justify-center gap-1.5 mb-1.5">
                              {awayTeamData && (
                                <ImageWithFallback
                                  src={awayTeamData.logos[1] || awayTeamData.logos[0]}
                                  alt={awayTeamData.school}
                                  className="w-6 h-6 object-contain"
                                />
                              )}
                              <span className="text-gray-400 text-[10px]">@</span>
                              {homeTeamData && (
                                <ImageWithFallback
                                  src={homeTeamData.logos[1] || homeTeamData.logos[0]}
                                  alt={homeTeamData.school}
                                  className="w-6 h-6 object-contain"
                                />
                              )}
                            </div>
                            <div className="text-[9px] text-gray-300 text-center leading-tight">
                              {game.away} @ {game.home}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                  
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Search teams..."
                      value={awaySearch}
                      onChange={(e) => setAwaySearch(e.target.value)}
                      className="w-full backdrop-blur-sm border border-white/10 rounded-lg pl-12 pr-4 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/40 focus:border-cyan-500/40 text-lg"
                      autoFocus
                    />
                  </div>
                </div>
                <div className="flex-1 p-6 overflow-y-auto" style={{ 
                  zIndex: 1000001,
                  position: 'relative'
                }}>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 pb-4" style={{ 
                    zIndex: 1000002,
                    position: 'relative'
                  }}>
                    {filteredAwayTeams.map((team) => (
                      <button
                        key={team.id}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          handleAwayTeamSelect(team);
                        }}
                        className="flex flex-col items-center gap-2 p-4 sm:p-5 backdrop-blur-sm hover:bg-white/10 transition-all duration-300 rounded-lg border border-white/10 hover:border-white/25 shadow-lg hover:shadow-xl hover:scale-105 group"
                      >
                        <ImageWithFallback
                          src={team.logos[1] || team.logos[0]}
                          alt={team.school}
                          className="w-12 h-12 sm:w-14 sm:h-14 object-contain group-hover:scale-110 transition-transform"
                        />
                        <div className="text-center">
                          <div className="text-white text-sm sm:text-base font-semibold">{team.school}</div>
                          <div className="text-slate-400 text-xs sm:text-sm">{team.conference}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </PortalModal>
          </div>

          {/* Swap Button */}
          <div className="flex justify-center">
            <button
              onClick={handleSwapTeams}
              className="flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-sm border border-gray-400/20 hover:border-cyan-500/40 hover:bg-cyan-500/10 transition-all duration-300 group"
              title="Swap teams"
              style={{ backdropFilter: 'none' }}
            >
              <ArrowLeftRight className="w-5 h-5 text-gray-400 group-hover:text-cyan-400 transition-colors" />
            </button>
          </div>

          {/* Home Team Selector */}
          <div className="relative" ref={homeDropdownRef}>
            <label className="text-gray-400 text-xs mb-2 block">Home Team</label>
            <button
              onClick={() => {
                setShowHomeDropdown(!showHomeDropdown);
                setShowAwayDropdown(false);
              }}
              className="w-full flex items-center justify-between p-4 backdrop-blur-sm border border-gray-400/20 hover:border-gray-400/30 rounded-xl transition-all duration-300 group"
              style={{ backdropFilter: 'none' }}
            >
              <div className="flex items-center gap-3">
                <ImageWithFallback
                  src={homeTeam.logos[1] || homeTeam.logos[0]}
                  alt={homeTeam.school}
                  className="w-8 h-8 object-contain"
                />
                <div className="text-left">
                  <div className="text-white font-medium">{homeTeam.school}</div>
                  <div className="text-gray-400 text-sm">{homeTeam.conference}</div>
                </div>
              </div>
              <ChevronDown className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
            </button>

            {/* Modern Portal Modal for Home Team */}
            <PortalModal isOpen={showHomeDropdown} onClose={() => setShowHomeDropdown(false)}>
              <div 
                data-portal-modal="true"
                className="backdrop-blur-2xl border-2 border-white/20 rounded-lg shadow-2xl w-full max-w-[95vw] sm:max-w-4xl h-[90vh] sm:h-[85vh] flex flex-col animate-in fade-in zoom-in-95 duration-200"
                onClick={(e) => e.stopPropagation()}
                style={{ 
                  boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)', 
                  zIndex: 1000000,
                  position: 'relative',
                  maxWidth: '1400px',
                  maxHeight: '900px'
                }}
              >
                <div className="p-4 sm:p-6 border-b border-white/10 flex-shrink-0">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <h3 className="text-white font-semibold text-xl sm:text-2xl">Select Home Team</h3>
                    <button 
                      onClick={() => setShowHomeDropdown(false)}
                      className="text-slate-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/10"
                    >
                      <X className="w-6 h-6" />
                    </button>
                  </div>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Search teams..."
                      value={homeSearch}
                      onChange={(e) => setHomeSearch(e.target.value)}
                      className="w-full backdrop-blur-sm border border-white/10 rounded-lg pl-12 pr-4 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/40 focus:border-cyan-500/40 text-lg"
                      autoFocus
                    />
                  </div>
                </div>
                <div className="flex-1 p-6 overflow-y-auto" style={{ 
                  zIndex: 1000001,
                  position: 'relative'
                }}>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 pb-4" style={{ 
                    zIndex: 1000002,
                    position: 'relative'
                  }}>
                    {filteredHomeTeams.map((team) => (
                      <button
                        key={team.id}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          handleHomeTeamSelect(team);
                        }}
                        className="flex flex-col items-center gap-2 p-4 sm:p-5 backdrop-blur-sm hover:bg-white/10 transition-all duration-300 rounded-lg border border-white/10 hover:border-white/25 shadow-lg hover:shadow-xl hover:scale-105 group"
                      >
                        <ImageWithFallback
                          src={team.logos[1] || team.logos[0]}
                          alt={team.school}
                          className="w-12 h-12 sm:w-14 sm:h-14 object-contain group-hover:scale-110 transition-transform"
                        />
                        <div className="text-center">
                          <div className="text-white text-sm sm:text-base font-semibold">{team.school}</div>
                          <div className="text-slate-400 text-xs sm:text-sm">{team.conference}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </PortalModal>
          </div>
        </div>

        {/* Prediction Buttons */}
        {awayTeam && homeTeam && !predictionLoading && (
          <div className="text-center py-6 flex flex-col gap-4">
            {/* Main Prediction Button */}
            <button
              onClick={() => onPrediction(homeTeam.school, awayTeam.school)}
              className="group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] 
                         transform hover:scale-[1.05] transition-all duration-500 ease-out"
              style={{
                background: `linear-gradient(135deg, 
                  ${awayTeam.primary_color || '#1e293b'}40 0%, 
                  ${awayTeam.primary_color || '#1e293b'}20 25%,
                  #0f172a80 50%,
                  ${homeTeam.primary_color || '#1e293b'}20 75%, 
                  ${homeTeam.primary_color || '#1e293b'}40 100%)`,
                border: `2px solid transparent`,
                backgroundClip: 'padding-box'
              }}
            >
              {/* Animated gradient border effect */}
              <div 
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                style={{
                  background: `linear-gradient(135deg, 
                    ${awayTeam.primary_color || '#60a5fa'}60, 
                    ${homeTeam.primary_color || '#a78bfa'}60)`,
                  filter: 'blur(20px)',
                  transform: 'scale(1.1)'
                }}
              ></div>
              
              {/* Team logos background */}
              <div className="absolute inset-0 flex items-center justify-between px-8 opacity-10 group-hover:opacity-20 transition-opacity duration-500">
                <ImageWithFallback
                  src={awayTeam.logos[1] || awayTeam.logos[0]}
                  alt={awayTeam.school}
                  className="w-24 h-24 object-contain transform -rotate-12 group-hover:rotate-0 transition-transform duration-700"
                />
                <ImageWithFallback
                  src={homeTeam.logos[1] || homeTeam.logos[0]}
                  alt={homeTeam.school}
                  className="w-24 h-24 object-contain transform rotate-12 group-hover:rotate-0 transition-transform duration-700"
                />
              </div>

              {/* Shimmer effect */}
              <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
              
              {/* Button content */}
              <div className="relative px-12 py-5 flex flex-col items-center gap-2">
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-white tracking-wide">Generate Prediction</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-gray-300 font-medium">
                  <span>{awayTeam.school}</span>
                  <span className="text-gray-500">vs</span>
                  <span>{homeTeam.school}</span>
                </div>
              </div>

              {/* Bottom glow */}
              <div 
                className="absolute bottom-0 left-0 right-0 h-1 opacity-60 group-hover:opacity-100 transition-opacity duration-500"
                style={{
                  background: `linear-gradient(90deg, 
                    ${awayTeam.primary_color || '#60a5fa'} 0%, 
                    #ffffff 50%, 
                    ${homeTeam.primary_color || '#a78bfa'} 100%)`
                }}
              ></div>
            </button>

            {/* Quick Insight Button */}
            {onQuickInsight && (
              <button
                onClick={onQuickInsight}
                className="group relative overflow-hidden rounded-xl shadow-lg hover:shadow-xl 
                           transform hover:scale-[1.02] transition-all duration-300 ease-out"
                style={{
                  background: `linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.15))`,
                  border: `1px solid rgba(139, 92, 246, 0.3)`,
                }}
              >
                {/* Animated glow effect */}
                <div 
                  className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                  style={{
                    background: `radial-gradient(circle at center, rgba(139, 92, 246, 0.4), transparent)`,
                    filter: 'blur(15px)',
                  }}
                ></div>
                
                {/* Button content */}
                <div className="relative px-8 py-3 flex items-center justify-center gap-2">
                  <Brain 
                    className="w-5 h-5 text-purple-400 group-hover:text-purple-300 transition-colors duration-300" 
                    strokeWidth={2}
                  />
                  <span className="text-base font-semibold text-purple-100 group-hover:text-white transition-colors duration-300">
                    Insight
                  </span>
                </div>

                {/* Shimmer effect */}
                <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
              </button>
            )}
          </div>
        )}

        {/* Loading Indicator */}
        {predictionLoading && (
          <div className="text-center py-4">
            <div className="inline-flex items-center gap-2 text-gray-300">
              <div className="animate-spin w-4 h-4 border-2 border-gray-300 border-t-transparent rounded-full"></div>
              <span>Getting prediction...</span>
            </div>
          </div>
        )}
      </div>
    </GlassCard>
  );
}