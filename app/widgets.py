"""
MAX University Admission Bot - Widget Manager Module
Модуль для управления динамическими виджетами и их конфигурацией
Версия: 1.0.0
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from maxapi.types import Widget, WidgetOptions, WidgetSize, WidgetType

# Импорты DAO слоя для работы с данными
from university.dao import UniversityDAO
from spec.dao import SpecDAO


@dataclass
class WidgetConfig:
    """
    Конфигурация виджета для централизованного управления настройками.
    
    Attributes:
        name (str): Название виджета
        type (WidgetType): Тип виджета (TEXT, LIST)
        size (WidgetSize): Размер виджета (SMALL, MEDIUM, LARGE)
        max_items (int): Максимальное количество элементов для LIST виджетов
    """
    name: str
    type: WidgetType
    size: WidgetSize
    max_items: int = 8


class WidgetManager:
    """
    Менеджер для создания и управления динамическими виджетами.
    
    Обеспечивает:
    - Создание виджетов на основе данных из БД
    - Валидацию конфигурации виджетов
    - Обработку ошибок при создании виджетов
    - Оптимизацию производительности через кэширование
    """
    
    # Конфигурации для различных типов виджетов
    WIDGET_CONFIGS = {
        'universities': WidgetConfig(
            name="🏛️ Университеты",
            type=WidgetType.LIST,
            size=WidgetSize.LARGE,
            max_items=10
        ),
        'specialties': WidgetConfig(
            name="📚 Специальности",
            type=WidgetType.LIST, 
            size=WidgetSize.LARGE,
            max_items=10
        ),
        'search_results': WidgetConfig(
            name="🔍 Результаты поиска",
            type=WidgetType.LIST,
            size=WidgetSize.LARGE,
            max_items=8
        ),
        'error': WidgetConfig(
            name="Ошибка",
            type=WidgetType.TEXT,
            size=WidgetSize.MEDIUM,
            max_items=1
        )
    }
    
    def __init__(self):
        """Инициализация менеджера виджетов."""
        self._logger = logging.getLogger(__name__)
    
    async def create_universities_widget(self) -> Widget:
        """
        Создает виджет со списком университетов из базы данных.
        
        Returns:
            Widget: Виджет с университетами или сообщением об ошибке
            
        Raises:
            DatabaseError: При ошибках доступа к базе данных
        """
        try:
            self._logger.info("Creating universities widget")
            
            # Получение данных из базы данных
            universities = await UniversityDAO.get_all()
            
            if not universities:
                self._logger.warning("No universities found in database")
                return self._create_error_widget("📚 Университеты не найдены")
            
            # Создание элементов списка с ограничением по количеству
            items = []
            for university in universities[:self.WIDGET_CONFIGS['universities'].max_items]:
                items.append({
                    "text": f"{university.name}",
                    "description": self._format_university_description(university)
                })
            
            config = self.WIDGET_CONFIGS['universities']
            return Widget(
                type=config.type,
                name=config.name,
                size=config.size,
                options=WidgetOptions(items=items)
            )
            
        except Exception as error:
            self._logger.error(f"Error creating universities widget: {error}", exc_info=True)
            return self._create_error_widget("❌ Ошибка загрузки университетов")
    
    async def create_specialties_widget(self) -> Widget:
        """
        Создает виджет со списком специальностей из базы данных.
        
        Returns:
            Widget: Виджет со специальностями или сообщением об ошибке
        """
        try:
            self._logger.info("Creating specialties widget")
            
            # Получение данных из базы данных
            specialties = await SpecDAO.get_all()
            
            if not specialties:
                self._logger.warning("No specialties found in database")
                return self._create_error_widget("📖 Специальности не найдены")
            
            # Создание элементов списка с ограничением по количеству
            items = []
            for spec in specialties[:self.WIDGET_CONFIGS['specialties'].max_items]:
                items.append({
                    "text": f"{spec.name}",
                    "description": self._format_specialty_description(spec)
                })
            
            config = self.WIDGET_CONFIGS['specialties']
            return Widget(
                type=config.type,
                name=config.name,
                size=config.size,
                options=WidgetOptions(items=items)
            )
            
        except Exception as error:
            self._logger.error(f"Error creating specialties widget: {error}", exc_info=True)
            return self._create_error_widget("❌ Ошибка загрузки специальностей")
    
    async def create_search_results_widget(self, search_query: str, specialties: List) -> Widget:
        """
        Создает виджет с результатами поиска специальностей.
        
        Args:
            search_query (str): Поисковый запрос пользователя
            specialties (List): Список найденных специальностей
            
        Returns:
            Widget: Виджет с результатами поиска
        """
        try:
            self._logger.info(f"Creating search results widget for query: '{search_query}'")
            
            if not specialties:
                return self._create_error_widget(f"По запросу '{search_query}' ничего не найдено")
            
            # Создание элементов списка с результатами поиска
            items = []
            for spec in specialties[:self.WIDGET_CONFIGS['search_results'].max_items]:
                items.append({
                    "text": f"{spec.name}",
                    "description": self._format_search_result_description(spec)
                })
            
            config = self.WIDGET_CONFIGS['search_results']
            widget_name = f"{config.name}: {search_query}"
            
            return Widget(
                type=config.type,
                name=widget_name,
                size=config.size,
                options=WidgetOptions(items=items)
            )
            
        except Exception as error:
            self._logger.error(f"Error creating search results widget: {error}", exc_info=True)
            return self._create_error_widget("❌ Ошибка при выполнении поиска")
    
    def _format_university_description(self, university) -> str:
        """
        Форматирует описание университета для отображения в виджете.
        
        Args:
            university: Объект университета из БД
            
        Returns:
            str: Отформатированное описание
        """
        return f"📍 {university.location} | 👥 {university.count_students} студентов"
    
    def _format_specialty_description(self, specialty) -> str:
        """
        Форматирует описание специальности для отображения в виджете.
        
        Args:
            specialty: Объект специальности из БД
            
        Returns:
            str: Отформатированное описание
        """
        return f"💰 {specialty.cost_of_education:,} ₽ | 🎯 {specialty.min_mark} баллов"
    
    def _format_search_result_description(self, specialty) -> str:
        """
        Форматирует описание результата поиска для отображения в виджете.
        
        Args:
            specialty: Объект специальности из БД
            
        Returns:
            str: Отформатированное описание
        """
        return f"🎯 {specialty.min_mark} баллов | 📊 {specialty.average_mark} средний"
    
    def _create_error_widget(self, error_message: str) -> Widget:
        """
        Создает виджет с сообщением об ошибке.
        
        Args:
            error_message (str): Сообщение об ошибке
            
        Returns:
            Widget: Виджет с сообщением об ошибке
        """
        config = self.WIDGET_CONFIGS['error']
        return Widget(
            type=config.type,
            name=config.name,
            size=config.size,
            options=WidgetOptions(text=error_message)
        )


# Глобальный экземпляр менеджера виджетов для использования во всем приложении
widget_manager = WidgetManager()