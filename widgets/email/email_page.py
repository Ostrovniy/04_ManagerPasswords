import tkinter as tk
from tkinter import ttk
from DB.email import EmailTable
from tkinter.messagebox import askyesnocancel
from widgets.email.table import ListEmails
from widgets.pro import TreeviewPro, ButtonDellPro, ButtonEditPro, ButtonAddPro, ButtonCopyPro
from widgets.email.form import FromEmail

# Константы для формы
BG_FROM = '#121212'
FG_FORM = '#ffefe1'
FONT_FROM = ('Arial', 18, 'bold')

class MainEmail(tk.Frame):
    def __init__(self, parent, table_email: EmailTable):
        super().__init__(parent, bd=1, relief="groove", bg="#0e0e0e")

        # FromPhone располагается слева и не растягивается по ширине
        self.addEmail = FromEmail(self, table_email)
        self.addEmail.pack(side=tk.LEFT, fill=tk.Y, expand=False)  # Заполняет только по высоте, не растягивается по ширине

        # ListPhones располагается справа и заполняет всё оставшееся пространство
        self.listEmails = ListEmails(self, table_email)
        self.listEmails.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  # Заполняет оставшееся пространство

        # Обмен ссылками двух компонентов
        self.listEmails.set_form_control(self.addEmail)
        self.addEmail.set_table_control(self.listEmails)