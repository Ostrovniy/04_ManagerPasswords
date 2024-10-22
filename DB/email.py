from datetime import datetime
from tkinter import PhotoImage
from cripto.AesManeger import AESEncryptionManager

class EmailTable:
    # Атрибут класса (общий для всех экземпляров)
    list_email_type = ['Google', 'Mail', 'Yahoo', 'Outlook', 'Yandex', 'ProtonMail']
    def __init__(self, db_connection, password) -> None:
        # Соидинения
        self.connection = db_connection
        # Курсор
        self.cursor = self.connection.cursor()
        # Пароль для шыфроки и дышифровки
        self.password = password
        # Менеджер шыфрования и рассыфрования
        self.aes_manager = AESEncryptionManager(self.password)

        # настройка для отрисовки TreeviewPro, название нельзя менять
        # Название колонок
        self.list_columns_for_treeview = ['id', 'date_added', 'email_type', 'name', 'login', 'password', 'phonerestore', 'backupmail', 'description', 'last_modified']
        # Название колонок для отрисовки
        self.list_columns_name_for_treeview = ['№', 'Добавлено', 'Тип почты', 'Название', 'Логин', 'Пароль', 'Телефон вост.', 'Резервная почта', 'Комментарий', 'Изменено']
        # Динамическое изменения размера колонки при изменении размера екрана
        self.list_columns_stretch_treeview = [False, False, False, False, False, False, False, False, True, False]
        # Шырина колонок по умолчанию
        self.list_columns_width_treeview = [60, 120, 110, 140, 140, 100, 170, 170, 0, 120]
        # Сипсок Иконок для заголовка таблицы #9FA6AD
        self.list_columns_icons_treeview = [PhotoImage(file='img\\id.png'), 
                                            PhotoImage(file='img\\date.png'), 
                                            PhotoImage(file='img\\status.png'), 
                                            PhotoImage(file='img\\name.png'),
                                            PhotoImage(file='img\\email.png'),
                                            PhotoImage(file='img\\pin.png'),
                                            PhotoImage(file='img\\phone.png'),
                                            PhotoImage(file='img\\email.png'),
                                            PhotoImage(file='img\\comment.png'),
                                            PhotoImage(file='img\\editdate.png')
                                            ]

     # Создания таблицы "Почта"
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            email_type BLOB,
            email_type_iv BLOB,            -- Хранение в формате BLOB
            name BLOB,
            name_iv BLOB,                 -- Хранение в формате BLOB
            login BLOB,
            login_iv BLOB,       -- Хранение в формате BLOB
            password BLOB,
            password_iv BLOB,                 -- Хранение в формате BLOB
            phonerestore BLOB,
            phonerestore_iv BLOB,                 -- Хранение в формате BLOB
            backupmail BLOB, 
            backupmail_iv BLOB,                 -- Хранение в формате BLOB
            description BLOB,
            description_iv BLOB,          -- Хранение в формате BLOB
            last_modified DATETIME DEFAULT CURRENT_TIMESTAMP 
            )
        ''')
    
    # Метод для добавления записи в таблицу "Телефон"
    def save_encrypt_to_table(self, email_type=None, email_type_iv=None, name=None, name_iv=None, login=None, login_iv=None, password=None, password_iv=None, phonerestore=None, phonerestore_iv=None, backupmail=None, backupmail_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
                INSERT INTO email (email_type, email_type_iv, name, name_iv, login, login_iv, password, password_iv, phonerestore, phonerestore_iv, backupmail, backupmail_iv, description, description_iv)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email_type, email_type_iv, name, name_iv, login, login_iv, password, password_iv, phonerestore, phonerestore_iv, backupmail, backupmail_iv,  description, description_iv))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись успешно добавлена.")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении почты: {e}")
            return False
        
    # Шыфровка и добавления данных в бд 
    def add_email(self, email_type=None, name=None, login=None, password=None, phonerestore=None, backupmail=None, description=None):
        email_type_iv, email_type_encrypt = self.aes_manager.encrypt_data(email_type) if email_type is not None else (None, None) # 1) Шифрование поля "email_type"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        login_iv, login_encrypt = self.aes_manager.encrypt_data(login) if login is not None else (None, None) # 3) Шифрование поля "login"
        password_iv, password_encrypt = self.aes_manager.encrypt_data(password) if password is not None else (None, None) # 4) Шифрование поля "password"
        phonerestore_iv, phonerestore_encrypt = self.aes_manager.encrypt_data(phonerestore) if phonerestore is not None else (None, None) # 5) Шифрование поля "phonerestore"
        backupmail_iv, backupmail_encrypt = self.aes_manager.encrypt_data(backupmail) if backupmail is not None else (None, None) # 6) Шифрование поля "backupmail"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"

        # Сохранения зашыфрованных данных в таблицу
        status_add = self.save_encrypt_to_table(
            email_type=email_type_encrypt, 
            email_type_iv=email_type_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            login=login_encrypt, 
            login_iv=login_iv, 
            password=password_encrypt, 
            password_iv=password_iv, 
            phonerestore=phonerestore_encrypt, 
            phonerestore_iv=phonerestore_iv, 
            backupmail=backupmail_encrypt, 
            backupmail_iv=backupmail_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_add

    # Получить сиписок всех email
    # get_all_data обязательное название
    def get_all_data(self):
        """Получить все записи из таблицы email в виде списка словарей."""
        try:
            self.cursor.execute('SELECT * FROM email')
            rows = self.cursor.fetchall()  # Получить все записи из запроса

            emails_list = []
            # Порядок должен быть как в переменной self.list_columns_for_treeview
            for row in rows:
                email = {
                    'id': row[0],
                    'date_added': datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M'),
                    'email_type': self.aes_manager.decrypt_data(row[3], row[2]),
                    'name': self.aes_manager.decrypt_data(row[5], row[4]),
                    'login': self.aes_manager.decrypt_data(row[7], row[6]),
                    'password':self.aes_manager.decrypt_data(row[9], row[8]),
                    'phonerestore': self.aes_manager.decrypt_data(row[11], row[10]),
                    'backupmail': self.aes_manager.decrypt_data(row[13], row[12]),
                    'description': self.aes_manager.decrypt_data(row[15], row[14]),
                    'last_modified': datetime.strptime(row[16], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')
                }
                emails_list.append(email)

            return emails_list
        except Exception as e:
            print(f"Ошибка при получении записей: {e}")
            return []
    
    # Метод для удаления email по ID
    def dell_email_by_id(self, email_id: int) -> None:
        """Удаляет запись из таблицы 'email' по переданному ID."""
        try:
            self.cursor.execute("DELETE FROM email WHERE id = ?", (email_id,))
            self.connection.commit()
            print(f"Запись с ID {email_id} успешно удалена.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при удалении записи: {e}")

    
    # Обновления данных в таблице по айдишнику
    def update_encrypt_in_table(self, id, email_type=None, email_type_iv=None, name=None, name_iv=None, login=None, login_iv=None, password=None, password_iv=None, phonerestore=None, phonerestore_iv=None, backupmail=None, backupmail_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
            UPDATE email
            SET email_type = ?, email_type_iv = ?, name = ?, name_iv = ?, login = ?, login_iv = ?, password = ?, password_iv = ?, phonerestore = ?, phonerestore_iv = ?, backupmail = ?, backupmail_iv = ?, description = ?, description_iv = ?, last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (email_type, email_type_iv, name, name_iv, login, login_iv, password, password_iv, phonerestore, phonerestore_iv, backupmail, backupmail_iv, description, description_iv, id))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись с id={id} успешно обновлена.")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении email с id={id}: {e}")
            return False
        
    # Зашыфровака данных и обновления в таблцие по айдишнику
    def edit_email(self, id, email_type=None, name=None, login=None, password=None, phonerestore=None, backupmail=None, description=None):
        email_type_iv, email_type_encrypt = self.aes_manager.encrypt_data(email_type) if email_type is not None else (None, None) # 1) Шифрование поля "email_type"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        login_iv, login_encrypt = self.aes_manager.encrypt_data(login) if login is not None else (None, None) # 3) Шифрование поля "login"
        password_iv, password_encrypt = self.aes_manager.encrypt_data(password) if password is not None else (None, None) # 4) Шифрование поля "password"
        phonerestore_iv, phonerestore_encrypt = self.aes_manager.encrypt_data(phonerestore) if phonerestore is not None else (None, None) # 5) Шифрование поля "phonerestore"
        backupmail_iv, backupmail_encrypt = self.aes_manager.encrypt_data(backupmail) if backupmail is not None else (None, None) # 6) Шифрование поля "backupmail"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"

        # Обновление зашифрованных данных в таблице
        status_update = self.update_encrypt_in_table(
            id=id,
            email_type=email_type_encrypt, 
            email_type_iv=email_type_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            login=login_encrypt, 
            login_iv=login_iv, 
            password=password_encrypt, 
            password_iv=password_iv, 
            phonerestore=phonerestore_encrypt, 
            phonerestore_iv=phonerestore_iv, 
            backupmail=backupmail_encrypt, 
            backupmail_iv=backupmail_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_update