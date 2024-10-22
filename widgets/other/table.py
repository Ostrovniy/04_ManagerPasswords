import tkinter as tk
from tkinter import ttk
from DB.other import OtherTable
from tkinter.messagebox import askyesnocancel
from widgets.pro import Toast, TreeviewPro, ButtonDellPro, ButtonEditPro, ButtonAddPro, ButtonCopyPro

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

class ListOthers(tk.Frame):
    def __init__(self, parent, table_other: OtherTable):
        # Форфма управления списом
        self.form_control = None

        super().__init__(parent, bd=1, relief="groove", bg=BG_FROM)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        # Менеджер таблицы "Телефоны"
        self.table_other = table_other

        # Фрейм меню, для хранения кнопок, Редактировать, Добавить и другие
        self.button_frame = tk.Frame(self, bg=BG_FROM)
        self.button_frame.pack(fill='x', padx=5, pady=(15, 5))

        # Кнопка Уадалить, по умолчанию деактивирована
        self.btn_dell = ButtonDellPro(self.button_frame, text='Dell')
        self.btn_dell.state_disabled()
        self.btn_dell.pack(side='left', padx=5)
        
        # Кнопка Редактировать, по умолчанию деактивирована
        self.btn_edit = ButtonEditPro(self.button_frame, text='Edit')
        self.btn_edit.state_disabled()
        self.btn_edit.pack(side='left', padx=5)

        # Кнопка Скопировать
        self.btn_copy = ButtonCopyPro(self.button_frame, text='Copy')
        self.btn_copy.state_disabled()
        self.btn_copy.pack(side='left', padx=5)

        # Таблица, список телефонов
        self.treePro = TreeviewPro(self, self.table_other )
        self.treePro.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Событие выбора строки в таблице
        self.treePro.bind("<<TreeviewSelect>>", self.item_selected)
    
    # Обработка события выделения в таблице
    def item_selected(self, event):
        res = [] # Выбранная строка
        for selected_item in self.treePro.selection():
            item = self.treePro.item(selected_item)
            res = item["values"]

        # Разблокировать кнопки
        self.treeProMenu_state_normal()

        # перевести все значения списка в строку
        res_str = [str(item) for item in res]

        # Передать кнопкам обработчики события с параметрами
        if len(res_str) != 0:
            self.btn_dell['command'] = lambda: self.delete_other(res_str[0])
            self.btn_copy['command'] = lambda: self.copy_other_data(res_str)
            self.btn_edit['command'] = lambda: self.form_control.set_edit_data_to_form({'select_row': res_str}) # Первод в режым редактирования
            
    def delete_other(self, id_other):
        """Обработка кнопки "Удалить" с подтверждением"""
        self.treeProMenu_state_disabled()
        res = askyesnocancel(title='Подтверждение', message='Действительно хотиле удалить ? ')
        if res:
            self.table_other.dell_other_by_id(int(id_other))
            self.treePro.refresh_treeview()
            self.treePro.clear_selection() # Снять выделения с несуществующего елемента в таблице
            self.update()
            Toast(self, "✅ Готово", f'id:{id_other} успешно удален')

    def copy_other_data(self, other):
        """Обработка кнопки "Скопировать" НАДо доработать ответ, в красивый текст"""
        self.treeProMenu_state_disabled()
        self.clipboard_clear()
        self.clipboard_append(other)
        self.update()
        Toast(self, "✅ Готово", 'Данные скопированы')
    
    def set_form_control(self, form):
        """Ссылка форму телефонов (форма) для управления """
        self.form_control = form

    # Активировать кнопки действия относительно таблицы
    def treeProMenu_state_normal(self):
        self.btn_dell.state_normal()
        self.btn_copy.state_normal()
        self.btn_edit.state_normal()

    # Активировать кнопки действия относительно таблицы
    def treeProMenu_state_disabled(self):
        self.btn_dell.state_disabled()
        self.btn_copy.state_disabled()
        self.btn_edit.state_disabled()



    
  

        

        