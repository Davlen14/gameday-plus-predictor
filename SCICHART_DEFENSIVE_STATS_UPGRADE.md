# 🛡️ SciChart Defensive Statistics Dashboard

## 📋 Overview
Transform the current `DefensiveStatistics` component into an interactive circular progress visualization with animated rings and comparative metrics.

## 🎯 Objective
Replace static progress bars with professional SciChart radial/polar charts showing defensive dominance with circular progress indicators and synchronized tooltips.

---

## 📦 Prerequisites

### Dependencies
```bash
cd frontend
npm install scichart scichart-react
```

### Current Component
- **File**: `frontend/src/components/figma/DefensiveStatistics.tsx`
- **Data source**: API returns defensive stats (sacks, interceptions, TFLs, etc.)

---

## 🏗️ Chart Layout Structure

Create a **radial gauge dashboard** with 8 defensive metrics:

```
     ┌─────────────────────────────────┐
     │         Sacks                   │
     │    ⚪━━━●━━━━━━━⚪                │
     │   UGA: 16    BAMA: 24           │
     ├─────────────────────────────────┤
     │      Interceptions              │
     │    ⚪━━━━━━●━━━⚪                 │
     │   UGA: 7     BAMA: 4            │
     └─────────────────────────────────┘
```

---

## 📊 Chart Configuration Files

### File: `defensive-radial-config.ts`

```typescript
import {
  SciChartSurface,
  NumericAxis,
  EAxisAlignment,
  EAutoRange,
  XyDataSeries,
  FastLineRenderableSeries,
  EllipsePointMarker,
  NumberRange,
  PolarChart,
} from 'scichart';

export interface DefensiveMetric {
  name: string;
  homeValue: number;
  awayValue: number;
  unit?: string;
  inverse?: boolean; // true if lower is better (e.g., yards allowed)
}

export const getDefensiveRadialConfig = (
  homeTeam: string,
  awayTeam: string,
  metrics: DefensiveMetric[],
  homeColor: string,
  awayColor: string
) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {
      theme: {
        background: 'transparent',
        gridBackgroundBrush: 'transparent',
        gridBorderBrush: 'rgba(255, 255, 255, 0.1)',
      }
    });

    // Create radial axis (angles)
    const angleAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Top,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 360),
      isPolarAxis: true,
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      majorGridLineStyle: {
        color: 'rgba(255, 255, 255, 0.1)',
        strokeThickness: 1,
      },
    });

    // Create radial distance axis
    const radiusAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Left,
      autoRange: EAutoRange.Always,
      isPolarAxis: true,
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      majorGridLineStyle: {
        color: 'rgba(255, 255, 255, 0.1)',
        strokeThickness: 1,
      },
    });

    sciChartSurface.xAxes.add(angleAxis);
    sciChartSurface.yAxes.add(radiusAxis);

    // Calculate angles for each metric (evenly distributed)
    const angleStep = 360 / metrics.length;

    // Create data series for home team (outer ring)
    const homeAngles = metrics.map((_, i) => i * angleStep);
    const homeValues = metrics.map(m => m.homeValue);
    
    const homeData = new XyDataSeries(wasmContext, {
      xValues: homeAngles,
      yValues: homeValues,
      dataSeriesName: homeTeam,
    });

    const homeSeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: homeData,
      stroke: homeColor,
      strokeThickness: 3,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 10,
        height: 10,
        fill: homeColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    // Create data series for away team (inner ring)
    const awayAngles = metrics.map((_, i) => i * angleStep);
    const awayValues = metrics.map(m => m.awayValue);
    
    const awayData = new XyDataSeries(wasmContext, {
      xValues: awayAngles,
      yValues: awayValues,
      dataSeriesName: awayTeam,
    });

    const awaySeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: awayData,
      stroke: awayColor,
      strokeThickness: 3,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 10,
        height: 10,
        fill: awayColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    sciChartSurface.renderableSeries.add(homeSeries, awaySeries);

    // Add labels for each metric
    metrics.forEach((metric, index) => {
      const angle = index * angleStep;
      const labelAnnotation = new TextAnnotation({
        x1: angle,
        y1: radiusAxis.visibleRange.max * 1.1,
        text: metric.name,
        textColor: '#ffffff',
        fontSize: 12,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.DataValue,
        yCoordinateMode: ECoordinateMode.DataValue,
        horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
      });
      sciChartSurface.annotations.add(labelAnnotation);
    });

    // Add rollover modifier for tooltips
    const rolloverModifier = new RolloverModifier({
      showTooltip: true,
      showAxisLabels: false,
      tooltipContainerBackground: 'rgba(0, 0, 0, 0.8)',
      tooltipTextColor: '#ffffff',
    });

    sciChartSurface.chartModifiers.add(rolloverModifier);

    return { sciChartSurface, wasmContext };
  };
};
```

---

## 🎯 Alternative: Circular Progress Rings

Create individual **circular progress indicators** for each metric:

### File: `defensive-circular-progress-config.ts`

```typescript
// 8 individual circular progress rings
// Each ring shows home vs away as inner/outer circles
// Fill percentage = value relative to max
// Color intensity = performance level

export const getCircularProgressConfig = (metric: DefensiveMetric) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

    // Create donut chart for this metric
    const maxValue = Math.max(metric.homeValue, metric.awayValue) * 1.2;
    const homePercent = (metric.homeValue / maxValue) * 100;
    const awayPercent = (metric.awayValue / maxValue) * 100;

    // Outer ring (home team)
    const homeRing = new DonutRenderableSeries(wasmContext, {
      innerRadius: 0.6,
      outerRadius: 0.9,
      segments: [
        { 
          value: homePercent,
          color: homeColor,
          label: `${homeTeam}: ${metric.homeValue}${metric.unit || ''}`
        },
        { 
          value: 100 - homePercent,
          color: 'rgba(255, 255, 255, 0.1)',
          label: ''
        }
      ],
      animate: true,
      animationDuration: 1000,
    });

    // Inner ring (away team)
    const awayRing = new DonutRenderableSeries(wasmContext, {
      innerRadius: 0.3,
      outerRadius: 0.5,
      segments: [
        { 
          value: awayPercent,
          color: awayColor,
          label: `${awayTeam}: ${metric.awayValue}${metric.unit || ''}`
        },
        { 
          value: 100 - awayPercent,
          color: 'rgba(255, 255, 255, 0.1)',
          label: ''
        }
      ],
      animate: true,
      animationDuration: 1000,
    });

    sciChartSurface.renderableSeries.add(homeRing, awayRing);

    // Add center text with metric name
    const centerText = new TextAnnotation({
      x1: 0.5,
      y1: 0.5,
      text: metric.name,
      textColor: '#ffffff',
      fontSize: 14,
      fontWeight: 'bold',
      xCoordinateMode: ECoordinateMode.Relative,
      yCoordinateMode: ECoordinateMode.Relative,
    });

    sciChartSurface.annotations.add(centerText);

    return { sciChartSurface };
  };
};
```

---

## 💡 Modern Visual Options

### Option 1: **Spider/Radar Chart** ⭐ RECOMMENDED
- Perfect for defensive metrics (8 axes)
- Overlaid polygons show team comparison
- Instant visual of strengths/weaknesses
- Matches football analytics aesthetic

### Option 2: **Gauge Dashboard**
- 8 semicircular gauges in 2 rows
- Needle points to team value
- Color zones: Red (poor) → Yellow (average) → Green (elite)
- Clean, professional look

### Option 3: **Stacked Radial Bars**
- Circular bar chart with 8 segments
- Each segment = one metric
- Inner ring = away, outer ring = home
- Fills clockwise from 0-360°

### Option 4: **Heat Rings**
- Concentric circles with color intensity
- Brighter = better performance
- 8 rings (one per metric)
- Compact visualization

---

## 🏗️ Component Structure

```typescript
import { SciChartReact as SciChart } from 'scichart-react';
import { getDefensiveRadialConfig } from './defensive-radial-config';

export const DefensiveStatistics = ({ predictionData, team1Data, team2Data }) => {
  const homeStats = predictionData?.team_statistics?.home;
  const awayStats = predictionData?.team_statistics?.away;

  const metrics: DefensiveMetric[] = [
    { name: 'Sacks', homeValue: homeStats.sacks, awayValue: awayStats.sacks },
    { name: 'Interceptions', homeValue: homeStats.interceptions, awayValue: awayStats.interceptions },
    { name: 'Tackles for Loss', homeValue: homeStats.tackles_for_loss, awayValue: awayStats.tackles_for_loss },
    { name: 'Fumbles Recovered', homeValue: homeStats.fumbles_recovered, awayValue: awayStats.fumbles_recovered },
    { name: 'Defense PPA', homeValue: homeStats.defense_ppa, awayValue: awayStats.defense_ppa, inverse: true },
    { name: 'Defense Success Rate', homeValue: homeStats.defense_success_rate, awayValue: awayStats.defense_success_rate, unit: '%', inverse: true },
    { name: 'Defense Explosiveness', homeValue: homeStats.defense_explosiveness, awayValue: awayStats.defense_explosiveness, inverse: true },
    { name: 'Defense Havoc Total', homeValue: homeStats.defense_havoc_total, awayValue: awayStats.defense_havoc_total, unit: '%' },
  ];

  // Calculate leader counts
  const homeLeads = metrics.filter(m => 
    m.inverse ? m.homeValue < m.awayValue : m.homeValue > m.awayValue
  ).length;
  const awayLeads = metrics.length - homeLeads;

  return (
    <GlassCard>
      <div className="flex items-center justify-between mb-4">
        <h3>Defensive Statistics</h3>
        <div className="flex gap-2 text-sm">
          <span style={{ color: awayColor }}>●</span> {awayTeam} leads {awayLeads}
          <span style={{ color: homeColor }}>●</span> {homeTeam} leads {homeLeads}
        </div>
      </div>

      <SciChart
        initChart={getDefensiveRadialConfig(
          homeTeam,
          awayTeam,
          metrics,
          team1Data?.primary_color || '#FF6B6B',
          team2Data?.primary_color || '#4ECDC4'
        )}
        style={{ height: '600px', width: '100%' }}
      />

      <InsightBox
        whatItMeans="Defensive metrics show ability to disrupt opponent's offense..."
        whyItMatters={`${homeLeads > awayLeads ? homeTeam : awayTeam} defense dominates in ${Math.max(homeLeads, awayLeads)} of 8 categories`}
        whoHasEdge={{
          team: homeLeads > awayLeads ? homeTeam : awayTeam,
          reason: `Superior in sacks, TFLs, and havoc rate`,
          magnitude: Math.abs(homeLeads - awayLeads) > 3 ? 'major' : 'moderate'
        }}
        keyDifferences={[
          `Sacks: ${homeStats.sacks} vs ${awayStats.sacks}`,
          `Interceptions: ${homeStats.interceptions} vs ${awayStats.interceptions}`,
          `Havoc rate: ${homeStats.defense_havoc_total}% vs ${awayStats.defense_havoc_total}%`
        ]}
      />
    </GlassCard>
  );
};
```

---

## 📊 Data Mapping

```typescript
// From API response:
predictionData.team_statistics.home = {
  sacks: 16,
  interceptions: 7,
  tackles_for_loss: 51,
  fumbles_recovered: 3,
  defense_ppa: 0.09,
  defense_success_rate: 37.8,
  defense_explosiveness: 1.152,
  defense_havoc_total: 14.7
}

predictionData.team_statistics.away = {
  sacks: 24,
  interceptions: 4,
  tackles_for_loss: 67,
  fumbles_recovered: 9,
  defense_ppa: 0.044,
  defense_success_rate: 36.8,
  defense_explosiveness: 1.24,
  defense_havoc_total: 18.6
}
```

---

## ✨ Interactive Features

1. **Animated Fill**: Rings/bars animate from 0 to value on mount
2. **Hover Highlight**: Mouse over metric highlights that axis/ring
3. **Click to Drill Down**: Click metric to see game-by-game breakdown
4. **Leader Indicators**: Trophy icon on winning team's data point
5. **Benchmark Overlay**: National average shown as dashed circle
6. **Percentile Badges**: Show where each value ranks nationally

---

## 🎨 Theme Customization

```typescript
const defensiveTheme = {
  background: 'rgba(255, 255, 255, 0.05)',
  gridColor: 'rgba(255, 255, 255, 0.1)',
  textColor: '#ffffff',
  homeTeamGlow: `0 0 15px ${homeColor}80`,
  awayTeamGlow: `0 0 15px ${awayColor}80`,
  winnerHighlight: 'rgba(76, 175, 80, 0.3)',
  loserHighlight: 'rgba(244, 67, 54, 0.3)',
};
```

---

## 🧪 Testing Checklist

- [ ] All 8 metrics display correctly
- [ ] Radial chart renders with proper scaling
- [ ] Tooltips show detailed defensive stats
- [ ] Leader count matches visual comparison
- [ ] Animations smooth and performant
- [ ] Responsive layout (mobile stacks vertically)
- [ ] Colors match team branding

---

## 🚀 Grid Layout Alternative

For a **dashboard of 8 individual circular gauges**:

```typescript
const gaugeGridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(4, 1fr)',
  gridTemplateRows: 'repeat(2, 1fr)',
  gap: '1em',
  padding: '1em',
};

// Render 8 separate SciChart instances
metrics.map(metric => (
  <SciChart
    key={metric.name}
    initChart={getCircularProgressConfig(metric)}
    style={{ height: '150px', width: '100%' }}
  />
))
```

---

**Status**: Ready to implement  
**Estimated Time**: 3-4 hours  
**Priority**: High - defensive dominance visualization  
**Impact**: Professional circular progress analytics like NFL Next Gen Stats
