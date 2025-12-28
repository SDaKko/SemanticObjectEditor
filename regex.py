# regex.py

def build_regex(state, transitions_dict, visited=None, memo=None):
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}

    if state not in transitions_dict or not transitions_dict[state]:
        return ""

    if state in memo:
        return memo[state]

    if state in visited:
        return ""  # Избегаем циклов

    visited.add(state)
    transitions = transitions_dict[state]

    # Группировка по следующему состоянию
    next_states = {}
    for label, next_state in transitions.items():
        if next_state not in next_states:
            next_states[next_state] = []
        next_states[next_state].append(label)

    sub_expressions = []

    for next_state, labels in next_states.items():
        unique_labels = list(set(labels))
        label_expr = unique_labels[0] if len(unique_labels) == 1 else f"({'|'.join(unique_labels)})"

        if next_state == 'Z':
            sub_expressions.append(label_expr)
        else:
            sub_expr = build_regex(next_state, transitions_dict, visited.copy(), memo)
            if sub_expr:
                combined = f"{label_expr}{sub_expr}"
            else:
                combined = label_expr
            sub_expressions.append(combined)

    visited.remove(state)

    if len(sub_expressions) == 0:
        result = ""
    elif len(sub_expressions) == 1:
        result = sub_expressions[0]
    else:
        result = f"({'|'.join(sub_expressions)})"

    # Упрощение: (q1) → q1
    result = remove_extra_parentheses(result)
    memo[state] = result
    return result


def remove_extra_parentheses(expr):
    import re
    while True:
        # Удаляем (q1) → q1
        new_expr = re.sub(r'\((q\d+)\)', r'\1', expr)
        if new_expr == expr:
            break
        expr = new_expr
    return expr
