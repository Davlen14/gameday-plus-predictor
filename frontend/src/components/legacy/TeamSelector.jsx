import React, { useState, useEffect, useMemo } from 'react';
import { teamService } from '../services/teamService.js';
import { useAppStore } from '../store.js';
import { GlassCard, LoadingSpinner, ErrorDisplay } from './DynamicComponents.jsx';

export const TeamSelector = () => {
    const [searchHome, setSearchHome] = useState('');
    const [searchAway, setSearchAway] = useState('');
    const [homeResults, setHomeResults] = useState([]);
    const [awayResults, setAwayResults] = useState([]);
    
    const { 
        selectedHomeTeam, 
        selectedAwayTeam, 
        setSelectedTeams,
        predictionLoading 
    } = useAppStore();

    // Get teams for dropdowns with search
    const allTeams = useMemo(() => teamService.getAllTeams(), []);

    // Handle team search
    useEffect(() => {
        if (searchHome.length > 1) {
            const results = teamService.searchTeams(searchHome, 5);
            setHomeResults(results);
        } else {
            setHomeResults([]);
        }
    }, [searchHome]);

    useEffect(() => {
        if (searchAway.length > 1) {
            const results = teamService.searchTeams(searchAway, 5);
            setAwayResults(results);
        } else {
            setAwayResults([]);
        }
    }, [searchAway]);

    const handleTeamSelect = (team, type) => {
        if (type === 'home') {
            setSelectedTeams(team, selectedAwayTeam);
            setSearchHome(team.school);
            setHomeResults([]);
        } else {
            setSelectedTeams(selectedHomeTeam, team);
            setSearchAway(team.school);
            setAwayResults([]);
        }
    };

    const TeamSearchInput = ({ 
        type, 
        value, 
        onChange, 
        results, 
        onSelect, 
        placeholder 
    }) => (
        <div className="relative">
            <input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                className="w-full p-4 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:border-cyan-500 focus:outline-none transition-colors"
                disabled={predictionLoading}
            />
            
            {results.length > 0 && (
                <div className="absolute top-full left-0 right-0 z-50 mt-1 glass-card border border-slate-600 rounded-xl overflow-hidden">
                    {results.map((team) => (
                        <div
                            key={team.id}
                            onClick={() => onSelect(team, type)}
                            className="p-3 hover:bg-slate-700/50 cursor-pointer border-b border-slate-600 last:border-b-0 flex items-center gap-3"
                        >
                            <img 
                                src={team.logos[0]} 
                                alt={team.school}
                                className="w-8 h-8 object-contain"
                                onError={(e) => {
                                    e.target.src = `https://via.placeholder.com/32x32?text=${team.school.charAt(0)}`;
                                }}
                            />
                            <div>
                                <div className="text-white font-medium">{team.school}</div>
                                <div className="text-slate-400 text-sm">{team.mascot} • {team.conference}</div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );

    const SelectedTeamDisplay = ({ team, type }) => {
        if (!team) return null;

        const colors = teamService.getTeamColors(team);
        
        return (
            <div 
                className="glass-card p-4 rounded-xl border"
                style={{ borderColor: colors.primary + '40' }}
            >
                <div className="flex items-center gap-4">
                    <img 
                        src={team.logos[0]} 
                        alt={team.school}
                        className="w-12 h-12 object-contain"
                    />
                    <div className="flex-1">
                        <div className="text-white font-bold text-lg">{team.school}</div>
                        <div className="text-slate-300">{team.mascot}</div>
                        <div className="text-slate-400 text-sm">{team.conference}</div>
                    </div>
                    <div className="text-right">
                        <div className="text-slate-400 text-sm">{type === 'home' ? '🏠 Home' : '✈️ Away'}</div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="space-y-6 max-w-4xl mx-auto">
            {/* Search Inputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <label className="text-slate-300 font-medium">Home Team 🏠</label>
                    <TeamSearchInput
                        type="home"
                        value={searchHome}
                        onChange={setSearchHome}
                        results={homeResults}
                        onSelect={handleTeamSelect}
                        placeholder="Search for home team..."
                    />
                </div>
                
                <div className="space-y-2">
                    <label className="text-slate-300 font-medium">Away Team ✈️</label>
                    <TeamSearchInput
                        type="away"
                        value={searchAway}
                        onChange={setSearchAway}
                        results={awayResults}
                        onSelect={handleTeamSelect}
                        placeholder="Search for away team..."
                    />
                </div>
            </div>

            {/* Selected Teams Display */}
            {(selectedHomeTeam || selectedAwayTeam) && (
                <div className="space-y-4">
                    <h4 className="text-white font-semibold">Selected Matchup</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {selectedHomeTeam && (
                            <SelectedTeamDisplay team={selectedHomeTeam} type="home" />
                        )}
                        {selectedAwayTeam && (
                            <SelectedTeamDisplay team={selectedAwayTeam} type="away" />
                        )}
                    </div>
                </div>
            )}

            {/* Quick Team Stats */}
            {selectedHomeTeam && selectedAwayTeam && (
                <div className="glass-card p-4 rounded-xl border border-cyan-500/40">
                    <div className="text-center">
                        <div className="text-cyan-400 font-semibold mb-2">🎯 Matchup Ready</div>
                        <div className="text-slate-300">
                            {selectedAwayTeam.school} @ {selectedHomeTeam.school}
                        </div>
                        <div className="text-slate-400 text-sm mt-1">
                            {selectedAwayTeam.conference} vs {selectedHomeTeam.conference}
                        </div>
                    </div>
                </div>
            )}

            {/* Loading State */}
            {predictionLoading && (
                <div className="text-center py-4">
                    <LoadingSpinner size="lg" className="mx-auto mb-2" />
                    <div className="text-slate-300">Analyzing matchup...</div>
                </div>
            )}
        </div>
    );
};