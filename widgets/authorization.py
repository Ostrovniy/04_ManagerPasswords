import re
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from widgets.pro import InputGroupFrame, ButtonPro
from cripto.PassMeneger import PasswordManager
from DB.settings import SettingsTable

# Фрейм: Добавить телефон в БД
class Authorization(tk.LabelFrame):
    def __init__(self, parent, settings_table:SettingsTable, load_mainapp):
        """Шаг 8: Создаем фрейм Авторизации, получаем 
                Менеджер паролей: PasswordManager - для хешырования пароля, проверки хеша пароли
                Таблицу найстроки: SettingsTable - для работы с таблицей где храняться хеш пароля, соль
                load_mainapp - функция запуска главного врейма, если авториазция успешная 
        """
        super().__init__(parent, text="Введите пароль доступа", bd=1, relief="groove", bg='#121212', fg='#ffefe1')
        self.pack()

        self.settings_table = settings_table
        self.password_manager = PasswordManager()
        self.load_mainapp = load_mainapp


        self.password = InputGroupFrame(self, title='Введите пароль')
        self.password.pack(anchor='w')

        self.btn = ButtonPro(self, text='Войти', command=self.click_btn)
        self.btn.pack(anchor='w', padx=5, pady=5)

    # Обработка нажатия кнопки "Войти"
    def click_btn(self):
        """Шаг 9: Обработка нажатия кнопки войти, при которой проверяеться введенный пароль с сохранненым хешем в БД

                self.password.input.get_input_data() - текущий введенны пароль
                hash_password, salt - хеш пароля и соль пароля, которая хранитсья в БД
                self.password_manager.authorization - проверяет текущий парол, на подленность
                self.load_mainapp(input_password) - Запуск функции отрисовки главноего приложения с передачей пароля для 
                дальнейшер шыфровки и рассыфровки данных
        """
        # Проверка что пароль не пустой
        if self.password.input.get_input_data():
            # Получить Хеш и Соль с БЛ для Аунтификации
            hash_password, salt = self.settings_table.get_hash_and_sale_password()
            input_password = self.password.input.get_input_data()

            # Сверка хеша БД с веденным паролем
            if self.password_manager.authorization(salt, hash_password, input_password):
                self.load_mainapp(input_password) # Запустить фрейм Главного приложения с меню с передачей ему пароля
            else:
                showerror('Ошибка', 'Неверный пароль')
                return
        else:
            showerror('Ошибка', 'Пароль не может быть пустым')
            return



