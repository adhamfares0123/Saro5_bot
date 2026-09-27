import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("8905309308:AAF-gBzQEvmmUajPkn63lC4alHr2O_UzGeY")
CHANNEL = "@A0ha0"
CHANNEL_LINK = "https://t.me/A0ha0"
DEVELOPER = "@adha0n"
OWNER_ID = 7758427502

GAMES = {
    "pubg": "PUBG Mobile",
    "freefire": "Free Fire",
    "valorant": "Valorant",
    "fortnite": "Fortnite",
    "efootball": "eFootball",
    "roblox": "Roblox",
    "cod": "Call of Duty",
    "genshin": "Genshin Impact",
    "coc": "Clash of Clans",
    "cr": "Clash Royale",
    "ludo": "Ludo King",
    "pool": "8 Ball Pool"
}

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(CHANNEL, update.effective_user.id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message or (update.callback_query.message if update.callback_query else None)

    if not await check_join(update, context):
        kb = [
            [InlineKeyboardButton("اشترك في القناة 📢", url=CHANNEL_LINK)],
            [InlineKeyboardButton("تحققت من الاشتراك ✅", callback_data="check")]
        ]
        text = f"يا هلا {user.first_name} 👋\nلازم تشترك في قناة {CHANNEL} الاول عشان تستخدم البوت 🔒"
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    kb = [
        [InlineKeyboardButton("PUBG", callback_data="pubg"), InlineKeyboardButton("Free Fire", callback_data="freefire")],
        [InlineKeyboardButton("Valorant", callback_data="valorant"), InlineKeyboardButton("Fortnite", callback_data="fortnite")],
        [InlineKeyboardButton("eFootball", callback_data="efootball"), InlineKeyboardButton("Roblox", callback_data="roblox")],
        [InlineKeyboardButton("COD", callback_data="cod"), InlineKeyboardButton("Genshin", callback_data="genshin")],
        [InlineKeyboardButton("Clash of Clans", callback_data="coc"), InlineKeyboardButton("Clash Royale", callback_data="cr")],
        [InlineKeyboardButton("Ludo", callback_data="ludo"), InlineKeyboardButton("8 Ball Pool", callback_data="pool")],
        [InlineKeyboardButton(f"المطور {DEVELOPER} 👨‍💻", url=f"https://t.me/{DEVELOPER.replace('@','')}")]
    ]
    txt = f"أهلا {user.first_name} ✨\nاختار لعبتك من القائمة تحت 👇\nID: <code>{user.id}</code>"

    if update.callback_query:
        await update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    else:
        await message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")

async def btn_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "check":
        await start(update, context)
        return
    
    name = GAMES.get(q.data, q.data)
    kb = [
        [InlineKeyboardButton(f"شحن {name} 💳", url=f"{CHANNEL_LINK}?start={q.data}")],
        [InlineKeyboardButton("رجوع للقائمة 🔙", callback_data="check")]
    ]
    await q.edit_message_text(f"اخترت: {name} 🎮", reply_markup=InlineKeyboardMarkup(kb))

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn_handler))
    print(f"البوت شغال... المطور {DEVELOPER} - القناة {CHANNEL}")
    app.run_polling()
