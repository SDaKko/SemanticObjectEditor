# Файл graph_metrics.py
# Вычисление метрик графа и разделение характеристик по градации
import math


# def calculate_graph_metrics(dict_char):
#     """
#     Вычисляет метрики графа на основе словаря характеристик.
#
#     Args:
#         dict_char: Словарь характеристик {характеристика: [список_следующих]}
#
#     Returns:
#         dict: Словарь с метриками:
#             - vertices: количество вершин (уникальных характеристик)
#             - edges: количество дуг (уникальные переходы)
#             - density: плотность графа (edges / vertices)
#             - complexity_score: оценка сложности (0.0 - 1.0)
#     """
#     if not dict_char:
#         return {
#             'vertices': 0,
#             'edges': 0,
#             'density': 0.0,
#             'complexity_score': 0.0
#         }
#
#     # Количество вершин (уникальных характеристик)
#     vertices = len(dict_char)
#
#     # Количество дуг (уникальные переходы)
#     # Сначала проверим структуру данных
#     unique_edges = set()
#
#     for char, next_chars in dict_char.items():
#         # Преобразуем next_chars в список, если это не список
#         if not isinstance(next_chars, list):
#             if next_chars:  # Если это не пустая строка или не None
#                 next_chars = [next_chars]
#             else:
#                 next_chars = []
#
#         # Используем множество для удаления дубликатов в списке следующих характеристик
#         unique_next_chars = set(next_chars)
#         for next_char in unique_next_chars:
#             if next_char:  # Игнорируем пустые значения
#                 unique_edges.add((char, next_char))
#
#     edges = len(unique_edges)
#
#     # Плотность графа (отношение дуг к вершинам)
#     # Для полного графа максимальная плотность = vertices * (vertices - 1)
#     if vertices <= 1:
#         max_possible_edges = 0
#         density = 0.0
#     else:
#         max_possible_edges = vertices * (vertices - 1)
#         density = edges / max_possible_edges if max_possible_edges > 0 else 0.0
#
#     # Оценка сложности на основе метрик
#     # Нормализуем значения для получения оценки от 0.0 до 1.0
#     # Используем комбинацию количества вершин, дуг и плотности
#     # vertices_score = min(vertices / 10.0, 1.0)  # Нормализуем до 10 вершин
#     # edges_score = min(edges / 20.0, 1.0)  # Нормализуем до 20 дуг
#
#     # Логарифмическая шкала — учитывает рост, но сглаживает
#     vertices_score = min(math.log(vertices + 1) / math.log(50), 1.0)
#     edges_score = min(math.log(edges + 1) / math.log(100), 1.0)
#     density_score = density  # Уже нормализовано
#
#     # Взвешенная комбинация метрик
#     complexity_score = (vertices_score * 0.3 + edges_score * 0.4 + density_score * 0.3)
#     complexity_score = min(complexity_score, 1.0)  # Ограничиваем до 1.0
#
#     return {
#         'vertices': vertices,
#         'edges': edges,
#         'density': round(density, 3),
#         'complexity_score': round(complexity_score, 3)
#     }


def calculate_graph_metrics(dict_char):
    """
    Вычисляет метрики графа с логарифмической нормализацией.
    Сложность перестаёт расти после:
        - 100 вершин
        - 200 дуг
    """
    if not dict_char:
        return {
            'vertices': 0,
            'edges': 0,
            'density': 0.0,
            'complexity_score': 0.0
        }

    vertices = len(dict_char)

    # Количество дуг (уникальные переходы)
    unique_edges = set()
    for char, next_chars in dict_char.items():
        if not isinstance(next_chars, list):
            next_chars = [next_chars] if next_chars else []
        for next_char in set(next_chars):
            if next_char:
                unique_edges.add((char, next_char))
    edges = len(unique_edges)

    # Плотность (как раньше)
    if vertices <= 1:
        density = 0.0
    else:
        max_possible_edges = vertices * (vertices - 1)
        density = edges / max_possible_edges if max_possible_edges > 0 else 0.0

    # Логарифмическая нормализация
    # Сложность растёт до 100 вершин и 200 дуг
    V_THRESHOLD = 100
    E_THRESHOLD = 200

    vertices_score = min(math.log(vertices + 1) / math.log(V_THRESHOLD), 1.0)
    edges_score    = min(math.log(edges + 1)    / math.log(E_THRESHOLD), 1.0)
    density_score  = density

    # Взвешенная сложность
    complexity_score = (vertices_score * 0.3 +
                        edges_score    * 0.4 +
                        density_score  * 0.3)

    complexity_score = min(complexity_score, 1.0)

    return {
        'vertices': vertices,
        'edges': edges,
        'density': round(density, 3),
        'complexity_score': round(complexity_score, 3)
    }


def categorize_characteristics(dict_char, gradation_type='simple'):
    """
    Разделяет характеристики на категории по метрикам графа.

    Args:
        dict_char: Словарь характеристик {характеристика: [список_следующих]}
        gradation_type: Тип градации ('simple' или 'detailed')
            - 'simple': (0.5, 0.75, 1.0)
            - 'detailed': (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)

    Returns:
        dict: Словарь с категориями характеристик:
            - categories: {категория: [список_характеристик]}
            - metrics: метрики графа
            - gradation: использованная градация
    """
    metrics = calculate_graph_metrics(dict_char)
    complexity = metrics['complexity_score']

    # Определяем градацию
    if gradation_type == 'simple':
        gradation = [0.5, 0.75, 1.0]
    else:  # detailed
        gradation = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # Определяем категорию для каждой характеристики
    categories = {}

    for char, next_chars in dict_char.items():
        # Преобразуем next_chars в список, если это не список
        if not isinstance(next_chars, list):
            if next_chars:  # Если это не пустая строка или не None
                next_chars = [next_chars]
            else:
                next_chars = []

        # Вычисляем локальную метрику для характеристики
        # Количество уникальных исходящих дуг
        local_edges = len(set(next_chars))
        max_local_edges = len(dict_char) - 1  # Максимум возможных переходов

        if max_local_edges > 0:
            local_density = local_edges / max_local_edges
        else:
            local_density = 0.0

        # Комбинируем глобальную и локальную метрики
        local_complexity = (complexity * 0.6 + local_density * 0.4)

        # Определяем категорию на основе градации
        category = None
        for threshold in gradation:
            if local_complexity <= threshold:
                category = f"{threshold:.2f}"
                break

        # Если не попали ни в одну категорию, относим к максимальной
        if category is None:
            category = f"{gradation[-1]:.2f}"

        if category not in categories:
            categories[category] = []
        categories[category].append({
            'char': char,
            'next_chars': next_chars,
            'local_edges': local_edges,
            'local_complexity': round(local_complexity, 3)
        })

    return {
        'categories': categories,
        'metrics': metrics,
        'gradation': gradation
    }


def get_characteristics_by_category(dict_char, gradation_type='simple'):
    """
    Возвращает характеристики, разделенные по категориям с метриками.

    Args:
        dict_char: Словарь характеристик
        gradation_type: Тип градации ('simple' или 'detailed')

    Returns:
        dict: Структурированные данные для отображения
    """
    result = categorize_characteristics(dict_char, gradation_type)

    # Форматируем результат для удобного отображения
    formatted_categories = {}
    for category, chars in result['categories'].items():
        formatted_categories[category] = {
            'count': len(chars),
            'characteristics': [item['char'] for item in chars],
            'details': chars
        }

    return {
        'categories': formatted_categories,
        'metrics': result['metrics'],
        'gradation': result['gradation'],
        'total_vertices': result['metrics']['vertices'],
        'total_edges': result['metrics']['edges']
    }