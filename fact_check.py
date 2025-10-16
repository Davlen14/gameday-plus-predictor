#!/usr/bin/env python3
"""
Fact-check script to verify Ole Miss vs Washington State data accuracy
"""

import asyncio
from graphqlpredictor import LightningPredictor

async def fact_check():
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    predictor = LightningPredictor(api_key)
    
    print("=" * 80)
    print("🔍 FACT-CHECKING OLE MISS VS WASHINGTON STATE DATA")
    print("=" * 80)
    
    # Let's verify the raw data
    import aiohttp
    
    query = """
    query FactCheck($homeTeamId: Int!, $awayTeamId: Int!, $currentYear: smallint = 2025) {
        # Team Info
        homeTeam: currentTeams(where: {teamId: {_eq: $homeTeamId}}) {
            school conference teamId
        }
        awayTeam: currentTeams(where: {teamId: {_eq: $awayTeamId}}) {
            school conference teamId
        }
        
        # Season Records
        homeGames: game(where: {
            _or: [{homeTeamId: {_eq: $homeTeamId}}, {awayTeamId: {_eq: $homeTeamId}}],
            season: {_eq: $currentYear}
        }, orderBy: {week: ASC}) {
            week homeTeam awayTeam homePoints awayPoints homeTeamId awayTeamId
        }
        
        awayGames: game(where: {
            _or: [{homeTeamId: {_eq: $awayTeamId}}, {awayTeamId: {_eq: $awayTeamId}}],
            season: {_eq: $currentYear}
        }, orderBy: {week: ASC}) {
            week homeTeam awayTeam homePoints awayPoints homeTeamId awayTeamId
        }
        
        # Ratings
        homeRatings: ratings(where: {teamId: {_eq: $homeTeamId}, year: {_eq: $currentYear}}) {
            elo fpi
        }
        awayRatings: ratings(where: {teamId: {_eq: $awayTeamId}, year: {_eq: $currentYear}}) {
            elo fpi
        }
        
        # Advanced Metrics
        homeMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $homeTeamId}, year: {_eq: $currentYear}}) {
            epa epaAllowed success successAllowed
        }
        awayMetrics: adjustedTeamMetrics(where: {teamId: {_eq: $awayTeamId}, year: {_eq: $currentYear}}) {
            epa epaAllowed success successAllowed
        }
        
        # Talent
        homeTalent: teamTalent(where: {team: {teamId: {_eq: $homeTeamId}}, year: {_eq: $currentYear}}) {
            talent
        }
        awayTalent: teamTalent(where: {team: {teamId: {_eq: $awayTeamId}}, year: {_eq: $currentYear}}) {
            talent
        }
        
        # Market Lines for this specific game
        marketLines: gameLines(where: {
            gameId: {_eq: 401752733}
        }) {
            spread spreadOpen overUnder provider { name }
        }
    }
    """
    
    async with aiohttp.ClientSession() as session:
        result = await predictor._execute_query(session, query, {
            "homeTeamId": 145,  # Ole Miss
            "awayTeamId": 265,  # Washington State
            "currentYear": 2025
        })
    
    data = result.get('data', {})
    
    print("\n✅ VERIFIED DATA:")
    print("=" * 80)
    
    # Teams
    home = data['homeTeam'][0] if data.get('homeTeam') else {}
    away = data['awayTeam'][0] if data.get('awayTeam') else {}
    print(f"\n🏈 TEAMS:")
    print(f"   Home: {home.get('school')} (ID: {home.get('teamId')})")
    print(f"   Away: {away.get('school')} (ID: {away.get('teamId')})")
    
    # Records
    print(f"\n📊 SEASON RECORDS:")
    home_wins = 0
    home_losses = 0
    for game in data.get('homeGames', []):
        if game.get('homePoints') is not None and game.get('awayPoints') is not None:
            if game['homeTeamId'] == 145:
                if game['homePoints'] > game['awayPoints']:
                    home_wins += 1
                else:
                    home_losses += 1
            else:
                if game['awayPoints'] > game['homePoints']:
                    home_wins += 1
                else:
                    home_losses += 1
    
    away_wins = 0
    away_losses = 0
    for game in data.get('awayGames', []):
        if game.get('homePoints') is not None and game.get('awayPoints') is not None:
            if game['homeTeamId'] == 265:
                if game['homePoints'] > game['awayPoints']:
                    away_wins += 1
                else:
                    away_losses += 1
            else:
                if game['awayPoints'] > game['homePoints']:
                    away_wins += 1
                else:
                    away_losses += 1
    
    print(f"   Ole Miss: {home_wins}-{home_losses}")
    print(f"   Washington State: {away_wins}-{away_losses}")
    
    # Ratings
    home_ratings = data['homeRatings'][0] if data.get('homeRatings') else {}
    away_ratings = data['awayRatings'][0] if data.get('awayRatings') else {}
    print(f"\n⚡ RATINGS:")
    print(f"   Ole Miss ELO: {home_ratings.get('elo', 'N/A')}")
    print(f"   Washington State ELO: {away_ratings.get('elo', 'N/A')}")
    print(f"   Ole Miss FPI: {home_ratings.get('fpi', 'N/A')}")
    print(f"   Washington State FPI: {away_ratings.get('fpi', 'N/A')}")
    
    # Advanced Metrics
    home_metrics = data['homeMetrics'][0] if data.get('homeMetrics') else {}
    away_metrics = data['awayMetrics'][0] if data.get('awayMetrics') else {}
    print(f"\n📈 ADVANCED METRICS:")
    print(f"   Ole Miss EPA: {home_metrics.get('epa', 'N/A')}")
    print(f"   Washington State EPA: {away_metrics.get('epa', 'N/A')}")
    print(f"   Ole Miss Success Rate: {home_metrics.get('success', 'N/A')}")
    print(f"   Washington State Success Rate: {away_metrics.get('success', 'N/A')}")
    
    # Talent
    home_talent = data['homeTalent'][0] if data.get('homeTalent') else {}
    away_talent = data['awayTalent'][0] if data.get('awayTalent') else {}
    print(f"\n🌟 TALENT:")
    print(f"   Ole Miss: {home_talent.get('talent', 'N/A')}")
    print(f"   Washington State: {away_talent.get('talent', 'N/A')}")
    
    # Market Lines
    print(f"\n💰 MARKET LINES:")
    for line in data.get('marketLines', []):
        provider = line.get('provider', {}).get('name', 'Unknown')
        spread = line.get('spread')
        total = line.get('overUnder')
        print(f"   {provider}: Spread {spread}, Total {total}")
    
    # Analysis
    print("\n" + "=" * 80)
    print("🔍 ANALYSIS:")
    print("=" * 80)
    
    elo_diff = home_ratings.get('elo', 0) - away_ratings.get('elo', 0)
    fpi_diff = home_ratings.get('fpi', 0) - away_ratings.get('fpi', 0)
    talent_diff = home_talent.get('talent', 0) - away_talent.get('talent', 0)
    
    print(f"\n📊 DIFFERENTIALS:")
    print(f"   ELO: {elo_diff:+.0f} (Ole Miss {'advantage' if elo_diff > 0 else 'disadvantage'})")
    print(f"   FPI: {fpi_diff:+.2f} (Ole Miss {'advantage' if fpi_diff > 0 else 'disadvantage'})")
    print(f"   Talent: {talent_diff:+.2f} (Ole Miss {'advantage' if talent_diff > 0 else 'disadvantage'})")
    
    # Expected spread based on ELO
    # ELO difference of ~600 points = ~17 point spread typically
    expected_spread_from_elo = (elo_diff / 25) + 2.5  # Home field advantage
    print(f"\n🎯 EXPECTED SPREAD FROM ELO: Ole Miss -{expected_spread_from_elo:.1f}")
    print(f"   Market Line: Ole Miss -32.5")
    print(f"   Model Prediction: Ole Miss -2.6")
    
    print(f"\n⚠️  INVESTIGATION:")
    if expected_spread_from_elo > 20:
        print(f"   ✅ ELO suggests large spread ({expected_spread_from_elo:.1f}) - market may be correct")
        print(f"   ❌ Model prediction (-2.6) seems VERY low")
        print(f"\n   POSSIBLE MODEL ISSUES:")
        print(f"   1. Spread scaling may be too conservative")
        print(f"   2. Market consensus weight (20%) not pulling hard enough")
        print(f"   3. Differential calculation may need adjustment")
    
    return data

if __name__ == "__main__":
    asyncio.run(fact_check())
