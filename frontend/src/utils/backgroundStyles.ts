// Standardized background styles for consistent UI - Midnight Gray Theme
export const backgroundStyles = {
  // Main containers
  glassCard: 'bg-gray-900/95 backdrop-blur-xl border border-gray-400/15 rounded-2xl',
  
  // Inner content containers
  contentContainer: 'bg-gray-800/50 rounded-2xl border border-gray-400/20 backdrop-blur-md',
  
  // Sub-containers and cards
  subContainer: 'bg-gray-700/40 rounded-xl border border-gray-400/15 backdrop-blur-sm',
  
  // Interactive elements
  interactive: 'bg-gray-700/40 hover:bg-gray-600/60 border border-gray-400/15 hover:border-gray-300/25 rounded-lg transition-all duration-300',
  
  // Input elements
  input: 'bg-gray-700/40 border border-gray-400/15 rounded-lg focus:border-gray-300/40 focus:ring-2 focus:ring-gray-300/25',
  
  // Modal overlays
  modal: 'bg-gray-900/95 backdrop-blur-xl border border-gray-400/15 rounded-2xl shadow-2xl',
  
  // Progress bars and metrics
  progressBar: 'bg-gray-700/60 rounded-full overflow-hidden',
  
  // Hover states
  hover: 'hover:bg-gray-700/25 transition-colors',
  
  // Borders
  border: {
    subtle: 'border-gray-400/15',
    medium: 'border-gray-400/25',
    strong: 'border-gray-300/35'
  }
} as const;

// Shadow utilities
export const shadows = {
  card: 'shadow-2xl',
  subtle: 'shadow-lg',
  strong: 'shadow-[0_25px_50px_-12px_rgba(0,0,0,0.6)]'
} as const;

// Backdrop blur utilities
export const backdropBlur = {
  light: 'backdrop-blur-sm',
  medium: 'backdrop-blur-md',
  strong: 'backdrop-blur-xl'
} as const;