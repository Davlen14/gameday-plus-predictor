import React from 'react';

interface ComparisonBarProps {
  label: string;
  coach1Value: number;
  coach2Value: number;
  max: number;
  inverse?: boolean;
  coach1Name: string;
  coach2Name: string;
  coach1Color?: string;
  coach2Color?: string;
}

export const ComparisonBar: React.FC<ComparisonBarProps> = ({ 
  label, 
  coach1Value, 
  coach2Value, 
  max, 
  inverse = false,
  coach1Name,
  coach2Name,
  coach1Color = '#a855f7',
  coach2Color = '#3b82f6'
}) => {
  const coach1Pct = Math.min((coach1Value / max) * 100, 100);
  const coach2Pct = Math.min((coach2Value / max) * 100, 100);
  
  const winner = inverse ? 
    (coach1Value < coach2Value ? 'coach1' : 'coach2') :
    (coach1Value > coach2Value ? 'coach1' : 'coach2');
  
  return (
    <div className="comparison-bar mb-4">
      <div className="label text-xs sm:text-sm text-gray-400 mb-2 font-medium tracking-wide uppercase">{label}</div>
      <div className="flex items-center gap-3 sm:gap-4">
        {/* Coach 1 Value */}
        <div className={`value text-sm sm:text-base font-bold min-w-[50px] sm:min-w-[60px] text-right ${winner === 'coach1' ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(5,150,105,0.8)]' : 'text-white'}`}>
          {coach1Value.toFixed(1)}
        </div>
        
        {/* Bars */}
        <div className="bars flex-1 flex gap-2">
          <div className="bar-container flex-1 bg-gray-800/30 rounded-full h-3 sm:h-4 overflow-hidden relative">
            <div 
              className="bar h-full transition-all duration-1000"
              style={{
                width: `${coach1Pct}%`,
                background: winner === 'coach1' ? 'linear-gradient(90deg, #10b981, #34d399)' : `linear-gradient(90deg, ${coach1Color}, ${coach1Color}cc)`,
                boxShadow: winner === 'coach1' ? '0 0 15px rgba(5,150,105,0.6)' : `0 0 10px ${coach1Color}40`
              }}
            />
          </div>
          <div className="bar-container flex-1 bg-gray-800/30 rounded-full h-3 sm:h-4 overflow-hidden relative">
            <div 
              className="bar h-full transition-all duration-1000"
              style={{
                width: `${coach2Pct}%`,
                background: winner === 'coach2' ? 'linear-gradient(90deg, #10b981, #34d399)' : `linear-gradient(90deg, ${coach2Color}, ${coach2Color}cc)`,
                boxShadow: winner === 'coach2' ? '0 0 15px rgba(5,150,105,0.6)' : `0 0 10px ${coach2Color}40`
              }}
            />
          </div>
        </div>
        
        {/* Coach 2 Value */}
        <div className={`value text-sm sm:text-base font-bold min-w-[50px] sm:min-w-[60px] text-left ${winner === 'coach2' ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(5,150,105,0.8)]' : 'text-white'}`}>
          {coach2Value.toFixed(1)}
        </div>
      </div>
    </div>
  );
};
