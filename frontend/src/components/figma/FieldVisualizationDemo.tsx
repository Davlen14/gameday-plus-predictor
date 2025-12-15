import React from 'react';
import FieldVisualizationModern from './FieldVisualizationModern';

// Demo component showing the new FieldVisualizationModern with sample data
const FieldVisualizationDemo: React.FC = () => {
  // Sample data matching the screenshot you showed
  const sampleData = {
    quarter: 4,
    score: {
      home: 31,
      away: 21
    },
    possession: {
      team: 'Tulane',
      logo: 'https://a.espncdn.com/i/teamlogos/ncaa/500/2655.png'
    },
    fieldPosition: {
      yardLine: 41,
      down: 2,
      distance: 9
    },
    homeTeam: {
      name: 'North Texas',
      abbr: 'UNT',
      color: '#00853E',
      logo: 'https://a.espncdn.com/i/teamlogos/ncaa/500/249.png'
    },
    awayTeam: {
      name: 'Tulane',
      abbr: 'TULN',
      color: '#006747',
      logo: 'https://a.espncdn.com/i/teamlogos/ncaa/500/2655.png'
    },
    driveStats: {
      plays: 6,
      yards: 37,
      timeOfPossession: '3:31',
      thirdDowns: '0/1',
      redZone: false,
      result: 'inProgress' as const
    },
    keyPlayers: [
      {
        name: 'Javin Gordon',
        number: '23',
        position: 'RB',
        image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4430810.png',
        stats: {
          primary: { label: 'CAR', value: 9 },
          secondary: { label: 'YDS', value: 18 },
          tertiary: { label: 'TD', value: 0 }
        }
      },
      {
        name: "S'Maje Burrell",
        number: '26',
        position: 'LB',
        image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4567890.png',
        stats: {
          primary: { label: 'TOT', value: 1 },
          secondary: { label: 'SOLO', value: 1 },
          tertiary: { label: 'TFL', value: 0 }
        }
      }
    ],
    recentPlays: [
      {
        id: 'play-1',
        quarter: 4,
        time: '7:21',
        down: '1st',
        distance: 10,
        yardLine: 'TULN 41',
        description: 'No Huddle-Shotgun #23 J.Gordon rush right for 1 yard gain to the TLN41 (#26 S.Burrell)',
        yards: 1,
        playType: 'run' as const,
        player: {
          name: 'Javin Gordon',
          number: '23',
          image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4430810.png'
        }
      },
      {
        id: 'play-2',
        quarter: 3,
        time: '0:00',
        down: '4th',
        distance: 1,
        yardLine: 'UNT 1',
        description: '#5 M.Pratt pass complete short right to #18 A.Keys for 60 yards to the UNT1 (TOUCHDOWN)',
        yards: 60,
        playType: 'touchdown' as const,
        player: {
          name: 'Makhi Hughes',
          number: '5',
          image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4567123.png'
        }
      },
      {
        id: 'play-3',
        quarter: 3,
        time: '2:50',
        down: '3rd',
        distance: 7,
        yardLine: 'UNT 31',
        description: '#8 C.McDonald punt 19 yards to the UNT19',
        yards: -19,
        playType: 'punt' as const
      },
      {
        id: 'play-4',
        quarter: 3,
        time: '3:34',
        down: '2nd',
        distance: 10,
        yardLine: 'UNT 7',
        description: '#12 D.Smith intercepted by #21 J.Johnson at the UNT 7 (TURNOVER)',
        yards: 0,
        playType: 'interception' as const,
        player: {
          name: 'Josh Johnson',
          number: '21',
          image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4456789.png'
        }
      },
      {
        id: 'play-5',
        quarter: 3,
        time: '6:12',
        down: '1st',
        distance: 10,
        yardLine: 'TULN 24',
        description: '#5 M.Hughes rush left for 13 yards gain (1st DOWN)',
        yards: 13,
        playType: 'run' as const,
        player: {
          name: 'Makhi Hughes',
          number: '5',
          image: 'https://a.espncdn.com/i/headshots/college-football/players/full/4567123.png'
        }
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Modern Field Visualization</h1>
          <p className="text-white/60">Enhanced play-by-play with player cards and drive statistics</p>
        </div>
        
        <FieldVisualizationModern {...sampleData} />
        
        {/* Usage Instructions */}
        <div className="mt-12 bg-gradient-to-br from-gray-900/40 to-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 p-6 shadow-2xl">
          <h2 className="text-white text-2xl font-bold mb-4">Features</h2>
          <ul className="text-white/80 space-y-2">
            <li>✅ <strong>Live Score Header</strong> - Quarter indicator with team logos and scores</li>
            <li>✅ <strong>Key Players Sidebar</strong> - Player cards with headshots and stats (3 metrics each)</li>
            <li>✅ <strong>Drive Statistics</strong> - Plays, yards, time of possession, 3rd down conversions</li>
            <li>✅ <strong>Interactive Field</strong> - Animated ball position with team-colored endzones</li>
            <li>✅ <strong>Play-by-Play Timeline</strong> - Recent plays with expandable player details</li>
            <li>✅ <strong>Color-Coded Play Types</strong> - Touchdowns (green), passes (blue), runs (orange), penalties (yellow), interceptions (red)</li>
            <li>✅ <strong>Glassmorphism Design</strong> - Transparent backgrounds with backdrop blur effects</li>
            <li>✅ <strong>Smooth Animations</strong> - Hover effects, transitions, and scale transforms</li>
          </ul>
          
          <h3 className="text-white text-xl font-bold mt-6 mb-3">Integration Example</h3>
          <pre className="bg-black/40 rounded-lg p-4 overflow-x-auto">
            <code className="text-green-400 text-sm">{`import FieldVisualizationModern from './components/figma/FieldVisualizationModern';

// In your prediction component
<FieldVisualizationModern
  quarter={predictionData.game_state?.quarter}
  score={{ home: homeScore, away: awayScore }}
  possession={currentPossession}
  fieldPosition={fieldPos}
  homeTeam={homeTeamData}
  awayTeam={awayTeamData}
  driveStats={currentDrive}
  keyPlayers={topPerformers}
  recentPlays={playByPlayData}
/>`}</code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default FieldVisualizationDemo;
