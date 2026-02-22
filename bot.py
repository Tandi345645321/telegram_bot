#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import asyncio
import http.server
import socketserver
import json
import time

from telegram.ext import Application, CommandHandler

from config import TOKEN, logger
from handlers import start, check_command
from admin_commands import admin_menu, blocklist, blockadd, blockdel, stats

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "alive"}).encode()
        self.wfile.write(response)
    def log_message(self, format, *args):
        pass

def run_http_server():
    """Запуск HTTP-сервера в главном потоке"""
    with socketserver.TCPServer(("0.0.0.0", 8080), HealthHandler) as httpd:
        logger.info("HTTP-сервер для health checks запущен на порту 8080")
        httpd.serve_forever()

def run_bot():
    """Запуск Telegram бота в отдельном потоке с собственным event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CommandHandler("admin", admin_menu))
    app.add_handler(CommandHandler("blocklist", blocklist))
    app.add_handler(CommandHandler("blockadd", blockadd))
    app.add_handler(CommandHandler("blockdel", blockdel))
    app.add_handler(CommandHandler("stats", stats))
    
    logger.info("Бот запущен и готов к работе...")
    app.run_polling()

def main():
    # Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Небольшая пауза, чтобы бот успел инициализироваться
    time.sleep(2)
    
    # Запускаем HTTP-сервер в главном потоке (он будет работать вечно)
    run_http_server()

if __name__ == "__main__":
    main()
