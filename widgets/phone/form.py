import re

import tkinter as tk
from DB.phone import PhoneTable
from widgets.phone.table import ListPhones
from widgets.pro import ButtonPro, InputGroupFrame, ComboboxGroupFrame, TextProGroupFrame, ClearButtonPro, TitleLabel, Toast

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

class FromPhone(tk.Frame):
    """Форма ввода номера телефона - доступна для добавления телефона и для редактирования
        -- table_phone - БД таблица телефонов, с пред настройками
        -- editdata - словарь данных, если указан, форма в режыме редактирования иначе режым добавления записи
    """
    def __init__(self, parent, table_phone: PhoneTable):
        # Список под уплавлением формы
        self.table_control = None

        # Менеджер таблицы "Телефоны"
        self.table_phone = table_phone

        # Данные для редактирования
        self.editdata = None 

        # Заголовок формы в зависимости от статуса формы (Добавления / Редактирования)
        self.from_text = f"Отредактировать телефон, id: {self.editdata['select_row'][0]}" if self.is_edit() else "Добавить телефон"

        # Иницыализация фрейма для формы
        super().__init__(parent, bd=1, relief="groove", bg=BG_FROM)
        self.pack(fill="both", expand=True, padx=(10,0), pady=10) # padx=(10,0) Ноль, потому что в таблице будет отступ 10

        # Заголовок формы
        self.title_form = TitleLabel(self, text=self.from_text, font=FONT_FROM)
        self.title_form.pack(anchor='w', padx=5, pady=5)

        # Статус телефона: Новый, Удалить, Старый и прочее (usage_tag TEXT)
        self.list_status = PhoneTable.list_usage_tag
        self.status = ComboboxGroupFrame(self, values=self.list_status, title='Статус')
        self.status.pack(anchor='w')

        # Название телефонв: (name)
        self.name = InputGroupFrame(self, title='Название номера',  help_text='Для чего используеться номер')
        self.name.pack(anchor='w')

        # Телефон: (phone NOT NULL UNIQUE)
        self.phone = InputGroupFrame(self, title='Мобильный номер',  help_text='Обязательное поле', placeholder='+380...')
        self.phone.pack(anchor='w')

        # Две строки для 4-х пинкодов
        row1 = tk.Frame(self)
        row1.pack(anchor='w')  # Первая строка

        row2 = tk.Frame(self)
        row2.pack(anchor='w')  # Вторая строка

        # pin1: Первая строка
        self.pin1 = InputGroupFrame(row1, title='PIN 1', entryrow='one/half',  help_text='Находиться на карточке', placeholder='1111')
        self.pin1.pack(side='left')  # Размещаем слева с отступом

        # pin2: Первая строка
        self.pin2 = InputGroupFrame(row1, title='PIN 2', entryrow='one/half',  help_text='Не всегда есть', placeholder='1111')
        self.pin2.pack(side='left')  # Размещаем слева от предыдущего элемента с отступом

        # puk1: Вторая строка
        self.puk1 = InputGroupFrame(row2, title='PUK 1', entryrow='one/half',  help_text='Находиться на карточке', placeholder='12345678')
        self.puk1.pack(side='left')  # Размещаем слева с отступом

        # puk2: Вторая строка
        self.puk2 = InputGroupFrame(row2, title='PUK 2', entryrow='one/half',  help_text='Не всегда есть', placeholder='12345678')
        self.puk2.pack(side='left')  # Размещаем слева от предыдущего элемента с отступом

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
            Toast(self.table_control, "⛔️ Ошибка", 'Невалидный номер +38097...')
            return

        # Получить введенные данные в форму
        status, name, phone, pin1, pin2, puk1, puk2, description = self.get_data_form()

        # Редактирование или добавления данных
        if self.is_edit():
            # id редактируемой записи
            id = self.editdata['select_row'][0]
            # Редактирование данных в таблице (Шыфрование происходит внутри метода edit_phone)
            status = self.table_phone.edit_phone(id, usage_tag=status,name=name,phone=phone,pin1=pin1,pin2=pin2,puk1=puk1,puk2=puk2,description=description)
            message=f'{phone} отредактирован'
        else:
            # Добавления нового телефона в бд (Шыфрование происходит внутри метода add_phone)
            status = self.table_phone.add_phone(usage_tag=status,name=name,phone=phone,pin1=pin1,pin2=pin2,puk1=puk1,puk2=puk2,description=description)
            message='Телефон добавлен!'
            
        # Обновления списка с данными 
        self.table_control.treePro.refresh_treeview()

        # Проверка успешности записи/изменения в бд
        if status:
            #showinfo(title="Готово", message=message)
            Toast(self.table_control, "✅ Готово", message, duration=4000)
            if self.is_edit():
                self.form_to_add() # переводим форму в режым добавления, выходим с редактирования
            # очистить форму в любом раскладе
            self.clear_form()
        else:
            #showinfo(title="Ошибка", message='Неполучилось внести изменения в БД, попробуйте позже')
            Toast(self.table_control, "⛔️ Ошибка", 'Подключения не установлено')

    def clear_form(self):
        """Очистить введенные данные в форму
        Сохраняем в список ссылки на Екземплар класса у которых у всех есть метод clear() и вызываем его, аналог запили self.status.combobox.clear()
        Проблема: удаляеться плейсхолдер
        """
        for wid in [self.status.combobox, self.name.input, self.phone.input, self.pin1.input, self.pin2.input, self.puk1.input, self.puk2.input, self.description.textpro]:
            wid.clear()
        
    def get_data_form(self):
        """Получить введенные значения в форму"""
        status = self.status.combobox.get_input_data()
        name = self.name.input.get_input_data()
        phone = self.phone.input.get_input_data()
        pin1 = self.pin1.input.get_input_data()
        pin2 = self.pin2.input.get_input_data()
        puk1 = self.puk1.input.get_input_data()
        puk2 = self.puk2.input.get_input_data()
        description = self.description.textpro.get_input_data()

        return status, name, phone, pin1, pin2, puk1, puk2, description

    def set_edit_data_to_form(self, data=None):
        """Вставить данные для редактирования в поле ввода формы
            self.editdata['select_row'] = [7, '23.09.2024 14:40', 'Старый', 'Личный', 3805567, 5555, 5555, 23456789, 98765432, 'Старый личный телефон', '23.09.2024 14:40']
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
        

        self.status.combobox.set_input_data(self.editdata['select_row'][2])
        self.name.input.set_input_data(self.editdata['select_row'][3])
        self.pin1.input.set_input_data(self.editdata['select_row'][5])
        self.pin2.input.set_input_data(self.editdata['select_row'][6])
        self.puk1.input.set_input_data(self.editdata['select_row'][7])
        self.puk2.input.set_input_data(self.editdata['select_row'][8])
        self.description.textpro.set_input_data(self.editdata['select_row'][9])

        # Номер телефона, добавления + в начало номера
        if self.editdata['select_row'][4][0] != '+':
            self.phone.input.set_input_data('+'+self.editdata['select_row'][4])
        else:
            self.phone.input.set_input_data(self.editdata['select_row'][4])

    def is_edit(self):
        """Форма находиться в режыме редактирования ?"""
        if self.editdata is not None:
            return True
        return False
    
    def is_form_valid(self):
        """Валидатор формы, проверяет телефон на валидность только"""
        phone = self.phone.input.get_input_data()

        # Регулярное выражение для проверки формата номера телефона
        phone_pattern = r"^\+380\d{9}$"
    
        if re.match(phone_pattern, phone):
            return True
        else:
            return False
        
    def set_table_control(self, listPhones: ListPhones):
        """Ссылка на список телефонов (таблица) для управления """
        self.table_control = listPhones

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

    

        