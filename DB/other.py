from datetime import datetime
from tkinter import PhotoImage
from cripto.AesManeger import AESEncryptionManager

class OtherTable:
    # Атрибут класса (общий для всех экземпляров)
    list_grup = ['Telegram', 'Instagram', 'Facebook', 'X', 'Другое']

    def __init__(self, db_connection, password) -> None:
        self.connection = db_connection
        self.cursor = self.connection.cursor()
        self.password = password
        self.aes_manager = AESEncryptionManager(self.password)

        # настройка для отрисовки TreeviewPro
        # Название колонок
        self.list_columns_for_treeview = ['id', 'date_added', 'grup', 'name', 'login', 'password', 'phone', 'email', 'url', 'description', 'last_modified']
        # Название колонок для отрисовки
        self.list_columns_name_for_treeview = ['№', 'Добавлено', 'Статус', 'Название', 'Логин', 'Пароль', 'Телефон', 'Почта', 'Ссылка', 'Комментарий', 'Изменено']
        # Динамическое изменения размера колонки при изменении размера екрана
        self.list_columns_stretch_treeview = [False, False, False, False, False, False, False, False, False, True, False]
        # (Подогнать)Шырина колонок по умолчанию
        self.list_columns_width_treeview = [60, 120, 80, 140, 140, 100, 100, 100, 100, 0, 120]
        # (Подогнать) Сипсок Иконок для заголовка таблицы #9FA6AD
        self.list_columns_icons_treeview = [PhotoImage(file='img\\id.png'), 
                                            PhotoImage(file='img\\date.png'), 
                                            PhotoImage(file='img\\status.png'), 
                                            PhotoImage(file='img\\name.png'),
                                            PhotoImage(file='img\\phone.png'),
                                            PhotoImage(file='img\\pin.png'),
                                            PhotoImage(file='img\\pin.png'),
                                            PhotoImage(file='img\\pin.png'),
                                            PhotoImage(file='img\\pin.png'),
                                            PhotoImage(file='img\\comment.png'),
                                            PhotoImage(file='img\\editdate.png')
                                            ]

    # Создания таблицы "Другое"
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS other (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            grup BLOB,
            grup_iv BLOB,            -- Хранение в формате BLOB
            name BLOB,
            name_iv BLOB,                 -- Хранение в формате BLOB
            login BLOBE,
            login_iv BLOB,                  -- Хранение в формате BLOB
            password BLOB,
            password_iv BLOB,                 -- Хранение в формате BLOB
            phone BLOB,
            phone_iv BLOB,                 -- Хранение в формате BLOB
            email BLOB, 
            email_iv BLOB,                 -- Хранение в формате BLOB
            url BLOB,
            url_iv BLOB,                 -- Хранение в формате BLOB
            description BLOB,
            description_iv BLOB,          -- Хранение в формате BLOB
            last_modified DATETIME DEFAULT CURRENT_TIMESTAMP 
            )
        ''')

    # Метод для добавления записи в таблицу "other"
    def save_encrypt_to_table(self, grup=None, grup_iv=None, name=None, name_iv=None, login=None, login_iv=None, password=None, password_iv=None, phone=None, phone_iv=None, email=None, email_iv=None, url=None, url_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
                INSERT INTO other (grup, grup_iv, name, name_iv, login, login_iv, password, password_iv, phone, phone_iv, email, email_iv, url, url_iv, description, description_iv)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (grup, grup_iv, name, name_iv, login, login_iv, password, password_iv, phone, phone_iv, email, email_iv, url, url_iv, description, description_iv))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись успешно добавлена.")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении other: {e}")
            return False

    # Запись зашыфрованного пароля
    def add_other(self, grup=None, name=None, login=None, password=None, phone=None, email=None, url=None, description=None):
        grup_iv, grup_encrypt = self.aes_manager.encrypt_data(grup) if grup is not None else (None, None) # 1) Шифрование поля "grup"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        login_iv, login_encrypt = self.aes_manager.encrypt_data(login) if login is not None else (None, None) # 3) Шифрование поля "login"
        password_iv, password_encrypt = self.aes_manager.encrypt_data(password) if password is not None else (None, None) # 4) Шифрование поля "password"
        phone_iv, phone_encrypt = self.aes_manager.encrypt_data(phone) if phone is not None else (None, None) # 5) Шифрование поля "phone"
        email_iv, email_encrypt = self.aes_manager.encrypt_data(email) if email is not None else (None, None) # 6) Шифрование поля "email"
        url_iv, url_encrypt = self.aes_manager.encrypt_data(url) if url is not None else (None, None) # 7) Шифрование поля "url"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"

        # Сохранения зашыфрованных данных в таблицу
        status_add = self.save_encrypt_to_table(
            grup=grup_encrypt, 
            grup_iv=grup_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            login=login_encrypt, 
            login_iv=login_iv, 
            password=password_encrypt, 
            password_iv=password_iv, 
            phone=phone_encrypt, 
            phone_iv=phone_iv, 
            email=email_encrypt, 
            email_iv=email_iv, 
            url=url_encrypt, 
            url_iv=url_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_add
    
    # Получить сиписок всех other с БД и рассыфровать их  !!! get_all_data обятательное занвание
    def get_all_data(self):
        """Получить все записи из таблицы other в виде списка словарей."""
        try:
            self.cursor.execute('SELECT * FROM other')
            rows = self.cursor.fetchall()  # Получить все записи из запроса

            other_list = []
            # Порядок должен быть как в переменной self.list_columns_for_treeview
            for row in rows:
                other = {
                    'id': row[0],
                    'date_added': datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M'),
                    'grup': self.aes_manager.decrypt_data(row[3], row[2]),
                    'name': self.aes_manager.decrypt_data(row[5], row[4]),
                    'login': self.aes_manager.decrypt_data(row[7], row[6]),
                    'password':self.aes_manager.decrypt_data(row[9], row[8]),
                    'phone': self.aes_manager.decrypt_data(row[11], row[10]),
                    'email': self.aes_manager.decrypt_data(row[13], row[12]),
                    'url': self.aes_manager.decrypt_data(row[15], row[14]),
                    'description': self.aes_manager.decrypt_data(row[17], row[16]),
                    'last_modified': datetime.strptime(row[18], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')
                }
                other_list.append(other)

            return other_list
        except Exception as e:
            print(f"Ошибка при получении записей: {e}")
            return []

    # Метод для удаления other по ID
    def dell_other_by_id(self, other_id: int) -> None:
        """Удаляет запись из таблицы 'other' по переданному ID."""
        try:
            self.cursor.execute("DELETE FROM other WHERE id = ?", (other_id,))
            self.connection.commit()
            print(f"Запись с ID {other_id} успешно удалена.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при удалении записи: {e}")

    # Обновления данных в таблице по айдишнику
    def update_encrypt_in_table(self, id, grup=None, grup_iv=None, name=None, name_iv=None, login=None, login_iv=None, password=None, password_iv=None, phone=None, phone_iv=None, email=None, email_iv=None, url=None, url_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
            UPDATE other
            SET grup = ?, grup_iv = ?, name = ?, name_iv = ?, login = ?, login_iv = ?, password = ?, password_iv = ?, phone = ?, phone_iv = ?, email = ?, email_iv = ?, url = ?, url_iv = ?, description = ?, description_iv = ?, last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (grup, grup_iv, name, name_iv, login, login_iv, password, password_iv, phone, phone_iv, email, email_iv, url, url_iv, description, description_iv, id))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись с id={id} успешно обновлена.")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении телефона с id={id}: {e}")
            return False
        
    # Зашыфровака данных и обновления в таблцие по айдишнику
    def edit_other(self, id, grup=None, name=None, login=None, password=None, phone=None, email=None, url=None, description=None):
        grup_iv, grup_encrypt = self.aes_manager.encrypt_data(grup) if grup is not None else (None, None) # 1) Шифрование поля "grup"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        login_iv, login_encrypt = self.aes_manager.encrypt_data(login) if login is not None else (None, None) # 3) Шифрование поля "login"
        password_iv, password_encrypt = self.aes_manager.encrypt_data(password) if password is not None else (None, None) # 4) Шифрование поля "password"
        phone_iv, phone_encrypt = self.aes_manager.encrypt_data(phone) if phone is not None else (None, None) # 5) Шифрование поля "phone"
        email_iv, email_encrypt = self.aes_manager.encrypt_data(email) if email is not None else (None, None) # 6) Шифрование поля "email"
        url_iv, url_encrypt = self.aes_manager.encrypt_data(url) if url is not None else (None, None) # 7) Шифрование поля "url"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"


        # Обновление зашифрованных данных в таблице
        status_update = self.update_encrypt_in_table(
            id=id,
            grup=grup_encrypt, 
            grup_iv=grup_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            login=login_encrypt, 
            login_iv=login_iv, 
            password=password_encrypt, 
            password_iv=password_iv, 
            phone=phone_encrypt, 
            phone_iv=phone_iv, 
            email=email_encrypt, 
            email_iv=email_iv, 
            url=url_encrypt, 
            url_iv=url_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_update



    
    
