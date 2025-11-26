// Dynamic configuration hub for the football analytics dashboard
export const CONFIG = {
    // Dynamic API management
    API: {
        BASE_URL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:5002',
        ENDPOINTS: {
            TEAMS: '/teams',
            PREDICT: '/predict'
        },
        TIMEOUT: 10000,
        RETRY_ATTEMPTS: 3
    },
    
    // Dynamic sections that can be enabled/disabled  
    SECTIONS: {
        TEAM_SELECTOR: { enabled: true, order: 1 },
        PREDICTION_CARDS: { enabled: true, order: 2 },
        CHARTS: { enabled: true, order: 3 },
        EPA_ANALYSIS: { enabled: true, order: 4 },
        WEATHER: { enabled: false, order: 5, comingSoon: true },
        PLAYER_IMPACT: { enabled: false, order: 6, comingSoon: true },
        MARKET_COMPARISON: { enabled: true, order: 7 },
        ALGORITHM_BREAKDOWN: { enabled: true, order: 8 },
        GLOSSARY: { enabled: true, order: 15 }
    },
    
    // Dynamic chart configurations
    CHARTS: {
        COLORS: {
            home: '#3b82f6',
            away: '#8b5cf6',
            positive: '#10b981',
            negative: '#ef4444',
            neutral: '#06b6d4',
            warning: '#f59e0b'
        },
        RESPONSIVE: true,
        ANIMATION_DURATION: 1000
    },

    // UI Configuration
    UI: {
        ANIMATIONS: {
            FADE_DURATION: 500,
            SLIDE_DURATION: 300,
            PULSE_DURATION: 2000
        },
        BREAKPOINTS: {
            SM: 640,
            MD: 768,
            LG: 1024,
            XL: 1280,
            '2XL': 1536
        }
    }
};