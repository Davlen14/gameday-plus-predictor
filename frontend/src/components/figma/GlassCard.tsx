import { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  glowColor?: string;
}

export function GlassCard({ children, className = '', glowColor }: GlassCardProps) {
  return (
    <div className="relative group">
      {glowColor && (
        <div className={`absolute -inset-1 bg-gradient-to-br ${glowColor} rounded-xl blur-2xl opacity-60 group-hover:opacity-90 transition-all duration-500`}></div>
      )}
      <div 
        className={`relative overflow-hidden bg-slate-900/98 backdrop-blur-xl border border-white/20 rounded-lg transition-all duration-300 ${className}`}
        style={{ 
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)',
        }}
      >
        <div className="relative z-10">
          {children}
        </div>
      </div>
    </div>
  );
}
