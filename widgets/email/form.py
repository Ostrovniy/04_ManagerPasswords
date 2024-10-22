import re
import tkinter as tk
from DB.email import EmailTable
from widgets.email.table import ListEmails
from widgets.phone.table import ListPhones
from widgets.pro import ButtonPro, InputGroupFrame, ComboboxGroupFrame, TextProGroupFrame, ClearButtonPro, TitleLabel, Toast

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

# ['id', 'date_added', 'email_type', 'name', 'login', 'password', 'phonerestore', 'backupmail', 'description', 'last_modified']

class FromEmail(tk.Frame):
    def __init__(self, parent, table_email: EmailTable):
        # Список под уплавлением формы
        self.table_control = None

        # Менеджер таблицы "Email"
        self.table_email = table_email

        # Данные для редактирования
        self.editdata = None 

        # Заголовок формы в зависимости от статуса формы (Добавления / Редактирования)
        self.from_text = f"Отредактировать email, id: {self.editdata['select_row'][0]}" if self.is_edit() else "Добавить email"

        # Иницыализация фрейма для формы
        super().__init__(parent, bd=1, relief="groove", bg=BG_FROM)
        self.pack(fill="both", expand=True, padx=(10,0), pady=10) # padx=(10,0) Ноль, потому что в таблице будет отступ 10

        # Заголовок формы
        self.title_form = TitleLabel(self, text=self.from_text, font=FONT_FROM)
        self.title_form.pack(anchor='w', padx=5, pady=5)

        # Статус email: Google, Mail и прочее (email_type)
        self.list_email_type = EmailTable.list_email_type
        self.email_type = ComboboxGroupFrame(self, values=self.list_email_type, title='Тип')
        self.email_type.pack(anchor='w')

        # Название телефонв: (name)
        self.name = InputGroupFrame(self, title='Название',  help_text='Для чего используеться email')
        self.name.pack(anchor='w')

        # Логин: (email )
        self.login = InputGroupFrame(self, title='Логин',  help_text='email', placeholder='qqqq@qq.com')
        self.login.pack(anchor='w')

        # Пароль: (password)
        self.password = InputGroupFrame(self, title='Пароль', placeholder='********')
        self.password.pack(anchor='w')

        # Телефон востановления: (phonerestore)
        self.phonerestore = InputGroupFrame(self, title='Телефон востановления',  help_text='или тебефон регастрации аккаунта', placeholder='+380...')
        self.phonerestore.pack(anchor='w')

        # Телефон востановления: (phonerestore)
        self.backupmail = InputGroupFrame(self, title='Резервная почта',  help_text='Почта для востановления доступа', placeholder='qqqq@qq.com')
        self.backupmail.pack(anchor='w')

        # Описание: (description )
        self.description = TextProGroupFrame(self, title='Комментарий')
        self.description.pack(anchor='w')

        # Строка для двух кнопок под формой
        row1 = tk.Frame(self, bg='#121212')
        row1.pack(anchor='w')  # Третяя строка

        # Кнопка: Сохранить (Для добавления и редактирования формы)
        btn_pro = ButtonPro(row1, text='Сохранить', command=self.send_form)
        btn_pro.pack(side='left', padx=5, pady=5)

        # Кнопка размещаеться при режыме редактирования
        self.btn_cancel = ClearButtonPro(row1, text='Cancel editing', command=self.form_to_add)
            
        # Кнопка: Очистить форму, доступная только при добавлении данных (размещаеться по умолчанию)
        self.btn_clear = ClearButtonPro(row1, text=' Очистить', command=self.clear_form)
        self.btn_clear.pack(side='left', padx=5, pady=5)

    def send_form(self):
        """Обработка нажатия кнопки Сохранить, происходит валидация формы, добавления или редактирования данных в БД"""
        # Проверка валидности формы
        if not self.is_form_valid():
            Toast(self.table_control, "⛔️ Ошибка", 'Форма не прошла валидацию')
            return

        # Получить введенные данные в форму
        email_type, name, login, password, phonerestore, backupmail, description = self.get_data_form()

        # Редактирование или добавления данных
        if self.is_edit():
            # id редактируемой записи
            id = self.editdata['select_row'][0]
            # Редактирование данных в таблице (Шыфрование происходит внутри метода edit_email)
            status = self.table_email.edit_email(id, email_type=email_type,name=name,login=login,password=password,phonerestore=phonerestore,backupmail=backupmail,description=description)
            message=f'{login} отредактирован'
        else:
            # Добавления нового телефона в бд (Шыфрование происходит внутри метода add_phone)
            status = self.table_email.add_email(email_type=email_type,name=name,login=login,password=password,phonerestore=phonerestore,backupmail=backupmail,description=description)
            message='Почта добавлен!'
        
        # Обновления списка с данными 
        self.table_control.treePro.refresh_treeview()

        # Проверка успешности записи/изменения в бд
        if status:
            Toast(self.table_control, "✅ Готово", message, duration=4000)
            if self.is_edit():
                self.form_to_add() # переводим форму в режым добавления, выходим с редактирования
            # очистить форму в любом раскладе
            self.clear_form()
        else:
            Toast(self.table_control, "⛔️ Ошибка", 'Подключения не установлено')

    def clear_form(self):
        """Очистить введенные данные в форму
        Сохраняем в список ссылки на Екземплар класса у которых у всех есть метод clear() и вызываем его, аналог запили self.status.combobox.clear()
        Проблема: удаляеться плейсхолдер
        """
        for wid in [self.email_type.combobox, self.name.input, self.login.input, self.password.input, self.phonerestore.input, self.backupmail.input, self.description.textpro]:
            wid.clear()

    def get_data_form(self):
        """Получить введенные значения в форму"""
        email_type = self.email_type.combobox.get_input_data()
        name = self.name.input.get_input_data()
        login = self.login.input.get_input_data()
        password = self.password.input.get_input_data()
        phonerestore = self.phonerestore.input.get_input_data()
        backupmail = self.backupmail.input.get_input_data()
        description = self.description.textpro.get_input_data()

        return email_type, name, login, password, phonerestore, backupmail, description

    def set_edit_data_to_form(self, data=None):
        """Вставить данные для редактирования в поле ввода формы"""
        # При редактировании отключаем меню Кнопок
        self.table_control.treeProMenu_state_disabled()
        # Изменить название формы на Редактирование
        self.title_form['text'] = 'Редактирование'
        # Скрыть кнопку "Очистить форму"
        self.btn_clear.pack_forget()
        # Разместить кнопку "Отменить редактирование"
        self.btn_cancel.pack(side='left', padx=5, pady=5)
        # Данные для редактирования 
        self.editdata = data
        
        # ['2', '02.10.2024 11:37', 'Google', 'Название', 'lasdjfasl@gmail.ru', 'qwerty', '380979765432', 'lasdjfasl@gmail.ru', 'Для бинанса\n', '02.10.2024 11:37']
        self.email_type.combobox.set_input_data(self.editdata['select_row'][2])
        self.name.input.set_input_data(self.editdata['select_row'][3])
        self.login.input.set_input_data(self.editdata['select_row'][4])
        self.password.input.set_input_data(self.editdata['select_row'][5])
        self.backupmail.input.set_input_data(self.editdata['select_row'][7])
        self.description.textpro.set_input_data(self.editdata['select_row'][8])

        # Номер телефона, добавления + в начало номера
        # Проверка номер на пустоту
        if self.editdata['select_row'][6]:
            if self.editdata['select_row'][6][0] != '+':
                self.phonerestore.input.set_input_data('+'+self.editdata['select_row'][6])
            else:
                self.phonerestore.input.set_input_data(self.editdata['select_row'][6])
        else:
            self.phonerestore.input.set_input_data(self.editdata['select_row'][6])

    def is_edit(self):
        """Форма находиться в режыме редактирования ?"""
        if self.editdata is not None:
            return True
        return False

    def is_form_valid(self):
        """Валидатор формы"""
        return True
    
    def set_table_control(self, listEmails: ListEmails):
        """Ссылка на список телефонов (таблица) для управления """
        self.table_control = listEmails
    
    def form_to_add(self):
        """Перевести форму в режым добавления данных"""
        # Изменить название формы на Добавление
        self.title_form['text'] = 'Добавления email'
        # Очистить словарь редактирования
        self.editdata = None
        # Скрыть кнопку Отменыть редактирования
        self.btn_cancel.pack_forget()
        # Разместить кнопку Очистки формы
        self.btn_clear.pack(side='left', padx=5, pady=5)
        # Очистить форму
        self.clear_form()