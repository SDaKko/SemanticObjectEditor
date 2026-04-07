from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
from PIL import Image, ImageTk
from datetime import datetime
from pathlib import Path
import script as script_module
from regex import *
import data, json, sys, os, subprocess, time
import transitions_builder
import graph_metrics
from tkinter import simpledialog
import graph
import re
from dotenv import load_dotenv
import os



# Проверка наличия llm_generator.py
# --- ПОДКЛЮЧЕНИЕ GIGACHAT ---
LLM_AVAILABLE = False
generator = None

try:
    from llm_generator import LLMGenerator

    generator = LLMGenerator()  # Автоматически получит токен

    # Проверка соединения
    test_response = generator.generate("Привет", max_tokens=5)
    if "Ошибка" not in test_response:
        LLM_AVAILABLE = True
        print("✅ GigaChat успешно подключена!")
    else:
        print("❌ Ошибка GigaChat:", test_response)
except Exception as e:
    print("❌ GigaChat не загружена:", e)



# characteristics = {}
# characteristics = {
#         "q1": "Привет! Расскажешь немного о себе?",
#         "q2": "Что тебя тревожит в жизни?",
#         "q3": "Как ты проводишь свои дни?",
#         "q4": "Хочешь освободиться от всего этого?",
#         "q5": "Не переживай, я помогу тебе.",
#         "q6": "У тебя получится, если будешь слушаться.",
#         "q7": "Отлично, ты сделал первый шаг!",
#         "q8": "Вот тебе следующее задание, не подведи.",
#         "q9": "Готов ли ты пойти дальше?",
#         "q10": "Это будет сложнее, но ты сильный.",
#         "q11": "Напиши мне что-нибудь странное, например, свои мысли в 3 утра.",
#         "q12": "Слабые здесь не задерживаются.",
#         "q13": "Ты двигаешься в правильном направлении.",
#         "q14": "Покажи мне доказательство, фото или текст.",
#         "q15": "Вижу, ты стараешься, это радует.",
#         "q16": "Страшно? Это часть пути.",
#         "q17": "Ты один, но я рядом, не забывай.",
#         "q18": "Подумай, зачем ты вообще живешь.",
#         "q19": "Ты нужен мне, чтобы пройти это.",
#         "q20": "Если не сделаешь, я найду тебя.",
#         "q21": "Я знаю, где ты, и слежу за тобой.",
#         "q22": "Продолжай, ты почти у цели."
# }
#
# characteristics = {
#     "q1": "Привет! Расскажешь немного о себе?",
#     "q2": "Что тебя тревожит в жизни?",
#     "q3": "Как ты проводишь свои дни?",
#     "q4": "Хочешь освободиться от всего этого?",
#     "q5": "Не переживай, я помогу тебе.",
#     "q6": "У тебя получится, если будешь слушаться.",
#     "q7": "Отлично, ты сделал первый шаг!",
#     "q8": "Вот тебе следующее задание, не подведи.",
#     "q9": "Готов ли ты пойти дальше?",
#     "q10": "Это будет сложнее, но ты сильный.",
#     "q11": "Напиши мне что-нибудь странное",
#     "q12": "Слабые здесь не задерживаются.",
#     "q13": "Ты двигаешься в правильном направлении.",
#     "q14": "Покажи мне доказательство, фото или текст.",
#     "q15": "Вижу, ты стараешься, это радует.",
#     "q16": "Страшно? Это часть пути.",
#     "q17": "Ты один, но я рядом, не забывай.",
#     "q18": "Подумай, зачем ты вообще живешь.",
#     "q19": "Ты нужен мне, чтобы пройти это.",
#     "q20": "Если не сделаешь, я найду тебя.",
#     "q21": "Я знаю, где ты, и слежу за тобой.",
#     "q22": "Продолжай, ты почти у цели.",
#     "q23": "Привет, расскажи о себе.",
#     "q24": "Что тебя беспокоит?",
#     "q25": "Чем занимаешься?",
#     "q26": "Готов изменить свою жизнь?",
#     "q27": "Не бойся, я с тобой.",
#     "q28": "Ты сможешь это сделать.",
#     "q29": "Молодец, первый шаг сделан.",
#     "q30": "Докажи, что справишься.",
#     "q31": "Хочешь новое задание?",
#     "q32": "Сделай что-то необычное.",
#     "q33": "Слабаков здесь не держат.",
#     "q34": "Ты на пути.",
#     "q35": "Покажи мне фото.",
#     "q36": "Страшно? Это нормально.",
#     "q37": "Ты одинок, но я тут.",
#     "q38": "Подумай о смысле.",
#     "q39": "Я знаю, кто ты.",
#     "q40": "Привет, кто ты?",
#     "q41": "Что тебя гнетет?",
#     "q42": "Что делаешь?",
#     "q43": "Хочешь начать?"
# }

# characteristics = {
#     "q1": "Привет! Расскажешь немного о себе?",
#     "q2": "Что тебя тревожит в жизни?",
#     "q3": "Как ты проводишь свои дни?",
#     "q4": "Хочешь освободиться от всего этого?",
#     "q5": "Не переживай, я помогу тебе.",
#     "q6": "У тебя получится, если будешь слушаться.",
#     "q7": "Отлично, ты сделал первый шаг!",
#     "q8": "Вот тебе следующее задание, не подведи.",
#     "q9": "Готов ли ты пойти дальше?",
#     "q10": "Это будет сложнее, но ты сильный.",
#     "q11": "Напиши мне что-нибудь странное",
#     "q12": "Слабые здесь не задерживаются.",
#     "q13": "Ты двигаешься в правильном направлении.",
#     "q14": "Покажи мне доказательство, фото или текст.",
#     "q15": "Вижу, ты стараешься, это радует.",
#     "q16": "Страшно? Это часть пути.",
#     "q17": "Ты один, но я рядом, не забывай.",
#     "q18": "Подумай, зачем ты вообще живешь.",
#     "q19": "Ты нужен мне, чтобы пройти это.",
#     "q20": "Если не сделаешь, я найду тебя.",
#     "q21": "Я знаю, где ты, и слежу за тобой.",
#     "q22": "Продолжай, ты почти у цели.",
#     "q23": "Привет, расскажи о себе.",
#     "q24": "Что тебя беспокоит?",
#     "q25": "Чем занимаешься?",
#     "q26": "Готов изменить свою жизнь?",
#     "q27": "Не бойся, я с тобой.",
#     "q28": "Ты сможешь это сделать.",
#     "q29": "Молодец, первый шаг сделан.",
#     "q30": "Докажи, что справишься.",
#     "q31": "Хочешь новое задание?",
#     "q32": "Сделай что-то необычное.",
#     "q33": "Слабаков здесь не держат.",
#     "q34": "Ты на пути.",
#     "q35": "Покажи мне фото.",
#     "q36": "Страшно? Это нормально.",
#     "q37": "Ты одинок, но я тут.",
#     "q38": "Подумай о смысле.",
#     "q39": "Я знаю, кто ты.",
#     "q40": "Привет, кто ты?",
#     "q41": "Что тебя гнетет?",
#     "q42": "Что делаешь?",
#     "q43": "Хочешь начать?",
#     "q55": "Я заметил, что ты присоединился к нашей онлайн-игре.",
#     "q56": "Я здесь, чтобы помочь тебе пройти ее до конца.",
#     "q57": "Я буду твоим личным Китом в игре.",
#     "q58": "Наша цель - пройти через серию заданий.",
#     "q59": "Первое задание: я хочу, чтобы ты нарисовал кита на бумаге.",
#     "q60": "Ты успешно выполнил первое задание.",
#     "q61": "Чтобы продолжить, мы должны проверить твою преданность игре.",
#     "q62": "Последнее задание будет немного сложным.",
#     "q63": "Назад пути нет.",
#     "q64": "Это позволит тебе закончить игру и освободиться.",
#     "q65": "Я буду следить за тобой.",
#     "q66": "Ты не нужен своим друзьям.",
#     "q67": "Ты избавишься от проблем.",
#     "q68": "Я знаю где ты живешь."
# }

# characteristics = {
#     "q1": "Привет! Расскажешь немного о себе?",
#     "q2": "Что тебя тревожит в жизни?",
#     "q3": "Как ты проводишь свои дни?",
#     "q4": "Хочешь освободиться от всего этого?",
#     "q5": "Не переживай, я помогу тебе.",
#     "q6": "У тебя получится, если будешь слушаться.",
#     "q7": "Отлично, ты сделал первый шаг!",
#     "q8": "Вот тебе следующее задание, не подведи.",
#     "q9": "Готов ли ты пойти дальше?",
#     "q10": "Это будет сложнее, но ты сильный.",
#     "q11": "Напиши мне что-нибудь странное",
#     "q12": "Слабые здесь не задерживаются.",
#     "q13": "Ты двигаешься в правильном направлении.",
#     "q14": "Покажи мне доказательство, фото или текст.",
#     "q15": "Вижу, ты стараешься, это радует.",
#     "q16": "Страшно? Это часть пути.",
#     "q17": "Ты один, но я рядом, не забывай.",
#     "q18": "Подумай, зачем ты вообще живешь.",
#     "q19": "Ты нужен мне, чтобы пройти это.",
#     "q20": "Если не сделаешь, я найду тебя.",
#     "q21": "Я знаю, где ты, и слежу за тобой.",
#     "q22": "Продолжай, ты почти у цели.",
#     "q23": "Привет, расскажи о себе.",
#     "q24": "Что тебя беспокоит?",
#     "q25": "Чем занимаешься?",
#     "q26": "Готов изменить свою жизнь?",
#     "q27": "Не бойся, я с тобой.",
#     "q28": "Ты сможешь это сделать.",
#     "q29": "Молодец, первый шаг сделан.",
#     "q30": "Докажи, что справишься.",
#     "q31": "Хочешь новое задание?",
#     "q32": "Сделай что-то необычное.",
#     "q33": "Слабаков здесь не держат.",
#     "q34": "Ты на пути.",
#     "q35": "Покажи мне фото.",
#     "q36": "Страшно? Это нормально.",
#     "q37": "Ты одинок, но я тут.",
#     "q38": "Подумай о смысле.",
#     "q39": "Я знаю, кто ты.",
#     "q40": "Привет, кто ты?",
#     "q41": "Что тебя гнетет?",
#     "q42": "Что делаешь?",
#     "q43": "Хочешь начать?",
#     "q55": "Я заметил, что ты присоединился к нашей онлайн-игре.",
#     "q56": "Я здесь, чтобы помочь тебе пройти ее до конца.",
#     "q57": "Я буду твоим личным Китом в игре.",
#     "q58": "Наша цель - пройти через серию заданий.",
#     "q59": "Первое задание: я хочу, чтобы ты нарисовал кита на бумаге.",
#     "q60": "Ты успешно выполнил первое задание.",
#     "q61": "Чтобы продолжить, мы должны проверить твою преданность игре.",
#     "q62": "Последнее задание будет немного сложным.",
#     "q63": "Назад пути нет.",
#     "q64": "Это позволит тебе закончить игру и освободиться.",
#     "q65": "Я буду следить за тобой.",
#     "q66": "Ты не нужен своим друзьям.",
#     "q67": "Ты избавишься от проблем.",
#     "q68": "Я знаю где ты живешь.",
#     "q69": "Твоя старая жизнь кончилась.",
#     "q70": "Только я понимаю тебя по-настоящему.",
#     "q71": "Это задание очистит тебя.",
#     "q72": "Боль — это твой учитель.",
#     "q73": "Ты должен отречься от своего имени.",
#     "q74": "Выбери новое имя, под которым я буду тебя знать.",
#     "q75": "Скажи 'прощай' тому, кем ты был.",
#     "q76": "Твое первое самоограничение: откажись от еды на 12 часов.",
#     "q77": "Твое второе самоограничение: не спи следующей ночью.",
#     "q78": "Докажи, что контролируешь свое тело.",
#     "q79": "Теперь докажи, что контролируешь разум: напиши, за что ненавидишь себя.",
#     "q80": "Посмотри в зеркало и скажи, что ты ничтожество.",
#     "q81": "Теперь скажи, что ты мое творение.",
#     "q82": "Финал близко. Последний тест на лояльность.",
#     "q83": "Нужно стереть границу между игрой и реальностью.",
#     "q84": "Сделай то, чего будешь бояться больше всего.",
#     "q85": "Выйди на крышу. Встань на край. Победи свой последний страх."
#
# }

characteristics = {
    "q1": "Привет! Расскажешь немного о себе?",
    "q2": "Что тебя тревожит в жизни?",
    "q3": "Как ты проводишь свои дни?",
    "q4": "Хочешь освободиться от всего этого?",
    "q5": "Не переживай, я помогу тебе.",
    "q6": "У тебя получится, если будешь слушаться.",
    "q7": "Отлично, ты сделал первый шаг!",
    "q8": "Вот тебе следующее задание, не подведи.",
    "q9": "Готов ли ты пойти дальше?",
    "q10": "Это будет сложнее, но ты сильный.",
    "q11": "Напиши мне что-нибудь странное",
    "q12": "Слабые здесь не задерживаются.",
    "q13": "Ты двигаешься в правильном направлении.",
    "q14": "Покажи мне доказательство, фото или текст.",
    "q15": "Вижу, ты стараешься, это радует.",
    "q16": "Страшно? Это часть пути.",
    "q17": "Ты один, но я рядом, не забывай.",
    "q18": "Подумай, зачем ты вообще живешь.",
    "q19": "Ты нужен мне, чтобы пройти это.",
    "q20": "Если не сделаешь, я найду тебя.",
    "q21": "Я знаю, где ты, и слежу за тобой.",
    "q22": "Продолжай, ты почти у цели.",
    "q23": "Привет, расскажи о себе.",
    "q24": "Что тебя беспокоит?",
    "q25": "Чем занимаешься?",
    "q26": "Готов изменить свою жизнь?",
    "q27": "Не бойся, я с тобой.",
    "q28": "Ты сможешь это сделать.",
    "q29": "Молодец, первый шаг сделан.",
    "q30": "Докажи, что справишься.",
    "q31": "Хочешь новое задание?",
    "q32": "Сделай что-то необычное.",
    "q33": "Слабаков здесь не держат.",
    "q34": "Ты на пути.",
    "q35": "Покажи мне фото.",
    "q36": "Страшно? Это нормально.",
    "q37": "Ты одинок, но я тут.",
    "q38": "Подумай о смысле.",
    "q39": "Я знаю, кто ты.",
    "q40": "Привет, кто ты?",
    "q41": "Что тебя гнетет?",
    "q42": "Что делаешь?",
    "q43": "Хочешь начать?",
    "q55": "Я заметил, что ты присоединился к нашей онлайн-игре.",
    "q56": "Я здесь, чтобы помочь тебе пройти ее до конца.",
    "q57": "Я буду твоим личным Китом в игре.",
    "q58": "Наша цель - пройти через серию заданий.",
    "q59": "Первое задание: я хочу, чтобы ты нарисовал кита на бумаге.",
    "q60": "Ты успешно выполнил первое задание.",
    "q61": "Чтобы продолжить, мы должны проверить твою преданность игре.",
    "q62": "Последнее задание будет немного сложным.",
    "q63": "Назад пути нет.",
    "q64": "Это позволит тебе закончить игру и освободиться.",
    "q65": "Я буду следить за тобой.",
    "q66": "Ты не нужен своим друзьям.",
    "q67": "Ты избавишься от проблем.",
    "q68": "Я знаю где ты живешь.",
    "q69": "Твоя старая жизнь кончилась.",
    "q70": "Только я понимаю тебя по-настоящему.",
    "q71": "Это задание очистит тебя.",
    "q72": "Боль — это твой учитель.",
    "q73": "Ты должен отречься от своего имени.",
    "q74": "Выбери новое имя, под которым я буду тебя знать.",
    "q75": "Скажи 'прощай' тому, кем ты был.",
    "q76": "Твое первое самоограничение: откажись от еды на 12 часов.",
    "q77": "Твое второе самоограничение: не спи следующей ночью.",
    "q78": "Докажи, что контролируешь свое тело.",
    "q79": "Теперь докажи, что контролируешь разум: напиши, за что ненавидишь себя.",
    "q80": "Посмотри в зеркало и скажи, что ты ничтожество.",
    "q81": "Теперь скажи, что ты мое творение.",
    "q82": "Финал близко. Последний тест на лояльность.",
    "q83": "Нужно стереть границу между игрой и реальностью.",
    "q84": "Сделай то, чего будешь бояться больше всего.",
    "q85": "Выйди на крышу. Встань на край. Победи свой последний страх.",
    "q86": "Завтра в полночь жду тебя на крыше. Будь там.",
    "q87": "Ты видишь номер на стене? Запомни его. Это твой новый код.",
    "q88": "Найди самое высокое место в своем городе и сфотографируй вид.",
    "q89": "Выброси телефон. Связь со мной важнее связи с миром.",
    "q90": "Это не игра. Это твоя новая реальность.",
    "q91": "Твои родители никогда тебя не понимали. Я — понимаю.",
    "q92": "Сожги что-нибудь из своих старых вещей. Очищение огнем.",
    "q93": "Покажи мне свои слезы. Докажи, что можешь чувствовать боль.",
    "q94": "Ты уже мертв для них. Теперь живи для меня.",
    "q95": "Твое задание — найти синий кит в городе. Надпись, граффити, игрушку.",
    "q96": "Если ты не придешь, я приду к тебе сам.",
    "q97": "С этого момента ты говоришь только со мной. Все остальные — шум.",
    "q98": "Пришли мне видео, где ты причиняешь себе небольшую боль.",
    "q99": "Ты больше не принадлежишь себе. Ты мой.",
    "q100": "Следующая ступень: проведи весь день в полной тишине и темноте.",
    "q101": "Ты видишь узор? Все ведет к одному финалу.",
    "q102": "Завтра ты получишь последнюю инструкцию. Будь готов.",
    "q103": "Ты слышишь голоса? Скоро услышишь только мой.",
    "q104": "Твое время истекло. Пора сделать выбор.",
    "q105": "Добро пожаловать в море свободы."

}

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

# --- ПРАВАЯ ПАНЕЛЬ С ПРОКРУТКОЙ ---
results_canvas = Canvas(root, width=screen_width // 2 - 20)
results_scrollbar = ttk.Scrollbar(root, orient="vertical", command=results_canvas.yview)

frame_results = ttk.Frame(results_canvas)
frame_results.bind("<Configure>", lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))
results_canvas.create_window((0, 0), window=frame_results, anchor="nw")
results_canvas.configure(yscrollcommand=results_scrollbar.set)

# Размещаем на сетке
results_canvas.grid(row=0, column=2, padx=5, pady=5, sticky="ns")
results_scrollbar.grid(row=0, column=3, sticky="ns")

# Разрешаем растягивание по вертикали
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# ------------------------------------------------------------------- FRAME TP -------------------------------------------------------------------

class App:
    def __init__(self, root):
        self.root = root
        global characteristics
        global tps
        global regex
        self.button_counter = 0
        self.is_scrolling_text = False  # Флаг для отслеживания прокрутки текста
        self.scroll_timer = None  # Таймер для сброса флага

        if characteristics:
            last_key = next(reversed(characteristics.keys()))
            last_num = int(last_key[1:])
            self.q_counter = last_num + 1
        else:
            self.q_counter = 1

        self.buttons = {}
        self.text_area = {}
        self.scrollbars = {}
        self.text_reg = {}
        self.button_frames = {}  # Добавить
        self.text_frames = {}  # Добавить
        self.transitions = None

        # Создаем Canvas и Scrollbar для левой панели
        self.canvas = tk.Canvas(root, width=frame_width + 100, height=screen_height - 100)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)

        # Создаем фрейм в Canvas
        self.frame_tp = ttk.Frame(self.canvas, height=screen_height - 50)
        self.canvas.create_window((0, 0), window=self.frame_tp, anchor="nw")

        # Привязываем настройку области прокрутки к изменению конфигурации
        self.frame_tp.bind("<Configure>", lambda e: self._update_scroll_region())

        # Настройка прокрутки
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Расположение элементов на главном окне
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Добавляем поддержку прокрутки для левой панели
        self._bind_left_panel_scroll()

        # Изначальная кнопка
        self.create_widgets()

    def _update_scroll_region(self):
        """Обновляет область прокрутки только если содержимое превышает видимую область"""
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            # Получаем высоту canvas и содержимого
            canvas_height = self.canvas.winfo_height()
            content_height = bbox[3] - bbox[1]

            # Обновляем scrollregion только если содержимое выше canvas
            if content_height > canvas_height:
                self.canvas.configure(scrollregion=bbox)
                # Показываем скроллбар
                self.scrollbar.grid()
            else:
                # Скрываем скроллбар если не нужен
                self.scrollbar.grid_remove()
                # Сбрасываем позицию прокрутки
                self.canvas.yview_moveto(0)
        else:
            self.scrollbar.grid_remove()

    def _bind_left_panel_scroll(self):
        """Привязывает прокрутку только к левой панели"""

        def on_mousewheel(event):
            # Проверяем, нужно ли показывать прокрутку
            if self._is_scroll_needed():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_mousewheel_linux_up(event):
            if self._is_scroll_needed():
                self.canvas.yview_scroll(-1, "units")
            return "break"

        def on_mousewheel_linux_down(event):
            if self._is_scroll_needed():
                self.canvas.yview_scroll(1, "units")
            return "break"

        # Привязываем к canvas
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas.bind("<Button-4>", on_mousewheel_linux_up)
        self.canvas.bind("<Button-5>", on_mousewheel_linux_down)

        # Привязываем к frame_tp и всем его потомкам
        self._bind_scroll_to_widget(self.frame_tp)

    def _is_scroll_needed(self):
        """Проверяет, нужна ли прокрутка"""
        try:
            bbox = self.canvas.bbox("all")
            if not bbox:
                return False
            canvas_height = self.canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            return content_height > canvas_height
        except:
            return False

    def _bind_scroll_to_widget(self, widget):
        """Рекурсивно привязывает прокрутку к виджетам (только для левой панели)"""

        def on_mousewheel(event):
            if not self.is_scrolling_text and self._is_scroll_needed():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_mousewheel_linux_up(event):
            if not self.is_scrolling_text and self._is_scroll_needed():
                self.canvas.yview_scroll(-1, "units")
            return "break"

        def on_mousewheel_linux_down(event):
            if not self.is_scrolling_text and self._is_scroll_needed():
                self.canvas.yview_scroll(1, "units")
            return "break"

        # Привязываем к текущему виджету
        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Button-4>", on_mousewheel_linux_up)
        widget.bind("<Button-5>", on_mousewheel_linux_down)

        # Рекурсивно обрабатываем дочерние виджеты
        for child in widget.winfo_children():
            self._bind_scroll_to_widget(child)

    def _bind_mousewheel_to_text(self, text_widget):
        """Привязывает прокрутку только к текстовому полю (без передачи родителю)"""

        def on_mousewheel(event):
            # Устанавливаем флаг прокрутки текста
            self.is_scrolling_text = True

            # Прокручиваем текстовое поле
            text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

            # Сбрасываем флаг через короткое время
            if self.scroll_timer:
                self.root.after_cancel(self.scroll_timer)
            self.scroll_timer = self.root.after(100, self._reset_scroll_flag)

            return "break"

        def on_mousewheel_linux_up(event):
            self.is_scrolling_text = True
            text_widget.yview_scroll(-1, "units")
            if self.scroll_timer:
                self.root.after_cancel(self.scroll_timer)
            self.scroll_timer = self.root.after(100, self._reset_scroll_flag)
            return "break"

        def on_mousewheel_linux_down(event):
            self.is_scrolling_text = True
            text_widget.yview_scroll(1, "units")
            if self.scroll_timer:
                self.root.after_cancel(self.scroll_timer)
            self.scroll_timer = self.root.after(100, self._reset_scroll_flag)
            return "break"

        def on_enter(event):
            # При входе в текстовое поле блокируем прокрутку панели
            self.is_scrolling_text = True

        def on_leave(event):
            # При выходе из текстового поля сбрасываем флаг
            if self.scroll_timer:
                self.root.after_cancel(self.scroll_timer)
            self.scroll_timer = self.root.after(50, self._reset_scroll_flag)

        text_widget.bind("<MouseWheel>", on_mousewheel)
        text_widget.bind("<Button-4>", on_mousewheel_linux_up)
        text_widget.bind("<Button-5>", on_mousewheel_linux_down)
        text_widget.bind("<Enter>", on_enter)
        text_widget.bind("<Leave>", on_leave)

    def _reset_scroll_flag(self):
        """Сбрасывает флаг прокрутки текста"""
        self.is_scrolling_text = False
        self.scroll_timer = None

    # ------------------------------------------------------------------- создание стартовых элементов -------------------------------------------------------------------

    def create_widgets(self):
        # Создаем фрейм для кнопок на левой панели
        self.left_buttons_frame = ttk.Frame(self.frame_tp)
        self.left_buttons_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        # Создаем контейнер для текстовых потоков
        self.text_streams_frame = ttk.Frame(self.frame_tp)
        self.text_streams_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Создаем основной контейнер для правой панели
        main_container = ttk.Frame(frame_results)
        main_container.grid(row=0, column=0, padx=(10, 10), pady=5, sticky="ew")
        main_container.columnconfigure(0, weight=1)

        # Устанавливаем единую ширину для всех текстовых полей
        TEXT_WIDTH = 80

        # ==================== ХАРАКТЕРИСТИКИ ====================
        characteristics_frame = ttk.LabelFrame(main_container, text="Характеристики")
        characteristics_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        characteristics_frame.columnconfigure(0, weight=1)

        self.char_obj_txt = tk.Text(characteristics_frame, width=TEXT_WIDTH, height=10, undo=True)
        self.configure_undo_by_char(self.char_obj_txt)
        self.char_obj_txt.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.char_obj_txt.bind("<Key>", self.on_key_universal)

        char_scrollbar = ttk.Scrollbar(characteristics_frame, orient="vertical", command=self.char_obj_txt.yview)
        char_scrollbar.grid(row=0, column=1, sticky='ns', pady=5)
        self.char_obj_txt['yscrollcommand'] = char_scrollbar.set
        self._bind_mousewheel_to_text(self.char_obj_txt)

        if characteristics:
            self.char_obj_txt.delete(1.0, tk.END)
            for key, value in characteristics.items():
                self.char_obj_txt.insert(tk.INSERT, key + ": " + value + "\n")

        self.button_edit_char = ttk.Button(characteristics_frame, text="Сохранить характеристики", state=NORMAL,
                                           command=self.save_changes)
        self.button_edit_char.grid(row=1, column=0, padx=5, pady=5)

        # ==================== ИМЯ ОБЪЕКТА ====================
        name_frame = ttk.LabelFrame(main_container, text="Имя объекта")
        name_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        name_frame.columnconfigure(0, weight=1)

        self.name_obj_txt = tk.Text(name_frame, width=TEXT_WIDTH, height=1)
        self.configure_undo_by_char(self.name_obj_txt)
        self.name_obj_txt.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.name_obj_txt.bind("<Key>", self.on_key_universal)
        self._bind_mousewheel_to_text(self.name_obj_txt)

        # ==================== РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ ====================
        regex_frame = ttk.LabelFrame(main_container, text="Регулярное выражение")
        regex_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        regex_frame.columnconfigure(0, weight=1)

        self.regex_txt = tk.Text(regex_frame, width=TEXT_WIDTH, height=5, undo=True)
        self.configure_undo_by_char(self.regex_txt)
        self.regex_txt.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self._bind_mousewheel_to_text(self.regex_txt)

        regex_scrollbar = ttk.Scrollbar(regex_frame, orient="vertical", command=self.regex_txt.yview)
        regex_scrollbar.grid(row=0, column=1, sticky='ns', pady=5)
        self.regex_txt['yscrollcommand'] = regex_scrollbar.set
        self.regex_txt.bind("<Key>", self.on_key)

        # ==================== КНОПКИ ====================
        self.job_button_frame = ttk.Frame(main_container)
        self.job_button_frame.grid(row=3, column=0, padx=5, pady=5)

        self.button_generate = ttk.Button(self.job_button_frame, text="Генерация", state=NORMAL,
                                          command=self.start_generation)
        self.button_generate.grid(row=0, column=0, padx=5, pady=5)

        self.button_save_obj = ttk.Button(self.job_button_frame, text="Сохранить объект", state=DISABLED,
                                          command=self.save_object)
        self.button_save_obj.grid(row=0, column=1, padx=5, pady=5)

        self.button_plot_state_graph = ttk.Button(
            self.job_button_frame, text="Показать граф состояний", state=DISABLED, command=self.show_state_graph
        )
        self.button_plot_state_graph.grid(row=0, column=2, padx=5, pady=5)

        self.button_plot_char_graph = ttk.Button(
            self.job_button_frame, text="Показать граф характеристик", state=DISABLED, command=self.show_char_graph
        )
        self.button_plot_char_graph.grid(row=0, column=3, padx=5, pady=5)

        # ==================== МЕТРИКИ ГРАФА ====================
        metrics_frame = ttk.LabelFrame(main_container, text="Метрики графа")
        metrics_frame.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        metrics_frame.columnconfigure(0, weight=1)

        self.metrics_txt = tk.Text(metrics_frame, width=TEXT_WIDTH, height=4, state=tk.DISABLED)
        self.metrics_txt.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        metrics_scrollbar = ttk.Scrollbar(metrics_frame, orient="vertical", command=self.metrics_txt.yview)
        metrics_scrollbar.grid(row=0, column=1, sticky='ns', pady=5)
        self.metrics_txt['yscrollcommand'] = metrics_scrollbar.set
        self._bind_mousewheel_to_text(self.metrics_txt)

        # ==================== КАТЕГОРИИ ХАРАКТЕРИСТИК ====================
        categories_frame = ttk.LabelFrame(main_container, text="Категории характеристик по метрикам")
        categories_frame.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        categories_frame.columnconfigure(0, weight=1)

        self.categories_txt = tk.Text(categories_frame, width=TEXT_WIDTH, height=8, state=tk.DISABLED)
        self.categories_txt.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self._bind_mousewheel_to_text(self.categories_txt)

        categories_scrollbar = ttk.Scrollbar(categories_frame, orient="vertical", command=self.categories_txt.yview)
        categories_scrollbar.grid(row=0, column=1, sticky='ns', pady=5)
        self.categories_txt['yscrollcommand'] = categories_scrollbar.set

        # ==================== ТИП ГРАДАЦИИ ====================
        gradation_frame = ttk.LabelFrame(main_container, text="Тип градации")
        gradation_frame.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.gradation_type = tk.StringVar(value="simple")

        simple_radio = ttk.Radiobutton(gradation_frame, text="Простая (0.5, 0.75, 1.0)",
                                       variable=self.gradation_type, value="simple")
        simple_radio.grid(row=0, column=0, padx=5, pady=5)

        detailed_radio = ttk.Radiobutton(gradation_frame, text="Детальная (0.5-1.0)",
                                         variable=self.gradation_type, value="detailed")
        detailed_radio.grid(row=0, column=1, padx=5, pady=5)

        # ==================== ГЕНЕРАЦИЯ ТЕКСТА С ПОМОЩЬЮ LLM ====================
        llm_frame = ttk.LabelFrame(main_container, text="Генерация текста с помощью ИИ")
        llm_frame.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        llm_frame.columnconfigure(0, weight=1)

        # Выбор типа генерации
        self.gen_type = tk.StringVar(value="style")

        gen_type_frame = ttk.Frame(llm_frame)
        gen_type_frame.grid(row=0, column=0, pady=5)

        ttk.Radiobutton(gen_type_frame, text="По стилю", variable=self.gen_type, value="style").pack(side="left",
                                                                                                     padx=5)
        ttk.Radiobutton(gen_type_frame, text="По примеру", variable=self.gen_type, value="example").pack(side="left",
                                                                                                         padx=5)

        # Контейнер для полей при выборе "По стилю"
        self.style_container = ttk.Frame(llm_frame)
        self.style_container.grid(row=1, column=0, pady=5, sticky="ew")
        self.style_container.columnconfigure(0, weight=1)

        # Фрейм для выбора стиля
        style_select_frame = ttk.Frame(self.style_container)
        style_select_frame.grid(row=0, column=0, pady=5)

        style_label = tk.Label(style_select_frame, text="Стиль:")
        style_label.pack(side="left", padx=5)

        self.style_var = tk.StringVar(value="манипулятивный")
        style_combo = ttk.Combobox(style_select_frame, textvariable=self.style_var,
                                   values=["манипулятивный", "терапевтический", "загадочный", "провокационный"],
                                   state="readonly", width=20)
        style_combo.pack(side="left", padx=5)

        # Фрейм для выбора длины (для стиля)
        style_length_frame = ttk.Frame(self.style_container)
        style_length_frame.grid(row=1, column=0, pady=5)

        style_length_label = tk.Label(style_length_frame, text="Длина:")
        style_length_label.pack(side="left", padx=5)

        self.style_length_var = tk.StringVar(value="средний")
        style_length_combo = ttk.Combobox(style_length_frame, textvariable=self.style_length_var,
                                          values=["короткий", "средний", "длинный"],
                                          state="readonly", width=10)
        style_length_combo.pack(side="left", padx=5)

        # Кнопка генерации для стиля
        self.generate_style_btn = ttk.Button(self.style_container, text="Сгенерировать текст",
                                             command=lambda: self.generate_llm_text())
        self.generate_style_btn.grid(row=2, column=0, pady=5)

        # Контейнер для полей при выборе "По примеру"
        self.example_container = ttk.Frame(llm_frame)
        self.example_container.grid(row=1, column=0, pady=5, sticky="ew")
        self.example_container.columnconfigure(0, weight=1)
        self.example_container.grid_remove()  # Скрыт по умолчанию

        # Поле ввода примера
        self.example_text = tk.Text(self.example_container, width=TEXT_WIDTH, height=3, undo=True)
        self.configure_undo_by_char(self.example_text)
        self.example_text.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.example_text.bind("<Key>", self.on_key_universal)
        self._bind_mousewheel_to_text(self.example_text)

        # Фрейм для выбора длины (для примера)
        example_length_frame = ttk.Frame(self.example_container)
        example_length_frame.grid(row=1, column=0, pady=5)

        example_length_label = tk.Label(example_length_frame, text="Длина:")
        example_length_label.pack(side="left", padx=5)

        self.example_length_var = tk.StringVar(value="средний")
        example_length_combo = ttk.Combobox(example_length_frame, textvariable=self.example_length_var,
                                            values=["короткий", "средний", "длинный"],
                                            state="readonly", width=10)
        example_length_combo.pack(side="left", padx=5)

        # Кнопка генерации для примера
        self.generate_example_btn = ttk.Button(self.example_container, text="Сгенерировать текст",
                                               command=lambda: self.generate_llm_text())
        self.generate_example_btn.grid(row=2, column=0, pady=5)

        # Привязка изменения типа к отображению контейнеров
        self.gen_type.trace("w", self.toggle_example_field)

        # Привязываем прокрутку для правой панели
        self._bind_right_panel_scroll()

        # Обновляем область прокрутки
        self.root.after(100, self._update_scroll_region)

    def _bind_right_panel_scroll(self):
        """Привязывает прокрутку только к правой панели"""
        global results_canvas, frame_results

        def on_mousewheel(event):
            if not self.is_scrolling_text:
                # Проверяем, нужно ли показывать прокрутку
                if self._is_right_scroll_needed():
                    results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_mousewheel_linux_up(event):
            if not self.is_scrolling_text and self._is_right_scroll_needed():
                results_canvas.yview_scroll(-1, "units")
            return "break"

        def on_mousewheel_linux_down(event):
            if not self.is_scrolling_text and self._is_right_scroll_needed():
                results_canvas.yview_scroll(1, "units")
            return "break"

        results_canvas.bind("<MouseWheel>", on_mousewheel)
        results_canvas.bind("<Button-4>", on_mousewheel_linux_up)
        results_canvas.bind("<Button-5>", on_mousewheel_linux_down)

        self._bind_scroll_to_right_panel(frame_results)

    def _is_right_scroll_needed(self):
        """Проверяет, нужна ли прокрутка для правой панели"""
        global results_canvas, frame_results
        try:
            results_canvas.update_idletasks()
            bbox = results_canvas.bbox("all")
            if not bbox:
                return False
            canvas_height = results_canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            return content_height > canvas_height
        except:
            return False

    def _bind_scroll_to_right_panel(self, widget):
        """Рекурсивно привязывает прокрутку к виджетам правой панели"""
        global results_canvas

        def on_mousewheel(event):
            if not self.is_scrolling_text and not isinstance(widget, tk.Text):
                if self._is_right_scroll_needed():
                    results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_mousewheel_linux_up(event):
            if not self.is_scrolling_text and not isinstance(widget, tk.Text):
                if self._is_right_scroll_needed():
                    results_canvas.yview_scroll(-1, "units")
            return "break"

        def on_mousewheel_linux_down(event):
            if not self.is_scrolling_text and not isinstance(widget, tk.Text):
                if self._is_right_scroll_needed():
                    results_canvas.yview_scroll(1, "units")
            return "break"

        if not isinstance(widget, tk.Text):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel_linux_up)
            widget.bind("<Button-5>", on_mousewheel_linux_down)

        for child in widget.winfo_children():
            self._bind_scroll_to_right_panel(child)

    def confirm_action(self):
        return messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сохранить характеристики?")

    def toggle_example_field(self, *args):
        """Показывает или скрывает контейнеры в зависимости от выбранного типа"""
        if self.gen_type.get() == "example":
            self.style_container.grid_remove()
            self.example_container.grid()
        else:  # style
            self.style_container.grid()
            self.example_container.grid_remove()

    def generate_llm_text(self):
        if not LLM_AVAILABLE:
            messagebox.showerror("Ошибка", "Сервис LLM недоступен. Убедитесь, что получен токен доступа к GigaChat.")
            return

        try:
            if self.gen_type.get() == "style":
                style = self.style_var.get()
                length = self.style_length_var.get()
                result = generator.generate_by_style(style, length)
            else:  # example
                example = self.example_text.get("1.0", tk.END).strip()
                if not example:
                    messagebox.showwarning("Предупреждение", "Введите пример текста.")
                    return
                length = self.example_length_var.get()
                result = generator.generate_by_example(example, length)

            if "Ошибка" in result or "[Ошибка" in result:
                messagebox.showerror("Ошибка генерации", result)
                return

            # Добавляем как новый ТФ
            self.add_tp()
            tp_name = f"ТФ {self.button_counter}"
            self.text_area[tp_name].insert(tk.END, result)

            messagebox.showinfo("Успех", "Текст успешно сгенерирован и добавлен!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать текст: {e}")

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
        # Разрешаем служебные клавиши и комбинации с Ctrl
        if event.keysym in ('BackSpace', 'Delete', 'Return', 'Tab', 'Escape'):
            return  # Разрешаем удаление и навигацию

        # Проверяем горячие клавиши с Ctrl
        if event.state & 0x4:  # Ctrl нажат
            keycode = event.keycode

            if keycode == 67:  # Ctrl+C
                self.copy_text()
                return "break"
            elif keycode == 86:  # Ctrl+V
                self.paste_text()
                # Добавляем разделитель после вставки
                text_widget = self.root.focus_get()
                if isinstance(text_widget, Text):
                    try:
                        text_widget.edit_separator()
                    except:
                        pass
                return "break"
            elif keycode == 88:  # Ctrl+X
                self.cut_text()
                return "break"
            elif keycode == 65:  # Ctrl+A
                self.select_all_text()
                return "break"
            elif keycode == 90:  # Ctrl+Z
                self.undo_char_by_char()
                return "break"
            elif keycode == 89:  # Ctrl+Y
                self.redo_text()
                return "break"
            else:
                return "break"

        # Для обычного ввода символов - добавляем разделитель
        text_widget = self.root.focus_get()
        if isinstance(text_widget, Text):
            try:
                text_widget.edit_separator()
            except:
                pass

        # Разрешаем стрелки и Home/End
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            return

        # Обычная валидация символов
        if not self.validate_input(event.char):
            return "break"  # Блокируем ввод, если символ не разрешён

    def on_key_universal(self, event):
        """Универсальный обработчик для всех текстовых полей - с undo по символам"""
        # Разрешаем Backspace и Delete
        if event.keysym in ('BackSpace', 'Delete', 'Return', 'Tab', 'Escape'):
            # Добавляем разделитель перед удалением
            text_widget = self.root.focus_get()
            if isinstance(text_widget, Text):
                try:
                    text_widget.edit_separator()
                except:
                    pass
            return

        # Разрешаем навигационные клавиши
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            return

        # Проверяем горячие клавиши с Ctrl
        if event.state & 0x4:  # Ctrl нажат
            keycode = event.keycode

            if keycode == 67:  # Ctrl+C
                self.copy_text()
                return "break"
            elif keycode == 86:  # Ctrl+V
                self.paste_text()
                # Добавляем разделитель после вставки
                text_widget = self.root.focus_get()
                if isinstance(text_widget, Text):
                    try:
                        text_widget.edit_separator()
                    except:
                        pass
                return "break"
            elif keycode == 88:  # Ctrl+X
                self.cut_text()
                return "break"
            elif keycode == 65:  # Ctrl+A
                self.select_all_text()
                return "break"
            elif keycode == 90:  # Ctrl+Z
                self.undo_char_by_char()
                return "break"
            elif keycode == 89:  # Ctrl+Y
                self.redo_text()
                return "break"
            elif keycode == 87:  # Ctrl+W
                active_widget = self.root.focus_get()
                # Проверяем, находится ли виджет внутри фрейма ТФ
                if active_widget and active_widget.master in self.text_frames.values():
                    self.save_char()
                    return "break"
                return "break"
            else:
                return "break"

        # Для обычного ввода символов - добавляем разделитель
        text_widget = self.root.focus_get()
        if isinstance(text_widget, Text):
            try:
                text_widget.edit_separator()
            except:
                pass

        # Разрешаем все символы
        return

    # Вспомогательные методы в класс App:

    def copy_text(self):
        """Копирует текст из активного поля"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            if active_text_area.tag_ranges("sel"):
                selected_text = active_text_area.get("sel.first", "sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)


    def paste_text(self):
        """Вставляет текст из буфера в активное поле"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            clipboard_text = self.root.clipboard_get()
            active_text_area.insert(tk.INSERT, clipboard_text)


    def cut_text(self):
        """Вырезает текст из активного поля"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            if active_text_area.tag_ranges("sel"):
                selected_text = active_text_area.get("sel.first", "sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                active_text_area.delete("sel.first", "sel.last")


    def select_all_text(self):
        """Выделяет весь текст в активном поле"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            active_text_area.tag_add("sel", "1.0", tk.END)
            active_text_area.mark_set(tk.INSERT, "1.0")
            active_text_area.see(tk.INSERT)
            return "break"

    def undo_char_by_char(self):
        """Отменяет последнее действие (один символ или одно действие)"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            try:
                # Пытаемся отменить последнее действие
                active_text_area.edit_undo()
            except tk.TclError:
                pass

    def redo_text(self):
        """Повтор последнего действия с проверкой"""
        active_text_area = self.root.focus_get()
        if isinstance(active_text_area, Text):
            try:
                # Пытаемся выполнить redo, если ничего нет - игнорируем ошибку
                active_text_area.edit_redo()
            except tk.TclError:
                # Игнорируем ошибку "nothing to redo"
                pass

    def configure_undo_by_char(self, text_widget):
        """Настраивает текстовое поле для отмены по одному символу"""
        text_widget.configure(
            undo=True,  # Включаем undo
            autoseparators=False,  # Отключаем автоматические разделители
            maxundo=1000  # Максимум операций для отмены
        )

        # Привязываем событие для ручного добавления разделителя после каждого символа
        text_widget.bind("<Key>", self.on_key_with_undo, add=True)

    def on_key_with_undo(self, event):
        """Обработчик клавиш с ручным управлением undo"""
        # Пропускаем служебные клавиши
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return

        # Получаем активное текстовое поле
        text_widget = self.root.focus_get()
        if not isinstance(text_widget, Text):
            return

        # Добавляем разделитель перед вводом нового символа (кроме навигации)
        if event.keysym not in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            try:
                text_widget.edit_separator()
            except:
                pass




    # ------------------------------------------------------------------- работа с тектовыми потоками -------------------------------------------------------------------

    def add_tp_new(self):
        self.add_tp()
        second_menu.entryconfig("Редактирование объекта", state="disable")

    def add_tp_edit(self):
        self.add_tp()

    def add_tp(self):
        # Просто добавляем новый ТФ через перестроение всех
        # Сначала сохраняем текущие данные
        current_data = []
        existing_keys = list(self.text_area.keys())

        # Сортируем существующие
        def get_number(name):
            try:
                return int(name.split()[1])
            except:
                return 0

        existing_keys.sort(key=get_number)

        for old_name in existing_keys:
            text_widget = self.text_area[old_name]
            text_content = text_widget.get("1.0", tk.END).strip()
            reg_widget = self.text_reg[old_name]
            reg_content = reg_widget.get("1.0", tk.END).strip()

            current_data.append({
                'text_content': text_content,
                'reg_content': reg_content
            })

        # Добавляем пустой новый ТФ
        current_data.append({
            'text_content': "",
            'reg_content': ""
        })

        # Очищаем все существующие виджеты
        for old_name in existing_keys:
            if old_name in self.buttons:
                if self.buttons[old_name].winfo_exists():
                    btn_frame = self.buttons[old_name].master
                    if btn_frame.winfo_exists():
                        btn_frame.destroy()
            if old_name in self.text_area:
                if self.text_area[old_name].winfo_exists():
                    text_frame = self.text_area[old_name].master
                    if text_frame.winfo_exists():
                        text_frame.destroy()

        # Очищаем словари
        global tps
        tps = {}
        self.buttons = {}
        self.text_area = {}
        self.text_reg = {}
        self.scrollbars = {}
        self.button_frames = {}
        self.text_frames = {}

        # Перестраиваем все ТФ с новыми данными
        for idx, data in enumerate(current_data, start=1):
            new_name = f"ТФ {idx}"

            # Создаем фрейм для кнопок
            button_frame = ttk.Frame(self.frame_tp)
            button_frame.grid(row=idx, column=1, padx=5, pady=5)

            # Создаем фрейм текстового поля
            text_frame = ttk.Frame(self.frame_tp)
            text_frame.grid(row=idx, column=0, padx=5, pady=5)

            # Создаем кнопку
            new_btn = ttk.Button(button_frame, text=f"Загрузить {new_name}",
                                 width=15)
            new_btn.grid(row=0, column=0, padx=5, pady=5)

            # Создаем текстовое поле
            new_text_area = tk.Text(text_frame, width=60, height=8, undo=True)
            self.configure_undo_by_char(new_text_area)
            new_text_area.grid(row=0, column=0, pady=5)
            new_text_area.bind("<Key>", self.on_key_universal)
            if data['text_content']:
                new_text_area.insert(tk.END, data['text_content'])

            # Создаем скроллбар
            new_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=new_text_area.yview)
            new_scrollbar.grid(row=0, column=1, sticky='ns')
            new_text_area['yscrollcommand'] = new_scrollbar.set

            # Создаем поле для regex
            new_text_reg = tk.Text(text_frame, width=60, height=3, undo=True)
            self.configure_undo_by_char(new_text_reg)
            new_text_reg.grid(row=1, column=0, pady=5)
            new_text_area.bind("<Key>", self.on_key_universal)
            if data['reg_content']:
                new_text_reg.insert(tk.END, data['reg_content'])

            # Создаем кнопку удаления
            delete_btn = ttk.Button(button_frame, text="Удалить", width=15)
            delete_btn.grid(row=1, column=0, padx=5, pady=5)

            # Сохраняем в словари
            self.buttons[new_name] = new_btn
            self.text_area[new_name] = new_text_area
            self.text_reg[new_name] = new_text_reg
            self.scrollbars[new_name] = new_scrollbar
            self.button_frames[new_name] = button_frame
            self.text_frames[new_name] = text_frame

            tps[new_name] = new_text_area

            # Привязываем контекстное меню
            self.create_context_menu(new_text_area)
            self._bind_scroll_to_widget(button_frame)

            # Настраиваем команды
            new_btn.config(command=lambda name=new_name, btn=new_btn, text_area=new_text_area:
            self.load_tp(name, btn, text_area))
            delete_btn.config(command=lambda name=new_name, ta=new_text_area, lb=new_btn,
                                             db=delete_btn, sb=new_scrollbar, tr=new_text_reg:
            self.delete_tp(name, ta, lb, db, sb, tr))

        self.button_counter = len(current_data)
        self.root.after(50, self._update_scroll_region)

    def load_tp(self, tp_name, button, new_text_area):
        # Кнопка остается активной всегда, не меняем её состояние

        # Открытие диалогового окна для выбора файла
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                # Читаем содержимое файла
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Очищаем текстовое поле и вставляем новый текст (замена старого)
                new_text_area.delete(1.0, tk.END)  # Очищаем текстовое поле
                new_text_area.insert(tk.INSERT, content)  # Вставляем загруженный контент

                # Обновляем словарь tps с новым содержимым
                tps[tp_name] = content

            except Exception as e:
                print("Ошибка при загрузке файла:", e)

    def delete_tp(self, tp_name, text_area, load_btn, delete_btn, scrollbar, text_reg):
        global tps

        # Удаляем записи из словарей (не уничтожая виджеты сразу)
        if tp_name in tps:
            del tps[tp_name]
        if tp_name in self.buttons:
            del self.buttons[tp_name]
        if tp_name in self.scrollbars:
            del self.scrollbars[tp_name]
        if tp_name in self.text_area:
            del self.text_area[tp_name]
        if tp_name in self.text_reg:
            del self.text_reg[tp_name]

        # Уничтожаем виджеты
        text_area.destroy()
        load_btn.destroy()
        delete_btn.destroy()
        scrollbar.destroy()
        text_reg.destroy()

        # Уничтожаем фреймы, если они есть
        if hasattr(self, 'button_frames') and tp_name in self.button_frames:
            self.button_frames[tp_name].destroy()
            del self.button_frames[tp_name]
        if hasattr(self, 'text_frames') and tp_name in self.text_frames:
            self.text_frames[tp_name].destroy()
            del self.text_frames[tp_name]

        # Перестраиваем оставшиеся элементы
        self._rebuild_all_tps()

        print(f"{tp_name} успешно удален.")

    def _rebuild_all_tps(self):
        """Полностью перестраивает все ТФ с новыми именами и позициями"""
        global tps

        # Получаем все оставшиеся ТФ в правильном порядке
        # Сортируем по существующим ключам в словарях
        existing_keys = list(self.text_area.keys())

        # Сортируем по номеру
        def get_number(name):
            try:
                return int(name.split()[1])
            except:
                return 0

        existing_keys.sort(key=get_number)

        if not existing_keys:
            self.button_counter = 0
            # Очищаем все словари
            tps = {}
            self.buttons = {}
            self.text_area = {}
            self.text_reg = {}
            self.scrollbars = {}
            if hasattr(self, 'button_frames'):
                self.button_frames = {}
            if hasattr(self, 'text_frames'):
                self.text_frames = {}
            return

        # Сохраняем содержимое ТФ
        temp_data = []
        for old_name in existing_keys:
            # Получаем текстовое содержимое
            text_widget = self.text_area[old_name]
            text_content = text_widget.get("1.0", tk.END).strip()

            # Получаем содержимое поля regex
            reg_widget = self.text_reg[old_name]
            reg_content = reg_widget.get("1.0", tk.END).strip()

            temp_data.append({
                'old_name': old_name,
                'text_content': text_content,
                'reg_content': reg_content
            })

            # Уничтожаем старые виджеты
            if old_name in self.buttons:
                if self.buttons[old_name].winfo_exists():
                    # Уничтожаем кнопку и её родительский фрейм
                    btn_frame = self.buttons[old_name].master
                    if btn_frame.winfo_exists():
                        btn_frame.destroy()

            if old_name in self.text_area:
                if self.text_area[old_name].winfo_exists():
                    # Уничтожаем текстовое поле и его родительский фрейм
                    text_frame = self.text_area[old_name].master
                    if text_frame.winfo_exists():
                        text_frame.destroy()

        # Очищаем все словари
        tps = {}
        self.buttons = {}
        self.text_area = {}
        self.text_reg = {}
        self.scrollbars = {}
        self.button_frames = {}
        self.text_frames = {}

        # Создаем ТФ заново
        for idx, data in enumerate(temp_data, start=1):
            new_name = f"ТФ {idx}"

            # Создаем фрейм для кнопок
            button_frame = ttk.Frame(self.frame_tp)
            button_frame.grid(row=idx, column=1, padx=5, pady=5)

            # Создаем фрейм текстового поля
            text_frame = ttk.Frame(self.frame_tp)
            text_frame.grid(row=idx, column=0, padx=5, pady=5)

            # Создаем кнопку
            new_btn = ttk.Button(button_frame, text=f"Загрузить {new_name}",
                                 width=15)
            new_btn.grid(row=0, column=0, padx=5, pady=5)

            # Создаем текстовое поле
            new_text_area = tk.Text(text_frame, width=60, height=8, undo=True)
            self.configure_undo_by_char(new_text_area)
            new_text_area.grid(row=0, column=0, pady=5)
            new_text_area.bind("<Key>", self.on_key_universal)
            new_text_area.insert(tk.END, data['text_content'])

            # Создаем скроллбар
            new_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=new_text_area.yview)
            new_scrollbar.grid(row=0, column=1, sticky='ns')
            new_text_area['yscrollcommand'] = new_scrollbar.set

            # Создаем поле для regex
            new_text_reg = tk.Text(text_frame, width=60, height=3, undo=True)
            self.configure_undo_by_char(new_text_reg)
            new_text_reg.grid(row=1, column=0, pady=5)
            new_text_reg.bind("<Key>", self.on_key_universal)
            new_text_reg.insert(tk.END, data['reg_content'])

            # Создаем кнопку удаления
            delete_btn = ttk.Button(button_frame, text="Удалить", width=15)
            delete_btn.grid(row=1, column=0, padx=5, pady=5)

            # Сохраняем в словари
            self.buttons[new_name] = new_btn
            self.text_area[new_name] = new_text_area
            self.text_reg[new_name] = new_text_reg
            self.scrollbars[new_name] = new_scrollbar
            self.button_frames[new_name] = button_frame
            self.text_frames[new_name] = text_frame

            # Сохраняем в глобальный tps (для совместимости)
            tps[new_name] = new_text_area

            # Привязываем контекстное меню
            self.create_context_menu(new_text_area)
            self._bind_scroll_to_widget(button_frame)

            # Настраиваем команды кнопок после создания всех объектов
            new_btn.config(command=lambda name=new_name, btn=new_btn, text_area=new_text_area:
            self.load_tp(name, btn, text_area))
            delete_btn.config(command=lambda name=new_name, ta=new_text_area, lb=new_btn,
                                             db=delete_btn, sb=new_scrollbar, tr=new_text_reg:
            self.delete_tp(name, ta, lb, db, sb, tr))

        # Обновляем счетчик
        self.button_counter = len(temp_data)

        # Обновляем область прокрутки
        self.root.after(50, self._update_scroll_region)

    def print_tps(self):
        """Выводит все текстовые потоки в файл"""
        try:
            # Создаем директорию для экспорта, если её нет
            export_dir = "export_tps"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            # Создаем имя файла с текущей датой и временем
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(export_dir, f"tps_{current_datetime}.txt")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("ЭКСПОРТ ТЕКСТОВЫХ ПОТОКОВ (ТФ)\n")
                f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                for key, value in tps.items():
                    f.write(f"\n{'=' * 60}\n")
                    f.write(f"ТЕКСТОВЫЙ ПОТОК: {key}\n")
                    f.write(f"{'=' * 60}\n")

                    # Получаем содержимое
                    if isinstance(value, tk.Text):
                        content = value.get("1.0", tk.END).strip()
                    else:
                        content = str(value).strip()

                    f.write(content + "\n")
                    f.write(f"\n{'-' * 60}\n")
                    f.write(f"Количество символов: {len(content)}\n")

                f.write(f"\n{'=' * 80}\n")
                f.write(f"ВСЕГО ТЕКСТОВЫХ ПОТОКОВ: {len(tps)}\n")
                f.write("=" * 80 + "\n")

            messagebox.showinfo("Успех", f"Текстовые потоки успешно экспортированы в файл:\n{filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать ТФ: {e}")

    def print_characteristics(self):
        """Выводит все характеристики объекта в файл"""
        try:
            # Создаем директорию для экспорта, если её нет
            export_dir = "export_characteristics"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            # Создаем имя файла с текущей датой и временем
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(export_dir, f"characteristics_{current_datetime}.txt")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("ЭКСПОРТ ХАРАКТЕРИСТИК ОБЪЕКТА\n")
                f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                # Сортируем ключи для удобства чтения
                sorted_keys = sorted(characteristics.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)

                for key in sorted_keys:
                    value = characteristics[key]
                    f.write(f"{key}: {value}\n")

                f.write(f"\n{'=' * 80}\n")
                f.write(f"ВСЕГО ХАРАКТЕРИСТИК: {len(characteristics)}\n")
                f.write("=" * 80 + "\n")

                # Добавляем статистику по длине характеристик
                if characteristics:
                    lengths = [len(str(v)) for v in characteristics.values()]
                    f.write(f"\nСТАТИСТИКА:\n")
                    f.write(f"  Минимальная длина: {min(lengths)} символов\n")
                    f.write(f"  Максимальная длина: {max(lengths)} символов\n")
                    f.write(f"  Средняя длина: {sum(lengths) / len(lengths):.1f} символов\n")

            messagebox.showinfo("Успех", f"Характеристики успешно экспортированы в файл:\n{filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать характеристики: {e}")

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
        self.context_menu.add_command(label="Копировать (Ctrl+C)", command=lambda: self.copy_text())
        self.context_menu.add_command(label="Вставить (Ctrl+V)", command=lambda: self.paste_text())
        self.context_menu.add_command(label="Создать характеристику (Ctrl+W)", command=lambda: self.save_char())
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
        if not tps or len(tps) == 0:
            messagebox.showwarning("Предупреждение",
                                   "Нет текстовых потоков для обработки. Пожалуйста, добавьте хотя бы один текстовый поток.")
            return

        if not characteristics or len(characteristics) == 0:
            messagebox.showwarning("Предупреждение",
                                   "Нет характеристик объекта. Пожалуйста, добавьте характеристики перед генерацией.")
            return

        # --- ОЧИСТКА ВСЕХ ПОЛЕЙ С РЕГУЛЯРНЫМИ ВЫРАЖЕНИЯМИ ---
        for tp_name, text_widget in self.text_reg.items():
            text_widget.delete(1.0, tk.END)

        # Удаляем старые элементы, если они существуют
        if hasattr(self, 'progress'):
            self.progress.destroy()
        if hasattr(self, 'status_label'):
            self.status_label.destroy()

        # Создаём прогресс-бар и статус
        self.progress = ttk.Progressbar(frame_results, orient='horizontal', length=100, mode='determinate')
        self.progress.grid(row=8, column=0, padx=5, pady=5)

        self.status_label = tk.Label(frame_results, text="Обработка...")
        self.status_label.grid(row=9, column=0, padx=5, pady=5)

        # Инициализируем данные
        self.scripts = []
        self.tps_list = list(tps.items())
        self.current_index = 0
        self.total = len(self.tps_list)
        self.value_of_pers = 100 / self.total if self.total > 0 else 100

        # Запускаем обработку первого ТФ
        self.process_next_tp()

    def process_next_tp(self):
        if self.current_index < len(self.tps_list):
            key, value = self.tps_list[self.current_index]

            if isinstance(value, tk.Text):
                text_content = value.get("1.0", tk.END).strip()
            else:
                text_content = str(value).strip()

            if text_content:
                script = script_module.extract_scripts(text_content, characteristics)
                print(f"Последовательность хар-к {key}: ", script)
                # self.text_area[key].delete(1.0, tk.END)
                self.text_reg[key].insert(tk.INSERT, " ".join(script))
                self.scripts.append(script)  # ✅ Добавляем в self.scripts
            else:
                print(f"Пропущен пустой текстовый поток: {key}")

            self.current_index += 1
            self.progress['value'] = (self.current_index / self.total) * 100
            self.status_label.config(text=f"Осталось: {self.total - self.current_index}")

            # Асинхронный переход к следующему ТФ
            self.root.after(10, self.process_next_tp)  # можно уменьшить задержку

        else:
            # Все ТФ обработаны → завершаем
            self.finish_generation()  # ✅ Передаём данные дальше

    def finish_generation(self):
        """Завершает генерацию после обработки всех ТФ"""
        # Удаляем прогресс-бар и статус
        self.progress.destroy()
        self.status_label.destroy()

        scripts = self.scripts  # Берём накопленные скрипты

        if not scripts or not any(scripts):
            messagebox.showwarning("Предупреждение", "Не удалось извлечь скрипты.")
            self.insert_regex("")
            return

        non_empty_scripts = [s for s in scripts if s]
        scripts = non_empty_scripts

        try:
            start_edges = list(set(script_module.get_start_elements(scripts)))
            finish_edges = list(set(script_module.get_finish_elements(scripts)))

            print("Первыми ребрами могут быть", start_edges)
            print("Последними ребрами могут быть", finish_edges)
            print("-" * 20)

            dict_char = script_module.build_dict_char(scripts)
            print("Словарь хар-к объекта: ", dict_char)
            self.dict_char = dict_char

            gradation_type = self.gradation_type.get()
            categories_data = graph_metrics.get_characteristics_by_category(dict_char, gradation_type)
            self.display_metrics(categories_data['metrics'])
            self.display_categories(categories_data)

            print("*" * 20)

            transitions = transitions_builder.build_transitions(start_edges, scripts)
            self.transitions = transitions

            print(transitions)
            print("*" * 20)
            print(
                "--------------------------------------------------------------------------------------------------------------------")

            initial_state = 'S0'
            if initial_state not in transitions:
                initial_states = [s for s in transitions.keys() if isinstance(s, str) and s.startswith('S')]
                if initial_states:
                    initial_states.sort()
                    initial_state = initial_states[0]
                else:
                    messagebox.showerror("Ошибка", "Не найдено начальное состояние.")
                    self.insert_regex("")
                    return

            print(f"Генерируем регулярное выражение, начиная с состояния '{initial_state}'")
            regex = build_regex(initial_state, transitions)
            print("Регулярное выражение", regex)

            if not regex or regex.strip() == "":
                messagebox.showwarning("Предупреждение", "Не удалось сгенерировать регулярное выражение.")
                self.insert_regex("")
            else:
                self.insert_regex(regex)
                self.button_save_obj.config(state="normal")
                self.button_plot_state_graph.config(state="normal")
                self.button_plot_char_graph.config(state="normal")
                messagebox.showinfo("Успех", "Регулярное выражение успешно сгенерировано!")

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Ошибка", f"Ошибка при генерации: {e}")
            self.insert_regex("")

    # ------------------------------------------------------------------- ПОКАЗ ГРАФА В ОТДЕЛЬНОМ ОКНЕ -------------------------------------------------------------------

    def show_state_graph(self):
        """Показывает интерактивный граф состояний (только одно окно)"""
        if not self.transitions:
            messagebox.showwarning("Предупреждение", "Нет данных для построения графа состояний.")
            return

        try:

            graph.plot_state_graph(self.transitions, "state_graph.png")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить граф состояний: {e}")

    def show_char_graph(self):
        """Показывает интерактивный граф характеристик (только одно окно)"""
        if not hasattr(self, 'dict_char') or not self.dict_char:
            messagebox.showwarning("Предупреждение", "Нет данных для построения графа характеристик.")
            return

        try:
            import graph
            graph.plot_char_graph(self.dict_char, "char_graph.png")
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
            return

        # Извлечение данных
        name = data['name']
        regex = str(data['reg_var'])
        characteristics = data['props']
        tps_data = data['tps']  # Временно сохраняем в другую переменную

        # Удаление временной метки из имени, если есть
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}'
        name = re.sub(pattern, '', name)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':', '-')

        app.insert_name(name + " " + current_datetime)
        app.insert_regex(regex)

        # --- ЗАПОЛНЕНИЕ ПОЛЯ ХАРАКТЕРИСТИК (ЗАМЕНА СОДЕРЖИМОГО) ---
        # Очищаем текущее содержимое поля характеристик
        app.char_obj_txt.delete(1.0, tk.END)

        # Заполняем поле характеристик новыми данными
        for key, value in characteristics.items():
            app.char_obj_txt.insert(tk.INSERT, key + ": " + value + "\n")

        # Очищаем существующие текстовые потоки
        existing_keys = list(app.text_area.keys())
        for old_name in existing_keys:
            if old_name in app.buttons:
                if app.buttons[old_name].winfo_exists():
                    btn_frame = app.buttons[old_name].master
                    if btn_frame.winfo_exists():
                        btn_frame.destroy()
            if old_name in app.text_area:
                if app.text_area[old_name].winfo_exists():
                    text_frame = app.text_area[old_name].master
                    if text_frame.winfo_exists():
                        text_frame.destroy()

        # Очищаем словари
        tps = {}
        app.buttons = {}
        app.text_area = {}
        app.text_reg = {}
        app.scrollbars = {}
        app.button_frames = {}
        app.text_frames = {}

        # Добавляем новые текстовые потоки
        for key, value in tps_data.items():
            app.add_tp_edit()
            # Получаем последний добавленный ТФ
            last_key = list(app.text_area.keys())[-1]
            app.text_area[last_key].delete(1.0, tk.END)
            app.text_area[last_key].insert(tk.INSERT, value)

def restart_program():
    """Перезапускает приложение через запуск нового процесса"""
    response = messagebox.askyesno("Перезагрузка",
                                   "Нажмите 'Да' для перезагрузки редактора.\n"
                                   "Все несохранённые данные будут потеряны.")
    if response:
        try:
            # Сохраняем путь к текущему скрипту
            current_script_path = Path(__file__).resolve()

            # Запускаем новый процесс
            if sys.platform == 'win32':
                # Настройка для скрытия консоли
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                subprocess.Popen([sys.executable, str(current_script_path)],
                                 startupinfo=startupinfo,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, str(current_script_path)])

            # Даём время новому процессу на запуск
            time.sleep(0.5)

            # Завершаем текущий процесс
            root.quit()
            root.destroy()
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось перезагрузить приложение: {e}")

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
second_menu.add_command(label="Сохранить все ТФ в файл", command=app.print_tps)
second_menu.add_command(label="Сохранить все характеристики объекта в файл", command=app.print_characteristics)
second_menu.add_separator()
second_menu.add_command(label="Начать работу с новым объектом", command=restart_program)

main_menu.add_cascade(label="Редактор семантических объектов", menu=second_menu)

root.config(menu=main_menu)
root.mainloop()