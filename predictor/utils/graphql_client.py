import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any

class GraphQLClient:
    """Handles GraphQL API communications for live data"""
    
    def __init__(self):
        self.endpoint = "https://collegefootballdata.com/graphql"
        self.session = None
    
    async def get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def execute_query(self, query: str, variables: Dict = None) -> Dict[str, Any]:
        """Execute a GraphQL query"""
        session = await self.get_session()
        
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            async with session.post(self.endpoint, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"GraphQL request failed with status {response.status}")
                    return {}
        except Exception as e:
            print(f"GraphQL request error: {e}")
            return {}
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()