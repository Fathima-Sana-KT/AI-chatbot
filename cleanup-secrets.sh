#!/bin/bash

echo "🔍 Step 1: Installing BFG if not already installed..."
brew install bfg

echo "📦 Step 2: Creating backup..."
git clone --mirror . ../chatbot-backup.git

echo "🧨 Step 3: Removing all .env files from history using BFG..."
bfg --delete-files .env

echo "🧹 Step 4: Cleaning reflog and garbage..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "🛡️ Step 5: Adding .env to .gitignore..."
echo "*.env" >> .gitignore
git add .gitignore

echo "📄 Step 6: Creating .env.example in backend/..."
mkdir -p backend
cat > backend/.env.example <<EOL
API_KEY=your_api_key_here
MODEL_NAME=gpt-neo
PORT=8000
EOL

git add backend/.env.example
git commit -m "Remove .env and add .env.example + .gitignore"

echo "🚀 Step 7: Force pushing cleaned repository to GitHub..."
git push --force --set-upstream origin main

echo "✅ All done! If any secrets were previously pushed, please revoke them immediately."