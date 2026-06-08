#!/bin/bash
cd "/Users/cashify/Desktop/jf_bot_deploy"
echo "Staging changes..."
git add .
echo "Committing changes..."
git commit -m "Update products edit modal, support modal, key management modal, mobile styling and bot integrations"
echo "Pushing to GitHub..."
git push
echo "Deployment push complete!"
