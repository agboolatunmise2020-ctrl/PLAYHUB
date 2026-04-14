import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Configuration
TOKEN = os.environ.get("BOT_TOKEN")

# 2. Keyboards - Purely internal educational navigation
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🎮 Game Mechanics"), KeyboardButton("📝 Strategy Guides")],
        [KeyboardButton("🛡️ Fair Play Rules"), KeyboardButton("⚖️ Privacy Policy")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 3. Logic Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to the Play Zone Hub!*\n\n"
        "Your dedicated educational tool for mastering game mechanics and strategies. "
        "Our goal is to help you improve your skills through data-driven tips and fair play guides.\n\n"
        "Select a category below to start learning!"
    )
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown', 
        reply_markup=main_menu_keyboard()
    )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🎮 Game Mechanics":
        msg = (
            "⚙️ *Understanding Game Mechanics*\n\n"
            "Mastering the 'rules of the engine' is the first step to winning. We analyze:\n"
            "• Physics and movement timing\n"
            "• Resource management loops\n"
            "• Probability and RNG factors"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "📝 Strategy Guides":
        msg = (
            "📝 *Advanced Strategy Guides*\n\n"
            "Elevate your playstyle with these core concepts:\n"
            "• Map awareness and positioning\n"
            "• Effective counter-play techniques\n"
            "• Long-term vs. Short-term objectives"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "🛡️ Fair Play Rules":
        msg = (
            "🛡️ *Fair Play & Ethics*\n\n"
            "A sustainable gaming community relies on integrity:\n"
            "1. Respect all players.\n"
            "2. Avoid unauthorized third-party tools.\n"
            "3. Report bugs to help improve the experience for everyone."
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text(
            "Play Zone Hub is an educational tool. We do not collect, store, or share any personal user data."
        )

# --- ASYNC MAIN FOR RENDER WORKER ---
async def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN is missing!")
        return

    print("Play Zone Hub Educational Bot starting...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    async with application:
        await application.initialize()
        await application.start()
        print("Bot is now polling...")
        await application.updater.start_polling(drop_pending_updates=True)
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
