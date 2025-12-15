# 🚀 Quick Integration Guide - Add Odds Timeline to Your Modal

## Prerequisites

```bash
cd frontend
npm install recharts date-fns
```

Move JSON files to `frontend/public/`:
```bash
mv *.json frontend/public/
```

---

## Integration Steps

### 1️⃣ Add Imports (Top of EVBettingDashboard.tsx)

```tsx
import { useOddsTimeline } from '../hooks/useOddsTimeline';
import { OddsTimelineChart } from './figma/OddsTimelineChart';
```

### 2️⃣ Add Hook (Inside component, after existing state)

Find this line around **line 593**:
```tsx
const [selectedGame, setSelectedGame] = useState<Game | null>(null);
```

Add RIGHT AFTER IT:
```tsx
// Odds timeline for modal
const { timeline, refresh } = useOddsTimeline({
  gameId: selectedGame?.id || '',
  awayTeam: selectedGame?.awayTeam || '',
  homeTeam: selectedGame?.homeTeam || '',
  isModalOpen: selectedGame !== null,
});
```

### 3️⃣ Add Chart to Modal (Around line 1188)

Find this section in your modal:
```tsx
<div className="modal-body">
  {/* 👇 ADD THE CHART HERE */}

  <div className="modal-section">
```

Replace with:
```tsx
<div className="modal-body">
  {/* 👇 NEW: Odds Timeline Chart */}
  <div className="modal-section" style={{ marginBottom: '2rem' }}>
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

  <div className="modal-section">
```

---

## That's It! ✅

Your modal now shows:
- 📊 Historical spread movement from JSON files
- 🔴 Live odds from Action Network API (polling every 3 minutes)
- 💾 Cached in localStorage
- 📈 Beautiful interactive chart
- 🎨 Color-coded by sportsbook

---

## Testing

1. Click on any game card to open modal
2. You should see the timeline chart at the top
3. Chart shows spread movement over time
4. Chart updates automatically every 3 minutes
5. Click refresh icon to manually update

---

## Customize API (Optional)

Edit `frontend/src/hooks/useOddsTimeline.ts` line 184:

```tsx
const response = await fetch(`/api/action-network/odds/${gameId}`);
```

Change to your actual Action Network endpoint.

---

## Troubleshooting

**Chart not showing?**
- Check browser console for errors
- Verify JSON files are in `frontend/public/`
- Check network tab for API calls

**No historical data?**
- Check team name mapping in hook
- Verify JSON filenames match GAME_FILE_MAP

**API not working?**
- Update fetchLiveOdds URL in hook
- Check API response format matches OddsDataPoint[]

---

## File Structure

```
frontend/
├── public/
│   ├── osu_indiana_historical_odds.json
│   ├── kennesaw_jacksonville_historical_odds.json
│   └── ... (other 6 JSON files)
├── src/
│   ├── hooks/
│   │   └── useOddsTimeline.ts          ✅ Created
│   ├── components/
│   │   ├── EVBettingDashboard.tsx      🔧 Modify
│   │   └── figma/
│   │       └── OddsTimelineChart.tsx   ✅ Created
```

---

## Next Steps

1. Copy-paste the 3 code snippets above
2. Install dependencies
3. Move JSON files
4. Test by clicking a game card
5. Customize sportsbook colors if needed

Done! 🎉
