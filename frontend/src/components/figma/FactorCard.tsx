import React from 'react';
import { CircularProgress } from './CircularProgress';
import type { FactorStat } from '../../types/coaching.types';

interface FactorCardProps {
  title: string;
  weight: string;
  rating: number;
  icon: string | React.ReactNode;
  stats: FactorStat[];
  badge?: string;
}

export const FactorCard: React.FC<FactorCardProps> = ({ 
  title, 
  weight, 
  rating, 
  icon, 
  stats, 
  badge 
}) => {
  return (
    <div 
      className="relative overflow-hidden rounded-lg p-4 transition-all duration-300 hover:scale-[1.02]"
      style={{
        background: 'rgba(15, 23, 42, 0.2)'
      }}
    >
      {/* Header with Icon and Title */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-2.5">
          <div className="flex-shrink-0">
            {typeof icon === 'string' ? (
              <span className="text-2xl">{icon}</span>
            ) : (
              <div className="p-1.5 rounded-lg" style={{ background: 'rgba(148, 163, 184, 0.1)' }}>
                {icon}
              </div>
            )}
          </div>
          <div>
            <h4 className="font-semibold text-white text-sm leading-tight">{title}</h4>
            <span className="text-xs text-gray-400 font-medium tracking-wide">Weight: {weight}</span>
          </div>
        </div>
        <div className="rating flex-shrink-0">
          <CircularProgress value={rating} size={48} />
        </div>
      </div>
      
      {/* Badge */}
      {badge && (
        <div className="mb-3 inline-block">
          <div 
            className="text-xs font-medium rounded px-2.5 py-1"
            style={{
              background: 'rgba(148, 163, 184, 0.12)',
              color: 'rgba(255, 255, 255, 0.9)'
            }}
          >
            {badge}
          </div>
        </div>
      )}
      
      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat, idx) => (
          <div key={idx} className="stat">
            <div className="text-xs text-gray-400 mb-1 font-medium tracking-wide uppercase">{stat.label}</div>
            <div className={`text-sm font-bold leading-tight ${stat.className || 'text-white'}`}>
              {stat.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
