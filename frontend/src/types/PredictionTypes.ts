// GameDay+ Prediction Data Types
export interface TeamData {
  name: string;
  school: string;
  logo?: string;
  conference?: string;
}

export interface PredictionResult {
  homeWinProb: number;
  awayWinProb: number;
  spread: number;
  total: number;
  homeScore: number;
  awayScore: number;
  confidence: number;
}

export interface TeamStats {
  overallEPA: number;
  passingEPA: number;
  rushingEPA: number;
  successRate: number;
  explosiveness: number;
}

export interface FieldPositionData {
  lineYards: { home: number; away: number };
  secondLevel: { home: number; away: number };
  openField: { home: number; away: number };
  highlightYards: { home: number; away: number };
}

export interface EPAComparisonData {
  overallEPADiff: number;
  passingEPADiff: number;
  rushingEPADiff: number;
  successRateDiff: number;
  explosivenesssDiff: number;
}

export interface MarketData {
  spread: number;
  total: number;
  homeMoneyline: number;
  awayMoneyline: number;
  consensus: string;
}

export interface WeatherData {
  temperature: number;
  windSpeed: number;
  precipitation: number;
  conditions: string;
}

export interface CoachingData {
  homeCoach: {
    name: string;
    experience: number;
    record: string;
    winPercentage: number;
  };
  awayCoach: {
    name: string;
    experience: number;
    record: string;
    winPercentage: number;
  };
}

export interface AdvancedMetrics {
  homeTeam: TeamStats;
  awayTeam: TeamStats;
  differentials: EPAComparisonData;
}

export interface ComponentWeights {
  opponentAdjusted: number;
  marketConsensus: number;
  compositeRatings: number;
  keyPlayerImpact: number;
  contextualFactors: number;
}

export interface PredictionSections {
  teamSelector: {
    homeTeam: TeamData;
    awayTeam: TeamData;
  };
  header: {
    matchup: string;
    gameTime?: string;
    venue?: string;
  };
  predictionCards: PredictionResult;
  confidence: {
    level: number;
    factors: string[];
  };
  marketComparison: MarketData;
  contextualAnalysis: {
    weather: WeatherData;
    byeWeeks: any;
    polls: any;
  };
  mediaInformation: {
    tv: string;
    radio: string;
    streaming: string;
  };
  epaComparison: EPAComparisonData;
  differentialAnalysis: AdvancedMetrics;
  winProbability: {
    homeWinProb: number;
    awayWinProb: number;
    factors: string[];
  };
  fieldPosition: FieldPositionData;
  keyPlayerImpact: {
    homePlayers: any[];
    awayPlayers: any[];
    impact: number;
  };
  advancedMetrics: AdvancedMetrics;
  weightsBreakdown: ComponentWeights;
  componentBreakdown: {
    weights: ComponentWeights;
    calculations: any;
  };
  comprehensiveStats: {
    homeTeam: any;
    awayTeam: any;
  };
  coachingComparison: CoachingData;
  driveEfficiency: {
    homeTeam: any;
    awayTeam: any;
  };
  extendedDefensiveAnalytics: {
    homeDefense: any;
    awayDefense: any;
  };
  apPollRankings: {
    homeRank?: number;
    awayRank?: number;
    rankings: any[];
  };
  seasonRecords: {
    homeRecord: string;
    awayRecord: string;
    homeGames: any[];
    awayGames: any[];
  };
  finalSummary: {
    prediction: PredictionResult;
    keyFactors: string[];
  };
}

export interface PredictionData {
  homeTeam: string;
  awayTeam: string;
  prediction: PredictionResult;
  sections: PredictionSections;
  formatted_analysis: string;
  success: boolean;
  error?: string;
}

export interface PredictionRequest {
  home_team: string;
  away_team: string;
}

export interface PredictionResponse {
  success: boolean;
  data?: PredictionData;
  error?: string;
  message?: string;
}

// Component Props Interfaces
export interface ComponentProps {
  predictionData?: any;
  isLoading?: boolean;
  error?: string;
}

export interface TeamSelectorProps {
  onPrediction: (homeTeam: string, awayTeam: string) => void;
  isLoading?: boolean;
  selectedTeams?: { home: string; away: string };
}

export interface PredictionCardsProps extends ComponentProps {
  predictionData?: PredictionResult;
}

export interface FieldPositionMetricsProps extends ComponentProps {
  predictionData?: FieldPositionData;
}

export interface EPAComparisonProps extends ComponentProps {
  predictionData?: EPAComparisonData;
}

export interface MarketComparisonProps extends ComponentProps {
  predictionData?: MarketData;
}

export interface CoachingComparisonProps extends ComponentProps {
  predictionData?: CoachingData;
}