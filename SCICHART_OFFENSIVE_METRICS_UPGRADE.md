# 🏈 SciChart Advanced Offensive Metrics Dashboard

## 📋 Overview
Transform the current `AdvancedOffensiveMetrics` component into an interactive horizontal comparison dashboard with animated bars, sparklines, and synchronized tooltips.

## 🎯 Objective
Replace static percentage displays with professional SciChart visualizations showing head-to-head offensive metric comparisons with leading indicators and trend analysis.

---

## 📦 Prerequisites

### Dependencies
```bash
cd frontend
npm install scichart scichart-react
```

### Current Component
- **File**: `frontend/src/components/figma/AdvancedOffensiveMetrics.tsx` (or similar)
- **Data source**: API returns offensive stats with PPA, success rates, explosiveness, etc.

---

## 🏗️ Implementation Plan

### Chart Layout Structure

Create a **multi-row horizontal bar chart dashboard** with 8 metric comparisons:

```
┌─────────────────────────────────────────────────┐
│  Offense PPA         [████████░░] 0.254         │
│                      [████████░░] 0.254         │
├─────────────────────────────────────────────────┤
│  Success Rate        [████████░░] 48.6%         │
│                      [███████░░░] 45.8%         │
├─────────────────────────────────────────────────┤
│  Explosiveness       [████████░░] 1.127         │
│                      [█████████░] 1.26          │
└─────────────────────────────────────────────────┘
```

---

## 📊 Chart Configuration Files

### File: `offensive-metrics-config.ts`

```typescript
import { 
  EAutoRange,
  EAxisAlignment,
  FastColumnRenderableSeries,
  NumericAxis,
  SciChartSurface,
  XyDataSeries,
  NumberRange,
  ELabelAlignment,
  EHorizontalAnchorPoint,
  EVerticalAnchorPoint
} from 'scichart';

export interface OffensiveMetric {
  name: string;
  homeValue: number;
  awayValue: number;
  unit?: string;
  inverse?: boolean; // true if lower is better
  maxScale?: number;
}

export const getOffensiveMetricsConfig = (
  homeTeam: string,
  awayTeam: string,
  metrics: OffensiveMetric[],
  homeColor: string,
  awayColor: string
) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {
      theme: {
        axisBandsFill: 'rgba(255, 255, 255, 0.02)',
        gridBackgroundBrush: 'transparent',
        gridBorderBrush: 'rgba(255, 255, 255, 0.1)',
        majorGridLineBrush: 'rgba(255, 255, 255, 0.1)',
        minorGridLineBrush: 'rgba(255, 255, 255, 0.05)',
      }
    });

    // Create horizontal bar chart for each metric
    const yAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Left,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, metrics.length * 2),
      drawMajorGridLines: false,
      drawMinorGridLines: false,
      labelStyle: {
        color: '#ffffff',
        fontSize: 14,
        fontWeight: 'bold',
      },
      // Custom labels for metric names
      labelProvider: {
        formatLabel: (dataValue: number) => {
          const index = Math.floor(dataValue / 2);
          return metrics[index]?.name || '';
        }
      }
    });

    const xAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Top,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 100),
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      labelStyle: { color: '#ffffff', fontSize: 12 },
    });

    sciChartSurface.xAxes.add(xAxis);
    sciChartSurface.yAxes.add(yAxis);

    // Add horizontal bars for each metric
    metrics.forEach((metric, index) => {
      const yPosition = index * 2;
      
      // Home team bar
      const homeData = new XyDataSeries(wasmContext, {
        xValues: [0, metric.homeValue],
        yValues: [yPosition, yPosition],
      });
      
      const homeSeries = new FastColumnRenderableSeries(wasmContext, {
        dataSeries: homeData,
        fill: homeColor,
        stroke: homeColor,
        strokeThickness: 2,
        dataPointWidth: 0.8,
        opacity: 0.8,
      });

      // Away team bar (offset by 1)
      const awayData = new XyDataSeries(wasmContext, {
        xValues: [0, metric.awayValue],
        yValues: [yPosition + 1, yPosition + 1],
      });
      
      const awaySeries = new FastColumnRenderableSeries(wasmContext, {
        dataSeries: awayData,
        fill: awayColor,
        stroke: awayColor,
        strokeThickness: 2,
        dataPointWidth: 0.8,
        opacity: 0.8,
      });

      sciChartSurface.renderableSeries.add(homeSeries, awaySeries);

      // Add value labels
      const homeLabel = new TextAnnotation({
        x1: metric.homeValue,
        y1: yPosition,
        text: `${metric.homeValue}${metric.unit || ''}`,
        textColor: '#ffffff',
        fontSize: 14,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.DataValue,
        yCoordinateMode: ECoordinateMode.DataValue,
      });

      const awayLabel = new TextAnnotation({
        x1: metric.awayValue,
        y1: yPosition + 1,
        text: `${metric.awayValue}${metric.unit || ''}`,
        textColor: '#ffffff',
        fontSize: 14,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.DataValue,
        yCoordinateMode: ECoordinateMode.DataValue,
      });

      sciChartSurface.annotations.add(homeLabel, awayLabel);
    });

    // Add cursor modifier for tooltips
    const cursorModifier = new CursorModifier({
      showTooltip: true,
      showAxisLabels: true,
      crosshairStroke: 'rgba(255, 255, 255, 0.3)',
      tooltipContainerBackground: 'rgba(0, 0, 0, 0.8)',
    });

    sciChartSurface.chartModifiers.add(cursorModifier);

    return { sciChartSurface, wasmContext };
  };
};
```

---

## 🎨 Alternative: Diverging Bar Chart

For better visual comparison, use a **diverging bar chart** where bars extend left (away team) and right (home team) from center:

### File: `offensive-diverging-config.ts`

```typescript
// Center-aligned diverging bars
// Home team bars extend RIGHT (positive)
// Away team bars extend LEFT (negative)
// Shows immediate visual comparison of which team leads

export const getDivergingMetricsConfig = (
  homeTeam: string,
  awayTeam: string,
  metrics: OffensiveMetric[],
  homeColor: string,
  awayColor: string
) => {
  return async (divId: string) => {
    // ... surface setup ...

    metrics.forEach((metric, index) => {
      const yPosition = (metrics.length - index - 1) * 2; // Reverse order (top to bottom)
      
      // Home team: positive values (extend right)
      const homeData = new XyDataSeries(wasmContext, {
        xValues: [0, metric.homeValue],
        yValues: [yPosition, yPosition],
      });

      // Away team: negative values (extend left)
      const awayData = new XyDataSeries(wasmContext, {
        xValues: [0, -metric.awayValue],
        yValues: [yPosition + 0.6, yPosition + 0.6],
      });

      // Add series with gradient fills
      const homeSeries = new FastColumnRenderableSeries(wasmContext, {
        dataSeries: homeData,
        fill: {
          linearGradient: {
            startPoint: { x: 0, y: 0 },
            endPoint: { x: 1, y: 0 },
            stops: [
              { offset: 0, color: homeColor + '80' },
              { offset: 1, color: homeColor }
            ]
          }
        },
        stroke: homeColor,
        dataPointWidth: 0.5,
      });

      const awaySeries = new FastColumnRenderableSeries(wasmContext, {
        dataSeries: awayData,
        fill: {
          linearGradient: {
            startPoint: { x: 0, y: 0 },
            endPoint: { x: 1, y: 0 },
            stops: [
              { offset: 0, color: awayColor },
              { offset: 1, color: awayColor + '80' }
            ]
          }
        },
        stroke: awayColor,
        dataPointWidth: 0.5,
      });

      sciChartSurface.renderableSeries.add(homeSeries, awaySeries);
    });

    return { sciChartSurface };
  };
};
```

---

## 🎯 Alternative: Bullet Chart with Targets

Create **bullet charts** showing actual value vs benchmark:

```typescript
// Each metric shows:
// - Bar = actual value
// - Vertical line = national average
// - Color intensity = percentile rank
```

---

## 💡 Modern Visual Options

### Option 1: **Animated Racing Bars**
- Bars "race" from 0 to final value on load
- Smooth easing animation
- Winner highlighted with glow effect

### Option 2: **Sparkline Trends**
- Small line chart next to each bar showing season trend
- Shows if metric is improving/declining
- Adds context beyond single game

### Option 3: **Radial Progress Rings**
- Circular progress indicators instead of bars
- Fills clockwise from top
- Percentage in center
- More compact, fits 8 metrics in less space

### Option 4: **Heatmap Grid**
- 8 rows × 2 columns (home vs away)
- Color intensity shows value magnitude
- Instant visual pattern recognition

---

## 🏗️ Component Structure

```typescript
import { SciChartReact as SciChart } from 'scichart-react';
import { getOffensiveMetricsConfig } from './offensive-metrics-config';

export const AdvancedOffensiveMetrics = ({ predictionData, team1Data, team2Data }) => {
  const homeStats = predictionData?.team_statistics?.home;
  const awayStats = predictionData?.team_statistics?.away;

  const metrics: OffensiveMetric[] = [
    { name: 'Offense PPA', homeValue: homeStats.offense_ppa, awayValue: awayStats.offense_ppa },
    { name: 'Success Rate', homeValue: homeStats.success_rate_offense, awayValue: awayStats.success_rate_offense, unit: '%' },
    { name: 'Explosiveness', homeValue: homeStats.explosiveness_offense, awayValue: awayStats.explosiveness_offense },
    { name: 'Power Success', homeValue: homeStats.power_success, awayValue: awayStats.power_success, unit: '%' },
    { name: 'Stuff Rate', homeValue: homeStats.stuff_rate, awayValue: awayStats.stuff_rate, unit: '%', inverse: true },
    { name: 'Line Yards', homeValue: homeStats.line_yards, awayValue: awayStats.line_yards },
    { name: 'Second Level Yards', homeValue: homeStats.second_level_yards, awayValue: awayStats.second_level_yards },
    { name: 'Open Field Yards', homeValue: homeStats.open_field_yards, awayValue: awayStats.open_field_yards },
  ];

  const homeColor = team1Data?.primary_color || '#FF6B6B';
  const awayColor = team2Data?.primary_color || '#4ECDC4';

  return (
    <GlassCard>
      <div className="flex items-center justify-between mb-4">
        <h3>Advanced Offensive Metrics</h3>
        <div className="flex gap-2">
          <span className="text-sm">
            <span style={{ color: awayColor }}>●</span> {awayTeam} leads {awayLeads}
          </span>
          <span className="text-sm">
            <span style={{ color: homeColor }}>●</span> {homeTeam} leads {homeLeads}
          </span>
        </div>
      </div>

      <SciChart
        initChart={getOffensiveMetricsConfig(homeTeam, awayTeam, metrics, homeColor, awayColor)}
        style={{ height: '500px', width: '100%' }}
      />

      <InsightBox {...insightProps} />
    </GlassCard>
  );
};
```

---

## 📊 Data Mapping

```typescript
// From API response:
predictionData.team_statistics.home = {
  offense_ppa: 0.254,
  success_rate_offense: 48.6,
  explosiveness_offense: 1.127,
  power_success: 72.3,
  stuff_rate: 18.5,
  line_yards: 3.1,
  second_level_yards: 1.08,
  open_field_yards: 0.9
}

predictionData.team_statistics.away = {
  offense_ppa: 0.254,
  success_rate_offense: 45.8,
  explosiveness_offense: 1.26,
  power_success: 68.9,
  stuff_rate: 16.0,
  line_yards: 2.99,
  second_level_yards: 0.92,
  open_field_yards: 0.68
}
```

---

## ✨ Interactive Features

1. **Hover Tooltips**: Show exact values + national percentile rank
2. **Click to Compare**: Click metric to see historical trend
3. **Animated Entrance**: Bars animate from 0 to value on mount
4. **Leader Indicators**: Arrow showing which team leads each metric
5. **Benchmark Lines**: Dashed line showing national average
6. **Color Intensity**: Darker color = better performance

---

## 🎨 Theme Customization

```typescript
const chartTheme = {
  background: 'rgba(255, 255, 255, 0.05)', // Match glassmorphism
  gridLines: 'rgba(255, 255, 255, 0.1)',
  textColor: '#ffffff',
  homeTeamGradient: `linear-gradient(90deg, ${homeColor}80, ${homeColor})`,
  awayTeamGradient: `linear-gradient(90deg, ${awayColor}, ${awayColor}80)`,
  winnerGlow: '0 0 10px rgba(76, 175, 80, 0.5)',
};
```

---

## 🧪 Testing Checklist

- [ ] All 8 metrics display correctly
- [ ] Bars animate smoothly on load
- [ ] Hover tooltips show detailed stats
- [ ] Colors match team primary colors
- [ ] Leader count updates correctly
- [ ] Responsive on mobile (stack vertically)
- [ ] Performance with rapid prediction changes

---

## 🚀 Alternative Chart Types

### Radial Bars (Circular)
```typescript
// Use PolarChart instead of XyChart
// Metrics arranged in circle
// Visually striking, fits more in less space
```

### Lollipop Chart
```typescript
// Thin line from 0 to value with circle at end
// More minimal than bars
// Better for dense layouts
```

### Slope Chart
```typescript
// Two vertical axes (home vs away)
// Diagonal lines connecting values
// Shows relative performance instantly
```

---

**Status**: Ready to implement  
**Estimated Time**: 3-4 hours  
**Priority**: High - key comparison metrics  
**Impact**: Professional ESPN-style offensive analytics
