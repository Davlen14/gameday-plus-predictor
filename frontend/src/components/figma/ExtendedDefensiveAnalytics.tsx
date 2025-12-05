import React, { useMemo, useState } from 'react';
import { GlassCard } from './GlassCard';
import { Shield, Target, TrendingDown, BarChart3, Check, Info, ChevronDown, ChevronUp, ArrowRight, ArrowLeft } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { extractSection, generateTeamAbbr } from '../../utils/teamUtils';

interface ExtendedDefensiveAnalyticsProps {
  predictionData?: any;
}

export function ExtendedDefensiveAnalytics({ predictionData }: ExtendedDefensiveAnalyticsProps) {
  const [expandedMetric, setExpandedMetric] = useState<string | null>(null);
  const awayTeam = predictionData?.team_selector?.away_team;
  const homeTeam = predictionData?.team_selector?.home_team;

  // Parse Extended Defensive Analytics from EPA and differential sections
  const parseDefensiveAnalytics = useMemo(() => {
    const analysis = predictionData?.formatted_analysis;
    
    if (!analysis || !awayTeam || !homeTeam) {
      return [
        { metric: 'Overall EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'EPA Allowed (Defense)', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Passing EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Rushing EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'EPA Differential', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Success Rate Differential', away: '0.0%', home: '0.0%', advantage: 'Tied' },
        { metric: 'Defensive Plays', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Defensive Drives', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Points Per Opportunity', away: '0.00', home: '0.00', advantage: 'Tied' },
        { metric: 'Field Position Average', away: '0.0', home: '0.0', advantage: 'Tied' }
      ];
    }

    try {
      const metrics = [];
      
      // Simple EPA extraction with safer regex
      const epaMatch = analysis.match(/Overall EPA:\s*([^:]+):\s*([\+\-\d\.]+)\s*([^:]+):\s*([\+\-\d\.]+)/);
      const epaAllowedMatch = analysis.match(/EPA Allowed:\s*([^:]+):\s*([\+\-\d\.]+)\s*([^:]+):\s*([\+\-\d\.]+)/);
      const passEpaMatch = analysis.match(/Passing EPA:\s*([^:]+):\s*([\+\-\d\.]+)\s*([^:]+):\s*([\+\-\d\.]+)/);
      const rushEpaMatch = analysis.match(/Rushing EPA:\s*([^:]+):\s*([\+\-\d\.]+)\s*([^:]+):\s*([\+\-\d\.]+)/);
      
      // Additional defensive metrics from table format
      const defensePlayMatch = analysis.match(/Defense Plays\s+(\d+)\s+(\d+)\s+(\w+)/);
      const defenseDriveMatch = analysis.match(/Defense Drives\s+(\d+)\s+(\d+)\s+(\w+)/);
      const defensePpaMatch = analysis.match(/Defense Total PPA\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      const defensePointsMatch = analysis.match(/Defense Points Per Opp\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      const fieldPosMatch = analysis.match(/Def Field Pos Avg Start\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      const fieldPosPtsMatch = analysis.match(/Def Field Pos Pred Pts\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      
      // Additional havoc and specialized metrics
      const havocFrontMatch = analysis.match(/Def Havoc Front Seven\s+([\d\.]+)%\s+([\d\.]+)%\s+(\w+)/);
      const havocDbMatch = analysis.match(/Def Havoc DB\s+([\d\.]+)%\s+([\d\.]+)%\s+(\w+)/);
      const defRushPpaMatch = analysis.match(/Def Rush Plays PPA\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      const defRushSuccessMatch = analysis.match(/Def Rush Success Rate\s+([\d\.]+)%\s+([\d\.]+)%\s+(\w+)/);
      const defPassPpaMatch = analysis.match(/Def Pass Plays PPA\s+([\d\.\-]+)\s+([\d\.\-]+)\s+(\w+)/);
      const defPassSuccessMatch = analysis.match(/Def Pass Success Rate\s+([\d\.]+)%\s+([\d\.]+)%\s+(\w+)/);
      
      if (epaMatch) {
        const awayEPA = parseFloat(epaMatch[2]) || 0;
        const homeEPA = parseFloat(epaMatch[4]) || 0;
        metrics.push({ 
          metric: 'Overall EPA', 
          away: awayEPA.toFixed(3), 
          home: homeEPA.toFixed(3), 
          advantage: awayEPA > homeEPA ? awayTeam.name : homeTeam.name 
        });
      }

      if (epaAllowedMatch) {
        const awayEPAAllowed = parseFloat(epaAllowedMatch[2]) || 0;
        const homeEPAAllowed = parseFloat(epaAllowedMatch[4]) || 0;
        metrics.push({ 
          metric: 'EPA Allowed (Defense)', 
          away: awayEPAAllowed.toFixed(3), 
          home: homeEPAAllowed.toFixed(3), 
          advantage: awayEPAAllowed < homeEPAAllowed ? awayTeam.name : homeTeam.name 
        });
      }

      if (passEpaMatch) {
        const awayPassEPA = parseFloat(passEpaMatch[2]) || 0;
        const homePassEPA = parseFloat(passEpaMatch[4]) || 0;
        metrics.push({ 
          metric: 'Passing EPA', 
          away: awayPassEPA.toFixed(3), 
          home: homePassEPA.toFixed(3), 
          advantage: awayPassEPA > homePassEPA ? awayTeam.name : homeTeam.name 
        });
      }

      if (rushEpaMatch) {
        const awayRushEPA = parseFloat(rushEpaMatch[2]) || 0;
        const homeRushEPA = parseFloat(rushEpaMatch[4]) || 0;
        metrics.push({ 
          metric: 'Rushing EPA', 
          away: awayRushEPA.toFixed(3), 
          home: homeRushEPA.toFixed(3), 
          advantage: awayRushEPA > homeRushEPA ? awayTeam.name : homeTeam.name 
        });
      }

      // Add additional defensive metrics
      if (defensePlayMatch) {
        const awayPlays = parseInt(defensePlayMatch[1]) || 0;
        const homePlays = parseInt(defensePlayMatch[2]) || 0;
        metrics.push({ 
          metric: 'Defense Plays', 
          away: awayPlays.toString(), 
          home: homePlays.toString(), 
          advantage: defensePlayMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defenseDriveMatch) {
        const awayDrives = parseInt(defenseDriveMatch[1]) || 0;
        const homeDrives = parseInt(defenseDriveMatch[2]) || 0;
        metrics.push({ 
          metric: 'Defense Drives', 
          away: awayDrives.toString(), 
          home: homeDrives.toString(), 
          advantage: defenseDriveMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defensePpaMatch) {
        const awayPpa = parseFloat(defensePpaMatch[1]) || 0;
        const homePpa = parseFloat(defensePpaMatch[2]) || 0;
        metrics.push({ 
          metric: 'Defense Total PPA', 
          away: awayPpa.toFixed(2), 
          home: homePpa.toFixed(2), 
          advantage: defensePpaMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defensePointsMatch) {
        const awayPoints = parseFloat(defensePointsMatch[1]) || 0;
        const homePoints = parseFloat(defensePointsMatch[2]) || 0;
        metrics.push({ 
          metric: 'Points Per Opportunity', 
          away: awayPoints.toFixed(2), 
          home: homePoints.toFixed(2), 
          advantage: defensePointsMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (fieldPosMatch) {
        const awayFieldPos = parseFloat(fieldPosMatch[1]) || 0;
        const homeFieldPos = parseFloat(fieldPosMatch[2]) || 0;
        metrics.push({ 
          metric: 'Field Position Average', 
          away: awayFieldPos.toFixed(1), 
          home: homeFieldPos.toFixed(1), 
          advantage: fieldPosMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (fieldPosPtsMatch) {
        const awayFieldPts = parseFloat(fieldPosPtsMatch[1]) || 0;
        const homeFieldPts = parseFloat(fieldPosPtsMatch[2]) || 0;
        metrics.push({ 
          metric: 'Field Position Predicted Points', 
          away: awayFieldPts.toFixed(3), 
          home: homeFieldPts.toFixed(3), 
          advantage: fieldPosPtsMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      // Havoc metrics
      if (havocFrontMatch) {
        const awayHavocFront = parseFloat(havocFrontMatch[1]) || 0;
        const homeHavocFront = parseFloat(havocFrontMatch[2]) || 0;
        metrics.push({ 
          metric: 'Havoc Front Seven', 
          away: awayHavocFront.toFixed(1) + '%', 
          home: homeHavocFront.toFixed(1) + '%', 
          advantage: havocFrontMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (havocDbMatch) {
        const awayHavocDb = parseFloat(havocDbMatch[1]) || 0;
        const homeHavocDb = parseFloat(havocDbMatch[2]) || 0;
        metrics.push({ 
          metric: 'Havoc DB', 
          away: awayHavocDb.toFixed(1) + '%', 
          home: homeHavocDb.toFixed(1) + '%', 
          advantage: havocDbMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      // Defensive play type metrics
      if (defRushPpaMatch) {
        const awayRushPpa = parseFloat(defRushPpaMatch[1]) || 0;
        const homeRushPpa = parseFloat(defRushPpaMatch[2]) || 0;
        metrics.push({ 
          metric: 'Def Rush Plays PPA', 
          away: awayRushPpa.toFixed(3), 
          home: homeRushPpa.toFixed(3), 
          advantage: defRushPpaMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defRushSuccessMatch) {
        const awayRushSuccess = parseFloat(defRushSuccessMatch[1]) || 0;
        const homeRushSuccess = parseFloat(defRushSuccessMatch[2]) || 0;
        metrics.push({ 
          metric: 'Def Rush Success Rate', 
          away: awayRushSuccess.toFixed(1) + '%', 
          home: homeRushSuccess.toFixed(1) + '%', 
          advantage: defRushSuccessMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defPassPpaMatch) {
        const awayPassPpa = parseFloat(defPassPpaMatch[1]) || 0;
        const homePassPpa = parseFloat(defPassPpaMatch[2]) || 0;
        metrics.push({ 
          metric: 'Def Pass Plays PPA', 
          away: awayPassPpa.toFixed(3), 
          home: homePassPpa.toFixed(3), 
          advantage: defPassPpaMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      if (defPassSuccessMatch) {
        const awayPassSuccess = parseFloat(defPassSuccessMatch[1]) || 0;
        const homePassSuccess = parseFloat(defPassSuccessMatch[2]) || 0;
        metrics.push({ 
          metric: 'Def Pass Success Rate', 
          away: awayPassSuccess.toFixed(1) + '%', 
          home: homePassSuccess.toFixed(1) + '%', 
          advantage: defPassSuccessMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      return metrics.length > 0 ? metrics : [
        { metric: 'Overall EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'EPA Allowed (Defense)', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Passing EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Rushing EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Defense Plays', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Defense Drives', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Defense Total PPA', away: '0.00', home: '0.00', advantage: 'Tied' },
        { metric: 'Points Per Opportunity', away: '0.00', home: '0.00', advantage: 'Tied' }
      ];
    } catch (error) {
      console.error('Error parsing defensive analytics:', error);
      return [
        { metric: 'Overall EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'EPA Allowed (Defense)', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Passing EPA', away: '0.000', home: '0.000', advantage: 'Tied' },
        { metric: 'Rushing EPA', away: '0.000', home: '0.000', advantage: 'Tied' }
      ];
    }
  }, [predictionData?.formatted_analysis, awayTeam, homeTeam]);

  // Parse Season Summary Statistics from advanced metrics and field position data
  const parseSeasonSummary = useMemo(() => {
    const analysis = predictionData?.formatted_analysis;
    
    if (!analysis || !awayTeam || !homeTeam) {
      return [
        { metric: 'ELO Rating', away: '1500', home: '1500', advantage: 'Tied' },
        { metric: 'FPI Rating', away: '0.0', home: '0.0', advantage: 'Tied' },
        { metric: 'Success Rate', away: '50.0%', home: '50.0%', advantage: 'Tied' },
        { metric: 'Explosiveness', away: '1.000', home: '1.000', advantage: 'Tied' },
        { metric: 'Total Plays', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Total Drives', away: '0', home: '0', advantage: 'Tied' }
      ];
    }

    try {
      const metrics = [];
      
      // Extract ELO ratings
      const eloMatch = analysis.match(/ELO Ratings:\s*([^:]+):\s*(\d+)\s*([^:]+):\s*(\d+)/);
      if (eloMatch) {
        const awayElo = parseInt(eloMatch[2]) || 1500;
        const homeElo = parseInt(eloMatch[4]) || 1500;
        metrics.push({ 
          metric: 'ELO Rating', 
          away: awayElo.toString(), 
          home: homeElo.toString(), 
          advantage: awayElo > homeElo ? awayTeam.name : homeTeam.name 
        });
      }

      // Extract FPI ratings
      const fpiMatch = analysis.match(/FPI Ratings:\s*([^:]+):\s*([\d\.]+)\s*([^:]+):\s*([\d\.]+)/);
      if (fpiMatch) {
        const awayFpi = parseFloat(fpiMatch[2]) || 0;
        const homeFpi = parseFloat(fpiMatch[4]) || 0;
        metrics.push({ 
          metric: 'FPI Rating', 
          away: awayFpi.toFixed(2), 
          home: homeFpi.toFixed(2), 
          advantage: awayFpi > homeFpi ? awayTeam.name : homeTeam.name 
        });
      }

      // Extract Success Rate
      const successMatch = analysis.match(/Success Rate:\s*([^:]+):\s*([\d\.]+)\s*([^:]+):\s*([\d\.]+)/);
      if (successMatch) {
        const awaySuccess = parseFloat(successMatch[2]) || 0.5;
        const homeSuccess = parseFloat(successMatch[4]) || 0.5;
        metrics.push({ 
          metric: 'Success Rate', 
          away: (awaySuccess * 100).toFixed(1) + '%', 
          home: (homeSuccess * 100).toFixed(1) + '%', 
          advantage: awaySuccess > homeSuccess ? awayTeam.name : homeTeam.name 
        });
      }

      // Extract Explosiveness
      const explosiveMatch = analysis.match(/Explosiveness:\s*([^:]+):\s*([\d\.]+)\s*([^:]+):\s*([\d\.]+)/);
      if (explosiveMatch) {
        const awayExplosive = parseFloat(explosiveMatch[2]) || 1;
        const homeExplosive = parseFloat(explosiveMatch[4]) || 1;
        metrics.push({ 
          metric: 'Explosiveness', 
          away: awayExplosive.toFixed(3), 
          home: homeExplosive.toFixed(3), 
          advantage: awayExplosive > homeExplosive ? awayTeam.name : homeTeam.name 
        });
      }

      // Add Season Summary metrics from defensive table
      const gamesPlayedMatch = analysis.match(/Games Played\s+(\d+)\s+(\d+)\s+(\w+)/);
      if (gamesPlayedMatch) {
        const awayGames = parseInt(gamesPlayedMatch[1]) || 0;
        const homeGames = parseInt(gamesPlayedMatch[2]) || 0;
        metrics.push({ 
          metric: 'Games Played', 
          away: awayGames.toString(), 
          home: homeGames.toString(), 
          advantage: gamesPlayedMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const totalYardsMatch = analysis.match(/Total Offensive Yards\s+([\d,]+)\s+([\d,]+)\s+(\w+)/);
      if (totalYardsMatch) {
        const awayYards = totalYardsMatch[1].replace(',', '');
        const homeYards = totalYardsMatch[2].replace(',', '');
        metrics.push({ 
          metric: 'Total Offensive Yards', 
          away: awayYards, 
          home: homeYards, 
          advantage: totalYardsMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const firstDownsAllowedMatch = analysis.match(/First Downs Allowed\s+(\d+)\s+(\d+)\s+(\w+)/);
      if (firstDownsAllowedMatch) {
        const awayFirstDowns = parseInt(firstDownsAllowedMatch[1]) || 0;
        const homeFirstDowns = parseInt(firstDownsAllowedMatch[2]) || 0;
        metrics.push({ 
          metric: 'First Downs Allowed', 
          away: awayFirstDowns.toString(), 
          home: homeFirstDowns.toString(), 
          advantage: firstDownsAllowedMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const turnoversCreatedMatch = analysis.match(/Turnovers Created\s+(\d+)\s+(\d+)\s+(\w+)/);
      if (turnoversCreatedMatch) {
        const awayTurnovers = parseInt(turnoversCreatedMatch[1]) || 0;
        const homeTurnovers = parseInt(turnoversCreatedMatch[2]) || 0;
        metrics.push({ 
          metric: 'Turnovers Created', 
          away: awayTurnovers.toString(), 
          home: homeTurnovers.toString(), 
          advantage: turnoversCreatedMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const turnoverMarginMatch = analysis.match(/Turnover Margin\s+([\+\-]?\d+)\s+([\+\-]?\d+)\s+(\w+)/);
      if (turnoverMarginMatch) {
        const awayMargin = turnoverMarginMatch[1];
        const homeMargin = turnoverMarginMatch[2];
        metrics.push({ 
          metric: 'Turnover Margin', 
          away: awayMargin, 
          home: homeMargin, 
          advantage: turnoverMarginMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const penaltiesMatch = analysis.match(/Penalties Per Game\s+([\d\.]+)\s+([\d\.]+)\s+(\w+)/);
      if (penaltiesMatch) {
        const awayPenalties = parseFloat(penaltiesMatch[1]) || 0;
        const homePenalties = parseFloat(penaltiesMatch[2]) || 0;
        metrics.push({ 
          metric: 'Penalties Per Game', 
          away: awayPenalties.toFixed(1), 
          home: homePenalties.toFixed(1), 
          advantage: penaltiesMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      const penaltyYardsMatch = analysis.match(/Penalty Yards Per Game\s+([\d\.]+)\s+([\d\.]+)\s+(\w+)/);
      if (penaltyYardsMatch) {
        const awayPenaltyYards = parseFloat(penaltyYardsMatch[1]) || 0;
        const homePenaltyYards = parseFloat(penaltyYardsMatch[2]) || 0;
        metrics.push({ 
          metric: 'Penalty Yards Per Game', 
          away: awayPenaltyYards.toFixed(1), 
          home: homePenaltyYards.toFixed(1), 
          advantage: penaltyYardsMatch[3] === 'Away' ? awayTeam.name : homeTeam.name 
        });
      }

      return metrics.length > 0 ? metrics : [
        { metric: 'ELO Rating', away: '1500', home: '1500', advantage: 'Tied' },
        { metric: 'FPI Rating', away: '0.0', home: '0.0', advantage: 'Tied' },
        { metric: 'Success Rate', away: '50.0%', home: '50.0%', advantage: 'Tied' },
        { metric: 'Explosiveness', away: '1.000', home: '1.000', advantage: 'Tied' },
        { metric: 'Games Played', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Total Offensive Yards', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'First Downs Allowed', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Turnovers Created', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Turnover Margin', away: '0', home: '0', advantage: 'Tied' },
        { metric: 'Penalties Per Game', away: '0.0', home: '0.0', advantage: 'Tied' },
        { metric: 'Penalty Yards Per Game', away: '0.0', home: '0.0', advantage: 'Tied' }
      ];
    } catch (error) {
      console.error('Error parsing season summary:', error);
      return [
        { metric: 'ELO Rating', away: '1500', home: '1500', advantage: 'Tied' },
        { metric: 'FPI Rating', away: '0.0', home: '0.0', advantage: 'Tied' },
        { metric: 'Success Rate', away: '50.0%', home: '50.0%', advantage: 'Tied' },
        { metric: 'Explosiveness', away: '1.000', home: '1.000', advantage: 'Tied' }
      ];
    }
  }, [predictionData?.formatted_analysis, awayTeam, homeTeam]);

  const defensiveData = parseDefensiveAnalytics;
  const summaryData = parseSeasonSummary;
  
  // Helper function to check if color is blue or black
  const isBlueOrBlack = (color: string) => {
    const hex = color.toLowerCase();
    // Check for blue colors (dark blue, navy, etc.)
    const isBlue = hex.includes('004') || hex.includes('003') || hex.includes('002') || hex.includes('001') || 
                   hex === '#000080' || hex === '#003366' || hex === '#002244' || hex === '#041e42';
    // Check for black/very dark colors
    const isBlack = hex === '#000000' || hex === '#222222' || hex === '#1a1a1a' || hex === '#333333';
    return isBlue || isBlack;
  };

  // Use team data or fallback
  const team1Logo = awayTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png";
  const team2Logo = homeTeam?.logo || "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png";
  const team1Name = awayTeam?.name || "Ohio State";
  const team2Name = homeTeam?.name || "Illinois";
  
  // Get display colors - use alt_color if primary is blue/black
  const team1Color = (awayTeam?.primary_color && isBlueOrBlack(awayTeam.primary_color)) 
    ? (awayTeam.alt_color || awayTeam.secondary_color || '#ce1141') 
    : (awayTeam?.primary_color || "#ce1141");
    
  const team2Color = (homeTeam?.primary_color && isBlueOrBlack(homeTeam.primary_color)) 
    ? (homeTeam.alt_color || homeTeam.secondary_color || '#ff5f05') 
    : (homeTeam?.primary_color || "#ff5f05");
  const team1Abbr = awayTeam ? generateTeamAbbr(awayTeam.name) : "OSU";
  const team2Abbr = homeTeam ? generateTeamAbbr(homeTeam.name) : "ILL";

  // Calculate highlights from real data  
  const epaAllowedAway = defensiveData.find(d => d.metric === 'EPA Allowed (Defense)')?.away || '0.000';
  const epaAllowedHome = defensiveData.find(d => d.metric === 'EPA Allowed (Defense)')?.home || '0.000';
  const epaAllowedAwayNum = parseFloat(epaAllowedAway);
  const epaAllowedHomeNum = parseFloat(epaAllowedHome);
  const epaAllowedDiff = Math.abs(epaAllowedAwayNum - epaAllowedHomeNum).toFixed(3);
  const epaAllowedAdvantage = epaAllowedAwayNum < epaAllowedHomeNum ? team1Abbr : team2Abbr;

  
  const overallEpaAway = defensiveData.find(d => d.metric === 'Overall EPA')?.away || '0.000';
  const overallEpaHome = defensiveData.find(d => d.metric === 'Overall EPA')?.home || '0.000';
  const overallEpaAwayNum = parseFloat(overallEpaAway);
  const overallEpaHomeNum = parseFloat(overallEpaHome);
  const overallEpaDiff = Math.abs(overallEpaAwayNum - overallEpaHomeNum).toFixed(3);
  const overallEpaAdvantage = overallEpaAwayNum > overallEpaHomeNum ? team1Abbr : team2Abbr;
  
  const successRateAway = summaryData.find(d => d.metric === 'Success Rate')?.away || '50.0%';
  const successRateHome = summaryData.find(d => d.metric === 'Success Rate')?.home || '50.0%';
  const successAwayNum = parseFloat(successRateAway.replace('%', ''));
  const successHomeNum = parseFloat(successRateHome.replace('%', ''));
  const successDiff = Math.abs(successAwayNum - successHomeNum).toFixed(1);
  const successAdvantage = successAwayNum > successHomeNum ? team1Abbr : team2Abbr;  const turnoverMarginAway = summaryData.find(d => d.metric === 'Turnover Margin')?.away || '0';
  const turnoverMarginHome = summaryData.find(d => d.metric === 'Turnover Margin')?.home || '0';
  const marginAwayNum = parseInt(turnoverMarginAway.replace('+', ''));
  const marginHomeNum = parseInt(turnoverMarginHome.replace('+', ''));
  const marginDiff = Math.abs(marginAwayNum - marginHomeNum);
  const marginAdvantage = marginAwayNum > marginHomeNum ? team1Abbr : team2Abbr;
  return (
    <div className="space-y-6">
      {/* Extended Defensive Analytics */}
      <GlassCard glowColor={`from-[${team1Color}]/20 to-[${team2Color}]/20`} className="p-4 sm:p-6 border-gray-500/40">
        <div className="flex items-center justify-between mb-4 sm:mb-6">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="p-1.5 sm:p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
              <Shield className="w-4 h-4 sm:w-5 sm:h-5 text-red-400" />
            </div>
            <h3 className="text-white font-semibold text-sm sm:text-base">Extended Defensive Analytics</h3>
          </div>
          
          {/* Team Legend */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={team1Logo}
                alt={team1Name}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team1Color }}>{team1Abbr}</span>
            </div>
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={team2Logo}
                alt={team2Name}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team2Color }}>{team2Abbr}</span>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          {defensiveData.map((data, index) => {
            // Parse values for comparison
            const parseVal = (val: string): number => {
              if (val.includes('%')) return parseFloat(val.replace('%', ''));
              if (val.includes(':')) {
                const [min, sec] = val.split(':').map(Number);
                return min + sec / 60;
              }
              if (val.startsWith('+') || val.startsWith('-')) return parseFloat(val);
              return parseFloat(val.replace(/,/g, '')) || 0;
            };
            
            const awayVal = parseVal(data.away);
            const homeVal = parseVal(data.home);
            const diff = awayVal - homeVal;
            const isExpanded = expandedMetric === data.metric;
            
            // Calculate bar widths (0-100% scale)
            const maxVal = Math.max(Math.abs(awayVal), Math.abs(homeVal));
            const awayBarWidth = maxVal > 0 ? `${(Math.abs(awayVal) / maxVal) * 100}%` : '0%';
            const homeBarWidth = maxVal > 0 ? `${(Math.abs(homeVal) / maxVal) * 100}%` : '0%';
            
            return (
              <div key={index} className="space-y-0">
                <div 
                  className="backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-white/5"
                  onClick={() => setExpandedMetric(isExpanded ? null : data.metric)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold"
                        style={{ 
                          fontSize: '1.25rem',
                          color: team1Color,
                          textShadow: `0 0 10px ${team1Color}40`
                        }}
                      >
                        {data.away}
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: awayBarWidth,
                          background: `linear-gradient(to right, ${team1Color}80, ${team1Color})`,
                          boxShadow: `0 0 12px ${team1Color}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff < -0.1 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{data.metric}</span>
                        {diff > 0.1 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className="analytical-number text-sm"
                        style={{ 
                          color: data.advantage === team1Name ? team1Color : data.advantage === team2Name ? team2Color : '#22d3ee',
                          textShadow: `0 0 8px ${data.advantage === team1Name ? team1Color : data.advantage === team2Name ? team2Color : '#22d3ee'}40`
                        }}
                      >
                        {data.advantage === 'Tied' || data.advantage === 'Even' ? 'Even' : `${data.advantage === team1Name ? team1Abbr : team2Abbr} +${Math.abs(diff).toFixed(2)}`}
                      </div>
                      <span className="text-xs text-slate-500">Defensive Metric</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold"
                        style={{ 
                          fontSize: '1.25rem',
                          color: team2Color,
                          textShadow: `0 0 10px ${team2Color}40`
                        }}
                      >
                        {data.home}
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: homeBarWidth,
                          background: `linear-gradient(to left, ${team2Color}80, ${team2Color})`,
                          boxShadow: `0 0 12px ${team2Color}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {data.metric} comparison: {team1Name} ({data.away}) vs {team2Name} ({data.home}). 
                      {data.advantage !== 'Tied' && data.advantage !== 'Even' 
                        ? `${data.advantage} holds the advantage in this defensive metric.`
                        : 'Both teams are evenly matched in this metric.'}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </GlassCard>

      {/* Season Summary Statistics */}
      <GlassCard glowColor={`from-${team1Color.replace('#', '')}/20 to-${team2Color.replace('#', '')}/20`} className="p-4 sm:p-6 border-gray-500/40">
        <div className="flex items-center justify-between mb-4 sm:mb-6">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="p-1.5 sm:p-2 rounded-lg bg-slate-500/20 border border-gray-500/40">
              <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400" />
            </div>
            <h3 className="text-white font-semibold text-sm sm:text-base">Season Summary Statistics</h3>
          </div>
          
          {/* Team Legend */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={team1Logo}
                alt={team1Name}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team1Color }}>{team1Abbr}</span>
            </div>
            <div className="flex items-center gap-2">
              <ImageWithFallback 
                src={team2Logo}
                alt={team2Name}
                className="w-6 h-6 object-contain"
              />
              <span className="text-xs font-bold" style={{ color: team2Color }}>{team2Abbr}</span>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          {summaryData.map((data, index) => {
            // Parse values for comparison
            const parseVal = (val: string): number => {
              if (val.includes('%')) return parseFloat(val.replace('%', ''));
              if (val.includes(':')) {
                const [min, sec] = val.split(':').map(Number);
                return min + sec / 60;
              }
              if (val.startsWith('+') || val.startsWith('-')) return parseFloat(val);
              return parseFloat(val.replace(/,/g, '')) || 0;
            };
            
            const awayVal = parseVal(data.away);
            const homeVal = parseVal(data.home);
            const diff = awayVal - homeVal;
            const isExpanded = expandedMetric === data.metric;
            
            // Calculate bar widths
            const maxVal = Math.max(Math.abs(awayVal), Math.abs(homeVal));
            const awayBarWidth = maxVal > 0 ? `${(Math.abs(awayVal) / maxVal) * 100}%` : '0%';
            const homeBarWidth = maxVal > 0 ? `${(Math.abs(homeVal) / maxVal) * 100}%` : '0%';
            
            return (
              <div key={index} className="space-y-0">
                <div 
                  className="backdrop-blur-sm p-4 rounded-lg border border-white/10 hover:border-white/20 transition-all cursor-pointer hover:bg-white/5"
                  onClick={() => setExpandedMetric(isExpanded ? null : data.metric)}
                  style={{
                    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-center">
                    {/* Away Team Value (Left) */}
                    <div className="text-right space-y-1">
                      <div 
                        className="analytical-number font-bold"
                        style={{ 
                          fontSize: '1.25rem',
                          color: team1Color,
                          textShadow: `0 0 10px ${team1Color}40`
                        }}
                      >
                        {data.away}
                      </div>
                      <div 
                        className="h-2 rounded-full ml-auto transition-all duration-300"
                        style={{ 
                          width: awayBarWidth,
                          background: `linear-gradient(to right, ${team1Color}80, ${team1Color})`,
                          boxShadow: `0 0 12px ${team1Color}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>

                    {/* Center (Metric Info) */}
                    <div className="flex flex-col items-center gap-1 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        {diff < -0.1 && (
                          <ArrowLeft className="w-4 h-4 text-green-400" />
                        )}
                        <span className="text-slate-300 text-sm">{data.metric}</span>
                        {diff > 0.1 && (
                          <ArrowRight className="w-4 h-4 text-green-400" />
                        )}
                        <Info className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 transition-colors" />
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </div>
                      <div 
                        className="analytical-number text-sm"
                        style={{ 
                          color: data.advantage === team1Name ? team1Color : data.advantage === team2Name ? team2Color : '#22d3ee',
                          textShadow: `0 0 8px ${data.advantage === team1Name ? team1Color : data.advantage === team2Name ? team2Color : '#22d3ee'}40`
                        }}
                      >
                        {data.advantage === 'Tied' || data.advantage === 'Even' ? 'Even' : `${data.advantage === team1Name ? team1Abbr : team2Abbr} +${Math.abs(diff).toFixed(2)}`}
                      </div>
                      <span className="text-xs text-slate-500">Season Statistic</span>
                    </div>

                    {/* Home Team Value (Right) */}
                    <div className="text-left space-y-1">
                      <div 
                        className="analytical-number font-bold"
                        style={{ 
                          fontSize: '1.25rem',
                          color: team2Color,
                          textShadow: `0 0 10px ${team2Color}40`
                        }}
                      >
                        {data.home}
                      </div>
                      <div 
                        className="h-2 rounded-full transition-all duration-300"
                        style={{ 
                          width: homeBarWidth,
                          background: `linear-gradient(to left, ${team2Color}80, ${team2Color})`,
                          boxShadow: `0 0 12px ${team2Color}60, inset 0 1px 2px rgba(255,255,255,0.2)`
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 leading-relaxed px-4">
                      {data.metric} comparison: {team1Name} ({data.away}) vs {team2Name} ({data.home}). 
                      {data.advantage !== 'Tied' && data.advantage !== 'Even' 
                        ? `${data.advantage} holds the advantage in this statistical category.`
                        : 'Both teams are evenly matched in this category.'}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </GlassCard>

      {/* Defensive Efficiency Visualization - Modernized */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Defense Plays Card */}
        <GlassCard glowColor="from-emerald-500/20 to-green-500/20" className="p-5 border-emerald-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-green-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40 shadow-lg shadow-emerald-500/20">
                <Target className="w-6 h-6 text-emerald-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                ELITE
              </div>
            </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-3xl font-bold text-white drop-shadow-lg">{epaAllowedAway}</span>
                  <span className="text-sm text-gray-400">vs</span>
                  <span className="text-3xl font-bold text-white drop-shadow-lg">{epaAllowedHome}</span>
                </div>
                <div className="text-sm text-gray-300 font-medium">EPA Allowed (Defense)</div>
                <div className="mt-3 p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                  <div className="text-xs text-emerald-400 font-semibold">
                    {epaAllowedAdvantage} Advantage: <span className="text-white">{epaAllowedDiff}</span> EPA difference
                  </div>
                </div>
              </div>
          </div>
        </GlassCard>

        {/* Points Per Opportunity Card */}
        <GlassCard glowColor="from-cyan-500/20 to-blue-500/20" className="p-5 border-cyan-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-cyan-500/20 border border-cyan-500/40 shadow-lg shadow-cyan-500/20">
                <TrendingDown className="w-6 h-6 text-cyan-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                EFFICIENCY
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-white drop-shadow-lg">{overallEpaAway}</span>
                <span className="text-sm text-gray-400">vs</span>
                <span className="text-3xl font-bold text-white drop-shadow-lg">{overallEpaHome}</span>
              </div>
              <div className="text-sm text-gray-300 font-medium">Overall EPA</div>
              <div className="mt-3 p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
                <div className="text-xs text-cyan-400 font-semibold">
                  {overallEpaAdvantage} advantage: <span className="text-white">{overallEpaDiff}</span> EPA difference
                </div>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Turnover Margin Card */}
        <GlassCard glowColor="from-amber-500/20 to-orange-500/20" className="p-5 border-amber-500/40 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
          <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg bg-amber-500/20 border border-amber-500/40 shadow-lg shadow-amber-500/20">
                <Shield className="w-6 h-6 text-amber-400" />
              </div>
              <div className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/40">
                IMPACT
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-white drop-shadow-lg">{successRateAway}</span>
                <span className="text-sm text-gray-400">vs</span>
                <span className="text-3xl font-bold text-white drop-shadow-lg">{successRateHome}</span>
              </div>
              <div className="text-sm text-gray-300 font-medium">Success Rate</div>
              <div className="mt-3 p-2 rounded-lg bg-amber-500/10 border border-amber-500/30">
                <div className="text-xs text-amber-400 font-semibold">
                  {successAdvantage} <span className="text-white">+{successDiff}%</span> advantage 
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

function DefenseStatRow({ metric, away, home, advantage, awayTeam, homeTeam }: { 
  metric: string; 
  away: string; 
  home: string; 
  advantage: string;
  awayTeam?: any;
  homeTeam?: any;
}) {
  const getAdvantageDisplay = (adv: string) => {
    // Check if advantage matches team name
    const isAwayAdvantage = awayTeam && adv === awayTeam.name;
    const isHomeAdvantage = homeTeam && adv === homeTeam.name;
    
    if (isAwayAdvantage) {
      return (
        <div className="flex items-center justify-center gap-2">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-green-500/20 rounded-lg blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <ImageWithFallback 
              src={awayTeam.logo}
              alt={awayTeam.name}
              className="relative w-7 h-7 object-contain transform hover:scale-125 transition-all duration-200"
              style={{
                filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.4))',
              }}
            />
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-emerald-400 to-green-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/50">
              <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
            </div>
          </div>
        </div>
      );
    }
    
    if (isHomeAdvantage) {
      return (
        <div className="flex items-center justify-center gap-2">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-green-500/20 rounded-lg blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <ImageWithFallback 
              src={homeTeam.logo}
              alt={homeTeam.name}
              className="relative w-7 h-7 object-contain transform hover:scale-125 transition-all duration-200"
              style={{
                filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.4))',
              }}
            />
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-emerald-400 to-green-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/50">
              <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
            </div>
          </div>
        </div>
      );
    }
    
    return (
      <span className="px-3 py-1.5 rounded-full text-xs font-bold text-slate-400 bg-slate-500/20 border border-slate-500/30 hover:border-slate-500/50 transition-colors">
        {adv}
      </span>
    );
  };

  return (
    <tr className="border-b border-gray-700/20 hover:bg-gradient-to-r hover:from-gray-800/40 hover:to-gray-800/20 transition-all duration-200 group">
      <td className="py-4 px-4 text-gray-300 font-semibold group-hover:text-white transition-colors">{metric}</td>
      <td className="py-4 px-4 text-center">
        <span className="font-mono text-base text-gray-200 group-hover:text-white transition-colors font-semibold">
          {away}
        </span>
      </td>
      <td className="py-4 px-4 text-center">
        <span className="font-mono text-base text-gray-200 group-hover:text-white transition-colors font-semibold">
          {home}
        </span>
      </td>
      <td className="py-4 px-4 text-center">
        {getAdvantageDisplay(advantage)}
      </td>
    </tr>
  );
}