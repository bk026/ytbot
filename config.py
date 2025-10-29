# app/config.py
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # must be set in Render environment
CHANNEL_ID = os.getenv("CHANNEL_ID", "@YourChannelUsername")  # set your channel username or numeric id in Render
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE", "https://your-render-service.onrender.com")
SECRET_PATH = os.getenv("SECRET_PATH", "/webhook")  # using simple /webhook per your choice
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/ytbot")
