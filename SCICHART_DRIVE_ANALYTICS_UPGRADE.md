# 🏈 SciChart Drive Analytics Dashboard Upgrade

## 📋 Overview
Transform the current `DriveEfficiency.tsx` component into an interactive multi-chart analytics dashboard using SciChart's grid layout system (inspired by the Server Traffic Dashboard example).

## 🎯 Objective
Replace the current custom spider chart with a professional 5-chart dashboard that displays drive analytics across multiple synchronized visualizations.

---

## 📦 Prerequisites

### 1. Install SciChart Dependencies
```bash
cd frontend
npm install scichart scichart-react
```

### 2. Reference Files
- **Example to follow**: The Server Traffic Dashboard code provided (with grid layout, synchronized cursors, and chart grouping)
- **Current component**: `frontend/src/components/figma/DriveEfficiency.tsx`
- **Data source**: API returns `drive_analytics` object with:
  - `quarter_data`: Array of Q1-Q4 with `scoringPct`, `drives`, `scored`
  - `field_position_data`: Array of 4 zones with `scoringPct`, `drives`, `scored`
  - `drive_outcomes`: Object with `touchdowns`, `fieldGoals`, `punts`, `turnovers`, `totalScoring` (all percentages)

---

## 🏗️ Implementation Steps

### Step 1: Create Chart Configuration Files

Create these new files in `frontend/src/components/figma/drive-analytics/`:

#### **`quarter-performance-config.ts`**
```typescript
// Main timeline chart showing Q1-Q4 scoring efficiency over time
// Chart Type: Line/Area chart with two series (home vs away)
// X-Axis: Quarters (Q1, Q2, Q3, Q4)
// Y-Axis: Scoring % (0-100)
// Features: Cursor modifier, tooltip, zoom/pan
```

#### **`field-position-config.ts`**
```typescript
// Stacked/Grouped bar chart showing scoring rates by field position
// Chart Type: Horizontal stacked bar chart
// Categories: Own 1-20, Own 21-40, Own 41-Mid, Opp Territory
// Series: Home team, Away team
// Y-Axis: Scoring percentage
```

#### **`drive-flow-config.ts`**
```typescript
// Real-time drive flow showing sequential drive outcomes
// Chart Type: Scatter/bubble chart or waterfall chart
// X-Axis: Drive number (sequential)
// Y-Axis: Outcome type (TD=7, FG=3, Punt=0, Turnover=-1)
// Features: Grid layout toggle for individual game drives
```

#### **`drive-outcomes-config.ts`**
```typescript
// Column chart comparing outcome percentages
// Chart Type: Grouped column chart
// Categories: Touchdowns, Field Goals, Punts, Turnovers
// Series: Home team, Away team
```

#### **`scoring-pie-config.ts`**
```typescript
// Pie chart showing total scoring efficiency
// Chart Type: Donut/Pie chart
// Segments: Home scoring %, Away scoring %, Non-scoring %
```

### Step 2: Create Supporting Classes

#### **`DriveModifierGroup.ts`**
```typescript
// Extends ModifierGroup from the example
// Manages synchronized cursor/rollover across all 5 charts
export class DriveModifierGroup extends ModifierGroup {
  // Add drive-specific synchronization logic
}
```

#### **`DriveAxisSyncManager.ts`**
```typescript
// Manages X-axis visible range synchronization
// Allows toggling sync on/off for independent zoom
export class DriveAxisSyncManager {
  enabled: boolean = true;
  // Sync logic for quarter timeline across charts
}
```

### Step 3: Transform DriveEfficiency Component

Replace the current component structure with:

```typescript
import { SciChartReact as SciChart, ChartGroupLoader } from 'scichart-react';
import { getQuarterPerformanceConfig } from './drive-analytics/quarter-performance-config';
import { getFieldPositionConfig } from './drive-analytics/field-position-config';
import { getDriveFlowConfig } from './drive-analytics/drive-flow-config';
import { getDriveOutcomesConfig } from './drive-analytics/drive-outcomes-config';
import { getScoringPieConfig } from './drive-analytics/scoring-pie-config';

export const DriveEfficiency = ({ predictionData, team1Data, team2Data }: DriveEfficiencyProps) => {
  // Extract drive analytics from API
  const driveAnalytics = predictionData?.drive_analytics;
  const homeData = driveAnalytics?.home;
  const awayData = driveAnalytics?.away;

  // State management
  const [modifierGroup] = useState(new DriveModifierGroup());
  const [axisSyncManager] = useState(new DriveAxisSyncManager());
  const [isAxisSynced, setIsAxisSynced] = useState(true);
  const [isGridLayout, setIsGridLayout] = useState(false);

  return (
    <GlassCard className="col-span-2">
      <h3>Drive Efficiency & Game Flow Analytics</h3>
      
      <ChartGroupLoader style={driveGridStyle}>
        {/* Top: Quarter-by-Quarter Performance Timeline */}
        <SciChart
          initChart={getQuarterPerformanceConfig(homeData, awayData)}
          onInit={onQuarterChartInit}
          style={quarterChartStyle}
        />

        {/* Middle Left: Field Position Scoring Mastery */}
        <SciChart
          initChart={getFieldPositionConfig(homeData, awayData)}
          onInit={onFieldPositionChartInit}
          style={fieldPositionStyle}
        />

        {/* Middle Right: Drive Flow Analysis */}
        <SciChart
          initChart={getDriveFlowConfig(homeData, awayData, isGridLayout)}
          onInit={onDriveFlowChartInit}
          style={driveFlowStyle}
        />

        {/* Bottom Left: Drive Outcome Breakdown */}
        <SciChart
          initChart={getDriveOutcomesConfig(homeData, awayData)}
          style={outcomesStyle}
        />

        {/* Bottom Right: Total Scoring Efficiency */}
        <SciChart
          initChart={getScoringPieConfig(homeData, awayData)}
          style={pieStyle}
        />
      </ChartGroupLoader>

      {/* Keep existing InsightBox at bottom */}
      <InsightBox {...insightProps} />
    </GlassCard>
  );
};
```

### Step 4: Grid Layout Styles

```typescript
const driveGridStyle: React.CSSProperties = {
  height: '600px',
  display: 'grid',
  gridTemplateColumns: 'repeat(4, 1fr)',
  gridTemplateRows: 'repeat(8, 1fr)',
  gap: '0.5em',
  padding: '1em',
};

const quarterChartStyle = {
  gridRow: '1 / 4',      // Top section, spans 3 rows
  gridColumn: '1 / -1',   // Full width
};

const fieldPositionStyle = {
  gridRow: '4 / 7',       // Middle section
  gridColumn: '1 / 3',    // Left half
};

const driveFlowStyle = {
  gridRow: '4 / 7',       // Middle section
  gridColumn: '3 / -1',   // Right half
};

const outcomesStyle = {
  gridRow: '7 / -1',      // Bottom section
  gridColumn: 'span 3',   // Left 3/4
};

const pieStyle = {
  gridRow: '7 / -1',      // Bottom section
  gridColumn: 'span 1',   // Right 1/4
};
```

---

## 📊 Data Mapping

### From API to Chart Configs

**Quarter Performance Chart:**
```typescript
const homeQuarterData = homeData.quarter_data.map(q => ({
  x: q.quarter,           // "Q1", "Q2", "Q3", "Q4"
  y: q.scoringPct,        // 62.1, 43.2, 55.3, 29.6
}));
```

**Field Position Chart:**
```typescript
const homeFieldData = homeData.field_position_data.map(fp => ({
  category: fp.zone,      // "Own 1-20", "Own 21-40", etc.
  value: fp.scoringPct,   // 20.0, 66.7, 33.3, 50.8
  drives: fp.drives,      // 25, 39, 9, 59
}));
```

**Drive Outcomes Chart:**
```typescript
const homeOutcomes = [
  { category: 'Touchdowns', value: homeData.drive_outcomes.touchdowns },
  { category: 'Field Goals', value: homeData.drive_outcomes.fieldGoals },
  { category: 'Punts', value: homeData.drive_outcomes.punts },
  { category: 'Turnovers', value: homeData.drive_outcomes.turnovers },
];
```

---

## 🎨 Theme Integration

Match your existing glassmorphism design:

```typescript
const chartTheme = {
  background: 'rgba(255, 255, 255, 0.05)',
  foreground: '#ffffff',
  gridColor: 'rgba(255, 255, 255, 0.1)',
  homeTeamColor: team1Data?.primary_color || '#FF6B6B',
  awayTeamColor: team2Data?.primary_color || '#4ECDC4',
};
```

---

## ✨ Interactive Features to Implement

1. **Synchronized Cursors**: Hover over Q2 in timeline → highlights Q2 data in all charts
2. **Axis Sync Toggle**: Settings button to enable/disable synchronized zoom
3. **Grid Layout Toggle**: Switch drive flow between stacked and grid view
4. **Tooltips**: Show detailed stats on hover (e.g., "Q2: 16/37 drives scored (43.2%)")
5. **Animations**: Smooth transitions when loading new predictions
6. **Responsive Design**: Adjust grid layout for mobile (stack charts vertically)

---

## 🧪 Testing Checklist

- [ ] Charts render with Georgia vs Alabama data
- [ ] Cursor synchronization works across all 5 charts
- [ ] Tooltips display correct drive statistics
- [ ] Grid layout toggle switches drive flow view
- [ ] Axis sync toggle enables/disables zoom coordination
- [ ] Charts update when new prediction is loaded
- [ ] Mobile responsive (charts stack vertically)
- [ ] Theme matches glassmorphism design
- [ ] Performance is smooth with real data (132+ drives)

---

## 📝 Notes

- **Current component**: 1,477 lines with custom SVG spider chart
- **New approach**: ~800 lines using SciChart's professional charting library
- **Performance**: SciChart is optimized for large datasets (handles 132 drives easily)
- **Maintainability**: Chart configs are modular and reusable
- **User experience**: Interactive tooltips, zoom, pan, synchronized views

---

## 🚀 Deployment

After implementation:

1. Test with `npm run dev`
2. Load Georgia vs Alabama prediction
3. Verify all 5 charts display correctly
4. Test interactive features (hover, zoom, toggle)
5. Push to production

---

## 💡 Future Enhancements

- Add "Export to PDF" button for chart dashboard
- Implement real-time updates during live games
- Add historical comparison (overlay previous matchups)
- Create "Drive by Drive" timeline view with play-by-play
- Add predictive overlays showing expected vs actual outcomes

---

## 📚 Reference Links

- SciChart React: https://www.scichart.com/documentation/react/
- Example Dashboard: Server Traffic Dashboard (provided code)
- Current Data Structure: `app.py` line 667+ (`analyze_team_drives_for_ui`)

---

**Status**: Ready to implement
**Estimated Time**: 4-6 hours
**Priority**: High - transforms static percentages into interactive analytics
**Impact**: Professional ESPN-level drive analytics visualization
