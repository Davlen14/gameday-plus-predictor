#!/usr/bin/env python3
"""
Schema Explorer for College Football Data GraphQL API
This script explores the actual schema to find the correct field names for composite rankings
"""

import asyncio
import aiohttp
import json
from typing import Dict, List

class SchemaExplorer:
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

    async def explore_ratings_schema(self):
        """Explore the ratings/composite rankings schema"""
        print("🔍 EXPLORING COMPOSITE RANKINGS SCHEMA")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            
            # 1. Find all rating-related query fields
            print("\n1️⃣ Finding all rating-related query fields...")
            schema_query = """
            query {
                __schema {
                    queryType {
                        fields {
                            name
                            description
                        }
                    }
                }
            }
            """
            
            result = await self._execute_query(session, schema_query)
            rating_fields = []
            
            for field in result['data']['__schema']['queryType']['fields']:
                name = field['name'].lower()
                if any(keyword in name for keyword in ['rating', 'rank', 'elo', 'fpi', 'sp']):
                    rating_fields.append(field)
                    print(f"   📊 {field['name']}: {field.get('description', 'No description')}")
            
            # 2. Explore each rating-related field in detail
            for field in rating_fields:
                await self._explore_field_schema(session, field['name'])
            
            # 3. Test actual data queries for promising fields
            await self._test_data_queries(session, rating_fields)

    async def _explore_field_schema(self, session: aiohttp.ClientSession, field_name: str):
        """Explore the schema of a specific field"""
        print(f"\n2️⃣ Exploring {field_name} schema...")
        
        # Get the return type of the field
        type_query = f"""
        query {{
            __type(name: "{field_name.title()}") {{
                fields {{
                    name
                    type {{
                        name
                        kind
                    }}
                    description
                }}
            }}
        }}
        """
        
        try:
            result = await self._execute_query(session, type_query)
            if result['data']['__type']:
                print(f"   📋 Fields available in {field_name}:")
                for field in result['data']['__type']['fields'] or []:
                    type_name = field['type']['name'] if field['type'] else 'Unknown'
                    print(f"      • {field['name']}: {type_name}")
            else:
                print(f"   ❌ Could not find type schema for {field_name}")
        except Exception as e:
            print(f"   ⚠️ Error exploring {field_name}: {e}")

        # Also try the filter/input type
        filter_type_query = f"""
        query {{
            __type(name: "{field_name.title()}BoolExp") {{
                inputFields {{
                    name
                    type {{
                        name
                        kind
                    }}
                }}
            }}
        }}
        """
        
        try:
            result = await self._execute_query(session, filter_type_query)
            if result['data']['__type']:
                print(f"   🔍 Filter fields for {field_name}:")
                for field in result['data']['__type']['inputFields'] or []:
                    if not field['name'].startswith('_'):  # Skip GraphQL meta fields
                        type_name = field['type']['name'] if field['type'] else 'Unknown'
                        print(f"      • {field['name']}: {type_name}")
        except Exception as e:
            print(f"   ⚠️ Error exploring {field_name} filters: {e}")

    async def _test_data_queries(self, session: aiohttp.ClientSession, rating_fields: List[Dict]):
        """Test actual data queries to see what works"""
        print(f"\n3️⃣ Testing actual data queries...")
        
        for field in rating_fields:
            field_name = field['name']
            print(f"\n   🧪 Testing {field_name}...")
            
            # Try a simple query with common field names
            common_fields = ['year', 'teamId', 'team', 'rating', 'value', 'rank', 'elo', 'fpi', 'sp']
            
            for test_fields in [['year'], ['teamId'], ['team'], ['rating'], ['year', 'teamId'], ['year', 'team']]:
                test_query = f"""
                query {{
                    {field_name}(limit: 1) {{
                        {' '.join(test_fields)}
                    }}
                }}
                """
                
                try:
                    result = await self._execute_query(session, test_query)
                    if 'errors' not in result:
                        print(f"      ✅ Working fields: {test_fields}")
                        if result['data'][field_name]:
                            print(f"         Sample data: {result['data'][field_name][0]}")
                        break
                except Exception as e:
                    continue
            else:
                print(f"      ❌ Could not find working field combination for {field_name}")

    async def explore_specific_ratings_tables(self):
        """Explore specific known ratings tables"""
        print("\n4️⃣ EXPLORING SPECIFIC RATINGS TABLES")
        print("=" * 60)
        
        # Known possible table names from college football data
        possible_tables = [
            'ratings',
            'teamRatings', 
            'weeklyRatings',
            'systemRatings',
            'compositeRatings',
            'eloRatings',
            'fpiRatings',
            'spRatings'
        ]
        
        async with aiohttp.ClientSession() as session:
            for table in possible_tables:
                await self._test_table_exists(session, table)

    async def _test_table_exists(self, session: aiohttp.ClientSession, table_name: str):
        """Test if a table exists and what fields it has"""
        print(f"\n   🔍 Testing {table_name}...")
        
        # Test if table exists with minimal query
        test_query = f"""
        query {{
            {table_name}(limit: 1) {{
                __typename
            }}
        }}
        """
        
        try:
            result = await self._execute_query(session, test_query)
            if 'errors' not in result:
                print(f"      ✅ {table_name} exists!")
                
                # Now explore its schema
                await self._explore_field_schema(session, table_name)
                
                # Try to get actual data
                await self._sample_table_data(session, table_name)
            else:
                print(f"      ❌ {table_name} does not exist")
        except Exception as e:
            print(f"      ❌ {table_name} error: {e}")

    async def _sample_table_data(self, session: aiohttp.ClientSession, table_name: str):
        """Get sample data from a table to understand its structure"""
        print(f"   📊 Getting sample data from {table_name}...")
        
        # Try different field combinations to see what works
        field_combinations = [
            ['year', 'week', 'teamId'],
            ['year', 'teamId', 'rating'],
            ['season', 'team', 'value'],
            ['year', 'week', 'team'],
            ['teamId', 'year', 'elo'],
            ['teamId', 'year', 'fpi'],
            ['teamId', 'year', 'sp']
        ]
        
        for fields in field_combinations:
            test_query = f"""
            query {{
                {table_name}(limit: 2) {{
                    {' '.join(fields)}
                }}
            }}
            """
            
            try:
                result = await self._execute_query(session, test_query)
                if 'errors' not in result and result['data'][table_name]:
                    print(f"      ✅ Working fields: {fields}")
                    for i, row in enumerate(result['data'][table_name][:2]):
                        print(f"         Row {i+1}: {row}")
                    return  # Found working combination, stop testing
            except Exception as e:
                continue
        
        print(f"      ❌ Could not find working field combination for {table_name}")

    async def explore_all_types(self):
        """Get all types in the schema to find rating-related ones"""
        print("\n5️⃣ EXPLORING ALL SCHEMA TYPES")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            schema_query = """
            query {
                __schema {
                    types {
                        name
                        kind
                        description
                    }
                }
            }
            """
            
            result = await self._execute_query(session, schema_query)
            
            rating_types = []
            for type_info in result['data']['__schema']['types']:
                name = type_info['name'].lower()
                if any(keyword in name for keyword in ['rating', 'rank', 'elo', 'fpi', 'sp', 'poll']):
                    if not name.startswith('__'):  # Skip GraphQL internal types
                        rating_types.append(type_info)
            
            print(f"   📋 Found {len(rating_types)} rating-related types:")
            for type_info in rating_types:
                print(f"      • {type_info['name']} ({type_info['kind']}): {type_info.get('description', 'No description')}")
            
            return rating_types

async def main():
    # API Key for College Football Data
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    
    explorer = SchemaExplorer(api_key)
    
    try:
        print("🚀 Starting Schema Exploration for Composite Rankings")
        print("=" * 80)
        
        # Step 1: Explore ratings schema
        await explorer.explore_ratings_schema()
        
        # Step 2: Test specific known table names
        await explorer.explore_specific_ratings_tables()
        
        # Step 3: Get all types to see what we might have missed
        rating_types = await explorer.explore_all_types()
        
        print("\n" + "=" * 80)
        print("✅ SCHEMA EXPLORATION COMPLETE")
        print("=" * 80)
        print("Check the output above to find the correct field names for composite rankings!")
        
    except Exception as e:
        print(f"❌ Error during exploration: {e}")

if __name__ == "__main__":
    asyncio.run(main())