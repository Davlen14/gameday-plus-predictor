import {
  SciChartSurface,
  NumericAxis,
  EAxisAlignment,
  EAutoRange,
  XyDataSeries,
  FastLineRenderableSeries,
  EllipsePointMarker,
  NumberRange,
  TextAnnotation,
  ECoordinateMode,
  EHorizontalAnchorPoint,
  RolloverModifier,
  MouseWheelZoomModifier,
  ZoomPanModifier,
  EXyDirection,
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
  return async (divId: string | HTMLDivElement) => {
    const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

    // Create standard X/Y axes for radar-like visualization
    const xAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Bottom,
      autoRange: EAutoRange.Never,
      visibleRange: new NumberRange(0, metrics.length),
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      drawLabels: false,
    });

    const yAxis = new NumericAxis(wasmContext, {
      axisAlignment: EAxisAlignment.Left,
      autoRange: EAutoRange.Always,
      drawMajorGridLines: true,
      drawMinorGridLines: false,
      drawLabels: true,
    });

    sciChartSurface.xAxes.add(xAxis);
    sciChartSurface.yAxes.add(yAxis);

    // Normalize values for better visualization
    const allValues = [...metrics.map(m => m.homeValue), ...metrics.map(m => m.awayValue)];
    const maxValue = Math.max(...allValues);

    // Create data series for home team
    const homeXValues = metrics.map((_, i) => i);
    const homeYValues = metrics.map(m => m.inverse ? maxValue - m.homeValue : m.homeValue);

    const homeData = new XyDataSeries(wasmContext, {
      xValues: homeXValues,
      yValues: homeYValues,
      dataSeriesName: homeTeam,
    });

    const homeSeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: homeData,
      stroke: homeColor,
      strokeThickness: 4,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: homeColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    // Create data series for away team
    const awayXValues = metrics.map((_, i) => i);
    const awayYValues = metrics.map(m => m.inverse ? maxValue - m.awayValue : m.awayValue);

    const awayData = new XyDataSeries(wasmContext, {
      xValues: awayXValues,
      yValues: awayYValues,
      dataSeriesName: awayTeam,
    });

    const awaySeries = new FastLineRenderableSeries(wasmContext, {
      dataSeries: awayData,
      stroke: awayColor,
      strokeThickness: 4,
      pointMarker: new EllipsePointMarker(wasmContext, {
        width: 12,
        height: 12,
        fill: awayColor,
        stroke: '#ffffff',
        strokeThickness: 2,
      }),
    });

    sciChartSurface.renderableSeries.add(homeSeries, awaySeries);

    // Add labels for each metric using TextAnnotations
    metrics.forEach((metric, index) => {
      const maxY = Math.max(...homeYValues, ...awayYValues);
      const labelAnnotation = new TextAnnotation({
        x1: index,
        y1: maxY * 1.05,
        text: metric.name,
        textColor: '#ffffff',
        fontSize: 11,
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
    });

    sciChartSurface.chartModifiers.add(rolloverModifier);
    sciChartSurface.chartModifiers.add(new MouseWheelZoomModifier());
    sciChartSurface.chartModifiers.add(new ZoomPanModifier({ xyDirection: EXyDirection.XyDirection }));

    return { sciChartSurface, wasmContext };
  };
};
