import { ReactNode } from 'react';

interface ClearGlassCardProps {
  children: ReactNode;
  className?: string;
}

export function ClearGlassCard({ children, className = '' }: ClearGlassCardProps) {
  return (
    <div className="relative group">
      <div 
        className={`relative overflow-hidden rounded-xl transition-all duration-300 hover:scale-[1.01] ${className}`}
        style={{ 
          background: 'transparent',
          border: '1px solid rgba(148, 163, 184, 0.12)',
          boxShadow: 'none',
          backdropFilter: 'none'
        }}
      >
        <div className="relative z-10">
          {children}
        </div>
      </div>
    </div>
  );
}
