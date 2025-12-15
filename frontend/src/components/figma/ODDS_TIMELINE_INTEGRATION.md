# Odds Timeline Integration Guide

## Quick Start

### 1. Install Required Dependencies

```bash
cd frontend
npm install recharts date-fns
```

### 2. Move Historical JSON Files to Public Directory

```bash
# Move your 8 historical JSON files to frontend/public/
mv *.json frontend/public/
```

Files should be:
- `osu_indiana_historical_odds.json`
- `kennesaw_jacksonville_historical_odds.json`
- `jmu_troy_historical_odds.json`
- `duke_virginia_historical_odds.json`
- `georgia_alabama_historical_odds.json`
- `wmu_miami_oh_historical_odds.json`
- `byu_texas_tech_historical_odds.json`
- `north_texas_tulane_historical_odds.json`

### 3. Integrate into Existing Dashboard

#### Option A: Add to EVBettingDashboard (Recommended)

In `frontend/src/components/EVBettingDashboard.tsx`:

```tsx
import { GameModal } from './figma/GameModal';

// Add state for selected game
const [selectedGame, setSelectedGame] = useState<Game | null>(null);

// In your game card component, add onClick:
<div
  className="game-card"
  onClick={() => setSelectedGame(game)}
  style={{ cursor: 'pointer' }}
>
  {/* existing card content */}
</div>

// Add modal at the end of your component:
{selectedGame && (
  <GameModal
    isOpen={selectedGame !== null}
    onClose={() => setSelectedGame(null)}
    gameId={selectedGame.id}
    awayTeam={selectedGame.awayTeam}
    homeTeam={selectedGame.homeTeam}
    awayRank={selectedGame.awayRank}
    homeRank={selectedGame.homeRank}
  />
)}
```

#### Option B: Use Hook Directly in Custom Component

```tsx
import { useOddsTimeline } from '../hooks/useOddsTimeline';
import { OddsTimelineChart } from './figma/OddsTimelineChart';

function MyGameComponent() {
  const { timeline, refresh } = useOddsTimeline({
    gameId: 'osu_indiana',
    awayTeam: 'Indiana',
    homeTeam: 'Ohio State',
    isModalOpen: true,
  });

  return (
    <OddsTimelineChart
      data={timeline.data}
      lastUpdated={timeline.lastUpdated}
      isLoading={timeline.isLoading}
      error={timeline.error}
      onRefresh={refresh}
      awayTeam="Indiana"
      homeTeam="Ohio State"
    />
  );
}
```

## How It Works

### Data Flow

```
1. Modal Opens
   ↓
2. useOddsTimeline hook initializes
   ↓
3. Load from localStorage (if exists)
   ↓
4. Load historical JSON file
   ↓
5. Fetch live data from Action Network API
   ↓
6. Merge historical + live (dedupe by timestamp + bookId)
   ↓
7. Save to localStorage
   ↓
8. Render OddsTimelineChart
   ↓
9. Poll API every 3 minutes
   ↓
10. Update chart in real-time
```

### File Mapping

The hook automatically maps team names to JSON files:

```tsx
const GAME_FILE_MAP = {
  'osu_indiana': 'osu_indiana_historical_odds.json',
  'kennesaw_jacksonville': 'kennesaw_jacksonville_historical_odds.json',
  // ... etc
};
```

Team names are normalized:
- Lowercase
- Spaces → underscores
- Parentheses removed

Examples:
- "Ohio State" → "ohio_state"
- "Miami (OH)" → "miami_oh"

### localStorage Keys

Data is stored as: `odds_timeline_{gameId}`

Example:
```json
{
  "data": [/* OddsDataPoint[] */],
  "lastUpdated": "2025-12-05T20:47:00Z"
}
```

## Configuration Options

### Hook Options

```tsx
interface UseOddsTimelineOptions {
  gameId: string | number;        // Unique game identifier
  awayTeam: string;               // Away team name
  homeTeam: string;               // Home team name
  isModalOpen: boolean;           // Controls hook activation
  pollInterval?: number;          // Default: 180000 (3 min)
  enablePolling?: boolean;        // Default: true
}
```

### Customize Polling

```tsx
const { timeline } = useOddsTimeline({
  gameId: 'my_game',
  awayTeam: 'Team A',
  homeTeam: 'Team B',
  isModalOpen: true,
  pollInterval: 60000,  // Poll every 1 minute
  enablePolling: true,  // Set to false to disable
});
```

### Manual Control

```tsx
const { timeline, refresh, clearCache, isPolling } = useOddsTimeline({...});

// Manual refresh (skips cache)
await refresh();

// Clear localStorage cache
clearCache();

// Check if polling is active
console.log(isPolling); // true/false
```

## Action Network API Integration

### Update API Endpoint

In `frontend/src/hooks/useOddsTimeline.ts`, update the `fetchLiveOdds` function:

```tsx
const fetchLiveOdds = async (gameId: string | number): Promise<OddsDataPoint[]> => {
  try {
    // REPLACE THIS with your actual Action Network endpoint
    const response = await fetch(`YOUR_API_URL/odds/${gameId}`);

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const data = await response.json();

    // Transform YOUR response format to OddsDataPoint[]
    return data.odds.map((odd: any) => ({
      bookId: odd.bookId,
      spread: odd.spread,
      spreadOdds: odd.spreadOdds,
      total: odd.total,
      totalOdds: odd.totalOdds,
      moneyline: odd.moneyline,
      timestamp: odd.timestamp || new Date().toISOString(),
    }));
  } catch (error) {
    console.error('Error fetching live odds:', error);
    return [];
  }
};
```

### Sample API Response

Expected format from Action Network:

```json
{
  "odds": [
    {
      "bookId": 69,
      "spread": -4.5,
      "spreadOdds": -110,
      "total": 47.5,
      "totalOdds": -110,
      "moneyline": -200,
      "timestamp": "2025-12-05T20:47:00Z"
    }
  ]
}
```

## Chart Customization

### Sportsbook Colors

Edit `frontend/src/components/figma/OddsTimelineChart.tsx`:

```tsx
const BOOK_COLORS: Record<number, string> = {
  15: '#2563eb',  // FanDuel - Blue
  68: '#7c3aed',  // Caesars - Purple
  69: '#dc2626',  // DraftKings - Red
  71: '#059669',  // BetMGM - Green
  75: '#ea580c',  // Fanatics - Orange
  30: '#ca8a04',  // Bovada - Yellow
  // Add your custom sportsbook colors
};
```

### Sportsbook Names

```tsx
const SPORTSBOOK_NAMES: Record<number, string> = {
  15: 'FanDuel',
  68: 'Caesars',
  69: 'DraftKings',
  71: 'BetMGM',
  75: 'Fanatics',
  30: 'Bovada',
  // Add your custom sportsbooks
};
```

## Error Handling

The hook provides comprehensive error handling:

```tsx
const { timeline } = useOddsTimeline({...});

if (timeline.error) {
  console.error('Error:', timeline.error);
  // Show error message to user
}

if (timeline.isLoading) {
  // Show loading state
}

if (timeline.data.length === 0) {
  // No data available
}
```

## Performance Optimization

### Cleanup on Modal Close

The hook automatically:
- Stops polling when `isModalOpen = false`
- Clears intervals on unmount
- Prevents state updates after unmount

### Caching Strategy

1. First load: Check localStorage → Load historical JSON → Fetch live API
2. Subsequent loads: Use cached data while fetching updates
3. Manual refresh: Bypass cache, reload everything

### Memory Management

- Historical data loaded only once per mount
- Merged data replaces previous state (no accumulation)
- localStorage limited to latest merged dataset

## Troubleshooting

### Chart Not Showing

1. Check console for errors
2. Verify JSON files are in `frontend/public/`
3. Confirm team names match mapping

### No Historical Data

Add custom mapping in hook:

```tsx
const GAME_FILE_MAP: Record<string, string> = {
  'your_game_key': 'your_historical_file.json',
};
```

### API Not Polling

1. Check `enablePolling` is true
2. Verify `isModalOpen` is true
3. Check network tab for API calls

### Duplicate Data Points

The merge function deduplicates by `timestamp + bookId`:

```tsx
const key = `${item.timestamp}_${item.bookId}`;
```

Ensure your API returns consistent timestamps.

## TypeScript Types

All types are exported from the hook:

```tsx
import { OddsDataPoint, OddsTimeline } from '../hooks/useOddsTimeline';

const myData: OddsDataPoint[] = [
  {
    bookId: 69,
    spread: -4.5,
    spreadOdds: -110,
    total: 47.5,
    totalOdds: -110,
    moneyline: -200,
    timestamp: '2025-12-05T20:47:00Z',
  }
];
```

## Testing

### Test with Mock Data

```tsx
// In your component
const mockTimeline = {
  data: [...],
  lastUpdated: new Date().toISOString(),
  isLoading: false,
  error: null,
};

<OddsTimelineChart {...mockTimeline} />
```

### Test Polling

Set short interval for testing:

```tsx
const { timeline } = useOddsTimeline({
  pollInterval: 5000, // 5 seconds for testing
  // ... other options
});
```

## Production Checklist

- [ ] All 8 JSON files in `frontend/public/`
- [ ] Action Network API endpoint configured
- [ ] API response transformer working
- [ ] Sportsbook colors/names customized
- [ ] Error handling tested
- [ ] Polling interval set correctly
- [ ] localStorage keys unique per game
- [ ] Chart rendering on all screen sizes
- [ ] Modal close cleanup verified

## Support

For issues or questions, check:
1. Browser console for errors
2. Network tab for API calls
3. localStorage for cached data
4. This integration guide

Happy betting! 🎲
