import React from 'react';
import EVBettingDashboard from '../EVBettingDashboard';

interface EVPlusPageProps {
  onBack: () => void;
}

export const EVPlusPage: React.FC<EVPlusPageProps> = ({ onBack }) => {
  return (
    <div className="min-h-screen relative overflow-hidden" style={{
      background: `
        linear-gradient(135deg, #050506 0%, #0a0a0b 25%, #060607 50%, #080809 75%, #050506 100%),
        radial-gradient(ellipse at top left, rgba(12, 12, 14, 0.3), transparent 50%),
        radial-gradient(ellipse at bottom right, rgba(10, 10, 12, 0.3), transparent 50%),
        linear-gradient(180deg, #070708 0%, #030304 100%)
      `
    }}>
      {/* Grid Pattern and Red Gradient Overlays - Exact Week14 Style */}
      <div 
        className="fixed inset-0 pointer-events-none"
        style={{
          backgroundImage: `
            repeating-linear-gradient(
              0deg,
              transparent,
              transparent 0.5px,
              rgba(255, 255, 255, 0.025) 0.5px,
              rgba(255, 255, 255, 0.025) 1px
            ),
            repeating-linear-gradient(
              90deg,
              transparent,
              transparent 0.5px,
              rgba(255, 255, 255, 0.025) 0.5px,
              rgba(255, 255, 255, 0.025) 1px
            ),
            repeating-linear-gradient(
              45deg,
              rgba(255, 255, 255, 0.02) 0px,
              rgba(255, 255, 255, 0.02) 0.5px,
              transparent 0.5px,
              transparent 4px
            ),
            repeating-linear-gradient(
              -45deg,
              rgba(255, 255, 255, 0.02) 0px,
              rgba(255, 255, 255, 0.02) 0.5px,
              transparent 0.5px,
              transparent 4px
            ),
            repeating-linear-gradient(
              30deg,
              rgba(204, 0, 28, 0.035) 0px,
              rgba(204, 0, 28, 0.035) 1px,
              transparent 1px,
              transparent 16px
            ),
            repeating-linear-gradient(
              -30deg,
              rgba(161, 0, 20, 0.035) 0px,
              rgba(161, 0, 20, 0.035) 1px,
              transparent 1px,
              transparent 16px
            ),
            radial-gradient(
              ellipse at 25% 15%, 
              rgba(204, 0, 28, 0.12) 0%, 
              rgba(161, 0, 20, 0.08) 30%,
              transparent 60%
            ),
            radial-gradient(
              ellipse at 75% 85%, 
              rgba(115, 0, 13, 0.12) 0%, 
              rgba(161, 0, 20, 0.08) 30%,
              transparent 60%
            ),
            radial-gradient(
              circle at 50% 30%, 
              rgba(255, 255, 255, 0.06) 0%, 
              transparent 35%
            ),
            radial-gradient(
              circle at 80% 70%, 
              rgba(204, 0, 28, 0.06) 0%, 
              transparent 25%
            )
          `,
          backgroundSize: `
            1px 1px,
            1px 1px,
            4px 4px,
            4px 4px,
            16px 16px,
            16px 16px,
            800px 800px,
            700px 700px,
            400px 400px,
            300px 300px
          `,
          zIndex: 0
        }}
      />
      
      {/* Content */}
      <div className="relative z-10">
        {/* EV Betting Dashboard */}
        <EVBettingDashboard onBack={onBack} />
      </div>
    </div>
  );
};