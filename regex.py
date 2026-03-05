# regex.py
import re

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
        return ""  # Защита от циклов

    visited.add(state)
    transitions = transitions_dict[state]
    sub_expressions = []

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

        # Формируем ветви: label + expr
        branches = [f"{label}{expr}" if expr else label for expr in target_exprs]

        # Выносим общий префикс до объединения
        inner_expr = extract_common_prefix("|".join(branches))

        # Оборачиваем в () только при необходимости
        if "|" in inner_expr:
            if inner_expr.startswith("(") and inner_expr.endswith(")") and is_balanced_and_single_group(inner_expr):
                combined = inner_expr
            else:
                combined = f"({inner_expr})"
        else:
            combined = inner_expr

        sub_expressions.append(combined)

    visited.remove(state)

    # Собираем основное выражение
    if not sub_expressions:
        result = ""
    elif len(sub_expressions) == 1:
        result = sub_expressions[0]
    else:
        result = f"({'|'.join(sub_expressions)})"

    # Удаляем лишние скобки
    result = remove_extra_parentheses(result)

    # Финальная оптимизация: удаляем (A), если A — один блок без |
    result = simplify_final(result)

    memo[state] = result
    return result


def extract_common_prefix(expr):
    import re

    def unparen(s):
        while s.startswith("(") and s.endswith(")"):
            inner = s[1:-1]
            if inner.count("(") == inner.count(")") and inner.count(")") > 0:
                break
            s = inner
        return s

    expr = unparen(expr)
    parts = expr.split("|")
    if len(parts) <= 1:
        return expr

    tokens_list = [re.findall(r'q\d+', part) for part in parts]
    min_len = min(len(t) for t in tokens_list) if tokens_list else 0
    common = []
    for i in range(min_len):
        if all(tokens[i] == tokens_list[0][i] for tokens in tokens_list):
            common.append(tokens_list[0][i])
        else:
            break

    if len(common) == 0:
        return f"({'|'.join(parts)})"

    suffixes = []
    for tokens in tokens_list:
        suffix_tokens = tokens[len(common):]
        suffix = "".join(suffix_tokens)
        suffixes.append(suffix if suffix else "")

    prefix_str = "".join(common)
    if len(set(suffixes)) == 1:
        return prefix_str + suffixes[0]
    else:
        inner = "|".join(suffixes)
        if len(suffixes) > 1:
            inner = f"({inner})"
        return prefix_str + inner


def remove_extra_parentheses(expr):
    changed = True
    while changed:
        changed = False
        # Удаляем (qN) → qN
        new_expr = re.sub(r'\((q\d+)\)', r'\1', expr)
        if new_expr != expr:
            changed = True
            expr = new_expr
            continue

        # Удаляем (A) → A, если A не содержит | на верхнем уровне
        new_expr = remove_single_wrappers(expr)
        if new_expr != expr:
            changed = True
            expr = new_expr

    return expr


def remove_single_wrappers(s):
    if len(s) < 3 or not s.startswith("(") or not s.endswith(")"):
        return s

    depth = 0
    for i, char in enumerate(s):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                if i == len(s) - 1:
                    inner = s[1:-1]
                    if '|' not in get_top_level_parts(inner):
                        return inner
                break
    return s


def is_balanced_and_single_group(s):
    if not s.startswith("(") or not s.endswith(")"):
        return False
    depth = 0
    for i, char in enumerate(s):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return i == len(s) - 1
    return False


def get_top_level_parts(expr):
    parts = []
    current = ""
    depth = 0
    for char in expr:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if char == '|' and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts


def simplify_final(expr):
    """
    Финальная очистка: удаляет лишние скобки вокруг одиночных блоков.
    Например: (q1(q2|q3)) → q1(q2|q3), если это часть альтернативы.
    """
    if not expr or '|' not in expr:
        return expr

    # Разбиваем на части по |, но сохраняем структуру
    parts = get_top_level_parts(expr)
    simplified_parts = []

    for part in parts:
        # Если часть — это (A), и A не содержит |, то убираем скобки
        if (
            part.startswith("(") and
            part.endswith(")") and
            is_balanced_and_single_group(part)
        ):
            inner = part[1:-1]
            if '|' not in get_top_level_parts(inner):
                simplified_parts.append(inner)
            else:
                simplified_parts.append(part)
        else:
            simplified_parts.append(part)

    # Если после упрощения остался один элемент — возвращаем его без скобок
    if len(simplified_parts) == 1:
        return simplified_parts[0]

    # Иначе объединяем с |
    result = "|".join(simplified_parts)

    # Если результат — это (A|B|C), и он единственный, оставляем как есть
    return result
