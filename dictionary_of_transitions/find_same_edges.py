# Файл find_same_edges.py

def find_one_same_edges(state, transitions_dict):
    """Поиск состояний с одинаковыми исходящими рёбрами"""
    # Проверяем, существует ли состояние в словаре
    if state not in transitions_dict:
        return []

    # Извлекаем рёбра для заданного состояния
    target_edges = transitions_dict[state]
    same_edge_states = []

    # Проверяем, ведёт ли состояние прямо к Z
    leads_to_z = any(target == 'Z' for target in target_edges.values())

    # Сравниваем с другими состояниями
    for other_state, edges in transitions_dict.items():
        # Пропускаем само себя и защищённые состояния
        if other_state == state or other_state == 'Z':
            continue

        # Проверяем, ведёт ли другое состояние к Z
        other_leads_to_z = any(target == 'Z' for target in edges.values())

        # Если ОДНО ведёт к Z, а другое нет - НЕ объединяем
        if leads_to_z != other_leads_to_z:
            continue

        # Если оба ведут к Z, проверяем точное совпадение словарей
        if leads_to_z and other_leads_to_z:
            if edges == target_edges:
                same_edge_states.append(other_state)
        else:
            # Для не-финальных состояний можно объединять при равенстве рёбер
            if edges == target_edges:
                same_edge_states.append(other_state)

    return same_edge_states


def find_all_same_edges(transitions_dict):
    """Находит все группы состояний с одинаковыми рёбрами"""
    result = []
    seen = set()  # Множество для отслеживания уже добавленных наборов

    for state in transitions_dict.keys():
        # Пропускаем защищённые состояния
        if state == 'Z':
            continue

        same_edges = find_one_same_edges(state, transitions_dict)
        if same_edges and state not in seen:
            # Создаём множество состояний
            edge_set = {state}
            edge_set.update(same_edges)
            edge_set = tuple(sorted(edge_set))

            if edge_set not in seen:
                result.append(edge_set)
                seen.update(edge_set)

    return result


def same_edges(transitions_dict):
    """Обёртка для получения групп одинаковых рёбер"""
    same_edges_groups = find_all_same_edges(transitions_dict)
    return same_edges_groups