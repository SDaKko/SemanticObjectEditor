# transitions_builder.py

from graph import optimize_state_graph  # Добавить импорт в начало файла

transitions = {}
state_counter = -1
scripts = []  # Будем получать извне


def get_new_state_name():
    global state_counter
    state_counter += 1
    return f'S{state_counter}'


def build_transitions(start_edges, input_scripts, optimize=True):
    """
    Строит граф переходов между состояниями.

    Args:
        start_edges: Список начальных характеристик
        input_scripts: Список сценариев
        optimize: Если True, выполняет оптимизацию графа (объединение эквивалентных состояний)

    Returns:
        dict: Словарь переходов (оптимизированный, если optimize=True)
    """
    global state_counter, scripts
    scripts = input_scripts
    state_counter = -1
    initial_state = get_new_state_name()
    transitions.clear()
    transitions[initial_state] = {}
    final_state = 'Z'
    transitions[final_state] = {}

    char_is_last = set(seq[-1] for seq in scripts if seq)

    def process_path(seq, index, current_state):
        if index >= len(seq):
            return
        edge = seq[index]
        is_last = (index == len(seq) - 1)

        if is_last:
            if edge not in transitions[current_state]:
                transitions[current_state][edge] = []
            if 'Z' not in transitions[current_state][edge]:
                transitions[current_state][edge].append('Z')
        else:
            next_edge = seq[index + 1]
            if edge not in transitions[current_state]:
                next_state_name = get_new_state_name()
                transitions[current_state][edge] = [next_state_name]
                transitions[next_state_name] = {}
            else:
                existing_targets = transitions[current_state][edge]
                target_state = None
                for t in existing_targets:
                    if t != 'Z' and next_edge in transitions.get(t, {}):
                        target_state = t
                        break
                if target_state is None:
                    target_state = get_new_state_name()
                    transitions[current_state][edge].append(target_state)
                    transitions[target_state] = {}
            # Рекурсивно обрабатываем следующий шаг
            next_state = transitions[current_state][edge][-1]
            process_path(seq, index + 1, next_state)

    for seq in input_scripts:
        if seq and seq[0] in start_edges:
            process_path(seq, 0, initial_state)

    # Оптимизация графа (ОДИН РАЗ здесь)
    if optimize:
        print("Выполняется оптимизация графа...")
        result = optimize_state_graph(transitions)
        print("Оптимизация завершена")
        return result

    return transitions
