# Файл test_integration.py
# Интеграционные тесты для проверки работы всей системы

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from regex import build_regex
import dictionary_of_transitions.build_dictionary as build_dictionary
import script as script_module


def test_full_workflow():
    """Тест полного рабочего процесса генерации регулярного выражения"""
    print("=" * 80)
    print("ИНТЕГРАЦИОННЫЙ ТЕСТ: Полный рабочий процесс")
    print("=" * 80)
    
    # Шаг 1: Создаем тестовые характеристики объекта
    print("\nШаг 1: Создание характеристик объекта")
    characteristics = {
        'Q1': 'начало работы',
        'Q2': 'основной процесс',
        'Q3': 'завершение работы'
    }
    print(f"Характеристики: {characteristics}")
    
    # Шаг 2: Создаем тестовые текстовые потоки
    print("\nШаг 2: Создание текстовых потоков")
    text_flows = {
        'TP1': 'Начало работы. Основной процесс. Завершение работы.',
        'TP2': 'Начало работы. Основной процесс. Основной процесс. Завершение работы.',
        'TP3': 'Начало работы. Завершение работы.'
    }
    print(f"Текстовые потоки: {text_flows}")
    
    # Шаг 3: Извлекаем скрипты из текстовых потоков
    print("\nШаг 3: Извлечение скриптов из текстовых потоков")
    scripts = []
    for tp_name, text in text_flows.items():
        script = script_module.extract_scripts(text, characteristics)
        scripts.append(script)
        print(f"{tp_name}: {script}")
    
    # Шаг 4: Строим словарь переходов
    print("\nШаг 4: Построение словаря переходов")
    dict_char = script_module.build_dict_char(scripts)
    print(f"Словарь переходов: {dict_char}")
    
    # Шаг 5: Находим начальные и конечные элементы
    print("\nШаг 5: Поиск начальных и конечных элементов")
    start_edges = script_module.get_start_elements(tuple(scripts))
    finish_edges = script_module.get_finish_elements(tuple(scripts))
    print(f"Начальные элементы: {start_edges}")
    print(f"Конечные элементы: {finish_edges}")
    
    # Шаг 6: Строим основной словарь переходов
    print("\nШаг 6: Построение основного словаря переходов")
    transitions = build_dictionary.build_main_dict(dict_char, start_edges, finish_edges)
    print(f"Словарь переходов: {transitions}")
    
    # Шаг 7: Генерируем регулярное выражение
    print("\nШаг 7: Генерация регулярного выражения")
    regex = build_regex('S0', transitions)
    print(f"Регулярное выражение: {regex}")
    
    print("\n" + "=" * 80)
    print("ИНТЕГРАЦИОННЫЙ ТЕСТ ЗАВЕРШЕН")
    print("=" * 80)
    
    return regex


def test_with_sample_data():
    """Тест с примерными данными, похожими на реальные"""
    print("\n" + "=" * 80)
    print("ТЕСТ С ПРИМЕРНЫМИ ДАННЫМИ")
    print("=" * 80)
    
    # Примерные характеристики для объекта "Документ"
    characteristics = {
        'Q1': 'создание документа',
        'Q2': 'редактирование документа',
        'Q3': 'проверка документа',
        'Q4': 'сохранение документа',
        'Q5': 'отправка документа'
    }
    
    # Примерные текстовые потоки
    text_flows = {
        'TP1': 'Создание документа. Редактирование документа. Сохранение документа.',
        'TP2': 'Создание документа. Редактирование документа. Проверка документа. Сохранение документа.',
        'TP3': 'Создание документа. Редактирование документа. Отправка документа.',
        'TP4': 'Создание документа. Сохранение документа.'
    }
    
    print(f"\nХарактеристики: {characteristics}")
    print(f"\nТекстовые потоки:")
    for key, value in text_flows.items():
        print(f"  {key}: {value}")
    
    # Извлекаем скрипты
    scripts = []
    for tp_name, text in text_flows.items():
        script = script_module.extract_scripts(text, characteristics)
        scripts.append(script)
        print(f"\nСкрипт {tp_name}: {script}")
    
    # Строим граф переходов
    dict_char = script_module.build_dict_char(scripts)
    print(f"\nСловарь переходов: {dict_char}")
    
    start_edges = script_module.get_start_elements(tuple(scripts))
    finish_edges = script_module.get_finish_elements(tuple(scripts))
    print(f"\nНачальные элементы: {start_edges}")
    print(f"Конечные элементы: {finish_edges}")
    
    # Строим основной словарь
    transitions = build_dictionary.build_main_dict(dict_char, start_edges, finish_edges)
    print(f"\nОсновной словарь переходов: {transitions}")
    
    # Генерируем регулярное выражение
    regex = build_regex('S0', transitions)
    print(f"\n" + "=" * 80)
    print(f"РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ: {regex}")
    print("=" * 80)
    
    return regex


if __name__ == '__main__':
    # Запускаем интеграционные тесты
    test_full_workflow()
    test_with_sample_data()

