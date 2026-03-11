# Port.io Discord Bot 🦎

A **fully configuration-driven** Discord bot that queries any Port.io instance using natural language. No code changes needed — just edit `config.yaml` to customize for your Port.io setup.

**Fork-friendly.** Deploy to Railway.app in 5 minutes.

## Features

- 🎯 **Configuration-Driven** — All intents and queries defined in `config.yaml`
- 🔧 **Fully Extensible** — Add new intents/queries without touching Python code
- 🦎 **Any Port.io Setup** — Works with any blueprints and properties
- 🚀 **Easy Deployment** — Railway.app, Docker, or local Python
- 📝 **Interactive Setup** — Optional `setup.py` wizard for non-technical users
- ⚡ **Async GraphQL** — Fast, responsive queries with proper error handling

## Architecture

```
config.yaml (user-editable)
    ↓
config_parser.py (loads YAML + env vars)
    ↓
bot.py (Discord handler)
    ↓
port_executor.py (generic Port API queries)
```

Everything is data-driven. Users customize via YAML; no Python code changes needed.

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
git clone https://github.com/btotharye/port-discord-bot.git
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

### 4. Configure the Bot

#### Option A: Interactive Setup (Recommended)
```bash
python setup.py
```

This creates `config.yaml` and `.env` interactively.

#### Option B: Manual Setup
```bash
cp .env.example .env
```

Edit `.env` and add your tokens:
```
PORT_API_TOKEN=your_port_api_token_here
DISCORD_TOKEN=your_discord_bot_token_here
```

### 5. Customize config.yaml (Optional)
Edit `config.yaml` to add/modify intents and queries:

```yaml
intents:
  my_custom_query:
    keywords: ["my", "custom", "keywords"]
    blueprint: "MyBlueprint"
    query_type: "count_with_property"
    property: "some_property"
    response: "📊 Result: {count} items, avg: {avg_some_property}"
```

See [Configuring Intents](#configuring-intents) below.

### 6. Run the Bot
```bash
python bot.py
```

You should see:
```
✅ Bot logged in as YourBotName#1234
📡 Listening on #port-herp-ops
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
8. Create a channel called `#port-herp-ops` (or change `discord_channel` in `config.yaml`)

## Configuring Intents

All intents are defined in `config.yaml`. You can add custom intents without touching Python code.

### Intent Configuration Structure

```yaml
intents:
  intent_name:
    keywords: ["word1", "word2", "word3"]  # User message must contain any of these
    blueprint: "YourBlueprint"               # Port blueprint name
    query_type: "count_with_property"        # See query types below
    property: "property_name"                # (optional, required for count_with_property)
    limit: 5                                 # (optional, for list_latest)
    order_by: "created_at"                   # (optional, for list_latest)
    response: "📊 Result: {count}"           # Response template with placeholders
```

### Query Types

#### 1. `count_with_property`
Count all entities of a blueprint and aggregate/average a numeric property.

**Returns:**
- `{count}` — Total entity count
- `{avg_PROPERTY}` — Average value of the property

**Example:**
```yaml
animals:
  keywords: ["animal", "count", "how many"]
  blueprint: "Animal"
  query_type: "count_with_property"
  property: "health_score"
  response: "🦎 Total Animals: {count} • Avg Health: {avg_health_score}%"
```

#### 2. `list_latest`
Get the N latest entities ordered by a field.

**Returns:**
- `{results}` — Newline-separated list of entities with timestamps

**Example:**
```yaml
deployments:
  keywords: ["deploy", "version", "release"]
  blueprint: "Deployment"
  query_type: "list_latest"
  limit: 5
  order_by: "created_at"
  response: "✅ Latest Deployments:\n{results}"
```

#### 3. `list_all`
List all entities grouped/counted by a property.

**Returns:**
- `{results}` — Newline-separated count breakdown

**Example:**
```yaml
users:
  keywords: ["user", "users", "tier"]
  blueprint: "User"
  query_type: "list_all"
  group_by: "subscription_tier"
  response: "👥 Users by Tier:\n{results}"
```

#### 4. `list_blueprints`
List all available blueprints in your Port workspace.

**Returns:**
- `{blueprints}` — Comma-separated blueprint names

**Example:**
```yaml
entities:
  keywords: ["blueprints", "entities", "available"]
  query_type: "list_blueprints"
  response: "📊 Available blueprints: {blueprints}"
```

## Using the Bot

Once running, send messages in your configured Discord channel:

```
User: "How many animals do we have?"
Bot: 🦎 Total Animals: 42 • Avg Health: 87.3%

User: "Show recent deployments"
Bot: ✅ Latest Deployments:
     • v2.3.1 (2h ago)
     • v2.3.0 (1d ago)
     • v2.2.9 (3d ago)

User: "What blueprints are available?"
Bot: 📊 Available blueprints: Animal, Deployment, User, Feeding
```

## Deployment to Railway.app

### 1. Push to GitHub
If not already done:
```bash
git add .
git commit -m "Configure Port Discord bot"
git push origin main
```

### 2. Connect to Railway.app
1. Go to [railway.app](https://railway.app)
2. Click **New Project**
3. Select **Deploy from GitHub repo** → Authorize GitHub
4. Select your fork of `port-discord-bot`
5. Railway detects the `Dockerfile` automatically

### 3. Add Environment Variables
In Railway project settings:
1. Click **Variables**
2. Add:
   - `PORT_API_TOKEN`: your Port.io API token
   - `DISCORD_TOKEN`: your Discord bot token
3. Click **Deploy**

### 4. Monitor
Railway will build and deploy automatically. Watch logs:
```
✅ Bot logged in as YourBotName#1234
📡 Listening on #port-herp-ops
```

Your bot is now live! 🚀

## Project Structure

```
port-discord-bot/
├── config.yaml              # User-editable configuration
├── bot.py                   # Main Discord bot entry point
├── config_parser.py         # Loads config.yaml + env vars
├── port_executor.py         # Generic Port API query executor
├── setup.py                 # Interactive setup wizard
├── requirements.txt         # Python dependencies
├── .env.example             # Template for environment variables
├── Dockerfile               # Container image for Railway
└── README.md               # This file
```

### File Responsibilities

- **`config.yaml`** — User edits this to customize intents/queries
- **`bot.py`** — Discord event handler, delegates to port_executor
- **`config_parser.py`** — Loads YAML, expands `${ENV_VAR}` syntax
- **`port_executor.py`** — Generic GraphQL query builder + executor
- **`setup.py`** — Interactive CLI wizard to create config files

## Customization Examples

### Example 1: Track Feeding Acceptance

```yaml
# In config.yaml
feedings:
  keywords: ["feeding", "feed", "acceptance", "accepted"]
  blueprint: "Feeding"
  query_type: "count_with_property"
  property: "acceptance_rate"
  response: "🍖 Feedings: {count} total • Avg Acceptance: {avg_acceptance_rate}%"
```

Message: `"How's our feeding acceptance?"`
Bot: `🍖 Feedings: 156 total • Avg Acceptance: 91.3%`

### Example 2: List All Deployment Services

```yaml
# In config.yaml
services:
  keywords: ["service", "services", "list"]
  blueprint: "Service"
  query_type: "list_all"
  group_by: "status"
  response: "🔧 Services by Status:\n{results}"
```

Message: `"What services do we have?"`
Bot:
```
🔧 Services by Status:
• healthy: 8
• degraded: 1
• offline: 0
```

### Example 3: Custom Blueprint Query

```yaml
# In config.yaml
habitats:
  keywords: ["habitat", "enclosure", "tank"]
  blueprint: "Habitat"
  query_type: "count_with_property"
  property: "temperature"
  response: "🌡️ Habitats: {count} • Avg Temp: {avg_temperature}°F"
```

## Troubleshooting

### Bot doesn't respond
- ✅ Verify `PORT_API_TOKEN` and `DISCORD_TOKEN` in `.env`
- ✅ Check bot is in the server
- ✅ Ensure channel name matches `discord_channel` in `config.yaml`
- ✅ Check bot logs for errors

### "Port API request timed out"
- ✅ Verify `PORT_API_TOKEN` is correct and active
- ✅ Check Port.io API status
- ✅ Ensure your Port workspace is accessible

### "Unknown query type" error
- ✅ Check `query_type` spelling in `config.yaml`
- ✅ Valid types: `count_with_property`, `list_latest`, `list_all`, `list_blueprints`

### Bot crashes on startup
- ✅ Ensure `requirements.txt` dependencies are installed: `pip install -r requirements.txt`
- ✅ Check `.env` file has both tokens
- ✅ Check `config.yaml` exists and is valid YAML

### GraphQL errors
- ✅ Verify blueprint name exists in your Port workspace
- ✅ Verify property name exists in that blueprint
- ✅ Try simplifying the query (start with `count_with_property`)

## Architecture Advantages

### ✅ For Users
- **No coding required** — customize via YAML
- **Fork-friendly** — git clone → edit config.yaml → deploy
- **Extensible** — add intents without touching Python

### ✅ For Developers
- **Configuration-driven** — clear separation of data vs. logic
- **Testable** — each component (parser, executor) is independently testable
- **Maintainable** — adding new query types doesn't require modifying bot.py

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -am "Add feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

## License

MIT License — see LICENSE file for details.

## Support

For issues or feature requests:
1. Check this README's Troubleshooting section
2. Review `config.yaml` for syntax errors
3. Open a GitHub issue with error logs and configuration

---

**Built with ❤️ for flexible Port.io automation**
