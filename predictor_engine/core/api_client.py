"""
GraphQL API Client Module - Handles all College Football Data API interactions
Manages authentication, query execution, and data fetching
"""

import aiohttp
import asyncio
import json
from typing import Dict, Any, List, Optional


class GraphQLClient:
    """Handles GraphQL API interactions with College Football Data"""
    
    def __init__(self, api_key: str, current_year: int = 2025, current_week: int = 9):
        self.api_key = api_key
        self.base_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.current_year = current_year
        self.current_week = current_week
    
    async def execute_query(self, session: aiohttp.ClientSession, query: str, variables: Dict) -> Dict:
        """Execute GraphQL query"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "variables": variables
        }

        async with session.post(self.base_url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"GraphQL query failed: {response.status}")
            return await response.json()
    
    async def fetch_game_prediction_data(self, home_team_id: int, away_team_id: int) -> Dict[str, Any]:
        """Fetch comprehensive game prediction data"""
        
        query = """
        query GamePredictorEnhanced($homeTeamId: Int!, $awayTeamId: Int!, $currentYear: smallint = 2025, $currentWeek: smallint = 9) {
            # Current season team metrics (ENHANCED with all available fields)
            homeTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $homeTeamId}, year: {_eq: $currentYear}}) {
                epa epaAllowed explosiveness explosivenessAllowed success successAllowed
                passingEpa passingEpaAllowed rushingEpa rushingEpaAllowed
                passingDownsSuccess passingDownsSuccessAllowed
                standardDownsSuccess standardDownsSuccessAllowed
                lineYards lineYardsAllowed secondLevelYards secondLevelYardsAllowed
                openFieldYards openFieldYardsAllowed highlightYards highlightYardsAllowed
            }
            awayTeamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $awayTeamId}, year: {_eq: $currentYear}}) {
                epa epaAllowed explosiveness explosivenessAllowed success successAllowed
                passingEpa passingEpaAllowed rushingEpa rushingEpaAllowed
                passingDownsSuccess passingDownsSuccessAllowed
                standardDownsSuccess standardDownsSuccessAllowed
                lineYards lineYardsAllowed secondLevelYards secondLevelYardsAllowed
                openFieldYards openFieldYardsAllowed highlightYards highlightYardsAllowed
            }
            
            # KEY PLAYER METRICS - Individual Player Analysis (Simplified)
            allPlayers: adjustedPlayerMetrics(
                where: {
                    year: {_eq: $currentYear}
                },
                orderBy: {metricValue: DESC},
                limit: 100
            ) {
                athleteId
                metricType
                metricValue
                plays
                athlete {
                    name
                }
            }
            
            # Team talent ratings
            homeTeamTalent: teamTalent(where: {team: {teamId: {_eq: $homeTeamId}}, year: {_eq: $currentYear}}) {
                talent
            }
            awayTeamTalent: teamTalent(where: {team: {teamId: {_eq: $awayTeamId}}, year: {_eq: $currentYear}}) {
                talent
            }
            
            # All season games for comprehensive analysis
            homeSeasonGames: game(where: {_or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}], season: {_eq: $currentYear}}, orderBy: {week: ASC}) {
                id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
            }
            awaySeasonGames: game(where: {_or: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $awayTeamId}}], season: {_eq: $currentYear}}, orderBy: {week: ASC}) {
                id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
            }
            
            # Recent games (last 4) for immediate form
            homeRecentGames: game(where: {_or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}], season: {_eq: $currentYear}}, orderBy: {startDate: DESC}, limit: 4) {
                id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
            }
            awayRecentGames: game(where: {_or: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $awayTeamId}}], season: {_eq: $currentYear}}, orderBy: {startDate: DESC}, limit: 4) {
                id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
            }
            
            # Team information
            homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}}) {
                school conference
            }
            awayTeam: currentTeams(where: {teamId: {_eq: $awayTeamId}}) {
                school conference
            }
            
            # Composite ratings for validation
            homeRatings: ratings(where: {
                teamId: {_eq: $homeTeamId}, 
                year: {_eq: $currentYear}
            }, limit: 1) {
                overallRating offenseRating defenseRating specialTeamsRating
            }
            awayRatings: ratings(where: {
                teamId: {_eq: $awayTeamId}, 
                year: {_eq: $currentYear}
            }, limit: 1) {
                overallRating offenseRating defenseRating specialTeamsRating
            }
            
            # Current matchup to get game ID for betting lines
            currentMatchup: game(where: {
                homeTeamId: {_eq: $homeTeamId},
                awayTeamId: {_eq: $awayTeamId},
                season: {_eq: $currentYear},
                week: {_eq: $currentWeek}
            }) {
                id startDate venue {
                    name city state
                }
                weather {
                    temperature windSpeed precipitation
                }
            }
            
            # AP Poll rankings for context
            homeApPoll: poll(where: {
                teamId: {_eq: $homeTeamId},
                year: {_eq: $currentYear},
                poll: {_eq: "AP Top 25"}
            }, orderBy: {week: DESC}, limit: 1) {
                rank points firstPlaceVotes
            }
            awayApPoll: poll(where: {
                teamId: {_eq: $awayTeamId},
                year: {_eq: $currentYear},
                poll: {_eq: "AP Top 25"}
            }, orderBy: {week: DESC}, limit: 1) {
                rank points firstPlaceVotes
            }
            
            # Recruiting rankings for talent assessment
            homeRecruiting: teamRecruitingRankings(where: {
                teamId: {_eq: $homeTeamId}
            }, orderBy: {year: DESC}, limit: 3) {
                year rank averageRating totalCommits
            }
            awayRecruiting: teamRecruitingRankings(where: {
                teamId: {_eq: $awayTeamId}
            }, orderBy: {year: DESC}, limit: 3) {
                year rank averageRating totalCommits
            }
            
            # Transfer portal data for roster changes
            homeTransfers: portal(where: {
                teamId: {_eq: $homeTeamId}
            }, orderBy: {transferDate: DESC}, limit: 10) {
                athleteId season rating stars position
            }
            awayTransfers: portal(where: {
                teamId: {_eq: $awayTeamId}
            }, orderBy: {transferDate: DESC}, limit: 10) {
                athleteId season rating stars position
            }
        }
        """

        async with aiohttp.ClientSession() as session:
            result = await self.execute_query(session, query, {
                "homeTeamId": home_team_id,
                "awayTeamId": away_team_id,
                "currentYear": self.current_year,
                "currentWeek": self.current_week
            })

            # Check for errors
            if 'data' not in result:
                if 'errors' in result:
                    raise Exception(f"GraphQL errors: {result['errors']}")
                else:
                    raise Exception(f"Unexpected response structure: {result}")
            
            # Try to get gameId for additional data
            current_matchup = result['data'].get('currentMatchup', [])
            if current_matchup:
                game_id = current_matchup[0].get('id')
                if game_id:
                    print(f"🎯 Found gameId: {game_id} - Fetching market lines...")
                    game_lines = await self.fetch_game_lines(session, game_id)
                    result['data']['marketLines'] = game_lines
                    
                    print(f"🎯 Fetching game media information...")
                    game_media = await self.fetch_game_media(session, game_id)
                    result['data']['gameMedia'] = game_media
                else:
                    print("⚠️ No gameId found in current matchup")
            else:
                print("⚠️ No current matchup found")

            return result['data']
    
    async def fetch_game_lines(self, session: aiohttp.ClientSession, game_id: int) -> List[Dict]:
        """Fetch betting lines for a specific game"""
        lines_query = """
        query GameLines($gameId: Int!) {
            gameLines(where: {gameId: {_eq: $gameId}}) {
                gameId
                spread
                spreadOpen
                overUnder
                overUnderOpen
                moneylineHome
                moneylineAway
                provider {
                    name
                }
            }
        }
        """
        
        try:
            result = await self.execute_query(session, lines_query, {"gameId": game_id})
            return result.get('data', {}).get('gameLines', [])
        except Exception as e:
            print(f"⚠️ Failed to fetch game lines: {e}")
            return []

    async def fetch_game_media(self, session: aiohttp.ClientSession, game_id: int) -> List[Dict]:
        """Fetch media information for a specific game"""
        media_query = """
        query GameMedia($gameId: Int!) {
            game(where: {id: {_eq: $gameId}}) {
                id
                homeTeam
                awayTeam
                startDate
                mediaInfo {
                    mediaType
                    name
                }
            }
        }
        """
        
        try:
            result = await self.execute_query(session, media_query, {"gameId": game_id})
            games = result.get('data', {}).get('game', [])
            if games:
                return games[0].get('mediaInfo', [])
            return []
        except Exception as e:
            print(f"⚠️ Failed to fetch game media: {e}")
            return []
    
    async def fetch_player_stats(self, team_id: int, position: str = None) -> List[Dict]:
        """Fetch player statistics for a team"""
        where_clause = f"teamId: {{_eq: {team_id}}}, year: {{_eq: {self.current_year}}}"
        if position:
            where_clause += f", position: {{_eq: \"{position}\"}}"
        
        player_query = f"""
        query TeamPlayers {{
            adjustedPlayerMetrics(where: {{{where_clause}}}, orderBy: {{metricValue: DESC}}, limit: 50) {{
                athleteId
                metricType
                metricValue
                plays
                athlete {{
                    name
                    position
                }}
            }}
        }}
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.execute_query(session, player_query, {})
                return result.get('data', {}).get('adjustedPlayerMetrics', [])
        except Exception as e:
            print(f"⚠️ Failed to fetch player stats: {e}")
            return []
    
    async def fetch_team_stats(self, team_id: int) -> Dict[str, Any]:
        """Fetch comprehensive team statistics"""
        stats_query = """
        query TeamStats($teamId: Int!, $currentYear: smallint!) {
            teamMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $teamId}, year: {_eq: $currentYear}}) {
                epa epaAllowed explosiveness explosivenessAllowed success successAllowed
                passingEpa passingEpaAllowed rushingEpa rushingEpaAllowed
                passingDownsSuccess passingDownsSuccessAllowed
                standardDownsSuccess standardDownsSuccessAllowed
                lineYards lineYardsAllowed secondLevelYards secondLevelYardsAllowed
                openFieldYards openFieldYardsAllowed highlightYards highlightYardsAllowed
            }
            
            seasonGames: game(where: {_or: [{homeTeamId: {_eq: $teamId}}, {awayTeamId: {_eq: $teamId}}], season: {_eq: $currentYear}}, orderBy: {week: ASC}) {
                id homePoints awayPoints homeTeam awayTeam homeTeamId awayTeamId homePostgameWinProb awayPostgameWinProb homeStartElo awayStartElo week seasonType
            }
            
            teamInfo: currentTeams(where: {teamId: {_eq: $teamId}}) {
                school conference division
            }
            
            talent: teamTalent(where: {team: {teamId: {_eq: $teamId}}, year: {_eq: $currentYear}}) {
                talent
            }
        }
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.execute_query(session, stats_query, {
                    "teamId": team_id,
                    "currentYear": self.current_year
                })
                return result.get('data', {})
        except Exception as e:
            print(f"⚠️ Failed to fetch team stats: {e}")
            return {}
    
    async def fetch_coaching_data(self, team_id: int) -> Dict[str, Any]:
        """Fetch coaching statistics and records"""
        coaching_query = """
        query CoachingData($teamId: Int!, $currentYear: smallint!) {
            coachingRecords: coachingRecord(where: {
                teamId: {_eq: $teamId},
                year: {_eq: $currentYear}
            }) {
                wins losses ties
                coach {
                    name
                }
            }
            
            historicalRecords: coachingRecord(where: {
                teamId: {_eq: $teamId}
            }, orderBy: {year: DESC}, limit: 5) {
                year wins losses ties
                coach {
                    name
                }
            }
        }
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.execute_query(session, coaching_query, {
                    "teamId": team_id,
                    "currentYear": self.current_year
                })
                return result.get('data', {})
        except Exception as e:
            print(f"⚠️ Failed to fetch coaching data: {e}")
            return {}
    
    async def fetch_conference_standings(self, conference: str) -> List[Dict]:
        """Fetch conference standings"""
        standings_query = """
        query ConferenceStandings($conference: String!, $currentYear: smallint!) {
            conferenceStandings: currentTeams(where: {conference: {_eq: $conference}}) {
                school
                teamId
            }
        }
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.execute_query(session, standings_query, {
                    "conference": conference,
                    "currentYear": self.current_year
                })
                return result.get('data', {}).get('conferenceStandings', [])
        except Exception as e:
            print(f"⚠️ Failed to fetch conference standings: {e}")
            return []
    
    async def fetch_weather_data(self, game_id: int) -> Dict[str, Any]:
        """Fetch weather data for a specific game"""
        weather_query = """
        query GameWeather($gameId: Int!) {
            game(where: {id: {_eq: $gameId}}) {
                weather {
                    temperature
                    windSpeed
                    windDirection
                    precipitation
                    humidity
                    visibility
                }
                venue {
                    name
                    city
                    state
                    elevation
                    capacity
                    grass
                    dome
                }
            }
        }
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.execute_query(session, weather_query, {"gameId": game_id})
                games = result.get('data', {}).get('game', [])
                if games:
                    return {
                        'weather': games[0].get('weather', {}),
                        'venue': games[0].get('venue', {})
                    }
                return {}
        except Exception as e:
            print(f"⚠️ Failed to fetch weather data: {e}")
            return {}
    
    def set_current_week(self, week: int):
        """Update the current week for queries"""
        self.current_week = week
    
    def set_current_year(self, year: int):
        """Update the current year for queries"""
        self.current_year = year