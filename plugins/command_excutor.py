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

import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def cmd_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Execute a system command"""
    if not context.args:
        await update.message.reply_text("Usage: /cmd [command]")
        return

    command = " ".join(context.args)

    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        output = result.stderr if result.returncode != 0 else result.stdout
        await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ An error occurred while executing the command: {str(e)}")
