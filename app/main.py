import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from secure.security import register_user, authorize_user, hash_password, verify_password
from migrations.database import conn, cursor


def main():
    """Главное меню приложения"""
    while True:
        print("\n=== Система управления пользователями ===")
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Хэширование пароля")
        print("4. Проверка пароля")
        print("5. Выход")
        
        choice = input("\nВыберите действие (1-5): ").strip()
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            hash_password_menu()
        elif choice == "4":
            verify_password_menu()
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def register():
    """Регистрация нового пользователя"""
    print("\n--- Регистрация ---")
    username = input("Введите имя пользователя: ").strip()
    password = input("Введите пароль: ").strip()
    
    if not username or not password:
        print("Имя пользователя и пароль не могут быть пустыми!")
        return
    
    if register_user(username, password, cursor, conn):
        print("✅ Пользователь успешно зарегистрирован!")
    else:
        print("❌ Пользователь с таким именем уже существует!")


def login():
    """Авторизация пользователя"""
    print("\n--- Авторизация ---")
    username = input("Введите имя пользователя: ").strip()
    password = input("Введите пароль: ").strip()
    
    if not username or not password:
        print("Имя пользователя и пароль не могут быть пустыми!")
        return
    
    if authorize_user(username, password, cursor):
        print("✅ Авторизация успешна!")
    else:
        print("❌ Неверное имя пользователя или пароль!")


def hash_password_menu():
    """Хэширование пароля"""
    print("\n--- Хэширование пароля ---")
    password = input("Введите пароль для хэширования: ").strip()
    
    if not password:
        print("Пароль не может быть пустым!")
        return
    
    hashed = hash_password(password)
    print(f"Хэшированный пароль: {hashed}")


def verify_password_menu():
    """Проверка пароля"""
    print("\n--- Проверка пароля ---")
    hashed_password = input("Введите хэшированный пароль: ").strip()
    password = input("Введите пароль для проверки: ").strip()
    
    if not hashed_password or not password:
        print("Хэшированный пароль и пароль не могут быть пустыми!")
        return
    
    if verify_password(hashed_password, password):
        print("✅ Пароль совпадает!")
    else:
        print("❌ Пароль не совпадает!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()