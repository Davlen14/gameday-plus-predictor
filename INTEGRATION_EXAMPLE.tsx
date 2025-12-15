/**
 * INTEGRATION GUIDE: Add Odds Timeline to Your Existing Modal
 *
 * This file shows EXACTLY how to integrate the odds timeline chart
 * into your existing EVBettingDashboard modal.
 */

// ============================================================================
// STEP 1: Add imports at the top of EVBettingDashboard.tsx
// ============================================================================

import { useOddsTimeline } from '../hooks/useOddsTimeline';
import { OddsTimelineChart } from './figma/OddsTimelineChart';

// ============================================================================
// STEP 2: Inside your EVBettingDashboard component, add the hook
// ============================================================================

const EVBettingDashboard: React.FC<EVBettingDashboardProps> = ({ onBack }) => {
  // ... your existing state ...
  const [selectedGame, setSelectedGame] = useState<Game | null>(null);

  // 👇 ADD THIS: Odds timeline hook
  const { timeline, refresh, isPolling } = useOddsTimeline({
    gameId: selectedGame?.id || '',
    awayTeam: selectedGame?.awayTeam || '',
    homeTeam: selectedGame?.homeTeam || '',
    isModalOpen: selectedGame !== null,
    pollInterval: 180000, // 3 minutes
    enablePolling: true,
  });

  // ... rest of your component ...

// ============================================================================
// STEP 3: Find your modal section (around line 1137) and ADD the timeline
// ============================================================================

// Your existing modal code:
{selectedGame && (
  <div className="modal-overlay" onClick={() => setSelectedGame(null)}>
    <div className="modal-content" onClick={(e) => e.stopPropagation()}>

      {/* Your existing modal header */}
      <div className="modal-header">
        {/* ... existing header content ... */}
      </div>

      <div className="modal-body">

        {/* 👇 ADD THIS NEW SECTION - Right after modal-body opens */}
        <div className="modal-section">
          <OddsTimelineChart
            data={timeline.data}
            lastUpdated={timeline.lastUpdated}
            isLoading={timeline.isLoading}
            error={timeline.error}
            onRefresh={refresh}
            awayTeam={selectedGame.awayTeam}
            homeTeam={selectedGame.homeTeam}
          />
        </div>
        {/* 👆 END NEW SECTION */}

        {/* Your existing modal sections below */}
        <div className="modal-section">
          <h3 className="modal-section-title">
            {/* ... your existing content ... */}
          </h3>
        </div>

        {/* ... rest of your modal ... */}
      </div>
    </div>
  </div>
)}

// ============================================================================
// STEP 4: Add CSS styling to EVBettingDashboard.css
// ============================================================================

/* Add this at the bottom of EVBettingDashboard.css */

.modal-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

/* Ensure modal content is scrollable */
.modal-content {
  max-height: 90vh;
  overflow-y: auto;
}

.modal-body {
  padding: 1.5rem;
}

// ============================================================================
// STEP 5: Install dependencies
// ============================================================================

/**
 * Run in terminal:
 *
 * cd frontend
 * npm install recharts date-fns
 */

// ============================================================================
// STEP 6: Move your JSON files
// ============================================================================

/**
 * Move all 8 historical JSON files to frontend/public/:
 *
 * mv osu_indiana_historical_odds.json frontend/public/
 * mv kennesaw_jacksonville_historical_odds.json frontend/public/
 * mv jmu_troy_historical_odds.json frontend/public/
 * mv duke_virginia_historical_odds.json frontend/public/
 * mv georgia_alabama_historical_odds.json frontend/public/
 * mv wmu_miami_oh_historical_odds.json frontend/public/
 * mv byu_texas_tech_historical_odds.json frontend/public/
 * mv north_texas_tulane_historical_odds.json frontend/public/
 */

// ============================================================================
// THAT'S IT! Your modal now has:
// ============================================================================

/**
 * ✅ Historical odds baseline loaded from JSON
 * ✅ Live API polling every 3 minutes
 * ✅ Automatic merge without duplicates
 * ✅ localStorage persistence
 * ✅ Beautiful timeline chart with spread movement
 * ✅ Automatic cleanup when modal closes
 * ✅ Manual refresh button
 * ✅ Loading and error states
 * ✅ Sportsbook-specific colors
 * ✅ Opening vs current spread comparison
 */

// ============================================================================
// OPTIONAL: Customize the Action Network API endpoint
// ============================================================================

/**
 * In frontend/src/hooks/useOddsTimeline.ts, find fetchLiveOdds function
 * and update the API URL to match your Action Network endpoint:
 *
 * const response = await fetch(`YOUR_API_URL/odds/${gameId}`);
 */

export {};
