# dictionary_of_transitions/build_dictionary.py

import dictionary_of_transitions.find_same_edges as find_same_edges
import dictionary_of_transitions.find_duplicate as find_duplicate
import dictionary_of_transitions.replace as replace

transitions = {}
state_counter = -1
scripts = []  # Будем получать извне


def get_new_state_name():
    global state_counter
    state_counter += 1
    return f'S{state_counter}'


def build_transitions(graph, start_edges, finish_edges, input_scripts):
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
            # Берём только что созданное состояние
            next_state = transitions[current_state][edge][-1]
            process_path(seq, index + 1, next_state)

    for seq in input_scripts:
        if seq and seq[0] in start_edges:
            process_path(seq, 0, initial_state)

    return transitions



def replace_pre_aft_duplicate(transitions):
    """Безопасное удаление дубликатов с защитой Z и конечных переходов"""
    if not transitions:
        return transitions

    duplicates = find_duplicate.main_find_duplicate(transitions)
    iteration = 0
    max_iterations = 10  # Защита от бесконечного цикла

    while duplicates and iteration < max_iterations:
        iteration += 1
        new_state = get_new_state_name()

        # Берём только первую группу дубликатов
        group = duplicates[0]

        # Проверяем, ведёт ли КАКОЕ-ЛИБО состояние в группе к Z
        leads_to_z = False
        z_transitions = {}

        for state in group:
            if state in transitions:
                for edge, target in transitions[state].items():
                    if target == 'Z':
                        leads_to_z = True
                        z_transitions[edge] = 'Z'

        # Заменяем состояния в группе
        for state in list(group):  # Используем list() для копии
            if state in transitions:
                transitions = replace.replace_name_state(
                    transitions, state, new_state, protected_states={'Z'}
                )

        # Восстанавливаем переходы к Z, если они были потеряны
        if leads_to_z and new_state in transitions:
            for edge, target in z_transitions.items():
                transitions[new_state][edge] = 'Z'

        # Ищем новые дубликаты
        duplicates = find_duplicate.main_find_duplicate(transitions)

    return transitions




def build_main_dict(graph, start_edges, finish_edges, input_scripts):
    global transitions
    transitions = build_transitions(graph, start_edges, finish_edges, input_scripts)
    print("Стартовый словарь\n", transitions)




    # # Удаляем дубли состояний
    # transitions = replace_pre_aft_duplicate(transitions)
    # print("После замены дубликатов\n", transitions)
    #
    # # Группируем одинаковые переходы
    # same_edges_groups = find_same_edges.same_edges(transitions)
    # for group in same_edges_groups:
    #     new_name = get_new_state_name()
    #     for state in group:
    #         replace.replace_name_state(transitions, state, new_name)
    # print("После объединения одинаковых edges", transitions)

    return transitions
