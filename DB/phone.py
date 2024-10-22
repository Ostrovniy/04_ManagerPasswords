from datetime import datetime
from tkinter import PhotoImage
from cripto.AesManeger import AESEncryptionManager

class PhoneTable:
    # Атрибут класса (общий для всех экземпляров)
    list_usage_tag = ['Активный', 'Старый', 'Выкинуть', 'Основной', 'Рабочий']
    def __init__(self, db_connection, password) -> None:
        self.connection = db_connection
        self.cursor = self.connection.cursor()
        self.password = password
        self.aes_manager = AESEncryptionManager(self.password)

        # настройка для отрисовки TreeviewPro
        # Название колонок
        self.list_columns_for_treeview = ['id', 'date_added', 'usage_tag', 'name', 'phone', 'pin1', 'pin2', 'puk1', 'puk2', 'description', 'last_modified']
        # Название колонок для отрисовки
        self.list_columns_name_for_treeview = ['№', 'Добавлено', 'Статус', 'Название', 'Номер', 'PIN1', 'PIN2', 'PUK1', 'PUK2', 'Комментарий', 'Изменено']
        # Динамическое изменения размера колонки при изменении размера екрана
        self.list_columns_stretch_treeview = [False, False, False, False, False, False, False, False, False, True, False]
        # Шырина колонок по умолчанию
        self.list_columns_width_treeview = [60, 120, 80, 140, 140, 60, 60, 65, 65, 0, 120]
        # Сипсок Иконок для заголовка таблицы #9FA6AD
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

        
    # Создания таблицы "Телефон"
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            usage_tag BLOB,
            usage_tag_iv BLOB,            -- Хранение в формате BLOB
            name BLOB,
            name_iv BLOB,                 -- Хранение в формате BLOB
            phone BLOB NOT NULL UNIQUE,
            phone_iv BLOB NOT NULL,       -- Хранение в формате BLOB
            pin1 BLOB,
            pin1_iv BLOB,                 -- Хранение в формате BLOB
            pin2 BLOB,
            pin2_iv BLOB,                 -- Хранение в формате BLOB
            puk1 BLOB, 
            puk1_iv BLOB,                 -- Хранение в формате BLOB
            puk2 BLOB,
            puk2_iv BLOB,                 -- Хранение в формате BLOB
            description BLOB,
            description_iv BLOB,          -- Хранение в формате BLOB
            last_modified DATETIME DEFAULT CURRENT_TIMESTAMP 
            )
        ''')
    # Метод для добавления записи в таблицу "Телефон"
    def save_encrypt_to_table(self, usage_tag=None, usage_tag_iv=None, name=None, name_iv=None, phone=None, phone_iv=None, pin1=None, pin1_iv=None, pin2=None, pin2_iv=None, puk1=None, puk1_iv=None, puk2=None, puk2_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
                INSERT INTO phone (usage_tag, usage_tag_iv, name, name_iv, phone, phone_iv, pin1, pin1_iv, pin2, pin2_iv, puk1, puk1_iv, puk2, puk2_iv, description, description_iv)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usage_tag, usage_tag_iv, name, name_iv, phone, phone_iv, pin1, pin1_iv, pin2, pin2_iv, puk1, puk1_iv, puk2, puk2_iv, description, description_iv))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись успешно добавлена.")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении телефона: {e}")
            return False

    # Запись зашыфрованного пароля
    def add_phone(self, usage_tag=None, name=None, phone=None, pin1=None, pin2=None, puk1=None, puk2=None, description=None):
        usage_tag_iv, usage_tag_encrypt = self.aes_manager.encrypt_data(usage_tag) if usage_tag is not None else (None, None) # 1) Шифрование поля "usage_tag"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        phone_iv, phone_encrypt = self.aes_manager.encrypt_data(phone) if phone is not None else (None, None) # 3) Шифрование поля "phone"
        pin1_iv, pin1_encrypt = self.aes_manager.encrypt_data(pin1) if pin1 is not None else (None, None) # 4) Шифрование поля "pin1"
        pin2_iv, pin2_encrypt = self.aes_manager.encrypt_data(pin2) if pin2 is not None else (None, None) # 5) Шифрование поля "pin2"
        puk1_iv, puk1_encrypt = self.aes_manager.encrypt_data(puk1) if puk1 is not None else (None, None) # 6) Шифрование поля "puk1"
        puk2_iv, puk2_encrypt = self.aes_manager.encrypt_data(puk2) if puk2 is not None else (None, None) # 7) Шифрование поля "puk2"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"

        # Сохранения зашыфрованных данных в таблицу
        status_add = self.save_encrypt_to_table(
            usage_tag=usage_tag_encrypt, 
            usage_tag_iv=usage_tag_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            phone=phone_encrypt, 
            phone_iv=phone_iv, 
            pin1=pin1_encrypt, 
            pin1_iv=pin1_iv, 
            pin2=pin2_encrypt, 
            pin2_iv=pin2_iv, 
            puk1=puk1_encrypt, 
            puk1_iv=puk1_iv, 
            puk2=puk2_encrypt, 
            puk2_iv=puk2_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_add
    
    # Получить сиписок всех телефонов с БД и рассыфровать их 
    # !!! get_all_data обятательное занвание
    def get_all_data(self):
        """Получить все записи из таблицы phone в виде списка словарей."""
        try:
            self.cursor.execute('SELECT * FROM phone')
            rows = self.cursor.fetchall()  # Получить все записи из запроса

            phones_list = []
            # Порядок должен быть как в переменной self.list_columns_for_treeview
            for row in rows:
                phone = {
                    'id': row[0],
                    'date_added': datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M'),
                    'usage_tag': self.aes_manager.decrypt_data(row[3], row[2]),
                    'name': self.aes_manager.decrypt_data(row[5], row[4]),
                    'phone': self.aes_manager.decrypt_data(row[7], row[6]),
                    'pin1':self.aes_manager.decrypt_data(row[9], row[8]),
                    'pin2': self.aes_manager.decrypt_data(row[11], row[10]),
                    'puk1': self.aes_manager.decrypt_data(row[13], row[12]),
                    'puk2': self.aes_manager.decrypt_data(row[15], row[14]),
                    'description': self.aes_manager.decrypt_data(row[17], row[16]),
                    'last_modified': datetime.strptime(row[18], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')
                }
                phones_list.append(phone)

            #print(phones_list)
            return phones_list
        except Exception as e:
            print(f"Ошибка при получении записей: {e}")
            return []


    # Метод для удаления телефона по ID
    def dell_phone_by_id(self, phone_id: int) -> None:
        """Удаляет запись из таблицы 'phone' по переданному ID."""
        try:
            self.cursor.execute("DELETE FROM phone WHERE id = ?", (phone_id,))
            self.connection.commit()
            print(f"Запись с ID {phone_id} успешно удалена.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при удалении записи: {e}")

    # Обновления данных в таблице по айдишнику
    def update_encrypt_in_table(self, id, usage_tag=None, usage_tag_iv=None, name=None, name_iv=None, phone=None, phone_iv=None, pin1=None, pin1_iv=None, pin2=None, pin2_iv=None, puk1=None, puk1_iv=None, puk2=None, puk2_iv=None, description=None, description_iv=None):
        try:
            self.cursor.execute('''
            UPDATE phone
            SET usage_tag = ?, usage_tag_iv = ?, name = ?, name_iv = ?, phone = ?, phone_iv = ?, pin1 = ?, pin1_iv = ?, pin2 = ?, pin2_iv = ?, puk1 = ?, puk1_iv = ?, puk2 = ?, puk2_iv = ?, description = ?, description_iv = ?, last_modified = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (usage_tag, usage_tag_iv, name, name_iv, phone, phone_iv, pin1, pin1_iv, pin2, pin2_iv, puk1, puk1_iv, puk2, puk2_iv, description, description_iv, id))
        
            self.connection.commit()  # Сохранение изменений в БД
            print(f"Запись с id={id} успешно обновлена.")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении телефона с id={id}: {e}")
            return False
        
    # Зашыфровака данных и обновления в таблцие по айдишнику
    def edit_phone(self, id, usage_tag=None, name=None, phone=None, pin1=None, pin2=None, puk1=None, puk2=None, description=None):
        usage_tag_iv, usage_tag_encrypt = self.aes_manager.encrypt_data(usage_tag) if usage_tag is not None else (None, None) # 1) Шифрование поля "usage_tag"
        name_iv, name_encrypt = self.aes_manager.encrypt_data(name) if name is not None else (None, None) # 2) Шифрование поля "name"
        phone_iv, phone_encrypt = self.aes_manager.encrypt_data(phone) if phone is not None else (None, None) # 3) Шифрование поля "phone"
        pin1_iv, pin1_encrypt = self.aes_manager.encrypt_data(pin1) if pin1 is not None else (None, None) # 4) Шифрование поля "pin1"
        pin2_iv, pin2_encrypt = self.aes_manager.encrypt_data(pin2) if pin2 is not None else (None, None) # 5) Шифрование поля "pin2"
        puk1_iv, puk1_encrypt = self.aes_manager.encrypt_data(puk1) if puk1 is not None else (None, None) # 6) Шифрование поля "puk1"
        puk2_iv, puk2_encrypt = self.aes_manager.encrypt_data(puk2) if puk2 is not None else (None, None) # 7) Шифрование поля "puk2"
        description_iv, description_encrypt = self.aes_manager.encrypt_data(description) if description is not None else (None, None) # 8) Шифрование поля "description"

        # Обновление зашифрованных данных в таблице
        status_update = self.update_encrypt_in_table(
            id=id,
            usage_tag=usage_tag_encrypt, 
            usage_tag_iv=usage_tag_iv, 
            name=name_encrypt, 
            name_iv=name_iv, 
            phone=phone_encrypt, 
            phone_iv=phone_iv, 
            pin1=pin1_encrypt, 
            pin1_iv=pin1_iv, 
            pin2=pin2_encrypt, 
            pin2_iv=pin2_iv, 
            puk1=puk1_encrypt, 
            puk1_iv=puk1_iv, 
            puk2=puk2_encrypt, 
            puk2_iv=puk2_iv, 
            description=description_encrypt, 
            description_iv=description_iv
        )

        return status_update



    
    
