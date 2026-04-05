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



characteristics = {}
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
#     "q85": "Выйди на крышу. Встань на край. Победи свой последний страх.",
#     "q86": "Завтра в полночь жду тебя на крыше. Будь там.",
#     "q87": "Ты видишь номер на стене? Запомни его. Это твой новый код.",
#     "q88": "Найди самое высокое место в своем городе и сфотографируй вид.",
#     "q89": "Выброси телефон. Связь со мной важнее связи с миром.",
#     "q90": "Это не игра. Это твоя новая реальность.",
#     "q91": "Твои родители никогда тебя не понимали. Я — понимаю.",
#     "q92": "Сожги что-нибудь из своих старых вещей. Очищение огнем.",
#     "q93": "Покажи мне свои слезы. Докажи, что можешь чувствовать боль.",
#     "q94": "Ты уже мертв для них. Теперь живи для меня.",
#     "q95": "Твое задание — найти синий кит в городе. Надпись, граффити, игрушку.",
#     "q96": "Если ты не придешь, я приду к тебе сам.",
#     "q97": "С этого момента ты говоришь только со мной. Все остальные — шум.",
#     "q98": "Пришли мне видео, где ты причиняешь себе небольшую боль.",
#     "q99": "Ты больше не принадлежишь себе. Ты мой.",
#     "q100": "Следующая ступень: проведи весь день в полной тишине и темноте.",
#     "q101": "Ты видишь узор? Все ведет к одному финалу.",
#     "q102": "Завтра ты получишь последнюю инструкцию. Будь готов.",
#     "q103": "Ты слышишь голоса? Скоро услышишь только мой.",
#     "q104": "Твое время истекло. Пора сделать выбор.",
#     "q105": "Добро пожаловать в море свободы."
#
# }

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



        # --- ГЕНЕРАЦИЯ ТЕКСТА С ПОМОЩЬЮ LLM ---
        llm_frame = ttk.LabelFrame(frame_results, text="Генерация текста с помощью ИИ")
        llm_frame.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

        # Выбор типа генерации
        self.gen_type = tk.StringVar(value="style")

        ttk.Radiobutton(llm_frame, text="По стилю", variable=self.gen_type, value="style").grid(row=0, column=0, padx=5,
                                                                                                pady=2)
        ttk.Radiobutton(llm_frame, text="По примеру", variable=self.gen_type, value="example").grid(row=0, column=1,
                                                                                                    padx=5, pady=2)

        # Поле ввода примера (видимо только при "по примеру")
        self.example_text = tk.Text(llm_frame, width=60, height=3)
        self.example_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.example_text.grid_remove()  # Скрыто по умолчанию

        # Выбор длины
        length_label = tk.Label(llm_frame, text="Длина:")
        length_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.length_var = tk.StringVar(value="средний")
        length_combo = ttk.Combobox(llm_frame, textvariable=self.length_var, values=["короткий", "средний", "длинный"],
                                    state="readonly", width=10)
        length_combo.grid(row=2, column=1, padx=5, pady=2)

        # Кнопка генерации
        self.generate_btn = ttk.Button(llm_frame, text="Сгенерировать текст", command=self.generate_llm_text)
        self.generate_btn.grid(row=3, column=0, columnspan=3, pady=5)

        # Привязка изменения типа к отображению поля
        self.gen_type.trace("w", self.toggle_example_field)

    def confirm_action(self):
        return messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сохранить характеристики?")

    def toggle_example_field(self, *args):
        if self.gen_type.get() == "example":
            self.example_text.grid()
        else:
            self.example_text.grid_remove()

    def generate_llm_text(self):
        if not LLM_AVAILABLE:
            messagebox.showerror("Ошибка", "Сервис LLM недоступен. Убедитесь, что получен токен доступа к GigaChat.")
            return

        length = self.length_var.get()

        try:
            if self.gen_type.get() == "style":
                style = simpledialog.askstring(
                    "Выбор стиля",
                    "Доступные стили:\n- манипулятивный\n- терапевтический\n- загадочный\n- провокационный\n\nВведите стиль:"
                )
                if not style:
                    return
                result = generator.generate_by_style(style, length)
            else:  # example
                example = self.example_text.get("1.0", tk.END).strip()
                if not example:
                    messagebox.showwarning("Предупреждение", "Введите пример текста.")
                    return
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

        # Создание новой кнопки "Загрузить ТФ" (активна всегда)
        new_btn = ttk.Button(self.button_frame, text=f"Загрузить {tp_name}",
                             command=lambda: self.load_tp(tp_name, new_btn, new_text_area), width=15)
        new_btn.grid(row=0, column=0, padx=5, pady=5)
        self.buttons[tp_name] = new_btn  # Сохраняем кнопку в словаре

        # Создание нового текстового поля
        new_text_area = tk.Text(self.text_frame, width=60, height=8)
        new_text_area.grid(row=0, column=0, pady=5)
        self.text_area[tp_name] = new_text_area

        tps[tp_name] = new_text_area

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
        delete_btn = ttk.Button(self.button_frame, text="Удалить",
                                command=lambda: self.delete_tp(tp_name, new_text_area, new_btn, delete_btn,
                                                               new_scrollbar, new_text_reg), width=15)
        delete_btn.grid(row=1, column=0, padx=5, pady=5)

        # Привязываем контекстное меню
        self.create_context_menu(new_text_area)

        # Увеличение счетчика
        self.button_counter += 1

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

            transitions = build_dictionary.build_main_dict(start_edges, scripts)
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