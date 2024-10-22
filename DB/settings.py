import sqlite3

class SettingsTable:
    def __init__(self, db_connection):
        self.connection = db_connection
        self.cursor = self.connection.cursor()
        self.col = ['id', 'date_added', 'hash_passwort', 'salt']

    # Создать таблицу с настройками
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_added DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                hash_passwort TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')

    # Проверить, пуста ли таблица
    def is_table_empty(self) -> bool:
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        row_count = self.cursor.fetchone()[0]
        return row_count == 0

    # Добавить запись в таблицу
    def add_registration(self, settings: dict):
        query = '''INSERT INTO settings (hash_passwort, salt) VALUES (?, ?)'''

        self.cursor.execute(query, (settings['hash_passwort'], settings['salt']))
        self.connection.commit()
        print('Настройки добавлены')
    
    # Получить 
    def get_hash_and_sale_password(self):
        self.cursor.execute('SELECT hash_passwort, salt FROM settings')
        return self.cursor.fetchone()



