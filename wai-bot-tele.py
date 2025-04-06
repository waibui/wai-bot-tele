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

try:
    import sys
    
    sys.dont_write_bytecode = True
    
    from utils.dependencies import install_dependencies
    try:
        install_dependencies()
    except Exception as e:
        sys.exit(e)
        
    from dotenv import load_dotenv
    load_dotenv()
    
    import os
    from utils.logger import Logger
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

except KeyboardInterrupt:
    sys.exit("[!] Keyboard Interrupt detected!")
except Exception as e:
    sys.exit(e)
    
    
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")
    
    app = Application.builder().token(token).build()
    
    
if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        sys.exit("[!] Keyboard Interrupt detected!")
    except Exception as e:
        sys.exit(e)
