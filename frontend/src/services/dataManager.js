import { CONFIG } from '../config.js';
import { teamService } from './teamService.js';

// Smart data handling with caching and error management
class DataManager {
    constructor() {
        this.cache = new Map();
        this.cacheTimestamps = new Map();
        this.CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
    }

    // Check if data is cached and still valid
    isCached(key) {
        if (!this.cache.has(key)) return false;
        const timestamp = this.cacheTimestamps.get(key);
        return timestamp && (Date.now() - timestamp) < this.CACHE_DURATION;
    }

    // Generic API call with retry logic
    async apiCall(url, options = {}, retries = CONFIG.API.RETRY_ATTEMPTS) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), CONFIG.API.TIMEOUT);

            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            if (retries > 0 && !error.name === 'AbortError') {
                console.warn(`API call failed, retrying... (${retries} attempts left)`);
                await new Promise(resolve => setTimeout(resolve, 1000));
                return this.apiCall(url, options, retries - 1);
            }
            throw error;
        }
    }

    // Fetch teams from local fbs.json (no API call needed!)
    async fetchTeams() {
        const cacheKey = 'teams';
        if (this.isCached(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            // Get teams from local fbs.json via teamService
            const teams = teamService.getAllTeams();
            const data = {
                success: true,
                teams: teams,
                count: teams.length
            };

            this.cache.set(cacheKey, data);
            this.cacheTimestamps.set(cacheKey, Date.now());

            return data;
        } catch (error) {
            console.error('Failed to load teams from local data:', error);
            throw new Error(`Unable to load teams: ${error.message}`);
        }
    }

    // Make prediction with comprehensive error handling and team validation
    async makePrediction(homeTeam, awayTeam) {
        try {
            // Validate teams using local team service first
            const validation = teamService.validateMatchup(homeTeam, awayTeam);
            if (!validation.isValid) {
                throw new Error(validation.errors.join('; '));
            }

            // Use team names for the API call
            const homeTeamName = validation.teams.home.school;
            const awayTeamName = validation.teams.away.school;

            const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PREDICT}`;
            const options = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    home_team: homeTeamName, 
                    away_team: awayTeamName 
                })
            };

            const data = await this.apiCall(url, options);
            
            // Validate response structure
            if (!data.success && !data.home_team) {
                throw new Error('Invalid prediction response from server');
            }

            // Enhance the response with local team data
            const enhancedData = this.enhancePredictionData(data, validation.teams);

            return enhancedData;
        } catch (error) {
            console.error('Prediction failed:', error);
            throw new Error(`Prediction failed: ${error.message}`);
        }
    }

    // Enhance prediction data with local team information
    enhancePredictionData(data, teams) {
        return {
            ...data,
            enhanced_teams: {
                home: teamService.getTeamSummary(teams.home),
                away: teamService.getTeamSummary(teams.away)
            },
            team_colors: {
                home: teamService.getTeamColors(teams.home),
                away: teamService.getTeamColors(teams.away)
            },
            team_logos: {
                home: teamService.getTeamLogos(teams.home),
                away: teamService.getTeamLogos(teams.away)
            }
        };
    }

    // Clear cache
    clearCache() {
        this.cache.clear();
        this.cacheTimestamps.clear();
    }

    // Get cache status
    getCacheStatus() {
        const status = {};
        for (const [key] of this.cache.entries()) {
            const timestamp = this.cacheTimestamps.get(key);
            const age = timestamp ? Date.now() - timestamp : 0;
            const isValid = age < this.CACHE_DURATION;
            status[key] = { age, isValid, ageMinutes: Math.floor(age / 60000) };
        }
        return status;
    }
}

// Export singleton instance
export const dataManager = new DataManager();