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

import pyautogui
from datetime import datetime
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes

async def cmd_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot current window"""
    try:
        screenshot = pyautogui.screenshot()

        screenshot_filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        
        with BytesIO() as byte_io:
            screenshot.save(byte_io, format="PNG")
            byte_io.seek(0)
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=byte_io,
                filename=screenshot_filename
            )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error screenshot: {str(e)}")

