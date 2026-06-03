# regex.py

import re
def build_regex(state, transitions_dict, visited=None, memo=None, depth=0):
    """
    Строит регулярное выражение из графа состояний.
    transitions_dict должен быть УЖЕ ОПТИМИЗИРОВАН!
    """

    if visited is None:
        visited = set()
    if memo is None:
        memo = {}

    # Проверка существования состояния
    if state not in transitions_dict:
        return ""

    if not transitions_dict[state]:
        return ""

    if state in memo:
        return memo[state]

    if state in visited:
        return ""  # Защита от циклов

    visited.add(state)
    transitions = transitions_dict[state]

    indent = "  " * depth

    branches = []

    for label, next_states in transitions.items():
        if not isinstance(next_states, list):
            next_states = [next_states]

        # Разделяем на завершающие и продолжающие переходы
        final_transitions = []
        continue_transitions = []

        for next_state in next_states:
            if next_state == 'Z':
                final_transitions.append(None)
            else:
                rec = build_regex(next_state, transitions_dict, visited.copy(), memo, depth + 1)
                if rec:
                    continue_transitions.append(rec)
                else:
                    continue_transitions.append("")

        has_final = len(final_transitions) > 0
        has_continue = len(continue_transitions) > 0 and any(c for c in continue_transitions if c)

        # Формируем выражение
        if has_final and has_continue:
            unique_continues = list(dict.fromkeys([c for c in continue_transitions if c]))
            if len(unique_continues) == 1:
                branch = f"{label}({unique_continues[0]}|)"
            else:
                inner = "|".join(unique_continues)
                branch = f"{label}({inner}|)"
        elif has_final and not has_continue:
            branch = label
        elif not has_final and len(continue_transitions) == 1:
            branch = f"{label}{continue_transitions[0]}"
        elif not has_final and len(continue_transitions) > 1:
            unique_continues = list(dict.fromkeys([c for c in continue_transitions if c]))
            inner = "|".join(unique_continues)
            branch = f"{label}({inner})"
        else:
            branch = label

        branches.append(branch)

    visited.remove(state)

    # Объединяем ветви
    if not branches:
        result = ""
    elif len(branches) == 1:
        result = branches[0]
    else:
        result = merge_branches(branches)

    result = simplify_expression(result)

    memo[state] = result
    return result

def merge_branches(branches):
    """Объединяет ветви с общим префиксом"""
    if len(branches) <= 1:
        return branches[0] if branches else ""

    # Ищем общий префикс на уровне токенов
    common_prefix = find_common_prefix(branches)

    if common_prefix:
        suffixes = []
        all_have_prefix = True

        for branch in branches:
            if branch.startswith(common_prefix):
                suffix = branch[len(common_prefix):]
                suffixes.append(suffix if suffix else "")
            else:
                all_have_prefix = False
                suffixes.append(branch)

        if all_have_prefix:
            suffixes_merged = merge_branches(suffixes)
            if suffixes_merged and "|" in suffixes_merged:
                return f"{common_prefix}({suffixes_merged})"
            elif suffixes_merged:
                return f"{common_prefix}{suffixes_merged}"
            else:
                return common_prefix

    # Если нет общего префикса, объединяем через |
    unique_branches = list(dict.fromkeys(branches))
    if len(unique_branches) == 1:
        return unique_branches[0]

    all_simple = all(re.match(r'^q\d+$', b) for b in unique_branches)
    if all_simple:
        return f"({'|'.join(unique_branches)})"

    return f"({'|'.join(unique_branches)})"


def find_common_prefix(strings):
    """
    Находит общий префикс для всех строк на уровне токенов.
    """
    if not strings:
        return ""

    if len(strings) == 1:
        return strings[0]

    # Разбиваем каждую строку на токены
    tokenized = []
    for s in strings:
        tokens = re.findall(r'q\d+|\(|\)|\|', s)
        tokenized.append(tokens)

    # Ищем общий префикс среди токенов
    common_tokens = []
    min_len = min(len(t) for t in tokenized)

    for i in range(min_len):
        current_token = tokenized[0][i]
        if all(t[i] == current_token for t in tokenized):
            common_tokens.append(current_token)
        else:
            break

    # Склеиваем токены обратно в строку
    return ''.join(common_tokens)


def simplify_expression(expr):
    """Упрощает регулярное выражение"""
    if not expr:
        return expr

    # (qN) -> qN
    expr = re.sub(r'\(q(\d+)\)', r'q\1', expr)

    # Удаляем пустые группы ()
    expr = re.sub(r'\(\)', '', expr)

    # Удаляем двойные скобки
    changed = True
    while changed:
        changed = False
        new_expr = re.sub(r'\(\(([^()]+)\)\)', r'(\1)', expr)
        if new_expr != expr:
            expr = new_expr
            changed = True

    # Удаляем внешние скобки, если всё выражение в них
    if expr.startswith('(') and expr.endswith(')'):
        expr = expr[1:-1]

    return expr