import math
import logging
from pyrogram import enums
import time
from datetime import datetime
from pytz import timezone
from config import Config, Txt
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
import re

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def log_error(client, error_message):
    LOG_CHANNEL = Config.LOG_CHANNEL
    try:
        await client.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"<b>⚠️ Error Log:</b>\n<code>{error_message}</code>"
        )
    except Exception as e:
        print(f"Failed to log error: {e}")
        
async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start

    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time, time_to_completion, estimated_total_time = calculate_times(
            diff, current, total, speed
        )

        progress = generate_progress_bar(percentage)
        tmp = progress + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )

        try:
            await message.edit(text=f"{ud_type}\n\n{tmp}")
        except:
            pass


def generate_progress_bar(percentage):
    return (
        "".join(["⬢" for _ in range(math.floor(percentage / 5))])
        + "".join(["⬡" for _ in range(20 - math.floor(percentage / 5))])
    )


def calculate_times(diff, current, total, speed):
    elapsed_time = TimeFormatter(milliseconds=round(diff) * 1000)
    time_to_completion = TimeFormatter(round((total - current) / speed) * 1000)
    estimated_total_time = elapsed_time + time_to_completion
    return elapsed_time, time_to_completion, estimated_total_time


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}ʙ"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{days}ᴅ, ") if days else ""
    ) + (
        (f"{hours}ʜ, ") if hours else ""
    ) + (
        (f"{minutes}ᴍ, ") if minutes else ""
    ) + (
        (f"{seconds}ꜱ, ") if seconds else ""
    ) + (
        (f"{milliseconds}ᴍꜱ, ") if milliseconds else ""
    )
    return tmp[:-2]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime("%d %B, %Y")
        time_str = curr.strftime("%I:%M:%S %p")
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"Uꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\n"
            f"Dᴀᴛᴇ: {date}\nTɪᴍᴇ: {time_str}\n\nBy: {b.mention}",
        )

def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.\w+)?$'
    match = re.search(pattern, input_string)
    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''
        if prefix == None:
            if suffix == None:
                return f"{filename}{extension}"
            return f"{filename} {suffix}{extension}"
        elif suffix == None:
            if prefix == None:
               return f"{filename}{extension}"
            return f"{prefix}{filename}{extension}"
        else:
            return f"{prefix}{filename} {suffix}{extension}"


    else:
        return input_string


async def is_req_subscribed(bot, user_id, rqfsub_channels):
    btn = []
    for channel_id in rqfsub_channels:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status != enums.ChatMemberStatus.BANNED:
                continue
            else:
                await bot.send_message(user_id, text="Sorry, You are banned.")
        except UserNotParticipant:
            pass
        except Exception as e:
            logger.error(f"Error checking membership in {channel_id}: {e}")

        try:
            chat   = await bot.get_chat(channel_id)
            invite = await bot.create_chat_invite_link(
                channel_id,
                creates_join_request=True
            )
            btn.append([InlineKeyboardButton(f"⛔️ Join {chat.title}", url=invite.invite_link)])
        except ChatAdminRequired:
            logger.warning(f"Bot not admin in {channel_id}")
        except Exception as e:
            logger.warning(f"Invite link error for {channel_id}: {e}")

    return btn


async def is_subscriber(bot, user_id, fsub_channels):
    btn = []
    user_id = int(user_id)
    for channel_id in fsub_channels:
        chat = await bot.get_chat(int(channel_id))
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)])
        except Exception as e:
            logger.error(f"Error checking membership in {channel_id}: {e}")
    return btn

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)])
        except Exception as e:
            pass
    return btn