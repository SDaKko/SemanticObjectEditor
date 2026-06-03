# graph_metrics.py
import math
def calculate_graph_metrics(dict_char):
    """
    Вычисляет метрики графа.
    МЕТРИКИ:
    1. vertices - количество вершин (уникальных характеристик)
    2. edges - количество уникальных переходов (дуг)
    3. max_possible_edges - максимально возможное количество дуг
       - Для ориентированного графа: vertices**2
       - Каждая вершина может иметь переход в саму себя
    4. density - плотность графа = edges / max_possible_edges
    5. complexity_score - общая сложность графа (от 0.0 до 1.0)
    """
    if not dict_char:
        return {
            'vertices': 0,
            'edges': 0,
            'density': 0.0,
            'complexity_score': 0.0
        }

    vertices = len(dict_char)

    # === 1. Количество уникальных переходов (дуг) ===
    unique_edges = set()
    for char, next_chars in dict_char.items():
        if not isinstance(next_chars, list):
            next_chars = [next_chars] if next_chars else []
        for next_char in set(next_chars):
            if next_char:  # Игнорируем пустые значения
                unique_edges.add((char, next_char))
    edges = len(unique_edges)

    # === 2. Максимально возможное количество дуг ===
    # Для ориентированного графа:
    # каждая из vertices вершин может иметь переход в любую из vertices вершин
    # включая саму себя: vertices * vertices = vertices**2
    max_possible_edges = vertices * vertices if vertices > 0 else 0

    # === 3. Плотность графа ===
    # Показывает, какая доля возможных связей реально существует
    # Пример: 54 вершины - максимум 2916 дуг (включая петли)
    # Если дуг 54 - плотность = 54/2916 = 0.0185 (1.85%)
    if max_possible_edges > 0:
        density = edges / max_possible_edges
    else:
        density = 0.0

    # === 4. Нормированные метрики ===
    def logistic_norm(x, midpoint=50, steepness=0.05):
        return 1 / (1 + math.exp(-steepness * (x - midpoint)))

    vertices_score = logistic_norm(vertices, midpoint=50, steepness=0.05)
    edges_score = logistic_norm(edges, midpoint=100, steepness=0.03)
    density_score = density

    # === 5. Итоговая сложность ===
    complexity_score = (vertices_score * 0.3 +
                        edges_score * 0.5 +
                        density_score * 0.2)

    complexity_score = min(max(complexity_score, 0.0), 1.0)

    return {
        'vertices': vertices,
        'edges': edges,
        'density': round(density, 4),
        'complexity_score': round(complexity_score, 4)
    }


def calculate_local_complexity(char, next_chars, total_vertices):
    """
    Вычисляет локальную сложность для одной характеристики.

    Локальная сложность = количество исходящих дуг / максимально возможное количество

    Максимально возможное количество исходящих дуг ДЛЯ ОДНОЙ ВЕРШИНЫ:
    - Если разрешены петли: total_vertices (может перейти в себя + во все другие)
    """
    if not isinstance(next_chars, list):
        next_chars = [next_chars] if next_chars else []

    unique_targets = set(next_chars)
    out_degree = len(unique_targets)

    # Максимально возможное количество исходящих дуг из одной вершины
    max_possible = total_vertices

    if max_possible <= 0:
        return 0.0

    return out_degree / max_possible


def categorize_characteristics(dict_char, gradation_type='simple'):
    """
    Разделяет характеристики на категории по локальной сложности.

    Типы градации:
    - 'simple': шаг 0.25 - [0.25, 0.5, 0.75, 1.0]
    - 'detailed': шаг 0.1 - [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    """
    metrics = calculate_graph_metrics(dict_char)
    total_vertices = metrics['vertices']

    # === ТИПЫ ГРАДАЦИИ ===
    if gradation_type == 'simple':
        # Простая градация: через 0.25 от 0 до 1
        gradation = [0.25, 0.5, 0.75, 1.0]
    else:  # detailed
        # Детальная градация: через 0.1 от 0 до 1
        gradation = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    categories = {}

    for char, next_chars in dict_char.items():
        if not isinstance(next_chars, list):
            next_chars = [next_chars] if next_chars else []

        unique_targets = set(next_chars)
        local_edges = len(unique_targets)

        # Локальная сложность с учётом петель
        local_complexity = calculate_local_complexity(char, next_chars, total_vertices)
        local_complexity = round(local_complexity, 3)

        # Определяем категорию
        category = None
        for threshold in gradation:
            if local_complexity <= threshold:
                category = f"{threshold:.2f}"
                break

        if category is None:
            category = f"{gradation[-1]:.2f}"

        if category not in categories:
            categories[category] = []

        categories[category].append({
            'char': char,
            'next_chars': list(unique_targets),
            'local_edges': local_edges,
            'local_complexity': local_complexity
        })

    return {
        'categories': categories,
        'metrics': metrics,
        'gradation': gradation
    }


def get_characteristics_by_category(dict_char, gradation_type='simple'):
    """Возвращает характеристики, разделенные по категориям."""
    result = categorize_characteristics(dict_char, gradation_type)

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
