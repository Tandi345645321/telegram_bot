from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from utils import check_site_global, create_status_chart, analyze_blocking, is_blocked
from config import logger, FRIEND_USERNAME, FRIEND_GREETING, LOCATIONS

friend_greeted = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username
    
    if username and username.lower() == FRIEND_USERNAME.lower():
        if user.id not in friend_greeted:
            friend_greeted.add(user.id)
            await update.message.reply_text(FRIEND_GREETING)
            return
    
    await update.message.reply_text(
        "👋 Привет! Я бот для проверки доступности сайтов.\n\n"
        "/check <домен> — проверить доступность сайта по всему миру\n"
        "Например: /check google.com"
    )

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Укажите домен. Например:\n/check example.com\n/check google.ru"
        )
        return
    
    domain = context.args[0].lower().strip()
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    
    status_msg = await update.message.reply_text(
        f"🔍 Проверяю {domain}... Это займёт около 30 секунд"
    )
    
    try:
        results = await check_site_global(domain)
        analysis = analyze_blocking(results)
        rkn_blocked = is_blocked(domain)
        chart_buf = create_status_chart(results, domain, rkn_blocked)
        
        country_names = {loc["country"]: loc["name"] for loc in LOCATIONS}
        text = f"📊 **Результаты проверки {domain}**\n\n"
        for r in results:
            name = country_names.get(r["country"], r["country"])
            time_str = f"{r['response_time']/1000:.2f}с" if r["response_time"] > 0 else "—"
            text += f"{name}: {r['status']} ({time_str})\n"
        text += f"\n{analysis}"
        if rkn_blocked:
            text += "\n\n⚠️ **Этот сайт находится в реестре заблокированных РКН**"
        text += f"\n\n🕒 Проверка: {datetime.now().strftime('%H:%M:%S')}"
        
        await status_msg.delete()
        await update.message.reply_photo(
            photo=chart_buf,
            caption=text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.exception("Ошибка в check_command")
        await status_msg.edit_text(f"❌ Ошибка при проверке: {str(e)}")