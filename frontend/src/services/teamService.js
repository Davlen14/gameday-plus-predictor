// Team service that uses local fbs.json data
import fbsData from '../fbs.json';

class TeamService {
    constructor() {
        this.teams = fbsData;
        this.teamMap = new Map();
        this.nameMap = new Map();
        this.mascotMap = new Map();
        this.abbreviationMap = new Map();
        
        // Build lookup maps for fast searching
        this.buildMaps();
    }

    // Build various lookup maps for efficient team searching
    buildMaps() {
        this.teams.forEach(team => {
            // Map by ID
            this.teamMap.set(team.id, team);
            
            // Map by school name (various formats)
            this.nameMap.set(team.school.toLowerCase(), team);
            this.nameMap.set(team.school.toLowerCase().replace(/\s+/g, ''), team);
            
            // Map by mascot
            this.mascotMap.set(team.mascot.toLowerCase(), team);
            
            // Map by abbreviation
            this.abbreviationMap.set(team.abbreviation.toLowerCase(), team);
            
            // Handle special cases and common variations
            this.addCommonVariations(team);
        });
    }

    // Add common team name variations
    addCommonVariations(team) {
        const school = team.school.toLowerCase();
        
        // Common variations
        const variations = [];
        
        // Handle "State" variations
        if (school.includes(' state')) {
            variations.push(school.replace(' state', ' st'));
            variations.push(school.replace(' state', ''));
        }
        
        // Handle "University" variations
        if (school.includes('university')) {
            variations.push(school.replace('university', 'u'));
            variations.push(school.replace(' university', ''));
        }
        
        // Handle ampersand
        if (school.includes('&')) {
            variations.push(school.replace('&', 'and'));
        }
        
        // Special team mappings for common search terms
        const specialCases = {
            'usc': team.school === 'USC' ? team : null,
            'southern cal': team.school === 'USC' ? team : null,
            'miami': team.school === 'Miami' ? team : null,
            'miami fl': team.school === 'Miami' ? team : null,
            'miami (fl)': team.school === 'Miami' ? team : null,
            'cal': team.school === 'California' ? team : null,
            'uc berkeley': team.school === 'California' ? team : null,
            'washington state': team.school === 'Washington State' ? team : null,
            'wsu': team.school === 'Washington State' ? team : null,
            'wazzu': team.school === 'Washington State' ? team : null,
            'tennessee': team.school === 'Tennessee' ? team : null,
            'tenn': team.school === 'Tennessee' ? team : null,
            'ut': team.school === 'Tennessee' ? team : null,
            'vols': team.school === 'Tennessee' ? team : null,
            'volunteers': team.school === 'Tennessee' ? team : null
        };
        
        // Add variations to maps
        variations.forEach(variation => {
            if (variation && variation !== school) {
                this.nameMap.set(variation, team);
            }
        });
        
        // Add special cases
        Object.entries(specialCases).forEach(([key, value]) => {
            if (value) {
                this.nameMap.set(key, value);
            }
        });
    }

    // Get all teams sorted by school name
    getAllTeams() {
        return [...this.teams].sort((a, b) => a.school.localeCompare(b.school));
    }

    // Get team by ID
    getTeamById(id) {
        return this.teamMap.get(parseInt(id));
    }

    // Get team by exact school name (for quick select games)
    getTeamByExactName(schoolName) {
        // Direct exact match first
        const exactMatch = this.teams.find(team => team.school === schoolName);
        if (exactMatch) return exactMatch;
        
        // Fallback to case-insensitive exact match
        const caseInsensitiveMatch = this.teams.find(team => 
            team.school.toLowerCase() === schoolName.toLowerCase()
        );
        return caseInsensitiveMatch;
    }

    // Smart team search - handles multiple input formats
    findTeam(query) {
        if (!query) return null;
        
        // If it's a number, treat as ID
        if (!isNaN(query)) {
            return this.getTeamById(parseInt(query));
        }
        
        const queryLower = query.toLowerCase().trim();
        
        // Try exact matches first
        let team = this.nameMap.get(queryLower) || 
                  this.mascotMap.get(queryLower) || 
                  this.abbreviationMap.get(queryLower);
        
        if (team) return team;
        
        // Try partial matches
        team = this.findPartialMatch(queryLower);
        if (team) return team;
        
        return null;
    }

    // Find partial matches for fuzzy searching
    findPartialMatch(query) {
        // CRITICAL: Explicit disambiguation for commonly confused teams
        // These MUST be checked before any fuzzy matching
        const exactDisambiguation = {
            'ohio': 'Ohio',           // Ohio Bobcats, NOT Ohio State
            'oklahoma': 'Oklahoma',   // Oklahoma Sooners, NOT Oklahoma State
            'miami': 'Miami',         // Miami Hurricanes, NOT Miami (OH)
            'georgia': 'Georgia',     // Georgia Bulldogs, NOT Georgia State/Tech
            'washington': 'Washington' // Washington Huskies, NOT Washington State
        };
        
        // If query exactly matches a disambiguation key, find that EXACT school name
        if (exactDisambiguation[query]) {
            const exactSchool = exactDisambiguation[query];
            for (const [name, team] of this.nameMap.entries()) {
                if (team.school === exactSchool) {
                    return team;
                }
            }
        }
        
        // First try exact word boundary matches
        for (const [name, team] of this.nameMap.entries()) {
            const nameWords = name.split(/\s+/);
            const queryWords = query.split(/\s+/);
            // Exact match on all words
            if (queryWords.length === nameWords.length && 
                queryWords.every((word, i) => nameWords[i] === word)) {
                return team;
            }
        }
        
        // Only allow partial matches if query has 2+ words (prevents "ohio" matching "ohio state")
        const queryWords = query.split(/\s+/);
        if (queryWords.length >= 2) {
            for (const [name, team] of this.nameMap.entries()) {
                if (name === query || name.startsWith(query + ' ')) {
                    return team;
                }
            }
        }
        
        // Try partial mascot match
        for (const [mascot, team] of this.mascotMap.entries()) {
            if (mascot.includes(query) || query.includes(mascot)) {
                return team;
            }
        }
        
        return null;
    }

    // Get teams by conference
    getTeamsByConference(conference) {
        return this.teams.filter(team => 
            team.conference.toLowerCase() === conference.toLowerCase()
        );
    }

    // Get all unique conferences
    getAllConferences() {
        const conferences = new Set(this.teams.map(team => team.conference));
        return Array.from(conferences).sort();
    }

    // Search teams with fuzzy matching
    searchTeams(query, limit = 10) {
        if (!query || query.length < 2) return [];
        
        const queryLower = query.toLowerCase();
        
        // Check special mappings first
        const specialMatch = this.nameMap.get(queryLower);
        if (specialMatch) {
            return [specialMatch];
        }
        
        const results = [];
        
        this.teams.forEach(team => {
            let score = 0;
            const schoolLower = team.school.toLowerCase();
            const mascotLower = team.mascot.toLowerCase();
            const abbrevLower = team.abbreviation.toLowerCase();
            
            // Exact matches get highest score (prioritize school name exact matches)
            if (schoolLower === queryLower) score = 1000;  // Increased to ensure exact wins
            else if (mascotLower === queryLower) score = 90;
            else if (abbrevLower === queryLower) score = 85;
            
            // Word-level exact matches (e.g., "Tennessee" in "Tennessee Tech")
            else if (schoolLower.split(' ').includes(queryLower)) score = 80;
            
            // Partial matches
            else if (schoolLower.includes(queryLower)) score = 70;
            else if (mascotLower.includes(queryLower)) score = 60;
            else if (abbrevLower.includes(queryLower)) score = 55;
            
            // Word boundary matches
            else if (schoolLower.split(' ').some(word => word.startsWith(queryLower))) score = 50;
            
            if (score > 0) {
                results.push({ team, score });
            }
        });
        
        return results
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map(result => result.team);
    }

    // Get team colors for UI
    getTeamColors(team) {
        if (!team) return { primary: '#1a1f26', secondary: '#ffffff' };
        
        return {
            primary: team.primary_color || '#1a1f26',
            secondary: team.alt_color || '#ffffff'
        };
    }

    // Get team logos
    getTeamLogos(team) {
        if (!team || !team.logos) {
            return {
                light: `https://via.placeholder.com/100x100?text=${team?.school?.charAt(0) || '?'}`,
                dark: `https://via.placeholder.com/100x100?text=${team?.school?.charAt(0) || '?'}`
            };
        }
        
        return {
            light: team.logos[0],
            dark: team.logos[1] || team.logos[0]
        };
    }

    // Get formatted team display name
    getDisplayName(team, format = 'full') {
        if (!team) return 'Unknown Team';
        
        switch (format) {
            case 'short':
                return team.abbreviation || team.school;
            case 'mascot':
                return team.mascot;
            case 'school':
                return team.school;
            case 'full':
            default:
                return `${team.school} ${team.mascot}`;
        }
    }

    // Convert team name to ID for API calls
    getTeamIdByName(teamName) {
        const team = this.findTeam(teamName);
        return team ? team.id : null;
    }

    // Get teams for dropdown/select components
    getTeamsForSelect() {
        return this.getAllTeams().map(team => ({
            value: team.id,
            label: team.school,
            team: team
        }));
    }

    // Validate team matchup
    validateMatchup(homeTeam, awayTeam) {
        const home = this.findTeam(homeTeam);
        const away = this.findTeam(awayTeam);
        
        const errors = [];
        
        if (!home) errors.push(`Home team "${homeTeam}" not found`);
        if (!away) errors.push(`Away team "${awayTeam}" not found`);
        if (home && away && home.id === away.id) {
            errors.push('Home and away teams cannot be the same');
        }
        
        return {
            isValid: errors.length === 0,
            errors,
            teams: { home, away }
        };
    }

    // Get team statistics/info summary
    getTeamSummary(team) {
        if (!team) return null;
        
        return {
            id: team.id,
            school: team.school,
            mascot: team.mascot,
            conference: team.conference,
            abbreviation: team.abbreviation,
            colors: this.getTeamColors(team),
            logos: this.getTeamLogos(team),
            displayName: this.getDisplayName(team)
        };
    }
}

// Export singleton instance
export const teamService = new TeamService();

// Export utility functions
export const {
    getAllTeams,
    getTeamById,
    findTeam,
    searchTeams,
    getTeamByExactName,
    getTeamsByConference,
    getAllConferences,
    getTeamColors,
    getTeamLogos,
    getDisplayName,
    getTeamIdByName,
    getTeamsForSelect,
    validateMatchup,
    getTeamSummary
} = teamService;