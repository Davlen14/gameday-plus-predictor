import React, { useState } from 'react';
import './EVBettingDashboard.css';
import fbsData from '../fbs.json';
import { LayoutGrid, Zap, TrendingUp, Calendar, CalendarDays, ArrowLeft } from 'lucide-react';

interface Team {
  id: number;
  school: string;
  mascot: string;
  abbreviation: string;
  conference: string;
  primary_color: string;
  alt_color: string;
  logos: string[];
}

const teams: Team[] = fbsData as Team[];

// Helper function to get team data
const getTeamData = (teamName: string): Team | null => {
  // First try exact match
  const exactMatch = teams.find(t => 
    t.school.toLowerCase() === teamName.toLowerCase()
  );
  if (exactMatch) return exactMatch;
  
  // Then try partial match, but prefer longer matches
  const partialMatches = teams.filter(t => 
    teamName.toLowerCase().includes(t.school.toLowerCase())
  );
  
  // Sort by school name length (descending) to prefer "Ohio State" over "Ohio"
  if (partialMatches.length > 0) {
    return partialMatches.sort((a, b) => b.school.length - a.school.length)[0];
  }
  
  return null;
};

interface PublicBetting {
  ml: { awayBet: number; homeBet: number; awayMoney: number; homeMoney: number };
  spread: { awayBet: number; homeBet: number; awayMoney: number; homeMoney: number };
  total: { overBet: number; underBet: number; overMoney: number; underMoney: number };
}

interface Game {
  id: number;
  dateTime: string;
  awayTeam: string;
  awayRecord: string;
  awayRank: string | null;
  homeTeam: string;
  homeRecord: string;
  homeRank: string | null;
  moneyline: {
    away: { odds: string; ev: string };
    home: { odds: string; ev: string };
  };
  spread: {
    awayLine: string;
    awayOdds: string;
    awayEv: string;
    homeLine: string;
    homeOdds: string;
    homeEv: string;
  };
  total: {
    line: string;
    overOdds: string;
    overEv: string;
    underOdds: string;
    underEv: string;
  };
  publicBetting: PublicBetting;
  isSharpPlay: boolean;
}

const GAMES_DATA: Game[] = [
  {
    id: 1,
    dateTime: "Today 7:00 PM",
    awayTeam: "Troy",
    awayRecord: "8-4",
    awayRank: null,
    homeTeam: "James Madison",
    homeRecord: "11-1",
    homeRank: "#19",
    moneyline: {
      away: { odds: "+1330", ev: "yes" },
      home: { odds: "-1329", ev: "no" }
    },
    spread: {
      awayLine: "+23.5",
      awayOdds: "+102",
      awayEv: "yes",
      homeLine: "-23.5",
      homeOdds: "-106",
      homeEv: "no"
    },
    total: {
      line: "46.5",
      overOdds: "-100",
      overEv: "no",
      underOdds: "+100",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 10, homeBet: 90, awayMoney: 41, homeMoney: 59 },
      spread: { awayBet: 42, homeBet: 58, awayMoney: 45, homeMoney: 55 },
      total: { overBet: 51, underBet: 49, overMoney: 48, underMoney: 52 }
    },
    isSharpPlay: true
  },
  {
    id: 2,
    dateTime: "Today 7:00 PM",
    awayTeam: "Kennesaw State",
    awayRecord: "9-3",
    awayRank: null,
    homeTeam: "Jacksonville State",
    homeRecord: "8-4",
    homeRank: null,
    moneyline: {
      away: { odds: "-122", ev: "no" },
      home: { odds: "+122", ev: "yes" }
    },
    spread: {
      awayLine: "-2.5",
      awayOdds: "-103",
      awayEv: "no",
      homeLine: "+2.5",
      homeOdds: "+104",
      homeEv: "yes"
    },
    total: {
      line: "60.5",
      overOdds: "+100",
      overEv: "no",
      underOdds: "-104",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 62, homeBet: 38, awayMoney: 58, homeMoney: 42 },
      spread: { awayBet: 55, homeBet: 45, awayMoney: 52, homeMoney: 48 },
      total: { overBet: 47, underBet: 53, overMoney: 49, underMoney: 51 }
    },
    isSharpPlay: false
  },
  {
    id: 3,
    dateTime: "Today 8:00 PM",
    awayTeam: "UNLV",
    awayRecord: "10-2",
    awayRank: null,
    homeTeam: "Boise State",
    homeRecord: "8-4",
    homeRank: null,
    moneyline: {
      away: { odds: "+194", ev: "yes" },
      home: { odds: "-194", ev: "no" }
    },
    spread: {
      awayLine: "+4.5",
      awayOdds: "+100",
      awayEv: "no",
      homeLine: "-4.5",
      homeOdds: "-106",
      homeEv: "no"
    },
    total: {
      line: "58.5",
      overOdds: "-105",
      overEv: "no",
      underOdds: "+101",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 28, homeBet: 72, awayMoney: 47, homeMoney: 53 },
      spread: { awayBet: 45, homeBet: 55, awayMoney: 51, homeMoney: 49 },
      total: { overBet: 56, underBet: 44, overMoney: 53, underMoney: 47 }
    },
    isSharpPlay: true
  },
  {
    id: 4,
    dateTime: "Today 8:00 PM",
    awayTeam: "North Texas",
    awayRecord: "11-1",
    awayRank: "#20",
    homeTeam: "Tulane",
    homeRecord: "10-2",
    homeRank: "#21",
    moneyline: {
      away: { odds: "-130", ev: "no" },
      home: { odds: "+123", ev: "yes" }
    },
    spread: {
      awayLine: "-2.5",
      awayOdds: "-104",
      awayEv: "no",
      homeLine: "+2.5",
      homeOdds: "+104",
      homeEv: "no"
    },
    total: {
      line: "66.5",
      overOdds: "-102",
      overEv: "no",
      underOdds: "-102",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 68, homeBet: 32, awayMoney: 65, homeMoney: 35 },
      spread: { awayBet: 58, homeBet: 42, awayMoney: 60, homeMoney: 40 },
      total: { overBet: 52, underBet: 48, overMoney: 54, underMoney: 46 }
    },
    isSharpPlay: false
  },
  {
    id: 5,
    dateTime: "Saturday 12:00 PM",
    awayTeam: "BYU",
    awayRecord: "11-1",
    awayRank: "#11",
    homeTeam: "Texas Tech",
    homeRecord: "11-1",
    homeRank: "#5",
    moneyline: {
      away: { odds: "+435", ev: "yes" },
      home: { odds: "-426", ev: "no" }
    },
    spread: {
      awayLine: "+12.5",
      awayOdds: "+101",
      awayEv: "yes",
      homeLine: "-12.5",
      homeOdds: "-102",
      homeEv: "no"
    },
    total: {
      line: "49.5",
      overOdds: "+101",
      overEv: "no",
      underOdds: "-110",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 14, homeBet: 86, awayMoney: 49, homeMoney: 51 },
      spread: { awayBet: 31, homeBet: 69, awayMoney: 42, homeMoney: 58 },
      total: { overBet: 44, underBet: 56, overMoney: 47, underMoney: 53 }
    },
    isSharpPlay: true
  },
  {
    id: 6,
    dateTime: "Saturday 12:00 PM",
    awayTeam: "Miami (OH)",
    awayRecord: "7-5",
    awayRank: null,
    homeTeam: "Western Michigan",
    homeRecord: "8-4",
    homeRank: null,
    moneyline: {
      away: { odds: "+127", ev: "yes" },
      home: { odds: "-117", ev: "no" }
    },
    spread: {
      awayLine: "+2.5",
      awayOdds: "+100",
      awayEv: "yes",
      homeLine: "-2.5",
      homeOdds: "-101",
      homeEv: "no"
    },
    total: {
      line: "43.5",
      overOdds: "-102",
      overEv: "no",
      underOdds: "+100",
      underEv: "yes"
    },
    publicBetting: {
      ml: { awayBet: 41, homeBet: 59, awayMoney: 45, homeMoney: 55 },
      spread: { awayBet: 39, homeBet: 61, awayMoney: 58, homeMoney: 42 },
      total: { overBet: 48, underBet: 52, overMoney: 46, underMoney: 54 }
    },
    isSharpPlay: true
  },
  {
    id: 7,
    dateTime: "Saturday 4:00 PM",
    awayTeam: "Georgia",
    awayRecord: "11-1",
    awayRank: "#3",
    homeTeam: "Alabama",
    homeRecord: "10-2",
    homeRank: "#10",
    moneyline: {
      away: { odds: "-122", ev: "no" },
      home: { odds: "+122", ev: "yes" }
    },
    spread: {
      awayLine: "-2.5",
      awayOdds: "+100",
      awayEv: "no",
      homeLine: "+2.5",
      homeOdds: "-104",
      homeEv: "no"
    },
    total: {
      line: "48.5",
      overOdds: "-100",
      overEv: "no",
      underOdds: "-110",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 54, homeBet: 46, awayMoney: 52, homeMoney: 48 },
      spread: { awayBet: 51, homeBet: 49, awayMoney: 49, homeMoney: 51 },
      total: { overBet: 47, underBet: 53, overMoney: 45, underMoney: 55 }
    },
    isSharpPlay: false
  },
  {
    id: 8,
    dateTime: "Saturday 8:00 PM",
    awayTeam: "Duke",
    awayRecord: "7-5",
    awayRank: null,
    homeTeam: "Virginia",
    homeRecord: "10-2",
    homeRank: "#16",
    moneyline: {
      away: { odds: "+178", ev: "yes" },
      home: { odds: "-173", ev: "no" }
    },
    spread: {
      awayLine: "+3.5",
      awayOdds: "+108",
      awayEv: "no",
      homeLine: "-3.5",
      homeOdds: "-108",
      homeEv: "yes"
    },
    total: {
      line: "57.5",
      overOdds: "-113",
      overEv: "no",
      underOdds: "+104",
      underEv: "yes"
    },
    publicBetting: {
      ml: { awayBet: 38, homeBet: 62, awayMoney: 42, homeMoney: 58 },
      spread: { awayBet: 44, homeBet: 56, awayMoney: 47, homeMoney: 53 },
      total: { overBet: 53, underBet: 47, overMoney: 51, underMoney: 49 }
    },
    isSharpPlay: false
  },
  {
    id: 9,
    dateTime: "Saturday 8:00 PM",
    awayTeam: "Ohio State",
    awayRecord: "12-0",
    awayRank: "#1",
    homeTeam: "Indiana",
    homeRecord: "12-0",
    homeRank: "#2",
    moneyline: {
      away: { odds: "-177", ev: "no" },
      home: { odds: "+178", ev: "yes" }
    },
    spread: {
      awayLine: "-3.5",
      awayOdds: "-107",
      awayEv: "no",
      homeLine: "+3.5",
      homeOdds: "+113",
      homeEv: "yes"
    },
    total: {
      line: "47.5",
      overOdds: "-108",
      overEv: "no",
      underOdds: "-100",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 75, homeBet: 25, awayMoney: 68, homeMoney: 32 },
      spread: { awayBet: 72, homeBet: 28, awayMoney: 70, homeMoney: 30 },
      total: { overBet: 58, underBet: 42, overMoney: 56, underMoney: 44 }
    },
    isSharpPlay: false
  }
];

type FilterType = 'all' | 'sharp' | 'ev' | 'today' | 'saturday';

interface EVBettingDashboardProps {
  onBack?: () => void;
}

const EVBettingDashboard: React.FC<EVBettingDashboardProps> = ({ onBack }) => {
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');

  const getFilteredGames = () => {
    switch (activeFilter) {
      case 'sharp':
        return GAMES_DATA.filter(game => game.isSharpPlay);
      case 'ev':
        return GAMES_DATA.filter(game => 
          game.moneyline.away.ev === 'yes' || 
          game.moneyline.home.ev === 'yes' ||
          game.spread.awayEv === 'yes' ||
          game.spread.homeEv === 'yes' ||
          game.total.overEv === 'yes' ||
          game.total.underEv === 'yes'
        );
      case 'today':
        return GAMES_DATA.filter(game => game.dateTime.includes('Today'));
      case 'saturday':
        return GAMES_DATA.filter(game => game.dateTime.includes('Saturday'));
      default:
        return GAMES_DATA;
    }
  };

  const getSharpMoneyIndicators = (game: Game) => {
    const indicators = [];

    // Moneyline sharp money check
    const mlBetDiff = game.publicBetting.ml.awayMoney - game.publicBetting.ml.awayBet;
    if (Math.abs(mlBetDiff) > 15) {
      indicators.push({
        type: mlBetDiff > 0 ? 'positive' : 'negative',
        text: `${mlBetDiff > 0 ? 'Sharp Money' : 'Public Heavy'} on ${
          mlBetDiff > 0 ? game.awayTeam.split(' ').pop() : game.homeTeam.split(' ').pop()
        } ML (${Math.abs(mlBetDiff)}% diff)`
      });
    }

    // Spread sharp money check
    const spreadBetDiff = game.publicBetting.spread.awayMoney - game.publicBetting.spread.awayBet;
    if (Math.abs(spreadBetDiff) > 15) {
      indicators.push({
        type: spreadBetDiff > 0 ? 'positive' : 'negative',
        text: `${spreadBetDiff > 0 ? 'Sharp Money' : 'Public Heavy'} on ${
          spreadBetDiff > 0 ? game.awayTeam.split(' ').pop() : game.homeTeam.split(' ').pop()
        } Spread (${Math.abs(spreadBetDiff)}% diff)`
      });
    }

    // Value indicator
    if (game.moneyline.away.ev === 'yes' || game.moneyline.home.ev === 'yes') {
      indicators.push({
        type: 'positive',
        text: 'Value Opportunity Detected'
      });
    }

    return indicators;
  };

  const filteredGames = getFilteredGames();
  const sharpPlaysCount = GAMES_DATA.filter(g => g.isSharpPlay).length;

  return (
    <div className="ev-dashboard">
      {/* HEADER */}
      <div className="ev-header">
        <div className="ev-header-main">
          <div className="ev-header-left">
            <img 
              src="/GameDayDark.png" 
              alt="Gameday Plus" 
              className="ev-logo"
            />
            <div className="ev-title-group">
              <h1>NCAAFB Championship Week</h1>
              <div className="ev-subtitle">
                Conference Championship Games • December 5, 2025 • Live Odds & Public Betting
              </div>
            </div>
          </div>
        </div>

        <div className="ev-filters">
          {onBack && (
            <button
              className="filter-pill"
              onClick={onBack}
            >
              <ArrowLeft size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
              Back
            </button>
          )}
          <button
            className={`filter-pill ${activeFilter === 'all' ? 'active' : ''}`}
            onClick={() => setActiveFilter('all')}
          >
            <LayoutGrid size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
            All Games ({GAMES_DATA.length})
          </button>
          <button
            className={`filter-pill ${activeFilter === 'sharp' ? 'active' : ''}`}
            onClick={() => setActiveFilter('sharp')}
          >
            <Zap size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
            Sharp Plays ({sharpPlaysCount})
          </button>
          <button
            className={`filter-pill ${activeFilter === 'ev' ? 'active' : ''}`}
            onClick={() => setActiveFilter('ev')}
          >
            <TrendingUp size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
            EV+ Opportunities
          </button>
          <button
            className={`filter-pill ${activeFilter === 'today' ? 'active' : ''}`}
            onClick={() => setActiveFilter('today')}
          >
            <Calendar size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
            Today's Games
          </button>
          <button
            className={`filter-pill ${activeFilter === 'saturday' ? 'active' : ''}`}
            onClick={() => setActiveFilter('saturday')}
          >
            <CalendarDays size={14} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
            Saturday Games
          </button>
        </div>
      </div>

      {/* GAMES CONTAINER */}
      <div className="ev-games-container">
        {filteredGames.map(game => {
          const mlSharp = Math.abs(game.publicBetting.ml.awayMoney - game.publicBetting.ml.awayBet) > 15;
          const spreadSharp = Math.abs(game.publicBetting.spread.awayMoney - game.publicBetting.spread.awayBet) > 15;
          const indicators = getSharpMoneyIndicators(game);
          
          const awayTeamData = getTeamData(game.awayTeam);
          const homeTeamData = getTeamData(game.homeTeam);
          
          // Format time display
          const formatGameTime = (dateTime: string) => {
            if (dateTime.toLowerCase().includes('today')) {
              // Extract just the time (e.g., "7:00 PM")
              const timeMatch = dateTime.match(/\d{1,2}:\d{2}\s*[AP]M/i);
              return timeMatch ? timeMatch[0] : dateTime;
            } else if (dateTime.toLowerCase().includes('saturday')) {
              // Replace "Saturday" with "SAT" and keep time
              return dateTime.replace(/saturday/i, 'SAT');
            }
            return dateTime;
          };

          return (
            <div key={game.id} className={`ev-game-card ${game.isSharpPlay ? 'sharp-play' : ''}`}>
              {/* GAME HEADER - OPTION C LAYOUT */}
              <div className="ev-game-header-optionC">
                {/* Watermark Logos - Enhanced */}
                {awayTeamData && (
                  <img 
                    src={awayTeamData.logos[0]} 
                    alt=""
                    className="ev-header-watermark-left-enhanced"
                  />
                )}
                {homeTeamData && (
                  <img 
                    src={homeTeamData.logos[0]} 
                    alt=""
                    className="ev-header-watermark-right-enhanced"
                  />
                )}
                
                {/* Main Matchup Row */}
                <div className="ev-matchup-main">
                  {/* Away Team (Left) */}
                  <div className="ev-team-block-away">
                    {game.awayRank && <div className="ev-rank-pro">{game.awayRank}</div>}
                    {awayTeamData && (
                      <img 
                        src={awayTeamData.logos[0]} 
                        alt={awayTeamData.school}
                        className="ev-team-logo-pro"
                      />
                    )}
                    <div className="ev-team-info-pro">
                      <span className="ev-team-name-pro">
                        {awayTeamData?.abbreviation || game.awayTeam}
                      </span>
                      <span className="ev-team-record-pro">({game.awayRecord})</span>
                    </div>
                  </div>
                  
                  {/* VS Divider - Enhanced */}
                  <div className="ev-vs-divider-pro">
                    <span className="ev-vs-text-pro">VS</span>
                  </div>
                  
                  {/* Home Team (Right) */}
                  <div className="ev-team-block-home">
                    <div className="ev-team-info-pro home">
                      <span className="ev-team-name-pro">
                        {homeTeamData?.abbreviation || game.homeTeam}
                      </span>
                      <span className="ev-team-record-pro">({game.homeRecord})</span>
                    </div>
                    {homeTeamData && (
                      <img 
                        src={homeTeamData.logos[0]} 
                        alt={homeTeamData.school}
                        className="ev-team-logo-pro"
                      />
                    )}
                    {game.homeRank && <div className="ev-rank-pro">{game.homeRank}</div>}
                  </div>
                </div>
                
                {/* Game Meta Bar - Split Layout */}
                <div className="ev-game-meta-bar">
                  <div className="ev-time-meta">
                    <svg className="ev-time-icon-pro" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {formatGameTime(game.dateTime)}
                  </div>
                  {game.isSharpPlay && (
                    <div className="ev-sharp-pro">
                      <svg className="ev-sharp-icon-pro" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
                      </svg>
                      SHARP PLAY
                    </div>
                  )}
                </div>
              </div>

              {/* BETTING MARKETS - INLINE */}
              <div className="ev-markets-inline">
                {/* MONEYLINE */}
                <div className="ev-market-inline">
                  <div className="ev-market-label">ML</div>
                  <div className="ev-market-values">
                    <div className={`ev-value ${game.moneyline.away.ev === 'yes' ? 'ev-highlight' : ''}`}>
                      {game.moneyline.away.odds}
                      {game.moneyline.away.ev === 'yes' && <span className="ev-dot"></span>}
                    </div>
                    <div className={`ev-value ${game.moneyline.home.ev === 'yes' ? 'ev-highlight' : ''}`}>
                      {game.moneyline.home.odds}
                      {game.moneyline.home.ev === 'yes' && <span className="ev-dot"></span>}
                    </div>
                  </div>
                </div>

                {/* SPREAD */}
                <div className="ev-market-inline">
                  <div className="ev-market-label">Spread</div>
                  <div className="ev-market-values">
                    <div className={`ev-value ${game.spread.awayEv === 'yes' ? 'ev-highlight' : ''}`}>
                      {game.spread.awayLine}
                      <span className="ev-odds-small">{game.spread.awayOdds}</span>
                      {game.spread.awayEv === 'yes' && <span className="ev-dot"></span>}
                    </div>
                    <div className={`ev-value ${game.spread.homeEv === 'yes' ? 'ev-highlight' : ''}`}>
                      {game.spread.homeLine}
                      <span className="ev-odds-small">{game.spread.homeOdds}</span>
                      {game.spread.homeEv === 'yes' && <span className="ev-dot"></span>}
                    </div>
                  </div>
                </div>

                {/* TOTAL */}
                <div className="ev-market-inline">
                  <div className="ev-market-label">Total</div>
                  <div className="ev-market-values">
                    <div className={`ev-value ${game.total.overEv === 'yes' ? 'ev-highlight' : ''}`}>
                      O {game.total.line}
                      <span className="ev-odds-small">{game.total.overOdds}</span>
                      {game.total.overEv === 'yes' && <span className="ev-dot"></span>}
                    </div>
                    <div className={`ev-value ${game.total.underEv === 'yes' ? 'ev-highlight' : ''}`}>
                      U {game.total.line}
                      <span className="ev-odds-small">{game.total.underOdds}</span>
                      {game.total.underEv === 'yes' && <span className="ev-dot"></span>}
                    </div>
                  </div>
                </div>
              </div>

              {/* PUBLIC BETTING - MINIMAL BARS */}
              <div className="ev-public-minimal">
                <div className="ev-mini-chart">
                  <div className="ev-mini-label">ML</div>
                  <div className="ev-mini-bar-wrapper">
                    <div 
                      className={`ev-mini-bar ${mlSharp ? 'sharp' : ''}`}
                      style={{ width: `${game.publicBetting.ml.awayMoney}%` }}
                    />
                  </div>
                  <div className="ev-mini-percent">{game.publicBetting.ml.awayMoney}%</div>
                </div>
                
                <div className="ev-mini-chart">
                  <div className="ev-mini-label">Spread</div>
                  <div className="ev-mini-bar-wrapper">
                    <div 
                      className={`ev-mini-bar ${spreadSharp ? 'sharp' : ''}`}
                      style={{ width: `${game.publicBetting.spread.awayMoney}%` }}
                    />
                  </div>
                  <div className="ev-mini-percent">{game.publicBetting.spread.awayMoney}%</div>
                </div>
                
                <div className="ev-mini-chart">
                  <div className="ev-mini-label">Total</div>
                  <div className="ev-mini-bar-wrapper">
                    <div 
                      className="ev-mini-bar"
                      style={{ width: `${game.publicBetting.total.overMoney}%` }}
                    />
                  </div>
                  <div className="ev-mini-percent">{game.publicBetting.total.overMoney}%</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default EVBettingDashboard;
