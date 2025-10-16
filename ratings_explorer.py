#!/usr/bin/env python3
"""
Focused exploration of discovered ratings tables
"""

import asyncio
import aiohttp
import json
from typing import Dict

class RatingsDetailExplorer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://graphql.collegefootballdata.com/v1/graphql"

    async def _execute_query(self, session: aiohttp.ClientSession, query: str, variables: Dict = None) -> Dict:
        """Execute GraphQL query"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "variables": variables or {}
        }

        async with session.post(self.base_url, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"GraphQL query failed: {response.status}")
            return await response.json()

    async def explore_ratings_table(self):
        """Deep dive into the ratings table"""
        print("🔍 DEEP DIVE: RATINGS TABLE")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            
            # Test all possible field combinations
            possible_fields = [
                'teamId', 'year', 'week', 'season', 'elo', 'rating', 'value', 'rank',
                'fpi', 'sp', 'spPlus', 'sagarin', 'bcs', 'ap', 'coaches', 'playoff',
                'system', 'systemName', 'ratingSystem', 'offensiveRating', 'defensiveRating',
                'overallRating', 'conference', 'team', 'school'
            ]
            
            print("   🧪 Testing individual fields...")
            working_fields = []
            
            for field in possible_fields:
                test_query = f"""
                query {{
                    ratings(limit: 1) {{
                        {field}
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, test_query)
                    if 'errors' not in result:
                        working_fields.append(field)
                        print(f"      ✅ {field}")
                    else:
                        print(f"      ❌ {field}")
                except Exception as e:
                    print(f"      ❌ {field} (error: {e})")
            
            print(f"\n   📋 Working fields found: {working_fields}")
            
            # Get sample data with all working fields
            if working_fields:
                print(f"\n   📊 Sample data with working fields:")
                sample_query = f"""
                query {{
                    ratings(limit: 5, where: {{year: {{_eq: 2025}}}}) {{
                        {' '.join(working_fields)}
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, sample_query)
                    if 'errors' not in result and result['data']['ratings']:
                        for i, row in enumerate(result['data']['ratings']):
                            print(f"      Row {i+1}: {row}")
                    else:
                        print("      No 2025 data found, trying without year filter...")
                        
                        # Try without year filter
                        sample_query = f"""
                        query {{
                            ratings(limit: 5) {{
                                {' '.join(working_fields)}
                            }}
                        }}
                        """
                        
                        result = await self._execute_query(session, sample_query)
                        if 'errors' not in result:
                            for i, row in enumerate(result['data']['ratings']):
                                print(f"      Row {i+1}: {row}")
                except Exception as e:
                    print(f"      Error getting sample data: {e}")

    async def explore_poll_tables(self):
        """Explore poll-related tables"""
        print("\n🔍 DEEP DIVE: POLL TABLES")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            
            # Test pollRank table
            print("   🧪 Testing pollRank table...")
            poll_fields = [
                'teamId', 'year', 'week', 'season', 'rank', 'school', 'team',
                'conference', 'poll', 'pollType', 'firstPlaceVotes', 'points'
            ]
            
            working_poll_fields = []
            
            for field in poll_fields:
                test_query = f"""
                query {{
                    pollRank(limit: 1) {{
                        {field}
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, test_query)
                    if 'errors' not in result:
                        working_poll_fields.append(field)
                        print(f"      ✅ {field}")
                    else:
                        print(f"      ❌ {field}")
                except Exception as e:
                    print(f"      ❌ {field} (error: {e})")
            
            # Get sample poll data
            if working_poll_fields:
                print(f"\n   📊 Sample pollRank data:")
                sample_query = f"""
                query {{
                    pollRank(limit: 5, where: {{year: {{_eq: 2025}}}}) {{
                        {' '.join(working_poll_fields)}
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, sample_query)
                    if 'errors' not in result and result['data']['pollRank']:
                        for i, row in enumerate(result['data']['pollRank']):
                            print(f"      Row {i+1}: {row}")
                except Exception as e:
                    print(f"      Error getting poll data: {e}")

    async def find_ohio_state_illinois_data(self):
        """Find specific data for Ohio State (194) and Illinois (356)"""
        print("\n🎯 FINDING OHIO STATE & ILLINOIS DATA")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            
            # Ohio State = 194, Illinois = 356
            team_ids = {'Ohio State': 194, 'Illinois': 356}
            
            for team_name, team_id in team_ids.items():
                print(f"\n   🏈 {team_name} (ID: {team_id}):")
                
                # Test ratings data
                ratings_query = f"""
                query {{
                    ratings(where: {{teamId: {{_eq: {team_id}}}, year: {{_eq: 2025}}}}) {{
                        teamId year elo
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, ratings_query)
                    if 'errors' not in result and result['data']['ratings']:
                        print(f"      📊 Ratings data: {result['data']['ratings']}")
                    else:
                        print(f"      ❌ No ratings data found for 2025")
                except Exception as e:
                    print(f"      ❌ Error getting ratings: {e}")
                
                # Test poll data
                poll_query = f"""
                query {{
                    pollRank(where: {{teamId: {{_eq: {team_id}}}, year: {{_eq: 2025}}}}) {{
                        teamId year week rank
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, poll_query)
                    if 'errors' not in result and result['data']['pollRank']:
                        print(f"      🏆 Poll data: {result['data']['pollRank'][:3]}")  # Show first 3
                    else:
                        print(f"      ❌ No poll data found for 2025")
                except Exception as e:
                    print(f"      ❌ Error getting polls: {e}")

    async def test_ratings_systems(self):
        """Test different rating systems that might be available"""
        print("\n🔍 TESTING DIFFERENT RATING SYSTEMS")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            
            # Check if there are different rating systems
            systems_query = """
            query {
                ratings(limit: 10, orderBy: {year: DESC}) {
                    teamId year elo
                }
            }
            """
            
            try:
                result = await self._execute_query(session, systems_query)
                if 'errors' not in result:
                    print("   📊 Recent ratings data:")
                    for row in result['data']['ratings']:
                        print(f"      {row}")
                        
                    # Check if there are any other rating fields by testing common ones
                    test_fields = ['fpi', 'sp', 'spPlus', 'sagarin', 'bcs', 'massey', 'colley', 'computer']
                    
                    print(f"\n   🧪 Testing additional rating fields:")
                    for field in test_fields:
                        test_query = f"""
                        query {{
                            ratings(limit: 1) {{
                                teamId year elo {field}
                            }}
                        }}
                        """
                        
                        try:
                            test_result = await self._execute_query(session, test_query)
                            if 'errors' not in test_result:
                                print(f"      ✅ {field} field exists!")
                            else:
                                print(f"      ❌ {field} field does not exist")
                        except:
                            print(f"      ❌ {field} field does not exist")
                            
            except Exception as e:
                print(f"   ❌ Error testing rating systems: {e}")

async def main():
    # API Key
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    explorer = RatingsDetailExplorer(api_key)
    
    try:
        print("🚀 DETAILED EXPLORATION OF COMPOSITE RANKINGS")
        print("=" * 80)
        
        # Deep dive into ratings table
        await explorer.explore_ratings_table()
        
        # Explore poll tables
        await explorer.explore_poll_tables()
        
        # Test different rating systems
        await explorer.test_ratings_systems()
        
        # Find specific team data
        await explorer.find_ohio_state_illinois_data()
        
        print("\n" + "=" * 80)
        print("✅ DETAILED EXPLORATION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error during exploration: {e}")

if __name__ == "__main__":
    asyncio.run(main())