# ⚡ SciChart Game Control Metrics Dashboard

## 📋 Overview
Transform the current `GameControlMetrics` component into an interactive tempo and possession analytics dashboard with radar-style visualization and synchronized comparisons.

## 🎯 Objective
Replace static progress bars with professional SciChart radar/spider charts showing tempo, possession, and game control metrics with animated overlays and synchronized tooltips.

---

## 📦 Prerequisites

### Dependencies
```bash
cd frontend
npm install scichart scichart-react
```

### Current Component
- **File**: `frontend/src/components/figma/GameControlMetrics.tsx`
- **Data source**: API returns possession time, turnover margin, penalties, drives per game

---

## 🏗️ Chart Layout Structure

Create a **multi-panel radar chart dashboard**:

```
┌─────────────────────────────────────────┐
│     Game Control Radar Chart            │
│                                          │
│           Possession Time                │
│               ●                          │
│              /│\                         │
│    Drives   / │ \   Turnovers           │
│      ●─────●  │  ●─────●                │
│            \  │  /                       │
│             \ │ /                        │
│              \│/                         │
│               ●                          │
│           Penalties                      │
└─────────────────────────────────────────┘
```

---

## 📊 Chart Configuration Files

### File: `game-control-radar-config.ts`

```typescript
import {
  SciChartSurface,
  NumericAxis,
  EAxisAlignment,
  EAutoRange,
  XyDataSeries,
  FastLineRenderableSeries,
  SplineLineRenderableSeries,
  EllipsePointMarker,
  NumberRange,
  EFillPaletteMode,
  GradientParams,
  Point,
} from 'scichart';

export interface GameControlMetric {
  name: string;
  homeValue: number;
  awayValue: number;
  maxScale: number;
  unit?: string;
  inverse?: boolean; // true if lower is better (e.g., penalties)
}

export const getGameControlRadarConfig = (
  homeTeam: string,
  awayTeam: string,
  metrics: GameControlMetric[],
  homeColor: string,
  awayColor: string
) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {
      theme: {
        background: 'transparent',
        gridBackgroundBrush: 'transparent',
        gridBorderBrush: 'rgba(255, 255, 255, 0.1)',
        majorGridLineBrush: 'rgba(255, 255, 255, 0.1)',
        minorGridLineBrush: 'rgba(255, 255, 255, 0.05)',
      }
    });

    // Configure polar axes
    const angleAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Top,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 360),
      isPolarAxis: true,
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      labelProvider: {
        formatLabel: (dataValue: number) => {
          // Custom labels for each metric position
          const index = Math.floor((dataValue / 360) * metrics.length);
          return metrics[index]?.name || '';
        }
      },
      labelStyle: {
        color: '#ffffff',
        fontSize: 14,
        fontWeight: 'bold',
      },
    });

    const radiusAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Left,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 100),
      isPolarAxis: true,
      drawMajorGridLines: true,
      drawMinorGridLines: true,
      majorGridLineStyle: {
        color: 'rgba(255, 255, 255, 0.15)',
        strokeThickness: 1,
        strokeDashArray: [5, 5],
      },
      minorGridLineStyle: {
        color: 'rgba(255, 255, 255, 0.05)',
        strokeThickness: 1,
      },
    });

    sciChartSurface.xAxes.add(angleAxis);
    sciChartSurface.yAxes.add(radiusAxis);

    // Convert metrics to angular positions
    const angleStep = 360 / metrics.length;
    
    // Normalize values to 0-100 scale for radar chart
    const normalizeValue = (value: number, maxScale: number, inverse: boolean = false) => {
      const normalized = (value / maxScale) * 100;
      return inverse ? 100 - normalized : normalized;
    };

    // Home team data (outer polygon)
    const homeAngles = metrics.map((_, i) => i * angleStep);
    const homeValues = metrics.map(m => 
      normalizeValue(m.homeValue, m.maxScale, m.inverse)
    );

    // Close the polygon by adding first point at end
    homeAngles.push(homeAngles[0]);
    homeValues.push(homeValues[0]);

    const homeData = new XyDataSeries(wasmContext, {
      xValues: homeAngles,
      yValues: homeValues,
      dataSeriesName: homeTeam,
    });

    const homeSeries = new SplineLineRenderableSeries(wasmContext, {
      dataSeries: homeData,
      stroke: homeColor,
      strokeThickness: 3,
      fill: homeColor + '30', // 30 = ~20% opacity
      fillLinearGradient: new GradientParams(
        new Point(0, 0),
        new Point(0, 1),
        [
          { offset: 0, color: homeColor + '60' },
          { offset: 1, color: homeColor + '10' }
        ]
      ),
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: homeColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
      paletteProvider: undefined,
    });

    // Away team data (inner polygon)
    const awayAngles = metrics.map((_, i) => i * angleStep);
    const awayValues = metrics.map(m => 
      normalizeValue(m.awayValue, m.maxScale, m.inverse)
    );

    // Close the polygon
    awayAngles.push(awayAngles[0]);
    awayValues.push(awayValues[0]);

    const awayData = new XyDataSeries(wasmContext, {
      xValues: awayAngles,
      yValues: awayValues,
      dataSeriesName: awayTeam,
    });

    const awaySeries = new SplineLineRenderableSeries(wasmContext, {
      dataSeries: awayData,
      stroke: awayColor,
      strokeThickness: 3,
      fill: awayColor + '30',
      fillLinearGradient: new GradientParams(
        new Point(0, 0),
        new Point(0, 1),
        [
          { offset: 0, color: awayColor + '60' },
          { offset: 1, color: awayColor + '10' }
        ]
      ),
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: awayColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    sciChartSurface.renderableSeries.add(homeSeries, awaySeries);

    // Add metric labels around the perimeter
    metrics.forEach((metric, index) => {
      const angle = index * angleStep;
      const angleRad = (angle * Math.PI) / 180;
      const labelRadius = 110; // Outside the chart

      const x = 50 + labelRadius * Math.sin(angleRad);
      const y = 50 - labelRadius * Math.cos(angleRad);

      const labelAnnotation = new TextAnnotation({
        x1: x,
        y1: y,
        text: metric.name,
        textColor: '#ffffff',
        fontSize: 13,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.Relative,
        yCoordinateMode: ECoordinateMode.Relative,
        horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
        verticalAnchorPoint: EVerticalAnchorPoint.Center,
      });

      sciChartSurface.annotations.add(labelAnnotation);

      // Add value labels
      const homeValueLabel = new TextAnnotation({
        x1: angle,
        y1: homeValues[index],
        text: `${metric.homeValue}${metric.unit || ''}`,
        textColor: homeColor,
        fontSize: 11,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.DataValue,
        yCoordinateMode: ECoordinateMode.DataValue,
      });

      const awayValueLabel = new TextAnnotation({
        x1: angle,
        y1: awayValues[index],
        text: `${metric.awayValue}${metric.unit || ''}`,
        textColor: awayColor,
        fontSize: 11,
        fontWeight: 'bold',
        xCoordinateMode: ECoordinateMode.DataValue,
        yCoordinateMode: ECoordinateMode.DataValue,
      });

      sciChartSurface.annotations.add(homeValueLabel, awayValueLabel);
    });

    // Add rollover modifier
    const rolloverModifier = new RolloverModifier({
      showTooltip: true,
      showAxisLabels: false,
      tooltipContainerBackground: 'rgba(0, 0, 0, 0.85)',
      tooltipTextColor: '#ffffff',
      rolloverLineStroke: 'rgba(255, 255, 255, 0.5)',
    });

    sciChartSurface.chartModifiers.add(rolloverModifier);

    // Add zoom/pan for interactivity
    const zoomPanModifier = new ZoomPanModifier({
      enableZoom: true,
      enablePan: true,
    });
    sciChartSurface.chartModifiers.add(zoomPanModifier);

    return { sciChartSurface, wasmContext };
  };
};
```

---

## 💡 Alternative: Segmented Progress Rings

Create **concentric progress rings** for each metric:

### File: `game-control-rings-config.ts`

```typescript
// 5 concentric rings (one per metric)
// Outer ring = Possession Time
// Inner rings = Turnover Margin, Penalties, Games Played, Drives/Game
// Each ring shows home vs away as split segments
// Color fill = percentage of total

export const getGameControlRingsConfig = (metrics: GameControlMetric[]) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

    metrics.forEach((metric, index) => {
      const outerRadius = 0.95 - (index * 0.15);
      const innerRadius = outerRadius - 0.12;

      // Calculate percentages
      const total = metric.homeValue + metric.awayValue;
      const homePercent = (metric.homeValue / total) * 100;
      const awayPercent = (metric.awayValue / total) * 100;

      // Create donut segment for this metric
      const ring = new DonutRenderableSeries(wasmContext, {
        innerRadius,
        outerRadius,
        segments: [
          { 
            value: homePercent,
            color: homeColor,
            label: `${homeTeam}: ${metric.homeValue}${metric.unit || ''}`,
            radiusAdjustment: 0,
          },
          { 
            value: awayPercent,
            color: awayColor,
            label: `${awayTeam}: ${metric.awayValue}${metric.unit || ''}`,
            radiusAdjustment: 0,
          }
        ],
        animate: true,
        animationDuration: 800 + (index * 200),
        animationEasing: 'easeOutCubic',
      });

      sciChartSurface.renderableSeries.add(ring);
    });

    return { sciChartSurface };
  };
};
```

---

## 🏗️ Component Structure

```typescript
import { SciChartReact as SciChart } from 'scichart-react';
import { getGameControlRadarConfig } from './game-control-radar-config';

export const GameControlMetrics = ({ predictionData, team1Data, team2Data }) => {
  const homeStats = predictionData?.team_statistics?.home;
  const awayStats = predictionData?.team_statistics?.away;

  const metrics: GameControlMetric[] = [
    { 
      name: 'Possession Time',
      homeValue: parseTimeToMinutes(homeStats.possession_time), // "402:05" -> 402.08
      awayValue: parseTimeToMinutes(awayStats.possession_time),
      maxScale: 480, // 8 hours (4 games × 60 min × 2)
      unit: ' min'
    },
    { 
      name: 'Turnover Margin',
      homeValue: homeStats.turnover_margin,
      awayValue: awayStats.turnover_margin,
      maxScale: 20,
      unit: ''
    },
    { 
      name: 'Penalty Yards',
      homeValue: homeStats.penalty_yards,
      awayValue: awayStats.penalty_yards,
      maxScale: 1000,
      unit: ' yds',
      inverse: true // Lower is better
    },
    { 
      name: 'Games Played',
      homeValue: homeStats.games_played,
      awayValue: awayStats.games_played,
      maxScale: 15,
      unit: ''
    },
    { 
      name: 'Drives/Game',
      homeValue: homeStats.drives_per_game,
      awayValue: awayStats.drives_per_game,
      maxScale: 15,
      unit: ''
    },
  ];

  // Calculate leader counts
  const homeLeads = metrics.filter(m => 
    m.inverse ? m.homeValue < m.awayValue : m.homeValue > m.awayValue
  ).length;
  const awayLeads = metrics.length - homeLeads;

  return (
    <GlassCard>
      <div className="flex items-center justify-between mb-4">
        <h3>Game Control Metrics</h3>
        <div className="text-sm">
          <span style={{ color: awayColor }}>●</span> {awayTeam} leads {awayLeads}
          {' / '}
          <span style={{ color: homeColor }}>●</span> {homeTeam} leads {homeLeads}
        </div>
      </div>

      <SciChart
        initChart={getGameControlRadarConfig(
          homeTeam,
          awayTeam,
          metrics,
          team1Data?.primary_color || '#FF6B6B',
          team2Data?.primary_color || '#4ECDC4'
        )}
        style={{ height: '600px', width: '100%' }}
      />

      {/* Individual metric breakdowns */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        {metrics.map(metric => (
          <div key={metric.name} className="p-4 bg-white/5 rounded-lg">
            <h4 className="text-sm font-semibold mb-2">{metric.name}</h4>
            <div className="flex items-center justify-between">
              <div className="text-center">
                <div style={{ color: awayColor }} className="text-2xl font-bold">
                  {metric.awayValue}{metric.unit}
                </div>
                <div className="text-xs text-gray-400">{awayTeam}</div>
              </div>
              <div className="text-gray-400">vs</div>
              <div className="text-center">
                <div style={{ color: homeColor }} className="text-2xl font-bold">
                  {metric.homeValue}{metric.unit}
                </div>
                <div className="text-xs text-gray-400">{homeTeam}</div>
              </div>
            </div>
            <div className="mt-2 text-xs text-center">
              {getAdvantageText(metric, homeTeam, awayTeam)}
            </div>
          </div>
        ))}
      </div>

      <InsightBox
        whatItMeans="Game control metrics show which team dictates pace and field position..."
        whyItMatters={`${homeLeads > awayLeads ? homeTeam : awayTeam} controls tempo in ${Math.max(homeLeads, awayLeads)} of 5 categories`}
        whoHasEdge={{
          team: homeLeads > awayLeads ? homeTeam : awayTeam,
          reason: 'Superior possession time and turnover margin',
          magnitude: Math.abs(homeLeads - awayLeads) > 2 ? 'significant' : 'moderate'
        }}
        keyDifferences={[
          `Possession: ${formatTime(homeStats.possession_time)} vs ${formatTime(awayStats.possession_time)}`,
          `Turnovers: ${homeStats.turnover_margin > 0 ? '+' : ''}${homeStats.turnover_margin} vs ${awayStats.turnover_margin > 0 ? '+' : ''}${awayStats.turnover_margin}`,
          `Penalties: ${homeStats.penalty_yards} vs ${awayStats.penalty_yards} yards`
        ]}
      />
    </GlassCard>
  );
};

// Helper functions
const parseTimeToMinutes = (timeStr: string): number => {
  const [minutes, seconds] = timeStr.split(':').map(Number);
  return minutes + (seconds / 60);
};

const formatTime = (timeStr: string): string => {
  const [hours, minutes, seconds] = timeStr.split(':');
  return `${hours}:${minutes.padStart(2, '0')}`;
};

const getAdvantageText = (metric: GameControlMetric, homeTeam: string, awayTeam: string): string => {
  const homeWins = metric.inverse 
    ? metric.homeValue < metric.awayValue 
    : metric.homeValue > metric.awayValue;
  
  const winner = homeWins ? homeTeam : awayTeam;
  const diff = Math.abs(metric.homeValue - metric.awayValue);
  
  return `${winner} advantage (${diff.toFixed(1)}${metric.unit || ''})`;
};
```

---

## 📊 Data Mapping

```typescript
// From API response:
predictionData.team_statistics.home = {
  possession_time: "402:05",  // MM:SS format
  turnover_margin: -1,
  penalty_yards: 491,
  games_played: 12,
  drives_per_game: 10.2
}

predictionData.team_statistics.away = {
  possession_time: "398:03",
  turnover_margin: 8,
  penalty_yards: 535,
  games_played: 12,
  drives_per_game: 10.1
}
```

---

## ✨ Interactive Features

1. **Animated Polygon Fill**: Radar polygons animate from center outward
2. **Hover Axis Highlight**: Mouse over metric highlights that radar axis
3. **Click to Expand**: Click metric to see game-by-game breakdown
4. **Advantage Indicators**: Arrow showing which polygon extends further
5. **Benchmark Overlay**: Average team values shown as middle circle
6. **Zoom Controls**: Zoom in/out on specific metrics

---

## 🎨 Theme Customization

```typescript
const gameControlTheme = {
  background: 'transparent',
  radarGridColor: 'rgba(255, 255, 255, 0.1)',
  homePolygonFill: homeColor + '30',
  awayPolygonFill: awayColor + '30',
  homePolygonStroke: homeColor,
  awayPolygonStroke: awayColor,
  advantageHighlight: 'rgba(76, 175, 80, 0.2)',
};
```

---

## 🧪 Testing Checklist

- [ ] Radar chart renders with 5 axes
- [ ] Polygons fill with team colors (20-30% opacity)
- [ ] Tooltips show detailed metric values
- [ ] Leader count matches visual comparison
- [ ] Animations smooth (polygon grows from center)
- [ ] Responsive (mobile uses stacked bars instead)
- [ ] Possession time parsing works correctly

---

## 🚀 Alternative: Horizontal Timeline

For **tempo visualization over quarters**:

```typescript
// X-axis = game time (Q1-Q4)
// Y-axis = possession percentage
// Shows which team controlled each quarter
// Stacked area chart with possession splits
```

---

**Status**: Ready to implement  
**Estimated Time**: 3-4 hours  
**Priority**: High - tempo and control visualization  
**Impact**: Professional radar analytics showing game control dominance
