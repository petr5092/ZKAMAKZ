# main.py
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
# Стилизация сообщений
# ==========================
class UniversityStyler:
    """Класс для стилизации информации о университетах"""
    
    @staticmethod
    def format_university_info(university_data):
        """Форматирует информацию о университете"""
        return f"""
🎓 *{university_data['name']}*

📍 *Расположение:* {university_data.get('location', 'Не указано')}
👥 *Количество студентов:* {university_data.get('student_count', 'Не указано')}
📅 *Год основания:* {university_data.get('founding_year', 'Не указан')}
💰 *Стоимость обучения:* {university_data.get('cost_range', ('Не указана', 'Не указана'))[0]:,} - {university_data.get('cost_range', ('Не указана', 'Не указана'))[1]:,} ₽/год
🎯 *Минимальный балл:* {university_data.get('min_score', 'Не указан')}
🎓 *Бюджетные места:* {university_data.get('budget_places', 'Не указано')}

📖 *Описание:*
{university_data.get('description', 'Описание отсутствует')}

📞 *Контакты:* {university_data.get('phone', 'Не указаны')}
🌐 *Сайт:* {university_data.get('website', 'Не указан')}
        """.strip()

    @staticmethod
    def format_university_short(university_data):
        """Краткое форматирование для списка университетов"""
        return f"🎓 {university_data['name']} | 📍 {university_data.get('location', 'Н/Д')}"

class SpecializationStyler:
    """Класс для стилизации информации о специальностях"""
    
    @staticmethod
    def format_specialization_info(spec_data):
        """Форматирует информацию о специальности"""
        specialties = spec_data.get('specialties', [])
        specialties_text = ', '.join(specialties) if specialties else 'Не указаны'
        
        return f"""
📚 *{spec_data['name']}*

📍 *Расположение:* {spec_data.get('location', 'Не указано')}
🎯 *Минимальный балл:* {spec_data.get('min_score', 'Не указан')}
💰 *Стоимость обучения:* {spec_data.get('cost_range', ('Не указана', 'Не указана'))[0]:,} - {spec_data.get('cost_range', ('Не указана', 'Не указана'))[1]:,} ₽/год
👥 *Количество студентов:* {spec_data.get('student_count', 'Не указано')}
🎓 *Бюджетные места:* {spec_data.get('budget_places', 'Не указано')}

📖 *Описание:*
{spec_data.get('description', 'Описание отсутствует')}

🎓 *Доступные специальности:*
{specialties_text}

📞 *Контакты:* {spec_data.get('phone', 'Не указаны')}
🌐 *Сайт:* {spec_data.get('website', 'Не указан')}
        """.strip()

    @staticmethod
    def format_specialization_short(spec_data):
        """Краткое форматирование для списка специальностей"""
        return f"📚 {spec_data['name']} | 🎯 {spec_data.get('min_score', 'Н/Д')} | 📍 {spec_data.get('location', 'Н/Д')}"

class MessageTemplates:
    """Шаблоны сообщений для бота"""
    
    @staticmethod
    def welcome_message():
        return """
🎉 *Добро пожаловать в бот-помощник по вузам!*

Здесь вы можете:
• 🏛️ Выбрать подходящий вуз
• 📚 Изучить специальности
• 💳 Узнать стоимость обучения
• 🎯 Оценить свои шансы

Выберите действие в меню ниже 👇
        """.strip()

    @staticmethod
    def universities_list_message(universities):
        """Сообщение со списком университетов"""
        if not universities:
            return "🏛️ *Доступные вузы:*\n\nПока нет данных о университетах"
        
        header = "🏛️ *Доступные вузы:*\n\n"
        universities_list = "\n".join([
            f"{i+1}. {UniversityStyler.format_university_short(uni)}"
            for i, uni in enumerate(universities)
        ])
        return header + universities_list

    @staticmethod
    def specializations_list_message(specializations):
        """Сообщение со списком специальностей"""
        if not specializations:
            return "📚 *Доступные специальности:*\n\nПока нет данных о специальностях"
        
        header = "📚 *Доступные специальности:*\n\n"
        specs_list = "\n".join([
            f"{i+1}. {SpecializationStyler.format_specialization_short(spec)}"
            for i, spec in enumerate(specializations)
        ])
        return header + specs_list

    @staticmethod
    def price_info_message(university_data):
        """Сообщение с информацией о стоимости"""
        min_cost, max_cost = university_data.get('cost_range', ('Не указана', 'Не указана'))
        return f"""
💳 *Информация о стоимости обучения*

🎓 *Вуз:* {university_data['name']}
💵 *Стоимость:* {min_cost:,} - {max_cost:,} ₽/год
🎓 *Бюджетные места:* {university_data.get('budget_places', 'Не указано')}
🎯 *Минимальный балл:* {university_data.get('min_score', 'Не указан')}

💡 *Примечание:* Актуальная информация на официальном сайте
        """.strip()

    @staticmethod
    def support_info_message():
        """Сообщение с информацией о поддержке"""
        return """
🛟 *Служба поддержки*

Если у вас возникли вопросы, вы можете обратиться в нашу службу поддержки:

📞 *Телефон:* +7 (495) 123-45-67
📧 *Email:* support@university.com
🕒 *Время работы:* 9:00 - 18:00 (Пн-Пт)

Мы всегда готовы помочь вам! 🤝
        """.strip()

# ==========================
# Провайдер данных о вузах
# ==========================
class UniversityDataProvider:
    @staticmethod
    def get_university_by_id(university_id: str) -> Optional[Dict[str, Any]]:
        universities = {
            "mgu": {
                "id": "mgu", 
                "name": "МГУ им. М.В. Ломоносова", 
                "location": "Москва", 
                "student_count": 47000,
                "founding_year": 1755, 
                "description": "Старейший университет России с богатой историей и традициями. Ведущий научный и образовательный центр страны.", 
                "cost_range": (250000, 400000),
                "min_score": 280, 
                "budget_places": 3000, 
                "phone": "+7 (495) 939-10-00", 
                "website": "msu.ru",
                "specialties": ["Механика", "Филология", "Экономика", "Юриспруденция", "Медицина", "Физика", "Химия"]
            },
            "bmstu": {
                "id": "bmstu", 
                "name": "МГТУ им. Н.Э. Баумана", 
                "location": "Москва", 
                "student_count": 19000,
                "founding_year": 1830, 
                "description": "Ведущий технический университет России, специализирующийся на инженерных науках и высоких технологиях.", 
                "cost_range": (300000, 450000), 
                "min_score": 270, 
                "budget_places": 2500,
                "phone": "+7 (499) 263-60-01", 
                "website": "bmstu.ru",
                "specialties": ["Робототехника", "Информатика", "Машиностроение", "Энергетика", "Авиастроение", "Кибернетика"]
            },
            "spbu": {
                "id": "spbu", 
                "name": "СПБГУ", 
                "location": "Санкт-Петербург", 
                "student_count": 30000,
                "founding_year": 1724, 
                "description": "Один из крупнейших классических университетов России в культурной столице с мировым признанием.", 
                "cost_range": (200000, 350000),
                "min_score": 260, 
                "budget_places": 4000, 
                "phone": "+7 (812) 328-20-00", 
                "website": "spbu.ru",
                "specialties": ["Международные отношения", "Филология", "Юриспруденция", "Экономика", "История", "Психология"]
            },
        }
        return universities.get(university_id)

    @staticmethod
    def get_all_universities() -> List[Dict[str, Any]]:
        return [UniversityDataProvider.get_university_by_id(uid) for uid in ["mgu", "bmstu", "spbu"]]

    @staticmethod
    def get_all_specializations() -> List[Dict[str, Any]]:
        """Возвращает список всех специальностей (на основе данных университетов)"""
        specializations = []
        for uni in UniversityDataProvider.get_all_universities():
            if uni and 'specialties' in uni:
                for spec_name in uni['specialties']:
                    specializations.append({
                        'name': spec_name,
                        'university': uni['name'],
                        'location': uni['location'],
                        'min_score': uni.get('min_score'),
                        'cost_range': uni.get('cost_range'),
                        'student_count': uni.get('student_count'),
                        'budget_places': uni.get('budget_places'),
                        'description': f"Специальность в {uni['name']}. {uni['description']}",
                        'phone': uni.get('phone'),
                        'website': uni.get('website')
                    })
        return specializations

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
    def create_specialization_buttons() -> List[List[CallbackButton]]:
        buttons = []
        specializations = UniversityDataProvider.get_all_specializations()
        for spec in specializations[:8]:  # Ограничиваем количество кнопок
            buttons.append([CallbackButton(text=f"📚 {spec['name']}", payload=f"spec_{spec['name'][:20]}")])
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
        return MessageTemplates.welcome_message()

    @staticmethod
    def get_main_menu_message() -> str:
        return "🎓 *Главное меню*\n\nВыберите действие:"

    @staticmethod
    def format_university_info(university_data: Dict[str, Any]) -> str:
        return UniversityStyler.format_university_info(university_data)

    @staticmethod
    def format_specialization_info(spec_data: Dict[str, Any]) -> str:
        return SpecializationStyler.format_specialization_info(spec_data)

    @staticmethod
    def get_payment_info() -> str:
        return "💳 *Информация о стоимости обучения*\n\nВыберите университет для просмотра стоимости:"

    @staticmethod
    def get_support_info() -> str:
        return MessageTemplates.support_info_message()

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
                                    text=MessageTemplates.universities_list_message(
                                        UniversityDataProvider.get_all_universities()
                                    ),
                                    buttons=ButtonFactory.create_university_buttons())

    elif payload == "show_specialties":
        await event.bot.send_message(chat_id=event.chat_id,
                                    text=MessageTemplates.specializations_list_message(
                                        UniversityDataProvider.get_all_specializations()
                                    ),
                                    buttons=ButtonFactory.create_specialization_buttons())

    elif payload == "show_payment":
        await event.bot.send_message(chat_id=event.chat_id,
                                    text=MessageTemplate.get_payment_info(),
                                    buttons=ButtonFactory.create_university_buttons())

    elif payload == "show_support":
        await event.bot.send_message(chat_id=event.chat_id,
                                    text=MessageTemplate.get_support_info(),
                                    buttons=ButtonFactory.create_back_button())

    elif payload.startswith("university_"):
        university_id = payload.replace("university_", "")
        uni = UniversityDataProvider.get_university_by_id(university_id)
        if uni:
            # Определяем контекст (из какого раздела пришел запрос)
            if "payment" in payload:
                text = MessageTemplates.price_info_message(uni)
            else:
                text = MessageTemplate.format_university_info(uni)
            
            await event.bot.send_message(chat_id=event.chat_id,
                                        text=text,
                                        buttons=ButtonFactory.create_back_button())

    elif payload.startswith("spec_"):
        spec_name = payload.replace("spec_", "")
        specializations = UniversityDataProvider.get_all_specializations()
        spec_data = next((spec for spec in specializations if spec['name'].startswith(spec_name)), None)
        
        if spec_data:
            text = MessageTemplate.format_specialization_info(spec_data)
            await event.bot.send_message(chat_id=event.chat_id,
                                        text=text,
                                        buttons=ButtonFactory.create_back_button())
        else:
            await event.bot.send_message(chat_id=event.chat_id,
                                        text="❌ Информация о специальности не найдена",
                                        buttons=ButtonFactory.create_back_button())

    else:
        await event.bot.send_message(chat_id=event.chat_id,
                                    text="❌ Неизвестная команда",
                                    buttons=ButtonFactory.create_back_button())

# ==========================
# Запуск бота
# ==========================
if __name__ == "__main__":
    async def main():
        print("🚀 Бот запущен...")
        print("📊 Доступные университеты:")
        for uni in UniversityDataProvider.get_all_universities():
            if uni:
                print(f"  - {uni['name']}")
        
        print("\n🎯 Доступные специальности:")
        for spec in UniversityDataProvider.get_all_specializations()[:5]:
            print(f"  - {spec['name']}")
        
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ Произошла ошибка: {e}")