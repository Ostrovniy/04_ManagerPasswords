import tkinter as tk
from DB.database import Database
from DB.email import EmailTable
from DB.other import OtherTable
from DB.settings import SettingsTable
from DB.phone import PhoneTable
from widgets.email.email_page import MainEmail
from widgets.other.other_page import MainOther
from widgets.phone.table import ListPhones
from widgets.phone.phone_page import MainPhone
from cripto.PassMeneger import PasswordManager
from widgets.phone.form import FromPhone
from widgets.registration import Registration
from widgets.authorization import Authorization
#from cripto.AesManeger import AESEncryptionManager

class MainApp(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()

        self.title("Meneger Passwords")
        self.geometry("1700x700")
        self.option_add("*tearOff", tk.FALSE) # Отключения отсоиденения окна с меню
        #self.style = ttk.Style(self)
        #self.style.theme_use("default") #default
        self.configure(bg='#0e1621')

        # Создаем менедреж БД и создаем подключения
        self.db = Database('password_storeg.db')
        self.main_conect = self.db.connect()

        # Передаем подлючения для работы с таблице и курсор создаеться внутри
        self.settings_table = SettingsTable(self.main_conect)
        # Создать таблицу с настройками
        self.settings_table.create_table()


        self.password_manager = PasswordManager()

        # Фрейм для загрузки виджетов
        self.widget_frame = tk.Frame(self, bg='#121212')
        self.widget_frame.pack(expand=True, fill=tk.BOTH)

        """Шаг 1: Проверйем пользовател зарегестрирован или нет, у него должна быть запись в таблице регистрации с Хешем пароля"""
        if self.settings_table.is_table_empty():
            """Шаг 2: Если записи нету, запускаем фрейм и просим Резерестрироваться, перейти в метод load_registration"""
            self.load_registration()
        else:
            """Шаг 6: Авторизация запускаеться при двух условиях
                1. Оператор if выше не отработал, что значит что регистрация уже прошла и запускаеться load_authorization
                2. В Классе Registration после регистрации вызываеться load_authorization, это нужно потому что мы находимя в __init__
            """
            self.load_authorization()
        
        
    # ТОЧКА ВХОДА ПОСЛЕ АВТОРИЗАЦИИ
    def load_mainapp(self, input_password):
        """Шаг 10: Запуск главного приложения, отрисовка главного фрейма, после успешной регистрации и авторизации
            self.password - введнный пароль который нам передал модуль Авторизации
            self.create_main_menu() - Создания основного меню
            self.load_addPhone() - Отрисовка галвного фрейма приложения
        """
        self.password = input_password # пароль доступа, для шыфрования и расшыфрования
        self.create_main_menu() # Создание меню

        # Создание таблицы с Телефонами и
        self.phone_table = PhoneTable(self.main_conect, self.password)
        self.phone_table.create_table()

        # Создание таблицы с Email
        self.email_table = EmailTable(self.main_conect, self.password)
        self.email_table.create_table()

        # Создание таблицы с Other
        self.other_table = OtherTable(self.main_conect, self.password)
        self.other_table.create_table()

        self.load_main_phone() # загрузка главного окошка

    # Создание главного меню, вынесено отдельно что бы не мешало
    def create_main_menu(self):
        # Создание меню
        self.main_menu = tk.Menu() # Главное меню bg='#090f16'
        self.password_nemu = tk.Menu() # Под меню друзей

        # Пункты главного меню
        self.main_menu.add_cascade(label='Пароли', menu=self.password_nemu)

        # Подпункты "Телефоны"
        self.password_nemu.add_command(label="Телефоны", command=self.load_main_phone)
        self.password_nemu.add_command(label="Email", command=self.load_main_email)
        self.password_nemu.add_command(label="Other", command=self.load_main_other)
        self.config(menu=self.main_menu)

    
    def load_main_phone(self):
        """Страница работы с мобильным телефоном"""
        self.clear_frame()
        self.main_phone = MainPhone(self.widget_frame, self.phone_table)
        self.main_phone.pack(expand=True, fill=tk.BOTH)

    def load_main_email(self):
        """Страница работы с email"""
        self.clear_frame()
        self.main_email = MainEmail(self.widget_frame, self.email_table)
        self.main_email.pack(expand=True, fill=tk.BOTH)

    def load_main_other(self):
        """Страница работы с other"""
        self.clear_frame()
        self.main_other = MainOther(self.widget_frame, self.other_table)
        self.main_other.pack(expand=True, fill=tk.BOTH)

    # Загрузить фрейм "Авторизация"
    def load_authorization(self):
        """Шаг 7: Очистить главный фрейм, и Разместить фрейм Authorization, перейти в него"""
        self.clear_frame()
        self.authorization = Authorization(self.widget_frame, self.settings_table, self.load_mainapp)
        self.authorization.pack(anchor='center', padx=10, pady=200) # размещения по центру

    # Загрузить фрейм "Регистрациия"
    def load_registration(self):
        """Шаг 3: Очистить главный фрейм, и Разместить фрейм Registration, перейти в него"""
        self.clear_frame()
        self.registration = Registration(self.widget_frame, self.settings_table, self.load_authorization)
        self.registration.pack(anchor='center', padx=10, pady=200) # размещения по центру
    
    def clear_frame(self):
        """Удаляет все виджеты из фрейма для загрузки."""
        for widget in self.widget_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    # Закрыть соидинения с БД
    app.main_conect.close()