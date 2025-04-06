import os
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

AUTHORIZED_USERS = set(filter(None, os.getenv('AUTHORIZED_USERS', '').split(',')))

def authorized(func):
    """Allow only authorized users to access the handler."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = str(update.effective_user.id)
        if uid not in AUTHORIZED_USERS:
            await update.message.reply_text("Unauthorized.")
            return
        return await func(update, context)
    
    return wrapper
