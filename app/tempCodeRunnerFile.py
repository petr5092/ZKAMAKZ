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
    def create_button(text: str, payload: str) -> CallbackButton:
        return CallbackButton(text=text, payload=payload)

    @staticmethod
    def create_main_menu_buttons() -> List[List[CallbackButton]]:
        return [
            [
                CallbackButton(text="🏛️ Выбрать вуз", payload="show_universities"),
                CallbackButton(text="📚 Специальности", payload="show_specialties")
            ],
            [
                CallbackButton(text="💳 Стоимость", payload="show_payment"),
                CallbackButton(text="🛟 Поддержка", payload="show_support")
            ]
        ]

    @staticmethod
    def create_university_buttons() -> List[List[CallbackButton]]:
        universities = UniversityDataProvider.get_all_universities()
        buttons = []

        for university in universities:
            if university:
                buttons.append([
                    CallbackButton(
                        text=f"🎓 {university['name']}",
                        payload=f"university_{university['id']}"
                    )
                ])

        buttons.append([CallbackButton(text="⬅️ Назад", payload="main_menu")])
        return buttons

    @staticmethod
    def create_back_button() -> List[List[CallbackButton]]:
        return [[CallbackButton(text="⬅️ Назад", payload="main_menu")]]


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
dp = Dispatcher(bot)


@dp.bot_started()
async def handle_bot_started(event: BotStarted):
    """Обработчик запуска бота."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=MessageTemplate.get_welcome_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )


@dp.callback()
async def handle_button_click(event: MessageCallback):
    """Обработчик нажатий на кнопки."""
    payload = event.callback.payload
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

    else:
        await event.callback.answer("Неизвестная команда")


async def show_main_menu(event: MessageCallback):
    """Показываем главное меню."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=MessageTemplate.get_main_menu_message(),
        buttons=ButtonFactory.create_main_menu_buttons()
    )


async def show_universities_list(event: MessageCallback):
    """Показываем список университетов."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Выберите университет:",
        buttons=ButtonFactory.create_university_buttons()
    )


async def show_university_details(event: MessageCallback, university_id: str):
    """Показываем детали выбранного университета."""
    university = UniversityDataProvider.get_university_by_id(university_id)
    if university:
        university_info = MessageTemplate.format_university_info(university)
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=university_info,
            buttons=ButtonFactory.create_back_button()
        )


async def show_specialties_list(event: MessageCallback):
    """Показываем список специальностей."""
    # Местная логика для специальностей
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Список специальностей:\n\n1. Механика\n2. Филология\n3. Экономика\n4. Юриспруденция\n",
        buttons=ButtonFactory.create_back_button()
    )


async def show_payment_info(event: MessageCallback):
    """Показываем информацию о стоимости обучения."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Информация о стоимости обучения:\n\nМинимальная стоимость: 200,000 ₽/год.\n"
             "Максимальная стоимость: 450,000 ₽/год.",
        buttons=ButtonFactory.create_back_button()
    )


async def show_support_info(event: MessageCallback):
    """Показываем информацию о поддержке."""
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Если у тебя возникли вопросы, ты можешь обратиться в нашу службу поддержки:\n\n"
             "📞 Телефон: +7 (495) 123-45-67\n"
             "📧 Почта: support@university.com",
        buttons=ButtonFactory.create_back_button()
    )


# Запуск бота
if __name__ == "__main__":
    bot.run(dp)
