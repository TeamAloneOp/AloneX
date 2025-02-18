from pyrogram import filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid
)
import random
from logging import getLogger
from AloneX import LOGGER
from config import LOGGER_ID as LOG_GROUP_ID
from AloneX.misc import SUDOERS
from AloneX import app
from AloneX.helper.admin_check import admin_check, admin_filter
from config import OWNER_ID
from pyrogram.types import *
from pyrogram.types import ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
from pyrogram.enums import ChatType, ChatMemberStatus

LOGGER = getLogger(__name__)

kickpic = [
    "https://graph.org/file/210751796ff48991b86a3.jpg",
    "https://graph.org/file/7b4924be4179f70abcf33.jpg",
    "https://graph.org/file/f6d8e64246bddc26b4f66.jpg",
]

button = [
    [
        InlineKeyboardButton(
            text="\x41\x6C\x6F\x6E\x65\x20\x43\x6F\x64\x65\x72", url="\x68\x74\x74\x70\x73\x3A\x2F\x2F\x74\x2E\x6D\x65\x2F\x41\x6C\x6F\x6E\x65\x48\x75\x56\x61\x69"
        )
    ]
]

def mention(user, name, mention=True):
    if mention:
        return f"[{name}](tg://openmessage?user_id={user})"
    else:
        return f"[{name}](https://t.me/{user})"

async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
    except:
        return None
    return [user.id, user.first_name]

async def bans_user(user_id, first_name, admin_id, admin_name, chat_id, message):
    try:
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        return "I need ban rights to perform this action.", False
    except UserAdminInvalid:
        return "I can't ban another admin!", False
    except Exception as e:
        if user_id == OWNER_ID:
            return "Why should I ban myself? I'm not that silly!", False
        return f"An error occurred: {e}", False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)
    await app.send_message(LOG_GROUP_ID, f"{user_mention} was banned by {admin_mention} in {message.chat.title}")

    ban_message = await message.reply_photo(
        photo=random.choice(kickpic),
        caption=f"{user_mention} was banned by {admin_mention}."
        # reply_markup=InlineKeyboardMarkup(button)  # unban button chad de
    )
    return ban_message, True

@app.on_message(filters.command("ban") & admin_filter)
async def ban_user_with_unban_button(client, message):
    chat = message.chat
    chat_id = message.chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if not member.privileges.can_restrict_members:
            return await message.reply_text("You don't have permission to ban someone.")
    else:
        return await message.reply_text("You don't have permission to ban someone.")
        
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except ValueError:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj is None:
                return await message.reply_text("User not found.")
            user_id = user_obj[0]
            first_name = user_obj[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        return await message.reply_text("Please specify a valid user or reply to their message.")
        
    msg_text, result = await bans_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if not result:
        return await message.reply_text(msg_text)

    unban_button = [
        [InlineKeyboardButton("ƲɴʙᴀƝ ƲsᴇƦ", callback_data=f"unban_{user_id}")]
    ]
    await message.reply_text(
        f"Click below to unban {first_name}.",
        reply_markup=InlineKeyboardMarkup(unban_button),
    )

@app.on_message(filters.command("unban") & admin_filter)
async def unban_user(client, message):
    chat = message.chat
    chat_id = message.chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if not member.privileges.can_restrict_members:
            return await message.reply_text("You don't have permission to unban someone.")
    else:
        return await message.reply_text("You don't have permission to unban someone.")
        
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except ValueError:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj is None:
                return await message.reply_text("User not found.")
            user_id = user_obj[0]
            first_name = user_obj[1]
    else:
        return await message.reply_text("Please specify a valid user to unban.")
    
    try:
        await app.unban_chat_member(chat_id, user_id)
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        await message.reply_photo(
            photo=random.choice(kickpic),
            caption=f"{user_mention} was unbanned by {admin_mention}.",
            reply_markup=InlineKeyboardMarkup(button),
        )
        await app.send_message(LOG_GROUP_ID, f"{user_mention} was unbanned by {admin_mention} in {message.chat.title}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@app.on_callback_query(filters.regex(r"unban_(\d+)"))
async def unban_button_callback(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    chat_id = callback_query.message.chat.id
    try:
        await app.unban_chat_member(chat_id, user_id)
        await callback_query.answer("User has been unbanned!")
        await callback_query.message.edit_text("The user has been successfully unbanned.")
    except Exception as e:
        await callback_query.answer(f"An error occurred: {e}")

@app.on_message(filters.command("kickme") & filters.group)
async def kickme_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id

    try:
        await app.ban_chat_member(chat_id, user_id)
        await message.reply_photo(
            photo=random.choice(kickpic),
            caption=f"{user_name} has kicked themselves out of the group!",
            reply_markup=InlineKeyboardMarkup(button),
        )
        await app.send_message(LOG_GROUP_ID, f"{user_name} used the kickme command in {message.chat.title}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
