import React from 'react';
import type { RankCategory } from '../../types/coaching.types';

interface RankBadgeProps {
  rank: number;
  score: number;
}

export const getRankCategory = (rank: number): RankCategory => {
  if (rank <= 5) return { 
    label: 'Elite', 
    color: 'from-yellow-400 to-yellow-600', 
    icon: '👑' 
  };
  if (rank <= 15) return { 
    label: 'Top Tier', 
    color: 'from-blue-400 to-blue-600', 
    icon: '⭐' 
  };
  if (rank <= 30) return { 
    label: 'Rising Star', 
    color: 'from-green-400 to-green-600', 
    icon: '🚀' 
  };
  if (rank <= 50) return { 
    label: 'Solid', 
    color: 'from-purple-400 to-purple-600', 
    icon: '💪' 
  };
  return { 
    label: 'Developing', 
    color: 'from-gray-400 to-gray-600', 
    icon: '📈' 
  };
};

export const RankBadge: React.FC<RankBadgeProps> = ({ rank, score }) => {
  const category = getRankCategory(rank);
  
  return (
    <div className="flex items-center gap-4">
      <div 
        className={`bg-gradient-to-r ${category.color} px-4 py-2 rounded-full font-bold text-sm text-white shadow-lg`}
        style={{
          textShadow: '0 2px 4px rgba(0,0,0,0.3)'
        }}
      >
        {category.icon} #{rank} {category.label}
      </div>
      <span className="text-white font-bold text-lg">
        {score.toFixed(1)}/100
      </span>
    </div>
  );
};
