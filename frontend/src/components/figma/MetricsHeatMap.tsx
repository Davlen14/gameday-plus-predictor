import React from 'react';
import fbsData from "../../fbs.json";

interface MetricData {
  name: string;
  illinoisValue: number;
  ohioStateValue: number;
  maxValue: number;
  minValue: number;
  unit?: string;
  higherIsBetter?: boolean;
}

interface HeatMapCellProps {
  value: number;
  normalizedValue: number;
  team: 'illinois' | 'ohiostate';
  isWinner: boolean;
  metric: string;
  unit?: string;
}

const HeatMapCell: React.FC<HeatMapCellProps> = ({ 
  value, 
  normalizedValue, 
  team, 
  isWinner, 
  metric, 
  unit = '' 
}) => {
  // Calculate color intensity based on normalized value (0-100)
  const getColorIntensity = (normalized: number, isWinning: boolean) => {
    const intensity = Math.round(normalized);
    
    if (isWinning) {
      // Green for winning team
      return {
        backgroundColor: `rgba(34, 197, 94, ${0.2 + (intensity / 100) * 0.6})`,
        borderColor: `rgba(34, 197, 94, ${0.4 + (intensity / 100) * 0.4})`,
        textColor: intensity > 70 ? 'text-white' : 'text-green-200'
      };
    } else {
      // Red for losing team
      return {
        backgroundColor: `rgba(239, 68, 68, ${0.2 + (intensity / 100) * 0.6})`,
        borderColor: `rgba(239, 68, 68, ${0.4 + (intensity / 100) * 0.4})`,
        textColor: intensity > 70 ? 'text-white' : 'text-red-200'
      };
    }
  };

  const colors = getColorIntensity(normalizedValue, isWinner);
  const teamColor = team === 'illinois' ? '#FF6B35' : '#E53E3E';

  return (
    <div 
      className={`relative p-4 rounded-lg border transition-all duration-500 hover:scale-105 group cursor-pointer`}
      style={{
        backgroundColor: colors.backgroundColor,
        borderColor: colors.borderColor,
        borderWidth: '1px'
      }}
    >
      {/* Glow effect on hover */}
      <div 
        className="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-30 transition-opacity duration-300"
        style={{
          boxShadow: `0 0 20px ${teamColor}`,
        }}
      />
      
      <div className="relative z-10">
        <div className="text-center">
          <div className={`text-lg font-bold ${colors.textColor} transition-colors duration-300`}>
            {value.toLocaleString()}{unit}
          </div>
          <div className="text-xs text-gray-400 mt-1">
            {Math.round(normalizedValue)}%
          </div>
          {isWinner && (
            <div className="text-xs text-green-300 font-semibold mt-1">
              ✓ ADVANTAGE
            </div>
          )}
        </div>
      </div>
      
      {/* Animated background pattern */}
      <div 
        className="absolute inset-0 opacity-10 rounded-lg"
        style={{
          backgroundImage: `radial-gradient(circle at 20% 50%, ${teamColor} 2px, transparent 2px)`,
          backgroundSize: '20px 20px'
        }}
      />
    </div>
  );
};

interface MetricsHeatMapProps {
  className?: string;
}

const MetricsHeatMap: React.FC<MetricsHeatMapProps> = ({ className = '' }) => {
  // Get team data from FBS JSON
  const getTeamData = (schoolName: string) => {
    return fbsData.find(team => team.school === schoolName);
  };

  const illinoisTeam = getTeamData('Illinois');
  const ohioStateTeam = getTeamData('Ohio State');

  // Get dark logos (second logo in the array)
  const illinoisLogo = illinoisTeam?.logos[1] || '';
  const ohioStateLogo = ohioStateTeam?.logos[1] || '';

  const metrics: MetricData[] = [
    {
      name: 'ELO Rating',
      illinoisValue: 1585,
      ohioStateValue: 2078,
      maxValue: 2200,
      minValue: 1400,
      higherIsBetter: true
    },
    {
      name: 'FPI Rating',
      illinoisValue: 10.4,
      ohioStateValue: 24.9,
      maxValue: 30,
      minValue: 0,
      higherIsBetter: true
    },
    {
      name: 'Talent Rating',
      illinoisValue: 662,
      ohioStateValue: 974,
      maxValue: 1000,
      minValue: 600,
      higherIsBetter: true
    },
    {
      name: 'Success Rate (Off)',
      illinoisValue: 0.460,
      ohioStateValue: 0.487,
      maxValue: 0.6,
      minValue: 0.3,
      higherIsBetter: true
    },
    {
      name: 'Success Rate (Def)',
      illinoisValue: 0.449,
      ohioStateValue: 0.378,
      maxValue: 0.6,
      minValue: 0.3,
      higherIsBetter: false // Lower is better for defense
    },
    {
      name: 'Explosiveness (Off)',
      illinoisValue: 0.929,
      ohioStateValue: 0.919,
      maxValue: 1.2,
      minValue: 0.7,
      higherIsBetter: true
    },
    {
      name: 'Explosiveness (Def)',
      illinoisValue: 0.937,
      ohioStateValue: 0.945,
      maxValue: 1.2,
      minValue: 0.7,
      higherIsBetter: false // Lower is better for defense
    }
  ];

  const normalizeValue = (value: number, min: number, max: number) => {
    return ((value - min) / (max - min)) * 100;
  };

  const determineWinner = (metric: MetricData) => {
    if (metric.higherIsBetter) {
      return metric.illinoisValue > metric.ohioStateValue ? 'illinois' : 'ohiostate';
    } else {
      return metric.illinoisValue < metric.ohioStateValue ? 'illinois' : 'ohiostate';
    }
  };

  return (
    <div className={`bg-black/20 backdrop-blur-sm rounded-2xl border border-gray-400/15 p-6 ${className}`}>
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-white text-center mb-2">
          Performance Heat Map
        </h3>
        <p className="text-gray-400 text-center text-sm">
          Color intensity shows relative performance • Green = Advantage • Red = Disadvantage
        </p>
      </div>

      {/* Legend */}
      <div className="flex justify-center items-center space-x-8 mb-6">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded bg-green-500/60 border border-green-500"></div>
          <span className="text-green-200 text-sm font-medium">Advantage</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded bg-red-500/60 border border-red-500"></div>
          <span className="text-red-200 text-sm font-medium">Disadvantage</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-gray-400 text-sm">Intensity = Relative Performance</div>
        </div>
      </div>

      {/* Heat Map Grid */}
      <div className="space-y-4">
        {/* Header Row */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-300">Metric</div>
          </div>
          <div className="text-center">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-orange-500/30 p-3 inline-flex items-center space-x-3 transition-all duration-300 hover:bg-white/15 hover:scale-105">
              {illinoisLogo ? (
                <img 
                  src={illinoisLogo}
                  alt="Illinois logo"
                  className="w-8 h-8 object-contain"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.parentElement!.innerHTML = `
                      <div class="w-8 h-8 bg-orange-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                        ILL
                      </div>
                    `;
                  }}
                />
              ) : (
                <div className="w-8 h-8 bg-orange-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  ILL
                </div>
              )}
              <div className="text-left">
                <div className="text-lg font-semibold text-orange-400">Illinois</div>
                <div className="text-xs text-gray-400">Fighting Illini</div>
              </div>
            </div>
          </div>
          <div className="text-center">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-red-500/30 p-3 inline-flex items-center space-x-3 transition-all duration-300 hover:bg-white/15 hover:scale-105">
              {ohioStateLogo ? (
                <img 
                  src={ohioStateLogo}
                  alt="Ohio State logo"
                  className="w-8 h-8 object-contain"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.parentElement!.innerHTML = `
                      <div class="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                        OSU
                      </div>
                    `;
                  }}
                />
              ) : (
                <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  OSU
                </div>
              )}
              <div className="text-left">
                <div className="text-lg font-semibold text-red-400">Ohio State</div>
                <div className="text-xs text-gray-400">Buckeyes</div>
              </div>
            </div>
          </div>
        </div>

        {/* Data Rows */}
        {metrics.map((metric, index) => {
          const winner = determineWinner(metric);
          const illinoisNormalized = normalizeValue(metric.illinoisValue, metric.minValue, metric.maxValue);
          const ohioStateNormalized = normalizeValue(metric.ohioStateValue, metric.minValue, metric.maxValue);

          return (
            <div key={metric.name} className="grid grid-cols-3 gap-4 items-center">
              {/* Metric Name */}
              <div className="text-center">
                <div className="text-white font-medium text-sm bg-gray-800/50 rounded-lg p-3 border border-gray-700">
                  {metric.name}
                  {!metric.higherIsBetter && (
                    <div className="text-xs text-gray-400 mt-1">
                      (Lower is better)
                    </div>
                  )}
                </div>
              </div>

              {/* Illinois Cell */}
              <HeatMapCell
                value={metric.illinoisValue}
                normalizedValue={illinoisNormalized}
                team="illinois"
                isWinner={winner === 'illinois'}
                metric={metric.name}
                unit={metric.unit}
              />

              {/* Ohio State Cell */}
              <HeatMapCell
                value={metric.ohioStateValue}
                normalizedValue={ohioStateNormalized}
                team="ohiostate"
                isWinner={winner === 'ohiostate'}
                metric={metric.name}
                unit={metric.unit}
              />
            </div>
          );
        })}
      </div>

      {/* Summary Stats */}
      <div className="mt-6 pt-6 border-t border-gray-400/15">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center bg-orange-500/10 rounded-lg p-4 border border-orange-500/20">
            <div className="text-orange-400 font-semibold">Illinois Advantages</div>
            <div className="text-2xl font-bold text-white">
              {metrics.filter(m => determineWinner(m) === 'illinois').length}
            </div>
            <div className="text-xs text-gray-400">out of {metrics.length} metrics</div>
          </div>
          <div className="text-center bg-red-500/10 rounded-lg p-4 border border-red-500/20">
            <div className="text-red-400 font-semibold">Ohio State Advantages</div>
            <div className="text-2xl font-bold text-white">
              {metrics.filter(m => determineWinner(m) === 'ohiostate').length}
            </div>
            <div className="text-xs text-gray-400">out of {metrics.length} metrics</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsHeatMap;