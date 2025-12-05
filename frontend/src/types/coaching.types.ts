// TypeScript interfaces for coaching analysis data

export interface EnhancedAnalysis {
  season_2025: {
    season_score: number;
    record: string;
    win_pct: number;
    quality_wins: number;
    blowout_wins: number;
    close_wins: number;
    bad_losses: number;
    rating: string;
  };
  recent_trend: {
    avg_trend: number;
    weighted_win_pct: number;
    recent_seasons: {
      [year: string]: {
        wins: number;
        losses: number;
        total: number;
        win_pct: number;
        weight: number;
      };
    };
  };
  talent_context: {
    tier: string;
    expected_win_pct: number;
    actual_win_pct: number;
    performance_delta: number;
    classification: string;
    context_score: number;
  };
  big_game_analysis: {
    big_game_score: number;
    clutch_rating: string;
    vs_top5_record: string;
    vs_top5_pct: number;
    vs_top10_pct: number;
    vs_ranked_pct: number;
    big_games_total: number;
  };
  recruiting: {
    avg_talent_composite: number;
    recent_avg_composite: number;
    talent_rating: number;
  };
  draft_analysis: {
    total_picks: number;
    first_rounders: number;
    top10_picks: number;
    score: number;
  };
  betting_2025: {
    total: number;
    covers: number;
    cover_rate: number;
  };
  consistency: {
    score: number;
    rating: string;
  };
}

export interface CoachRanking {
  name: string;
  team: string;
  conference: string;
  careerRecord: string;
  careerWinPct: number;
  "2025Record": string;
  "2025Games": number;
  composite_score: number;
  composite_rank: number;
  raw_score: number;
  coach_summary: string;
  enhanced_analysis: EnhancedAnalysis;
  totalWins?: number;
  overallRank?: number;
}

export interface RankCategory {
  label: string;
  color: string;
  icon: string;
}

export interface FactorStat {
  label: string;
  value: string | number;
  className?: string;
}
