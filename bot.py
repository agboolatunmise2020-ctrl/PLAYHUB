import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Configuration
TOKEN = os.environ.get("BOT_TOKEN")
# Redirect link - using your bot link as the destination
HUB_LINK = "https://t.me/PlayzoneHub_bot"
SUPPORT_USER = "@maxpromarketer"

# 2. Keyboards
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🎮 Enter Play Zone")],
        [KeyboardButton("📝 Game Tips"), KeyboardButton("🎁 Exclusive Offers")],
        [KeyboardButton("⚖️ Privacy Policy"), KeyboardButton("🆘 Support")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def hub_inline_button():
    keyboard = [[InlineKeyboardButton("🚀 Join Play Zone Hub", url=HUB_LINK)]]
    return InlineKeyboardMarkup(keyboard)

# 3. Logic Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Neutral, educational welcome message for Ad Approval
    welcome_text = (
        "👋 *Welcome to the Play Zone Hub!*\n\n"
        "Your central source for digital entertainment, daily games, and strategic tips. "
        "Discover new ways to play and stay updated with our latest community offers.\n\n"
        "Join thousands of players and start exploring today!"
    )
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown', 
        reply_markup=main_menu_keyboard()
    )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🎮 Enter Play Zone":
        await update.message.reply_text(
            "✅ *Access Granted.*\n\nClick below to enter the Hub and explore our current collection of games and promotions:",
            reply_markup=hub_inline_button(),
            parse_mode='Markdown'
        )

    elif text == "📝 Game Tips":
        msg = (
            "📝 *Gaming Insights & Tips*\n\n"
            "Boost your performance with our daily insights:\n"
            "• Optimized gameplay strategies\n"
            "• Understanding game mechanics\n"
            "• Community-voted top picks"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "🎁 Exclusive Offers":
        msg = (
            "🎁 *Community Promotions*\n\n"
            "We regularly update our offers to bring more fun to our players. "
            "Check the Play Zone Hub daily for exclusive limited-time rewards!"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text(
            "Play Zone Hub values your privacy. We do not share user data or personal information. "
            "Enjoy a secure entertainment experience."
        )

    elif text == "🆘 Support":
        await update.message.reply_text(
            f"Need assistance with the hub or our services?\n\n"
            f"Contact Support: {SUPPORT_USER}"
        )

# --- ASYNC MAIN FOR PYTHON 3.14 (Render Background Worker) ---
async def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN variable is missing!")
        return

    print("Play Zone Hub starting...")
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
