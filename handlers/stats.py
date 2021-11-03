import os
from platform import system, machine
from psutil import virtual_memory, disk_usage
from sys import version as python_version
from pytgcalls import __version__ as pytgcalls_version
from pyrogram import Client, filters, types, __version__ as pyrogram_version
from utils.decorators import authorized_only
from utils.functions import group_only
from solidAPI.other import get_stats, get_message as gm


@Client.on_message(filters.command("gstats") & group_only)
@authorized_only
async def gstats_(client: Client, message: types.Message):
    chat_id = message.chat.id
    bot_me = await client.get_me()
    bot_fullname = (
        bot_me.first_name
        if bot_me.first_name.endswith("bot")
        else f"{bot_me.first_name} bot"
    )
    msg = await message.reply(f"🔄 **{gm(chat_id, 'getting_global_stats')}**")
    chats, pm = get_stats()
    ram = f"{round(virtual_memory().total / (1024.0 ** 3))} GB"
    hdd = disk_usage("/")
    total = str(hdd.total / (1024.0 ** 3))
    used = str(hdd.used / (1024.0 ** 3))
    free = str(hdd.free / (1024.0 ** 3))
    mods = []
    for path in os.listdir("handlers"):
        if path.startswith("__"):
            pass
        else:
            mods.append(path)
    msgs = gm(chat_id, "global_stats_details").format(
        bot_fullname,
        system(),
        machine(),
        used[:4],
        total[:4],
        free[:4],
        ram,
        python_version.split()[0],
        pyrogram_version,
        pytgcalls_version,
        len(mods),
        chats,
        pm,
    )
    await msg.edit(msgs, disable_web_page_preview=True)
