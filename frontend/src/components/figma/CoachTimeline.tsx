import React, { useEffect, useRef, useState } from 'react';
import Highcharts from 'highcharts';
import fbsTeams from '../../fbs.json';

// Team lookup function to get data from fbs.json
const getTeamData = (schoolName: string) => {
  if (!schoolName) return null;
  const normalizedSearch = schoolName.toLowerCase().trim();
  
  const team = (fbsTeams as any[]).find((t: any) => {
    const schoolMatch = t.school?.toLowerCase() === normalizedSearch;
    const alt1Match = t.alt_name1?.toLowerCase() === normalizedSearch;
    const alt2Match = t.alt_name2?.toLowerCase() === normalizedSearch;
    const alt3Match = t.alt_name3?.toLowerCase() === normalizedSearch;
    return schoolMatch || alt1Match || alt2Match || alt3Match;
  });
  
  if (team) {
    return {
      ...team,
      color: team.primary_color || team.color || team.alt_color
    };
  }
  
  return null;
};

interface CoachTimelineProps {
  coachName: string;
  schoolName: string;
  teamColor: string;
  teamLogo: string;
  timelineData?: any;
}

interface SchoolModalData {
  name: string;
  logo: string;
  color: string;
  years: string;
  record: string;
  winPct: string;
  achievements: string[];
  notableSeasons: string[];
  legacy: string[];
}

export const CoachTimeline: React.FC<CoachTimelineProps> = ({ 
  coachName, 
  schoolName, 
  teamColor,
  teamLogo,
  timelineData 
}) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<Highcharts.Chart | null>(null);
  const [selectedSchool, setSelectedSchool] = useState<SchoolModalData | null>(null);
  const [currentFilter, setCurrentFilter] = useState<string>('all');

  // Use timeline data colors as fallback
  const effectiveColor = React.useMemo(() => 
    timelineData?.teamColor || teamColor, 
    [timelineData, teamColor]
  );
  
  const effectiveLogo = React.useMemo(() => 
    timelineData?.teamLogo || teamLogo, 
    [timelineData, teamLogo]
  );
  
  const coachHeadshot = React.useMemo(() => 
    timelineData?.coachHeadshot || '', 
    [timelineData]
  );

  // Get career schools data if available and enrich with fbs.json data
  const careerSchools = React.useMemo(() => {
    if (!timelineData?.career_schools) return [];
    
    return timelineData.career_schools.map((school: any) => {
      const schoolName = school.school_name || school.school || '';
      const teamData = getTeamData(schoolName);
      
      // Get proper color and logo from fbs.json, fallback to school data
      const color = teamData?.color || school.team_color || school.teamColor;
      const logo = teamData?.logos?.[0] || school.team_logo || school.teamLogo;
      
      // If still no valid color/logo, use defaults
      const finalColor = (color && color !== '#000000') ? color : teamColor;
      const finalLogo = logo || `https://a.espncdn.com/i/teamlogos/ncaa/500/default.png`;
      
      console.log('🎨 Enriching school:', schoolName, '| teamData.color:', teamData?.color, '| finalColor:', finalColor);
      
      return {
        ...school,
        school_name: schoolName,
        school: schoolName,
        team_color: finalColor,
        teamColor: finalColor,
        team_logo: finalLogo,
        teamLogo: finalLogo
      };
    });
  }, [timelineData, teamColor]);
  
  const hasMultipleSchools = React.useMemo(() => 
    careerSchools.length > 1, 
    [careerSchools]
  );

  useEffect(() => {
    if (!chartRef.current || !timelineData) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const { data, metadata } = timelineData;

    // Create chart with proper type casting
    if (!chartRef.current) return;
    
    const chartOptions: Highcharts.Options = {
      chart: {
        type: 'area',
        backgroundColor: `${effectiveColor}05`,
        height: 300,
        zooming: {
          type: 'x'
        }
      },

      title: {
        text: hasMultipleSchools ? `${coachName} Career Timeline - All Schools` : `AP Poll Rankings Timeline`,
        align: 'left',
        style: {
          color: hasMultipleSchools ? '#fff' : effectiveColor,
          fontSize: '14px',
          fontWeight: 'bold'
        }
      },

      subtitle: {
        text: hasMultipleSchools
          ? `Career: ${metadata.record || ''} (${metadata.win_pct || '0'}% Win Rate) • ${careerSchools.length} Schools • Click logos to view details`
          : `${metadata.record || ''} at ${schoolName} (${metadata.win_pct || '0'}% Win Rate)`,
        align: 'left',
        style: {
          color: '#94a3b8',
          fontSize: '11px'
        }
      },

      credits: {
        enabled: false
      },

      xAxis: {
        type: 'datetime',
        labels: {
          style: {
            color: '#94a3b8'
          }
        },
        gridLineColor: 'rgba(148, 163, 184, 0.1)',
        title: {
          text: hasMultipleSchools ? 'Coaching Timeline - Click team logos to view details' : 'Season Timeline',
          style: {
            color: '#94a3b8',
            fontSize: '11px'
          }
        },
        // Add plotBands for each school - flexible field names
        plotBands: hasMultipleSchools ? careerSchools.map((school: any, index: number) => {
          // Handle flexible field names
          const schoolName = school.school_name || school.school || 'Unknown';
          const schoolColor = school.team_color || school.teamColor || teamColor;
          const schoolLogo = school.team_logo || school.teamLogo || 'https://a.espncdn.com/i/teamlogos/ncaa/500/default.png';
          const years = school.years || '';
          
          // Parse years to get date range
          const yearParts = years.split('-');
          const startYear = parseInt(yearParts[0]?.trim() || new Date().getFullYear().toString());
          const endYear = yearParts[1] ? parseInt(yearParts[1].trim()) : new Date().getFullYear();
          
          return {
            from: Date.UTC(startYear, 0, 1),
            to: Date.UTC(endYear || new Date().getFullYear(), 11, 31),
            color: `${schoolColor}08`,
            label: {
              useHTML: true,
              text: `<div style="cursor: pointer; text-align: center;" data-school-index="${index}">
                      <img src="${schoolLogo}" style="width: 28px; height: 28px; display: block; margin: 0 auto 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));" onerror="this.style.display='none'" />
                      <div style="font-size: 10px; font-weight: 600; color: ${schoolColor}; text-shadow: 0 1px 3px rgba(0,0,0,0.5);">${schoolName}</div>
                      <div style="font-size: 9px; color: rgba(255,255,255,0.6);">${years}</div>
                    </div>`,
              align: 'center',
              y: -35
            },
            zIndex: 3
          };
        }) : []
      },

      yAxis: {
        title: {
          text: 'AP Poll Ranking',
          style: {
            color: '#94a3b8',
            fontSize: '14px'
          }
        },
        labels: {
          formatter: function(): string {
            const rank: number = 26 - (this.value as number);
            if (rank <= 0) return '';
            if (rank === 1) return '#1 🏆';
            if (rank <= 5) return '#' + rank;
            if (rank <= 10) return '#' + rank;
            if (rank <= 25) return '#' + rank;
            return 'Unranked';
          },
          style: {
            color: '#94a3b8'
          }
        },
        min: 0,
        max: 25,
        tickInterval: 5,
        gridLineColor: 'rgba(148, 163, 184, 0.1)',
        gridLineDashStyle: 'Dash'
      },

      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: effectiveColor,
        style: {
          color: '#fff'
        },
        formatter: function(): string {
          const rank: number = 26 - ((this as any).y || 0);
          const rankText: string = rank === 1 ? '#1 🏆' : '#' + rank;
          return '<b>' + Highcharts.dateFormat('%B %e, %Y', (this as any).x as number) + '</b><br/>' +
                 'AP Poll Rank: <b>' + rankText + '</b>';
        }
      },

      legend: {
        enabled: false
      },

      plotOptions: {
        area: {
          fillOpacity: 0.5,
          lineWidth: 2,
          marker: {
            enabled: false,
            states: {
              hover: {
                enabled: true,
                radius: 4
              }
            }
          }
        }
      },

      series: [{
        type: 'area',
        name: 'AP Poll Ranking',
        data: data,
        lineWidth: 3,
        // Use zones for multi-school color coding - flexible field names
        ...(hasMultipleSchools && careerSchools.length > 0 ? {
          zoneAxis: 'x',
          zones: (() => {
            const zonesArray = careerSchools.map((school: any, index: number) => {
            // Handle flexible field names
            const schoolColor = school.team_color || school.teamColor || teamColor;
            const isLast = index === careerSchools.length - 1;
            
            console.log('🔵 Zone', index, '| School:', school.school_name, '| Color:', schoolColor, '| team_color:', school.team_color, '| teamColor:', school.teamColor);
            
            // Calculate zone boundary based on NEXT school's START year
            let zoneValue;
            if (!isLast) {
              const nextSchool = careerSchools[index + 1];
              const nextYears = nextSchool.years || '';
              const nextStartYear = parseInt(nextYears.split('-')[0]?.trim() || '2100');
              zoneValue = Date.UTC(nextStartYear, 0, 1); // Start of next school's first year
            }
            
            return {
              value: zoneValue,
              color: schoolColor,
              fillColor: {
                linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                stops: [
                  [0, `${schoolColor}cc`],
                  [0.5, `${schoolColor}66`],
                  [1, `${schoolColor}1a`]
                ]
              }
            };
            });
            console.log('📊 Final zones array:', JSON.stringify(zonesArray, null, 2));
            return zonesArray;
          })()
        } : {
          color: effectiveColor,
          fillColor: {
            linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
            stops: [
              [0, `${effectiveColor}cc`],
              [0.5, `${effectiveColor}66`],
              [1, `${effectiveColor}1a`]
            ]
          }
        })
      }]
    };

    chartInstance.current = Highcharts.chart(chartRef.current, chartOptions);

    // Add click handlers to plotBand logos
    if (hasMultipleSchools && chartRef.current) {
      setTimeout(() => {
        const logoElements = chartRef.current?.querySelectorAll('[data-school-index]');
        logoElements?.forEach((element) => {
          element.addEventListener('click', (e) => {
            const schoolIndex = parseInt((e.currentTarget as HTMLElement).getAttribute('data-school-index') || '0');
            const school = careerSchools[schoolIndex];
            if (school) {
              setSelectedSchool(getSchoolModalData(school));
            }
          });
        });
      }, 100);
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [timelineData, coachName, schoolName, teamColor, teamLogo, hasMultipleSchools, careerSchools]);

  // Generate school modal data from career_schools - flexible field names
  const getSchoolModalData = (school: any): SchoolModalData | null => {
    if (!school) return null;
    
    // Handle multiple possible field name formats
    const schoolName = school.school_name || school.school || 'Unknown School';
    const schoolColor = school.team_color || school.teamColor || teamColor;
    const schoolLogo = school.team_logo || school.teamLogo || `https://a.espncdn.com/i/teamlogos/ncaa/500/default.png`;
    const winPct = typeof school.win_pct === 'number' ? school.win_pct.toFixed(1) : (school.win_pct || '0');
    
    return {
      name: schoolName,
      logo: schoolLogo,
      color: schoolColor,
      years: school.years || '',
      record: school.record || '',
      winPct: winPct,
      achievements: school.major_achievements || school.achievements || [],
      notableSeasons: school.notable_seasons || school.seasons || [],
      legacy: school.legacy_impact || school.legacy || []
    };
  };

  if (!timelineData) {
    return (
      <div className="glassmorphism p-6 rounded-xl text-center">
        <p className="text-gray-400">Timeline data not available for {coachName}</p>
      </div>
    );
  }

  return (
    <div className="glassmorphism p-6 rounded-xl" style={{
      border: `2px solid ${effectiveColor}40`,
      boxShadow: `0 8px 32px ${effectiveColor}20`
    }}>
      {/* Team Header with Logo and Coach Photo */}
      <div className="flex items-center gap-4 mb-4 pb-4 border-b border-white/10">
        {/* Team Logo */}
        <img 
          src={effectiveLogo} 
          alt={schoolName}
          className="w-14 h-14 object-contain"
        />
        
        {/* Coach Photo */}
        {coachHeadshot && (
          <img 
            src={coachHeadshot} 
            alt={coachName}
            className="w-14 h-14 rounded-full object-cover"
            style={{
              border: `2px solid ${effectiveColor}`,
              boxShadow: `0 4px 16px ${effectiveColor}40`
            }}
          />
        )}
        
        <div className="flex-1">
          <h4 className="text-lg font-bold text-white">{schoolName}</h4>
          <p className="text-sm text-gray-400">{coachName}</p>
        </div>
      </div>

      <div ref={chartRef} style={{ width: '100%', height: '300px' }} />
      
      {/* Metadata stats */}
      {timelineData.metadata && (
        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t" style={{ borderColor: `${effectiveColor}30` }}>
          <div className="text-center p-3 rounded-lg" style={{ 
            background: `linear-gradient(135deg, ${effectiveColor}15, rgba(15, 23, 42, 0.8))`,
            border: `1px solid ${effectiveColor}30`
          }}>
            <div className="text-xs text-gray-400 mb-1">Peak Talent</div>
            <div className="text-lg font-bold" style={{ color: effectiveColor }}>
              {timelineData.metadata.peak_talent?.talent ? timelineData.metadata.peak_talent.talent.toFixed(1) : '-'}
            </div>
            <div className="text-xs text-gray-500">
              {timelineData.metadata.peak_talent?.year || ''}
            </div>
          </div>
        <div className="text-center p-3 rounded-lg" style={{ 
          background: `linear-gradient(135deg, ${effectiveColor}15, rgba(15, 23, 42, 0.8))`,
          border: `1px solid ${effectiveColor}30`
        }}>
          <div className="text-xs text-gray-400 mb-1">Top Draft Year</div>
          <div className="text-lg font-bold" style={{ color: effectiveColor }}>
            {timelineData.metadata.top_draft_years?.[0]?.total || 0} picks
          </div>
          <div className="text-xs text-gray-500">
            {timelineData.metadata.top_draft_years?.[0]?.year || 'N/A'} {timelineData.metadata.top_draft_years?.[0]?.round1 ? `(${timelineData.metadata.top_draft_years[0].round1} Rd 1)` : ''}
          </div>
        </div>
        <div className="text-center p-3 rounded-lg" style={{ 
          background: `linear-gradient(135deg, ${effectiveColor}15, rgba(15, 23, 42, 0.8))`,
          border: `1px solid ${effectiveColor}30`
        }}>
          <div className="text-xs text-gray-400 mb-1">#1 Rankings</div>
          <div className="text-lg font-bold" style={{ color: effectiveColor }}>
            {timelineData.metadata.top_rankings_count || 0}
          </div>
          <div className="text-xs text-gray-500">
            {(timelineData.metadata.top_rankings_count || 0) > 0 ? 'weeks at #1' : 'never ranked #1'}
          </div>
        </div>
        </div>
      )}
      
      {/* Career Schools Grid - Only show if multiple schools */}
      {hasMultipleSchools && careerSchools.length > 0 && (
        <div className="mt-6 pt-6 border-t" style={{ borderColor: `${effectiveColor}30` }}>
          <h4 className="text-lg font-bold text-white mb-4">Coaching Career</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {careerSchools.map((school: any, index: number) => {
              // Handle flexible field names
              const schoolName = school.school_name || school.school || 'Unknown School';
              const schoolColor = school.team_color || school.teamColor || teamColor;
              const schoolLogo = school.team_logo || school.teamLogo || 'https://a.espncdn.com/i/teamlogos/ncaa/500/default.png';
              const winPct = typeof school.win_pct === 'number' ? school.win_pct.toFixed(1) : (school.win_pct || '0');
              
              return (
                <div
                  key={index}
                  onClick={() => setSelectedSchool(getSchoolModalData(school))}
                  className="cursor-pointer p-4 rounded-xl transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl relative group"
                  style={{
                    background: `linear-gradient(135deg, ${schoolColor}15, rgba(15, 23, 42, 0.8))`,
                    border: `1px solid ${schoolColor}30`,
                    boxShadow: `0 4px 16px ${schoolColor}20`
                  }}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <img 
                      src={schoolLogo} 
                      alt={schoolName} 
                      className="w-12 h-12 object-contain" 
                      onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
                    />
                    <div className="flex-1">
                      <h5 className="font-bold text-base" style={{ color: schoolColor }}>
                        {schoolName}
                      </h5>
                      <p className="text-xs text-gray-400">{school.years || 'N/A'}</p>
                    </div>
                    {/* View Details Icon */}
                    <div className="opacity-50 group-hover:opacity-100 transition-opacity">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="text-center p-2 rounded-lg" style={{ 
                      background: `${schoolColor}10`,
                      border: `1px solid ${schoolColor}20`
                    }}>
                      <div className="text-lg font-bold" style={{ color: schoolColor }}>
                        {school.record || 'N/A'}
                      </div>
                      <div className="text-xs text-gray-400">Record</div>
                    </div>
                    <div className="text-center p-2 rounded-lg" style={{ 
                      background: `${schoolColor}10`,
                      border: `1px solid ${schoolColor}20`
                    }}>
                      <div className="text-lg font-bold" style={{ color: schoolColor }}>
                        {winPct}%
                      </div>
                      <div className="text-xs text-gray-400">Win %</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
      
      {/* School Detail Modal */}
      {selectedSchool && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          style={{
            background: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(10px)',
            animation: 'fadeIn 0.3s ease'
          }}
          onClick={() => setSelectedSchool(null)}
        >
          <div 
            className="relative max-w-3xl w-full max-h-[90vh] overflow-y-auto rounded-3xl"
            style={{
              background: 'rgba(15, 23, 42, 0.95)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 20px 60px rgba(0, 0, 0, 0.6)',
              animation: 'slideUp 0.4s ease'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div 
              className="flex items-center justify-between p-8 border-b"
              style={{ borderColor: 'rgba(255, 255, 255, 0.1)' }}
            >
              <div className="flex items-center gap-6">
                <img 
                  src={selectedSchool.logo} 
                  alt={selectedSchool.name}
                  className="w-20 h-20 object-contain"
                  style={{
                    filter: 'drop-shadow(0 4px 20px rgba(0, 0, 0, 0.3))'
                  }}
                />
                <div>
                  <h2 
                    className="text-3xl font-extrabold"
                    style={{ 
                      color: selectedSchool.color,
                      letterSpacing: '-0.5px'
                    }}
                  >
                    {selectedSchool.name} Era
                  </h2>
                  <p className="text-white/80 mt-1">{selectedSchool.years}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedSchool(null)}
                className="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300 hover:rotate-90"
                style={{
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  color: 'rgba(255, 255, 255, 0.6)'
                }}
              >
                <span className="text-3xl font-light">×</span>
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-8">
              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div 
                  className="text-center p-5 rounded-2xl"
                  style={{
                    background: 'rgba(255, 255, 255, 0.08)',
                    backdropFilter: 'blur(5px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}
                >
                  <div className="text-3xl font-extrabold mb-2" style={{ color: selectedSchool.color }}>
                    {selectedSchool.record}
                  </div>
                  <div className="text-sm text-gray-400 uppercase tracking-wider">Overall Record</div>
                </div>
                <div 
                  className="text-center p-5 rounded-2xl"
                  style={{
                    background: 'rgba(255, 255, 255, 0.08)',
                    backdropFilter: 'blur(5px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}
                >
                  <div className="text-3xl font-extrabold mb-2" style={{ color: selectedSchool.color }}>
                    {selectedSchool.winPct}%
                  </div>
                  <div className="text-sm text-gray-400 uppercase tracking-wider">Win Percentage</div>
                </div>
              </div>

              {/* Achievements */}
              {selectedSchool.achievements && selectedSchool.achievements.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-xl font-bold text-white/95 mb-4" style={{ color: selectedSchool.color }}>
                    Major Achievements
                  </h3>
                  <ul className="space-y-3">
                    {selectedSchool.achievements.map((achievement, idx) => (
                      <li 
                        key={idx}
                        className="p-4 rounded-xl text-white/90"
                        style={{
                          background: 'rgba(255, 255, 255, 0.05)',
                          borderLeft: `3px solid ${selectedSchool.color}`
                        }}
                      >
                        {achievement}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Notable Seasons */}
              {selectedSchool.notableSeasons && selectedSchool.notableSeasons.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-xl font-bold text-white/95 mb-4" style={{ color: selectedSchool.color }}>
                    Notable Seasons
                  </h3>
                  <ul className="space-y-3">
                    {selectedSchool.notableSeasons.map((season, idx) => (
                      <li 
                        key={idx}
                        className="p-4 rounded-xl text-white/90"
                        style={{
                          background: 'rgba(255, 255, 255, 0.05)',
                          borderLeft: `3px solid rgba(255, 255, 255, 0.3)`
                        }}
                      >
                        {season}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Legacy */}
              {selectedSchool.legacy && selectedSchool.legacy.length > 0 && (
                <div>
                  <h3 className="text-xl font-bold text-white/95 mb-4" style={{ color: selectedSchool.color }}>
                    Legacy & Impact
                  </h3>
                  <ul className="space-y-3">
                    {selectedSchool.legacy.map((item, idx) => (
                      <li 
                        key={idx}
                        className="p-4 rounded-xl text-white/90"
                        style={{
                          background: 'rgba(255, 255, 255, 0.05)',
                          borderLeft: `3px solid ${selectedSchool.color}`
                        }}
                      >
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
