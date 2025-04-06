# -*- coding: utf-8 -*-
#  wai-life-bot - Telegram bot
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import sys
sys.dont_write_bytecode = True

try:
    from utils.dependencies import install_dependencies
    install_dependencies()
except Exception as e:
    print(f"[ERROR] Failed to install dependencies: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()

    import os
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    from utils.logger import Logger
    from utils.auth import authorized
    from manager.plugin_manager import PluginManager

except Exception as e:
    print(f"[ERROR] Failed during imports or environment setup: {e}")
    sys.exit(1)

plugin_manager = PluginManager()

@authorized
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "👋 Hello! I'm *Wai-Life Bot*.\n\n"
            "🤖 I help you remotely control your computer and automate tasks via Telegram.\n\n"
            "📌 Use /help to see the list of available commands.",
            parse_mode="Markdown"
        )
    except Exception as e:
        Logger.error(f"Error in /start command: {e}")
        await update.message.reply_text("⚠️ An error occurred while starting the bot.")

@authorized
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_text = plugin_manager.get_help()
        help_text = help_text.replace("*", "\*").replace("_", "\_").replace("[", "\[").replace("]", "\]").replace("(", "\(").replace(")", "\)")

        await update.message.reply_text(help_text, parse_mode="Markdown")
    except Exception as e:
        Logger.error(f"Error in /help command: {e}")
        await update.message.reply_text("⚠️ An error occurred while displaying help.")

@authorized
async def cmd_reload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = plugin_manager.reload()
        await update.message.reply_text(f"Reloaded {count} plugins.")
    except Exception as e:
        Logger.error(f"Error reloading plugins: {e}")
        await update.message.reply_text("⚠️ Failed to reload plugins.")

def main():
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", cmd_start))
        app.add_handler(CommandHandler("help", cmd_help))
        app.add_handler(CommandHandler("reload", cmd_reload))

        try:
            for handler in plugin_manager.get_handlers():
                app.add_handler(handler)
        except Exception as e:
            Logger.error(f"Failed to load plugin handlers: {e}")

        Logger.info("Bot started successfully. Listening for commands...")
        app.run_polling()

    except KeyboardInterrupt:
        Logger.warning("[!] Keyboard Interrupt detected!")
        sys.exit(0)
    except Exception as e:
        Logger.error(f"Unhandled exception in main(): {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
