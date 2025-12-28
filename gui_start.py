from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
from PIL import Image, ImageTk
from datetime import datetime
from pathlib import Path
import script as script_module
from regex import *
import data, json, sys, os, subprocess, time
import dictionary_of_transitions.build_dictionary as build_dictionary
import graph_metrics
import graph  # Убедитесь, что у вас есть graph.py
import re

characteristics = {}
tps = {}

root = Tk()
root.title("Редактор семантического объекта")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Устанавливаем размер и положение окна
root.geometry(f"{screen_width}x{screen_height - 70}+{-10}+{0}")
root.option_add("*tearOff", FALSE)

frame_width = screen_width // 2

# Создаем фрейм для отображения элементов для работы с характеристиками
frame_results = Frame(root, width=50)  # bg = "purple",
frame_results.grid(row=0, column=2, padx=5, pady=5)

# ------------------------------------------------------------------- FRAME TP -------------------------------------------------------------------

class App:
    def __init__(self, root):
        self.root = root
        global characteristics
        global tps
        global regex
        self.button_counter = 0  # Счетчик кнопок

        if characteristics:
            last_key = next(reversed(characteristics.keys()))  # Находим максимальный ключ
            last_num = int(last_key[1:])  # Извлекаем номер, преобразуем в int
            self.q_counter = last_num + 1
        else:
            self.q_counter = 1

        self.buttons = {}  # Словарь для хранения кнопок
        self.text_area = {}  #
        self.scrollbars = {}  # Словарь для хранения скроллбаров
        self.text_reg = {}  # Словарь для хранения текстовых полей регулярных выражений
        self.transitions = None  # Для хранения графа после генерации

        # Создаем Canvas и Scrollbar
        self.canvas = tk.Canvas(root, width=frame_width + 100, height=screen_height - 100)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)

        # Создаем фрейм в Canvas
        self.frame_tp = ttk.Frame(self.canvas, height=screen_height - 50,)
        self.canvas.create_window((0, 0), window=self.frame_tp, anchor="nw")

        # Привязываем настройку области прокрутки к изменению конфигурации
        self.frame_tp.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Настройка прокрутки
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Расположение элементов на главном окне
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Изначальная кнопка
        self.create_widgets()

    # ------------------------------------------------------------------- создание стартовых элементов -------------------------------------------------------------------

    def create_widgets(self):
        # Создаем фрейм для работы с характеристиками
        characteristics_frame = ttk.Frame(frame_results, width=frame_width - 690,)
        characteristics_frame.grid(row=0, column=0, padx=5, pady=5)

        # Подпись к полю
        char_name = tk.Label(characteristics_frame, text="Характеристики")
        char_name.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        # Создаем поле для характеристик объекта
        self.char_obj_txt = tk.Text(characteristics_frame, width=frame_width - 690, height=10)
        self.char_obj_txt.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="w")

        if characteristics:
            self.char_obj_txt.delete(1.0, tk.END)
            for key, value in characteristics.items():
                self.char_obj_txt.insert(tk.INSERT, key + ": " + value + "\n")

        # Кнопка для редактирования характеристик
        self.button_edit_char = ttk.Button(characteristics_frame, text="Сохранить характеристики", state=NORMAL, command=self.save_changes)
        self.button_edit_char.grid(row=2, column=0, padx=5, pady=5)

        # Подпись к полю
        obj_name = tk.Label(frame_results, text="Имя объекта")
        obj_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Создаем поле для имени объекта
        self.name_obj_txt = tk.Text(frame_results, width=frame_width - 690, height=1)
        self.name_obj_txt.grid(row=2, column=0, padx=5, pady=5)

        # Создаем поле для регулярного выражения
        self.regex_txt = tk.Text(frame_results, width=frame_width - 690, height=5)
        self.regex_txt.grid(row=3, column=0, padx=5, pady=5)

        # Установка валидации для текстового поля
        self.regex_txt.bind("<Key>", self.on_key)

        # Создаем фрейм для кнопок работы с регулярным выражением
        self.job_button_frame = ttk.Frame(frame_results)
        self.job_button_frame.grid(row=4, column=0, padx=5, pady=5)

        # Кнопка для запуска генерации регулярного выражения
        self.button_generate = ttk.Button(self.job_button_frame, text="Генерация", state=NORMAL, command=self.start_generation)
        self.button_generate.grid(row=0, column=0, padx=5, pady=5)

        # Кнопка для записи объекта в файл
        self.button_save_obj = ttk.Button(self.job_button_frame, text="Сохранить объект", state=DISABLED, command=self.save_object)
        self.button_save_obj.grid(row=0, column=1, padx=5, pady=5)

        # --- Кнопка: Показать граф состояний ---
        self.button_plot_state_graph = ttk.Button(
            self.job_button_frame, text="Показать граф состояний", state=DISABLED, command=self.show_state_graph
        )
        self.button_plot_state_graph.grid(row=0, column=2, padx=5, pady=5)

        # --- Кнопка: Показать граф характеристик ---
        self.button_plot_char_graph = ttk.Button(
            self.job_button_frame, text="Показать граф характеристик", state=DISABLED, command=self.show_char_graph
        )
        self.button_plot_char_graph.grid(row=0, column=3, padx=5, pady=5)

        # Фрейм для метрик графа
        metrics_frame = ttk.LabelFrame(frame_results, text="Метрики графа", width=frame_width - 690)
        metrics_frame.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        # Поле для отображения метрик
        self.metrics_txt = tk.Text(metrics_frame, width=frame_width - 690, height=4, state=tk.DISABLED)
        self.metrics_txt.grid(row=0, column=0, padx=5, pady=5)

        # Фрейм для категорий характеристик
        categories_frame = ttk.LabelFrame(frame_results, text="Категории характеристик по метрикам", width=frame_width - 690)
        categories_frame.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        # Поле для отображения категорий
        self.categories_txt = tk.Text(categories_frame, width=frame_width - 690, height=8, state=tk.DISABLED)
        self.categories_txt.grid(row=0, column=0, padx=5, pady=5)

        # Скроллбар для категорий
        categories_scrollbar = ttk.Scrollbar(categories_frame, orient="vertical", command=self.categories_txt.yview)
        categories_scrollbar.grid(row=0, column=1, sticky='ns')
        self.categories_txt['yscrollcommand'] = categories_scrollbar.set

        # Фрейм для выбора типа градации
        gradation_frame = ttk.Frame(frame_results)
        gradation_frame.grid(row=7, column=0, padx=5, pady=5)

        # Метка для выбора градации
        gradation_label = tk.Label(gradation_frame, text="Тип градации:")
        gradation_label.grid(row=0, column=0, padx=5, pady=5)

        # Переменная для выбора типа градации
        self.gradation_type = tk.StringVar(value="simple")

        # Радиокнопки для выбора типа градации
        simple_radio = ttk.Radiobutton(gradation_frame, text="Простая (0.5, 0.75, 1.0)",
                                       variable=self.gradation_type, value="simple")
        simple_radio.grid(row=0, column=1, padx=5, pady=5)

        detailed_radio = ttk.Radiobutton(gradation_frame, text="Детальная (0.5-1.0)",
                                         variable=self.gradation_type, value="detailed")
        detailed_radio.grid(row=0, column=2, padx=5, pady=5)

    def confirm_action(self):
        return messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сохранить характеристики?")

    def save_changes(self):
        if self.confirm_action():
            # Чтение текстового поля
            text = self.char_obj_txt.get("1.0", tk.END).strip()
            print(text)
            global characteristics
            characteristics = {}  # Очистка словаря, чтобы заново заполнить его

            # Парсинг текста обратно в словарь
            for line in text.split('\n'):
                print(line)
                line = line.strip()  # Убираем пробелы в начале и конце строки
                if line:  # Проверка, чтобы не обработать пустые строки
                    if ':' in line:  # Проверка на наличие двоеточия
                        key, value = line.split(':', 1)  # Разделяем по первому двоеточию
                        characteristics[key.strip()] = value.strip()  # Убираем лишние пробелы
                    else:
                        print(f"Пропущенная строка: '{line}' (нет двоеточия)")

            print("Сохранено:", characteristics)  # Выводим сохранённые данные в словаре

    # ------------------------------------------------------------------- ВАЛИДАТОР -------------------------------------------------------------------

    def validate_input(self, char):
        allowed_chars = "q()|1234567890"  # Разрешённые символы
        return char in allowed_chars or char == ''  # Позволяем удаление символов

    def on_key(self, event):
        if event.keysym in ('BackSpace', 'Delete'):  # Проверяем нажатие клавиш Backspace и Delete
            return  # Разрешаем удаление
        if not self.validate_input(event.char):
            return "break"  # Блокируем ввод, если символ не разрешён

    # ------------------------------------------------------------------- работа с тектовыми потоками -------------------------------------------------------------------

    def add_tp_new(self):
        self.add_tp()
        second_menu.entryconfig("Редактирование объекта", state="disable")

    def add_tp_edit(self):
        self.add_tp()

    def add_tp(self):
        # Создание имени для текущего ТФ
        tp_name = f"ТФ {self.button_counter + 1}"

        # Создаем фрейм для кнопок
        self.button_frame = ttk.Frame(self.frame_tp)
        self.button_frame.grid(row=self.button_counter + 1, column=1, padx=5, pady=5)

        # Создаем фрейм текстового поля и скролла
        self.text_frame = ttk.Frame(self.frame_tp)
        self.text_frame.grid(row=self.button_counter + 1, column=0, padx=5, pady=5)

        # Создание новой кнопки "Загрузить ТФ"
        new_btn = ttk.Button(self.button_frame, text=f"Загрузить {tp_name}", command=lambda: self.load_tp(tp_name, new_btn, new_text_area), width=15)
        new_btn.grid(row=0, column=0, padx=5, pady=5)
        self.buttons[tp_name] = new_btn  # Сохраняем кнопку в словаре

        # Создание нового текстового поля
        new_text_area = tk.Text(self.text_frame, width=60, height=8)
        new_text_area.grid(row=0, column=0, pady=5)
        self.text_area[tp_name] = new_text_area

        # Создание нового скроллбара
        new_scrollbar = ttk.Scrollbar(self.text_frame, orient="vertical", command=new_text_area.yview)
        new_scrollbar.grid(row=0, column=1, sticky='ns')
        new_text_area['yscrollcommand'] = new_scrollbar.set  # Привязка скроллбара к текстовому полю

        # Создание нового текстового поля для регулярного выражения
        new_text_reg = tk.Text(self.text_frame, width=60, height=3)
        new_text_reg.grid(row=1, column=0, pady=5)
        self.text_reg[tp_name] = new_text_reg

        # Добавляем текстовое поле и скроллбар в словари
        self.scrollbars[tp_name] = new_scrollbar

        # Кнопка "Удалить"
        delete_btn = ttk.Button(self.button_frame, text="Удалить", command=lambda: self.delete_tp(tp_name, new_text_area, new_btn, delete_btn, new_scrollbar, new_text_reg), width=15)
        delete_btn.grid(row=1, column=0, padx=5, pady=5)

        # Привязываем контекстное меню
        self.create_context_menu(new_text_area)

        # Увеличение счетчика
        self.button_counter += 1

    def load_tp(self, tp_name, button, new_text_area):
        button.config(state=tk.DISABLED)
        tps[tp_name] = new_text_area

        # Открытие диалогового окна для выбора файла
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                # Читаем содержимое файла
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Записываем содержимое в текстовое поле
                tps[tp_name].delete(1.0, tk.END)  # Очищаем текстовое поле
                tps[tp_name].configure(state="normal")
                tps[tp_name].insert(tk.INSERT, content)  # Вставляем загруженный контент в текстовое поле
                tps[tp_name].configure(state="disabled")

                tps[tp_name] = content  # Добавляем в словарь

            except Exception as e:
                print("Ошибка при загрузке файла:", e)

    def delete_tp(self, tp_name, text_area, load_btn, delete_btn, scrollbar, text_reg):
        # Удаляем текстовое поле, кнопки и скроллбар из интерфейса
        text_area.destroy()
        load_btn.destroy()
        delete_btn.destroy()
        scrollbar.destroy()  # Удаляем скроллбар
        text_reg.destroy()

        # Удаляем записи из словарей
        if tp_name in tps:
            del tps[tp_name]
        if tp_name in self.buttons:
            del self.buttons[tp_name]
        if tp_name in self.scrollbars:
            del self.scrollbars[tp_name]

        print(f"{tp_name} успешно удален.")

    def print_tps(self):
        # Выводим содержимое tps в консоль
        for key, value in tps.items():
            print(f"{key}: {value}")

    def print_characteristics(self):
        # Выводим содержимое characteristics в консоль
        for key, value in characteristics.items():
            print(f"{key}: {value}")

    # ------------------------------------------------------------------- СКРОЛ и КОНТЕКСТНОЕ МЕНЮ -------------------------------------------------------------------

    def on_mouse_wheel(self, event):
        # Управление прокруткой колесом мыши
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def add_mouse_wheel_bindings(self):
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows и Mac
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux прокрутка вверх
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))  # Linux прокрутка вниз

    def create_context_menu(self, text_area):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=lambda: self.copy_text())
        self.context_menu.add_command(label="Вставить", command=lambda: self.paste_text())
        self.context_menu.add_command(label="Создать характеристику", command=lambda: self.save_char())
        text_area.bind("<Button-3>", lambda event: self.show_context_menu(event, text_area))

    def show_context_menu(self, event, text_area):
        text_area.focus_set()  # Устанавливает фокус на текстовое поле
        self.context_menu.post(event.x_root, event.y_root)

    def save_char(self):
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            try:
                # Проверяем, есть ли выделенный текст
                if active_text_area.tag_ranges("sel"):
                    selected_text = active_text_area.get("sel.first", "sel.last")  # Получаем выделенный текст

                    # Подсвечиваем выбранный текст
                    start = active_text_area.index("sel.first")
                    end = active_text_area.index("sel.last")
                    active_text_area.tag_add("highlight", start, end)
                    # Устанавливаем параметры тега цветом
                    active_text_area.tag_config("highlight", background="lightgray")

                    # Сохраняем выделенный текст в словаре
                    key = f'q{self.q_counter}'  # Составляем ключ q1, q2, ...
                    characteristics[key] = selected_text  # Добавляем в словарь
                    self.q_counter += 1  # Увеличиваем счетчик для следующего ключа

                    self.char_obj_txt.mark_set(tk.INSERT, tk.END)
                    self.char_obj_txt.insert(tk.INSERT, key + ": " + selected_text + "\n")
                    self.char_obj_txt.see(tk.END)

                else:
                    messagebox.showwarning("Предупреждение", "Нет выделенного текста.")
            except tk.TclError:
                pass  # Игнорируем ошибку, если ничего не выделено

    # ------------------------------------------------------------------- РАБОТА С ТЕКСТОМ -------------------------------------------------------------------

    def copy_text(self):
        # Получаем текущее активное текстовое поле
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            try:
                # Проверяем, есть ли выделенный текст
                if active_text_area.tag_ranges("sel"):
                    selected_text = active_text_area.get("sel.first", "sel.last")  # Получаем выделенный текст
                    self.root.clipboard_clear()  # Очищаем буфер обмена
                    self.root.clipboard_append(selected_text)  # Добавляем выделенный текст в буфер обмена
                    print("Текст скопирован:", selected_text)  # Для отладки
            except tk.TclError:
                pass  # Игнорируем ошибку, если ничего не выделено

    def paste_text(self):
        # Получаем текущее активное текстовое поле
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            try:
                # Вставляем текст из буфера обмена
                active_text_area.insert(tk.INSERT, self.root.clipboard_get())
            except tk.TclError:
                pass  # Игнорируем ошибку, если буфер обмена пуст

    def insert_regex(self, regex):
        """Вставляет регулярное выражение в текстовое поле"""
        try:
            self.regex_txt.configure(state=NORMAL)
            self.regex_txt.delete(1.0, tk.END)  # Очищаем текстовое поле
            if regex:
                self.regex_txt.insert(tk.INSERT, regex)  # Вставляем загруженный контент в текстовое поле
            # Принудительно обновляем интерфейс
            self.root.update_idletasks()
            print(f"Регулярное выражение вставлено в поле: {regex}")
        except Exception as e:
            print(f"Ошибка при вставке регулярного выражения: {e}")
            import traceback
            traceback.print_exc()

    def insert_name(self, name):
        self.name_obj_txt.delete(1.0, tk.END)  # Очищаем текстовое поле
        self.name_obj_txt.insert(tk.INSERT, name)

    def display_metrics(self, metrics):
        """Отображает метрики графа в интерфейсе"""
        self.metrics_txt.configure(state=tk.NORMAL)
        self.metrics_txt.delete(1.0, tk.END)

        metrics_text = f"Вершины (характеристики): {metrics['vertices']}\n"
        metrics_text += f"Дуги (переходы): {metrics['edges']}\n"
        metrics_text += f"Плотность графа: {metrics['density']}\n"
        metrics_text += f"Оценка сложности: {metrics['complexity_score']:.3f}"

        self.metrics_txt.insert(tk.INSERT, metrics_text)
        self.metrics_txt.configure(state=tk.DISABLED)

    def display_categories(self, categories_data):
        """Отображает категории характеристик в интерфейсе"""
        self.categories_txt.configure(state=tk.NORMAL)
        self.categories_txt.delete(1.0, tk.END)

        categories_text = f"Всего вершин: {categories_data['total_vertices']}, Всего дуг: {categories_data['total_edges']}\n"
        categories_text += f"Используемая градация: {', '.join([str(g) for g in categories_data['gradation']])}\n"
        categories_text += "=" * 60 + "\n\n"

        # Сортируем категории по значению (от меньшего к большему)
        sorted_categories = sorted(categories_data['categories'].items(), key=lambda x: float(x[0]))

        for category, data in sorted_categories:
            categories_text += f"Категория {category} (сложность ≤ {category}):\n"
            categories_text += f"  Количество характеристик: {data['count']}\n"
            categories_text += f"  Характеристики: {', '.join(data['characteristics'])}\n"

            # Добавляем детали для каждой характеристики
            for detail in data['details']:
                categories_text += f"    - {detail['char']}: исходящих дуг={detail['local_edges']}, "
                categories_text += f"локальная сложность={detail['local_complexity']}\n"

            categories_text += "\n"

        self.categories_txt.insert(tk.INSERT, categories_text)
        self.categories_txt.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------- ГЕНЕРАЦИЯ -------------------------------------------------------------------

    def start_generation(self):
        # Проверка на пустой словарь tps
        if not tps or len(tps) == 0:
            messagebox.showwarning("Предупреждение",
                                   "Нет текстовых потоков для обработки. Пожалуйста, добавьте хотя бы один текстовый поток.")
            return

        # Проверка на наличие характеристик
        if not characteristics or len(characteristics) == 0:
            messagebox.showwarning("Предупреждение",
                                   "Нет характеристик объекта. Пожалуйста, добавьте характеристики перед генерацией.")
            return

        value_of_pers = 100 / (len(tps))  # Прогресс для каждого потока
        len_tps = len(tps)  # Кол-во потоков
        self.tp_counter = 1

        # Прогрессбар
        self.progress = ttk.Progressbar(frame_results, orient='horizontal', length=100, mode='determinate')
        self.progress.grid(row=8, column=0, padx=5, pady=5)

        # Метка для статуса
        self.status_label = tk.Label(frame_results, text=f"Осталось потоков: {len_tps}")
        self.status_label.grid(row=9, column=0, padx=5, pady=5)

        scripts = []  # Список для хранения созданных скриптов

        for key, value in tps.items():
            # Получаем текст из Text виджета, если value - это объект Text
            if isinstance(value, tk.Text):
                text_content = value.get("1.0", tk.END).strip()
            else:
                # Если это уже строка (например, при загрузке из файла)
                text_content = str(value).strip()

            # Пропускаем пустые текстовые потоки
            if not text_content:
                print(f"Пропущен пустой текстовый поток: {key}")
                continue

            script = script_module.extract_scripts(text_content, characteristics)
            print(f"Последовательность хар-к {key}: ", script)

            self.text_area[key].delete(1.0, tk.END)
            self.text_reg[key].insert(tk.INSERT, script)  # Вставляем контент в текстовое поле

            scripts.append(script)  # Добавляем созданный скрипт в список
            self.tp_counter += 1  # Увеличиваем счетчик для следующего потока
            len_tps -= 1
            self.progress['value'] += value_of_pers  # Увеличиваем значение прогрессбара
            self.root.update()  # Обновляем интерфейс
            self.status_label.config(text=f"Осталось потоков: {len_tps}")
            time.sleep(2)

        # Проверка, что есть хотя бы один скрипт
        if not scripts or len(scripts) == 0:
            messagebox.showwarning("Предупреждение",
                                   "Не удалось извлечь скрипты из текстовых потоков. Убедитесь, что слова в текстах совпадают со словами в характеристиках.")
            self.insert_regex("")  # Очищаем поле
            return

        # Проверка, что скрипты не пустые
        non_empty_scripts = [s for s in scripts if s and len(s) > 0]
        if not non_empty_scripts:
            messagebox.showwarning("Предупреждение",
                                   "Все скрипты пустые. Убедитесь, что слова в текстах совпадают со словами в характеристиках.")
            self.insert_regex("")  # Очищаем поле
            return

        scripts = non_empty_scripts  # Используем только непустые скрипты

        try:
            # Поиск первых и последних ребер
            start_edges = list(set(script_module.get_start_elements(scripts)))
            print("Первыми ребрами могут быть", start_edges)
            finish_edges = list(set(script_module.get_finish_elements(scripts)))
            print("Последними ребрами могут быть", finish_edges)

            print("-" * 20)

            dict_char = script_module.build_dict_char(scripts)
            print("Словарь хар-к объекта: ", dict_char)
            self.dict_char = dict_char

            # Вычисляем метрики графа и категории характеристик
            gradation_type = self.gradation_type.get()
            categories_data = graph_metrics.get_characteristics_by_category(dict_char, gradation_type)

            # Отображаем метрики
            self.display_metrics(categories_data['metrics'])

            # Отображаем категории характеристик
            self.display_categories(categories_data)

            print("*" * 20)

            # transitions = build_dictionary.build_main_dict(dict_char, start_edges, finish_edges)
            transitions = build_dictionary.build_main_dict(dict_char, start_edges, finish_edges, scripts)
            print(transitions)

            # Сохраняем граф переходов для последующей визуализации
            self.transitions = transitions

            print("*" * 20)

            print(
                "--------------------------------------------------------------------------------------------------------------------")

            # Проверяем наличие начального состояния 'S0' в словаре переходов
            if 'S0' not in transitions:
                # Ищем начальное состояние (обычно это первое состояние, начинающееся с 'S')
                initial_states = [s for s in transitions.keys() if isinstance(s, str) and s.startswith('S')]
                if initial_states:
                    # Сортируем и берем первое (обычно S0)
                    initial_states.sort()
                    initial_state = initial_states[0]
                    print(f"Начальное состояние 'S0' не найдено, используем '{initial_state}'")
                else:
                    messagebox.showerror("Ошибка", "Не найдено начальное состояние в словаре переходов.")
                    self.insert_regex("")
                    return
            else:
                initial_state = 'S0'

            # Генерируем регулярное выражение, начиная с начального состояния
            print(f"Генерируем регулярное выражение, начиная с состояния '{initial_state}'")
            regex = build_regex(initial_state, transitions)
            print("Регулярное выражение", regex)

            # Проверяем, что регулярное выражение не пустое
            if not regex or regex.strip() == "":
                messagebox.showwarning("Предупреждение",
                                       "Не удалось сгенерировать регулярное выражение. Проверьте данные и попробуйте снова.")
                self.insert_regex("")  # Очищаем поле
            else:
                self.insert_regex(regex)
                self.button_save_obj.config(state="normal")
                self.button_plot_state_graph.config(state="normal")  # Активируем кнопку "Показать граф"
                self.button_plot_char_graph.config(state="normal")
                messagebox.showinfo("Успех", "Регулярное выражение успешно сгенерировано!")

        except Exception as e:
            error_msg = f"Ошибка при генерации регулярного выражения: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            messagebox.showerror("Ошибка", error_msg)
            self.insert_regex("")  # Очищаем поле при ошибке

    # ------------------------------------------------------------------- ПОКАЗ ГРАФА В ОТДЕЛЬНОМ ОКНЕ -------------------------------------------------------------------

    def show_state_graph(self):
        """Открывает граф состояний (S0, S1, Z)"""
        if not self.transitions:
            messagebox.showwarning("Предупреждение", "Нет данных для построения графа состояний.")
            return

        try:
            import graph
            graph.plot_state_graph(self.transitions, "state_graph.png")

            window = Toplevel(self.root)
            window.title("Граф состояний")
            window.geometry("900x700")

            img = Image.open("state_graph.png")
            img = img.resize((850, 650), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = Label(window, image=photo)
            label.image = photo
            label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить граф состояний: {e}")

    def show_char_graph(self):
        """Открывает граф переходов между характеристиками (q1 → q2 → q3)"""
        if not hasattr(self, 'dict_char') or not self.dict_char:
            messagebox.showwarning("Предупреждение", "Нет данных для построения графа характеристик.")
            return

        try:
            import graph
            graph.plot_char_graph(self.dict_char, "char_graph.png")

            window = Toplevel(self.root)
            window.title("Граф характеристик")
            window.geometry("900x700")

            img = Image.open("char_graph.png")
            img = img.resize((850, 650), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = Label(window, image=photo)
            label.image = photo
            label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить граф характеристик: {e}")

    # ------------------------------------------------------------------- СОХРАНЕНИЕ ОБЪЕКТА -------------------------------------------------------------------

    def save_object(self):
        regex = self.regex_txt.get("1.0", tk.END)
        name = app.name_obj_txt.get("1.0", "end-1c")

        # Создаем новый словарь с переименованными ключами
        renamed_dict = {}
        for i, (key, value) in enumerate(tps.items(), start=1):
            renamed_key = f"ТФ {i}"
            if isinstance(value, tk.Text):
                text_content = value.get("1.0", tk.END).strip()
            else:
                text_content = str(value).strip()
            renamed_dict[renamed_key] = text_content

        if name:
            self.data_to_save = {
                "name": name,
                "reg_var": regex,
                "props": characteristics,
                "tps": renamed_dict
            }

            directory = "objects"
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = os.path.join(directory, name + '.json')
            if os.path.exists(filename):
                messagebox.showwarning("Предупреждение",
                                       f"Файл с именем '{name}.json' уже существует. Выберите другое имя.")
                return

            try:
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump(self.data_to_save, json_file, ensure_ascii=False)
                messagebox.showinfo("Успех", f"Объект успешно сохранён: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
        else:
            messagebox.showwarning("Предупреждение", "Имя файла не может быть пустым.")


# ------------------------------------------------------------------- ГЛОБАЛЬНЫЕ ФУНКЦИИ -------------------------------------------------------------------

def select_object():
    global tps
    global regex
    global characteristics

    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    second_menu.entryconfig("Создание объекта", state="disable")
    editor_menu.entryconfig("Добавить текстовый поток", state="normal")
    editor_menu.entryconfig("Выбрать объект", state="disable")

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                messagebox.showinfo("Успех", "Файл успешно загружен!")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка декодирования JSON.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

        # Извлечение данных
        name = data['name']
        regex = str(data['reg_var'])
        characteristics = data['props']
        tps = data['tps']

        # Удаление временной метки из имени, если есть
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}'
        name = re.sub(pattern, '', name)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':', '-')

        app.insert_name(name + " " + current_datetime)
        app.insert_regex(regex)

        for key, value in tps.items():
            app.add_tp_edit()
            app.text_area[key].insert(tk.INSERT, value)


def restart_program():
    messagebox.showerror("Перезагрузка", f"Нажмите 'ОК' и дождитесь перезагрузки редактора")
    current_script_path = Path(__file__).resolve()
    subprocess.Popen([sys.executable, str(current_script_path)])
    sys.exit()


# ------------------------------------------------------------------- ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ -------------------------------------------------------------------

app = App(root)

main_menu = Menu()
second_menu = Menu()
create_menu = Menu(second_menu)
editor_menu = Menu()

editor_menu.add_command(label="Выбрать объект", command=select_object)
editor_menu.add_command(label="Добавить текстовый поток", command=app.add_tp, state=DISABLED)

create_menu.add_command(label="Добавить текстовый поток", command=app.add_tp_new)

second_menu.add_cascade(label="Создание объекта", menu=create_menu)
second_menu.add_cascade(label="Редактирование объекта", menu=editor_menu)
second_menu.add_separator()
second_menu.add_command(label="Вывести все ТФ объекта", command=app.print_tps)
second_menu.add_command(label="Вывести все характеристики объекта", command=app.print_characteristics)
second_menu.add_separator()
second_menu.add_command(label="Начать работу с новым объектом", command=restart_program)

main_menu.add_cascade(label="Редактор семантических объектов", menu=second_menu)

root.config(menu=main_menu)
root.mainloop()