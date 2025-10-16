import { useState, useRef, useMemo, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { GlassCard } from './GlassCard';
import { Search, ChevronDown, ArrowLeftRight, X, Zap } from 'lucide-react';
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { useClickOutside } from "../../hooks/useClickOutside";
import { useAppStore } from "../../store";
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

// Debug: Log teams data on load
console.log('DEBUG: Teams loaded from fbs.json:', {
  count: teams.length,
  first3: teams.slice(0, 3).map(t => ({ id: t.id, school: t.school, logos: t.logos }))
});

// Modern Portal Modal Component
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
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-[9999]"
      onClick={(e) => {
        // Only close if clicking the backdrop, not the modal content
        if (e.target === e.currentTarget) {
          onClose?.();
        }
      }}
      style={{
        zIndex: 9999,
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0
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
}

export function TeamSelector({ onPrediction, isLoading, selectedTeams, onMatchupChange }: TeamSelectorProps) {
  const [awayTeam, setAwayTeam] = useState<Team>(teams[0]);
  const [homeTeam, setHomeTeam] = useState<Team>(teams[1]);
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
    const filtered = teams.filter(team => 
      team.school.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(awaySearch.toLowerCase())
    );
    console.log('DEBUG: Filtered away teams:', { 
      search: awaySearch, 
      count: filtered.length,
      first5: filtered.slice(0, 5).map(t => t.school)
    });
    return filtered;
  }, [awaySearch]);

  const filteredHomeTeams = useMemo(() => {
    const filtered = teams.filter(team => 
      team.school.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(homeSearch.toLowerCase())
    );
    console.log('DEBUG: Filtered home teams:', { 
      search: homeSearch, 
      count: filtered.length,
      first5: filtered.slice(0, 5).map(t => t.school)
    });
    return filtered;
  }, [homeSearch]);

  const handleAwayTeamSelect = (team: Team) => {
    console.log('Away team selected:', team.school);
    setAwayTeam(team);
    setShowAwayDropdown(false);
    setAwaySearch('');
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(team, homeTeam);
  };

  const handleHomeTeamSelect = (team: Team) => {
    console.log('Home team selected:', team.school);
    setHomeTeam(team);
    setShowHomeDropdown(false);
    setHomeSearch('');
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(awayTeam, team);
  };

  const handleSwapTeams = () => {
    console.log('Swapping teams');
    const temp = awayTeam;
    setAwayTeam(homeTeam);
    setHomeTeam(temp);
    
    // Don't auto-trigger prediction, wait for button click
    
    onMatchupChange?.(homeTeam, temp);
  };

  // Week 8 Key Games Quick Select - All Top Ranked Matchups
  const week8Games = [
    // Ranked vs Ranked Games (Top Priority)
    { away: 'Ole Miss', home: 'Georgia', label: '#5 Ole Miss @ #9 Georgia' },
    { away: 'Tennessee', home: 'Alabama', label: '#11 Tenn @ #6 Bama' },
    { away: 'LSU', home: 'Vanderbilt', label: '#10 LSU @ #17 Vandy' },
    { away: 'USC', home: 'Notre Dame', label: '#20 USC @ #13 Notre Dame' },
    { away: 'Utah', home: 'BYU', label: '#23 Utah @ #15 BYU' },
    
    // Other Top Ranked Games  
    { away: 'Ohio State', home: 'Wisconsin', label: '#1 OSU @ Wisconsin' },
    { away: 'Louisville', home: 'Miami', label: 'Louisville @ #2 Miami' },
    { away: 'Michigan State', home: 'Indiana', label: 'MSU @ #3 Indiana' },
    { away: 'Texas A&M', home: 'Arkansas', label: '#4 A&M @ Arkansas' },
    { away: 'Texas Tech', home: 'Arizona State', label: '#7 TTU @ ASU' },
    { away: 'Oregon', home: 'Rutgers', label: '#8 Oregon @ Rutgers' },
    { away: 'Georgia Tech', home: 'Duke', label: '#12 GT @ Duke' }
  ];

  const handleQuickGameSelect = (game: { away: string; home: string; label: string }) => {
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
    
    console.log('Quick game select DEBUG:', {
      away: game.away,
      awayMatch: awayTeamMatch?.school,
      awayMatchId: awayTeamMatch?.id,
      home: game.home,
      homeMatch: homeTeamMatch?.school,
      homeMatchId: homeTeamMatch?.id,
      expectedTennesseeId: 2633,
      expectedAlabamaId: 333
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

  return (
    <GlassCard className="p-6">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-white font-semibold text-xl">Select Matchup</h2>
          <div className="text-gray-400 text-sm">Choose teams to analyze</div>
        </div>

        {/* Week 8 Quick Games */}
        <div className="space-y-3">
          <h4 className="text-gray-300 font-medium flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            Week 8 Key Games - Quick Select
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {week8Games.map((game, idx) => {
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
                  
                  {/* Shimmer effect on hover */}
                  <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          {/* Away Team Selector */}
          <div className="relative" ref={awayDropdownRef}>
            <label className="text-gray-400 text-xs mb-2 block">Away Team</label>
            <button
              onClick={() => {
                setShowAwayDropdown(!showAwayDropdown);
                setShowHomeDropdown(false);
              }}
              className="w-full flex items-center justify-between p-4 bg-gray-800/40 border border-gray-400/15 hover:border-gray-400/25 rounded-xl transition-all duration-300 group"
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
                className="bg-gray-900/90 backdrop-blur-xl border border-gray-400/15 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="p-6 border-b border-gray-400/15">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-semibold text-xl">Select Away Team</h3>
                    <button 
                      onClick={() => setShowAwayDropdown(false)}
                      className="p-2 hover:bg-gray-800/50 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5 text-gray-400 hover:text-white" />
                    </button>
                  </div>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      placeholder="Search teams..."
                      value={awaySearch}
                      onChange={(e) => setAwaySearch(e.target.value)}
                      className="w-full bg-gray-800/40 border border-gray-400/15 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300/25 focus:border-gray-300/35"
                      autoFocus
                    />
                  </div>
                </div>
                <div className="p-6 max-h-[65vh] overflow-y-auto">
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {filteredAwayTeams.map((team) => (
                      <button
                        key={team.id}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          console.log('DEBUG: Away team button clicked:', team.school);
                          handleAwayTeamSelect(team);
                        }}
                        className="flex flex-col items-center gap-2 p-4 bg-gray-800/40 hover:bg-gray-700/60 transition-colors rounded-lg border border-gray-400/15 hover:border-gray-400/25"
                      >
                        <ImageWithFallback
                          src={team.logos[1] || team.logos[0]}
                          alt={team.school}
                          className="w-12 h-12 object-contain"
                        />
                        <div className="text-center">
                          <div className="text-white text-sm font-medium">{team.school}</div>
                          <div className="text-gray-400 text-xs">{team.conference}</div>
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
              className="flex items-center justify-center w-12 h-12 rounded-full bg-gray-800/40 border border-gray-400/15 hover:border-cyan-500/40 hover:bg-cyan-500/10 transition-all duration-300 group"
              title="Swap teams"
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
              className="w-full flex items-center justify-between p-4 bg-gray-800/40 border border-gray-400/15 hover:border-gray-400/25 rounded-xl transition-all duration-300 group"
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
                className="bg-gray-900/90 backdrop-blur-xl border border-gray-400/15 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="p-6 border-b border-gray-400/15">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-semibold text-xl">Select Home Team</h3>
                    <button 
                      onClick={() => setShowHomeDropdown(false)}
                      className="p-2 hover:bg-gray-800/50 rounded-lg transition-colors"
                    >
                      <X className="w-5 h-5 text-gray-400 hover:text-white" />
                    </button>
                  </div>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      placeholder="Search teams..."
                      value={homeSearch}
                      onChange={(e) => setHomeSearch(e.target.value)}
                      className="w-full bg-gray-800/40 border border-gray-400/15 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300/25 focus:border-gray-300/35"
                      autoFocus
                    />
                  </div>
                </div>
                <div className="p-6 max-h-[65vh] overflow-y-auto">
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {filteredHomeTeams.map((team) => (
                      <button
                        key={team.id}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          console.log('DEBUG: Home team button clicked:', team.school);
                          handleHomeTeamSelect(team);
                        }}
                        className="flex flex-col items-center gap-2 p-4 bg-gray-800/40 hover:bg-gray-700/60 transition-colors rounded-lg border border-gray-400/15 hover:border-gray-400/25"
                      >
                        <ImageWithFallback
                          src={team.logos[1] || team.logos[0]}
                          alt={team.school}
                          className="w-12 h-12 object-contain"
                        />
                        <div className="text-center">
                          <div className="text-white text-sm font-medium">{team.school}</div>
                          <div className="text-gray-400 text-xs">{team.conference}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </PortalModal>
          </div>
        </div>

        {/* Prediction Button */}
        {awayTeam && homeTeam && !predictionLoading && (
          <div className="text-center py-6">
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