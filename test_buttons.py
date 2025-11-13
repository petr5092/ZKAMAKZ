from app.main import ButtonFactory, UniversityDataProvider

def test_main_menu_buttons():
    buttons = ButtonFactory.create_main_menu_buttons()
    expected_texts = [
        ["🏛️ Выбрать вуз", "📚 Специальности"],
        ["💳 Стоимость", "🛟 Поддержка"]
    ]
    for row, expected_row in zip(buttons, expected_texts):
        actual_row = [btn.text for btn in row]
        assert actual_row == expected_row, f"Главное меню неверно: {actual_row}"
    print("✅ Главное меню кнопки корректны")

def test_university_buttons():
    buttons = ButtonFactory.create_university_buttons()
    universities = UniversityDataProvider.get_all_universities()
    # Проверяем, что есть кнопки для каждого университета
    for uni, button_row in zip(universities, buttons[:-1]):  # последняя кнопка "Назад"
        assert button_row[0].text.startswith("🎓"), f"Кнопка университета неверна: {button_row[0].text}"
        assert uni['name'] in button_row[0].text, f"Название университета не совпадает: {button_row[0].text}"
    # Проверяем кнопку "Назад"
    assert buttons[-1][0].text == "⬅️ Назад", "Кнопка 'Назад' отсутствует"
    print("✅ Кнопки университетов корректны")

def test_back_button():
    buttons = ButtonFactory.create_back_button()
    assert buttons[0][0].text == "⬅️ Назад", "Кнопка 'Назад' неверна"
    print("✅ Кнопка 'Назад' корректна")

if __name__ == "__main__":
    test_main_menu_buttons()
    test_university_buttons()
    test_back_button()
    print("🎉 Все тесты кнопок пройдены!")
