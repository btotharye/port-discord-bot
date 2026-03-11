#!/bin/bash
# Push Port Discord Bot to GitHub Herp-Ops org

set -e

echo "🚀 Port Discord Bot - GitHub Push Script"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "bot.py" ] || [ ! -f "port_client.py" ]; then
    echo "❌ Error: Not in port-discord-bot directory"
    echo "   Run this from /home/node/.openclaw/workspace/port-discord-bot/"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "✓ Project files detected"
echo ""

# Check if git is configured
if [ ! -d ".git" ]; then
    echo "❌ Error: Git repository not initialized"
    exit 1
fi

echo "🔑 Loading GitHub token..."
TOKEN=$(cat /home/node/.openclaw/workspace/.secrets/gh_token)
echo "✓ Token loaded"
echo ""

echo "📝 Attempting to create GitHub repository..."
echo "   Organization: Herp-Ops"
echo "   Repository: port-discord-bot"
echo ""

# Try to create the repository via REST API
RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/orgs/Herp-Ops/repos \
  -d '{
    "name": "port-discord-bot",
    "description": "Discord bot for querying Port.io data - Railway.app ready",
    "homepage": "https://github.com/Herp-Ops/port-discord-bot",
    "private": false,
    "has_issues": true,
    "has_projects": true
  }' -w "\n%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Repository created successfully!"
elif echo "$BODY" | grep -q '"name":"port-discord-bot"'; then
    echo "✅ Repository already exists (or was just created)"
elif [ "$HTTP_CODE" = "403" ]; then
    echo "⚠️  Token doesn't have permission to create org repositories"
    echo ""
    echo "📌 Manual Solution:"
    echo "   1. Go to: https://github.com/organizations/Herp-Ops/repositories/new"
    echo "   2. Enter repository name: port-discord-bot"
    echo "   3. Uncheck 'Initialize with README, .gitignore, or license'"
    echo "   4. Click 'Create repository'"
    echo "   5. Run this script again"
    exit 1
else
    echo "❌ Error creating repository (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
    exit 1
fi

echo ""
echo "📤 Configuring git remote..."

# Configure git remote
git remote remove origin 2>/dev/null || true
git remote add origin https://${TOKEN}@github.com/Herp-Ops/port-discord-bot.git
echo "✓ Remote configured: origin -> Herp-Ops/port-discord-bot"

echo ""
echo "🌿 Ensuring main branch..."
git branch -M main 2>/dev/null || true
echo "✓ On main branch"

echo ""
echo "📤 Pushing to GitHub..."
if git push -u origin main; then
    echo "✅ Push successful!"
else
    echo "❌ Push failed"
    exit 1
fi

echo ""
echo "✅ All done!"
echo ""
echo "📌 Next steps:"
echo "   1. Repository: https://github.com/Herp-Ops/port-discord-bot"
echo "   2. Deploy to Railway:"
echo "      - Go to https://railway.app"
echo "      - New project → Deploy from GitHub"
echo "      - Select Herp-Ops/port-discord-bot"
echo "      - Add env vars: DISCORD_TOKEN, PORT_API_TOKEN"
echo "      - Deploy!"
echo ""
echo "🎉 Done! Your bot will be live shortly."
