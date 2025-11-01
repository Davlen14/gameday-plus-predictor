import { useState, useRef } from 'react';
import { createPortal } from 'react-dom';
import { GlassCard } from './GlassCard';
import { Info, ChevronDown, ChevronUp, Search, X } from 'lucide-react';
import { useClickOutside } from "../../hooks/useClickOutside";

// Portal Modal Component
const PortalModal = ({ children, isOpen }: { children: React.ReactNode; isOpen: boolean }) => {
  if (!isOpen) return null;
  
  return createPortal(
    children,
    document.body
  );
};

const glossaryItems = [
  {
    title: 'EPA (Expected Points Added)',
    description: 'Measures the value of each play in terms of expected points. Positive EPA means the offense gained more points than expected, negative means the defense prevented points.',
    color: 'cyan'
  },
  {
    title: 'Success Rate',
    description: 'Percentage of plays that achieve at least 50% of needed yards on 1st down, 70% on 2nd down, or 100% on 3rd/4th down. Measures consistent offensive execution.',
    color: 'emerald'
  },
  {
    title: 'Explosiveness',
    description: 'Average EPA per successful play. Measures big-play ability and how explosive an offense is when they succeed.',
    color: 'orange'
  },
  {
    title: 'Havoc Rate',
    description: 'Percentage of plays where the defense creates a tackle for loss, forces a fumble, or defends a pass. Measures disruptive plays.',
    color: 'red'
  },
  {
    title: 'Stuff Rate',
    description: 'Percentage of running plays that are stopped at or before the line of scrimmage. Indicates defensive line dominance.',
    color: 'purple'
  },
  {
    title: 'Line Yards',
    description: 'Average yards before contact on running plays. Measures offensive line effectiveness independent of running back skill.',
    color: 'amber'
  },
  {
    title: 'Second Level Yards',
    description: 'Average yards gained 5-10 yards downfield. Measures linebacker and safety coverage effectiveness.',
    color: 'blue'
  },
  {
    title: 'Open Field Yards',
    description: 'Average yards gained 11+ yards downfield. Indicates ability to break tackles and create big plays in space.',
    color: 'green'
  },
  {
    title: 'Highlight Yards',
    description: 'Average yards on plays of 20+ yards. Measures explosive play efficiency and breakaway ability.',
    color: 'yellow'
  },
  {
    title: 'ELO Rating',
    description: 'Chess-style rating system that updates based on game results and opponent strength. Higher numbers indicate stronger teams.',
    color: 'indigo'
  },
  {
    title: 'FPI (Football Power Index)',
    description: 'ESPN\'s team efficiency metric that predicts how many points above average a team would score/allow vs average opponent.',
    color: 'cyan'
  },
  {
    title: 'Talent Rating',
    description: 'Composite recruiting rating based on player talent level. Measures the raw talent differential between teams.',
    color: 'pink'
  },
  {
    title: 'PPA (Predicted Points Added)',
    description: 'Alternative to EPA that uses down/distance/field position to predict point value of each play situation.',
    color: 'teal'
  },
  {
    title: 'Standard Downs',
    description: '1st down, 2nd and short (≤7 yards), 3rd/4th and short (≤4 yards). Measures base offensive efficiency.',
    color: 'emerald'
  },
  {
    title: 'Passing Downs',
    description: '2nd and long (8+ yards), 3rd/4th and long (5+ yards). Measures clutch performance in obvious passing situations.',
    color: 'blue'
  },
  {
    title: 'Power Success',
    description: 'Success rate on short-yardage situations (3rd/4th down & 2 yards or less). Measures goal-line and conversion efficiency.',
    color: 'red'
  },
  {
    title: 'Red Zone Efficiency',
    description: 'Scoring percentage when reaching the 20-yard line. Critical measure of finishing drives.',
    color: 'orange'
  },
  {
    title: 'Turnover Margin',
    description: 'Difference between turnovers forced and turnovers lost. Strong predictor of game outcomes.',
    color: 'purple'
  },
  {
    title: 'Three & Outs',
    description: 'Drives ending in 3 plays or less. Measures offensive struggles and defensive effectiveness.',
    color: 'gray'
  },
  {
    title: 'Time of Possession',
    description: 'Minutes controlling the ball. Indicates game control and ability to sustain drives.',
    color: 'amber'
  },
  {
    title: 'Platt Scaling',
    description: 'Statistical method that calibrates raw probabilities to improve accuracy based on historical prediction performance.',
    color: 'indigo'
  },
  {
    title: 'Market Signal',
    description: 'Strength of betting market consensus. Values >1.5 indicate strong market agreement, <1.0 suggests uncertainty.',
    color: 'cyan'
  },
  {
    title: 'Value Bet',
    description: 'When the model disagrees significantly with market odds, creating potential betting value.',
    color: 'green'
  },
  {
    title: 'Consensus Spread',
    description: 'Average point spread across multiple sportsbooks. Shows market expectations.',
    color: 'blue'
  },
  {
    title: 'Implied Probability',
    description: 'Probability suggested by betting odds. Converts odds into percentage chance of outcome.',
    color: 'teal'
  },
  {
    title: 'EPA Defense',
    description: 'Expected points prevented per play by defense. Negative numbers are better for defense.',
    color: 'red'
  },
  {
    title: 'Explosive Defense',
    description: 'Rate of allowing 15+ yard passing or 10+ yard rushing plays. Lower is better.',
    color: 'purple'
  },
  {
    title: 'Drive Efficiency',
    description: 'Average points scored per drive. Measures ability to convert possessions into points.',
    color: 'orange'
  },
  {
    title: 'Quick Scores',
    description: 'Drives of 4 plays or less resulting in scores. Shows big-play capability.',
    color: 'yellow'
  },
  {
    title: 'Methodical Drives',
    description: 'Drives of 10+ plays showing sustained execution and ball control.',
    color: 'emerald'
  },
  {
    title: 'Opponent-Adjusted',
    description: 'Statistics adjusted for strength of opponents faced. Provides context for raw numbers.',
    color: 'indigo'
  },
  {
    title: 'Strength of Schedule (SoS)',
    description: 'Difficulty rating of opponents played. Higher numbers indicate tougher schedules.',
    color: 'gray'
  },
  {
    title: 'Home Field Advantage',
    description: 'Statistical boost given to home teams, typically 2.5-3 points in college football.',
    color: 'amber'
  },
  {
    title: 'Player Impact Rating',
    description: 'Individual player\'s contribution to team success measured through advanced metrics.',
    color: 'pink'
  },
  {
    title: 'Win Probability',
    description: 'The model\'s calculated probability of each team winning based on all available metrics and historical data.',
    color: 'cyan'
  }
];

interface GlossaryProps {
  predictionData?: any;
}

export function Glossary({ predictionData }: GlossaryProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const modalRef = useRef<HTMLDivElement>(null);

  useClickOutside(modalRef, () => {
    setIsOpen(false);
    setSearchTerm('');
  });

  const filteredItems = glossaryItems.filter(item =>
    item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <GlassCard className="p-6">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between text-left hover:opacity-80 transition-opacity"
        >
          <h3 className="text-white font-semibold flex items-center gap-2">
            <Info className="w-5 h-5 text-cyan-400" />
            Metrics Glossary ({glossaryItems.length} terms)
          </h3>
          <ChevronDown className="w-5 h-5 text-cyan-400" />
        </button>
      </GlassCard>

      {/* Portal Modal */}
      <PortalModal isOpen={isOpen}>
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-2 sm:p-4 z-50"
          onClick={() => setIsOpen(false)}
          style={{ 
            zIndex: 999999,
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            width: '100vw',
            height: '100vh'
          }}
        >
          <div 
            ref={modalRef}
            className="bg-slate-900/98 backdrop-blur-xl border border-white/20 rounded-lg shadow-2xl w-full max-w-[95vw] sm:w-[90vw] h-[90vh] sm:h-[85vh] flex flex-col animate-in fade-in zoom-in-95 duration-200"
            onClick={(e) => e.stopPropagation()}
            style={{ 
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.8)', 
              zIndex: 1000000,
              position: 'relative',
              maxWidth: '1400px',
              maxHeight: '900px'
            }}
          >
            <div className="p-4 sm:p-6 border-b border-white/10 flex-shrink-0">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <h3 className="text-white font-semibold text-xl sm:text-2xl flex items-center gap-2">
                  <Info className="w-7 h-7 text-cyan-400" />
                  Metrics Glossary ({filteredItems.length} of {glossaryItems.length} terms)
                </h3>
                <button 
                  onClick={() => setIsOpen(false)}
                  className="text-slate-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/10"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search glossary terms..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-slate-800/60 border border-white/10 rounded-lg pl-12 pr-4 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/40 focus:border-cyan-500/40 text-lg"
                  autoFocus
                />
              </div>
            </div>
            <div 
              className="flex-1 p-6 overflow-y-auto" 
              style={{ 
                zIndex: 1000001,
                position: 'relative'
              }}
            >
              <div 
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 pb-4" 
                style={{ 
                  zIndex: 1000002,
                  position: 'relative'
                }}
              >
                {filteredItems.map((item, index) => (
                  <GlossaryItem key={index} {...item} />
                ))}
              </div>
              {filteredItems.length === 0 && (
                <div className="col-span-full text-center py-12">
                  <div className="text-slate-400 text-xl mb-2">No terms found</div>
                  <div className="text-slate-500 text-base">Try adjusting your search terms</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </PortalModal>
    </>
  );
}

function GlossaryItem({ title, description, color }: { title: string; description: string; color: string }) {
  const colors: Record<string, string> = {
    cyan: 'border-cyan-400/40 hover:border-cyan-400/70',
    blue: 'border-blue-400/40 hover:border-blue-400/70',
    purple: 'border-purple-400/40 hover:border-purple-400/70',
    emerald: 'border-emerald-400/40 hover:border-emerald-400/70',
    amber: 'border-amber-400/40 hover:border-amber-400/70',
    red: 'border-red-400/40 hover:border-red-400/70',
    orange: 'border-orange-400/40 hover:border-orange-400/70',
    green: 'border-green-400/40 hover:border-green-400/70',
    yellow: 'border-yellow-400/40 hover:border-yellow-400/70',
    indigo: 'border-indigo-400/40 hover:border-indigo-400/70',
    pink: 'border-pink-400/40 hover:border-pink-400/70',
    teal: 'border-teal-400/40 hover:border-teal-400/70',
    gray: 'border-gray-400/40 hover:border-gray-400/70'
  };

  const textColors: Record<string, string> = {
    cyan: 'text-cyan-300',
    blue: 'text-blue-300',
    purple: 'text-purple-300',
    emerald: 'text-emerald-300',
    amber: 'text-amber-300',
    red: 'text-red-300',
    orange: 'text-orange-300',
    green: 'text-green-300',
    yellow: 'text-yellow-300',
    indigo: 'text-indigo-300',
    pink: 'text-pink-300',
    teal: 'text-teal-300',
    gray: 'text-gray-300'
  };

  const bgColors: Record<string, string> = {
    cyan: 'bg-cyan-500/10 hover:bg-cyan-500/20',
    blue: 'bg-blue-500/10 hover:bg-blue-500/20',
    purple: 'bg-purple-500/10 hover:bg-purple-500/20',
    emerald: 'bg-emerald-500/10 hover:bg-emerald-500/20',
    amber: 'bg-amber-500/10 hover:bg-amber-500/20',
    red: 'bg-red-500/10 hover:bg-red-500/20',
    orange: 'bg-orange-500/10 hover:bg-orange-500/20',
    green: 'bg-green-500/10 hover:bg-green-500/20',
    yellow: 'bg-yellow-500/10 hover:bg-yellow-500/20',
    indigo: 'bg-indigo-500/10 hover:bg-indigo-500/20',
    pink: 'bg-pink-500/10 hover:bg-pink-500/20',
    teal: 'bg-teal-500/10 hover:bg-teal-500/20',
    gray: 'bg-gray-500/10 hover:bg-gray-500/20'
  };

  return (
    <div className={`${bgColors[color]} rounded-lg p-5 border backdrop-blur-sm transition-all duration-300 ${colors[color]} group cursor-default shadow-lg hover:shadow-xl`}>
      <h4 className={`${textColors[color]} font-bold text-lg mb-3 group-hover:scale-105 transition-transform drop-shadow-sm`}>{title}</h4>
      <p className="text-slate-100 text-base leading-relaxed font-medium">{description}</p>
    </div>
  );
}