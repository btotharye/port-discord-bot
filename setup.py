#!/usr/bin/env python3
"""
Interactive configuration wizard for Port Discord Bot.
Creates a basic config.yaml file with user-provided values.
"""

import yaml
import os


def setup():
    """Interactive setup wizard"""
    print("\n" + "="*60)
    print("⚙️  Port Discord Bot - Setup Wizard")
    print("="*60 + "\n")
    
    # Get Port API token
    print("First, we need your Port.io API credentials.")
    port_token = input("Enter your Port.io API token: ").strip()
    
    if not port_token:
        print("❌ Port API token is required!")
        return
    
    # Get Discord token
    print("\nNext, your Discord bot token.")
    discord_token = input("Enter your Discord bot token: ").strip()
    
    if not discord_token:
        print("❌ Discord token is required!")
        return
    
    # Get primary blueprint
    print("\nWhat's your primary blueprint?")
    print("(Examples: Animal, Project, User, Deployment, etc.)")
    blueprint = input("Enter blueprint name: ").strip()
    
    if not blueprint:
        print("❌ Blueprint name is required!")
        return
    
    # Get Discord channel
    discord_channel = input("Enter Discord channel name (default: port-herp-ops): ").strip()
    if not discord_channel:
        discord_channel = "port-herp-ops"
    
    # Create basic configuration
    config = {
        "port_api_token": "${PORT_API_TOKEN}",
        "discord_token": "${DISCORD_TOKEN}",
        "discord_channel": discord_channel,
        "intents": {
            "count": {
                "keywords": ["how many", "count", "total"],
                "blueprint": blueprint,
                "query_type": "count_with_property",
                "property": "id",
                "response": f"📊 Total {blueprint}s: {{count}}"
            },
            "list": {
                "keywords": ["list", "show", "all"],
                "blueprint": blueprint,
                "query_type": "list_all",
                "response": f"📊 {blueprint}s:\n{{results}}"
            },
            "entities": {
                "keywords": ["entities", "blueprints", "available"],
                "query_type": "list_blueprints",
                "response": "📊 Available blueprints: {blueprints}"
            }
        }
    }
    
    # Write configuration file
    try:
        with open("config.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print("\n✅ Configuration created at config.yaml")
    except Exception as e:
        print(f"❌ Failed to write config.yaml: {e}")
        return
    
    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write(f"PORT_API_TOKEN={port_token}\n")
            f.write(f"DISCORD_TOKEN={discord_token}\n")
        print("✅ Environment variables saved to .env")
        print("⚠️  Added .env to .gitignore - DO NOT commit this file!")
    except Exception as e:
        print(f"❌ Failed to write .env: {e}")
        return
    
    # Print next steps
    print("\n" + "="*60)
    print("📋 Next steps:")
    print("="*60)
    print("\n1. Review your configuration:")
    print("   cat config.yaml")
    print("\n2. Edit config.yaml to add more intents/queries (optional)")
    print("\n3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n4. Run the bot:")
    print("   python bot.py")
    print("\n5. For deployment to Railway.app:")
    print("   git add . && git commit -m 'Configure bot' && git push")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    setup()
