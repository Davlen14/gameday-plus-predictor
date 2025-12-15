import {
  SciChartSurface,
  NumericAxis,
  EAxisAlignment,
  EAutoRange,
  TextAnnotation,
  ECoordinateMode,
  EHorizontalAnchorPoint,
  EVerticalAnchorPoint,
  NumberRange,
  XyDataSeries,
  FastLineRenderableSeries,
  EllipsePointMarker,
} from 'scichart';

export interface DefensiveMetric {
  name: string;
  homeValue: number;
  awayValue: number;
  unit?: string;
  inverse?: boolean;
}

export const getCircularProgressConfig = (
  metric: DefensiveMetric,
  homeTeam: string,
  awayTeam: string,
  homeColor: string,
  awayColor: string
) => {
  return async (divId: string) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

    // Calculate percentages based on max value
    const maxValue = Math.max(metric.homeValue, metric.awayValue) * 1.2;
    const homePercent = (metric.homeValue / maxValue) * 100;
    const awayPercent = (metric.awayValue / maxValue) * 100;

    // For inverse metrics (lower is better), invert the colors
    const homeDisplayColor = metric.inverse 
      ? (metric.homeValue < metric.awayValue ? '#4ade80' : homeColor)
      : (metric.homeValue > metric.awayValue ? '#4ade80' : homeColor);
    
    const awayDisplayColor = metric.inverse
      ? (metric.awayValue < metric.homeValue ? '#4ade80' : awayColor)
      : (metric.awayValue > metric.homeValue ? '#4ade80' : awayColor);

    // Create polar axes for circular chart
    const angleAxis = new NumericAxis(wasmContext, {
      isVisible: false,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 360),
    });

    const radiusAxis = new NumericAxis(wasmContext, {
      isVisible: false,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, 100),
    });

    sciChartSurface.xAxes.add(angleAxis);
    sciChartSurface.yAxes.add(radiusAxis);

    // Create circular background ring (full circle)
    const bgAngles = [];
    const bgRadii = [];
    for (let angle = 0; angle <= 360; angle += 5) {
      bgAngles.push(angle);
      bgRadii.push(90); // Outer ring
    }

    const bgData = new XyDataSeries(wasmContext, {
      xValues: bgAngles,
      yValues: bgRadii,
    });

    const bgSeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: bgData,
      stroke: 'rgba(255, 255, 255, 0.05)',
      strokeThickness: 8,
    });

    // Create home team progress arc (outer ring)
    const homeAngles = [];
    const homeRadii = [];
    const homeArcLength = (homePercent / 100) * 360;
    for (let angle = 0; angle <= homeArcLength; angle += 5) {
      homeAngles.push(angle);
      homeRadii.push(90);
    }

    const homeData = new XyDataSeries(wasmContext, {
      xValues: homeAngles,
      yValues: homeRadii,
    });

    const homeSeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: homeData,
      stroke: homeDisplayColor,
      strokeThickness: 8,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: homeDisplayColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    // Create away team progress arc (inner ring)
    const awayAngles = [];
    const awayRadii = [];
    const awayArcLength = (awayPercent / 100) * 360;
    for (let angle = 0; angle <= awayArcLength; angle += 5) {
      awayAngles.push(angle);
      awayRadii.push(60);
    }

    const awayData = new XyDataSeries(wasmContext, {
      xValues: awayAngles,
      yValues: awayRadii,
    });

    const awaySeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: awayData,
      stroke: awayDisplayColor,
      strokeThickness: 8,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: awayDisplayColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    // Inner background ring
    const innerBgAngles = [];
    const innerBgRadii = [];
    for (let angle = 0; angle <= 360; angle += 5) {
      innerBgAngles.push(angle);
      innerBgRadii.push(60);
    }

    const innerBgData = new XyDataSeries(wasmContext, {
      xValues: innerBgAngles,
      yValues: innerBgRadii,
    });

    const innerBgSeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: innerBgData,
      stroke: 'rgba(255, 255, 255, 0.05)',
      strokeThickness: 8,
    });

    sciChartSurface.renderableSeries.add(bgSeries, innerBgSeries, homeSeries, awaySeries);

    // Add center text with metric name
    const centerText = new TextAnnotation({
      x1: 0.5,
      y1: 0.5,
      text: metric.name,
      textColor: '#ffffff',
      fontSize: 12,
      fontWeight: 'bold',
      xCoordinateMode: ECoordinateMode.Relative,
      yCoordinateMode: ECoordinateMode.Relative,
      horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
      verticalAnchorPoint: EVerticalAnchorPoint.Center,
    });

    // Add home team value (top)
    const homeValueText = new TextAnnotation({
      x1: 0.5,
      y1: 0.35,
      text: `${homeTeam}: ${metric.homeValue}${metric.unit || ''}`,
      textColor: homeColor,
      fontSize: 10,
      fontWeight: 'bold',
      xCoordinateMode: ECoordinateMode.Relative,
      yCoordinateMode: ECoordinateMode.Relative,
      horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
      verticalAnchorPoint: EVerticalAnchorPoint.Center,
    });

    // Add away team value (bottom)
    const awayValueText = new TextAnnotation({
      x1: 0.5,
      y1: 0.65,
      text: `${awayTeam}: ${metric.awayValue}${metric.unit || ''}`,
      textColor: awayColor,
      fontSize: 10,
      fontWeight: 'bold',
      xCoordinateMode: ECoordinateMode.Relative,
      yCoordinateMode: ECoordinateMode.Relative,
      horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
      verticalAnchorPoint: EVerticalAnchorPoint.Center,
    });

    sciChartSurface.annotations.add(centerText, homeValueText, awayValueText);

    return { sciChartSurface, wasmContext };
  };
};

// Alternative: Create a grid of 8 circular progress indicators
export const createDefensiveGaugeGrid = (
  metrics: DefensiveMetric[],
  homeTeam: string,
  awayTeam: string,
  homeColor: string,
  awayColor: string
) => {
  // Returns configuration for rendering multiple circular gauges
  return metrics.map((metric) => ({
    metric,
    config: getCircularProgressConfig(metric, homeTeam, awayTeam, homeColor, awayColor),
  }));
};
