# Port.io Discord Bot 🦎

A standalone Discord bot that queries Port.io data using natural language. Ask about animals, health, feedings, deployments, users, or scorecard status directly in Discord.

**Deployable to Railway.app in 5 minutes.**

## Features

- 🦎 **Animal Count**: Total animals in your Port.io database + average health score
- ❤️ **Health Overview**: Aggregate health scores and at-risk animal count
- 🍖 **Recent Feedings**: Feeding logs from the last 7 days + acceptance rates
- ✅ **Deployments**: Latest API and Frontend versions + deployment age
- 👥 **User Breakdown**: User count by subscription tier (Free, Hobbyist, Pro)
- 📊 **Scorecard Health**: Service tier ratings (Gold, Silver, Bronze)

## Prerequisites

### For Local Development
- Python 3.11+
- `pip` (Python package manager)
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- Port.io API Token (from your Port.io workspace settings)

### For Railway.app Deployment
- GitHub account
- Railway.app account (sign up at [railway.app](https://railway.app))
- Same Discord & Port tokens

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Herp-Ops/port-discord-bot.git
cd port-discord-bot
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your tokens:
```
DISCORD_TOKEN=your_discord_bot_token_here
PORT_API_TOKEN=your_port_api_token_here
```

### 5. Run the Bot
```bash
python bot.py
```

You should see:
```
✅ Bot logged in as YourBotName#1234
```

## Discord Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application → name it "Port Bot"
3. Go to **Bot** → click **Add Bot**
4. Copy the **Token** and paste into `.env` as `DISCORD_TOKEN`
5. Under **Scopes**, select:
   - `bot`
6. Under **Permissions**, select:
   - `Send Messages`
   - `Read Message History`
7. Copy the **OAuth2 URL** (under Scopes) and open it to invite the bot to your server
8. Create a channel called `#port-herp-ops` (or update `bot.py` to use a different channel name)

## Using the Bot

Once the bot is running and in your Discord server, send messages in `#port-herp-ops`:

```
# Ask about animals
"How many animals do we have?"
→ 🦎 Total Animals: 42 • Avg Health: 87.3%

# Check health status
"What's the health overview?"
→ ❤️ Health Overview: 84.2% • At Risk: 3

# View recent feedings
"Show me recent feedings"
→ 🍖 Recent Feedings: 25 this week • Acceptance: 92.1%

# Check deployments
"What's the latest deployment?"
→ ✅ API: v2.3.1 (2h ago) | ✅ Frontend: v1.9.2 (1h ago)

# User breakdown
"How many users do we have?"
→ 👥 Users: Free 150 | Hobbyist 32 | Pro 8

# Scorecard status
"What's our scorecard status?"
→ 📊 Scorecard: API Gold | Frontend Silver | Landing Bronze
```

## Deployment to Railway.app

### 1. Push to GitHub
If not already done:
```bash
git add .
git commit -m "Initial commit: Port Discord bot"
git push origin main
```

### 2. Connect to Railway.app
1. Go to [railway.app](https://railway.app)
2. Click **New Project**
3. Select **Deploy from GitHub repo** → Authorize GitHub
4. Select `Herp-Ops/port-discord-bot`
5. Railway detects the `Dockerfile` automatically

### 3. Add Environment Variables
In Railway project settings:
1. Click **Variables**
2. Add:
   - `DISCORD_TOKEN`: your Discord bot token
   - `PORT_API_TOKEN`: your Port.io API token
3. Click **Deploy**

### 4. Monitor
Railway will build and deploy automatically. Watch logs to confirm:
```
✅ Bot logged in as YourBotName#1234
```

**That's it!** Your bot is now live on Railway. 🚀

## Architecture

### `bot.py`
Main Discord bot entry point. Listens for messages in `#port-herp-ops`, parses intent, and calls Port client methods.

### `port_client.py`
GraphQL client for Port.io API. Handles all API queries with error handling and async/await for responsiveness.

### `intent_parser.py`
Natural language intent detection. Matches message keywords to query types without complex NLP.

### `Dockerfile`
Containerization for Railway.app. Uses `python:3.11-slim` for minimal image size.

## GraphQL Queries

The bot uses Port.io's GraphQL API. Query structure is based on your Port blueprints:
- `Animal` → health scores, count
- `Feeding` → feeding logs, acceptance rates
- `Deployment` → service versions, deployment timestamps
- `User` → subscription tier counts
- `Service` → scorecard scores

**Note:** If your Port schema differs, update GraphQL queries in `port_client.py` to match your blueprint structure.

## Error Handling

The bot gracefully handles:
- ❌ Port API timeouts (10s timeout)
- ❌ Missing or invalid tokens
- ❌ Network errors
- ❌ Unexpected response formats

If Port API is down, the bot replies with an error message instead of crashing.

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -am "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

## Troubleshooting

### Bot doesn't respond
- Verify `DISCORD_TOKEN` is correct
- Check bot is in the server
- Ensure `#port-herp-ops` channel exists
- Check bot logs for errors

### "Port API request timed out"
- Verify `PORT_API_TOKEN` is correct
- Check Port.io API status
- Verify your Port workspace is accessible

### Bot crashes on startup
- Ensure `requirements.txt` dependencies are installed
- Check `.env` file has both tokens
- Review bot logs for specific errors

## License

MIT License — see LICENSE file for details.

## Support

For issues or feature requests, open a GitHub issue or check Discord logs for detailed error messages.

---

**Built with ❤️ for Herp-Ops**
