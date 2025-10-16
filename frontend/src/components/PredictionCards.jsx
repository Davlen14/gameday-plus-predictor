import React from 'react';
import { usePredictionSelector } from '../store.js';
import { PredictionCard, GlassCard, LoadingSpinner, ErrorDisplay } from './DynamicComponents.jsx';

export const PredictionCards = () => {
    const { data, loading, error } = usePredictionSelector();

    if (loading) {
        return (
            <GlassCard title="🎯 Predictions" className="col-span-full">
                <div className="text-center py-8">
                    <LoadingSpinner size="lg" className="mx-auto mb-4" />
                    <div className="text-slate-300">Crunching the numbers...</div>
                </div>
            </GlassCard>
        );
    }

    if (error) {
        return (
            <GlassCard title="🎯 Predictions" className="col-span-full">
                <ErrorDisplay error={error} />
            </GlassCard>
        );
    }

    if (!data) {
        return (
            <GlassCard title="🎯 Predictions" className="col-span-full">
                <div className="text-center py-8 text-slate-400">
                    Select two teams to see predictions
                </div>
            </GlassCard>
        );
    }

    // Determine winner and confidence styling
    const getWinnerType = () => {
        if (data.home_win_probability > 60) return 'positive';
        if (data.home_win_probability < 40) return 'negative';
        return 'warning';
    };

    const getConfidenceType = () => {
        if (data.confidence > 80) return 'positive';
        if (data.confidence > 60) return 'warning';
        return 'neutral';
    };

    const getSpreadType = () => {
        if (Math.abs(data.spread) > 10) return 'warning';
        if (Math.abs(data.spread) < 3) return 'neutral';
        return 'positive';
    };

    return (
        <>
            {/* Main Prediction Cards */}
            <div className="col-span-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <PredictionCard
                    label="🏆 Predicted Winner"
                    value={data.predicted_winner}
                    detail={`${data.home_win_probability.toFixed(1)}% chance`}
                    type={getWinnerType()}
                />
                
                <PredictionCard
                    label="📊 Point Spread"
                    value={data.spread > 0 ? `+${data.spread.toFixed(1)}` : data.spread.toFixed(1)}
                    detail={`${data.home_team} ${data.spread > 0 ? 'getting' : 'favored by'} ${Math.abs(data.spread).toFixed(1)}`}
                    type={getSpreadType()}
                />
                
                <PredictionCard
                    label="🔢 Predicted Total"
                    value={data.total.toFixed(1)}
                    detail="Combined points"
                    type="neutral"
                />
                
                <PredictionCard
                    label="🎪 Confidence"
                    value={`${data.confidence.toFixed(1)}%`}
                    detail="Model certainty"
                    type={getConfidenceType()}
                />
            </div>

            {/* Enhanced Score Prediction */}
            <div className="col-span-full">
                <GlassCard title="🏈 Score Prediction" className="text-center">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
                        {/* Away Team */}
                        <div className="space-y-4">
                            {data.enhanced_teams?.away && (
                                <div className="flex items-center justify-center gap-3">
                                    <img 
                                        src={data.enhanced_teams.away.logos.light} 
                                        alt={data.away_team}
                                        className="w-16 h-16 object-contain"
                                    />
                                    <div>
                                        <div className="text-white font-bold text-lg">{data.away_team}</div>
                                        <div className="text-slate-400">Away</div>
                                    </div>
                                </div>
                            )}
                            <div className="metric-value-neutral text-4xl font-bold analytical-number">
                                {data.away_score}
                            </div>
                        </div>

                        {/* VS */}
                        <div className="text-slate-400 text-2xl font-bold">VS</div>

                        {/* Home Team */}
                        <div className="space-y-4">
                            {data.enhanced_teams?.home && (
                                <div className="flex items-center justify-center gap-3">
                                    <img 
                                        src={data.enhanced_teams.home.logos.light} 
                                        alt={data.home_team}
                                        className="w-16 h-16 object-contain"
                                    />
                                    <div>
                                        <div className="text-white font-bold text-lg">{data.home_team}</div>
                                        <div className="text-slate-400">Home</div>
                                    </div>
                                </div>
                            )}
                            <div className="metric-value-neutral text-4xl font-bold analytical-number">
                                {data.home_score}
                            </div>
                        </div>
                    </div>
                </GlassCard>
            </div>

            {/* Value Picks */}
            {(data.value_spread_pick || data.value_total_pick) && (
                <div className="col-span-full">
                    <GlassCard title="💰 Value Picks" className="border border-emerald-500/40">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {data.value_spread_pick && (
                                <div className="glass-card p-4 rounded-xl border border-emerald-500/40">
                                    <div className="text-emerald-400 font-semibold mb-2">📈 Spread Value</div>
                                    <div className="text-white text-lg">{data.value_spread_pick}</div>
                                    <div className="text-slate-400 text-sm">
                                        {data.spread_edge?.toFixed(1)} point edge
                                    </div>
                                </div>
                            )}
                            
                            {data.value_total_pick && (
                                <div className="glass-card p-4 rounded-xl border border-emerald-500/40">
                                    <div className="text-emerald-400 font-semibold mb-2">🎯 Total Value</div>
                                    <div className="text-white text-lg">{data.value_total_pick}</div>
                                    <div className="text-slate-400 text-sm">
                                        {data.total_edge?.toFixed(1)} point edge
                                    </div>
                                </div>
                            )}
                        </div>
                    </GlassCard>
                </div>
            )}

            {/* Key Factors */}
            {data.key_factors && data.key_factors.length > 0 && (
                <div className="col-span-full">
                    <GlassCard title="🔑 Key Factors">
                        <div className="flex flex-wrap gap-2">
                            {data.key_factors.map((factor, index) => (
                                <span 
                                    key={index}
                                    className="px-3 py-1 bg-cyan-500/20 border border-cyan-500/40 rounded-full text-cyan-300 text-sm"
                                >
                                    {factor}
                                </span>
                            ))}
                        </div>
                    </GlassCard>
                </div>
            )}
        </>
    );
};