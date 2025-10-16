#!/usr/bin/env python3
"""
Quick schema field discovery tool for College Football Data GraphQL API
Discovers the correct relationship field names for athlete and gamePlayerStat
"""

import asyncio
import aiohttp
import json

API_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

async def introspect_type(type_name: str):
    """Introspect a specific type to see its fields"""
    
    query = """
    query IntrospectType($typeName: String!) {
      __type(name: $typeName) {
        name
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_URL,
            json={"query": query, "variables": {"typeName": type_name}},
            headers=headers
        ) as response:
            return await response.json()

async def main():
    print("🔍 Discovering Schema Fields for athlete and gamePlayerStat\n")
    print("="*80)
    
    # 1. Check Athlete type fields
    print("\n🏈 ATHLETE TYPE FIELDS:")
    print("-"*80)
    athlete_result = await introspect_type("Athlete")
    
    if "data" in athlete_result and athlete_result["data"]["__type"]:
        fields = athlete_result["data"]["__type"]["fields"]
        print(f"\nTotal fields: {len(fields)}\n")
        
        # Look for relationship fields (arrays or objects)
        print("📊 All Fields:")
        for field in sorted(fields, key=lambda x: x["name"]):
            field_name = field["name"]
            field_type = field["type"]
            type_kind = field_type.get("kind", "")
            type_name = field_type.get("name", "")
            
            # Check if it's a list or object type
            if type_kind in ["LIST", "OBJECT"]:
                of_type = field_type.get("ofType")
                of_type_name = of_type.get("name", "") if of_type else ""
                print(f"  • {field_name}: {type_kind} of {of_type_name or type_name}")
            else:
                print(f"  • {field_name}: {type_name}")
    
    # 2. Check GamePlayerStat type fields
    print("\n\n🏈 GAME_PLAYER_STAT TYPE FIELDS:")
    print("-"*80)
    stat_result = await introspect_type("GamePlayerStat")
    
    if "data" in stat_result and stat_result["data"]["__type"]:
        fields = stat_result["data"]["__type"]["fields"]
        print(f"\nTotal fields: {len(fields)}\n")
        
        print("📊 All Fields:")
        for field in sorted(fields, key=lambda x: x["name"]):
            field_name = field["name"]
            field_type = field["type"]
            type_kind = field_type.get("kind", "")
            type_name = field_type.get("name", "")
            
            if type_kind in ["LIST", "OBJECT"]:
                of_type = field_type.get("ofType")
                of_type_name = of_type.get("name", "") if of_type else ""
                print(f"  • {field_name}: {type_kind} of {of_type_name or type_name}")
            else:
                print(f"  • {field_name}: {type_name}")
    
    # 3. Now check the BoolExp types to see filter options
    print("\n\n🎯 ATHLETEBOOLEXP (Filter Options):")
    print("-"*80)
    athlete_bool_result = await introspect_type("AthleteBoolExp")
    
    if "data" in athlete_bool_result and athlete_bool_result["data"]["__type"]:
        fields = athlete_bool_result["data"]["__type"]["fields"]
        if fields:
            print(f"\nAvailable filters: {len(fields)}\n")
            
            for field in sorted(fields, key=lambda x: x["name"]):
                field_name = field["name"]
                print(f"  • {field_name}")
        else:
            print("\nNo fields returned")
    
    print("\n\n🎯 GAMEPLAYERSTATBOOLEXP (Filter Options):")
    print("-"*80)
    stat_bool_result = await introspect_type("GamePlayerStatBoolExp")
    
    if "data" in stat_bool_result and stat_bool_result["data"]["__type"]:
        fields = stat_bool_result["data"]["__type"]["fields"]
        if fields:
            print(f"\nAvailable filters: {len(fields)}\n")
            
            for field in sorted(fields, key=lambda x: x["name"]):
                field_name = field["name"]
                print(f"  • {field_name}")
        else:
            print("\nNo fields returned")
    
    print("\n\n" + "="*80)
    print("✅ Schema Discovery Complete!")
    print("="*80)
    print("\nLook for relationship fields in the output above.")
    print("These are the field names to use for filtering active players!\n")

if __name__ == "__main__":
    asyncio.run(main())
