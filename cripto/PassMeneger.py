import os
from argon2 import PasswordHasher, exceptions

# Менеджер пароля, для регистарции и авторизации пользователя
class PasswordManager:
    def __init__(self):
        self.ph = PasswordHasher()

    # Генерирует случайную соль (16 байт) и возвращает её в виде строки.
    def generate_salt(self):
        return os.urandom(16).hex()

    # Хеширует пароль с использованием соли и возвращает хеш.
    def hash_password(self, password: str, salt: str) -> str:
        return self.ph.hash(password + salt)

    # Авторизация пользователя, сверка хешей
    def authorization(self, saved_salt: str, saved_hash: str, input_password: str) -> bool:
        try:
            self.ph.verify(saved_hash, input_password + saved_salt)
            return True
        except exceptions.VerifyMismatchError:
            return False
    
    # Регистрация пользователя
    def registration(self, password: str):
        salt = self.generate_salt() # Сренерировать соль
        hashed_password = self.hash_password(password, salt) # Получить хеш пароля
        return salt, hashed_password


