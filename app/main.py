"""
MAX University Bot - правильная реализация на основе реального maxapi
"""

import asyncio
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot('f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1')
dp = Dispatcher()


@dp.bot_started()
async def on_bot_started(event: BotStarted):
    """Когда пользователь запускает бота"""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Добро пожаловать в систему подачи документов! Используйте /start"
    )


@dp.message_created(Command('start'))
async def on_start(event: MessageCreated):
    """Команда /start - главное меню"""
    await event.message.answer(
        "Главное меню\n\n"
        "Команды:\n"
        "/universities - Список университетов\n" 
        "/specs - Список специальностей\n"
        "/help - Помощь"
    )


@dp.message_created(Command('universities'))
async def on_universities(event: MessageCreated):
    """Показать университеты из БД"""
    try:
        from university.dao import UniversityDAO
        universities = await UniversityDAO.get_all()
        
        if not universities:
            await event.message.answer("Университеты не найдены")
            return
            
        text = "Список университетов:\n\n"
        for uni in universities[:3]:
            text += f"{uni.name}\n"
            text += f"Местоположение: {uni.location}\n"
            text += f"Студентов: {uni.count_students}\n\n"
            
        await event.message.answer(text)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await event.message.answer("Ошибка загрузки университетов")


@dp.message_created(Command('specs')) 
async def on_specs(event: MessageCreated):
    """Показать специальности из БД"""
    try:
        from spec.dao import SpecDAO
        specs = await SpecDAO.get_all()
        
        if not specs:
            await event.message.answer("Специальности не найдены")
            return
            
        text = "Список специальностей:\n\n"
        for spec in specs[:3]:
            text += f"{spec.name}\n"
            text += f"Институт: {spec.institute}\n" 
            text += f"Стоимость: {spec.cost_of_education} руб/год\n\n"
            
        await event.message.answer(text)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await event.message.answer("Ошибка загрузки специальностей")


@dp.message_created(Command('help'))
async def on_help(event: MessageCreated):
    """Помощь"""
    await event.message.answer(
        "Помощь\n\n"
        "Поддержка: +7 (495) 123-45-67\n"
        "Email: support@university.ru"
    )


@dp.message_created()
async def on_any_message(event: MessageCreated):
    """Обработка любых сообщений"""
    text = event.message.text.lower()
    
    if 'привет' in text:
        await event.message.answer("Привет! Используйте /start")
    elif 'универ' in text:
        await on_universities(event)
    elif 'специальность' in text:
        await on_specs(event)
    else:
        await event.message.answer("Не понял. Используйте /start для меню")


async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())