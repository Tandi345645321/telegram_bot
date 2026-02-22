import logging

TOKEN = "8403715390:AAEdo8Tbl6Ns70X27CbLGBxjg5S_u3ctwzY"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

LOCATIONS = [
    {"country": "RU", "name": "🇷🇺 Россия"},
    {"country": "US", "name": "🇺🇸 США"},
    {"country": "DE", "name": "🇩🇪 Германия"},
    {"country": "JP", "name": "🇯🇵 Япония"},
    {"country": "BR", "name": "🇧🇷 Бразилия"},
    {"country": "AU", "name": "🇦🇺 Австралия"},
]

CREATOR_USERNAME = "hfvjw"
FRIEND_USERNAME = "Nonkap"
FRIEND_GREETING = "АХУЕТЬ ЭТО ЖЕ АРТЁМ ЖАДОВ, ЛЮБИМЫЙ ИЗ ЛЮБИМЫХ, СПАСИБО ЧТО ТЫ ЕСТЬ, ТЕБЯ МЫ ВСЕ ЛЮБИМ, ПОЛЬЗУЙСЯ НА ЗДОРОВЬЕ, Я ТЕБЯ ЛЮБЛЮ"

BLOCKED_FILE = "blocked.json"