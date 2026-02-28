from telethon import TelegramClient, events
import re

# Bot details
API_ID = 26978185 # Need to get this or use a dummy if not provided, but usually required for Telethon. 
# However, for a simple bot, python-telegram-bot or aiogram might be better if only using bot token.
# But the user mentioned "forwarding" which often implies UserBot if the bot is not an admin in the source.
# The user said "2 channel এর মধ্যে বট এডমিন আছে" (Bot is admin in both channels). 
# If the bot is admin, it can receive messages via standard bot API if privacy mode is off or it's a channel.
# Let's use `python-telegram-bot` or `aiogram`. Actually, `telethon` can also work as a bot.

# Given the requirements, I'll use `telethon` as it's versatile.
# For a bot, we only need API_ID and API_HASH which are standard for any Telegram app.
# Since the user only provided the Bot Token, I will use a common way to run it.
# Wait, Telethon needs API_ID/HASH. Maybe I should use `python-telegram-bot`.

import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8648013365:AAFP-Ea_BbnBPTpe0L6-C08VsPvQHw6AYnI"
SOURCE_CHANNEL_ID = -1003722624508
DEST_CHANNEL_ID = -1003824270566
USERNAME_TO_ADD = "Owner: @CEO_cryfex"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return
    
    channel_post = update.channel_post
    
    # Check if it's from the source channel
    if channel_post.chat_id != SOURCE_CHANNEL_ID:
        return

    # No links allowed
    if channel_post.entities:
        for entity in channel_post.entities:
            if entity.type in ['url', 'text_link']:
                return
    if channel_post.caption_entities:
         for entity in channel_post.caption_entities:
            if entity.type in ['url', 'text_link']:
                return

    text = channel_post.text or channel_post.caption or ""
    
    # Customizing the message
    lines = text.split('\n')
    market = ""
    time = ""
    timeframe = ""
    direction = ""
    is_win = "𝗪𝗜𝗡" in text
    is_loss = "𝗛𝗜𝗧 𝗚𝗔𝗟𝗘" in text
    
    for line in lines:
        if '💷' in line:
            market = line.replace('💷', '').strip()
        elif '⏳' in line:
            time = line.replace('⏳', '').strip()
        elif '⌚️' in line:
            timeframe = line.replace('⌚️', '').strip()
        elif any(d in line for d in ['🔴', '🟢', 'PUT', 'CALL']):
            direction = line.strip()
        elif '𝗪𝗜𝗡' in line or '𝗛𝗜𝗧 𝗚𝗔𝗟𝗘' in line:
            # Extract market and time from result message
            # Format: ✅  𝗪𝗜𝗡° ✅𝚄𝚂𝙳𝚃𝚁𝚈-𝙾𝚃𝙲𝚚 | ⏰ 𝟸𝟹:𝟻𝟼
            # Or: ☑️ 𝗛𝗜𝗧 𝗚𝗔𝗟𝗘 ☑️𝚄𝚂𝙳𝙿𝙺𝚁-𝙾𝚃𝙲𝚚 | ⏰ 𝟸𝟹:𝟺𝟿
            parts = line.split('|')
            if len(parts) > 1:
                time_part = parts[1].replace('⏰', '').strip()
                # Use regex to find the market name between indicators
                market_match = re.search(r'(?:✅|☑️|°)\s*([A-Z0-9-]+)', parts[0])
                if market_match:
                    market = market_match.group(1).strip()
                else:
                    # Fallback if regex fails
                    market_part = parts[0].split('✅')[-1].strip() if '✅' in parts[0] else parts[0].split('☑️')[-1].strip()
                    market = market_part.replace('°', '').strip()
                time = time_part

    if is_win:
        new_text = (
            "╔═══ 🟢 SIGNAL RESULT 🟢 ═══╗\n\n"
            f"✅ 𝗪𝗜𝗡 ➤ {market}\n\n"
            f"⏰ Entry Time ➤ {time}\n\n"
            "📈 Perfect Signal • Clean Profit 🔥\n\n"
            "👑 Join Vip up to 99% signel profit➜ @CEO_cryfex\n"
            "╚═━════════✦═══════━═╝"
        )
    elif is_loss:
        new_text = (
            "╔═══ 🔴 SIGNAL RESULT 🔴 ═══╗\n\n"
            f"❌ 𝗟𝗢𝗦𝗦 ➤ {market}\n\n"
            f"⏰ Entry Time ➤ {time}\n\n"
            "♻️ Recovery On Process ⚡\n\n"
            "📊 Next Signal Coming Soon\n"
            "╚═━═══════✦════════━═╝"
        )
    elif market and time:
        # Determine direction text and icon
        dir_label = "🔴 PUT ⬇️ DOWN"
        if 'CALL' in direction or '🟢' in direction:
            dir_label = "🟢 CALL ⬆️ UP"

        # Create new formatted message with the requested structure
        new_text = (
            "☂𝗦𝗢𝗣𝗡𝗢 𝗧𝗥𝗔𝗗𝗘𝗥•LIVE SIGNAL ☂\n\n"
            "💱 ╭─〔 𝗠𝗔𝗥𝗞𝗘𝗧 𝗣𝗔𝗜𝗥 〕─╮\n"
            f"     ➤  → 『 {market} 』\n"
            "      ╰────────────────✦\n\n"
            "⏰ ╭─〔 𝗘𝗡𝗧𝗥𝗬 𝗧𝗜𝗠𝗘 〕─╮\n"
            f"    ➤   ⌚  →  {time}\n"
            "      ╰───────◈──────╯\n\n"
            "⏳ ╭─〔 𝗧𝗥𝗔𝗗𝗘 𝗘𝗫𝗣𝗜𝗥𝗬 〕─╮\n"
            "        ➤ → 1 Minutes\n"
            "      ╰──────────────✦\n\n"
            "♻️ ╭─〔 𝗥𝗘𝗖𝗢𝗩𝗘𝗥𝗬 (𝗜𝗙 𝗟𝗢𝗦𝗦) 〕\n"
            "            ➤  ⚡ MTG→1\n"
            "      ╰──────────────✦\n\n"
            "📊 ╭─〔 𝗧𝗥𝗔𝗗𝗘 𝗗𝗜𝗥𝗘𝗖𝗧𝗜𝗢𝗡 〕─╮\n"
            f"       ➤ {dir_label}\n"
            "       ╰••┈┈┈┈┈✦✧✦┈┈┈┈┈••✦\n\n"
            "👑 Join Vip group ➜ @CEO_cryfex   \n"
            "╚═━═══════─═══════ ═━═╝"
        )
    else:
        # If it doesn't match the signal pattern, just append the owner info
        new_text = (
            f"{text}\n\n"
            "👑 Join Vip group ➜ @CEO_cryfex  \n"
            "╚═━════════─════════━═╝"
        )

    if channel_post.photo:
        await context.bot.send_photo(
            chat_id=DEST_CHANNEL_ID,
            photo=channel_post.photo[-1].file_id,
            caption=new_text
        )
    else:
        await context.bot.send_message(
            chat_id=DEST_CHANNEL_ID,
            text=new_text
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handle channel posts
    channel_handler = MessageHandler(filters.ChatType.CHANNEL, handle_message)
    application.add_handler(channel_handler)
    
    print("Bot is running...")
    application.run_polling()
