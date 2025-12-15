import React, { useEffect, useRef } from 'react';
import { SciChartReact } from 'scichart-react';
import { getDefensiveRadialConfig, DefensiveMetric } from './defensive-radial-config';

interface DefensiveMetrics {
  fumbles_recovered_per_game?: number;
  tackles_for_loss_per_game?: number;
  defense_success_rate?: number;
  sacks_per_game?: number;
  interceptions_per_game?: number;
  defense_ppa?: number;
  defense_havoc_total?: number;
  defense_explosiveness?: number;
}

interface TeamMetrics {
  normalized?: DefensiveMetrics;
  raw?: DefensiveMetrics;
}

interface DefensiveStatsSciChartProps {
  homeTeam: string;
  awayTeam: string;
  homeMetrics?: TeamMetrics;
  awayMetrics?: TeamMetrics;
  homeColor?: string;
  awayColor?: string;
}

export const DefensiveStatsSciChart: React.FC<DefensiveStatsSciChartProps> = ({
  homeTeam,
  awayTeam,
  homeMetrics,
  awayMetrics,
  homeColor = '#FF6B6B',
  awayColor = '#4ECDC4',
}) => {
  const chartDivId = 'defensive-radial-chart';

  if (!homeMetrics?.raw || !awayMetrics?.raw) {
    return (
      <div className="backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h3 className="text-xl font-bold text-white mb-4">🛡️ Defensive Statistics Dashboard</h3>
        <p className="text-gray-300">Defensive metrics not available</p>
      </div>
    );
  }

  // Extract 8 key defensive metrics
  const metrics: DefensiveMetric[] = [
    {
      name: 'Sacks/Game',
      homeValue: homeMetrics.raw.sacks_per_game || 0,
      awayValue: awayMetrics.raw.sacks_per_game || 0,
    },
    {
      name: 'Interceptions',
      homeValue: homeMetrics.raw.interceptions_per_game || 0,
      awayValue: awayMetrics.raw.interceptions_per_game || 0,
    },
    {
      name: 'TFL/Game',
      homeValue: homeMetrics.raw.tackles_for_loss_per_game || 0,
      awayValue: awayMetrics.raw.tackles_for_loss_per_game || 0,
    },
    {
      name: 'Fumbles Rec',
      homeValue: homeMetrics.raw.fumbles_recovered_per_game || 0,
      awayValue: awayMetrics.raw.fumbles_recovered_per_game || 0,
    },
    {
      name: 'Defense PPA',
      homeValue: homeMetrics.raw.defense_ppa || 0,
      awayValue: awayMetrics.raw.defense_ppa || 0,
      inverse: true, // Lower is better
    },
    {
      name: 'Success Rate',
      homeValue: homeMetrics.raw.defense_success_rate || 0,
      awayValue: awayMetrics.raw.defense_success_rate || 0,
      unit: '%',
      inverse: true, // Lower is better
    },
    {
      name: 'Explosiveness',
      homeValue: homeMetrics.raw.defense_explosiveness || 0,
      awayValue: awayMetrics.raw.defense_explosiveness || 0,
      inverse: true, // Lower is better
    },
    {
      name: 'Havoc Rate',
      homeValue: homeMetrics.raw.defense_havoc_total || 0,
      awayValue: awayMetrics.raw.defense_havoc_total || 0,
      unit: '%',
    },
  ];

  // Calculate leader counts
  const homeLeads = metrics.filter(m =>
    m.inverse ? m.homeValue < m.awayValue : m.homeValue > m.awayValue
  ).length;
  const awayLeads = metrics.length - homeLeads;

  return (
    <div className="backdrop-blur-xl rounded-2xl p-6 border border-white/20 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🛡️</span>
          <div>
            <h3 className="text-2xl font-bold text-white">Defensive Statistics Dashboard</h3>
            <p className="text-sm text-gray-400">SciChart Radar Analysis - 8 Key Metrics</p>
          </div>
        </div>
        <div className="flex gap-4 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: awayColor }}></span>
            <span className="text-white font-semibold">{awayTeam}</span>
            <span className="text-gray-400">leads {awayLeads}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: homeColor }}></span>
            <span className="text-white font-semibold">{homeTeam}</span>
            <span className="text-gray-400">leads {homeLeads}</span>
          </div>
        </div>
      </div>

      {/* SciChart Radial/Spider Chart */}
      <div className="bg-black/30 rounded-xl p-4 mb-6">
        <SciChartReact
          initChart={getDefensiveRadialConfig(
            homeTeam,
            awayTeam,
            metrics,
            homeColor,
            awayColor
          )}
          style={{ height: '600px', width: '100%' }}
        />
      </div>

      {/* Metric Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
        {metrics.map((metric, index) => {
          const homeWins = metric.inverse
            ? metric.homeValue < metric.awayValue
            : metric.homeValue > metric.awayValue;
          
          return (
            <div
              key={index}
              className="backdrop-blur-sm bg-white/5 rounded-lg p-4 border border-white/10 hover:border-white/20 transition-all"
            >
              <div className="text-xs text-gray-400 mb-2 font-semibold uppercase tracking-wider">
                {metric.name}
              </div>
              <div className="flex justify-between items-center gap-3">
                <div className={`flex-1 ${homeWins ? 'text-green-400' : 'text-gray-300'}`}>
                  <div className="text-lg font-bold">
                    {metric.homeValue.toFixed(metric.unit === '%' ? 1 : 2)}{metric.unit || ''}
                  </div>
                  <div className="text-xs text-gray-500">{homeTeam}</div>
                </div>
                <div className="text-2xl text-gray-600">vs</div>
                <div className={`flex-1 text-right ${!homeWins ? 'text-green-400' : 'text-gray-300'}`}>
                  <div className="text-lg font-bold">
                    {metric.awayValue.toFixed(metric.unit === '%' ? 1 : 2)}{metric.unit || ''}
                  </div>
                  <div className="text-xs text-gray-500">{awayTeam}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Insights Box */}
      <div className="mt-6 p-4 rounded-lg bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20">
        <div className="text-sm space-y-2">
          <div className="flex items-start gap-3">
            <div className="text-blue-400 font-bold text-xs">WHAT IT MEANS:</div>
            <div className="text-gray-300">
              Defensive metrics show each team's ability to disrupt opponent offenses through pressure, turnovers, and limiting explosive plays.
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="text-purple-400 font-bold text-xs">WHY IT MATTERS:</div>
            <div className="text-gray-300">
              {homeLeads > awayLeads ? homeTeam : awayTeam} defense dominates in {Math.max(homeLeads, awayLeads)} of 8 categories, suggesting stronger defensive performance.
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="text-green-400 font-bold text-xs">WHO HAS EDGE:</div>
            <div className="text-gray-300">
              <span className="font-bold" style={{ color: homeLeads > awayLeads ? homeColor : awayColor }}>
                {homeLeads > awayLeads ? homeTeam : awayTeam}
              </span>
              {' '}holds the defensive edge with superior metrics in key areas like {
                metrics
                  .filter(m => (m.inverse ? m.homeValue < m.awayValue : m.homeValue > m.awayValue) === (homeLeads > awayLeads))
                  .slice(0, 3)
                  .map(m => m.name)
                  .join(', ')
              }.
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-4 pt-4 border-t border-white/20 flex justify-center gap-6 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 border-2 rounded" style={{ borderColor: homeColor }}></div>
          <span className="text-gray-400">{homeTeam} Defense</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 border-2 rounded" style={{ borderColor: awayColor }}></div>
          <span className="text-gray-400">{awayTeam} Defense</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-400 rounded"></div>
          <span className="text-gray-400">Leader in Category</span>
        </div>
      </div>
    </div>
  );
};

export default DefensiveStatsSciChart;
