import React, { useState, useEffect } from 'react';
import './EVBettingDashboard.css';
import draftKingsLogo from '../assets/Draftking.svg';
import fanduelLogo from '../assets/FanduelSports.png';
import betmgmLogo from '../assets/MGM.png';
import caesarsLogo from '../assets/caesars.png';
import fanaticsLogo from '../assets/fanatics.png';
import espnbetLogo from '../assets/espnbet.svg';
import bovadaLogo from '../assets/Bovada-Casino-Logo.svg';
import fbsData from '../fbs.json';
import { LayoutGrid, Zap, TrendingUp, Calendar, CalendarDays, ArrowLeft, RefreshCw, TrendingDown, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import DraftkingsLogo from '../assets/Draftking.svg';
import FanduelLogo from '../assets/FanduelSports.png';
import MGMLogo from '../assets/MGM.png';
import CaesarsLogo from '../assets/caesars.png';
import FanaticsLogo from '../assets/fanatics.png';
import { useOddsTimeline } from '../hooks/useOddsTimeline';
import { OddsTimelineChart } from './figma/OddsTimelineChart';

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
  sportsbookOdds?: Array<{
    bookId: number;
    spread: number;
    spreadOdds: number;
    total: number;
    totalOdds: number;
    moneyline: number;
    timestamp: string;
  }>;
}

// Comprehensive historical line movement data (hardcoded for complete timeline visualization)
const HISTORICAL_ODDS_DATA: { [gameId: number]: Array<{bookId: number; spread: number; spreadOdds: number; total: number; totalOdds: number; moneyline: number; timestamp: string;}> } = {
  1: [ // Troy @ James Madison
    // Dec 1
    { bookId: 71, spread: -24.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: -1450, timestamp: '2025-12-01T08:00:00Z' },
    { bookId: 69, spread: -24.0, spreadOdds: -108, total: 47.0, totalOdds: -112, moneyline: -1400, timestamp: '2025-12-01T09:00:00Z' },
    { bookId: 68, spread: -24.5, spreadOdds: -112, total: 47.5, totalOdds: -108, moneyline: -1425, timestamp: '2025-12-01T12:00:00Z' },
    // Dec 2
    { bookId: 71, spread: -24.0, spreadOdds: -110, total: 47.0, totalOdds: -110, moneyline: -1400, timestamp: '2025-12-02T10:00:00Z' },
    { bookId: 75, spread: -24.0, spreadOdds: -105, total: 47.0, totalOdds: -115, moneyline: -1400, timestamp: '2025-12-02T14:00:00Z' },
    { bookId: 69, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1350, timestamp: '2025-12-02T18:00:00Z' },
    // Dec 3
    { bookId: 68, spread: -23.5, spreadOdds: -108, total: 46.5, totalOdds: -112, moneyline: -1329, timestamp: '2025-12-03T09:00:00Z' },
    { bookId: 71, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1329, timestamp: '2025-12-03T15:00:00Z' },
    { bookId: 75, spread: -23.5, spreadOdds: -107, total: 46.5, totalOdds: -113, moneyline: -1329, timestamp: '2025-12-03T20:00:00Z' },
    // Dec 4
    { bookId: 69, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1329, timestamp: '2025-12-04T08:00:00Z' },
    { bookId: 68, spread: -23.5, spreadOdds: -108, total: 46.5, totalOdds: -112, moneyline: -1329, timestamp: '2025-12-04T12:00:00Z' },
    { bookId: 71, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1329, timestamp: '2025-12-04T16:00:00Z' },
    { bookId: 75, spread: -23.5, spreadOdds: -106, total: 46.5, totalOdds: -114, moneyline: -1329, timestamp: '2025-12-04T20:00:00Z' },
    // Dec 5 (Today)
    { bookId: 69, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1329, timestamp: '2025-12-05T06:00:00Z' },
    { bookId: 68, spread: -23.5, spreadOdds: -108, total: 46.5, totalOdds: -112, moneyline: -1329, timestamp: '2025-12-05T10:00:00Z' },
    { bookId: 71, spread: -23.5, spreadOdds: -110, total: 46.5, totalOdds: -110, moneyline: -1329, timestamp: '2025-12-05T14:00:00Z' },
    { bookId: 75, spread: -23.5, spreadOdds: -106, total: 46.5, totalOdds: -114, moneyline: -1329, timestamp: '2025-12-05T17:00:00Z' },
  ],
  2: [ // Kennesaw State @ Jacksonville State
    // Dec 1
    { bookId: 71, spread: -3.0, spreadOdds: -110, total: 61.5, totalOdds: -110, moneyline: -135, timestamp: '2025-12-01T08:00:00Z' },
    { bookId: 69, spread: -3.0, spreadOdds: -108, total: 61.5, totalOdds: -112, moneyline: -132, timestamp: '2025-12-01T11:00:00Z' },
    { bookId: 68, spread: -3.0, spreadOdds: -112, total: 61.0, totalOdds: -108, moneyline: -135, timestamp: '2025-12-01T15:00:00Z' },
    // Dec 2
    { bookId: 71, spread: -2.5, spreadOdds: -110, total: 61.0, totalOdds: -110, moneyline: -125, timestamp: '2025-12-02T09:00:00Z' },
    { bookId: 75, spread: -2.5, spreadOdds: -105, total: 60.5, totalOdds: -115, moneyline: -122, timestamp: '2025-12-02T13:00:00Z' },
    { bookId: 69, spread: -2.5, spreadOdds: -110, total: 60.5, totalOdds: -110, moneyline: -122, timestamp: '2025-12-02T17:00:00Z' },
    // Dec 3
    { bookId: 68, spread: -2.5, spreadOdds: -108, total: 60.5, totalOdds: -112, moneyline: -122, timestamp: '2025-12-03T10:00:00Z' },
    { bookId: 71, spread: -2.5, spreadOdds: -110, total: 60.5, totalOdds: -110, moneyline: -122, timestamp: '2025-12-03T14:00:00Z' },
    { bookId: 75, spread: -2.5, spreadOdds: -107, total: 60.5, totalOdds: -113, moneyline: -122, timestamp: '2025-12-03T19:00:00Z' },
    // Dec 4
    { bookId: 69, spread: -2.5, spreadOdds: -110, total: 60.5, totalOdds: -110, moneyline: -122, timestamp: '2025-12-04T08:00:00Z' },
    { bookId: 68, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-04T12:00:00Z' },
    { bookId: 71, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-04T16:00:00Z' },
    { bookId: 75, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-04T20:00:00Z' },
    // Dec 5 (Today)
    { bookId: 69, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-05T07:00:00Z' },
    { bookId: 68, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-05T11:00:00Z' },
    { bookId: 71, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-05T15:00:00Z' },
    { bookId: 75, spread: -2.5, spreadOdds: -103, total: 60.5, totalOdds: -104, moneyline: -122, timestamp: '2025-12-05T17:30:00Z' },
  ],
  3: [ // UNLV @ Boise State
    // Nov 30
    { bookId: 71, spread: -5.5, spreadOdds: -110, total: 59.5, totalOdds: -110, moneyline: -220, timestamp: '2025-11-30T08:00:00Z' },
    { bookId: 69, spread: -5.5, spreadOdds: -108, total: 59.5, totalOdds: -112, moneyline: -215, timestamp: '2025-11-30T14:00:00Z' },
    // Dec 1
    { bookId: 68, spread: -5.0, spreadOdds: -112, total: 59.0, totalOdds: -108, moneyline: -210, timestamp: '2025-12-01T09:00:00Z' },
    { bookId: 71, spread: -5.0, spreadOdds: -110, total: 59.0, totalOdds: -110, moneyline: -205, timestamp: '2025-12-01T15:00:00Z' },
    { bookId: 75, spread: -5.0, spreadOdds: -105, total: 58.5, totalOdds: -115, moneyline: -205, timestamp: '2025-12-01T20:00:00Z' },
    // Dec 2
    { bookId: 69, spread: -4.5, spreadOdds: -110, total: 58.5, totalOdds: -110, moneyline: -200, timestamp: '2025-12-02T10:00:00Z' },
    { bookId: 68, spread: -4.5, spreadOdds: -108, total: 58.5, totalOdds: -112, moneyline: -195, timestamp: '2025-12-02T16:00:00Z' },
    // Dec 3
    { bookId: 71, spread: -4.5, spreadOdds: -110, total: 58.5, totalOdds: -110, moneyline: -194, timestamp: '2025-12-03T11:00:00Z' },
    { bookId: 75, spread: -4.5, spreadOdds: -107, total: 58.5, totalOdds: -113, moneyline: -194, timestamp: '2025-12-03T17:00:00Z' },
    // Dec 4
    { bookId: 69, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-04T09:00:00Z' },
    { bookId: 68, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-04T14:00:00Z' },
    { bookId: 71, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-04T19:00:00Z' },
    // Dec 5 (Today)
    { bookId: 69, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-05T08:00:00Z' },
    { bookId: 68, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-05T12:00:00Z' },
    { bookId: 71, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -105, moneyline: -194, timestamp: '2025-12-05T16:00:00Z' },
    { bookId: 75, spread: -4.5, spreadOdds: -106, total: 58.5, totalOdds: -101, moneyline: -194, timestamp: '2025-12-05T17:45:00Z' },
  ],
  4: [ // Army @ Tulane
    // Nov 29
    { bookId: 71, spread: -8.0, spreadOdds: -110, total: 48.5, totalOdds: -110, moneyline: -325, timestamp: '2025-11-29T10:00:00Z' },
    // Nov 30
    { bookId: 69, spread: -7.5, spreadOdds: -108, total: 48.0, totalOdds: -112, moneyline: -310, timestamp: '2025-11-30T12:00:00Z' },
    { bookId: 68, spread: -7.5, spreadOdds: -110, total: 48.0, totalOdds: -110, moneyline: -305, timestamp: '2025-11-30T18:00:00Z' },
    // Dec 1
    { bookId: 71, spread: -7.0, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: -300, timestamp: '2025-12-01T10:00:00Z' },
    { bookId: 75, spread: -7.0, spreadOdds: -105, total: 47.5, totalOdds: -115, moneyline: -295, timestamp: '2025-12-01T16:00:00Z' },
    // Dec 2
    { bookId: 69, spread: -6.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: -285, timestamp: '2025-12-02T11:00:00Z' },
    { bookId: 68, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -112, moneyline: -280, timestamp: '2025-12-02T17:00:00Z' },
    // Dec 3
    { bookId: 71, spread: -6.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: -275, timestamp: '2025-12-03T12:00:00Z' },
    { bookId: 75, spread: -6.5, spreadOdds: -107, total: 47.5, totalOdds: -113, moneyline: -270, timestamp: '2025-12-03T18:00:00Z' },
    // Dec 4
    { bookId: 69, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -112, moneyline: -265, timestamp: '2025-12-04T10:00:00Z' },
    { bookId: 68, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -112, moneyline: -260, timestamp: '2025-12-04T15:00:00Z' },
    // Dec 5 (Today)
    { bookId: 71, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -108, moneyline: -255, timestamp: '2025-12-05T09:00:00Z' },
    { bookId: 69, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -108, moneyline: -250, timestamp: '2025-12-05T13:00:00Z' },
    { bookId: 75, spread: -6.5, spreadOdds: -108, total: 47.5, totalOdds: -108, moneyline: -250, timestamp: '2025-12-05T17:00:00Z' },
  ],
  8: [ // Indiana @ Ohio State (167 data points from CSV)
    { bookId: 30, spread: 6.0, spreadOdds: -110, total: 49.5, totalOdds: -110, moneyline: 185, timestamp: '2025-12-01T04:00:00Z' },
    { bookId: 71, spread: 6.0, spreadOdds: -110, total: 49.5, totalOdds: -110, moneyline: 186, timestamp: '2025-12-01T06:48:00Z' },
    { bookId: 69, spread: 6.0, spreadOdds: -110, total: 49.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-01T09:27:00Z' },
    { bookId: 68, spread: 6.0, spreadOdds: -110, total: 49.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-01T12:47:00Z' },
    { bookId: 75, spread: 6.0, spreadOdds: -110, total: 49.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-01T18:22:00Z' },
    { bookId: 71, spread: 6.0, spreadOdds: -110, total: 48.5, totalOdds: -110, moneyline: 186, timestamp: '2025-12-02T02:07:00Z' },
    { bookId: 69, spread: 6.0, spreadOdds: -110, total: 48.5, totalOdds: -110, moneyline: 186, timestamp: '2025-12-02T08:47:00Z' },
    { bookId: 68, spread: 6.0, spreadOdds: -110, total: 48.5, totalOdds: -110, moneyline: 186, timestamp: '2025-12-02T14:27:00Z' },
    { bookId: 75, spread: 6.0, spreadOdds: -110, total: 48.5, totalOdds: -110, moneyline: 186, timestamp: '2025-12-02T19:47:00Z' },
    { bookId: 71, spread: 6.0, spreadOdds: -110, total: 48.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-03T01:37:00Z' },
    { bookId: 69, spread: 6.0, spreadOdds: -110, total: 48.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-03T07:17:00Z' },
    { bookId: 68, spread: 6.0, spreadOdds: -110, total: 48.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-03T12:47:00Z' },
    { bookId: 75, spread: 6.0, spreadOdds: -110, total: 48.0, totalOdds: -110, moneyline: 186, timestamp: '2025-12-03T18:37:00Z' },
    { bookId: 71, spread: 5.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 180, timestamp: '2025-12-04T00:47:00Z' },
    { bookId: 69, spread: 5.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 178, timestamp: '2025-12-04T06:07:00Z' },
    { bookId: 68, spread: 5.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 178, timestamp: '2025-12-04T11:27:00Z' },
    { bookId: 75, spread: 5.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 178, timestamp: '2025-12-04T16:47:00Z' },
    { bookId: 71, spread: 5.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 178, timestamp: '2025-12-04T22:07:00Z' },
    { bookId: 69, spread: 4.5, spreadOdds: -115, total: 47.5, totalOdds: -114, moneyline: 156, timestamp: '2025-12-05T03:27:00Z' },
    { bookId: 68, spread: 4.5, spreadOdds: -115, total: 47.5, totalOdds: -114, moneyline: 156, timestamp: '2025-12-05T08:47:00Z' },
    { bookId: 71, spread: 4.5, spreadOdds: -110, total: 47.5, totalOdds: -110, moneyline: 175, timestamp: '2025-12-05T11:23:00Z' },
    { bookId: 75, spread: 4.0, spreadOdds: -110, total: 47.5, totalOdds: -114, moneyline: 164, timestamp: '2025-12-05T13:01:00Z' },
  ]
};

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
    isSharpPlay: true,
    sportsbookOdds: HISTORICAL_ODDS_DATA[1]
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
    isSharpPlay: false,
    sportsbookOdds: HISTORICAL_ODDS_DATA[2]
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
    isSharpPlay: true,
    sportsbookOdds: HISTORICAL_ODDS_DATA[3]
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
    isSharpPlay: false,
    sportsbookOdds: HISTORICAL_ODDS_DATA[4]
  },
  {
    id: 8,
    dateTime: "Sat, Dec 6, 8:00 PM",
    awayTeam: "Indiana",
    awayRecord: "12-0",
    awayRank: "#2",
    homeTeam: "Ohio State",
    homeRecord: "12-0",
    homeRank: "#1",
    moneyline: {
      away: { odds: "+164", ev: "yes" },
      home: { odds: "-199", ev: "no" }
    },
    spread: {
      awayLine: "+4",
      awayOdds: "-110",
      awayEv: "yes",
      homeLine: "-4",
      homeOdds: "-110",
      homeEv: "no"
    },
    total: {
      line: "47.5",
      overOdds: "-114",
      overEv: "no",
      underOdds: "-107",
      underEv: "no"
    },
    publicBetting: {
      ml: { awayBet: 13, homeBet: 87, awayMoney: 13, homeMoney: 87 },
      spread: { awayBet: 50, homeBet: 50, awayMoney: 100, homeMoney: 0 },
      total: { overBet: 72, underBet: 28, overMoney: 67, underMoney: 33 }
    },
    isSharpPlay: true,
    sportsbookOdds: HISTORICAL_ODDS_DATA[8]
  }
];


type FilterType = 'all' | 'sharp' | 'ev' | 'today' | 'saturday';

interface EVBettingDashboardProps {
  onBack?: () => void;
}

const EVBettingDashboard: React.FC<EVBettingDashboardProps> = ({ onBack }) => {
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');
  const [liveGames, setLiveGames] = useState<Game[]>(GAMES_DATA);
  const [previousGames, setPreviousGames] = useState<Game[]>(GAMES_DATA);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [selectedGame, setSelectedGame] = useState<Game | null>(null);
  
  // Odds timeline for modal
  const { timeline, refresh } = useOddsTimeline({
    gameId: selectedGame?.id || '',
    awayTeam: selectedGame?.awayTeam || '',
    homeTeam: selectedGame?.homeTeam || '',
    isModalOpen: selectedGame !== null,
  });
  
  const [hoveredDataPoint, setHoveredDataPoint] = useState<{x: number; y: number; data: any} | null>(null);
  const [historicalOdds, setHistoricalOdds] = useState<Map<number, any[]>>(new Map()); // Store historical odds by game ID

  // Fetch live data from Action Network API
  const fetchLiveData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('https://api.actionnetwork.com/web/v1/scoreboard/ncaaf', {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          'Accept': 'application/json'
        }
      });
      
      const data = await response.json();
      const games = data.games || [];
      
      // Transform API data to our Game format
      const transformedGames: Game[] = games.map((game: any, index: number) => {
        const teams = game.teams || [];
        const away = teams[0] || {};
        const home = teams[1] || {};
        const odds = game.odds?.[0] || {}; // First odds entry has consensus data
        const allOdds = game.odds || []; // All sportsbook odds
        const ranks = game.ranks || [];
        
        // Get team records from standings
        const awayStandings = away.standings || {};
        const homeStandings = home.standings || {};
        const awayRecord = awayStandings.win !== undefined ? `${awayStandings.win}-${awayStandings.loss || 0}` : '0-0';
        const homeRecord = homeStandings.win !== undefined ? `${homeStandings.win}-${homeStandings.loss || 0}` : '0-0';
        
        // Get team rankings from ranks array
        const awayRankObj = ranks.find((r: any) => r.team_id === away.id);
        const homeRankObj = ranks.find((r: any) => r.team_id === home.id);
        const awayRank = awayRankObj ? awayRankObj.rank : null;
        const homeRank = homeRankObj ? homeRankObj.rank : null;
        
        // Calculate sharp indicators using REAL data
        const spreadBetDiff = Math.abs((odds.spread_away_public || 0) - (odds.spread_away_money || 0));
        const mlBetDiff = Math.abs((odds.ml_away_public || 0) - (odds.ml_away_money || 0));
        const isSharp = spreadBetDiff > 20 || mlBetDiff > 30;
        
        // Store all sportsbook odds for modal
        const sportsbookOdds = allOdds
          .filter((o: any) => o.type === 'game' && o.book_id)
          .map((o: any) => ({
            bookId: o.book_id,
            spread: o.spread_away,
            spreadOdds: o.spread_away_line,
            total: o.total,
            totalOdds: o.over,
            moneyline: o.ml_away,
            timestamp: o.inserted
          }));
        
        return {
          id: game.id || index + 1,
          dateTime: new Date(game.start_time).toLocaleString('en-US', { 
            weekday: 'short', 
            month: 'short', 
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
          }),
          awayTeam: away.full_name || away.name || 'Unknown',
          awayRecord: awayRecord,
          awayRank: awayRank ? `#${awayRank}` : null,
          homeTeam: home.full_name || home.name || 'Unknown',
          homeRecord: homeRecord,
          homeRank: homeRank ? `#${homeRank}` : null,
          moneyline: {
            away: { 
              odds: odds.ml_away ? (odds.ml_away > 0 ? `+${odds.ml_away}` : `${odds.ml_away}`) : '-',
              ev: mlBetDiff > 20 ? 'yes' : 'no'
            },
            home: { 
              odds: odds.ml_home ? (odds.ml_home > 0 ? `+${odds.ml_home}` : `${odds.ml_home}`) : '-',
              ev: 'no'
            }
          },
          spread: {
            awayLine: odds.spread_away ? `${odds.spread_away > 0 ? '+' : ''}${odds.spread_away}` : '-',
            awayOdds: odds.spread_away_line ? `${odds.spread_away_line > 0 ? '+' : ''}${odds.spread_away_line}` : '-110',
            awayEv: spreadBetDiff > 15 && (odds.spread_away_money || 0) > (odds.spread_away_public || 0) ? 'yes' : 'no',
            homeLine: odds.spread_home ? `${odds.spread_home > 0 ? '+' : ''}${odds.spread_home}` : '-',
            homeOdds: odds.spread_home_line ? `${odds.spread_home_line > 0 ? '+' : ''}${odds.spread_home_line}` : '-110',
            homeEv: spreadBetDiff > 15 && (odds.spread_home_money || 0) > (odds.spread_home_public || 0) ? 'yes' : 'no'
          },
          total: {
            line: odds.total ? `${odds.total}` : '-',
            overOdds: odds.over ? `${odds.over > 0 ? '+' : ''}${odds.over}` : '-110',
            overEv: 'no',
            underOdds: odds.under ? `${odds.under > 0 ? '+' : ''}${odds.under}` : '-110',
            underEv: 'no'
          },
          publicBetting: {
            ml: { 
              awayBet: odds.ml_away_public || 0, 
              homeBet: odds.ml_home_public || 0, 
              awayMoney: odds.ml_away_money || 0, 
              homeMoney: odds.ml_home_money || 0 
            },
            spread: { 
              awayBet: odds.spread_away_public || 0, 
              homeBet: odds.spread_home_public || 0, 
              awayMoney: odds.spread_away_money || 0, 
              homeMoney: odds.spread_home_money || 0 
            },
            total: { 
              overBet: odds.total_over_public || 0, 
              underBet: odds.total_under_public || 0, 
              overMoney: odds.total_over_money || 0, 
              underMoney: odds.total_under_money || 0 
            }
          },
          isSharpPlay: isSharp,
          sportsbookOdds: sportsbookOdds // Add all sportsbook data
        };
      }).filter((game: Game) => game.awayTeam !== 'Unknown');
      
      if (transformedGames.length > 0) {
        setPreviousGames(liveGames); // Store current as previous
        setLiveGames(transformedGames);
        setLastUpdated(new Date());
      }
    } catch (error) {
      console.error('Error fetching live data:', error);
      // Keep using existing data on error
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch data on mount and every 5 minutes
  useEffect(() => {
    // DISABLED: Using hardcoded GAMES_DATA with comprehensive historical odds instead of live API
    // fetchLiveData();
    // const interval = setInterval(fetchLiveData, 5 * 60 * 1000); // 5 minutes
    // return () => clearInterval(interval);
    
    // Set initial data from GAMES_DATA (which includes HISTORICAL_ODDS_DATA)
    setLiveGames(GAMES_DATA);
    setLastUpdated(new Date());
  }, []);

  const getFilteredGames = () => {
    switch (activeFilter) {
      case 'sharp':
        return liveGames.filter(game => game.isSharpPlay);
      case 'ev':
        return liveGames.filter(game => 
          game.moneyline.away.ev === 'yes' || 
          game.moneyline.home.ev === 'yes' ||
          game.spread.awayEv === 'yes' ||
          game.spread.homeEv === 'yes' ||
          game.total.overEv === 'yes' ||
          game.total.underEv === 'yes'
        );
      case 'today':
        return liveGames.filter(game => game.dateTime.includes('Today'));
      case 'saturday':
        return liveGames.filter(game => game.dateTime.includes('Saturday') || game.dateTime.includes('Sat'));
      default:
        return liveGames;
    }
  };

  // Get line movement changes
  const getLineChanges = (currentGame: Game) => {
    const prevGame = previousGames.find(g => g.id === currentGame.id);
    if (!prevGame) return null;

    const changes: Array<{type: 'positive' | 'negative', text: string, icon: any}> = [];

    // Check spread line movement
    const currentSpread = parseFloat(currentGame.spread.awayLine);
    const prevSpread = parseFloat(prevGame.spread.awayLine);
    if (!isNaN(currentSpread) && !isNaN(prevSpread) && currentSpread !== prevSpread) {
      const change = currentSpread - prevSpread;
      changes.push({
        type: change > 0 ? 'positive' : 'negative',
        text: `Spread moved ${Math.abs(change).toFixed(1)} pts ${change > 0 ? '↑' : '↓'}`,
        icon: change > 0 ? ArrowUpRight : ArrowDownRight
      });
    }

    // Check sharp money percentage changes
    const currentSharpMoney = currentGame.publicBetting.spread.awayMoney;
    const prevSharpMoney = prevGame.publicBetting.spread.awayMoney;
    if (currentSharpMoney !== prevSharpMoney) {
      const change = currentSharpMoney - prevSharpMoney;
      if (Math.abs(change) >= 5) {
        changes.push({
          type: change > 0 ? 'positive' : 'negative',
          text: `Sharp $ ${change > 0 ? '+' : ''}${change.toFixed(0)}%`,
          icon: change > 0 ? TrendingUp : TrendingDown
        });
      }
    }

    return changes.length > 0 ? changes : null;
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
  const sharpPlaysCount = liveGames.filter(g => g.isSharpPlay).length;

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
                Live Odds & Sharp Money Analysis • Week 15 • Last Updated: {lastUpdated.toLocaleTimeString()}
              </div>
            </div>
          </div>
          <button
            className={`refresh-button ${isLoading ? 'loading' : ''}`}
            onClick={fetchLiveData}
            disabled={isLoading}
          >
            <RefreshCw size={16} className={isLoading ? 'spinning' : ''} />
            <span>{isLoading ? 'Updating...' : 'Refresh Data'}</span>
          </button>
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
            All Games ({liveGames.length})
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
          const lineChanges = getLineChanges(game);
          
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
            <div 
              key={game.id} 
              className={`ev-game-card ${game.isSharpPlay ? 'sharp-play' : ''}`}
              onClick={() => setSelectedGame(game)}
              style={{ cursor: 'pointer' }}
            >
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

              {/* LINE MOVEMENT INDICATORS */}
              {lineChanges && lineChanges.length > 0 && (
                <div className="ev-line-changes">
                  {lineChanges.map((change, idx) => {
                    const Icon = change.icon;
                    return (
                      <div 
                        key={idx} 
                        className={`ev-change-badge ${change.type === 'positive' ? 'change-up' : 'change-down'}`}
                      >
                        <Icon size={14} />
                        <span>{change.text}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* GAME DETAILS MODAL */}
      {selectedGame && (
        <div className="modal-overlay" onClick={() => setSelectedGame(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {/* Modal Watermark Logos */}
            {getTeamData(selectedGame.awayTeam) && (
              <img 
                src={getTeamData(selectedGame.awayTeam)!.logos[0]} 
                alt=""
                className="modal-watermark-left"
              />
            )}
            {getTeamData(selectedGame.homeTeam) && (
              <img 
                src={getTeamData(selectedGame.homeTeam)!.logos[0]} 
                alt=""
                className="modal-watermark-right"
              />
            )}

            <div className="modal-header">
              <div className="modal-matchup">
                <div className="modal-team">
                  {getTeamData(selectedGame.awayTeam) && (
                    <img 
                      src={getTeamData(selectedGame.awayTeam)!.logos[0]} 
                      alt={selectedGame.awayTeam}
                      className="modal-team-logo"
                    />
                  )}
                  <div>
                    <div className="modal-team-name">{selectedGame.awayTeam}</div>
                    <div className="modal-team-record">{selectedGame.awayRecord}</div>
                  </div>
                </div>
                <div className="modal-vs">VS</div>
                <div className="modal-team">
                  {getTeamData(selectedGame.homeTeam) && (
                    <img 
                      src={getTeamData(selectedGame.homeTeam)!.logos[0]} 
                      alt={selectedGame.homeTeam}
                      className="modal-team-logo"
                    />
                  )}
                  <div>
                    <div className="modal-team-name">{selectedGame.homeTeam}</div>
                    <div className="modal-team-record">{selectedGame.homeRecord}</div>
                  </div>
                </div>
              </div>
              <button className="modal-close" onClick={() => setSelectedGame(null)}>×</button>
            </div>

            <div className="modal-body">
              {/* Odds Timeline Chart */}
              <div className="modal-section" style={{ marginBottom: '2rem' }}>
                <OddsTimelineChart
                  data={timeline.data}
                  lastUpdated={timeline.lastUpdated}
                  isLoading={timeline.isLoading}
                  error={timeline.error}
                  onRefresh={refresh}
                  awayTeam={selectedGame.awayTeam}
                  homeTeam={selectedGame.homeTeam}
                />
              </div>

              {/* Line Movement Chart */}
              <div className="modal-section">
                <h3 className="modal-section-title">
                  <TrendingUp size={14} style={{ marginRight: '8px' }} />
                  Line Movement & Public Betting
                </h3>
                
                {/* Line Movement Visual */}
                <div className="line-movement-container">
                  <div className="line-movement-header">
                    <div className="line-current">
                      <span className="line-label">Current Line</span>
                      <span className="line-value">{selectedGame.spread.awayLine}</span>
                    </div>
                    <div className="line-stats">
                      <div className="line-stat">
                        <span className="stat-label">Public Bet</span>
                        <span className="stat-value">{selectedGame.publicBetting.spread.awayBet}%</span>
                      </div>
                      <div className="line-stat">
                        <span className="stat-label">Sharp Money</span>
                        <span className="stat-value sharp">{selectedGame.publicBetting.spread.awayMoney}%</span>
                      </div>
                    </div>
                  </div>

                  {/* Visual Line Movement Chart with Multiple Sportsbooks */}
                  <div className="line-chart" style={{position: 'relative'}}>
                    <div className="chart-y-axis">
                      <span>-2.5</span>
                      <span>-3.0</span>
                      <span>-3.5</span>
                      <span>-4.0</span>
                      <span>-4.5</span>
                      <span>-5.0</span>
                    </div>
                    <div className="chart-area">
                      {/* Grid lines */}
                      <svg 
                        className="chart-svg" 
                        viewBox="0 0 1000 240" 
                        preserveAspectRatio="none"
                        style={{cursor: 'crosshair'}}
                        onMouseMove={(e) => {
                          const rect = e.currentTarget.getBoundingClientRect();
                          const x = ((e.clientX - rect.left) / rect.width) * 1000;
                          const y = ((e.clientY - rect.top) / rect.height) * 240;
                          setHoveredDataPoint({x, y, data: {spread: -3.5, time: '12/5 2PM'}});
                        }}
                        onMouseLeave={() => setHoveredDataPoint(null)}
                      >
                        <defs>
                          {/* Grid pattern */}
                          <pattern id="grid" width="66.67" height="40" patternUnits="userSpaceOnUse">
                            <path d="M 66.67 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="1"/>
                          </pattern>
                          {/* Glow effect for hover */}
                          <filter id="glow">
                            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                            <feMerge>
                              <feMergeNode in="coloredBlur"/>
                              <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                          </filter>
                        </defs>
                        
                        {/* Grid background */}
                        <rect width="1000" height="240" fill="url(#grid)" />
                        
                        {/* Dynamic chart lines from real data */}
                        {selectedGame.sportsbookOdds && (() => {
                          // Group odds by bookId to create separate lines for each sportsbook
                          const bookIds = [71, 69, 68, 75, 79]; // DraftKings, FanDuel, BetMGM, Caesars, Fanatics
                          const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#a855f7'];
                          const bookNames = ['DraftKings', 'FanDuel', 'BetMGM', 'Caesars', 'Fanatics'];
                          
                          // Get all unique timestamps and sort them
                          const timestamps = [...new Set(selectedGame.sportsbookOdds.map(o => o.timestamp))]
                            .sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
                          
                          if (timestamps.length === 0) return null;
                          
                          // Calculate dynamic scale for Y axis based on actual data
                          const allSpreads = selectedGame.sportsbookOdds.map(o => o.spread).filter(s => s !== null && s !== undefined);
                          const minSpread = Math.min(...allSpreads);
                          const maxSpread = Math.max(...allSpreads);
                          const spreadRange = Math.max(Math.abs(maxSpread - minSpread), 2); // Minimum range of 2
                          const padding = spreadRange * 0.1; // 10% padding
                          const scaleY = (spread: number) => {
                            return ((spread - (maxSpread + padding)) / ((minSpread - padding) - (maxSpread + padding))) * 240;
                          };
                          
                          return bookIds.map((bookId, bookIdx) => {
                            // Get data points for this sportsbook
                            const bookData = timestamps
                              .map((ts, idx) => {
                                const entry = selectedGame.sportsbookOdds!.find(
                                  o => o.bookId === bookId && o.timestamp === ts
                                );
                                if (!entry) return null;
                                
                                const x = (idx / (timestamps.length - 1)) * 1000;
                                const y = scaleY(entry.spread);
                                return { x, y, spread: entry.spread, timestamp: ts };
                              })
                              .filter(d => d !== null);
                            
                            if (bookData.length === 0) return null;
                            
                            // Generate SVG path
                            const pathData = bookData
                              .map((d, i) => `${i === 0 ? 'M' : 'L'} ${d!.x} ${d!.y}`)
                              .join(' ');
                            
                            const lastPoint = bookData[bookData.length - 1]!;
                            
                            return (
                              <g key={bookId}>
                                {/* Line path */}
                                <path
                                  d={pathData}
                                  stroke={colors[bookIdx]}
                                  strokeWidth="2.5"
                                  fill="none"
                                  strokeLinecap="round"
                                  style={{transition: 'all 0.2s ease'}}
                                  className="chart-line"
                                />
                                
                                {/* Data point circles */}
                                {bookData.map((d, i) => (
                                  <circle
                                    key={i}
                                    cx={d!.x}
                                    cy={d!.y}
                                    r={i === bookData.length - 1 ? 5 : 3}
                                    fill={colors[bookIdx]}
                                    style={{cursor: 'pointer', transition: 'all 0.2s ease'}}
                                    filter={i === bookData.length - 1 ? 'url(#glow)' : undefined}
                                    onMouseEnter={(e) => {
                                      e.currentTarget.setAttribute('r', i === bookData.length - 1 ? '7' : '5');
                                      const timestamp = new Date(d!.timestamp);
                                      setHoveredDataPoint({
                                        x: d!.x,
                                        y: d!.y,
                                        data: {
                                          spread: d!.spread > 0 ? `+${d!.spread}` : d!.spread,
                                          time: timestamp.toLocaleString('en-US', {
                                            month: 'short',
                                            day: 'numeric',
                                            hour: 'numeric',
                                            minute: '2-digit',
                                            hour12: true
                                          }),
                                          book: bookNames[bookIdx]
                                        }
                                      });
                                    }}
                                    onMouseLeave={(e) => {
                                      e.currentTarget.setAttribute('r', i === bookData.length - 1 ? '5' : '3');
                                      setHoveredDataPoint(null);
                                    }}
                                  />
                                ))}
                              </g>
                            );
                          });
                        })()}
                        
                        {/* Hover crosshair */}
                        {hoveredDataPoint && (
                          <>
                            <line 
                              x1={hoveredDataPoint.x} 
                              y1="0" 
                              x2={hoveredDataPoint.x} 
                              y2="240" 
                              stroke="rgba(255,255,255,0.2)" 
                              strokeWidth="1"
                              strokeDasharray="4,4"
                            />
                            <line 
                              x1="0" 
                              y1={hoveredDataPoint.y} 
                              x2="1000" 
                              y2={hoveredDataPoint.y} 
                              stroke="rgba(255,255,255,0.2)" 
                              strokeWidth="1"
                              strokeDasharray="4,4"
                            />
                          </>
                        )}
                      </svg>
                      
                      {/* Tooltip */}
                      {hoveredDataPoint && (
                        <div style={{
                          position: 'absolute',
                          left: `${(hoveredDataPoint.x / 1000) * 100}%`,
                          top: `${(hoveredDataPoint.y / 240) * 100}%`,
                          transform: 'translate(-50%, -120%)',
                          background: 'rgba(0, 0, 0, 0.95)',
                          border: '1px solid rgba(255, 255, 255, 0.2)',
                          padding: '10px 14px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          color: '#fff',
                          pointerEvents: 'none',
                          zIndex: 1000,
                          whiteSpace: 'nowrap',
                          backdropFilter: 'blur(10px)'
                        }}>
                          <div style={{fontWeight: 500, marginBottom: '6px', color: '#fff'}}>{hoveredDataPoint.data.book}</div>
                          <div style={{color: '#999', marginBottom: '2px'}}>{hoveredDataPoint.data.time}</div>
                          <div style={{color: '#10b981', fontWeight: 500}}>Spread: {hoveredDataPoint.data.spread}</div>
                        </div>
                      )}
                    </div>
                    <div className="chart-x-axis">
                      {selectedGame.sportsbookOdds && (() => {
                        const timestamps = [...new Set(selectedGame.sportsbookOdds.map(o => o.timestamp))]
                          .sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
                        
                        if (timestamps.length === 0) {
                          return <span>No data</span>;
                        }
                        
                        // Show appropriate intervals based on dataset size
                        const interval = Math.max(1, Math.floor(timestamps.length / 8));
                        return timestamps.map((ts, idx) => {
                          if (idx % interval !== 0 && idx !== timestamps.length - 1) return null;
                          
                          const date = new Date(ts);
                          const now = new Date();
                          const isNow = idx === timestamps.length - 1;
                          
                          let label = '';
                          if (isNow) {
                            label = 'Now';
                          } else {
                            const month = date.getMonth() + 1;
                            const day = date.getDate();
                            const hour = date.getHours();
                            const ampm = hour >= 12 ? 'PM' : 'AM';
                            const displayHour = hour % 12 || 12;
                            label = `${month}/${day} ${displayHour}${ampm}`;
                          }
                          
                          return <span key={idx}>{label}</span>;
                        });
                      })()}
                    </div>
                  </div>
                  
                  {/* Legend */}
                  <div style={{
                    display: 'flex',
                    gap: '20px',
                    marginTop: '16px',
                    paddingTop: '16px',
                    borderTop: '1px solid rgba(255,255,255,0.08)',
                    fontSize: '11px',
                    color: '#999'
                  }}>
                    <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                      <div style={{width: '12px', height: '2px', background: '#3b82f6'}}></div>
                      DraftKings
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                      <div style={{width: '12px', height: '2px', background: '#10b981'}}></div>
                      FanDuel
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                      <div style={{width: '12px', height: '2px', background: '#f59e0b'}}></div>
                      BetMGM
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                      <div style={{width: '12px', height: '2px', background: '#ef4444'}}></div>
                      Caesars
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                      <div style={{width: '12px', height: '2px', background: '#a855f7'}}></div>
                      Fanatics
                    </div>
                  </div>
                </div>
              </div>

              {/* Multi-Sportsbook Table */}
              <div className="modal-section">
                <h3 className="modal-section-title">
                  <LayoutGrid size={14} style={{ marginRight: '8px' }} />
                  Sportsbook Comparison
                </h3>
                
                <div className="sportsbook-table-container">
                  <table className="sportsbook-table">
                    <thead>
                      <tr>
                        <th>Sportsbook</th>
                        <th>Spread</th>
                        <th>Spread Odds</th>
                        <th>Movement</th>
                        <th>Total</th>
                        <th>Total Odds</th>
                        <th>Movement</th>
                        <th>Moneyline</th>
                        <th>Last Updated</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedGame.sportsbookOdds && selectedGame.sportsbookOdds.length > 0 ? (
                        selectedGame.sportsbookOdds
                          .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                          .slice(0, 20)
                          .map((book, idx) => {
                            const bookNames: {[key: number]: string} = {
                              15: 'Consensus',
                              68: 'BetMGM',
                              69: 'FanDuel',
                              71: 'DraftKings',
                              75: 'Caesars',
                              30: 'PointsBet',
                              72: 'BetRivers',
                              73: 'SuperBook',
                              74: 'Unibet',
                              76: 'WynnBET',
                              79: 'Fanatics',
                              83: 'ESPN BET',
                              84: 'Bovada',
                              85: 'BetOnline',
                              86: 'MyBookie'
                            };
                            
                            const bookLogos: {[key: string]: string} = {
                              'DraftKings': DraftkingsLogo,
                              'FanDuel': FanduelLogo,
                              'BetMGM': MGMLogo,
                              'Caesars': CaesarsLogo,
                              'Fanatics': FanaticsLogo
                            };
                            
                            const bookName = bookNames[book.bookId] || `Book ${book.bookId}`;
                            const isBest = idx === 0;
                            
                            // Calculate movement from previous entry
                            const prevBook = selectedGame.sportsbookOdds![idx + 1];
                            const spreadMovement = prevBook ? book.spread - prevBook.spread : 0;
                            const totalMovement = prevBook ? book.total - prevBook.total : 0;
                            
                            // Format timestamp
                            const timestamp = new Date(book.timestamp);
                            const now = new Date();
                            const diffMs = now.getTime() - timestamp.getTime();
                            const diffMins = Math.floor(diffMs / 60000);
                            const diffHours = Math.floor(diffMins / 60);
                            const diffDays = Math.floor(diffHours / 24);
                            
                            let timeAgo = '';
                            let fullTimestamp = '';
                            
                            if (diffMins < 1) {
                              timeAgo = 'Just now';
                            } else if (diffMins < 60) {
                              timeAgo = `${diffMins}m ago`;
                            } else if (diffHours < 24) {
                              timeAgo = `${diffHours}h ago`;
                            } else {
                              timeAgo = `${diffDays}d ago`;
                            }
                            
                            fullTimestamp = timestamp.toLocaleString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              hour: 'numeric',
                              minute: '2-digit',
                              hour12: true
                            });
                            
                            return (
                              <tr key={idx} className={isBest ? 'best-line' : ''}>
                                <td>
                                  <div className="book-name" style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
                                    {bookLogos[bookName] && (
                                      <img 
                                        src={bookLogos[bookName]} 
                                        alt={bookName} 
                                        style={{
                                          height: '28px', 
                                          width: 'auto', 
                                          objectFit: 'contain',
                                          filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.3)) drop-shadow(0 0 8px rgba(255,255,255,0.1))',
                                          transform: 'translateZ(0)',
                                        }} 
                                      />
                                    )}
                                    <span style={{
                                      color: 'rgba(148, 163, 184, 0.7)',
                                      fontSize: '13px',
                                      fontWeight: '500',
                                      letterSpacing: '0.01em'
                                    }}>
                                      {bookName}
                                    </span>
                                    {isBest && <span className="best-badge">LATEST</span>}
                                  </div>
                                </td>
                                <td className="spread-cell">
                                  {book.spread > 0 ? '+' : ''}{book.spread}
                                </td>
                                <td className="odds-cell">
                                  {book.spreadOdds > 0 ? '+' : ''}{book.spreadOdds}
                                </td>
                                <td className="movement-cell">
                                  {spreadMovement === 0 ? (
                                    <span style={{color: '#6b7280'}}>—</span>
                                  ) : spreadMovement > 0 ? (
                                    <span style={{color: '#10b981'}}>↑ {spreadMovement.toFixed(1)}</span>
                                  ) : (
                                    <span style={{color: '#ef4444'}}>↓ {Math.abs(spreadMovement).toFixed(1)}</span>
                                  )}
                                </td>
                                <td className="total-cell">
                                  {book.total}
                                </td>
                                <td className="odds-cell">
                                  {book.totalOdds > 0 ? '+' : ''}{book.totalOdds}
                                </td>
                                <td className="movement-cell">
                                  {totalMovement === 0 ? (
                                    <span style={{color: '#6b7280'}}>—</span>
                                  ) : totalMovement > 0 ? (
                                    <span style={{color: '#10b981'}}>↑ {totalMovement.toFixed(1)}</span>
                                  ) : (
                                    <span style={{color: '#ef4444'}}>↓ {Math.abs(totalMovement).toFixed(1)}</span>
                                  )}
                                </td>
                                <td className="ml-cell">
                                  {book.moneyline > 0 ? '+' : ''}{book.moneyline}
                                </td>
                                <td className="time-cell">
                                  <div style={{display: 'flex', flexDirection: 'column', gap: '2px'}}>
                                    <span style={{fontWeight: 400}}>{timeAgo}</span>
                                    <span style={{fontSize: '10px', color: '#666'}}>{fullTimestamp}</span>
                                  </div>
                                </td>
                              </tr>
                            );
                          })
                      ) : (
                        <tr>
                          <td colSpan={9} style={{textAlign: 'center', padding: '20px', color: '#666'}}>
                            No sportsbook data available
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>

                {/* Line Movement History Table */}
                <div className="line-history-container">
                  <h4 className="history-title">Recent Line Movement History</h4>
                  <div className="history-table-wrapper">
                    <table className="history-table">
                      <thead>
                        <tr>
                          <th>Updated</th>
                          <th>Bet / Money</th>
                          <th>Odds</th>
                          <th>Line</th>
                          <th>Change</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedGame.sportsbookOdds && selectedGame.sportsbookOdds.length > 0 ? (
                          selectedGame.sportsbookOdds
                            .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                            .slice(0, 15)
                            .map((entry, idx) => {
                              const timestamp = new Date(entry.timestamp);
                              const now = new Date();
                              const isToday = timestamp.toDateString() === now.toDateString();
                              const timeStr = timestamp.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
                              const dateStr = isToday ? 'Today' : timestamp.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                              
                              // Get public betting data
                              const awayBet = selectedGame.publicBetting.spread.awayBet;
                              const awayMoney = selectedGame.publicBetting.spread.awayMoney;
                              
                              // Calculate line change from previous entry
                              const prevEntry = selectedGame.sportsbookOdds![idx + 1];
                              const lineChange = prevEntry ? entry.spread - prevEntry.spread : 0;
                              
                              return (
                                <tr key={idx}>
                                  <td>
                                    <div className="time-stamp">{timeStr}<span>{dateStr}</span></div>
                                  </td>
                                  <td className="bet-money">{awayBet}% / {awayMoney}%</td>
                                  <td className="odds-value">{entry.spreadOdds > 0 ? '+' : ''}{entry.spreadOdds}</td>
                                  <td className="line-value">{entry.spread > 0 ? '+' : ''}{entry.spread}</td>
                                  <td>
                                    {lineChange === 0 ? (
                                      <span className="change-badge neutral">-</span>
                                    ) : lineChange > 0 ? (
                                      <span className="change-badge up">▲ {lineChange.toFixed(1)}</span>
                                    ) : (
                                      <span className="change-badge down">▼ {lineChange.toFixed(1)}</span>
                                    )}
                                  </td>
                                </tr>
                              );
                            })
                        ) : (
                          <tr>
                            <td colSpan={5} style={{textAlign: 'center', padding: '20px', color: '#666'}}>
                              No line movement data available
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Sharp Money Analysis */}
              <div className="modal-section">
                <h3 className="modal-section-title">
                  <Zap size={18} style={{ marginRight: '8px' }} />
                  Sharp Money Analysis
                </h3>
                <div className="modal-stats-grid">
                  <div className="modal-stat-card">
                    <div className="modal-stat-label">Spread Public Bets</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.spread.awayBet}% / {selectedGame.publicBetting.spread.homeBet}%</div>
                    <div className="modal-stat-teams">
                      {getTeamData(selectedGame.awayTeam)?.abbreviation} / {getTeamData(selectedGame.homeTeam)?.abbreviation}
                    </div>
                  </div>
                  <div className="modal-stat-card sharp-indicator">
                    <div className="modal-stat-label">Spread Sharp Money</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.spread.awayMoney}% / {selectedGame.publicBetting.spread.homeMoney}%</div>
                    <div className="modal-stat-diff">
                      Difference: {Math.abs(selectedGame.publicBetting.spread.awayMoney - selectedGame.publicBetting.spread.awayBet)}%
                    </div>
                  </div>
                  <div className="modal-stat-card">
                    <div className="modal-stat-label">Moneyline Public Bets</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.ml.awayBet}% / {selectedGame.publicBetting.ml.homeBet}%</div>
                  </div>
                  <div className="modal-stat-card sharp-indicator">
                    <div className="modal-stat-label">Moneyline Sharp Money</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.ml.awayMoney}% / {selectedGame.publicBetting.ml.homeMoney}%</div>
                    <div className="modal-stat-diff">
                      Difference: {Math.abs(selectedGame.publicBetting.ml.awayMoney - selectedGame.publicBetting.ml.awayBet)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Betting Lines */}
              <div className="modal-section">
                <h3 className="modal-section-title">
                  <TrendingUp size={18} style={{ marginRight: '8px' }} />
                  Current Lines
                </h3>
                <div className="modal-lines-grid">
                  <div className="modal-line-card">
                    <div className="modal-line-type">Spread</div>
                    <div className="modal-line-values">
                      <div className="modal-line-item">
                        <span className="modal-line-team">{getTeamData(selectedGame.awayTeam)?.abbreviation}</span>
                        <span className="modal-line-number">{selectedGame.spread.awayLine}</span>
                        <span className="modal-line-odds">{selectedGame.spread.awayOdds}</span>
                      </div>
                      <div className="modal-line-item">
                        <span className="modal-line-team">{getTeamData(selectedGame.homeTeam)?.abbreviation}</span>
                        <span className="modal-line-number">{selectedGame.spread.homeLine}</span>
                        <span className="modal-line-odds">{selectedGame.spread.homeOdds}</span>
                      </div>
                    </div>
                  </div>
                  <div className="modal-line-card">
                    <div className="modal-line-type">Moneyline</div>
                    <div className="modal-line-values">
                      <div className="modal-line-item">
                        <span className="modal-line-team">{getTeamData(selectedGame.awayTeam)?.abbreviation}</span>
                        <span className="modal-line-odds">{selectedGame.moneyline.away.odds}</span>
                      </div>
                      <div className="modal-line-item">
                        <span className="modal-line-team">{getTeamData(selectedGame.homeTeam)?.abbreviation}</span>
                        <span className="modal-line-odds">{selectedGame.moneyline.home.odds}</span>
                      </div>
                    </div>
                  </div>
                  <div className="modal-line-card">
                    <div className="modal-line-type">Total</div>
                    <div className="modal-line-values">
                      <div className="modal-line-item">
                        <span className="modal-line-team">Over</span>
                        <span className="modal-line-number">{selectedGame.total.line}</span>
                        <span className="modal-line-odds">{selectedGame.total.overOdds}</span>
                      </div>
                      <div className="modal-line-item">
                        <span className="modal-line-team">Under</span>
                        <span className="modal-line-number">{selectedGame.total.line}</span>
                        <span className="modal-line-odds">{selectedGame.total.underOdds}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Total Betting Percentages */}
              <div className="modal-section">
                <h3 className="modal-section-title">
                  <Calendar size={18} style={{ marginRight: '8px' }} />
                  Over/Under Analysis
                </h3>
                <div className="modal-stats-grid">
                  <div className="modal-stat-card">
                    <div className="modal-stat-label">Total Public Bets</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.total.overBet}% Over / {selectedGame.publicBetting.total.underBet}% Under</div>
                  </div>
                  <div className="modal-stat-card sharp-indicator">
                    <div className="modal-stat-label">Total Sharp Money</div>
                    <div className="modal-stat-value">{selectedGame.publicBetting.total.overMoney}% Over / {selectedGame.publicBetting.total.underMoney}% Under</div>
                    <div className="modal-stat-diff">
                      Difference: {Math.abs(selectedGame.publicBetting.total.overMoney - selectedGame.publicBetting.total.overBet)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Sharp Play Indicators */}
              {selectedGame.isSharpPlay && (
                <div className="modal-section sharp-play-section">
                  <h3 className="modal-section-title">
                    <Zap size={18} style={{ marginRight: '8px' }} />
                    Sharp Play Detected
                  </h3>
                  {getSharpMoneyIndicators(selectedGame).map((indicator, idx) => (
                    <div key={idx} className={`modal-indicator ${indicator.type}`}>
                      {indicator.text}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EVBettingDashboard;
