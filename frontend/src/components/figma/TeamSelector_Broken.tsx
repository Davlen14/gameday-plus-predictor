import { useState, useRef, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { GlassCard } from './GlassCard';
import { Search, ChevronDown, ArrowLeftRight } from 'lucide-react';
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

// Portal Modal Component
const PortalModal = ({ children, isOpen }: { children: React.ReactNode; isOpen: boolean }) => {
  if (!isOpen) return null;
  
  return createPortal(
    children,
    document.body
  );
};

interface TeamSelectorProps {
  onMatchupChange?: (awayTeam: Team, homeTeam: Team) => void;
}

export function TeamSelector({ onMatchupChange }: TeamSelectorProps) {
  const [awayTeam, setAwayTeam] = useState<Team>(teams[0]);
  const [homeTeam, setHomeTeam] = useState<Team>(teams[1]);
  const [showAwayDropdown, setShowAwayDropdown] = useState(false);
  const [showHomeDropdown, setShowHomeDropdown] = useState(false);
  const [awaySearch, setAwaySearch] = useState('');
  const [homeSearch, setHomeSearch] = useState('');

  // Connect to your Flask API via Zustand store
  const { fetchPrediction, predictionLoading, setSelectedTeams } = useAppStore();

  const awayDropdownRef = useRef<HTMLDivElement>(null);
  const homeDropdownRef = useRef<HTMLDivElement>(null);

  useClickOutside(awayDropdownRef, () => {
    setShowAwayDropdown(false);
    setAwaySearch('');
  });

  useClickOutside(homeDropdownRef, () => {
    setShowHomeDropdown(false);
    setHomeSearch('');
  });

  const filteredAwayTeams = useMemo(() => 
    teams.filter(team => 
      team.school.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(awaySearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(awaySearch.toLowerCase())
    ), [awaySearch]
  );

  const filteredHomeTeams = useMemo(() => 
    teams.filter(team => 
      team.school.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.conference.toLowerCase().includes(homeSearch.toLowerCase()) ||
      team.mascot.toLowerCase().includes(homeSearch.toLowerCase())
    ), [homeSearch]
  );

  const handleAwayTeamSelect = (team: Team) => {
    console.log('Away team selected:', team.school);
    setAwayTeam(team);
    setShowAwayDropdown(false);
    setAwaySearch('');
    
    // Update store and trigger API call to your Flask backend
    setSelectedTeams(homeTeam, team);
    fetchPrediction(homeTeam.school, team.school);
    
    onMatchupChange?.(team, homeTeam);
  };

  const handleHomeTeamSelect = (team: Team) => {
    console.log('Home team selected:', team.school);
    setHomeTeam(team);
    setShowHomeDropdown(false);
    setHomeSearch('');
    
    // Update store and trigger API call to your Flask backend
    setSelectedTeams(team, awayTeam);
    fetchPrediction(team.school, awayTeam.school);
    
    onMatchupChange?.(awayTeam, team);
  };

  const handleSwapTeams = () => {
    console.log('Swapping teams');
    const temp = awayTeam;
    setAwayTeam(homeTeam);
    setHomeTeam(temp);
    
    // Update store and trigger API call to your Flask backend
    setSelectedTeams(temp, homeTeam);
    fetchPrediction(temp.school, homeTeam.school);
    
    onMatchupChange?.(homeTeam, temp);
  };

  return (
    <GlassCard className="p-6">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-white font-semibold text-xl">Select Matchup</h2>
          <div className="text-gray-400 text-sm">Choose teams to analyze</div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] gap-4 items-center">
          {/* Away Team Selector */}
          <div className="relative" ref={awayDropdownRef} style={{ zIndex: 1 }}>
            <label className="text-gray-400 text-xs mb-2 block">Away Team</label>
            <button
              onClick={() => setShowAwayDropdown(!showAwayDropdown)}
              className="w-full backdrop-blur-sm border border-gray-400/15 rounded-lg p-4 hover:border-gray-400/25 hover:bg-white/10 transition-all duration-300 group"
            >
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-white/10 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <ImageWithFallback
                    src={awayTeam.logos[1] || awayTeam.logos[0]}
                    alt={awayTeam.school}
                    className="relative w-12 h-12 object-contain"
                  />
                </div>
                <div className="flex-1 text-left">
                  <div className="flex items-center gap-2">
                    <span className="text-white font-semibold">{awayTeam.school}</span>
                  </div>
                  <span className="text-gray-400 text-sm">{awayTeam.conference}</span>
                </div>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showAwayDropdown ? 'rotate-180' : ''}`} />
              </div>
            </button>

            {/* Away Team Dropdown - Simple */}
            {showAwayDropdown && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-gray-900/95 backdrop-blur-xl border border-gray-400/15 rounded-2xl shadow-2xl max-h-96 overflow-hidden z-50">
                <div className="p-4 border-b border-gray-400/15">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      placeholder="Search teams..."
                      value={awaySearch}
                      onChange={(e) => setAwaySearch(e.target.value)}
                      className="w-full backdrop-blur-sm border border-gray-400/15 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300/25 focus:border-gray-300/35"
                      autoFocus
                    />
                  </div>
                </div>
                <div className="p-4 max-h-80 overflow-y-auto">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {filteredAwayTeams.map((team) => (
                      <button
                        key={team.id}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          console.log('Team button clicked:', team.school);
                          handleAwayTeamSelect(team);
                        }}
                        className="flex items-center gap-3 p-3 backdrop-blur-sm hover:bg-white/10 transition-colors rounded-lg border border-gray-400/15 hover:border-gray-400/25 cursor-pointer text-left"
                      >
                        <ImageWithFallback
                          src={team.logos[1] || team.logos[0]}
                          alt={team.school}
                          className="w-8 h-8 object-contain"
                        />
                        <div>
                          <div className="text-white text-sm font-medium">{team.school}</div>
                          <div className="text-gray-400 text-xs">{team.conference}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
                <div 
                  className="bg-gray-900/90 backdrop-blur-xl border border-gray-400/15 rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-visible animate-in fade-in slide-in-from-left-2 duration-200"
                  onClick={(e) => e.stopPropagation()}
                  style={{ 
                    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)', 
                    zIndex: 1000000,
                    position: 'relative'
                  }}
                >
                  <div className="p-6 border-b border-gray-400/15">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-white font-semibold text-xl">Select Away Team</h3>
                      <button 
                        onClick={() => setShowAwayDropdown(false)}
                        className="text-gray-400 hover:text-white transition-colors text-2xl"
                      >
                        ✕
                      </button>
                    </div>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Search teams..."
                        value={awaySearch}
                        onChange={(e) => setAwaySearch(e.target.value)}
                        className="w-full backdrop-blur-sm border border-gray-400/15 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300/25 focus:border-gray-300/35"
                        autoFocus
                      />
                    </div>
                  </div>
                  <div 
                    className="p-6 max-h-[70vh] overflow-y-auto" 
                    style={{ 
                      zIndex: 1000001,
                      position: 'relative'
                    }}
                  >
                    <div 
                      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3" 
                      style={{ 
                        zIndex: 1000002,
                        position: 'relative'
                      }}
                    >
                      {filteredAwayTeams.map((team) => (
                        <button
                          key={team.id}
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('Team button clicked:', team.school);
                            handleAwayTeamSelect(team);
                          }}
                          className="flex flex-col items-center gap-2 p-4 backdrop-blur-sm hover:bg-white/10 transition-colors rounded-lg border border-gray-400/15 hover:border-gray-400/25 cursor-pointer"
                          style={{ 
                            zIndex: 1000003,
                            position: 'relative'
                          }}
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
              </div>
            </PortalModal>
          </div>

          {/* Swap Button */}
          <button
            onClick={handleSwapTeams}
            className="hidden md:flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-sm border border-gray-400/15 hover:border-cyan-500/40 hover:bg-cyan-500/10 transition-all duration-300 group"
            title="Swap teams"
          >
            <ArrowLeftRight className="w-5 h-5 text-gray-400 group-hover:text-cyan-400 transition-colors" />
          </button>

          {/* Home Team Selector */}
          <div className="relative" ref={homeDropdownRef} style={{ zIndex: 1 }}>
            <label className="text-gray-400 text-xs mb-2 block">Home Team</label>
            <button
              onClick={() => setShowHomeDropdown(!showHomeDropdown)}
              className="w-full backdrop-blur-sm border border-gray-400/15 rounded-lg p-4 hover:border-gray-400/25 hover:bg-white/10 transition-all duration-300 group"
            >
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-white/10 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <ImageWithFallback
                    src={homeTeam.logos[1] || homeTeam.logos[0]}
                    alt={homeTeam.school}
                    className="relative w-12 h-12 object-contain"
                  />
                </div>
                <div className="flex-1 text-left">
                  <div className="flex items-center gap-2">
                    <span className="text-white font-semibold">{homeTeam.school}</span>
                  </div>
                  <span className="text-gray-400 text-sm">{homeTeam.conference}</span>
                </div>
                <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${showHomeDropdown ? 'rotate-180' : ''}`} />
              </div>
            </button>

            {/* Home Team Dropdown - Portal */}
            <PortalModal isOpen={showHomeDropdown}>
              <div 
                className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-end p-4"
                onClick={() => setShowHomeDropdown(false)}
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
                <div 
                  className="bg-gray-900/90 backdrop-blur-xl border border-gray-400/15 rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-visible animate-in fade-in slide-in-from-right-2 duration-200"
                  onClick={(e) => e.stopPropagation()}
                  style={{ 
                    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)', 
                    zIndex: 1000000,
                    position: 'relative'
                  }}
                >
                  <div className="p-6 border-b border-gray-400/15">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-white font-semibold text-xl">Select Home Team</h3>
                      <button 
                        onClick={() => setShowHomeDropdown(false)}
                        className="text-gray-400 hover:text-white transition-colors text-2xl"
                      >
                        ✕
                      </button>
                    </div>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Search teams..."
                        value={homeSearch}
                        onChange={(e) => setHomeSearch(e.target.value)}
                        className="w-full backdrop-blur-sm border border-gray-400/15 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300/25 focus:border-gray-300/35"
                        autoFocus
                      />
                    </div>
                  </div>
                  <div 
                    className="p-6 max-h-[70vh] overflow-y-auto" 
                    style={{ 
                      zIndex: 1000001,
                      position: 'relative'
                    }}
                  >
                    <div 
                      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3" 
                      style={{ 
                        zIndex: 1000002,
                        position: 'relative'
                      }}
                    >
                      {filteredHomeTeams.map((team) => (
                        <button
                          key={team.id}
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('Home team button clicked:', team.school);
                            handleHomeTeamSelect(team);
                          }}
                          className="flex flex-col items-center gap-2 p-4 backdrop-blur-sm hover:bg-white/10 transition-colors rounded-lg border border-gray-400/15 hover:border-gray-400/25 cursor-pointer"
                          style={{ 
                            zIndex: 1000003,
                            position: 'relative'
                          }}
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
              </div>
            </PortalModal>
          </div>
        </div>

        {/* Mobile Swap Button */}
        <button
          onClick={handleSwapTeams}
          className="md:hidden flex items-center justify-center gap-2 w-full py-2 rounded-lg backdrop-blur-sm border border-gray-400/15 hover:border-cyan-500/40 hover:bg-cyan-500/10 transition-all duration-300 group"
        >
          <ArrowLeftRight className="w-4 h-4 text-gray-400 group-hover:text-cyan-400 transition-colors" />
          <span className="text-gray-400 group-hover:text-cyan-400 text-sm transition-colors">Swap Teams</span>
        </button>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-3 pt-4 border-t border-gray-400/15">
          <div className="text-center">
            <div className="text-gray-400 text-xs mb-1">Away Record</div>
            <div className="text-white font-bold font-mono">5-0</div>
          </div>
          <div className="text-center">
            <div className="text-gray-400 text-xs mb-1">Home Record</div>
            <div className="text-white font-bold font-mono">5-1</div>
          </div>
        </div>

        {/* Analyze Button */}
        <button className="w-full py-3 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 border border-cyan-500/40 rounded-lg text-white font-semibold transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/20">
          Analyze Matchup
        </button>
      </div>
    </GlassCard>
  );
}