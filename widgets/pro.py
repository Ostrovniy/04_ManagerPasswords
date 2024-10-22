import tkinter as tk
from tkinter import PhotoImage, ttk
from DB.phone import PhoneTable


# https://mui.com/store/previews/devias-kit-pro/

# Основные стили приложения
BG_APP_COLOR = '#121212'                            # BG Приложения
FG_APP_COLOR = '#ffffff'                            # FG Приложения
FG_HELP_COLOR = '#c7c7c7'                           # FG Help текста
BG_INPUT_COLOR = '#121517'                          # BG Поля ввода Input
INPUT_ACTIVE_BORDER = '#23253e'                     # Обводка рамки, активного Input
INPUT_NOT_ACTIVE_BORDER = '#32383e'                 # Обводка рамки, НЕ активного Input
INPUT_FONT_SIZE = 10                                # Размер текста приложения
WIDTH_SIMVOL = 40                                   # Шырина поля ввода прилождения

# Стиль не активной кнопки, один для всех кнопок
BG_BUTTON_DISABLED = '#919191'                            
FG_BUTTON_DISABLED = '#121212'   

# Стили кнопки "Отправить"
BG_BUTTON = '#007acc'                               # BG
BG_BUTTON_HOVER = '#005f99'                         # BG при наведении
BG_BUTTON_ACTIVE = '#004d80'                        # BG при нажатии
BORDER_COLOR = '#1e1e1e'                            # Цвет границы

# Стиль Кнопки "Удалить"
BG_BUTTON_DELL = '#cc0030'           # Основной цвет кнопки
BG_BUTTON_HOVER_DELL = '#a80028'     # Цвет при наведении
BG_BUTTON_ACTIVE_DELL = '#8b0021'    # Цвет при нажатии
BORDER_COLOR_DELL = '#73001b'        # Цвет границы

# Стиль Кнопки "Редактировать"
BG_BUTTON_EDIT = '#ff9800'           # Основной цвет кнопки — оранжевый, символизирующий изменения и редактирование
BG_BUTTON_HOVER_EDIT = '#fb8c00'     # Цвет при наведении — чуть более насыщенный оранжевый
BG_BUTTON_ACTIVE_EDIT = '#f57c00'    # Цвет при нажатии — ещё более тёмный оранжевый
BORDER_COLOR_EDIT = '#e65100'        # Цвет границы — насыщенный тёмно-оранжевый для контраста

# Стиль Кнопки "Добавить/Создать"
BG_BUTTON_ADD = '#4caf50'           # Основной цвет кнопки — приглушённый зелёный
BG_BUTTON_HOVER_ADD = '#43a047'     # Цвет при наведении — немного темнее для акцента
BG_BUTTON_ACTIVE_ADD = '#388e3c'    # Цвет при нажатии — ещё более тёмный зелёный
BORDER_COLOR_ADD = '#2e7d32'        # Цвет границы — насыщенный тёмный зелёный для контраста

# Стиль Кнопки "Скопировать"
BG_BUTTON_COPY = '#9c27b0'           # Основной цвет кнопки — умеренный фиолетовый
BG_BUTTON_HOVER_COPY = '#8e24aa'     # Цвет при наведении — немного более тёмный и насыщенный фиолетовый
BG_BUTTON_ACTIVE_COPY = '#7b1fa2'    # Цвет при нажатии — тёмный фиолетовый
BORDER_COLOR_COPY = '#6a1b9a'        # Цвет границы — насыщенный тёмный фиолетовый для акцента



# Стилизация таблицы
BG_TREE_HEADER = '#202427'                          # BG Заголовка таблицы
FG_TREE_HEADER = '#9FA6AD'                          # FG Заголовка таблицы
BG_TREE_ROW = '#121517'


# Поле ввода: Input
class EntryPro(tk.Entry):
    def __init__(self, parent, row='normal', placeholder="", *args, **kwargs):
        """Input: Поле ввода"""
        # Задаем стандартные настройки виджета
        kwargs.setdefault('bg', BG_INPUT_COLOR)                                 # цвет фона
        kwargs.setdefault('fg', FG_APP_COLOR)                                   # цвет текста
        kwargs.setdefault('font', ('Arial', INPUT_FONT_SIZE))                   # шрифт и размер ('Arial', 12)
        kwargs.setdefault('relief', 'sunken')                                   # стиль рамки
        kwargs.setdefault('selectbackground', INPUT_ACTIVE_BORDER)   # фон для выделенного текста

        # ширина в символах, длина нормальная или пововина
        if row == 'normal':                               
            kwargs.setdefault('width', WIDTH_SIMVOL)
        else:
            kwargs.setdefault('width', int(WIDTH_SIMVOL/2)-1)                   
            
        kwargs.setdefault('justify', 'left')                                    # выравнивание текста
        kwargs.setdefault('state', 'normal')                                    # состояние
        kwargs.setdefault('highlightbackground', INPUT_NOT_ACTIVE_BORDER)       # цвет неактивной рамки
        kwargs.setdefault('highlightcolor', INPUT_ACTIVE_BORDER)                # цвет активной рамки
        kwargs.setdefault('highlightthickness', 1)                              # толщина рамки
        kwargs.setdefault('borderwidth', 0)                                     # толщина границы, убрало 3 границу залупскую
        kwargs.setdefault('insertbackground', FG_APP_COLOR)                     # цвет курсора
        kwargs.setdefault('insertwidth', 1)


        # Вызываем родительский конструктор с измененными аргументами
        super().__init__(parent, *args, **kwargs)

        # Настройки плейсхолдера
        self.placeholder = placeholder
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.insert(0, self.placeholder)
        self.configure(fg='grey')  # Цвет текста плейсхолдера

    def clear(self):
        """Очистить поле ввода, установить плейсхолдер со стилями"""
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.configure(fg='grey')  # Цвет текста плейсхолдера


    def get_input_data(self):
        """Получить введенное значения, проверяем что введенные данные не плейсхолдер"""
        # Если получаемые данные это плейсхолдер, вернуть пустую строку
        if self.get() == self.placeholder:
            return ''
        return self.get()

    def set_input_data(self, value):
        """Установить новое значения"""
        self.delete(0, tk.END) # Удаляем все данные с инпута вмести с плейсхолдером
        self.insert(0, value) # Вставляем данные
        self.configure(fg=FG_APP_COLOR) # Помогло избавиться от проблемы что вствляемый текст был вцетом как плейсхолжер

        # КОгда добавляемые данные пустые. устанавлием плейсхолдре
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg='grey')  # Цвет текста плейсхолдера

    def on_focus_in(self, *args):
        """Удаляет текст плейсхолдера, если пользователь начинает вводить данные. 
            Если мы навели на поле, а в поле текст Плейсходлера, мы его удаляем и возвращаем цвет на нормальный
            Поле готово для ввода, при этом если в нем будет какой то другой текст мы его не трогаем
        """
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(fg=FG_APP_COLOR)  # Цвет текста при вводе

    def on_focus_out(self, *args):
        """Если поле пустое когда мы убрали с него фокус, возвращает текст плейсхолдера и устанавливает его цвет обратно на серый."""
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg='grey')  # Цвет текста плейсхолдера

# Заголовок для поля ввода
class TitleLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        """Вспомагательный текст Названия поля ввода"""
        # Настройки стилей по умолчанию для темной темы
        kwargs.setdefault('bg', BG_APP_COLOR)                      
        kwargs.setdefault('fg', FG_APP_COLOR)                      
        kwargs.setdefault('font', ('Arial', INPUT_FONT_SIZE))               

        super().__init__(parent, *args, **kwargs)

# Help для поля ввода
class HelpLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        """Вспомагательный текст под полем ввода"""
        # Настройки стилей по умолчанию для темной темы
        kwargs.setdefault('bg', BG_APP_COLOR)                  
        kwargs.setdefault('fg', FG_HELP_COLOR)                     
        kwargs.setdefault('font', ('Arial', INPUT_FONT_SIZE-3))                

        super().__init__(parent, *args, **kwargs)

# Кнопка: Отправить
class ButtonPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Отправить (Синяя)"""
        super().__init__(parent, *args, **kwargs)

        # Настройки стиля кнопки
        self.configure(
            bg=BG_BUTTON,                           # Основной цвет фона
            fg=FG_APP_COLOR,                        # Цвет текста
            activebackground=BG_BUTTON_ACTIVE,      # Фон при нажатии
            activeforeground=FG_APP_COLOR,          # Цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Обработка навидения на кнопку
    def on_enter(self, e):
        self['bg'] = BG_BUTTON_HOVER   # Изменяем фон при наведении

    def on_leave(self, e):
        self['bg'] = BG_BUTTON         # Возвращаем основной фон

# Кнопка: Очистить форму
class ClearButtonPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Очистить (Серая)"""
        super().__init__(parent, *args, **kwargs)

        # Настройки стиля кнопки
        self.configure(
            bg="#B0B0B0",                           # Светло-серый фон
            fg="#FFFFFF",                           # Белый цвет текста
            activebackground="#909090",             # Темно-серый фон при нажатии
            activeforeground="#FFFFFF",             # Белый цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Обработка наведения на кнопку
    def on_enter(self, e):
        self['bg'] = "#A0A0A0"   # Изменяем фон на чуть более темный при наведении

    def on_leave(self, e):
        self['bg'] = "#B0B0B0"   # Возвращаем светло-серый фон

# Большое поле ввода
class TextPro(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        """Большое поле ввода: для коментариев"""
        super().__init__(parent, *args, **kwargs)

        # Стилизация под темную тему
        self.configure(
            bg=BG_INPUT_COLOR,                      # bg
            fg=FG_APP_COLOR,                        # fg
            insertbackground=FG_APP_COLOR,          # Белый курсор
            selectbackground=INPUT_ACTIVE_BORDER,          # фон для выделенного текста
            selectforeground=FG_APP_COLOR,          # Белый цвет выделенного текста
            font=('Arial', INPUT_FONT_SIZE),        # Шрифт и размер
            padx=5, pady=5,                         # Внутренние отступы
            wrap='word',                            # Перенос слов, по словам
            height=7,                               # Фиксированная высота в строках
            width=WIDTH_SIMVOL,                     # Фиксированная ширина в символах
            borderwidth=0,                          # толщина границы, убрало 3 границу залупскую
            highlightthickness=1, # Толщина рамки
            highlightbackground=INPUT_NOT_ACTIVE_BORDER, # Цвет не активной рамки
            highlightcolor=INPUT_ACTIVE_BORDER,  # Цвет активной рамки

        )
                      
    def clear(self):
        """Очистить поле ввода"""
        self.delete('1.0', tk.END)
    
    def get_input_data(self):
        """Получить введенное значения"""
        return self.get("1.0", tk.END)

    def set_input_data(self, value):
        """Установить значение в поле ввода"""
        self.clear()  # Очищаем поле перед установкой нового значения
        self.insert('1.0', value)

# Выпадающий список
class ComboboxPro(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        # Определяем пользовательский стиль
        style = ttk.Style()
        #tree_style.theme_use("default") #clam
        style.theme_use('default')  # Используем тему, которая поддерживает изменения стиля

        # Основной стиль combobox
        style.configure('Custom2.TCombobox',
                        fieldbackground=BG_INPUT_COLOR,
                        background=BG_APP_COLOR,
                        foreground=FG_APP_COLOR,
                        arrowcolor=FG_APP_COLOR,
                        selectbackground=BG_INPUT_COLOR,
                        selectforeground=FG_APP_COLOR,
                        highlightthickness=0,  # Толщина границы
                        borderwidth=1,               # Толщина рамки                    
                        )
        # Настройка фона и текста для состояния "не в фокусе"
        style.map('Custom2.TCombobox',
                  fieldbackground=[('readonly', BG_INPUT_COLOR), ('!focus', BG_INPUT_COLOR)],  # Фон при потере фокуса
                  #foreground=[('readonly', FG_APP_COLOR), ('!focus', FG_APP_COLOR)],          # Цвет текста при потере фокуса
                  #bordercolor=[('focus', INPUT_ACTIVE_BORDER)]  # Цвет рамки при фокусе
        )
        
        kwargs.setdefault('style', 'Custom2.TCombobox')
        kwargs.setdefault('width', WIDTH_SIMVOL)  # Задаем ширину в символах

        # Инициализируем ttk.Combobox с измененными параметрами
        super().__init__(parent, *args, **kwargs)
        self.configure(font=('Arial', INPUT_FONT_SIZE)) # Попробуем задать шрифт напрямую
        self.configure(state='readonly') # Устанавливаем режим "только для чтения"
    
    def clear(self):
        """Очистить выбранный элемент"""
        self.set('')  # Сбрасываем выбранное значение

    def get_input_data(self):
        """Возвращает текущее выбранное значение в combobox"""
        return self.get()

    def set_input_data(self, value):
        """Устанавливает переданное значение в combobox"""
        self.set(value)  # Устанавливаем переданное значение

# Галочка активации
class CheckbuttonPro(ttk.Checkbutton):
    def __init__(self, parent, *args, **kwargs):
        # Define a custom style
        style = ttk.Style()
        # Используем другую тему для более гибкого управления стилями
        style.theme_use('clam')  # Попробуй 'alt', 'default', 'clam'

        # Customize the checkbutton's appearance
        style.configure('Custom.TCheckbutton',background=BG_APP_COLOR, foreground=FG_APP_COLOR,font=('Arial', INPUT_FONT_SIZE))
        
        # Отключаем изменения стиля при наведении
        style.map('Custom.TCheckbutton',
                  background=[('!active', BG_APP_COLOR)],   # Фон не меняется при наведении
                  foreground=[('!active', FG_APP_COLOR)],   # Цвет текста не меняется
                  indicatorcolor=[('!active', FG_APP_COLOR)] # Цвет галочки не меняется
                  )

        # Apply the custom style to the checkbutton
        kwargs.setdefault('style', 'Custom.TCheckbutton')

        # Initialize the ttk.Checkbutton with the modified kwargs
        super().__init__(parent, *args, **kwargs)

# Фрейм для Заголовок + поле ввода
class ComboboxGroupFrame(tk.Frame):
    def __init__(self, parent, values, title="Label:", *args, **kwargs):
        # Стилизация фрейма
        kwargs.setdefault('bg', BG_APP_COLOR)  # Темный фон
        super().__init__(parent, *args, **kwargs) # Иницыализация фрейма
        
  
        # Создания: Заголовок, Поле ввода, Подсказка
        self.title = TitleLabel(self, text=title)
        self.combobox = ComboboxPro(self, values=values)


        # Размещение: Заголовок, Поле ввода, Подсказка
        self.title.pack(padx=5, anchor='w') # Отступ слева и права 5 и прижать к левой стороне
        self.combobox.pack(padx=5, pady=[0, 5]) # Отступ слева и справа 5 и отступ сверху 0 а сниху 0

        # Идея, в зависимости от выбраного значения менять стили, но со стилями еще та ебала

# Поле ввода и заголовок 
class TextProGroupFrame(tk.Frame):
    def __init__(self, parent, title="Label:", *args, **kwargs):
        kwargs.setdefault('bg', BG_APP_COLOR)  # Темный фон
        super().__init__(parent, *args, **kwargs)

        self.title = TitleLabel(self, text=title)
        self.textpro = TextPro(self)

        self.title.pack(padx=5, anchor='w') # Отступ слева и права 5 и прижать к левой стороне
        self.textpro.pack(padx=5, pady=[0, 5])

# Фрейм для Заголовок + поле ввода
class InputGroupFrame(tk.Frame):
    def __init__(self, parent, title="Label:", help_text = '', entryrow = 'normal', placeholder="", *args, **kwargs):
        # Стилизация фрейма
        kwargs.setdefault('bg', BG_APP_COLOR)  # Темный фон
        super().__init__(parent, *args, **kwargs) # Иницыализация фрейма
        
        # Размещения внутри фрейма Виджетор
        if help_text:
            # Создания: Заголовок, Поле ввода, Подсказка
            self.title = TitleLabel(self, text=title)
            self.input = EntryPro(self, row=entryrow, placeholder=placeholder)
            self.help = HelpLabel(self, text=help_text)

            # Размещение: Заголовок, Поле ввода, Подсказка
            self.title.pack(padx=5, anchor='w') # Отступ слева и права 5 и прижать к левой стороне
            self.input.pack(padx=5, pady=[0, 0]) # Отступ слева и справа 5 и отступ сверху 0 а сниху 0
            self.help.pack(padx=5,  pady=[0, 5], anchor='w') # # Отступ слева и права 5 и прижать к левой стороне отступ сверху 0 а снизу 5
        else:
            # Создания: Заголовок, Поле ввода
            self.title = TitleLabel(self, text=title)
            self.input = EntryPro(self, row=entryrow, placeholder=placeholder)

            # Размещение: Заголовок, Поле ввода
            self.title.pack(padx=5, anchor='w') # Отступ слева и права 5 и прижать к левой стороне
            self.input.pack(padx=5, pady=[0, 5]) # Отступ слева и справа 5 и отступ сверху 0 а сниху 5

# Динамическая таблица, относительно таблицы БД
class TreeviewPro(ttk.Treeview):
    def __init__(self, parent, table, *args, **kwargs):
        """Custom Treeview widget with predefined column and style settings."""
        # Установка стиля
        self.setup_styles()

        # Set default styles and options
        kwargs.setdefault('show', 'headings')  # Only show headings
        kwargs.setdefault('selectmode', 'browse')  # Single selection mode
        kwargs.setdefault('style', 'Custom.Treeview')  # Применяем кастомный стиль

        # Список колонок относительно таблицы БД
        self.table = table
        self.columns = self.table.list_columns_for_treeview                # Названия колонок
        self.columns_name = self.table.list_columns_name_for_treeview      # Названия колонок для отрисовки
        self.columns_stretch = self.table.list_columns_stretch_treeview    # Динамическое изменения колонок
        self.columns_width = self.table.list_columns_width_treeview        # Ширина колонок
        self.columns_icon = self.table.list_columns_icons_treeview         # Ссылки на иконки для каждой колонки

        super().__init__(parent, *args, columns=self.columns,  **kwargs)


        # Customize column widths and settings if provided
        if self.columns:
            self.setup_columns()
            self.populate()


    def setup_styles(self):
        """Устанавливает кастомные стили для Treeview и его заголовков."""
        tree_style = ttk.Style()  # Определяем стиль для Treeview
        tree_style.theme_use("default") #clam


        # Настройка общего стиля для строки
        tree_style.configure(
            "Custom.Treeview", 
            background=BG_TREE_ROW, 
            fieldbackground=BG_APP_COLOR, # BG где нету записей BG_TREE_ROW
            foreground="#ffefe1", 
            rowheight=25,                   # Высота строки
            borderwidth=0,                # Толщина рамки
            relief="flat",                # Убрать видимость границы
            highlightthickness=0,         # Толщина выделенной рамки при фокусе
        )
        
        # Настроить стиль для заголовка Treeview
        tree_style.configure(
            "Custom.Treeview.Heading",
            background=BG_TREE_HEADER,
            foreground=FG_TREE_HEADER,
            font=("Arial", 10, "bold"),
            borderwidth=0,
            padding=5
        )

        # Настроить стиль для заголовков при выделении, не работают, но блокируют костомные стили
        tree_style.map(
            "Custom.Treeview.Heading",
            background=[('hover', '#22253c')]
        )

        tree_style.map(
            "Custom.Treeview",
            background=[('selected', '#22253c')]
        )
        

    # Настройка колонок таблицы
    def setup_columns(self):
        """Setup column headings and customize each column."""
        for i in range(len(self.columns)):
            # Динамическое подставления иконки
            if len(self.columns_icon) > i:
                self.heading(self.columns[i], text=self.columns_name[i], command=lambda i=i: self.sort(i, False), anchor='w', image=self.columns_icon[i])
            else:    
                self.heading(self.columns[i], text=self.columns_name[i], command=lambda i=i: self.sort(i, False), anchor='w')
            self.column(self.columns[i], stretch=self.columns_stretch[i], width=self.columns_width[i])

    # Получение данных с БД и отрисовка их в таблице
    def populate(self):
        """Populate the treeview with data."""
        # get_all_phones
        for row in self.table.get_all_data():
            #self.insert('', tk.END, values=tuple(row.values()), image=self.columns_icon[1]) - image похожу не надо, наверное тестил 
            self.insert('', tk.END, values=tuple(row.values()))

    # Перерисовать данные в таблице
    def refresh_treeview(self):
        # Очистите текущие данные в treeview
        for item in self.get_children():
            self.delete(item)
        
        # Отрисовать данные с таблице (взять с бд)
        self.populate()

    # Сортировка таблицы по нажатию на заголовок
    def sort(self, col: int, reverse: bool):
        """ Сортировка таблицы
            - Col - Номер колонки, которую нажали
            - reverse - Переключатель сортировки (от А до Я и от Я до А)
        """
        l = [(self.set(k, col), k) for k in self.get_children("")]  # Получаем все значения столбцов
        l.sort(reverse=reverse)  # Сортируем список
        for index, (_, k) in enumerate(l):
            self.move(k, "", index)  # Переупорядочиваем значения
        self.heading(col, command=lambda: self.sort(col, not reverse))  # Включаем сортировку в обратном порядке

    def clear_selection(self):
        """Функция для очистки выделения в таблице"""
        self.selection_remove(self.selection())
        print("Выделение снято.")
    


# Кнопка: Удалить 
class ButtonDellPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Удалить, красная"""

        super().__init__(parent,  *args, **kwargs)
        # https://ru.freepik.com/icon/delete_10024276#fromView=search&page=1&position=9&uuid=07166359-5077-49c7-ae25-13e878c4ad94
        self.icon = PhotoImage(file="img\\delete.png")  # Укажите путь к вашему файлу PNG

        # Настройки стиля кнопки
        self.configure(
            bg=BG_BUTTON_DELL,                           # Основной цвет фона
            fg=FG_APP_COLOR,                        # Цвет текста
            activebackground=BG_BUTTON_ACTIVE_DELL,      # Фон при нажатии
            activeforeground=FG_APP_COLOR,          # Цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5,
            image=self.icon, # Указываем иконку
            compound="left" # # Иконка слева от текста
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Активировать кнопку
    def state_normal(self):
        self['state'] = 'normal'

    # Деактивировать кнопку
    def state_disabled(self):
        self['state'] = 'disabled'

    # Обработка навидения на кнопку
    def on_enter(self, e):
        self['bg'] = BG_BUTTON_HOVER_DELL   # Изменяем фон при наведении

    def on_leave(self, e):
        self['bg'] = BG_BUTTON_DELL         # Возвращаем основной фон

# Кнопка: Редактировать 
class ButtonEditPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Отправить (Синяя)"""
        super().__init__(parent, *args, **kwargs)
        # https://ru.freepik.com/icon/pen-square_10435606#fromView=search&page=1&position=0&uuid=a17bebde-889a-4ad2-9171-6754b74ce3a6
        self.icon = PhotoImage(file="img\\edit.png")  # Укажите путь к вашему файлу PNG

        # Настройки стиля кнопки
        self.configure(
            bg=BG_BUTTON_EDIT,                           # Основной цвет фона
            fg=FG_APP_COLOR,                        # Цвет текста
            activebackground=BG_BUTTON_ACTIVE_EDIT,      # Фон при нажатии
            activeforeground=FG_APP_COLOR,          # Цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5,
            image=self.icon, # Указываем иконку
            compound="left" # # Иконка слева от текста
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Активировать кнопку
    def state_normal(self):
        self['state'] = 'normal'

    # Деактивировать кнопку
    def state_disabled(self):
        self['state'] = 'disabled'

    # Обработка навидения на кнопку
    def on_enter(self, e):
        self['bg'] = BG_BUTTON_HOVER_EDIT   # Изменяем фон при наведении

    def on_leave(self, e):
        self['bg'] = BG_BUTTON_EDIT         # Возвращаем основной фон

# Кнопка: Добавить / Создать
class ButtonAddPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Отправить (Синяя)"""
        super().__init__(parent, *args, **kwargs)

        # Настройки стиля кнопки
        self.configure(
            bg=BG_BUTTON_ADD,                           # Основной цвет фона
            fg=FG_APP_COLOR,                        # Цвет текста
            activebackground=BG_BUTTON_ACTIVE_ADD,      # Фон при нажатии
            activeforeground=FG_APP_COLOR,          # Цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Активировать кнопку
    def state_normal(self):
        self['state'] = 'normal'

    # Деактивировать кнопку
    def state_disabled(self):
        self['state'] = 'disabled'

    # Обработка навидения на кнопку
    def on_enter(self, e):
        self['bg'] = BG_BUTTON_HOVER_ADD   # Изменяем фон при наведении

    def on_leave(self, e):
        self['bg'] = BG_BUTTON_ADD         # Возвращаем основной фон

# Кнопка: Копироват
class ButtonCopyPro(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        """Кнопка: Отправить (Синяя)"""
        super().__init__(parent, *args, **kwargs)
        # https://ru.freepik.com/icon/page_4640724#fromView=search&page=1&position=16&uuid=6a718d97-6177-4fca-93b4-0164ca02caeb
        self.icon = PhotoImage(file="img\\copy.png")  # Укажите путь к вашему файлу PNG

        # Настройки стиля кнопки
        self.configure(
            bg=BG_BUTTON_COPY,                           # Основной цвет фона
            fg=FG_APP_COLOR,                        # Цвет текста
            activebackground=BG_BUTTON_ACTIVE_COPY,      # Фон при нажатии
            activeforeground=FG_APP_COLOR,          # Цвет текста при нажатии
            borderwidth=0,                          # Толщина границы
            relief="solid",                         # Стиль границы
            font=('Arial', INPUT_FONT_SIZE, 'bold'),# Шрифт текста
            highlightthickness=0,                   # Убираем подсветку рамки
            padx=10,                                # Внутренние отступы
            pady=5,
            image=self.icon, # Указываем иконку
            compound="left" # # Иконка слева от текста
        )

        # Привязываем событие для изменения фона при наведении
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # Активировать кнопку
    def state_normal(self):
        self['state'] = 'normal'

    # Деактивировать кнопку
    def state_disabled(self):
        self['state'] = 'disabled'

    # Обработка навидения на кнопку
    def on_enter(self, e):
        self['bg'] = BG_BUTTON_HOVER_COPY   # Изменяем фон при наведении

    def on_leave(self, e):
        self['bg'] = BG_BUTTON_COPY         # Возвращаем основной фон


# Всплывающее коковое сообщение
class Toast:
    """ Важно, виджет отображаеться как все остальные и влияет на данные и может 
    их смещать как и остальные фреймы, вызывать нужно с самого правого компонета приложения
    Относительно него будет отображения
    
    Пример вызова: Toast(self.table_control, "⛔️ Ошибка", 'Невалидный номер +38097...')
    """
    def __init__(self, parent, title, message, duration=2500):
        self.parent = parent # Привязка к клавному окну
        self.title = title # Заголовк
        self.message = message # Текст сообщения
        self.duration = duration # Время отображения окна
        width=250 # Шырина контейнера
        height=60 # Высотка контейнера
        
        # Койтейнер
        self.toast_frame = tk.Frame(parent, bg=BG_INPUT_COLOR, padx=5, pady=5, width=width, height=height, borderwidth=2, relief='groove')
        self.toast_frame.pack_propagate(False)  # Отключаем автоматическое изменение размера
        self.toast_frame.pack(side="bottom", anchor="e", padx=10, pady=10)  # Размещаем внизу справа

        # Заголовок
        self.toast_label_title = tk.Label(self.toast_frame, text=self.title, fg=FG_APP_COLOR, bg=BG_INPUT_COLOR, font=("Arial", 13))
        self.toast_label_title.pack(anchor='w', padx=0, pady=0)

        # Сообщение
        self.toast_label = tk.Label(self.toast_frame, text=self.message, fg=FG_APP_COLOR, bg=BG_INPUT_COLOR, font=("Arial", 9))
        self.toast_label.pack(anchor='w', padx=0)
        
        # Таймер для автоматического закрытия через duration миллисекунд
        self.parent.after(self.duration, self.hide)

    def hide(self):
        self.toast_frame.pack_forget()  # Убираем Toast с экрана