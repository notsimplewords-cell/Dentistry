from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import psycopg2
from typing import Optional


# Создаем объект хэшера с параметрами по умолчанию
ph = PasswordHasher()


def register_user(username: str, password: str, cursor, conn) -> bool:
    """
    Функция регистрации пользователя с Argon2
    
    Args:
        username: Имя пользователя
        password: Пароль
        cursor: Курсор базы данных
        conn: Соединение с базой данных
    
    Returns:
        bool: True если регистрация успешна, False если пользователь уже существует
    """
    # Хэширование пароля
    password_hash = ph.hash(password)
    
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', 
                      (username, password_hash))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        # Пользователь с таким именем уже существует
        return False


def authorize_user(username: str, password: str, cursor) -> bool:
    """
    Функция авторизации пользователя с Argon2
    
    Args:
        username: Имя пользователя
        password: Пароль
        cursor: Курсор базы данных
    
    Returns:
        bool: True если авторизация успешна, False если пользователь не найден или пароль неверный
    """
    cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
    result = cursor.fetchone()
    
    if result is None:
        return False  # Пользователь не найден
    
    stored_hash = result[0]
    
    try:
        # Проверяем пароль с помощью Argon2
        return ph.verify(stored_hash, password)
    except VerifyMismatchError:
        return False  # Пароль неверный


def hash_password(password: str) -> str:
    """
    Хэширование пароля
    
    Args:
        password: Пароль для хэширования
    
    Returns:
        str: Хэшированный пароль
    """
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """
    Проверка пароля
    
    Args:
        hashed_password: Хэшированный пароль
        password: Пароль для проверки
    
    Returns:
        bool: True если пароль совпадает, False если нет
    """
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False