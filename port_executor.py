"""
Configuration-driven Port.io GraphQL query executor.
Executes queries based on intent configuration rather than hardcoded methods.
"""

import aiohttp
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta


class PortExecutor:
    """Execute GraphQL queries against Port.io API based on configuration"""
    
    def __init__(self, api_token: str):
        """
        Initialize executor with Port.io API token.
        
        Args:
            api_token: Port.io GraphQL API token
        """
        self.api_token = api_token
        self.base_url = "https://api.getport.io/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def execute_intent(self, intent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a query based on intent configuration.
        
        Args:
            intent_config: Configuration dict for the intent
        
        Returns:
            Query result dictionary with formatted values
        """
        query_type = intent_config.get("query_type")
        
        if query_type == "count_with_property":
            return await self.count_with_property(intent_config)
        elif query_type == "list_latest":
            return await self.list_latest(intent_config)
        elif query_type == "list_all":
            return await self.list_all(intent_config)
        elif query_type == "list_blueprints":
            return await self.list_blueprints(intent_config)
        else:
            return {"error": f"Unknown query type: {query_type}"}
    
    async def count_with_property(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Count entities and aggregate/average a numeric property.
        
        Args:
            config: Intent config with blueprint, property
        
        Returns:
            Dict with count and avg_{property}
        """
        blueprint = config.get("blueprint")
        property_name = config.get("property")
        
        query = f"""
        query {{
          entities(blueprint: "{blueprint}") {{
            pageInfo {{ total }}
            results {{ 
              properties {{ 
                {property_name}
              }} 
            }}
          }}
        }}
        """
        
        result = await self._query(query)
        
        # Check for errors
        if "errors" in result:
            return {"error": result["errors"][0].get("message", "Unknown error")}
        
        entities = result.get("data", {}).get("entities", {})
        count = entities.get("pageInfo", {}).get("total", 0)
        
        # Aggregate property values
        values = []
        for item in entities.get("results", []):
            if val := item.get("properties", {}).get(property_name):
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    pass
        
        avg = round(sum(values) / len(values), 1) if values else 0
        
        return {
            "count": count,
            f"avg_{property_name}": avg
        }
    
    async def list_latest(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get latest N entities ordered by a field.
        
        Args:
            config: Intent config with blueprint, order_by, limit
        
        Returns:
            Dict with results list
        """
        blueprint = config.get("blueprint")
        limit = config.get("limit", 5)
        order_by = config.get("order_by", "created_at")
        
        query = f"""
        query {{
          entities(blueprint: "{blueprint}", orderBy: [{{key: "{order_by}", direction: DESC}}], first: {limit}) {{
            results {{ 
              properties {{ 
                id
                title
                {order_by}
              }} 
            }}
          }}
        }}
        """
        
        result = await self._query(query)
        
        if "errors" in result:
            return {"error": result["errors"][0].get("message", "Unknown error")}
        
        entities = result.get("data", {}).get("entities", {}).get("results", [])
        
        # Format results as readable list
        items = []
        for e in entities:
            props = e.get("properties", {})
            title = props.get("title", props.get("id", "Unknown"))
            timestamp = props.get(order_by)
            age = self._time_ago(timestamp) if timestamp else "unknown"
            items.append(f"• {title} ({age})")
        
        return {"results": "\n".join(items) if items else "No results found"}
    
    async def list_all(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all entities of a blueprint grouped by a property.
        
        Args:
            config: Intent config with blueprint
        
        Returns:
            Dict with results list
        """
        blueprint = config.get("blueprint")
        group_by = config.get("group_by", "id")
        
        query = f"""
        query {{
          entities(blueprint: "{blueprint}") {{
            results {{ 
              properties {{ 
                {group_by}
              }} 
            }}
          }}
        }}
        """
        
        result = await self._query(query)
        
        if "errors" in result:
            return {"error": result["errors"][0].get("message", "Unknown error")}
        
        entities = result.get("data", {}).get("entities", {}).get("results", [])
        
        # Count by property value
        counts = {}
        for e in entities:
            if val := e.get("properties", {}).get(group_by):
                counts[val] = counts.get(val, 0) + 1
        
        # Format as readable list
        items = [f"• {key}: {count}" for key, count in sorted(counts.items())]
        
        return {"results": "\n".join(items) if items else "No results found"}
    
    async def list_blueprints(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all available blueprints.
        
        Args:
            config: Intent config (ignored for this query type)
        
        Returns:
            Dict with blueprint list
        """
        query = """
        query {
          blueprints {
            nodes {
              identifier
              title
            }
          }
        }
        """
        
        result = await self._query(query)
        
        if "errors" in result:
            return {"error": result["errors"][0].get("message", "Unknown error")}
        
        blueprints = result.get("data", {}).get("blueprints", {}).get("nodes", [])
        blueprint_list = [b.get("identifier") for b in blueprints]
        
        return {"blueprints": ", ".join(blueprint_list)}
    
    async def _query(self, query: str) -> Dict[str, Any]:
        """
        Execute a raw GraphQL query against Port.io API.
        
        Args:
            query: GraphQL query string
        
        Returns:
            Response dictionary (may contain errors)
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query}
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        return {"errors": [{"message": f"Port API returned {resp.status}"}]}
                    return await resp.json()
        except asyncio.TimeoutError:
            return {"errors": [{"message": "Port API request timed out"}]}
        except Exception as e:
            return {"errors": [{"message": str(e)}]}
    
    @staticmethod
    def _time_ago(iso_timestamp: str) -> str:
        """Convert ISO timestamp to relative time string"""
        if not iso_timestamp:
            return "unknown"
        
        try:
            deployed = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
            now = datetime.now(deployed.tzinfo)
            delta = now - deployed
            
            seconds = int(delta.total_seconds())
            
            if seconds < 60:
                return f"{seconds}s ago"
            elif seconds < 3600:
                return f"{seconds // 60}m ago"
            elif seconds < 86400:
                return f"{seconds // 3600}h ago"
            else:
                return f"{seconds // 86400}d ago"
        except Exception:
            return "unknown"
