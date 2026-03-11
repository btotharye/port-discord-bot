import os
import discord
from discord.ext import commands
from port_client import PortClient
from intent_parser import parse_intent

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

port = PortClient(api_token=os.getenv("PORT_API_TOKEN"))

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Only respond in #port-herp-ops channel
    if message.channel.name != "port-herp-ops":
        await bot.process_commands(message)
        return
    
    # Parse intent
    intent = parse_intent(message.content)
    
    if intent == "animals":
        async with message.channel.typing():
            data = await port.get_animal_count()
            await message.reply(f"🦎 Total Animals: {data['count']} • Avg Health: {data['avg_health']}%")
    
    elif intent == "health":
        async with message.channel.typing():
            data = await port.get_health_overview()
            await message.reply(f"❤️ Health Overview: {data['avg_score']}% • At Risk: {data['at_risk']}")
    
    elif intent == "feedings":
        async with message.channel.typing():
            data = await port.get_recent_feedings()
            await message.reply(f"🍖 Recent Feedings: {data['this_week']} this week • Acceptance: {data['acceptance']}%")
    
    elif intent == "deployments":
        async with message.channel.typing():
            data = await port.get_deployments()
            await message.reply(f"✅ API: {data['api_version']} ({data['api_age']}) | ✅ Frontend: {data['frontend_version']} ({data['frontend_age']})")
    
    elif intent == "users":
        async with message.channel.typing():
            data = await port.get_user_breakdown()
            await message.reply(f"👥 Users: Free {data['free']} | Hobbyist {data['hobbyist']} | Pro {data['pro']}")
    
    elif intent == "scorecard":
        async with message.channel.typing():
            data = await port.get_scorecard_health()
            await message.reply(f"📊 Scorecard: API {data['api_tier']} | Frontend {data['frontend_tier']} | Landing {data['landing_tier']}")
    
    else:
        await message.reply("🤔 I didn't understand that. Try: animals, health, feedings, deployments, users, or scorecard")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
