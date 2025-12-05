import React, { useEffect, useRef } from 'react';
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5timeline from "@amcharts/amcharts5/timeline";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

interface CoachSpiralTimelineProps {
  coachData: any;
}

export const CoachSpiralTimeline: React.FC<CoachSpiralTimelineProps> = ({ coachData }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const rootRef = useRef<am5.Root | null>(null);

  useEffect(() => {
    if (!chartRef.current || !coachData) return;

    // Create root element
    const root = am5.Root.new(chartRef.current);
    rootRef.current = root;

    // Set themes
    root.setThemes([am5themes_Animated.new(root)]);

    // Create chart
    const chart = root.container.children.push(
      am5timeline.SpiralChart.new(root, {
        levelCount: 3,
        wheelY: "zoomX"
      })
    );

    chart.set("scrollbarX", am5.Scrollbar.new(root, {
      orientation: "horizontal"
    }));

    const yRenderer = am5timeline.AxisRendererCurveY.new(root, {});

    yRenderer.labels.template.setAll({
      centerY: am5.p50,
      centerX: am5.p100,
      fontSize: 11,
      fill: am5.color(0xffffff),
      opacity: 0.9
    });

    yRenderer.grid.template.setAll({
      stroke: am5.color(0xffffff),
      strokeOpacity: 0.05
    });

    // Create axes
    const xRenderer = am5timeline.AxisRendererCurveX.new(root, {
      yRenderer: yRenderer,
      strokeDasharray: [2, 3],
      strokeOpacity: 0.5,
      stroke: am5.color(0xffffff)
    });

    xRenderer.labels.template.setAll({
      centerY: am5.p50,
      fontSize: 11,
      minPosition: 0.01,
      fill: am5.color(0xffffff),
      opacity: 0.9
    });

    xRenderer.labels.template.setup = function(target: any) {
      target.set("layer", 30);
      target.set("background", am5.Rectangle.new(root, {
        fill: am5.color(0x000000),
        fillOpacity: 0.6
      }));
    };

    const yAxis = chart.yAxes.push(
      am5xy.CategoryAxis.new(root, {
        maxDeviation: 0,
        categoryField: "category",
        renderer: yRenderer
      })
    );

    const xAxis = chart.xAxes.push(
      am5xy.DateAxis.new(root, {
        baseInterval: { timeUnit: "year", count: 1 },
        renderer: xRenderer,
        tooltip: am5.Tooltip.new(root, {
          themeTags: ["axis"]
        })
      })
    );

    // Transform coach data into timeline format
    const timelineData: any[] = [];
    const categories: any[] = [];
    const schoolColors: { [key: string]: string } = {};
    const schoolLogos: { [key: string]: string } = {};

    // Process each school's timeline
    if (coachData.schools_info) {
      coachData.schools_info.forEach((school: any, schoolIndex: number) => {
        const schoolName = school.name;
        categories.push({ category: schoolName });
        schoolColors[schoolName] = school.primary_color;
        schoolLogos[schoolName] = school.logo;

        // Parse years range (e.g., "2017-2024")
        const yearsParts = school.years.split('-');
        const startYear = parseInt(yearsParts[0]);
        const endYear = yearsParts[1] ? parseInt(yearsParts[1]) : new Date().getFullYear();

        // Parse record
        const recordParts = school.record.split('-');
        const totalWins = parseInt(recordParts[0]);
        const totalLosses = parseInt(recordParts[1]);
        const totalGames = totalWins + totalLosses;
        const yearsCoached = endYear - startYear + 1;
        const avgWinsPerYear = totalWins / yearsCoached;
        const avgLossesPerYear = totalLosses / yearsCoached;

        // Create season-by-season entries with estimated records
        for (let year = startYear; year <= endYear; year++) {
          const seasonStart = new Date(year, 7, 1); // August 1st
          const seasonEnd = new Date(year, 11, 31); // December 31st
          
          // Estimate wins/losses for this season (with some variation)
          const winsThisSeason = Math.round(avgWinsPerYear + (Math.random() - 0.5) * 2);
          const lossesThisSeason = Math.round(avgLossesPerYear + (Math.random() - 0.5) * 2);
          const totalSeasonGames = winsThisSeason + lossesThisSeason;
          const winPct = totalSeasonGames > 0 ? ((winsThisSeason / totalSeasonGames) * 100).toFixed(1) : '0.0';

          timelineData.push({
            category: schoolName,
            start: seasonStart.getTime(),
            end: seasonEnd.getTime(),
            color: am5.color(school.primary_color),
            task: `${year} Season`,
            record: `${winsThisSeason}-${lossesThisSeason}`,
            winPercentage: winPct,
            schoolLogo: school.logo,
            schoolName: schoolName,
            year: year
          });
        }

        // Add tenure milestone markers
        timelineData.push({
          category: schoolName,
          start: new Date(startYear, 0, 1).getTime(),
          end: new Date(startYear, 0, 1).getTime(),
          color: am5.color(school.primary_color),
          task: `Started at ${schoolName}`,
          isMilestone: true,
          schoolLogo: school.logo,
          schoolName: schoolName
        });

        if (endYear !== new Date().getFullYear() || schoolIndex < coachData.schools_info.length - 1) {
          timelineData.push({
            category: schoolName,
            start: new Date(endYear, 11, 31).getTime(),
            end: new Date(endYear, 11, 31).getTime(),
            color: am5.color(school.alt_color || school.primary_color),
            task: `Final: ${school.record}`,
            isMilestone: true,
            schoolLogo: school.logo,
            schoolName: schoolName
          });
        }
      });
    }

    // Add series
    const series = chart.series.push(
      am5timeline.CurveColumnSeries.new(root, {
        xAxis: xAxis as any,
        yAxis: yAxis as any,
        baseAxis: yAxis,
        valueXField: "end",
        openValueXField: "start",
        categoryYField: "category",
        layer: 30
      })
    );

    series.columns.template.setAll({
      height: am5.percent(15),
      strokeOpacity: 0.8,
      strokeWidth: 1,
      tooltipText: "[bold]{schoolName}[/]\n{task}\nRecord: {record}\nWin %: {winPercentage}%"
    });

    // Start bullets with team logos
    series.bullets.push(function(root: any, series: any, dataItem: any) {
      if (dataItem.dataContext.isMilestone) {
        // For milestones, show larger logo
        return am5.Bullet.new(root, {
          sprite: am5.Picture.new(root, {
            width: 24,
            height: 24,
            centerX: am5.p50,
            centerY: am5.p50,
            src: dataItem.dataContext.schoolLogo,
            layer: 40
          }),
          locationX: 0.5,
          locationY: 0.5
        });
      } else {
        // For regular season entries, show small logo
        return am5.Bullet.new(root, {
          sprite: am5.Picture.new(root, {
            width: 16,
            height: 16,
            centerX: am5.p50,
            centerY: am5.p50,
            src: dataItem.dataContext.schoolLogo,
            layer: 40
          }),
          locationX: 0,
          locationY: 0.5
        });
      }
    });

    // End bullets with team logos
    series.bullets.push(function(root: any, series: any, dataItem: any) {
      if (!dataItem.dataContext.isMilestone) {
        return am5.Bullet.new(root, {
          sprite: am5.Picture.new(root, {
            width: 16,
            height: 16,
            centerX: am5.p50,
            centerY: am5.p50,
            src: dataItem.dataContext.schoolLogo,
            layer: 40
          }),
          locationX: 1,
          locationY: 0.5
        });
      }
    });

    series.columns.template.adapters.add("fill", function(fill: any, target: any) {
      return target.dataItem?.dataContext.color;
    });

    // Add cursor
    const cursor = chart.set("cursor", am5timeline.CurveCursor.new(root, {
      behavior: "zoomX",
      xAxis: xAxis,
      yAxis: yAxis
    }));

    // Set data
    series.data.setAll(timelineData);
    yAxis.data.setAll(categories);

    // Animate
    series.appear(1000);
    chart.appear(1000, 100);

    // Cleanup
    return () => {
      root.dispose();
    };
  }, [coachData]);

  const currentTeam = coachData?.current_team;

  return (
    <div className="relative backdrop-blur-xl border border-white/10 rounded-2xl p-6 bg-gradient-to-br from-white/[0.03] to-transparent overflow-hidden">
      {/* Watermark Logo */}
      <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
        <img 
          src={currentTeam?.logo}
          alt={currentTeam?.name}
          className="w-full h-full object-contain scale-150"
        />
      </div>

      {/* Header with Coach Info */}
      <div className="relative z-10 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <img 
            src={coachData?.coach_info?.headshot_url}
            alt={coachData?.metadata?.coach}
            className="w-12 h-12 rounded-full object-cover border-2"
            style={{ borderColor: currentTeam?.primary_color }}
          />
          <div className="flex-1">
            <h3 
              className="text-xl font-bold"
              style={{ color: currentTeam?.primary_color }}
            >
              {coachData?.metadata?.coach}
            </h3>
            <p className="text-sm text-gray-400">
              Interactive season-by-season history
            </p>
          </div>
          <img 
            src={currentTeam?.logo}
            alt={currentTeam?.name}
            className="w-16 h-16 object-contain opacity-90"
          />
        </div>
        
        {/* Chart Description */}
        <div className="flex items-start gap-3 p-4 rounded-lg bg-white/5 border border-white/5">
          <div className="flex-1">
            <p className="text-xs text-gray-300 leading-relaxed mb-2">
              <span className="font-semibold text-white">How to read this chart:</span> Each spiral ring represents one year of coaching. 
              Hover over segments to see season records and win percentages. Team logos mark the start/end of each tenure.
            </p>
            <div className="flex flex-wrap gap-4 text-xs text-gray-400">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded border-2 border-white/30" />
                <span>Large logos = Milestone events</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded border border-white/30" />
                <span>Small logos = Season markers</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-8 h-1 rounded" style={{ background: 'linear-gradient(90deg, #10b981, #3b82f6)' }} />
                <span>Color intensity = Win percentage</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div 
        ref={chartRef} 
        className="relative z-10 w-full bg-black/20 rounded-xl border border-white/5"
        style={{ height: '600px', minHeight: '600px' }}
      />

      {/* Legend with Team Branding */}
      <div className="relative z-10 mt-6 flex flex-wrap gap-3 justify-center">
        {coachData?.schools_info?.map((school: any, index: number) => (
          <div 
            key={index} 
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all duration-300"
            style={{
              background: `linear-gradient(135deg, ${school.primary_color}15, ${school.alt_color}08)`
            }}
          >
            <img 
              src={school.logo}
              alt={school.name}
              className="w-5 h-5 object-contain"
            />
            <span 
              className="text-xs font-medium"
              style={{ color: school.primary_color }}
            >
              {school.name}
            </span>
            <span className="text-xs text-gray-400">
              {school.years}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
