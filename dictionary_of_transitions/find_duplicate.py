# Файл find_duplicate.py
def main_find_duplicate(transitions_dict):
    """Главная функция поиска дубликатов"""
    # Находим входные и выходные рёбра
    edges_info = find_edges(transitions_dict)
    # Ищем дубликаты, передаём оба параметра
    duplicates = find_duplicate_states(edges_info, transitions_dict)
    return duplicates


# Находим входные и выходные рёбра
def find_edges(transitions):
    edges_info = {}
    # Инициализация словаря для всех состояний
    for state in transitions.keys():
        edges_info[state] = {
            'incoming': set(),
            'outgoing': set()
        }

    # Заполнение выходных и входных рёбер
    for state, edges in transitions.items():
        for edge, next_state in edges.items():
            edges_info[state]['outgoing'].add(edge)
            edges_info[next_state]['incoming'].add(edge)
    return edges_info


# Ищем дубликаты - ИСПРАВЛЕНО: добавлен второй параметр
def find_duplicate_states(edges_info, transitions_dict):
    """Поиск состояний-дубликатов с защитой конечных состояний"""
    seen_states = {}
    duplicates = []

    # Специальные состояния, которые НЕЛЬЗЯ объединять
    protected_states = {'Z'}  # Конечное состояние

    for state in reversed(edges_info.keys()):
        # Пропускаем защищённые состояния
        if state in protected_states:
            continue

        # Получаем переходы из состояния
        state_transitions = transitions_dict.get(state, {})

        # ВАЖНО: включаем в ключ информацию о том, КУДА ведут переходы
        outgoing_with_targets = frozenset(
            (edge, target) for edge, target in state_transitions.items()
        )

        # Формируем ключ для сравнения
        key = (
            frozenset(edges_info[state]['incoming']),
            frozenset(edges_info[state]['outgoing']),
            outgoing_with_targets  # Добавляем информацию о целевых состояниях
        )

        # Проверяем, ведёт ли состояние к Z
        leads_to_z = any(target == 'Z' for target in state_transitions.values())

        if key in seen_states:
            # Только не-финальные состояния можно объединять
            if not leads_to_z:
                seen_states[key].add(state)
        else:
            seen_states[key] = {state}

    # Собираем группы дубликатов
    for states in seen_states.values():
        if len(states) > 1:  # Если есть более одного дубликата
            duplicates.append(states)

    return duplicates