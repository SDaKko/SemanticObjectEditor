# Файл script.py
import re
from typing import List, Tuple, Any


# Вычисление значения семантической близости
def semantic_similarity(sentence1, sentence2):
    # Очищаем от знаков препинания и приводим к нижнему регистру
    import string
    translator = str.maketrans('', '', string.punctuation)

    clean_s1 = sentence1.lower().translate(translator)
    clean_s2 = sentence2.lower().translate(translator)

    # Разбиваем на слова
    tokens1 = set(clean_s1.split())
    tokens2 = set(clean_s2.split())

    # Если оба множества пустые
    if len(tokens1) == 0 and len(tokens2) == 0:
        return 1.0
    if len(tokens1) == 0 or len(tokens2) == 0:
        return 0.0

    # Вычисляем пересечение и объединение
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)

    sem_prox = round((len(intersection) / len(union)), 2)
    return sem_prox


# Улучшенная токенизация - сохраняем предложения целиком
def tokenize(text):
    # Разбиваем по .?! но НЕ удаляем знаки внутри предложения
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


# Альтернативная токенизация - сохраняем знаки препинания
def tokenize_advanced(text):
    # Находим границы предложений, но не разрываем их
    sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-ZА-Я])')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]


# Вычисление сценария с улучшенным сравнением
def extract_scripts(text, character, threshold=0.6):
    sentences = tokenize(text)
    sequence = []

    print(f"Разбито на предложения: {sentences}")
    print(f"Порог схожести: {threshold}\n")

    # Для каждого предложения проверяем, встречается ли характеристика
    for sentence in sentences:

        best_match = None
        best_score = 0
        best_key = None

        for key, pattern in character.items():
            # Сравниваем текущее предложение с паттерном
            curr_sem_prox = semantic_similarity(pattern, sentence)

            print(f"Сравнение: '{sentence[:50]}...' с '{pattern[:50]}...' -> {curr_sem_prox}")

            if curr_sem_prox > best_score:
                best_score = curr_sem_prox
                best_key = key
                best_match = pattern

        # Если лучшая схожесть превышает порог
        if best_score >= threshold:
            print(f'*** СОВПАДЕНИЕ *** Предложение: "{sentence}"')
            print(f'  Подходит под: "{best_match}" с оценкой {best_score}')
            sequence.append(best_key)
        else:
            print(f'Нет совпадений для: "{sentence}" (лучшая оценка: {best_score})')
        print()

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


# Поиск списка первых элементов из каждого списка
def get_start_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    start_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[0] not in start_elements:
                start_elements.append(lst[0])  # Добавляем первый элемент в результат
    return start_elements


# Поиск списка последних элементов из каждого списка
def get_finish_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    finish_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[-1] not in finish_elements:
                finish_elements.append(lst[-1])  # Добавляем последний элемент в результат
    return finish_elements