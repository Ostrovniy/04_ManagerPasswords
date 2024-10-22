import re
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from widgets.pro import InputGroupFrame, ButtonPro
from cripto.PassMeneger import PasswordManager
from DB.settings import SettingsTable

# Фрейм: Добавить телефон в БД
class Registration(tk.LabelFrame):
    
    def __init__(self, parent, settings_table: SettingsTable, load_authorization):
        """Шаг 4: Создаем фрейм Регистрации, получаем 
                Менеджер паролей: PasswordManager - для хешырования пароля, проверки хеша пароли
                Таблицу найстроки: SettingsTable - для работы с таблицей где храняться хеш пароля, соль
                load_authorization - функция запуска фрейма Авторизации   
        """

        super().__init__(parent, text="Регистрация аккаунта", bd=1, relief="groove", bg='#121212', fg='#ffefe1')
        #self.pack(fill="both", expand=True, ipadx=2, ipady=2)
        self.pack()

        self.password_manager = PasswordManager() # менеджер паролей
        self.settings_table = settings_table # Таблица настройки
        self.load_authorization = load_authorization # Ссфлка на функцию, запуску фрейма авторизации

        self.password1 = InputGroupFrame(self, title='Введите пароль')
        self.password1.pack(anchor='w')

        self.password2 = InputGroupFrame(self, title='Подтвердире пароль')
        self.password2.pack(anchor='w')

        self.btn = ButtonPro(self, text='Регистрация', command=self.click_btn)
        self.btn.pack(anchor='w', padx=5, pady=5)

    # Обработка нажатия события
    def click_btn(self):
        """Шаг 5: Обработка нажатия кнопки "Регистрация" идет простая валидация паролей, и если все прошло успешно создаеться
            salt, hash_password - соль (случайная), хеш введенного пароля
            add_registration - добавляеться соль и хеш пароля в Таблицу Регистрации
            load_authorization - запускаеться функция Авторизациия, и переходим с шага Регистрации на Наш Авторизации
        """
        pass1 = self.password1.input.get_input_data()
        pass2 = self.password2.input.get_input_data()
        if len(pass1) < 5:
            showerror('Ошибка', 'Длина пароля должна быть больше 5 символов')
            return
        if pass1 != pass2:
            showerror('Ошибка', 'Пароли не совпадают, повториет ввод')
            return
        
        # Получить Хеш и Соль для введенного пароля
        salt, hash_password = self.password_manager.registration(pass1)
        # Сохранить Хеш и Соль в БД (Пользователь зарегестрировался)
        self.settings_table.add_registration({'hash_passwort': hash_password,'salt': salt})
        self.load_authorization() # Запустить фрейм авторизации
