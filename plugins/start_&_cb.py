import random
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep
from helper.utils import is_req_subscribed, is_subscribed, log_error
import asyncio

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        await message.react(emoji="🔥", big=True)
    except:
        pass
    m = await message.reply_text("⏳")
    await asyncio.sleep(0.4)
    await m.delete() 
    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    await db.add_user(client, message)
    # user_id = message.from_user.id
    # AUTH_CHANNEL = Config.AUTH_CHANNEL
    # AUTH_CHANNELS = Config.AUTH_CHANNELS
    # AUTH_REQ_CHANNELS = Config.AUTH_REQ_CHANNELS
    # FSUB_PICS = Config.FSUB_PICS
    # btn = []
    # if AUTH_CHANNEL:
    #     try:
    #         btn = await is_subscribed(client, message, AUTH_CHANNEL)
    #         if btn:
    #             username = (await client.get_me()).username
    #             if message.command[1]:
    #                 btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
    #             else:
    #                 btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
    #         reply_markup = InlineKeyboardMarkup(btn)
    #         photo = random.choice(FSUB_PICS) if FSUB_PICS else "https://graph.org/file/7478ff3eac37f4329c3d8.jpg"
    #         caption = (
    #             f"👋 ʜᴇʟʟᴏ {message.from_user.mention}\n\n"
    #             "🛑 ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\n"
    #             "👉 ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ʙᴇʟᴏᴡ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ."
    #         )
    #         await message.reply_photo(
    #             photo=photo,
    #             caption=caption,
    #             reply_markup=reply_markup,
    #             parse_mode=enums.ParseMode.HTML
    #         )
    #         return

    #     except Exception as e:
    #         await log_error(client, f"❗️ Force Sub Error:\n\n{repr(e)} {AUTH_CHANNEL}")
    #         logger.error(f"❗️ Force Sub Error:\n\n{repr(e)}")
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '🍁 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/MrBrutal_Bots'),
        InlineKeyboardButton(
            '🌿 Sᴜᴩᴩᴏʀᴛ', url='https://t.me/MrBrutal_Support')
    ], [
        InlineKeyboardButton('👨‍🏭 Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('❗ Hᴇʟᴩ', callback_data='help')
    ]                         
    ])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):    
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    if not Config.STRING_SESSION:
        if file.file_size > 2000 * 1024 * 1024:
            return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ")

    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    '🍁 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/MrBrutal_Bots'),
                InlineKeyboardButton(
                    '🌿 Sᴜᴩᴩᴏʀᴛ', url='https://t.me/MrBrutal_Support')
            ], [
                InlineKeyboardButton('💁‍♂️ Aʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('❗ Hᴇʟᴩ', callback_data='help')
            ]                             
            ])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")
            ]])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")
            ]])
        )

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
