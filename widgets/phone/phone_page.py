import tkinter as tk
from tkinter import ttk
from DB.phone import PhoneTable
from tkinter.messagebox import askyesnocancel
from widgets.pro import TreeviewPro, ButtonDellPro, ButtonEditPro, ButtonAddPro, ButtonCopyPro
from widgets.phone.form import FromPhone
from widgets.phone.table import ListPhones

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

class MainPhone(tk.Frame):
    def __init__(self, parent, table_phone: PhoneTable):
        super().__init__(parent, bd=1, relief="groove", bg="#0e0e0e")

        # FromPhone располагается слева и не растягивается по ширине
        self.addPhone = FromPhone(self, table_phone)
        self.addPhone.pack(side=tk.LEFT, fill=tk.Y, expand=False)  # Заполняет только по высоте, не растягивается по ширине

        # ListPhones располагается справа и заполняет всё оставшееся пространство
        self.listPhones = ListPhones(self, table_phone)
        self.listPhones.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  # Заполняет оставшееся пространство

        # Обмен ссылками двух компонентов
        self.listPhones.set_form_control(self.addPhone)
        self.addPhone.set_table_control(self.listPhones)

        
