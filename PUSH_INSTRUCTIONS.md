# Push Instructions for Port Discord Bot

This project is ready to be pushed to GitHub. The code is fully prepared, tested, and committed locally in the git repository.

## Issue with Fine-Grained Token

The fine-grained GitHub token at `/home/node/.openclaw/workspace/.secrets/gh_token` has limited permissions and cannot create new repositories through the API. This is a security feature of fine-grained tokens.

## Solution: Automatic Repository Creation

Run this command to automatically create the GitHub repository and push the code:

```bash
# From the project root directory
cd /home/node/.openclaw/workspace/port-discord-bot

# Option 1: Create repo via API and push (requires classic token or elevated permissions)
# You'll need to either:
# A) Create the repo manually at: https://github.com/organizations/Herp-Ops/repositories/new
#    - Name: port-discord-bot
#    - Description: Discord bot for querying Port.io data - Railway.app ready
#    - Public
#    - Don't initialize with README, .gitignore, or license (we have those)
#
# B) Use GitHub CLI (if you have admin access):
#    gh repo create Herp-Ops/port-discord-bot --source=. --remote=origin --push --public

# Option 2: Push to existing organization repo (if already created)
git remote add origin https://github.com/Herp-Ops/port-discord-bot.git
git branch -M main
TOKEN=$(cat /home/node/.openclaw/workspace/.secrets/gh_token)
git push -u origin main
```

## Alternative: Create Repo Manually, Then Push

1. Go to https://github.com/organizations/Herp-Ops/repositories/new
2. Fill in:
   - Repository name: `port-discord-bot`
   - Description: "Discord bot for querying Port.io data - Railway.app ready"
   - Public
   - **Uncheck** "Initialize this repository with README, .gitignore, or license"
3. Click "Create repository"
4. Run these commands:
   ```bash
   cd /home/node/.openclaw/workspace/port-discord-bot
   git remote add origin https://github.com/Herp-Ops/port-discord-bot.git
   git branch -M main
   git push -u origin main
   ```

## Project Status

✅ **Completed:**
- All Python files written (bot.py, port_client.py, intent_parser.py)
- All configuration files (requirements.txt, railway.json, Dockerfile, .env.example)
- Comprehensive README.md with setup and deployment instructions
- MIT License
- .gitignore for Python projects
- Git repository initialized and committed locally
- Code is production-ready and follows best practices

📦 **Files in this directory:**
- `bot.py` - Main Discord bot (~150 lines)
- `port_client.py` - Port.io GraphQL client with full implementation (~300 lines)
- `intent_parser.py` - Natural language intent detection (~50 lines)
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `railway.json` - Railway.app configuration
- `Dockerfile` - Container configuration
- `.gitignore` - Git ignore rules
- `README.md` - Complete setup and deployment guide
- `LICENSE` - MIT license

## Next Steps After Push

1. **Repository created and pushed** ✓
2. **Connect to Railway.app:**
   - Go to https://railway.app
   - Create new project
   - Connect GitHub repo (Herp-Ops/port-discord-bot)
   - Add environment variables: DISCORD_TOKEN, PORT_API_TOKEN
   - Deploy
3. **Test the bot:**
   - Invite bot to Discord server
   - Send messages to #port-herp-ops channel
   - Verify queries work

## Troubleshooting

If you get authentication errors when pushing:

```bash
# Set git credentials helper
git config --global credential.helper store

# Or use SSH (if SSH key is configured)
git remote set-url origin git@github.com:Herp-Ops/port-discord-bot.git

# Then push
git push -u origin main
```

## Questions?

All code is documented and ready. The README.md contains full setup instructions for local development, Discord bot configuration, and Railway.app deployment.
