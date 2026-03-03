# Файл replace.py

# Замена состояний
def replace_name_state(transitions, old_name, new_name, protected_states=None):
    """Безопасная замена состояния с защитой специальных состояний"""
    if protected_states is None:
        protected_states = {'Z'}

    # Проверяем, существует ли старое состояние
    if old_name not in transitions:
        print(f"Состояние {old_name} не найдено.")
        return transitions

    # Защищённые состояния нельзя заменять
    if old_name in protected_states:
        print(f"Предупреждение: попытка заменить защищённое состояние {old_name}")
        return transitions

    # Сохраняем переходы для старого состояния
    old_transitions = transitions[old_name]

    # Проверяем, ведёт ли состояние к Z
    leads_to_z = any(target == 'Z' for target in old_transitions.values())

    # Удаляем старое состояние
    del transitions[old_name]

    # Обновляем все переходы, ссылающиеся на старое состояние
    for state, edges in transitions.items():
        for edge in list(edges.keys()):  # Используем list() для безопасного удаления
            if edges[edge] == old_name:
                edges[edge] = new_name

    # Добавляем новое состояние с сохранением переходов
    # Но проверяем, не существует ли уже такое состояние
    if new_name not in transitions:
        transitions[new_name] = old_transitions
    else:
        # Если состояние уже существует, объединяем переходы
        for edge, target in old_transitions.items():
            transitions[new_name][edge] = target

    return transitions


# Замена всех вхождений
def replace_all_state(transitions, old_name, new_name):
    """Заменяет все вхождения старого состояния на новое"""
    for state, edges in transitions.items():
        for edge in list(edges.keys()):
            if edges[edge] == old_name:
                edges[edge] = new_name
    return transitions