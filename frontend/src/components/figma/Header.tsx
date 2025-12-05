import { Calendar, Clock, Tv, Star } from 'lucide-react';
import { GlassCard } from './GlassCard';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface HeaderProps {
  predictionData?: {
    header?: {
      game_info?: {
        date?: string;
        time?: string;
        network?: string;
        excitement_index?: number;
      };
      teams?: {
        away?: {
          name?: string;
          record?: string;
          logo?: string;
          rank?: number;
        };
        home?: {
          name?: string;
          record?: string;
          logo?: string;
          rank?: number;
        };
      };
    };
    team_selector?: {
      home_team?: {
        primary_color?: string;
        alt_color?: string;
      };
      away_team?: {
        primary_color?: string;
        alt_color?: string;
      };
    };
  };
  isLoading?: boolean;
}

export function Header({ predictionData, isLoading }: HeaderProps) {
  // Demo data: Week 13 Ranked Matchup - #16 USC @ #6 Oregon
  const demoData = {
    game_info: {
      date: "November 22, 2025",
      time: "8:30 PM ET",
      network: "NBC",
      excitement_index: 8.7
    },
    teams: {
      away: {
        name: "USC",
        record: "8-3",
        logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/30.png",
        rank: 16
      },
      home: {
        name: "Oregon", 
        record: "11-0",
        logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/2483.png",
        rank: 6
      }
    }
  };

  // Use live data from ui_components.header if available, otherwise use demo data
  const headerData = predictionData?.header || demoData;
  
  const homeTeam = headerData.teams?.home?.name || demoData.teams.home.name;
  const awayTeam = headerData.teams?.away?.name || demoData.teams.away.name;
  const homeRecord = headerData.teams?.home?.record || demoData.teams.home.record;
  const awayRecord = headerData.teams?.away?.record || demoData.teams.away.record;
  const homeRank = predictionData?.header?.teams?.home?.rank;
  const awayRank = predictionData?.header?.teams?.away?.rank;
  const homeLogo = headerData.teams?.home?.logo || demoData.teams.home.logo;
  const awayLogo = headerData.teams?.away?.logo || demoData.teams.away.logo;
  const gameDate = headerData.game_info?.date || demoData.game_info.date;
  const gameTime = headerData.game_info?.time || demoData.game_info.time;
  const network = headerData.game_info?.network || demoData.game_info.network;
  const excitementIndex = headerData.game_info?.excitement_index || demoData.game_info.excitement_index;

  // Get team colors from predictionData.team_selector if available
  const homeTeamColors = predictionData?.team_selector?.home_team;
  const awayTeamColors = predictionData?.team_selector?.away_team;

  return (
    <GlassCard className="p-3 sm:p-4 md:p-6">
      {/* Game Info Header */}
      <div className="text-center mb-4 sm:mb-6">
        <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-6 mb-3 text-xs sm:text-sm">
          {/* Date & Time */}
          <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground">
            <Calendar className="w-3 h-3 sm:w-4 sm:h-4" />
            <span className="whitespace-nowrap">{gameDate}</span>
          </div>
          <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground">
            <Clock className="w-3 h-3 sm:w-4 sm:h-4" />
            <span>{gameTime}</span>
          </div>
          
          {/* Network */}
          <div className="flex items-center gap-1.5 sm:gap-2 bg-blue-600/20 px-2 sm:px-3 py-0.5 sm:py-1 rounded-full border border-blue-500/30">
            <Tv className="w-3 h-3 sm:w-4 sm:h-4 text-blue-400" />
            <span className="text-blue-300 font-semibold">{network}</span>
          </div>
        </div>

        {/* Excitement Index */}
        <div className="flex items-center justify-center gap-2 mb-4">
          <span className="text-muted-foreground text-xs sm:text-sm">Excitement:</span>
          <div className="flex items-center gap-1">
            {[...Array(5)].map((_, i) => (
              <Star 
                key={i} 
                className="w-4 h-4 sm:w-5 sm:h-5 fill-current"
                style={{
                  color: i < Math.floor(excitementIndex) ? 'transparent' : '#6B7280',
                  background: i < Math.floor(excitementIndex) ? 'linear-gradient(45deg, #FFD700, #FFA500, #FF8C00, #DAA520, #B8860B, #CD853F, #FFD700)' : 'transparent',
                  WebkitBackgroundClip: i < Math.floor(excitementIndex) ? 'text' : 'initial',
                  WebkitTextFillColor: i < Math.floor(excitementIndex) ? 'transparent' : '#6B7280',
                  backgroundClip: i < Math.floor(excitementIndex) ? 'text' : 'initial'
                }}
              />
            ))}
            <span className="ml-1 sm:ml-2 text-xs sm:text-sm font-bold text-yellow-500">{excitementIndex.toFixed(1)}/5</span>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-0 items-center">
        {/* Away Team - Real Data */}
        <div className="text-center md:text-right flex flex-col items-center md:items-end md:pr-4">
          <div className="relative inline-block mb-2 sm:mb-3">
            <div 
              className="absolute inset-0 blur-2xl sm:blur-3xl rounded-full"
              style={{
                backgroundColor: awayTeamColors?.primary_color ? `${awayTeamColors.primary_color}33` : 'rgba(239, 68, 68, 0.2)'
              }}
            ></div>
            <ImageWithFallback
              src={awayLogo}
              alt={awayTeam}
              className="relative w-20 h-20 sm:w-32 sm:h-32 md:w-40 md:h-40 lg:w-56 lg:h-56 object-contain"
              style={{
                filter: `drop-shadow(0px 6px 16px ${awayTeamColors?.primary_color || 'rgba(239, 68, 68, 0.6)'}80) drop-shadow(0px 3px 8px rgba(0, 0, 0, 0.5)) drop-shadow(0px 1px 3px rgba(255, 255, 255, 0.2))`,
                transform: 'perspective(200px) rotateX(8deg) translateZ(10px)',
                transition: 'transform 0.3s ease'
              }}
            />
          </div>
          <div className="flex flex-wrap items-center gap-2 justify-center md:justify-end">
            <div className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-yellow-500/30 border border-yellow-600/40">
              <span className="text-yellow-700 font-bold text-sm sm:text-base lg:text-lg">Away</span>
            </div>
            <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white">
              {awayRank && `#${awayRank} `}{awayTeam}
            </h2>
          </div>
          <p className="text-gray-300 text-base sm:text-lg font-semibold">{awayRecord}</p>
        </div>

        {/* VS */}
        <div className="text-center flex-shrink-0 py-2 md:py-0">
          <div className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black bg-gradient-to-br from-yellow-400 via-amber-500 to-amber-300 bg-clip-text text-transparent">
            VS
          </div>
        </div>

        {/* Home Team - Real Data */}
        <div className="text-center md:text-left flex flex-col items-center md:items-start md:pl-4">
          <div className="relative inline-block mb-2 sm:mb-3">
            <div 
              className="absolute inset-0 blur-2xl sm:blur-3xl rounded-full"
              style={{
                backgroundColor: homeTeamColors?.primary_color ? `${homeTeamColors.primary_color}33` : 'rgba(249, 115, 22, 0.2)'
              }}
            ></div>
            <ImageWithFallback
              src={homeLogo}
              alt={homeTeam}
              className="relative w-20 h-20 sm:w-32 sm:h-32 md:w-40 md:h-40 lg:w-56 lg:h-56 object-contain"
              style={{
                filter: `drop-shadow(0px 6px 16px ${homeTeamColors?.primary_color || 'rgba(249, 115, 22, 0.6)'}80) drop-shadow(0px 3px 8px rgba(0, 0, 0, 0.5)) drop-shadow(0px 1px 3px rgba(255, 255, 255, 0.2))`,
                transform: 'perspective(200px) rotateX(8deg) translateZ(10px)',
                transition: 'transform 0.3s ease'
              }}
            />
          </div>
          <div className="flex flex-wrap items-center gap-2 justify-center md:justify-start">
            <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white">
              {homeRank && `#${homeRank} `}{homeTeam}
            </h2>
            <div className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-yellow-500/30 border border-yellow-600/40">
              <span className="text-yellow-700 font-bold text-sm sm:text-base lg:text-lg">Home</span>
            </div>
          </div>
          <p className="text-gray-300 text-base sm:text-lg font-semibold">{homeRecord}</p>
        </div>
      </div>
    </GlassCard>
  );
}
