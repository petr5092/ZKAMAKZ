import asyncio
import logging
import sys
from typing import List, Dict, Any, Optional

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, MessageCallback, CallbackButton

# Настройка кодировки для Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# ==========================
# Конфигурация
# ==========================
class BotConfig:
    BOT_TOKEN: str = "f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1"
    MAX_BUTTONS_PER_ROW: int = 2

# ==========================
# Провайдер данных о вузах
# ==========================
class UniversityDataProvider:
    @staticmethod
    def get_university_by_id(university_id: str) -> Optional[Dict[str, Any]]:
        universities = {
            "mgu": {"id": "mgu", "name": "МГУ им. М.В. Ломоносова", "location": "Москва", "student_count": 47000,
                    "founding_year": 1755, "description": "Старейший университет России", "cost_range": (250000, 400000),
                    "min_score": 280, "budget_places": 3000, "phone": "+7 (495) 939-10-00", "website": "msu.ru",
                    "specialties": ["Механика", "Филология", "Экономика", "Юриспруденция", "Медицина"]},
            "bmstu": {"id": "bmstu", "name": "МГТУ им. Н.Э. Баумана", "location": "Москва", "student_count": 19000,
                      "founding_year": 1830, "description": "Ведущий технический университет России",
                      "cost_range": (300000, 450000), "min_score": 270, "budget_places": 2500,
                      "phone": "+7 (499) 263-60-01", "website": "bmstu.ru",
                      "specialties": ["Робототехника", "Информатика", "Машиностроение", "Энергетика"]},
            "spbu": {"id": "spbu", "name": "СПБГУ", "location": "Санкт-Петербург", "student_count": 30000,
                     "founding_year": 1724, "description": "Классический университет России", "cost_range": (200000, 350000),
                     "min_score": 260, "budget_places": 4000, "phone": "+7 (812) 328-20-00", "website": "spbu.ru",
                     "specialties": ["Международные отношения", "Филология", "Юриспруденция", "Экономика"]},
        }
        return universities.get(university_id)

    @staticmethod
    def get_all_universities() -> List[Dict[str, Any]]:
        return [UniversityDataProvider.get_university_by_id(uid) for uid in ["mgu", "bmstu", "spbu"]]

# ==========================
# Фабрика кнопок
# ==========================
class ButtonFactory:
    @staticmethod
    def create_button(text: str, payload: str) -> CallbackButton:
        return CallbackButton(text=text, payload=payload)

    @staticmethod
    def create_main_menu_buttons() -> List[List[CallbackButton]]:
        return [
            [CallbackButton(text="🏛️ Выбрать вуз", payload="show_universities"),
             CallbackButton(text="📚 Специальности", payload="show_specialties")],
            [CallbackButton(text="💳 Стоимость", payload="show_payment"),
             CallbackButton(text="🛟 Поддержка", payload="show_support")]
        ]

    @staticmethod
    def create_university_buttons() -> List[List[CallbackButton]]:
        buttons = []
        for uni in UniversityDataProvider.get_all_universities():
            if uni:
                buttons.append([CallbackButton(text=f"🎓 {uni['name']}", payload=f"university_{uni['id']}")])
        buttons.append([CallbackButton(text="⬅️ Назад", payload="main_menu")])
        return buttons

    @staticmethod
    def create_back_button() -> List[List[CallbackButton]]:
        return [[CallbackButton(text="⬅️ Назад", payload="main_menu")]]

# ==========================
# Шаблоны сообщений
# ==========================
class MessageTemplate:
    @staticmethod
    def get_welcome_message() -> str:
        return (
            "👋 Добро пожаловать в систему подачи документов в вузы!\n\n"
            "Выберите действие:"
        )

    @staticmethod
    def get_main_menu_message() -> str:
        return "🎓 Главное меню\nВыберите действие:"

# ==========================
# Инициализация бота
# ==========================
bot = Bot(BotConfig.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.bot_started()
async def handle_bot_started(event):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=MessageTemplate.get_welcome_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )

# ==========================
# Обработка кнопок
# ==========================
@dp.message_callback()
async def handle_button_click(event):
    payload = event.callback.payload
    logger.info(f"Button clicked: {payload}")

    if payload == "main_menu":
        await event.bot.send_message(chat_id=event.chat_id,
                                     text=MessageTemplate.get_main_menu_message(),
                                     buttons=ButtonFactory.create_main_menu_buttons())
    elif payload == "show_universities":
        await event.bot.send_message(chat_id=event.chat_id,
                                     text="Выберите университет:",
                                     buttons=ButtonFactory.create_university_buttons())
    elif payload.startswith("university_"):
        university_id = payload.replace("university_", "")
        uni = UniversityDataProvider.get_university_by_id(university_id)
        if uni:
            text = f"🎓 {uni['name']}\n📍 {uni['location']}\nСтудентов: {uni['student_count']}"
            await event.bot.send_message(chat_id=event.chat_id,
                                         text=text,
                                         buttons=ButtonFactory.create_back_button())

# ==========================
# Запуск бота
# ==========================
if __name__ == "__main__":
    async def main():
        print("🚀 Бот запущен...")
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
