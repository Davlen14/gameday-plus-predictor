import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { ApiClient } from './services/apiClient';

// Global state management for the football analytics dashboard
export const useAppStore = create(
    devtools(
        (set, get) => ({
            // Teams data
            teams: [],
            teamsLoading: false,
            teamsError: null,

            // Prediction data from your Flask API
            predictionData: null,
            predictionLoading: false,
            predictionError: null,

            // UI state
            selectedHomeTeam: null,
            selectedAwayTeam: null,
            activeSections: [],
            sectionStates: {},

            // Actions
            setTeams: (teams) => set({ teams, teamsLoading: false }),
            setTeamsLoading: (loading) => set({ teamsLoading: loading }),
            setTeamsError: (error) => set({ teamsError: error, teamsLoading: false }),

            setPredictionData: (data) => set({ 
                predictionData: data, 
                predictionLoading: false,
                predictionError: null
            }),
            setPredictionLoading: (loading) => set({ predictionLoading: loading }),
            setPredictionError: (error) => set({ 
                predictionError: error, 
                predictionLoading: false 
            }),

            setSelectedTeams: (homeTeam, awayTeam) => set({ 
                selectedHomeTeam: homeTeam, 
                selectedAwayTeam: awayTeam 
            }),

            // Call your existing Flask API
            fetchPrediction: async (homeTeam, awayTeam) => {
                set({ predictionLoading: true, predictionError: null });
                
                try {
                    const result = await ApiClient.getPrediction(homeTeam, awayTeam);
                    
                    if (result.success) {
                        set({ 
                            predictionData: result.data,
                            predictionLoading: false,
                            predictionError: null
                        });
                    } else {
                        set({ 
                            predictionError: result.error,
                            predictionLoading: false
                        });
                    }
                } catch (error) {
                    set({ 
                        predictionError: error.message,
                        predictionLoading: false
                    });
                }
            },

            enableSection: (sectionId) => set((state) => {
                if (state.activeSections.includes(sectionId)) return state;
                return { activeSections: [...state.activeSections, sectionId] };
            }),

            setSectionState: (sectionId, state) => set((currentState) => ({
                sectionStates: {
                    ...currentState.sectionStates,
                    [sectionId]: state
                }
            })),

            // Clear all data (reset state)
            clearData: () => set({
                predictionData: null,
                predictionError: null,
                selectedHomeTeam: null,
                selectedAwayTeam: null
            })
        }),
        { name: 'gameday-analytics-store' }
    )
);

// Selectors for derived state
export const useTeamsSelector = () => useAppStore(state => ({
    teams: state.teams,
    loading: state.teamsLoading,
    error: state.teamsError
}));

export const usePredictionSelector = () => useAppStore(state => ({
    data: state.predictionData,
    loading: state.predictionLoading,
    error: state.predictionError
}));

export const useSelectedTeamsSelector = () => useAppStore(state => ({
    homeTeam: state.selectedHomeTeam,
    awayTeam: state.selectedAwayTeam
}));