import asyncio
from pyrogram import Client, enums
from pyrogram.errors import UserNotParticipant, FloodWait
import config

UPDATES_CHANNEL = getattr(config, "UPDATES_CHANNEL", "SSBotsUpdates")
DEALS_CHANNEL = getattr(config, "DEALS_CHANNEL", "Tg_Shoping")

async def get_channel_invite(client: Client, channel_target):
    """Returns a valid link for a channel (public t.me link or created invite link)"""
    try:
        if str(channel_target).startswith("-100") or str(channel_target).lstrip("-").isdigit():
            chat = await client.get_chat(int(channel_target))
            if chat.username:
                return f"https://t.me/{chat.username}"
            invite = await client.create_chat_invite_link(int(channel_target))
            return invite.invite_link
        else:
            clean_name = str(channel_target).lstrip("@")
            return f"https://t.me/{clean_name}"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await get_channel_invite(client, channel_target)
    except Exception:
        clean_name = str(channel_target).lstrip("@")
        return f"https://t.me/{clean_name}"

async def check_membership(client: Client, channel_target, user_id: int) -> bool:
    """Checks if a user is joined in a specific channel"""
    if not channel_target:
        return True
    try:
        chat_id = int(channel_target) if (str(channel_target).startswith("-100") or str(channel_target).lstrip("-").isdigit()) else f"@{str(channel_target).lstrip('@')}"
        member = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
        if member.status in (enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.LEFT):
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"[FSUB NOTE] Channel check warning ({channel_target}): {e}")
        return True

async def check_fsub(client: Client, user_id: int):
    """Verifies both Updates and Deals channels"""
    updates_ok = await check_membership(client, UPDATES_CHANNEL, user_id)
    deals_ok = await check_membership(client, DEALS_CHANNEL, user_id)
    is_fully_joined = updates_ok and deals_ok
    return is_fully_joined, updates_ok, deals_ok

