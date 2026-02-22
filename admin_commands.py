from telegram import Update
from telegram.ext import ContextTypes
from utils import load_blocked, add_blocked, remove_blocked
from config import CREATOR_USERNAME

def is_creator(user):
    return user.username and user.username.lower() == CREATOR_USERNAME.lower()

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_creator(update.effective_user):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    text = (
        "🔧 **Админ-меню**\n\n"
        "Доступные команды:\n"
        "/blocklist — показать список заблокированных сервисов\n"
        "/blockadd <домен> — добавить домен в список РКН\n"
        "/blockdel <домен> — удалить домен из списка\n"
        "/stats — статистика использования (пока не реализовано)"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def blocklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_creator(update.effective_user):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    blocked = load_blocked()
    if not blocked:
        await update.message.reply_text("Список заблокированных сервисов пуст.")
    else:
        text = "🚫 **Список заблокированных сервисов (РКН):**\n\n" + "\n".join(f"• {d}" for d in blocked)
        await update.message.reply_text(text, parse_mode="Markdown")

async def blockadd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_creator(update.effective_user):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    if not context.args:
        await update.message.reply_text("Укажите домен. Пример: /blockadd telegram.org")
        return
    
    domain = context.args[0].lower().strip()
    if add_blocked(domain):
        await update.message.reply_text(f"✅ Домен {domain} добавлен в список заблокированных.")
    else:
        await update.message.reply_text(f"ℹ️ Домен {domain} уже есть в списке.")

async def blockdel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_creator(update.effective_user):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    if not context.args:
        await update.message.reply_text("Укажите домен. Пример: /blockdel telegram.org")
        return
    
    domain = context.args[0].lower().strip()
    if remove_blocked(domain):
        await update.message.reply_text(f"✅ Домен {domain} удалён из списка заблокированных.")
    else:
        await update.message.reply_text(f"❌ Домен {domain} не найден в списке.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_creator(update.effective_user):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    await update.message.reply_text("📊 Статистика пока не реализована. Будет позже.")