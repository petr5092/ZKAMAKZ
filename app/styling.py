# app/styling.py
class UniversityStyler:
    """Класс для стилизации информации о университетах"""
    
    @staticmethod
    def format_university_info(university_data):
        """Форматирует информацию о университете"""
        return f"""
🎓 *{university_data['name']}*

📍 *Расположение:* {university_data.get('location', 'Не указано')}
👥 *Количество студентов:* {university_data.get('count_students', 'Не указано')}
🏘️ *Количество кампусов:* {university_data.get('count_campus', 'Не указано')}
🌐 *Филиалы:* {university_data.get('count_branches', 'Не указано')}

📖 *Описание:*
{university_data.get('description', 'Описание отсутствует')}
        """.strip()

    @staticmethod
    def format_university_short(university_data):
        """Краткое форматирование для списка университетов"""
        return f"🎓 {university_data['name']} | 📍 {university_data.get('location', 'Н/Д').split(',')[0]}"

class SpecializationStyler:
    """Класс для стилизации информации о специальностях"""
    
    @staticmethod
    def format_specialization_info(spec_data):
        """Форматирует информацию о специальности"""
        return f"""
📚 *{spec_data['name']}*

🏛️ *Университет:* {spec_data.get('university', 'Не указан')}
🏫 *Институт:* {spec_data.get('institute', 'Не указан')}
💵 *Стоимость обучения:* {spec_data.get('cost_of_education', 'Не указана')} руб/год
🎯 *Минимальный балл:* {spec_data.get('min_mark', 'Не указан')}
⭐ *Средний балл:* {spec_data.get('average_mark', 'Не указан')}
🎓 *Бюджетные места:* {spec_data.get('count_budget', 'Не указано')}

⏰ *Общая нагрузка:*
   • Всего часов: {spec_data.get('total_hours', 'Не указано')}
   • Практические часы: {spec_data.get('practical_hours', 'Не указано')}
   • Среднее часов: {spec_data.get('average_hours', 'Не указано')}

📊 *Академическая нагрузка:*
   • Экзамены: {spec_data.get('count_exams', 'Не указано')}
   • Курсовые работы: {spec_data.get('count_coursework', 'Не указано')}

📖 *Описание:*
{spec_data.get('description', 'Описание отсутствует')}
        """.strip()

    @staticmethod
    def format_specialization_short(spec_data):
        """Краткое форматирование для списка специальностей"""
        return f"📚 {spec_data['name']} | 🎯 {spec_data.get('min_mark', 'Н/Д')} | 💵 {spec_data.get('cost_of_education', 'Н/Д')} руб"

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
        return f"""
💳 *Информация о стоимости обучения*

🎓 *Вуз:* {university_data['name']}
💵 *Стоимость:* {university_data.get('cost_of_education', 'Не указана')} руб/год

💡 *Примечание:* Актуальная информация на официальном сайте
        """.strip()