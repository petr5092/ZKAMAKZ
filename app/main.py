import asyncio
import logging

from maxapi import Bot, Dispatcher

# Кнопки
from maxapi.types import (
    ChatButton, 
    LinkButton, 
    CallbackButton, 
    RequestGeoLocationButton, 
    MessageButton, 
    ButtonsPayload, # Для постройки клавиатуры без InlineKeyboardBuilder
    RequestContactButton, 
    OpenAppButton, 
)

from maxapi.types import (
    MessageCreated, 
    MessageCallback, 
    MessageChatCreated,
    CommandStart, 
    Command
)
from university.dao import UniversityDAO
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from spec.dao import SpecDAO

logging.basicConfig(level=logging.INFO)

bot = Bot('f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1')
dp = Dispatcher()


@dp.message_created(CommandStart())
async def echo(event: MessageCreated):
    builder = InlineKeyboardBuilder()
    universities = await UniversityDAO.get_all()
    for uni in universities:
        builder.row(
            CallbackButton(
                text=uni.name,
                payload=f'university_{uni.id}',
            )
        )
    await event.message.answer(
            text='Привет! Из какого ты университета?',
            attachments=[
                builder.as_markup()
            ]
        
    
        )


@dp.message_created()
async def search_spec(event: MessageCreated, uni_id: int):
    builder = InlineKeyboardBuilder()
    university = await UniversityDAO.find_by_id(uni_id)
    specs = await SpecDAO.get_all(university_id=uni_id)
    for spec in specs:
        builder.row(
            CallbackButton(
                text=spec.name,
                payload=f'specs_{spec.id}',
            )
        )
    await event.message.answer(
        text=f"{university.name}\n"
        f"Имеет {university.count_students} студентов, расположенных в {university.count_campus} кампусах,"
        f"а главный расположен по адресу: {university.location}\n"
        f"В этом вузе {university.count_branches} специальности",
        attachments=[
            builder.as_markup()
        ]
    

    )
@dp.message_callback()
async def message_callback(callback: MessageCallback):
    if callback.callback.payload.startswith('university_'):
        await search_spec(event=MessageCreated(message=callback.message,
                                               update_type=callback.update_type,
                                               timestamp=callback.timestamp
                                               ), 
                          uni_id=int(callback.callback.payload.split('_')[1])
                          )
    else:
        spec = await SpecDAO.find_by_id(int(callback.callback.payload.split('_')[1]))
        await callback.message.answer(
                            f"⏩ **Программа:** {spec.name}\n"
                            f"🏫 **Институт:** {spec.institute}\n\n"
                            
                            f"📝 **Описание:**\n"
                            f"{spec.description}\n\n"
                            
                            f"💰 **Стоимость обучения:** {spec.cost_of_education} руб.\n"
                            f"⏳ **Общее количество часов:** {spec.total_hours}\n"
                            f"🛠️ **Практических часов:** {spec.practical_hours}\n"
                            f"⏲️ **Среднее количество часов в неделю:** {spec.average_hours}\n\n"
                            
                            f"📚 **Количество экзаменов:** {spec.count_exams}\n"
                            f"📖 **Количество курсовых работ:** {spec.count_coursework}\n"
                            f"💼 **Количество бюджетных мест:** {spec.count_budget}\n\n"
                            
                            f"🎯 **Минимальный балл для поступления:** {spec.min_mark}\n"
                            f"🏅 **Средний балл поступивших:** {spec.average_mark}"
                            )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())