import aiohttp
import asyncio
from typing import Dict, Any
from datetime import datetime, timedelta


class PortClient:
    """GraphQL client for Port.io API"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.getport.io/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def _query(self, query: str, variables: Dict = None) -> Dict[str, Any]:
        """Make a GraphQL query to Port.io"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query, "variables": variables or {}}
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
    
    async def get_animal_count(self) -> Dict[str, Any]:
        """Get total animals and average health score"""
        query = """
        query {
          entities(blueprint: "Animal") {
            pageInfo { total }
            results {
              properties {
                health_score
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        # Check for errors
        if "errors" in result:
            return {"count": 0, "avg_health": 0, "error": result["errors"][0]["message"]}
        
        data = result.get("data", {}).get("entities", {})
        animals = data.get("pageInfo", {}).get("total", 0)
        
        health_scores = []
        for item in data.get("results", []):
            if score := item.get("properties", {}).get("health_score"):
                try:
                    health_scores.append(float(score))
                except (ValueError, TypeError):
                    pass
        
        avg_health = round(sum(health_scores) / len(health_scores), 1) if health_scores else 0
        
        return {"count": animals, "avg_health": avg_health}
    
    async def get_health_overview(self) -> Dict[str, Any]:
        """Get health overview from Port"""
        query = """
        query {
          entities(blueprint: "Animal") {
            results {
              properties {
                health_score
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        if "errors" in result:
            return {"avg_score": 0, "at_risk": 0, "error": result["errors"][0]["message"]}
        
        data = result.get("data", {}).get("entities", {}).get("results", [])
        
        scores = []
        at_risk = 0
        
        for item in data:
            if score := item.get("properties", {}).get("health_score"):
                try:
                    score_val = float(score)
                    scores.append(score_val)
                    if score_val < 50:
                        at_risk += 1
                except (ValueError, TypeError):
                    pass
        
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        
        return {"avg_score": avg_score, "at_risk": at_risk}
    
    async def get_recent_feedings(self) -> Dict[str, Any]:
        """Get recent feeding stats from last 7 days"""
        query = """
        query {
          entities(blueprint: "Feeding") {
            pageInfo { total }
            results {
              properties {
                feeding_date
                acceptance_rate
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        if "errors" in result:
            return {"this_week": 0, "acceptance": 0, "error": result["errors"][0]["message"]}
        
        data = result.get("data", {}).get("entities", {}).get("results", [])
        
        # Count feedings from last 7 days
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        this_week = 0
        acceptance_rates = []
        
        for item in data:
            props = item.get("properties", {})
            if feed_date := props.get("feeding_date"):
                if feed_date >= week_ago:
                    this_week += 1
            
            if rate := props.get("acceptance_rate"):
                try:
                    acceptance_rates.append(float(rate))
                except (ValueError, TypeError):
                    pass
        
        avg_acceptance = round(sum(acceptance_rates) / len(acceptance_rates), 1) if acceptance_rates else 0
        
        return {"this_week": this_week, "acceptance": avg_acceptance}
    
    async def get_deployments(self) -> Dict[str, Any]:
        """Get latest API and Frontend deployments"""
        query = """
        query {
          entities(blueprint: "Deployment") {
            results {
              properties {
                service_name
                version
                deployed_at
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        if "errors" in result:
            return {
                "api_version": "unknown",
                "api_age": "unknown",
                "frontend_version": "unknown",
                "frontend_age": "unknown",
                "error": result["errors"][0]["message"]
            }
        
        data = result.get("data", {}).get("entities", {}).get("results", [])
        
        api_info = {"version": "unknown", "deployed_at": None}
        frontend_info = {"version": "unknown", "deployed_at": None}
        
        for item in data:
            props = item.get("properties", {})
            service = props.get("service_name", "").lower()
            
            if "api" in service:
                api_info["version"] = props.get("version", "unknown")
                api_info["deployed_at"] = props.get("deployed_at")
            elif "frontend" in service:
                frontend_info["version"] = props.get("version", "unknown")
                frontend_info["deployed_at"] = props.get("deployed_at")
        
        api_age = self._time_ago(api_info["deployed_at"])
        frontend_age = self._time_ago(frontend_info["deployed_at"])
        
        return {
            "api_version": api_info["version"],
            "api_age": api_age,
            "frontend_version": frontend_info["version"],
            "frontend_age": frontend_age
        }
    
    async def get_user_breakdown(self) -> Dict[str, Any]:
        """Get user count by subscription tier"""
        query = """
        query {
          entities(blueprint: "User") {
            results {
              properties {
                subscription_tier
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        if "errors" in result:
            return {"free": 0, "hobbyist": 0, "pro": 0, "error": result["errors"][0]["message"]}
        
        data = result.get("data", {}).get("entities", {}).get("results", [])
        
        tiers = {"free": 0, "hobbyist": 0, "pro": 0}
        
        for item in data:
            if tier := item.get("properties", {}).get("subscription_tier", "").lower():
                if tier in tiers:
                    tiers[tier] += 1
        
        return tiers
    
    async def get_scorecard_health(self) -> Dict[str, Any]:
        """Get scorecard tier ratings for services"""
        query = """
        query {
          entities(blueprint: "Service") {
            results {
              properties {
                service_name
                scorecard_tier
              }
            }
          }
        }
        """
        result = await self._query(query)
        
        if "errors" in result:
            return {
                "api_tier": "Unknown",
                "frontend_tier": "Unknown",
                "landing_tier": "Unknown",
                "error": result["errors"][0]["message"]
            }
        
        data = result.get("data", {}).get("entities", {}).get("results", [])
        
        tiers = {"api_tier": "Unknown", "frontend_tier": "Unknown", "landing_tier": "Unknown"}
        
        for item in data:
            props = item.get("properties", {})
            service = props.get("service_name", "").lower()
            score_tier = props.get("scorecard_tier", "Unknown")
            
            if "api" in service:
                tiers["api_tier"] = score_tier
            elif "frontend" in service:
                tiers["frontend_tier"] = score_tier
            elif "landing" in service:
                tiers["landing_tier"] = score_tier
        
        return tiers
    
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
