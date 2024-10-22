# Manager Passwords

Менеджер паролей, который позволяет безопасно хранить свои пароли, PIN-коды и другую информацию. Все данные зашифрованы, и доступ к ним возможен только при вводе главного пароля.

## Как пользоваться

1. При первом запуске приложения установите главный пароль, который будет использоваться для входа и шифрования данных.
2. В менеджере есть три раздела:
   - **Телефоны**: хранение информации о телефонах, PIN-коды, PUK-коды и другие данные.
   - **Email**: хранение данных о почтовых аккаунтах, таких как email, пароли, телефон для восстановления, тип почты и т.д.
   - **Другое**: хранение любых других паролей или данных.
3. Все поля в базе данных зашифрованы.
4. Если вы забудете главный пароль, доступ ко всем записям будет утрачен.
5. Для полного сброса приложения удалите локальный файл базы данных `password_storage.db`.

![Пример работы](img/Screenshot.jpg)

### Шифрование данных

Программа использует алгоритм шифрования AES (Advanced Encryption Standard) в режиме CBC (Cipher Block Chaining) для обеспечения безопасности данных.

1. **Генерация ключа**:
   - Ключ для шифрования и расшифровки генерируется на основе главного пароля с использованием хэширования SHA-256.

2. **Шифрование данных**:
   - Перед шифрованием генерируется случайный IV (инициализационный вектор) для уникальности каждого шифрования.
   - Данные автоматически дополняются (padding) для соответствия блоку AES (16 байт).
   - Данные шифруются с использованием алгоритма AES и режима CBC.

3. **Расшифровка данных**:
   - Данные расшифровываются с использованием того же ключа и IV, которые были применены при шифровании.
   - Padding, добавленный при шифровании, удаляется, и данные возвращаются в исходном виде.

### Важное предупреждение

Не забывайте главный пароль, так как это единственный способ получить доступ ко всем данным.