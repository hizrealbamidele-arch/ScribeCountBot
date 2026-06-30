import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Get token from environment variable (secure for Railway)
TOKEN = os.environ.get("BOT_TOKEN", "")

# If no token is set, show error
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# ===== Helper Functions =====
def count_words(text: str) -> int:
    """Count words in text (splits by whitespace)"""
    return len(text.split())

def count_characters(text: str) -> int:
    """Count total characters including spaces"""
    return len(text)

def count_characters_no_spaces(text: str) -> int:
    """Count characters excluding spaces"""
    return len(text.replace(" ", ""))

def count_sentences(text: str) -> int:
    """Count sentences using ., !, ? as delimiters"""
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def count_paragraphs(text: str) -> int:
    """Count paragraphs by splitting on double newlines"""
    paragraphs = text.split('\n\n')
    # Filter out empty paragraphs
    paragraphs = [p for p in paragraphs if p.strip()]
    return len(paragraphs)

def estimate_reading_time(word_count: int) -> str:
    """Estimate reading time (200 words per minute avg)"""
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
    """Handle /start command"""
    user = update.effective_user
    welcome_message = (
        f"✍️ *Hello {user.first_name}!*\n\n"
        "Welcome to *ScribeCountBot* - your text analysis companion!\n\n"
        "📊 *What I can do:*\n"
        "• Count words, characters, sentences\n"
        "• Count paragraphs and estimate reading time\n"
        "• Support for multiple text formats\n\n"
        "🔹 *How to use:*\n"
        "Just send me any text, and I'll analyze it!\n"
        "You can also forward messages to me.\n\n"
        "Send /help to see all commands."
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📖 *ScribeCountBot Help*\n\n"
        "*Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/stats - Show bot statistics\n"
        "/about - About this bot\n\n"
        "*Text Analysis:*\n"
        "Simply send any text message and I'll provide:\n"
        "• Word count\n"
        "• Character count (with and without spaces)\n"
        "• Sentence count\n"
        "• Paragraph count\n"
        "• Estimated reading time\n\n"
        "*Tips:*\n"
        "• Send long texts for detailed analysis\n"
        "• Forward articles or documents\n"
        "• Works with any language!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    # This is a simple version - you can expand with database later
    stats_text = (
        "📊 *Bot Statistics*\n\n"
        "This bot is powered by:\n"
        "• Python 3.x\n"
        "• python-telegram-bot library\n"
        "• Deployed on Railway\n\n"
        "⚡ *Features:*\n"
        "• Real-time text analysis\n"
        "• Accurate counting algorithms\n"
        "• Fast response time"
    )
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
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
    """Handle incoming text messages"""
    # Get the text from the message
    text = update.message.text
    
    # Check if it's a command (handled elsewhere)
    if text.startswith('/'):
        return
    
    # If the message is too short
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to analyze!")
        return
    
    # Perform calculations
    word_count = count_words(text)
    char_count = count_characters(text)
    char_no_space = count_characters_no_spaces(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    reading_time = estimate_reading_time(word_count)
    
    # Format the response with a nice layout
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
    
    # Send the result
    await update.message.reply_text(response, parse_mode='Markdown')

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates"""
    print(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")

# ===== Main Function =====
def main():
    """Start the bot"""
    print("🚀 Starting ScribeCountBot...")
    
    # Create application with the token
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Add message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
