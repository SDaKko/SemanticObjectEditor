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
    sub_expressions = []

    # Группируем по наборам следующих состояний
    # Но лучше: для каждого ребра — все его цели
    for label, next_states in transitions.items():
        if not isinstance(next_states, list):
            continue
        target_exprs = []
        for next_state in next_states:
            if next_state == 'Z':
                target_exprs.append("")
            else:
                rec = build_regex(next_state, transitions_dict, visited.copy(), memo)
                target_exprs.append(rec if rec else "")
        # Комбинируем пути через это ребро
        if len(target_exprs) == 1:
            combined = label + target_exprs[0] if target_exprs[0] else label
        else:
            inner = "|".join(f"{label}{expr}" if expr else label for expr in target_exprs)
            combined = f"({inner})"
        sub_expressions.append(combined)

    visited.remove(state)

    if not sub_expressions:
        result = ""
    elif len(sub_expressions) == 1:
        result = sub_expressions[0]
    else:
        result = f"({'|'.join(sub_expressions)})"

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
