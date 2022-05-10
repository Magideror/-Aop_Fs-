import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from Music.config import get_queue
from Music.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message

from Music import SUDOERS, app, db_mem, userbot
from Music.MusicUtilities.database import get_active_chats, is_active_chat
from Music.MusicUtilities.helpers.checker import checker, checkerCB

from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
import os
import time
from os import path
import random
import asyncio
import shutil
from pytube import YouTube
from yt_dlp import YoutubeDL
from Music import converter
import yt_dlp
import shutil
import psutil
import re
import sys
from os import getenv
from Music.filters import command
from typing import Callable
from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from sys import version as pyver
from Music import (
    dbb,
    app,
    BOT_USERNAME,
    BOT_ID,
    BOT_NAME,
    ASSID,
    ASSNAME,
    ASSUSERNAME,
    ASSMENTION,
)
from Music.MusicUtilities.tgcallsrun import (
    music,
    convert,
    download,
    clear,
    get,
    is_empty,
    put,
    task_done,
    ASS_ACC,
)
from Music.MusicUtilities.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Music.MusicUtilities.database.onoff import (
    is_on_off,
    add_on,
    add_off,
)
from Music.MusicUtilities.database.chats import (
    get_served_chats,
    is_served_chat,
    add_served_chat,
    get_served_chats,
)
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    play_markup,
    playlist_markup,
    audio_markup,
    play_list_keyboard,
)
from Music.MusicUtilities.database.blacklistchat import (
    blacklisted_chats,
    blacklist_chat,
    whitelist_chat,
)
from Music.MusicUtilities.database.gbanned import (
    get_gbans_count,
    is_gbanned_user,
    add_gban_user,
    add_gban_user,
)
from Music.MusicUtilities.database.theme import (
    _get_theme,
    get_theme,
    save_theme,
)
from Music.MusicUtilities.database.assistant import (
    _get_assistant,
    get_assistant,
    save_assistant,
)
from Music.config import DURATION_LIMIT
from Music.MusicUtilities.helpers.decorators import authorized_users_only
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import (
    get_url,
    themes,
    random_assistant,
    ass_det,
)
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup2,
    search_markup,
)
from pyrogram import filters
from typing import Union
import subprocess
from asyncio import QueueEmpty
import shutil
import os
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

loop = asyncio.get_event_loop()

__MODULE__ = "Join/Leave"
__HELP__ = """
**Note:**
Only for Sudo Users
/joinassistant [Chat Username or Chat ID]
- Join assistant to a group.
/leaveassistant [Chat Username or Chat ID]
- Assistant will leave the particular group.
/leavebot [Chat Username or Chat ID]
- Bot will leave the particular chat.
"""

@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("Please Wait... Getting Queue..")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"Nothing in Queue")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**Queued List**\n\n"
        msg += "**Currently Playing:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚By:- {user_name}"
        msg += f"\n   ╚Duration:- Remaining `{dur_left}` out of `{duration_min}` Mins."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**Up Next In Queue:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️{name}"
                msg += f"\n   ╠Duration : {dur}"
                msg += f"\n   ╚Requested by : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**OUTPUT:**\n\n`Queued List`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"Tidak ada dalam Antrian")


@Client.on_message(command(["calls", f"calls@{BOT_USERNAME}", f"اونلاين@{BOT_USERNAME}", "اونلاين"]) & ~filters.edited)
async def active_group_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"🚫 error: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except BaseException:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            data = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{data}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ no active group calls")
    else:
        await message.reply_text(
            f"✏️ **Running Group Call List:**\n\n{text}\n❖ This is the list of all current active group call in my database.",
            disable_web_page_preview=True,
        )

@Client.on_message(filters.command("انضم") & filters.user(SUDOERS))
async def basffy(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Penggunaan:**\n/joinassistant [Nama Pengguna Obrolan atau ID Obrolan]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        return
    await message.reply_text("Bergabung.")
    
@Client.on_message(filters.command("غادر") & filters.user(SUDOERS))
async def baujaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Penggunaan:**\n/leave [Nama Pengguna Obrolan atau ID Obrolan]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        return
    await message.reply_text("Keluar.")

@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]) & ~filters.edited)
async def leave_all(c: Client, message: Message):
    if message.from_user.id not in SUDO_USERS:
        return
    run_1 = 0
    run_2 = 0
    msg = await message.reply("🔄 Userbot started leaving all groups")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            await remove_active_chat(dialog.chat.id)
            run_1 += 1
            await msg.edit(
                f"Userbot leaving...\n\nLeft from: {run_1} chats.\nFailed in: {run_2} chats."
            )
        except Exception:
            run_2 += 1
            await msg.edit(
                f"Userbot leaving...\n\nLeft from: {run_1} chats.\nFailed in: {run_2} chats."
            )
        await asyncio.sleep(0.7)
    await msg.delete()
    await client.send_message(
        message.chat.id, f"✅ Left from: {run_2} chats.\n❌ Failed in: {run_2} chats."
    )


@app.on_message(filters.command("leavebot") & filters.user(SUDOERS))
async def baaaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Penggunaan:**\n/leavebot [Nama Pengguna Obrolan atau ID Obrolan]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        print(e)
        return
    await message.reply_text("Bot telah berhasil meninggalkan obrolan")

