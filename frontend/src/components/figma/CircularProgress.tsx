import React from 'react';

interface CircularProgressProps {
  value: number;
  size?: number;
  strokeWidth?: number;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({ 
  value, 
  size = 60, 
  strokeWidth = 6 
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;
  
  const getColor = (val: number) => {
    if (val >= 80) return '#22c55e'; // green
    if (val >= 60) return '#3b82f6'; // blue
    if (val >= 40) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };
  
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg className="transform -rotate-90" width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255,255,255,0.1)"
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={getColor(value)}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            // transition removed
          }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-xs font-bold text-white">
          {value.toFixed(0)}
        </span>
      </div>
    </div>
  );
};
