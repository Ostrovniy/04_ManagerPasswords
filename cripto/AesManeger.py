import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class AESEncryptionManager:
    def __init__(self, password: str):
        self.key = self._generate_key_from_password(password)

    # Приватный метод для генерации ключа на основе пароля с использованием SHA-256
    @staticmethod
    def _generate_key_from_password(password: str) -> bytes:
        return hashlib.sha256(password.encode()).digest()

    # Шифрование данных с использованием AES-шифрования в режиме CBC и случайного IV
    def encrypt_data(self, plaintext: str) -> (bytes, bytes): # type: ignore
        iv = os.urandom(16)  # Генерация случайного IV (инициализационный вектор)

        # Добавляем padding, чтобы данные были кратны блоку AES (16 байт)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # Создаем объект Cipher для AES с режимом CBC и шифруем данные
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    # Расшифровка данных, зашифрованных с использованием AES (CBC)
    def decrypt_data(self, iv: bytes, ciphertext: bytes) -> str:
        # Создаем объект Cipher для AES с режимом CBC и расшифровываем данные
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Убираем padding, который был добавлен при шифровании
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()

