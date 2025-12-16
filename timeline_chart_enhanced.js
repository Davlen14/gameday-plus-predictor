// Enhanced Timeline Chart Function - Kirby Smart / Lane Kiffin Style
function renderTimelineChart(data) {
    const weeklyData = data.weekly || [];
    const plotBands = data.plot_bands || [];
    const flags = data.flags || [];
    const yearlyData = data.yearly || [];
    const monthlyData = data.monthly || [];
    
    // Prepare multiple data series
    const weeklyWinPct = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.win_pct]);
    const weeklyHomeWinPct = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.home_win_pct || 0]);
    const weeklyConfWinPct = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.conf_win_pct || 0]);
    const weeklyAPRank = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.ap_rank_score || 0]);
    const weeklyMargin = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.avg_margin || 0]);
    const weeklyWinStreak = weeklyData.filter(w => w.games > 0).map(w => [w.x, w.win_streak || 0]);
    
    // Prepare game-specific data for enhanced tooltips
    const gameData = weeklyData.filter(w => w.games > 0).map(w => ({
        x: w.x,
        y: w.win_pct,
        marker: {
            fillColor: w.win_pct >= 50 ? '#10B981' : '#EF4444',
            lineWidth: 2,
            lineColor: w.win_pct >= 50 ? '#34D399' : '#F87171',
            radius: w.ranked_wins > 0 ? 5 : 3,
            symbol: w.win_streak > 5 ? 'diamond' : 'circle'
        },
        custom: w
    }));
    
    // Convert plotBands with enhanced styling
    const chartPlotBands = plotBands.map(band => ({
        from: band.from,
        to: band.to,
        color: band.color || 'rgba(59, 130, 246, 0.05)',
        borderColor: 'rgba(59, 130, 246, 0.2)',
        borderWidth: 1,
        label: {
            text: band.label,
            align: 'center',
            verticalAlign: 'top',
            y: 20,
            style: {
                color: '#94a3b8',
                fontSize: '11px',
                fontFamily: 'JetBrains Mono, monospace',
                fontWeight: 'bold'
            }
        }
    }));
    
    console.log('Rendering advanced chart with', gameData.length, 'data points');
    
    Highcharts.chart('timeline-chart', {
        chart: {
            backgroundColor: 'transparent',
            style: {
                fontFamily: 'JetBrains Mono, monospace'
            },
            zooming: {
                type: 'x'
            },
            panning: {
                enabled: true,
                type: 'x'
            },
            panKey: 'shift',
            scrollablePlotArea: {
                minWidth: 800,
                scrollPositionX: 1
            }
        },
        title: {
            text: 'Career Analytics: Win %, Rankings, & Performance Metrics',
            style: {
                color: '#ffffff',
                fontSize: '16px',
                fontWeight: 'bold'
            }
        },
        subtitle: {
            text: 'Click and drag to zoom • Hold Shift and drag to pan • Toggle series in legend',
            style: {
                color: '#888',
                fontSize: '11px'
            }
        },
        xAxis: {
            type: 'datetime',
            labels: {
                style: {
                    color: '#94a3b8',
                    fontSize: '11px'
                }
            },
            gridLineColor: 'rgba(255, 255, 255, 0.05)',
            lineColor: 'rgba(255, 255, 255, 0.1)',
            plotBands: chartPlotBands
        },
        yAxis: [
            {
                // Primary axis - Win Percentages
                title: {
                    text: 'Win Percentage',
                    style: {
                        color: '#94a3b8',
                        fontSize: '12px'
                    }
                },
                labels: {
                    format: '{value}%',
                    style: {
                        color: '#94a3b8',
                        fontSize: '11px'
                    }
                },
                gridLineColor: 'rgba(255, 255, 255, 0.05)',
                min: 0,
                max: 100,
                plotLines: [{
                    value: 50,
                    color: 'rgba(239, 68, 68, 0.3)',
                    width: 2,
                    dashStyle: 'Dash',
                    zIndex: 3,
                    label: {
                        text: '.500',
                        style: {
                            color: '#EF4444',
                            fontSize: '10px'
                        }
                    }
                }]
            },
            {
                // Secondary axis - AP Ranking Score
                title: {
                    text: 'AP Ranking Quality',
                    style: {
                        color: '#f59e0b',
                        fontSize: '11px'
                    }
                },
                labels: {
                    style: {
                        color: '#f59e0b',
                        fontSize: '10px'
                    }
                },
                opposite: true,
                gridLineWidth: 0,
                min: 0,
                max: 100
            },
            {
                // Third axis - Point Margin
                title: {
                    text: 'Avg Point Margin',
                    style: {
                        color: '#06b6d4',
                        fontSize: '11px'
                    }
                },
                labels: {
                    format: '{value} pts',
                    style: {
                        color: '#06b6d4',
                        fontSize: '10px'
                    }
                },
                opposite: true,
                gridLineWidth: 0
            },
            {
                // Fourth axis - Win Streak
                title: {
                    text: 'Win Streak',
                    style: {
                        color: '#8b5cf6',
                        fontSize: '11px'
                    }
                },
                labels: {
                    style: {
                        color: '#8b5cf6',
                        fontSize: '10px'
                    }
                },
                opposite: false,
                gridLineWidth: 0,
                min: 0
            }
        ],
        legend: {
            enabled: true,
            itemStyle: {
                color: '#94a3b8',
                fontSize: '11px'
            },
            itemHoverStyle: {
                color: '#ffffff'
            }
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: true,
                    radius: 3,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 6
                        }
                    }
                },
                states: {
                    hover: {
                        lineWidthPlus: 2
                    }
                }
            },
            area: {
                fillOpacity: 0.15,
                lineWidth: 2.5
            }
        },
        tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderRadius: 8,
            style: {
                color: '#e2e8f0',
                fontSize: '11px'
            },
            shared: true,
            crosshairs: true
        },
        series: [
            {
                name: 'Win Percentage',
                type: 'area',
                data: gameData,
                color: '#10B981',
                fillColor: {
                    linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                    stops: [
                        [0, 'rgba(16, 185, 129, 0.3)'],
                        [1, 'rgba(16, 185, 129, 0.0)']
                    ]
                },
                lineWidth: 3,
                zones: [{
                    value: 50,
                    color: '#EF4444',
                    fillColor: {
                        linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                        stops: [
                            [0, 'rgba(239, 68, 68, 0.3)'],
                            [1, 'rgba(239, 68, 68, 0.0)']
                        ]
                    }
                }, {
                    color: '#10B981'
                }],
                tooltip: {
                    valueSuffix: '%',
                    valueDecimals: 1
                },
                yAxis: 0,
                zIndex: 3
            },
            {
                name: 'Home Win %',
                type: 'line',
                data: weeklyHomeWinPct,
                color: '#22d3ee',
                lineWidth: 2,
                dashStyle: 'ShortDot',
                tooltip: {
                    valueSuffix: '%',
                    valueDecimals: 1
                },
                yAxis: 0,
                zIndex: 2,
                visible: false
            },
            {
                name: 'Conference Win %',
                type: 'line',
                data: weeklyConfWinPct,
                color: '#a78bfa',
                lineWidth: 2,
                dashStyle: 'Dot',
                tooltip: {
                    valueSuffix: '%',
                    valueDecimals: 1
                },
                yAxis: 0,
                zIndex: 2,
                visible: false
            },
            {
                name: 'AP Ranking Quality',
                type: 'spline',
                data: weeklyAPRank,
                color: '#f59e0b',
                lineWidth: 2,
                dashStyle: 'ShortDash',
                tooltip: {
                    valueSuffix: ' / 100',
                    valueDecimals: 1
                },
                yAxis: 1,
                zIndex: 2,
                visible: false
            },
            {
                name: 'Avg Point Margin',
                type: 'spline',
                data: weeklyMargin,
                color: '#06b6d4',
                lineWidth: 2,
                tooltip: {
                    valueSuffix: ' pts',
                    valueDecimals: 1
                },
                yAxis: 2,
                zIndex: 2,
                visible: false
            },
            {
                name: 'Win Streak',
                type: 'column',
                data: weeklyWinStreak,
                color: '#8b5cf6',
                tooltip: {
                    valueSuffix: ' games',
                    valueDecimals: 0
                },
                yAxis: 3,
                zIndex: 1,
                visible: false
            }
        ],
        credits: {
            enabled: false
        },
        exporting: {
            enabled: true,
            buttons: {
                contextButton: {
                    theme: {
                        fill: 'rgba(255, 255, 255, 0.05)',
                        stroke: 'rgba(255, 255, 255, 0.1)',
                        states: {
                            hover: {
                                fill: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    }
                }
            }
        }
    });
}
