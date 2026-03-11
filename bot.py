"""
Port Discord Bot - Configuration-driven main entry point.
Loads configuration from config.yaml and responds to intents.
"""

import discord
from discord.ext import commands
from config_parser import ConfigParser
from port_executor import PortExecutor

# Load configuration
config = ConfigParser()

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize Port executor
port = PortExecutor(api_token=config.get_api_token())


@bot.event
async def on_ready():
    """Bot startup event"""
    print(f"✅ Bot logged in as {bot.user}")
    print(f"📡 Listening on #{config.get_discord_channel()}")


@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Only respond in configured channel
    if message.channel.name != config.get_discord_channel():
        await bot.process_commands(message)
        return
    
    # Parse intent from configuration
    intent = config.parse_intent(message.content)
    
    if intent:
        intent_config = config.get_intent_config(intent)
        
        try:
            # Show typing indicator while querying
            async with message.channel.typing():
                result = await port.execute_intent(intent_config)
            
            # Check for errors
            if "error" in result:
                await message.reply(f"❌ Error: {result['error']}")
            else:
                # Format response using template from config
                response_template = intent_config.get("response", "Got data: {results}")
                response = response_template.format(**result)
                await message.reply(response)
        
        except Exception as e:
            await message.reply(f"❌ Error querying Port: {str(e)}")
    
    else:
        # Intent not recognized
        await message.reply("🤔 I didn't understand that. Try asking about your blueprints or check config.yaml for available queries.")


if __name__ == "__main__":
    bot.run(config.get_discord_token())
