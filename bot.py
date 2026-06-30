import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please add BOT_TOKEN in Railway Variables tab")
    exit(1)

print(f"✅ Token loaded successfully (length: {len(TOKEN)})")

# ===== Helper Functions =====
def count_words(text: str) -> int:
    return len(text.split())

def count_characters(text: str) -> int:
    return len(text)

def count_characters_no_spaces(text: str) -> int:
    return len(text.replace(" ", ""))

def count_sentences(text: str) -> int:
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def count_paragraphs(text: str) -> int:
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def estimate_reading_time(word_count: int) -> str:
    if word_count == 0:
        return "0 seconds"
    minutes = word_count / 200
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    else:
        return f"{minutes:.1f} minute{'s' if minutes != 1 else ''}"

# ===== Command Handlers =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        f"✍️ *Hello {user.first_name}!*\n\n"
        "Welcome to *ScribeCountBot* - your text analysis companion!\n\n"
        "📊 *What I can do:*\n"
        "• Count words, characters, sentences\n"
        "• Count paragraphs and estimate reading time\n\n"
        "🔹 *How to use:*\n"
        "Just send me any text, and I'll analyze it!\n"
        "Send /help to see all commands."
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *ScribeCountBot Help*\n\n"
        "*Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help\n\n"
        "*Text Analysis:*\n"
        "Simply send any text message and I'll provide:\n"
        "• Word count\n"
        "• Character count (with and without spaces)\n"
        "• Sentence count\n"
        "• Paragraph count\n"
        "• Estimated reading time"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats_text = (
        "📊 *Bot Statistics*\n\n"
        "This bot is powered by:\n"
        "• Python\n"
        "• python-telegram-bot library\n"
        "• Deployed on Railway\n\n"
        "⚡ *Features:*\n"
        "• Real-time text analysis\n"
        "• Accurate counting algorithms\n"
        "• Fast response time"
    )
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "📝 *About ScribeCountBot*\n\n"
        "This bot was created to help writers, students, and professionals "
        "quickly analyze text for word and character counts.\n\n"
        "*Why ScribeCountBot?*\n"
        "✓ Simple and fast\n"
        "✓ No registration needed\n"
        "✓ Privacy-focused (we don't store your text)\n"
        "✓ Free to use\n\n"
        "Built with ❤️ using open-source tools."
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

# ===== Message Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text.startswith('/'):
        return
    
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to analyze!")
        return
    
    word_count = count_words(text)
    char_count = count_characters(text)
    char_no_space = count_characters_no_spaces(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    reading_time = estimate_reading_time(word_count)
    
    response = (
        f"📊 *Text Analysis Results*\n"
        f"{'─' * 25}\n"
        f"📝 *Words:* {word_count:,}\n"
        f"🔤 *Characters:* {char_count:,}\n"
        f"⬜ *Characters (no spaces):* {char_no_space:,}\n"
        f"📄 *Sentences:* {sentence_count:,}\n"
        f"📑 *Paragraphs:* {paragraph_count:,}\n"
        f"⏱️ *Reading time:* {reading_time}\n"
        f"{'─' * 25}\n"
        f"📎 *Text preview:*\n"
        f"`{text[:100]}{'...' if len(text) > 100 else ''}`"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ Error: {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")

# ===== Main Function =====
def main():
    print("🚀 Starting ScribeCountBot...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application built successfully")
        
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running! Waiting for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
