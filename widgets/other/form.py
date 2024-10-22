import re
import tkinter as tk
from DB.other import OtherTable
from widgets.other.table import ListOthers
from widgets.pro import ButtonPro, InputGroupFrame, ComboboxGroupFrame, TextProGroupFrame, ClearButtonPro, TitleLabel, Toast

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

# [ '!grup', '!name', '!login', '!password', '!phone', '!email', '!url', 'description']
class FromOther(tk.Frame):
    """Форма ввода дополнительных данных - доступна для добавления и для редактирования"""
    def __init__(self, parent, table_other: OtherTable):
        # Список под уплавлением формы
        self.table_control = None

        # Менеджер таблицы "Телефоны"
        self.table_other = table_other

        # Данные для редактирования
        self.editdata = None 

        # Заголовок формы в зависимости от статуса формы (Добавления / Редактирования)
        self.from_text = f"Отредактировать запись, id: {self.editdata['select_row'][0]}" if self.is_edit() else "Добавить запись"

        # Иницыализация фрейма для формы
        super().__init__(parent, bd=1, relief="groove", bg=BG_FROM)
        self.pack(fill="both", expand=True, padx=(10,0), pady=10) # padx=(10,0) Ноль, потому что в таблице будет отступ 10

        # Заголовок формы
        self.title_form = TitleLabel(self, text=self.from_text, font=FONT_FROM)
        self.title_form.pack(anchor='w', padx=5, pady=5)

        # Группа: Инстаграм, Телеграм, Другое (grup)
        self.list_grup = OtherTable.list_grup
        self.grup = ComboboxGroupFrame(self, values=self.list_grup, title='Группа')
        self.grup.pack(anchor='w')

        # Название телефонв: (name)
        self.name = InputGroupFrame(self, title='Название номера',  help_text='Для чего используеться номер')
        self.name.pack(anchor='w')

        # Логин: (email )
        self.login = InputGroupFrame(self, title='Логин',  help_text='email', placeholder='qqqq@qq.com')
        self.login.pack(anchor='w')

        # Пароль: (password)
        self.password = InputGroupFrame(self, title='Пароль', placeholder='********')
        self.password.pack(anchor='w')

        # Телефон: (phone)
        self.phone = InputGroupFrame(self, title='Мобильный номер', placeholder='+380...')
        self.phone.pack(anchor='w')

        # Логин: (email )
        self.email = InputGroupFrame(self, title='Почта',  help_text='Email почта', placeholder='qqqq@qq.com')
        self.email.pack(anchor='w')

        # Логин: (url )
        self.url = InputGroupFrame(self, title='Ссылка',  help_text='Url сайта')
        self.url.pack(anchor='w')

        # Описание: (description )
        self.description = TextProGroupFrame(self, title='Комментарий')
        self.description.pack(anchor='w')

        # Третяя строка, для двух кнопок (Сохранить, Очистить)
        row3 = tk.Frame(self, bg='#121212')
        row3.pack(anchor='w')  # Третяя строка

        # Кнопка: Сохранить (Для добавления и редактирования формы)
        btn_pro = ButtonPro(row3, text='Сохранить', command=self.send_form)
        btn_pro.pack(side='left', padx=5, pady=5)

        # Кнопка размещаеться при режыме редактирования
        self.btn_cancel = ClearButtonPro(row3, text='Cancel editing', command=self.form_to_add)
            
        # Кнопка: Очистить форму, доступная только при добавлении данных
        self.btn_clear = ClearButtonPro(row3, text=' Очистить', command=self.clear_form)
        # Кнопка размещаеться по умолчанию
        self.btn_clear.pack(side='left', padx=5, pady=5)

        
    def send_form(self):
        """Обработка нажатия кнопки Сохранить, происходит валидация формы, добавления или редактирования данных в БД"""
        
        # Проверка валидности формы
        if not self.is_form_valid():
            #showerror(title="Ошибка", message='Введите валидный номер телефона, в формате +38097...')
            Toast(self.table_control, "⛔️ Ошибка", 'Невалидные данные')
            return
        
        # Получить введенные данные в форму
        grup, name, login, password, phone, email, url, description = self.get_data_form()

        # Редактирование или добавления данных
        if self.is_edit():
            # id редактируемой записи
            id = self.editdata['select_row'][0]
            # Редактирование данных в таблице (Шыфрование происходит внутри метода edit_other)
            status = self.table_other.edit_other(id, grup=grup, name=name, login=login, password=password, phone=phone, email=email, url=url, description=description)
            message=f'{name} отредактирован'
        else:
            # Добавления новой записи в бд (Шыфрование происходит внутри метода add_other)
            status = self.table_other.add_other(grup=grup, name=name, login=login, password=password, phone=phone, email=email, url=url, description=description)
            message='Запись добавлена!'
        
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
        for wid in [self.grup.combobox, self.name.input, self.login.input, self.password.input, self.phone.input, self.email.input, self.url.input, self.description.textpro]:
            wid.clear()
        
    def get_data_form(self):
        """Получить введенные значения в форму"""
        grup = self.grup.combobox.get_input_data()
        name = self.name.input.get_input_data()
        login = self.login.input.get_input_data()
        password = self.password.input.get_input_data()
        phone = self.phone.input.get_input_data()
        email = self.email.input.get_input_data()
        url = self.url.input.get_input_data()
        description = self.description.textpro.get_input_data()

        return grup, name, login, password, phone, email, url, description

    def set_edit_data_to_form(self, data=None):
        """Вставить данные для редактирования в поле ввода формы
            self.editdata['select_row'] = ['id', 'date_added', 'grup', 'name', 'login', 'password', 'phone', 'email', 'url', 'description', 'last_modified']
        """
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

        self.grup.combobox.set_input_data(self.editdata['select_row'][2])
        self.name.input.set_input_data(self.editdata['select_row'][3])
        self.login.input.set_input_data(self.editdata['select_row'][4])
        self.password.input.set_input_data(self.editdata['select_row'][5])
        self.email.input.set_input_data(self.editdata['select_row'][7])
        self.url.input.set_input_data(self.editdata['select_row'][8])
        self.description.textpro.set_input_data(self.editdata['select_row'][9])

        # Номер телефона, добавления + в начало номера
        if self.editdata['select_row'][6][0] != '+':
            self.phone.input.set_input_data('+'+self.editdata['select_row'][6])
        else:
            self.phone.input.set_input_data(self.editdata['select_row'][6])

    def is_edit(self):
        """Форма находиться в режыме редактирования ?"""
        if self.editdata is not None:
            return True
        return False
    
    def is_form_valid(self):
        """Валидатор формы, проверяет телефон на валидность только"""
        return True
        
    def set_table_control(self, listOthers: ListOthers):
        """Ссылка на список телефонов (таблица) для управления """
        self.table_control = listOthers

    def form_to_add(self):
        """Перевести форму в режым добавления данных"""
        # Изменить название формы на Добавление
        self.title_form['text'] = 'Добавления'
        # Очистить словарь редактирования
        self.editdata = None
        # Скрыть кнопку Отменыть редактирования
        self.btn_cancel.pack_forget()
        # Разместить кнопку Очистки формы
        self.btn_clear.pack(side='left', padx=5, pady=5)
        # Очистить форму
        self.clear_form()

    

        