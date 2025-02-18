from AloneX import app
import config
from config import LOGGER_ID as LOG_GROUP_ID
from pyrogram import Client, filters
from pyrogram.errors import RPCError, ChatAdminRequired
from pyrogram.types import ChatMemberUpdated
from datetime import datetime


@app.on_chat_member_updated(filters.group, group=10)
async def member_has_joined(client: Client, member: ChatMemberUpdated):
    try:
        if member.new_chat_member and member.new_chat_member.user:
            user = member.new_chat_member.user

            if user.is_bot:
                return

            join_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            welcome_message = f"Welcome aboard, {user.mention}! We're thrilled to have you here."

            await client.send_message(
                chat_id=member.chat.id,
                text=welcome_message
            )

            log_message = f"""
            New Member Joined:

            Name: {user.first_name} {user.last_name if user.last_name else ""}
            Username: @{user.username if user.username else 'No username'}
            User ID: {user.id}
            Join Time: {join_time}
            Group Name: {member.chat.title}  
            Group Link: {member.chat.invite_link if member.chat.invite_link else 'No invite link'}
            """
            await client.send_message(
                chat_id=LOG_GROUP_ID,
                text=log_message
            )

    except ChatAdminRequired:
        print("Bot lacks permission to send messages or access profile photos.")
    except RPCError as e:
        print(f"Error: {e}")

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: Client, member: ChatMemberUpdated):
    try:
        if member.old_chat_member and member.old_chat_member.user:
            user = member.old_chat_member.user

            if user.is_bot:
                return

            leave_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            goodbye_message = f"Goodbye, {user.mention}! We'll miss you. Take care!"

            await client.send_message(
                chat_id=member.chat.id,
                text=goodbye_message
            )

            log_message = f"""
            Member Left:

            Name: {user.first_name} {user.last_name if user.last_name else ""}
            Username: @{user.username if user.username else 'No username'}
            User ID: {user.id}
            Leave Time: {leave_time}
            Group Name: {member.chat.title} 
            Group Link: {member.chat.invite_link if member.chat.invite_link else 'No invite link'}
            """
            await client.send_message(
                chat_id=LOG_GROUP_ID,
                text=log_message
            )

    except ChatAdminRequired:
        print("Bot lacks permission to send messages or access profile photos.")
    except RPCError as e:
        print(f"Error: {e}")
