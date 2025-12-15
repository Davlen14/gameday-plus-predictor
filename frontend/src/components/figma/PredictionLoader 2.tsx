import React from 'react';

interface PredictionLoaderProps {
  homeTeam?: {
    name: string;
    logo: string;
    color: string;
  };
  awayTeam?: {
    name: string;
    logo: string;
    color: string;
  };
}

export function PredictionLoader({ homeTeam, awayTeam }: PredictionLoaderProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-xl bg-black/60 animate-in fade-in duration-300">
      <div className="relative">
        {/* Main container */}
        <div className="flex items-center gap-8 md:gap-16">
          {/* Away Team Logo */}
          <div className="relative group">
            <div 
              className="absolute inset-0 rounded-full blur-2xl opacity-60 animate-pulse"
              style={{ 
                background: awayTeam?.color || '#3b82f6',
                animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
              }}
            />
            <div 
              className="relative w-32 h-32 md:w-40 md:h-40 rounded-full flex items-center justify-center backdrop-blur-sm border-4 shadow-2xl animate-in zoom-in-50 duration-500"
              style={{
                borderColor: awayTeam?.color || '#3b82f6',
                background: `radial-gradient(circle, ${awayTeam?.color}15, transparent)`,
                animation: 'float 3s ease-in-out infinite'
              }}
            >
              {awayTeam?.logo ? (
                <img 
                  src={awayTeam.logo} 
                  alt={awayTeam.name}
                  className="w-24 h-24 md:w-32 md:h-32 object-contain drop-shadow-2xl"
                  style={{
                    filter: 'drop-shadow(0 0 20px rgba(255,255,255,0.3))',
                    animation: 'logoSpin 4s ease-in-out infinite'
                  }}
                />
              ) : (
                <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 animate-pulse" />
              )}
            </div>
            {awayTeam?.name && (
              <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                <div className="text-white font-semibold text-sm md:text-base tracking-wide backdrop-blur-sm px-4 py-1 rounded-full border border-white/20">
                  {awayTeam.name}
                </div>
              </div>
            )}
          </div>

          {/* VS Divider with Lightning Animation */}
          <div className="relative flex flex-col items-center gap-4">
            {/* Lightning bolt animation */}
            <div className="absolute inset-0 flex items-center justify-center">
              <svg width="60" height="100" viewBox="0 0 60 100" className="animate-pulse">
                <defs>
                  <linearGradient id="lightning" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#fbbf24', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#f59e0b', stopOpacity: 1 }} />
                  </linearGradient>
                </defs>
                <path 
                  d="M 30 10 L 20 45 L 35 45 L 25 85 L 45 40 L 30 40 Z" 
                  fill="url(#lightning)"
                  className="opacity-20"
                  style={{
                    animation: 'flash 1.5s ease-in-out infinite'
                  }}
                />
              </svg>
            </div>

            {/* VS Text */}
            <div className="relative z-10">
              <div 
                className="text-6xl md:text-7xl font-black italic tracking-tighter"
                style={{
                  fontFamily: 'Orbitron, system-ui',
                  background: 'linear-gradient(135deg, #C0C0C0, #E5E5E5, #A9A9A9, #D3D3D3)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                  textShadow: '0 0 40px rgba(255,255,255,0.3)',
                  animation: 'glow 2s ease-in-out infinite'
                }}
              >
                VS
              </div>
            </div>

            {/* Spinning rings */}
            <svg className="absolute inset-0 w-full h-full" style={{ animation: 'spin 8s linear infinite' }}>
              <circle cx="50%" cy="50%" r="60" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
            </svg>
            <svg className="absolute inset-0 w-full h-full" style={{ animation: 'spin-reverse 6s linear infinite' }}>
              <circle cx="50%" cy="50%" r="70" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="1" strokeDasharray="4 4" />
            </svg>
          </div>

          {/* Home Team Logo */}
          <div className="relative group">
            <div 
              className="absolute inset-0 rounded-full blur-2xl opacity-60 animate-pulse"
              style={{ 
                background: homeTeam?.color || '#8b5cf6',
                animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite 0.5s'
              }}
            />
            <div 
              className="relative w-32 h-32 md:w-40 md:h-40 rounded-full flex items-center justify-center backdrop-blur-sm border-4 shadow-2xl animate-in zoom-in-50 duration-500 delay-150"
              style={{
                borderColor: homeTeam?.color || '#8b5cf6',
                background: `radial-gradient(circle, ${homeTeam?.color}15, transparent)`,
                animation: 'float 3s ease-in-out infinite 0.5s'
              }}
            >
              {homeTeam?.logo ? (
                <img 
                  src={homeTeam.logo} 
                  alt={homeTeam.name}
                  className="w-24 h-24 md:w-32 md:h-32 object-contain drop-shadow-2xl"
                  style={{
                    filter: 'drop-shadow(0 0 20px rgba(255,255,255,0.3))',
                    animation: 'logoSpin 4s ease-in-out infinite 0.5s'
                  }}
                />
              ) : (
                <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 animate-pulse" />
              )}
            </div>
            {homeTeam?.name && (
              <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                <div className="text-white font-semibold text-sm md:text-base tracking-wide backdrop-blur-sm px-4 py-1 rounded-full border border-white/20">
                  {homeTeam.name}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Loading text */}
        <div className="absolute -bottom-20 left-1/2 transform -translate-x-1/2 text-center whitespace-nowrap">
          <div className="text-white text-lg md:text-xl font-semibold mb-2 flex items-center gap-3">
            <div className="flex gap-1">
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
            <span className="font-mono">Analyzing matchup</span>
            <div className="flex gap-1">
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
          <div className="text-slate-400 text-sm font-mono">Running prediction engine...</div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{__html: `
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        
        @keyframes logoSpin {
          0%, 100% { transform: rotateY(0deg); }
          50% { transform: rotateY(360deg); }
        }
        
        @keyframes glow {
          0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.3); }
          50% { text-shadow: 0 0 40px rgba(255,255,255,0.6); }
        }
        
        @keyframes flash {
          0%, 100% { opacity: 0.2; }
          50% { opacity: 0.8; }
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes spin-reverse {
          from { transform: rotate(360deg); }
          to { transform: rotate(0deg); }
        }
      `}} />
    </div>
  );
}
