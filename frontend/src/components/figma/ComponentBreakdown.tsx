import { GlassCard } from './GlassCard';
import { Calculator, TrendingUp, TrendingDown, Target, Activity, Users, CloudRain, Trophy } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { extractSection } from '../../utils/teamUtils';
import React from 'react';

interface ComponentBreakdownProps {
  predictionData?: any;
}

export function ComponentBreakdown({ predictionData }: ComponentBreakdownProps) {
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;
  
  // Parse component breakdown from section [14]
  const parseComponentData = () => {
    const section = predictionData?.formatted_analysis ? extractSection(predictionData.formatted_analysis, 14) : null;
    
    if (!section) {
      return {
        opponent_adjusted: 0,
        market_consensus: 0,
        composite_ratings: 0,
        key_player_impact: 0,
        contextual_factors: 0,
        raw_differential: 0,
        home_field_advantage: 0,
        conference_bonus: 0,
        weather_penalty: 0,
        adjusted_differential: 0
      };
    }

    // Parse each component value - match format like "Opponent-Adjusted (50%): 0.108"
    const parseValue = (label: string) => {
      const pattern = new RegExp(`${label}\\s*\\([^)]+\\):\\s*([-+]?\\d+\\.\\d+)`, 'i');
      const match = section.match(pattern);
      return match ? parseFloat(match[1]) : 0;
    };

    // Parse adjustment values - match format like "Home Field Advantage: +2.5"
    const parseAdjustment = (label: string) => {
      const pattern = new RegExp(`${label}:\\s*([-+]?\\d+\\.\\d+)`, 'i');
      const match = section.match(pattern);
      return match ? parseFloat(match[1]) : 0;
    };

    return {
      opponent_adjusted: parseValue('Opponent-Adjusted'),
      market_consensus: parseValue('Market Consensus'),
      composite_ratings: parseValue('Composite Ratings'),
      key_player_impact: parseValue('Key Player Impact'),
      contextual_factors: parseValue('Contextual Factors'),
      raw_differential: parseAdjustment('Raw Differential'),
      home_field_advantage: parseAdjustment('Home Field Advantage'),
      conference_bonus: parseAdjustment('Conference Bonus'),
      weather_penalty: parseAdjustment('Weather Penalty'),
      adjusted_differential: parseAdjustment('Adjusted Differential')
    };
  };

  const data = parseComponentData();
  
  const team1Logo = awayTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png";
  const team2Logo = homeTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png";
  const team1Name = awayTeam?.name || "Away";
  const team2Name = homeTeam?.name || "Home";
  const team1Color = awayTeam?.primary_color || "#ce1141";
  const team2Color = homeTeam?.primary_color || "#ff5f05";

  const formatValue = (val: number) => val >= 0 ? `+${val.toFixed(3)}` : val.toFixed(3);
  const getValueColor = (val: number) => val > 0 ? 'text-emerald-400' : val < 0 ? 'text-red-400' : 'text-gray-400';

  return (
    <GlassCard glowColor="from-slate-500/10 to-gray-500/10" className="p-4 sm:p-6 border-gray-500/20">
      {/* Header with Team Logos */}
      <div className="mb-4 sm:mb-6">
        <div className="flex items-center justify-between mb-3 sm:mb-4 flex-wrap gap-2">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="p-1.5 sm:p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/40 shadow-lg shadow-cyan-500/20">
              <Calculator className="w-5 h-5 sm:w-6 sm:h-6 text-cyan-400" />
            </div>
            <h3 className="text-white font-bold text-base sm:text-xl">
              <span className="hidden sm:inline">Weighted Component Breakdown</span>
              <span className="sm:hidden">Components</span>
            </h3>
          </div>
        </div>
        
        {/* Team Matchup Visual */}
        <div className="flex items-center justify-between bg-gradient-to-r from-slate-800/60 via-slate-800/40 to-slate-800/60 rounded-lg p-3 sm:p-4 border border-slate-600/30 gap-2">
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <ImageWithFallback src={team1Logo} alt={team1Name} className="w-8 h-8 sm:w-12 sm:h-12 object-contain flex-shrink-0" />
            <div className="min-w-0">
              <div className="text-xs sm:text-sm text-gray-400">Away</div>
              <div className="font-semibold text-white text-sm sm:text-base truncate">{team1Name}</div>
            </div>
          </div>
          <div className="text-lg sm:text-2xl font-bold text-gray-500 flex-shrink-0">VS</div>
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <div className="text-right min-w-0">
              <div className="text-xs sm:text-sm text-gray-400">Home</div>
              <div className="font-semibold text-white text-sm sm:text-base truncate">{team2Name}</div>
            </div>
            <ImageWithFallback src={team2Logo} alt={team2Name} className="w-12 h-12 object-contain" />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {/* Component 1: Opponent-Adjusted */}
        <ComponentCard
          number={1}
          title="Opponent-Adjusted Metrics"
          percentage={50}
          value={data.opponent_adjusted}
          color="blue"
          icon={<Target className="w-5 h-5" />}
          description="Advanced EPA metrics adjusted for opponent strength, temporal performance trends, and strength of schedule"
        />

        {/* Component 2: Market Consensus */}
        <ComponentCard
          number={2}
          title="Market Consensus"
          percentage={20}
          value={data.market_consensus}
          color="purple"
          icon={<Activity className="w-5 h-5" />}
          description="Aggregated sportsbook lines and market movement analysis from multiple betting markets"
        />

        {/* Component 3: Composite Ratings */}
        <ComponentCard
          number={3}
          title="Composite Ratings - Talent"
          percentage={15}
          value={data.composite_ratings}
          color="emerald"
          icon={<Trophy className="w-5 h-5" />}
          description="Combined FPI, ELO, and recruiting talent rankings differential between teams"
        />

        {/* Component 4: Key Player Impact */}
        <ComponentCard
          number={4}
          title="Key Player Impact"
          percentage={10}
          value={data.key_player_impact}
          color="amber"
          icon={<Users className="w-5 h-5" />}
          description="QB efficiency, top WR production, and overall player impact differential analysis"
        />

        {/* Component 5: Contextual Factors */}
        <ComponentCard
          number={5}
          title="Contextual Factors"
          percentage={5}
          value={data.contextual_factors}
          color="rose"
          icon={<CloudRain className="w-5 h-5" />}
          description="Weather conditions, bye week advantages, travel distance, and AP Poll momentum"
        />

        {/* Final Calculation */}
        <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/80 rounded-xl p-6 border-2 border-cyan-500/40 backdrop-blur-sm shadow-2xl shadow-cyan-500/20">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-lg bg-cyan-500/20 border border-cyan-500/40">
              <Calculator className="w-6 h-6 text-cyan-400" />
            </div>
            <h4 className="font-bold text-white text-xl">Final Calculation</h4>
          </div>
          
          <div className="space-y-3 text-base mb-6">
            <CalcRow label="Opponent-Adjusted (50%)" value={formatValue(data.opponent_adjusted)} valueColor={getValueColor(data.opponent_adjusted)} />
            <CalcRow label="Market Consensus (20%)" value={formatValue(data.market_consensus)} valueColor={getValueColor(data.market_consensus)} />
            <CalcRow label="Composite Ratings (15%)" value={formatValue(data.composite_ratings)} valueColor={getValueColor(data.composite_ratings)} />
            <CalcRow label="Key Player Impact (10%)" value={formatValue(data.key_player_impact)} valueColor={getValueColor(data.key_player_impact)} />
            <div className="border-b border-cyan-500/30 pb-3">
              <CalcRow label="Contextual Factors (5%)" value={formatValue(data.contextual_factors)} valueColor={getValueColor(data.contextual_factors)} />
            </div>
            
            {/* Raw Differential */}
            <div className="flex justify-between items-center pt-3 bg-slate-800/50 rounded-lg p-4 border border-slate-600/40">
              <span className="text-white font-bold text-lg">RAW DIFFERENTIAL:</span>
              <span className={`text-3xl font-bold font-mono drop-shadow-lg ${getValueColor(data.raw_differential)}`}>
                {formatValue(data.raw_differential)}
              </span>
            </div>
          </div>
          
          {/* Adjustments */}
          <div className="space-y-3 text-base border-t-2 border-cyan-500/30 pt-6">
            <div className="mb-4">
              <h5 className="text-white font-bold text-base mb-2 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                Situational Adjustments
              </h5>
              <p className="text-xs text-gray-400 leading-relaxed">
                Additional factors that modify the raw differential based on game-specific circumstances
              </p>
            </div>
            
            <div className="flex justify-between items-center text-emerald-400 bg-emerald-500/10 rounded-lg p-3 border border-emerald-500/30 group hover:bg-emerald-500/15 transition-all">
              <div className="flex-1">
                <span className="font-semibold block">+ Home Field Advantage</span>
                <span className="text-xs text-emerald-300/70 mt-1 block">Standard 2.5 point home field boost</span>
              </div>
              <span className="font-mono font-bold text-lg">{formatValue(data.home_field_advantage)}</span>
            </div>
            
            <div className="flex justify-between items-center text-emerald-400 bg-emerald-500/10 rounded-lg p-3 border border-emerald-500/30 group hover:bg-emerald-500/15 transition-all">
              <div className="flex-1">
                <span className="font-semibold block">+ Conference Bonus</span>
                <span className="text-xs text-emerald-300/70 mt-1 block">Same-conference familiarity adjustment</span>
              </div>
              <span className="font-mono font-bold text-lg">{formatValue(data.conference_bonus)}</span>
            </div>
            
            <div className="flex justify-between items-center text-amber-400 bg-amber-500/10 rounded-lg p-3 border border-amber-500/30 group hover:bg-amber-500/15 transition-all">
              <div className="flex-1">
                <span className="font-semibold block">- Weather Penalty</span>
                <span className="text-xs text-amber-300/70 mt-1 block">Adverse conditions impact (wind/rain/temp)</span>
              </div>
              <span className="font-mono font-bold text-lg">{formatValue(data.weather_penalty)}</span>
            </div>
            
            {/* Adjusted Differential */}
            <div className="mt-6 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-xl p-6 border-2 border-cyan-400/50 shadow-xl shadow-cyan-500/30">
              <div className="flex items-center gap-2 mb-3">
                <Calculator className="w-5 h-5 text-cyan-400" />
                <span className="text-white font-bold text-xl">ADJUSTED DIFFERENTIAL</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-xs text-gray-400 leading-relaxed mb-2">
                    Final prediction differential after all weighted components and situational adjustments
                  </p>
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <span>Positive = {homeTeam?.name || 'Home'} Favored</span>
                    <span>•</span>
                    <span>Negative = {awayTeam?.name || 'Away'} Favored</span>
                  </div>
                </div>
                <span className={`text-5xl font-bold font-mono drop-shadow-2xl ${getValueColor(data.adjusted_differential)} ml-4`}>
                  {formatValue(data.adjusted_differential)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}

// Component Card for each weighted factor
function ComponentCard({ number, title, percentage, value, color, icon, description }: {
  number: number;
  title: string;
  percentage: number;
  value: number;
  color: string;
  icon: React.ReactNode;
  description?: string;
}) {
  const colorClasses = {
    blue: {
      bg: 'from-blue-500/20 to-blue-600/10',
      border: 'border-blue-400/40',
      text: 'text-blue-400',
      glow: 'drop-shadow-[0_0_10px_rgba(59,130,246,0.4)]'
    },
    purple: {
      bg: 'from-purple-500/20 to-purple-600/10',
      border: 'border-purple-400/40',
      text: 'text-purple-400',
      glow: 'drop-shadow-[0_0_10px_rgba(168,85,247,0.4)]'
    },
    emerald: {
      bg: 'from-emerald-500/20 to-emerald-600/10',
      border: 'border-emerald-400/40',
      text: 'text-emerald-400',
      glow: 'drop-shadow-[0_0_10px_rgba(16,185,129,0.4)]'
    },
    amber: {
      bg: 'from-amber-500/20 to-amber-600/10',
      border: 'border-amber-400/40',
      text: 'text-amber-400',
      glow: 'drop-shadow-[0_0_10px_rgba(245,158,11,0.4)]'
    },
    rose: {
      bg: 'from-rose-500/20 to-rose-600/10',
      border: 'border-rose-400/40',
      text: 'text-rose-400',
      glow: 'drop-shadow-[0_0_10px_rgba(244,63,94,0.4)]'
    }
  };

  const colors = colorClasses[color as keyof typeof colorClasses];
  const formatValue = (val: number) => val >= 0 ? `+${val.toFixed(3)}` : val.toFixed(3);

  return (
    <div className={`bg-gradient-to-br ${colors.bg} rounded-xl p-3 sm:p-5 border ${colors.border} backdrop-blur-sm hover:scale-[1.01] transition-transform duration-200`}>
      <div className="flex items-center justify-between mb-2 sm:mb-3 gap-2 flex-wrap">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <div className={`p-1.5 sm:p-2 rounded-lg bg-gradient-to-br ${colors.bg} border ${colors.border} ${colors.text} flex-shrink-0`}>
            {icon}
          </div>
          <div className="min-w-0">
            <h4 className={`${colors.text} font-bold text-sm sm:text-base truncate`}>
              [{number}/5] {title}
            </h4>
            <div className="text-xs text-gray-400 mt-0.5">Weight: {percentage}%</div>
          </div>
        </div>
        <span className={`${colors.text} font-bold text-xl sm:text-2xl font-mono ${colors.glow} whitespace-nowrap`}>
          {formatValue(value)}
        </span>
      </div>
      {description && (
        <div className="mt-2 sm:mt-3 pt-2 sm:pt-3 border-t border-gray-600/30">
          <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
        </div>
      )}
    </div>
  );
}

function CalcRow({ label, value, valueColor }: { label: string; value: string; valueColor?: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-gray-300 font-medium">{label}:</span>
      <span className={`font-bold font-mono text-lg ${valueColor || 'text-gray-200'}`}>{value}</span>
    </div>
  );
}
