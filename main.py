# app/main.py
import os
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from telegram import Bot, Update, InputFile
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_BASE, SECRET_PATH, TEMP_DIR
from downloader import download_video, download_audio, cleanup_file
from pathlib import Path

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

@app.post(SECRET_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    asyncio.create_task(handle_update(update))
    return {"ok": True}

async def handle_update(update: Update):
    try:
        if update.message is None:
            return
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        text = update.message.text or ""
        if text.startswith("/start"):
            await bot.send_message(chat_id, "Send me a YouTube link and I'll give download options.")
            return

        # Force subscribe check (best-effort)
        try:
            member = await bot.get_chat_member(CHANNEL_ID, user_id)
            if getattr(member, 'status', '') in ["left", "kicked"]:
                invite = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
                await bot.send_message(chat_id,
                    f"Please join our channel first: {invite.invite_link}\nThen send the link again.")
                return
        except Exception:
            await bot.send_message(chat_id, f"Please join {CHANNEL_ID} and then re-send the link.")
            return

        url = text.strip()
        kb = [
            [{"text":"Video 144p", "callback_data": f"video|144|{url}"},
             {"text":"Video 360p", "callback_data": f"video|360|{url}"}],
            [{"text":"Video 480p", "callback_data": f"video|480|{url}"},
             {"text":"Video 720p", "callback_data": f"video|720|{url}"}],
            [{"text":"Audio (MP3)", "callback_data": f"audio|0|{url}"}],
        ]
        await bot.send_message(chat_id, "Choose format:", reply_markup={"inline_keyboard": kb})
    except Exception as e:
        print("handle_update error:", e)

@app.post(SECRET_PATH + "/callback")
async def callback(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    if update.callback_query:
        cq = update.callback_query
        chat_id = cq.message.chat.id
        await bot.answer_callback_query(cq.id, text="Preparing your file, please wait...")
        payload = cq.data
        typ, height_str, url = payload.split("|", 2)
        try:
            if typ == "video":
                max_h = int(height_str)
                path = download_video(url, max_h)
                with open(path, 'rb') as f:
                    await bot.send_video(chat_id=chat_id, video=InputFile(f))
                cleanup_file(path)
            else:
                path = download_audio(url)
                with open(path, 'rb') as f:
                    await bot.send_audio(chat_id=chat_id, audio=InputFile(f))
                cleanup_file(path)
        except Exception as e:
            await bot.send_message(chat_id, f"Error: {e}")
    return {"ok": True}
