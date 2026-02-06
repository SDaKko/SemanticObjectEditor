# Файл script.py

import re
from typing import List, Tuple, Any

# Извлечение последовательностей характеристик из текстов
# Вычисление значения семантической близости
def semantic_similarity(sentence1, sentence2):
    # Создаются множества для удаления повторяющихся элементов
    tokens1 = set(sentence1)
    tokens2 = set(sentence2)

    # Вычисляется пересечение множеств
    intersection = tokens1.intersection(tokens2)
    # Вычисляется объединение множеств
    union = tokens1.union(tokens2)

    sem_prox = round((len(intersection) / len(union)), 2)
    # Вычисляется семантическая близость
    return sem_prox

# Токенизация по предложениям
def tokenize(text):
    sentences = re.split(r'[.?!]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

# Вычисление сценария в каждом ТП
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def extract_scripts(text, character):
    sequence = []
    sentences = re.split(r'[.?!]', text)

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        best_key = None
        best_score = 0.7

        for key, pattern in character.items():
            score = similarity(sent, pattern)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key:
            sequence.append(best_key)

    return sequence

# Построение словаря характеристик из сценариев
def build_dict_char(scripts):
    # Получаем уникальные элементы всех скриптов для упрощения
    unique_elements = set()
    for script in scripts:
        unique_elements.update(script)

    # Словарь для хранения множеств следования
    sequences = {elem: [] for elem in unique_elements}

    # Смотрим на все комбинации в скриптах
    for i in range(len(scripts)):
        for j in range(len(scripts[i]) - 1):
            primary = scripts[i][j]
            secondary = scripts[i][j + 1]
            sequences[primary].append(secondary)

    return sequences

# Поиск списка последних элементов из каждого списка
def get_start_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    start_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[0] not in start_elements:
                start_elements.append(lst[0])  # Добавляем последний элемент в результат
    return start_elements

# Поиск списка последних элементов из каждого списка
def get_finish_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    finish_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[-1] not in finish_elements:
                finish_elements.append(lst[-1])  # Добавляем последний элемент в результат
    return finish_elements