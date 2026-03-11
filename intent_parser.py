"""
Intent parser for natural language message understanding.
Detects user intent from Discord messages and returns the corresponding query type.
"""


def parse_intent(message: str) -> str:
    """
    Parse user message and return intent keyword.
    
    Args:
        message: User's Discord message text
    
    Returns:
        Intent keyword: "animals", "health", "feedings", "deployments", "users", 
                       "scorecard", or None if intent cannot be determined
    """
    lower = message.lower().strip()
    
    # Intent keyword groups
    animals_keywords = ["animal", "reptile", "count", "many", "how many", "total animals", "animals"]
    health_keywords = ["health", "score", "overview", "collection", "condition", "status"]
    feeding_keywords = ["feeding", "feed", "recent", "logs", "feedings", "accepted", "acceptance"]
    deploy_keywords = ["deploy", "deployment", "version", "release", "api", "frontend"]
    user_keywords = ["user", "users", "tier", "subscription", "how many users", "signup"]
    scorecard_keywords = ["scorecard", "readiness", "production", "tier", "gold", "silver", "bronze"]
    
    # Check animals
    if any(kw in lower for kw in animals_keywords):
        return "animals"
    
    # Check health
    if any(kw in lower for kw in health_keywords):
        return "health"
    
    # Check feedings
    if any(kw in lower for kw in feeding_keywords):
        return "feedings"
    
    # Check deployments
    if any(kw in lower for kw in deploy_keywords):
        return "deployments"
    
    # Check users
    if any(kw in lower for kw in user_keywords):
        return "users"
    
    # Check scorecard
    if any(kw in lower for kw in scorecard_keywords):
        return "scorecard"
    
    return None
