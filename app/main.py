"""
MAX University Admission Bot
Корпоративная версия с интерактивными кнопками

Модуль: main.py
Версия: 3.0.1
Автор: dex_aka_slon
"""

import asyncio
import logging
import sys
from typing import List, Dict, Any, Optional

# Импорты фреймворка MAX API
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated, MessageButton

# Настройка кодировки для Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Конфигурация логирования для мониторинга в продакшене
class UnicodeSafeStreamHandler(logging.StreamHandler):
    """Обработчик логов, безопасный для Unicode символов."""
    
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except UnicodeEncodeError:
            # Заменяем проблемные Unicode символы
            record.msg = record.msg.encode('ascii', 'replace').decode('ascii')
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        UnicodeSafeStreamHandler(),  # Безопасный вывод в консоль
    ]
)
logger = logging.getLogger(__name__)


class BotConfig:
    """
    Конфигурация бота.
    В продакшене значения должны загружаться из защищенного хранилища.
    """
    
    # Токен аутентификации бота в MAX платформе
    BOT_TOKEN: str = "f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1"
    
    # Настройки отображения
    MAX_BUTTONS_PER_ROW: int = 2
    MAX_UNIVERSITIES_DISPLAY: int = 6


class UniversityDataProvider:
    """
    Провайдер данных об университетах.
    В реальной системе данные должны загружаться из базы данных или API.
    """
    
    @staticmethod
    def get_university_by_id(university_id: str) -> Optional[Dict[str, Any]]:
        """
        Получить информацию об университете по идентификатору.
        
        Args:
            university_id (str): Уникальный идентификатор университета
            
        Returns:
            Optional[Dict[str, Any]]: Данные университета или None если не найден
        """
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
        """
        Получить список всех университетов.
        
        Returns:
            List[Dict[str, Any]]: Список университетов
        """
        return [
            UniversityDataProvider.get_university_by_id("mgu"),
            UniversityDataProvider.get_university_by_id("bmstu"), 
            UniversityDataProvider.get_university_by_id("spbu")
        ]
    
    @staticmethod
    def get_specialties() -> Dict[str, Dict[str, Any]]:
        """
        Получить информацию о специальностях.
        
        Returns:
            Dict[str, Dict[str, Any]]: Словарь специальностей
        """
        return {
            "it": {
                "name": "IT и программирование",
                "description": "Разработка программного обеспечения, кибербезопасность, анализ данных",
                "demand": "Высокая",
                "avg_salary": "120,000+ ₽",
                "universities": ["bmstu", "mgu", "spbu"]
            },
            "engineering": {
                "name": "Инженерия и технологии",
                "description": "Машиностроение, робототехника, строительство, энергетика", 
                "demand": "Высокая",
                "avg_salary": "90,000+ ₽",
                "universities": ["bmstu", "mgu"]
            },
            "economics": {
                "name": "Экономика и финансы",
                "description": "Экономика, менеджмент, финансы, бизнес-аналитика",
                "demand": "Средняя", 
                "avg_salary": "80,000+ ₽",
                "universities": ["mgu", "spbu"]
            }
        }


class ButtonFactory:
    """
    Фабрика для создания интерактивных кнопок.
    Реализует паттерн Factory для единообразного создания UI элементов.
    """
    
    @staticmethod
    def create_button(text: str, payload: str) -> MessageButton:
        """
        Создать кнопку с заданным текстом и payload.
        
        Args:
            text (str): Текст кнопки
            payload (str): Данные для обработки нажатия
            
        Returns:
            MessageButton: Созданная кнопка
        """
        return MessageButton(text=text, payload=payload)
    
    @staticmethod
    def create_main_menu_buttons() -> List[List[MessageButton]]:
        """
        Создать кнопки главного меню.
        
        Returns:
            List[List[MessageButton]]: Двумерный список кнопок для отображения в строках
        """
        return [
            [
                ButtonFactory.create_button("Выбрать вуз", "show_universities"),
                ButtonFactory.create_button("Специальности", "show_specialties")
            ],
            [
                ButtonFactory.create_button("Стоимость обучения", "show_payment_info"),
                ButtonFactory.create_button("Поддержка", "show_support_info")
            ],
            [
                ButtonFactory.create_button("Поиск", "show_search_menu")
            ]
        ]
    
    @staticmethod
    def create_university_buttons() -> List[List[MessageButton]]:
        """
        Создать кнопки для выбора университетов.
        
        Returns:
            List[List[MessageButton]]: Кнопки университетов с навигацией
        """
        universities = UniversityDataProvider.get_all_universities()
        buttons = []
        
        # Создаем кнопки для каждого университета
        for i in range(0, len(universities), BotConfig.MAX_BUTTONS_PER_ROW):
            row = []
            for university in universities[i:i + BotConfig.MAX_BUTTONS_PER_ROW]:
                if university:
                    button_text = f"{university['name']}"
                    row.append(ButtonFactory.create_button(button_text, f"university_{university['id']}"))
            if row:
                buttons.append(row)
        
        # Добавляем кнопку навигации
        buttons.append([ButtonFactory.create_button("Главное меню", "main_menu")])
        
        return buttons
    
    @staticmethod
    def create_specialty_buttons() -> List[List[MessageButton]]:
        """
        Создать кнопки для выбора специальностей.
        
        Returns:
            List[List[MessageButton]]: Кнопки специальностей с навигацией
        """
        specialties = UniversityDataProvider.get_specialties()
        buttons = []
        
        for specialty_id, specialty_data in specialties.items():
            button_text = f"{specialty_data['name']}"
            buttons.append([ButtonFactory.create_button(button_text, f"specialty_{specialty_id}")])
        
        buttons.append([ButtonFactory.create_button("Главное меню", "main_menu")])
        
        return buttons
    
    @staticmethod
    def create_back_button() -> List[List[MessageButton]]:
        """
        Создать стандартную кнопку возврата.
        
        Returns:
            List[List[MessageButton]]: Кнопка возврата в главное меню
        """
        return [
            [ButtonFactory.create_button("Главное меню", "main_menu")]
        ]
    
    @staticmethod
    def create_university_action_buttons(university_id: str) -> List[List[MessageButton]]:
        """
        Создать кнопки действий для университета.
        
        Args:
            university_id (str): Идентификатор университета
            
        Returns:
            List[List[MessageButton]]: Кнопки действий
        """
        return [
            [
                ButtonFactory.create_button("Подать документы", f"apply_{university_id}"),
                ButtonFactory.create_button("В избранное", f"favorite_{university_id}")
            ],
            [
                ButtonFactory.create_button("Другие вузы", "show_universities"),
                ButtonFactory.create_button("Главное меню", "main_menu")
            ]
        ]


class MessageTemplate:
    """
    Шаблоны сообщений для обеспечения консистентности текста.
    """
    
    @staticmethod
    def get_welcome_message() -> str:
        """
        Получить приветственное сообщение.
        
        Returns:
            str: Текст приветствия
        """
        return (
            "Добро пожаловать в систему подачи документов в вузы!\n\n"
            "Расскажите, какой вуз вас интересует?\n\n"
            "Я помогу вам:\n"
            "• Найти подходящий университет\n" 
            "• Выбрать специальность\n"
            "• Узнать условия поступления\n"
            "• Подать документы онлайн\n\n"
            "Выберите действие из меню ниже:"
        )
    
    @staticmethod
    def get_main_menu_message() -> str:
        """
        Получить сообщение главного меню.
        
        Returns:
            str: Текст главного меню
        """
        return (
            "Главное меню\n\n"
            "Выберите интересующий вас раздел:"
        )
    
    @staticmethod
    def get_university_list_message() -> str:
        """
        Получить сообщение со списком университетов.
        
        Returns:
            str: Текст списка университетов
        """
        return (
            "Выберите университет:\n\n"
            "Вот популярные университеты России. "
            "Нажмите на кнопку для получения подробной информации:"
        )
    
    @staticmethod
    def format_university_info(university_data: Dict[str, Any]) -> str:
        """
        Форматировать информацию об университете.
        
        Args:
            university_data (Dict[str, Any]): Данные университета
            
        Returns:
            str: Отформатированная информация
        """
        min_cost, max_cost = university_data['cost_range']
        
        return (
            f"{university_data['full_name']}\n\n"
            f"Город: {university_data['location']}\n"
            f"Студентов: {university_data['student_count']:,}\n"
            f"Основан: {university_data['founding_year']} год\n\n"
            f"Описание: {university_data['description']}\n\n"
            f"Стоимость обучения: {min_cost:,} - {max_cost:,} руб/год\n"
            f"Минимальный балл: {university_data['min_score']}+\n"
            f"Бюджетные места: {university_data['budget_places']:,}\n\n"
            f"Приемная комиссия: {university_data['phone']}\n"
            f"Сайт: {university_data['website']}\n\n"
            f"Популярные специальности:\n"
            + "\n".join([f"• {spec}" for spec in university_data['specialties']]) +
            f"\n\nВыберите действие:"
        )


class BotService:
    """
    Основной сервис бота, содержащий бизнес-логику.
    """
    
    def __init__(self):
        """Инициализация сервиса бота."""
        self.bot = Bot(BotConfig.BOT_TOKEN)
        self.dispatcher = Dispatcher()
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Настройка обработчиков событий."""
        self.dispatcher.bot_started()(self._handle_bot_started)
        self.dispatcher.message_created(Command('start'))(self._handle_start_command)
        self.dispatcher.message_created(Command('universities'))(self._handle_universities_command)
        self.dispatcher.message_created(Command('help'))(self._handle_help_command)
        self.dispatcher.message_created()(self._handle_message_created)
    
    async def _handle_bot_started(self, event: BotStarted) -> None:
        """
        Обработчик события запуска бота.
        
        Args:
            event (BotStarted): Событие запуска бота
        """
        logger.info(f"Bot started by user in chat {event.chat_id}")
        
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=MessageTemplate.get_welcome_message(),
            buttons=ButtonFactory.create_main_menu_buttons()
        )
    
    async def _handle_start_command(self, event: MessageCreated) -> None:
        """
        Обработчик команды /start.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        logger.info(f"Start command received from user {event.message.chat_id}")
        
        await event.message.answer(
            text=MessageTemplate.get_main_menu_message(),
            buttons=ButtonFactory.create_main_menu_buttons()
        )
    
    async def _handle_universities_command(self, event: MessageCreated) -> None:
        """
        Обработчик команды /universities.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        await self._show_universities_list(event)
    
    async def _handle_help_command(self, event: MessageCreated) -> None:
        """
        Обработчик команды /help.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        help_text = (
            "Справка по использованию бота\n\n"
            "Основные команды:\n"
            "/start - Главное меню\n"
            "/universities - Список университетов\n"
            "/help - Эта справка\n\n"
            "Как пользоваться:\n"
            "1. Используйте кнопки для навигации\n"
            "2. Пишите названия вузов для поиска\n"
            "3. Выбирайте специальности через меню\n\n"
            "Для технической поддержки обращайтесь:\n"
            "Телефон: +7 (495) 123-45-67\n"
            "Email: support@university.ru"
        )
        
        await event.message.answer(
            text=help_text,
            buttons=ButtonFactory.create_back_button()
        )
    
    async def _handle_message_created(self, event: MessageCreated) -> None:
        """
        Обработчик всех созданных сообщений.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        user_message = event.message.text
        logger.info(f"Message received from user {event.message.chat_id}: {user_message}")
        
        # Обработка действий через кнопки
        if user_message == "main_menu":
            await self._show_main_menu(event)
        elif user_message == "show_universities":
            await self._show_universities_list(event)
        elif user_message == "show_specialties":
            await self._show_specialties_list(event)
        elif user_message == "show_payment_info":
            await self._show_payment_info(event)
        elif user_message == "show_support_info":
            await self._show_support_info(event)
        elif user_message.startswith("university_"):
            university_id = user_message.replace("university_", "")
            await self._show_university_details(event, university_id)
        elif user_message.startswith("specialty_"):
            specialty_id = user_message.replace("specialty_", "")
            await self._show_specialty_details(event, specialty_id)
        else:
            await self._handle_text_message(event, user_message)
    
    async def _show_main_menu(self, event: MessageCreated) -> None:
        """
        Показать главное меню.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        await event.message.answer(
            text=MessageTemplate.get_main_menu_message(),
            buttons=ButtonFactory.create_main_menu_buttons()
        )
    
    async def _show_universities_list(self, event: MessageCreated) -> None:
        """
        Показать список университетов.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        await event.message.answer(
            text=MessageTemplate.get_university_list_message(),
            buttons=ButtonFactory.create_university_buttons()
        )
    
    async def _show_university_details(self, event: MessageCreated, university_id: str) -> None:
        """
        Показать детальную информацию об университете.
        
        Args:
            event (MessageCreated): Событие создания сообщения
            university_id (str): Идентификатор университета
        """
        university_data = UniversityDataProvider.get_university_by_id(university_id)
        
        if not university_data:
            await event.message.answer("Информация об университете временно недоступна")
            return
        
        await event.message.answer(
            text=MessageTemplate.format_university_info(university_data),
            buttons=ButtonFactory.create_university_action_buttons(university_id)
        )
    
    async def _show_specialties_list(self, event: MessageCreated) -> None:
        """
        Показать список специальностей.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        specialties_text = (
            "Выберите направление подготовки:\n\n"
            "Нажмите на кнопку для просмотра подробной информации "
            "и списка университетов по выбранной специальности:"
        )
        
        await event.message.answer(
            text=specialties_text,
            buttons=ButtonFactory.create_specialty_buttons()
        )
    
    async def _show_specialty_details(self, event: MessageCreated, specialty_id: str) -> None:
        """
        Показать детальную информацию о специальности.
        
        Args:
            event (MessageCreated): Событие создания сообщения
            specialty_id (str): Идентификатор специальности
        """
        specialties = UniversityDataProvider.get_specialties()
        specialty_data = specialties.get(specialty_id)
        
        if not specialty_data:
            await event.message.answer("Информация о специальности временно недоступна")
            return
        
        response_text = (
            f"{specialty_data['name']}\n\n"
            f"Описание: {specialty_data['description']}\n\n"
            f"Востребованность: {specialty_data['demand']}\n"
            f"Средняя зарплата: {specialty_data['avg_salary']}\n\n"
            f"Рекомендуемые университеты:\n"
            + "\n".join([f"• {UniversityDataProvider.get_university_by_id(uni_id)['name']}" 
                        for uni_id in specialty_data['universities']]) +
            f"\n\nВыберите действие:"
        )
        
        buttons = [
            [
                ButtonFactory.create_button("Посмотреть вузы", "show_universities"),
                ButtonFactory.create_button("Главное меню", "main_menu")
            ]
        ]
        
        await event.message.answer(
            text=response_text,
            buttons=buttons
        )
    
    async def _show_payment_info(self, event: MessageCreated) -> None:
        """
        Показать информацию об оплате обучения.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        payment_text = (
            "Информация об оплате обучения\n\n"
            "Стоимость обучения (в год):\n"
            "• Бакалавриат: 250,000 - 500,000 руб\n"
            "• Магистратура: 300,000 - 600,000 руб\n"
            "• Аспирантура: 200,000 - 400,000 руб\n\n"
            "Способы оплаты:\n"
            "• Банковской картой онлайн\n"
            "• Банковский перевод\n"
            "• Наличными в кассе университета\n\n"
            "Контакты бухгалтерии:\n"
            "Телефон: +7 (495) 123-45-67\n"
            "Email: finance@university.ru\n"
            "График: Пн-Пт 9:00-18:00"
        )
        
        await event.message.answer(
            text=payment_text,
            buttons=ButtonFactory.create_back_button()
        )
    
    async def _show_support_info(self, event: MessageCreated) -> None:
        """
        Показать информацию о поддержке.
        
        Args:
            event (MessageCreated): Событие создания сообщения
        """
        support_text = (
            "Служба поддержки\n\n"
            "Контакты:\n"
            "Горячая линия: +7 (495) 123-45-67\n"
            "Email: support@university.ru\n"
            "Онлайн-чат: Круглосуточно\n"
            "Офис: Москва, ул. Образцова, 1\n\n"
            "График работы:\n"
            "Пн-Пт: 9:00-18:00\n"
            "Сб: 10:00-16:00\n"
            "Вс: выходной\n\n"
            "Мы всегда рады помочь вам с выбором университета и подачей документов!"
        )
        
        await event.message.answer(
            text=support_text,
            buttons=ButtonFactory.create_back_button()
        )
    
    async def _handle_text_message(self, event: MessageCreated, message_text: str) -> None:
        """
        Обработать текстовое сообщение от пользователя.
        
        Args:
            event (MessageCreated): Событие создания сообщения
            message_text (str): Текст сообщения
        """
        message_lower = message_text.lower()
        
        # Обработка приветственных сообщений
        if any(word in message_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
            await self._show_main_menu(event)
            return
        
        # Обработка запросов об университетах
        if any(word in message_lower for word in ['мгу', 'ломоносов']):
            await self._show_university_details(event, "mgu")
        elif any(word in message_lower for word in ['бауманк', 'мгту']):
            await self._show_university_details(event, "bmstu")
        elif any(word in message_lower for word in ['спбгу', 'петербург']):
            await self._show_university_details(event, "spbu")
        else:
            # Общий ответ на неизвестные сообщения
            response_text = (
                f"Поиск информации по запросу: '{message_text}'\n\n"
                f"Используйте кнопки ниже для навигации или напишите:\n"
                f"• Название вуза (МГУ, Бауманка, СПБГУ)\n"
                f"• Команду /start для главного меню\n"
                f"• Команду /help для справки"
            )
            
            await event.message.answer(
                text=response_text,
                buttons=ButtonFactory.create_main_menu_buttons()
            )
    
    async def start_polling(self) -> None:
        """
        Запустить опрос событий бота.
        """
        try:
            await self.dispatcher.start_polling(self.bot)
        except Exception as error:
            logger.critical(f"Bot polling failed: {error}")
            raise


async def main():
    """
    Основная точка входа в приложение.
    
    Запускает бота и обрабатывает критические ошибки.
    """
    # Используем ASCII-friendly сообщения для логов
    logger.info("Starting MAX University Admission Bot (Corporate Edition)")
    print("MAX University Bot is starting...")
    
    try:
        bot_service = BotService()
        await bot_service.start_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user request")
        print("Bot stopped by user")
    except Exception as error:
        logger.critical(f"Fatal error: {error}")
        print(f"Application failed to start: {error}")
        raise


if __name__ == '__main__':
    # Запуск приложения с обработкой исключений
    try:
        asyncio.run(main())
    except Exception as error:
        print(f"Application failed: {error}")