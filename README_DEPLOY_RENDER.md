# ytbot — Deploy on Render.com (Quick guide)

## Before deploy
1. Create a Git repository and push this project.
2. In Render, create a **New → Web Service** and connect your repo.

## Render settings
- Choose **Environment**: Docker
- Build command: (Render will use Dockerfile)
- Start command: (Docker CMD used)

## Environment variables (set in Render dashboard)
- BOT_TOKEN = <your Telegram bot token>
- CHANNEL_ID = <@YourChannelUsername or numeric id>
- WEBHOOK_BASE = https://your-render-service.onrender.com  (replace with actual Render service URL)
- SECRET_PATH = /webhook
- TEMP_DIR = /tmp/ytbot

## After deploy
1. Get your Render service URL (https://your-service.onrender.com)
2. Set Telegram webhook (replace <TOKEN> and path):
   ```
   curl -F "url=https://your-service.onrender.com/webhook" https://api.telegram.org/bot<TOKEN>/setWebhook
   ```
3. Test: send /start, then a YouTube link.

## Notes
- Make sure your bot is admin in the channel if you want force-join checks to work.
- Large files may require special handling (upload to S3 and send link).
- Keep BOT_TOKEN secret.
