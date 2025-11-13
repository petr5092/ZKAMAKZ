"""
MAX University Admission Bot
Корпоративная версия с работающими кнопками

Модуль: main.py
Версия: 3.1.1
Автор: dex_aka_slon
"""

import asyncio
import logging
import sys
from typing import List, Dict, Any, Optional

# Импорты фреймворка MAX API
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated, MessageButton, MessageCallback

# Настройка кодировки для Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class BotConfig:
    """Конфигурация бота."""
    BOT_TOKEN: str = "f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1"
    MAX_BUTTONS_PER_ROW: int = 2


class UniversityDataProvider:
    """Провайдер данных об университетах."""
    
    @staticmethod
    def get_university_by_id(university_id: str) -> Optional[Dict[str, Any]]:
        universities = {
            "mgu": {
                "id": "mgu",
                "name": "МГУ им. М.В. Ломоносова",
                "full_name": "Московский государственный университет имени М.В. Ломоносова",
                "location": "Москва",
                "student_count": 47000,
                "founding_year": 1755,
                "description": "Старейший и самый престижный университет России с богатой историей и традициями.",
                "cost_range": (250000, 400000),
                "min_score": 280,
                "budget_places": 3000,
                "phone": "+7 (495) 939-10-00",
                "website": "msu.ru",
                "specialties": ["Механика", "Филология", "Экономика", "Юриспруденция", "Медицина"]
            },
            "bmstu": {
                "id": "bmstu",
                "name": "МГТУ им. Н.Э. Баумана", 
                "full_name": "Московский государственный технический университет имени Н.Э. Баумана",
                "location": "Москва",
                "student_count": 19000,
                "founding_year": 1830,
                "description": "Ведущий технический университет России, специализирующийся на инженерных науках.",
                "cost_range": (300000, 450000),
                "min_score": 270,
                "budget_places": 2500,
                "phone": "+7 (499) 263-60-01",
                "website": "bmstu.ru",
                "specialties": ["Робототехника", "Информатика", "Машиностроение", "Энергетика"]
            },
            "spbu": {
                "id": "spbu",
                "name": "СПБГУ",
                "full_name": "Санкт-Петербургский государственный университет",
                "location": "Санкт-Петербург", 
                "student_count": 30000,
                "founding_year": 1724,
                "description": "Один из крупнейших классических университетов России в культурной столице.",
                "cost_range": (200000, 350000),
                "min_score": 260,
                "budget_places": 4000,
                "phone": "+7 (812) 328-20-00",
                "website": "spbu.ru",
                "specialties": ["Международные отношения", "Филология", "Юриспруденция", "Экономика"]
            }
        }
        return universities.get(university_id)
    
    @staticmethod
    def get_all_universities() -> List[Dict[str, Any]]:
        return [
            UniversityDataProvider.get_university_by_id("mgu"),
            UniversityDataProvider.get_university_by_id("bmstu"), 
            UniversityDataProvider.get_university_by_id("spbu")
        ]


class ButtonFactory:
    """Фабрика для создания интерактивных кнопок."""
    
    @staticmethod
    def create_button(text: str, payload: str) -> MessageButton:
        return MessageButton(text=text, payload=payload)
    
    @staticmethod
    def create_main_menu_buttons() -> List[List[MessageButton]]:
        return [
            [
                MessageButton(text="🏛️ Выбрать вуз", payload="show_universities"),
                MessageButton(text="📚 Специальности", payload="show_specialties")
            ],
            [
                MessageButton(text="💳 Стоимость", payload="show_payment"),
                MessageButton(text="🛟 Поддержка", payload="show_support")
            ]
        ]
    
    @staticmethod
    def create_university_buttons() -> List[List[MessageButton]]:
        universities = UniversityDataProvider.get_all_universities()
        buttons = []
        
        for university in universities:
            if university:
                buttons.append([
                    MessageButton(
                        text=f"🎓 {university['name']}", 
                        payload=f"university_{university['id']}"
                    )
                ])
        
        buttons.append([MessageButton(text="⬅️ Назад", payload="main_menu")])
        return buttons
    
    @staticmethod
    def create_back_button() -> List[List[MessageButton]]:
        return [[MessageButton(text="⬅️ Назад", payload="main_menu")]]


class MessageTemplate:
    """Шаблоны сообщений."""
    
    @staticmethod
    def get_welcome_message() -> str:
        return (
            "👋 **Добро пожаловать в систему подачи документов в вузы!**\n\n"
            "🎓 **Какой вуз ты выбираешь?**\n\n"
            "Я помогу тебе:\n"
            "• Найти подходящий университет 🏛️\n" 
            "• Выбрать специальность 📚\n"
            "• Узнать условия поступления 📝\n"
            "• Подать документы онлайн 🎓\n\n"
            "Выбери действие:"
        )
    
    @staticmethod
    def get_main_menu_message() -> str:
        return "🎓 **Главное меню**\n\nВыбери действие:"
    
    @staticmethod
    def format_university_info(university_data: Dict[str, Any]) -> str:
        min_cost, max_cost = university_data['cost_range']
        return (
            f"🎓 **{university_data['full_name']}**\n\n"
            f"📍 **Город:** {university_data['location']}\n"
            f"👥 **Студентов:** {university_data['student_count']:,}\n"
            f"📅 **Основан:** {university_data['founding_year']} год\n\n"
            f"**Описание:** {university_data['description']}\n\n"
            f"💰 **Стоимость:** {min_cost:,} - {max_cost:,} ₽/год\n"
            f"🎯 **Мин. балл:** {university_data['min_score']}+\n"
            f"🎓 **Бюджетные места:** {university_data['budget_places']:,}\n\n"
            f"📞 **Приемная комиссия:** {university_data['phone']}\n"
            f"🌐 **Сайт:** {university_data['website']}"
        )


# Инициализация бота и диспетчера
bot = Bot(BotConfig.BOT_TOKEN)
dp = Dispatcher()


@dp.bot_started()
async def handle_bot_started(event: BotStarted):
    """Обработчик запуска бота."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=MessageTemplate.get_welcome_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )


@dp.message_callback()
async def handle_button_click(event: MessageCallback):
    """Обработчик нажатий на кнопки - ОСНОВНОЙ МЕТОД ДЛЯ КНОПОК!"""
    payload = event.payload
    logger.info(f"Button clicked: {payload}")
    
    if payload == "main_menu":
        await show_main_menu(event)
    
    elif payload == "show_universities":
        await show_universities_list(event)
    
    elif payload == "show_specialties":
        await show_specialties_list(event)
    
    elif payload == "show_payment":
        await show_payment_info(event)
    
    elif payload == "show_support":
        await show_support_info(event)
    
    elif payload.startswith("university_"):
        university_id = payload.replace("university_", "")
        await show_university_details(event, university_id)
    
    elif payload.startswith("apply_"):
        university_id = payload.replace("apply_", "")
        await show_application_form(event, university_id)
    
    elif payload.startswith("favorite_"):
        university_id = payload.replace("favorite_", "")
        await add_to_favorites(event, university_id)
    
    else:
        await event.answer("Неизвестная команда")


async def show_main_menu(event: MessageCallback):
    """Показать главное меню."""
    await event.edit_message(
        text=MessageTemplate.get_main_menu_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )


async def show_universities_list(event: MessageCallback):
    """Показать список университетов."""
    text = "🏛️ **Выбери университет:**\n\nВот популярные университеты России:"
    await event.edit_message(
        text=text,
        buttons=ButtonFactory.create_university_buttons()
    )


async def show_university_details(event: MessageCallback, university_id: str):
    """Показать детали университета."""
    university_data = UniversityDataProvider.get_university_by_id(university_id)
    
    if not university_data:
        await event.answer("Университет не найден")
        return
    
    buttons = [
        [MessageButton(text="📝 Подать документы", payload=f"apply_{university_id}")],
        [MessageButton(text="⭐ В избранное", payload=f"favorite_{university_id}")],
        [MessageButton(text="🏛️ Другие вузы", payload="show_universities")],
        [MessageButton(text="⬅️ Главное меню", payload="main_menu")]
    ]
    
    await event.edit_message(
        text=MessageTemplate.format_university_info(university_data),
        buttons=buttons
    )


async def show_specialties_list(event: MessageCallback):
    """Показать список специальностей."""
    text = (
        "📚 **Специальности**\n\n"
        "В разработке... Скоро здесь появятся все направления подготовки!\n\n"
        "А пока выбери университет чтобы увидеть доступные специальности:"
    )
    await event.edit_message(
        text=text,
        buttons=ButtonFactory.create_back_button()
    )


async def show_payment_info(event: MessageCallback):
    """Показать информацию об оплате."""
    text = (
        "💳 **Стоимость обучения**\n\n"
        "**Бакалавриат:** 250,000 - 500,000 ₽/год\n"
        "**Магистратура:** 300,000 - 600,000 ₽/год\n\n"
        "📞 **Бухгалтерия:** +7 (495) 123-45-67\n"
        "✉️ **Email:** finance@university.ru"
    )
    await event.edit_message(
        text=text,
        buttons=ButtonFactory.create_back_button()
    )


async def show_support_info(event: MessageCallback):
    """Показать информацию о поддержке."""
    text = (
        "🛟 **Поддержка**\n\n"
        "📞 **Горячая линия:** +7 (495) 123-45-67\n"
        "✉️ **Email:** support@university.ru\n"
        "💬 **Онлайн-чат:** Круглосуточно\n\n"
        "**График работы:**\n"
        "• Пн-Пт: 9:00-18:00\n"
        "• Сб: 10:00-16:00\n"
        "• Вс: выходной"
    )
    await event.edit_message(
        text=text,
        buttons=ButtonFactory.create_back_button()
    )


async def show_application_form(event: MessageCallback, university_id: str):
    """Показать форму подачи документов."""
    university_data = UniversityDataProvider.get_university_by_id(university_id)
    
    if not university_data:
        await event.answer("Университет не найден")
        return
    
    text = (
        f"📝 **Подача документов в {university_data['name']}**\n\n"
        "Для подачи документов необходимо:\n"
        "1. Заполнить заявление\n"
        "2. Приложить копии документов\n"
        "3. Указать выбранные специальности\n\n"
        "📞 **Контакты приемной комиссии:**\n"
        f"Телефон: {university_data['phone']}\n"
        f"Сайт: {university_data['website']}\n\n"
        "Функция онлайн-подачи документов скоро будет доступна!"
    )
    
    buttons = [
        [MessageButton(text="🏛️ Назад к вузу", payload=f"university_{university_id}")],
        [MessageButton(text="⬅️ Главное меню", payload="main_menu")]
    ]
    
    await event.edit_message(text=text, buttons=buttons)


async def add_to_favorites(event: MessageCallback, university_id: str):
    """Добавить университет в избранное."""
    university_data = UniversityDataProvider.get_university_by_id(university_id)
    
    if not university_data:
        await event.answer("Университет не найден")
        return
    
    await event.answer(f"🎓 {university_data['name']} добавлен в избранное!")
    
    # Возвращаемся к информации об университете
    await show_university_details(event, university_id)


@dp.message_created(Command('start'))
async def handle_start_command(event: MessageCreated):
    """Обработчик команды /start."""
    await event.message.answer(
        text=MessageTemplate.get_welcome_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )


@dp.message_created()
async def handle_text_messages(event: MessageCreated):
    """Обработчик текстовых сообщений."""
    user_message = event.message.text.lower()
    
    if any(word in user_message for word in ['привет', 'start', 'начать']):
        await handle_start_command(event)
    
    elif any(word in user_message for word in ['мгу', 'ломоносов']):
        # Создаем временное сообщение с кнопкой МГУ
        buttons = [[MessageButton(text="🎓 МГУ", payload="university_mgu")]]
        await event.message.answer(
            text="Нажми на кнопку чтобы посмотреть информацию об МГУ:",
            buttons=buttons
        )
    
    elif any(word in user_message for word in ['бауманк', 'мгту']):
        buttons = [[MessageButton(text="🔧 МГТУ", payload="university_bmstu")]]
        await event.message.answer(
            text="Нажми на кнопку чтобы посмотреть информацию о МГТУ:",
            buttons=buttons
        )
    
    elif any(word in user_message for word in ['спбгу', 'петербург']):
        buttons = [[MessageButton(text="🌉 СПБГУ", payload="university_spbu")]]
        await event.message.answer(
            text="Нажми на кнопку чтобы посмотреть информацию о СПБГУ:",
            buttons=buttons
        )
    
    else:
        await event.message.answer(
            text=(
                "🎓 **Привет! Я помогу тебе выбрать университет.**\n\n"
                "Используй кнопки ниже или напиши:\n"
                "• МГУ\n• Бауманка\n• СПБГУ\n\n"
                "Или нажми /start для главного меню!"
            ),
            buttons=ButtonFactory.create_main_menu_buttons()
        )


async def main():
    """Основная функция запуска."""
    logger.info("Starting MAX University Bot with working buttons...")
    
    try:
        await dp.start_polling(bot)
    except Exception as error:
        logger.critical(f"Bot failed: {error}")
        raise


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
    except Exception as error:
        print(f"Error: {error}")