import asyncio

from pyrogram import filters, Client
from pyrogram.types import ChatMemberUpdated, Message

from base.client_base import user
from solidAPI.chat import add_chat, del_chat, get_chat
from solidAPI import get_message as gm


@Client.on_chat_member_updated(filters.group)
async def on_bot_added(client: Client, msg: ChatMemberUpdated):
    bot_id = (await client.get_me()).id
    chat_id = msg.chat.id
    members_id = msg.new_chat_member.user.id
    lang = msg.new_chat_member.invited_by.language_code
    if members_id == bot_id:
        x = get_chat(chat_id)
        if not x:
            return add_chat(chat_id, lang if lang else "en")
        return


@Client.on_message(filters=filters.left_chat_member)
async def on_bot_kicked(client: Client, msg: Message):
    bot_id = (await client.get_me()).id
    chat_id = msg.chat.id
    members = msg.left_chat_member
    if members.id == bot_id:
        del_chat(chat_id)
        await user.send_message(chat_id, gm(chat_id, "bot_leave_from_chat"))
        await asyncio.sleep(3)
        await user.leave_chat(chat_id)
        return
