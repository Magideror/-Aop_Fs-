import asyncio
from Music.filters import command
import math
import os
import time
from random import randint
from urllib.parse import urlparse
import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
import re
import sys
from os import getenv
from yt_dlp import YoutubeDL
from Music import ( dbb, app, BOT_USERNAME, BOT_ID, BOT_NAME, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION,)
ydl_opts = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}
DEV_BOT = getenv("DEV_BOT")

@Client.on_message(command(["song", f"song@{BOT_USERNAME}", f"بحث@{BOT_USERNAME}", "بحث"]) & ~filters.edited)
def song(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("🔎 جار البحث ...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
    except Exception as e:
        m.edit("❌ song not found.\n\nplease give a valid song name.")
        print(str(e))
        return
    m.edit("📥 جار تحميل الملف...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎧 تم التحميل بواسطة @{BOT_USERNAME}\n\nمطور البوت @{DEV_BOT}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 جار رفع الملف...")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit("❌ error, wait for bot owner to fix")
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton(
                        "الدعم ☆", url=f"https://t.me/{GROUP}"),
                   InlineKeyboardButton(
                        "القناه ☆", url=f"https://t.me/{CHANNEL}"),
                ],[
                   InlineKeyboardButton(
                        "اضف البوت الي مجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ],
            ]
        ),
