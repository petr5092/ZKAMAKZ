"""
MAX University Admission Bot - Configuration Module
Модуль для управления конфигурацией приложения и переменными окружения
Версия: 1.0.0
"""

import os
from typing import Dict, Any, Optional

from pydantic import PostgresDsn, validator, root_validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Настройки подключения к базе данных PostgreSQL.
    
    Attributes:
        POSTGRES_HOST (str): Хост базы данных
        POSTGRES_PORT (int): Порт базы данных
        POSTGRES_USER (str): Пользователь базы данных
        POSTGRES_PASSWORD (str): Пароль базы данных  
        POSTGRES_NAME (str): Название базы данных
        DATABASE_URL (str): Полный URL подключения (вычисляется автоматически)
    """
    
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_NAME: str = "university_db"
    
    @root_validator(skip_on_failure=True)
    def build_database_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Строит URL для подключения к базе данных из отдельных компонентов.
        
        Args:
            values (Dict[str, Any]): Значения валидируемых полей
            
        Returns:
            Dict[str, Any]: Обновленные значения с добавленным DATABASE_URL
            
        Raises:
            ValueError: Если отсутствуют обязательные поля для построения URL
        """
        required_fields = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_NAME']
        
        # Проверка наличия всех обязательных полей
        for field in required_fields:
            if field not in values or not values[field]:
                raise ValueError(f"Missing required field for database URL: {field}")
        
        # Построение DSN строки для asyncpg
        values["DATABASE_URL"] = (
            f"postgresql+asyncpg://{values['POSTGRES_USER']}:"
            f"{values['POSTGRES_PASSWORD']}@{values['POSTGRES_HOST']}:"
            f"{values['POSTGRES_PORT']}/{values['POSTGRES_NAME']}"
        )
        
        return values
    
    @validator('POSTGRES_PORT')
    def validate_port(cls, v: int) -> int:
        """
        Валидация порта базы данных.
        
        Args:
            v (int): Значение порта
            
        Returns:
            int: Валидированный порт
            
        Raises:
            ValueError: Если порт вне допустимого диапазона
        """
        if not 1 <= v <= 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {v}")
        return v


class BotSettings(BaseSettings):
    """
    Настройки бота и API.
    
    Attributes:
        BOT_TOKEN (str): Токен бота для MAX API
        API_TIMEOUT (int): Таймаут для API запросов в секундах
        MAX_RETRIES (int): Максимальное количество повторных попыток при ошибках
    """
    
    BOT_TOKEN: str
    API_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    @validator('BOT_TOKEN')
    def validate_bot_token(cls, v: str) -> str:
        """
        Валидация токена бота.
        
        Args:
            v (str): Токен бота
            
        Returns:
            str: Валидированный токен
            
        Raises:
            ValueError: Если токен пустой или слишком короткий
        """
        if not v:
            raise ValueError("Bot token cannot be empty")
        if len(v) < 10:
            raise ValueError("Bot token seems too short")
        return v


class Settings(DatabaseSettings, BotSettings):
    """
    Основные настройки приложения, объединяющие все конфигурации.
    
    Attributes:
        DEBUG (bool): Режим отладки
        LOG_LEVEL (str): Уровень логирования
        CACHE_TTL (int): Время жизни кэша в секундах
    """
    
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    CACHE_TTL: int = 300  # 5 minutes
    
    class Config:
        """
        Конфигурация Pydantic для загрузки переменных окружения.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Описание полей для автоматической документации
        fields = {
            'POSTGRES_PASSWORD': {
                'description': 'PostgreSQL database password',
                'example': 'my_secure_password_123'
            },
            'BOT_TOKEN': {
                'description': 'MAX API bot authentication token',
                'example': 'f9LHodD0cOLdZCQzzsrZ_sKrQpZJlMrzV4cs-f9IZvKVTFNl9FIL9sjEXa9uAnUgzoD9VI1ei0LMQOp8EtL1'
            }
        }


def get_settings() -> Settings:
    """
    Фабрика для получения экземпляра настроек.
    
    Returns:
        Settings: Экземпляр настроек приложения
    """
    return Settings()


# Глобальный экземпляр настроек для использования во всем приложении
settings = get_settings()


if __name__ == "__main__":
    # Вывод информации о конфигурации при прямом запуске (для отладки)
    print("=== Application Configuration ===")
    print(f"Database URL: {settings.DATABASE_URL.replace(settings.POSTGRES_PASSWORD, '***')}")
    print(f"Bot Token: {settings.BOT_TOKEN[:10]}...")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Log Level: {settings.LOG_LEVEL}")