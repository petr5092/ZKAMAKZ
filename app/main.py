"""
MAX University Admission Bot dex
Модуль чат-бота для системы подачи документов в вузы petr5092
Версия: 1.0.0 
"""

import asyncio
import logging
from typing import List, Optional

# Импорты из MAX API
from maxapi import Bot, Dispatcher
from maxapi.types import (
    BotStarted, 
    Command, 
    MessageCreated, 
    Widget, 
    WidgetOptions, 
    WidgetSize, 
    WidgetType
)

# Импорты DAO слоя для работы с базой данных
from university.dao import UniversityDAO
from spec.dao import SpecDAO

# Настройка логирования для мониторинга и отладки
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота с токеном из настроек безопасности
# В продакшене токен должен храниться в защищенном хранилище
bot = Bot('f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1')
dp = Dispatcher()


class WidgetFactory:
    """
    Фабрика для создания виджетов.
    Централизует логику создания виджетов для обеспечения согласованности.
    """
    
    @staticmethod
    def create_payment_widget() -> Widget:
        """
        Создает виджет с информацией об оплате обучения.
        
        Returns:
            Widget: Виджет типа TEXT с информацией о стоимости обучения
        """
        return Widget(
            type=WidgetType.TEXT,
            name="💳 Оплата",
            size=WidgetSize.SMALL,
            options=WidgetOptions(
                text=(
                    "**Стоимость обучения:**\n\n"
                    "• Бакалавриат: 250,000-500,000 ₽/год\n"
                    "• Магистратура: 300,000-600,000 ₽/год\n\n"
                    "📞 Бухгалтерия: +7 (495) 123-45-67\n"
                    "✉️ finance@university.ru"
                )
            )
        )

    @staticmethod
    def create_timer_widget() -> Widget:
        """
        Создает виджет с таймером до окончания приема документов.
        
        Returns:
            Widget: Виджет типа TEXT с информацией о сроках
        """
        return Widget(
            type=WidgetType.TEXT,
            name="⏰ Время до окончания", 
            size=WidgetSize.SMALL,
            options=WidgetOptions(
                text=(
                    "**Прием документов 2024:**\n\n"
                    "📅 Бакалавриат: 25 дней\n"
                    "📅 Магистратура: 30 дней\n\n"
                    "⚡ Успей подать заявление!"
                )
            )
        )

    @staticmethod
    def create_my_config_widget() -> Widget:
        """
        Создает виджет с конфигурациями пользователя.
        
        Returns:
            Widget: Виджет типа LIST с пользовательскими настройками
        """
        return Widget(
            type=WidgetType.LIST,
            name="🎯 Мои конфигурации",
            size=WidgetSize.MEDIUM,
            options=WidgetOptions(
                items=[
                    {
                        "text": "Уровень образования", 
                        "description": "Бакалавриат"
                    },
                    {
                        "text": "Выбранные направления", 
                        "description": "3 специальности"
                    },
                    {
                        "text": "Статус документов", 
                        "description": "На проверке"
                    },
                    {
                        "text": "Избранное", 
                        "description": "5 университетов"
                    }
                ]
            )
        )

    @staticmethod
    def create_instruction_widget() -> Widget:
        """
        Создает виджет с пошаговой инструкцией подачи документов.
        
        Returns:
            Widget: Виджет типа TEXT с инструкциями
        """
        return Widget(
            type=WidgetType.TEXT,
            name="📖 Инструкция",
            size=WidgetSize.LARGE,
            options=WidgetOptions(
                text=(
                    "**Пошаговая инструкция:**\n\n"
                    "1. **Регистрация**\n"
                    "   - Создайте личный кабинет\n"
                    "   - Подтвердите email\n\n"
                    "2. **Выбор программ**\n"
                    "   - Изучите специальности\n"
                    "   - Добавьте в избранное\n\n"
                    "3. **Подача документов**\n"
                    "   - Заполните анкету\n"
                    "   - Загрузите сканы\n\n"
                    "4. **Ожидание**\n"
                    "   - Проверка документов: 3-5 дней\n"
                    "   - Приглашение на собеседование"
                )
            )
        )

    @staticmethod
    def create_support_widget() -> Widget:
        """
        Создает виджет с контактами службы поддержки.
        
        Returns:
            Widget: Виджет типа LIST с контактами поддержки
        """
        return Widget(
            type=WidgetType.LIST,
            name="🛟 Поддержка",
            size=WidgetSize.SMALL,
            options=WidgetOptions(
                items=[
                    {
                        "text": "Горячая линия", 
                        "description": "+7 (495) 123-45-67"
                    },
                    {
                        "text": "Email", 
                        "description": "support@university.ru"
                    },
                    {
                        "text": "Онлайн-чат", 
                        "description": "Круглосуточно"
                    },
                    {
                        "text": "Офис", 
                        "description": "Москва, ул. Образцова, 1"
                    }
                ]
            )
        )

    @staticmethod
    def create_help_widget() -> Widget:
        """
        Создает виджет с часто задаваемыми вопросами.
        
        Returns:
            Widget: Виджет типа TEXT с FAQ
        """
        return Widget(
            type=WidgetType.TEXT,
            name="❓ Справка",
            size=WidgetSize.MEDIUM,
            options=WidgetOptions(
                text=(
                    "**Частые вопросы:**\n\n"
                    "• **Какие документы нужны?**\n"
                    "  Паспорт, аттестат, фото 3x4\n\n"
                    "• **Сроки рассмотрения?**\n"
                    "  От 3 до 14 рабочих дней\n\n"
                    "• **Есть ли общежитие?**\n"
                    "  Да, для иногородних\n\n"
                    "• **Военная кафедра?**\n"
                    "  На технических специальностях"
                )
            )
        )


# Инициализация фабрики виджетов
widget_factory = WidgetFactory()

# Создание статических виджетов при запуске приложения
PAYMENT_WIDGET = widget_factory.create_payment_widget()
TIMER_WIDGET = widget_factory.create_timer_widget()
MY_CONFIG_WIDGET = widget_factory.create_my_config_widget()
INSTRUCTION_WIDGET = widget_factory.create_instruction_widget()
SUPPORT_WIDGET = widget_factory.create_support_widget()
HELP_WIDGET = widget_factory.create_help_widget()


@dp.bot_started()
async def handle_bot_started(event: BotStarted) -> None:
    """
    Обработчик события запуска бота.
    Отправляет приветственное сообщение при первом взаимодействии с пользователем.
    
    Args:
        event (BotStarted): Событие запуска бота
    """
    logger.info(f"Bot started by user in chat {event.chat_id}")
    
    welcome_message = (
        "🎓 **Добро пожаловать в систему подачи документов в вузы!**\n\n"
        "**Доступные команды:**\n"
        "/start - Главное меню\n"
        "/widgets - Все виджеты\n" 
        "/universities - Университеты\n"
        "/specs - Специальности\n"
        "/help - Помощь"
    )
    
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=welcome_message
    )


@dp.message_created(Command('start'))
async def handle_main_menu(event: MessageCreated) -> None:
    """
    Обработчик команды /start.
    Отображает главное меню с основными виджетами.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Main menu requested by user in chat {event.chat_id}")
    
    await event.message.answer(
        text="🏠 **Главное меню**\n\nВыберите раздел или используйте команды:",
        widgets=[
            PAYMENT_WIDGET,
            TIMER_WIDGET, 
            MY_CONFIG_WIDGET
        ]
    )


@dp.message_created(Command('widgets'))
async def handle_all_widgets(event: MessageCreated) -> None:
    """
    Обработчик команды /widgets.
    Отображает все доступные виджеты системы.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"All widgets requested by user in chat {event.chat_id}")
    
    await event.message.answer(
        text="📊 **Все доступные виджеты**",
        widgets=[
            PAYMENT_WIDGET,
            TIMER_WIDGET,
            MY_CONFIG_WIDGET,
            INSTRUCTION_WIDGET, 
            SUPPORT_WIDGET,
            HELP_WIDGET
        ]
    )


@dp.message_created(Command('universities'))
async def handle_universities_list(event: MessageCreated) -> None:
    """
    Обработчик команды /universities.
    Загружает и отображает список университетов из базы данных.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Universities list requested by user in chat {event.chat_id}")
    
    try:
        # Получение данных из базы данных через DAO слой
        universities = await UniversityDAO.get_all()
        
        if not universities:
            logger.warning("No universities found in database")
            await event.message.answer("📚 Университеты не найдены в базе данных")
            return
        
        # Создание элементов списка для виджета
        university_items = []
        for university in universities[:8]:  # Ограничение для оптимизации отображения
            university_items.append({
                "text": f"{university.name}",
                "description": f"📍 {university.location} | 👥 {university.count_students} студентов"
            })
        
        # Создание динамического виджета с университетами
        universities_widget = Widget(
            type=WidgetType.LIST,
            name="🏛️ Университеты",
            size=WidgetSize.LARGE,
            options=WidgetOptions(items=university_items)
        )
        
        response_text = (
            f"🏛️ **Список университетов**\n\n"
            f"Найдено: {len(universities)} университетов"
        )
        
        await event.message.answer(
            text=response_text,
            widgets=[universities_widget]
        )
        
        logger.info(f"Successfully displayed {len(universities)} universities")
        
    except Exception as error:
        logger.error(f"Error loading universities: {error}", exc_info=True)
        await event.message.answer("❌ Произошла ошибка при загрузке университетов")


@dp.message_created(Command('specs'))
async def handle_specs_list(event: MessageCreated) -> None:
    """
    Обработчик команды /specs.
    Загружает и отображает список специальностей из базы данных.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Specialties list requested by user in chat {event.chat_id}")
    
    try:
        # Получение данных из базы данных через DAO слой
        specs = await SpecDAO.get_all()
        
        if not specs:
            logger.warning("No specialties found in database")
            await event.message.answer("📖 Специальности не найдены в базе данных")
            return
        
        # Создание элементов списка для виджета
        spec_items = []
        for spec in specs[:8]:  # Ограничение для оптимизации отображения
            spec_items.append({
                "text": f"{spec.name}",
                "description": f"💰 {spec.cost_of_education:,} ₽ | 🎯 {spec.min_mark} баллов"
            })
        
        # Создание динамического виджета со специальностями
        specs_widget = Widget(
            type=WidgetType.LIST,
            name="📚 Специальности", 
            size=WidgetSize.LARGE,
            options=WidgetOptions(items=spec_items)
        )
        
        response_text = (
            f"📚 **Список специальностей**\n\n"
            f"Найдено: {len(specs)} специальностей"
        )
        
        await event.message.answer(
            text=response_text,
            widgets=[specs_widget]
        )
        
        logger.info(f"Successfully displayed {len(specs)} specialties")
        
    except Exception as error:
        logger.error(f"Error loading specialties: {error}", exc_info=True)
        await event.message.answer("❌ Произошла ошибка при загрузке специальностей")


@dp.message_created(Command('search'))
async def handle_specs_search(event: MessageCreated) -> None:
    """
    Обработчик команды /search.
    Выполняет поиск специальностей по ключевому слову.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    # Извлечение поискового запроса из текста сообщения
    search_text = event.message.text.replace('/search', '').strip()
    
    if not search_text:
        logger.info("Empty search query received")
        await event.message.answer(
            "🔍 **Поиск специальностей**\n\n"
            "Используйте: /search [название]\n\n"
            "**Примеры:**\n"
            "/search программирование\n"
            "/search экономика\n" 
            "/search инженерия"
        )
        return
    
    logger.info(f"Search request: '{search_text}' in chat {event.chat_id}")
    
    try:
        # Получение всех специальностей для фильтрации
        all_specs = await SpecDAO.get_all()
        
        # Фильтрация специальностей по поисковому запросу
        filtered_specs = [
            spec for spec in all_specs 
            if (search_text.lower() in spec.name.lower() or 
                search_text.lower() in spec.institute.lower())
        ]
        
        if not filtered_specs:
            logger.info(f"No results found for search: '{search_text}'")
            await event.message.answer(f"🔍 По запросу '{search_text}' ничего не найдено")
            return
        
        # Создание элементов списка для виджета с результатами поиска
        spec_items = []
        for spec in filtered_specs[:6]:  # Ограничение для оптимизации отображения
            spec_items.append({
                "text": f"{spec.name}",
                "description": f"🏛️ {spec.institute} | 💰 {spec.cost_of_education:,} ₽"
            })
        
        # Создание динамического виджета с результатами поиска
        search_widget = Widget(
            type=WidgetType.LIST,
            name=f"🔍 Результаты поиска: {search_text}",
            size=WidgetSize.LARGE,
            options=WidgetOptions(items=spec_items)
        )
        
        response_text = (
            f"🔍 **Результаты поиска по '{search_text}'**\n\n"
            f"Найдено: {len(filtered_specs)} специальностей"
        )
        
        await event.message.answer(
            text=response_text,
            widgets=[search_widget]
        )
        
        logger.info(f"Search completed: found {len(filtered_specs)} results for '{search_text}'")
        
    except Exception as error:
        logger.error(f"Error during search: {error}", exc_info=True)
        await event.message.answer("❌ Произошла ошибка при выполнении поиска")


@dp.message_created(Command('payment'))
async def handle_payment_info(event: MessageCreated) -> None:
    """
    Обработчик команды /payment.
    Отображает информацию об оплате обучения.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Payment info requested by user in chat {event.chat_id}")
    await event.message.answer(
        text="💳 **Информация об оплате**",
        widgets=[PAYMENT_WIDGET]
    )


@dp.message_created(Command('timer'))
async def handle_timer_info(event: MessageCreated) -> None:
    """
    Обработчик команды /timer.
    Отображает информацию о сроках подачи документов.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Timer info requested by user in chat {event.chat_id}")
    await event.message.answer(
        text="⏰ **Сроки подачи документов**", 
        widgets=[TIMER_WIDGET]
    )


@dp.message_created(Command('help'))
async def handle_help_info(event: MessageCreated) -> None:
    """
    Обработчик команды /help.
    Отображает справочную информацию и частые вопросы.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    logger.info(f"Help info requested by user in chat {event.chat_id}")
    await event.message.answer(
        text="❓ **Справка и частые вопросы**",
        widgets=[HELP_WIDGET]
    )


@dp.message_created()
async def handle_all_messages(event: MessageCreated) -> None:
    """
    Обработчик всех сообщений, не соответствующих командам.
    Обеспечивает обработку естественного языка для улучшения UX.
    
    Args:
        event (MessageCreated): Событие создания сообщения
    """
    user_message = event.message.text.lower()
    logger.info(f"Received message: '{user_message}' in chat {event.chat_id}")
    
    # Обработка приветственных сообщений
    if any(word in user_message for word in ['привет', 'здравствуй', 'hello', 'hi']):
        await event.message.answer(
            "👋 Привет! Я помогу вам с подачей документов в вузы. "
            "Используйте /start для начала работы."
        )
    
    # Обработка запросов об университетах
    elif any(word in user_message for word in ['университет', 'вуз', 'универ']):
        await handle_universities_list(event)
    
    # Обработка запросов о специальностях
    elif any(word in user_message for word in ['специальность', 'направление', 'программа']):
        await handle_specs_list(event)
    
    # Обработка запросов об оплате
    elif any(word in user_message for word in ['оплата', 'стоимость', 'цена']):
        await handle_payment_info(event)
    
    # Обработка запросов о сроках
    elif any(word in user_message for word in ['срок', 'время', 'когда']):
        await handle_timer_info(event)
    
    # Обработка запросов о помощи
    elif any(word in user_message for word in ['помощь', 'help', 'поддержка']):
        await handle_help_info(event)
    
    # Ответ на непонятные сообщения
    else:
        logger.info(f"Unrecognized message: '{user_message}'")
        await event.message.answer(
            "🤔 Не совсем понимаю ваш вопрос.\n\n"
            "**Попробуйте одну из команд:**\n"
            "/start - Главное меню\n" 
            "/universities - Университеты\n"
            "/specs - Специальности\n"
            "/search - Поиск специальностей\n"
            "/help - Помощь"
        )


async def main() -> None:
    """
    Основная функция запуска бота.
    Инициализирует и запускает polling для обработки событий.
    """
    logger.info("Starting MAX University Admission Bot...")
    
    try:
        # Запуск long-polling для получения событий от MAX API
        await dp.start_polling(bot)
    except Exception as error:
        logger.critical(f"Bot crashed with error: {error}", exc_info=True)
        raise
    finally:
        logger.info("MAX University Admission Bot stopped")


if __name__ == '__main__':
    """
    Точка входа в приложение.
    Запускает асинхронный event loop для работы бота.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user request")
    except Exception as error:
        logger.critical(f"Unexpected error: {error}", exc_info=True)