#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import http.server
import socketserver
import json

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

def run_http_server(ready_event):
    with socketserver.TCPServer(("0.0.0.0", 8080), HealthHandler) as httpd:
        logger.info("HTTP-сервер для health checks запущен на порту 8080")
        ready_event.set()
        httpd.serve_forever()

def main():
    ready_event = threading.Event()
    http_thread = threading.Thread(target=run_http_server, args=(ready_event,))
    http_thread.daemon = True
    http_thread.start()
    
    ready_event.wait()
    logger.info("HTTP-сервер готов, запускаем Telegram бота...")
    
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

if __name__ == "__main__":
    main()