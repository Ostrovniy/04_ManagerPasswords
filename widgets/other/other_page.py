import tkinter as tk
from tkinter import ttk
from DB.other import OtherTable
from tkinter.messagebox import askyesnocancel
from widgets.other.form import FromOther
from widgets.other.table import ListOthers
from widgets.pro import TreeviewPro, ButtonDellPro, ButtonEditPro, ButtonAddPro, ButtonCopyPro

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

class MainOther(tk.Frame):
    def __init__(self, parent, table_other: OtherTable):
        super().__init__(parent, bd=1, relief="groove", bg="#0e0e0e")

        # FromOther располагается слева и не растягивается по ширине
        self.addOther = FromOther(self, table_other)
        self.addOther.pack(side=tk.LEFT, fill=tk.Y, expand=False)  # Заполняет только по высоте, не растягивается по ширине

        # listOthers располагается справа и заполняет всё оставшееся пространство
        self.listOthers = ListOthers(self, table_other)
        self.listOthers.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  # Заполняет оставшееся пространство

        # Обмен ссылками двух компонентов
        self.listOthers.set_form_control(self.addOther)
        self.addOther.set_table_control(self.listOthers)