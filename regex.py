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

    # Для каждого исходящего ребра собираем варианты
    branches = []

    for label, next_states in transitions.items():
        if not isinstance(next_states, list):
            continue

        # Для каждого следующего состояния строим выражение
        next_exprs = []
        for next_state in next_states:
            if next_state == 'Z':
                next_exprs.append("")
            else:
                rec = build_regex(next_state, transitions_dict, visited.copy(), memo)
                next_exprs.append(rec if rec else "")

        # Формируем выражение для текущего ребра
        if len(next_exprs) == 1:
            if next_exprs[0]:
                branch = f"{label}{next_exprs[0]}"
            else:
                branch = label
        else:
            # Несколько вариантов после этого ребра
            non_empty = [expr for expr in next_exprs if expr != ""]
            if not non_empty:
                branch = label
            elif len(non_empty) == 1:
                branch = f"{label}{non_empty[0]}"
            else:
                inner = "|".join(non_empty)
                branch = f"{label}({inner})"

        branches.append(branch)

    visited.remove(state)

    # Объединяем все ветви
    if not branches:
        result = ""
    elif len(branches) == 1:
        result = branches[0]
    else:
        # Объединяем все ветви через | с поиском общего префикса
        result = merge_branches_with_common_prefix(branches)

    memo[state] = result
    return result


def merge_branches_with_common_prefix(branches):
    """Объединяет ветви с общим префиксом для более компактного выражения"""
    if len(branches) <= 1:
        return branches[0] if branches else ""

    # Ищем общий префикс
    common_prefix = find_common_prefix(branches)

    if common_prefix:
        # Проверяем, что общий префикс - это целые токены qN
        # Чтобы не разрывать q1 и q23 на q и 1|23
        if common_prefix.endswith('q'):
            # Если общий префикс заканчивается на 'q', то это не полный токен
            # Нужно найти общий префикс по полным токенам
            common_prefix = find_common_token_prefix(branches)

        if common_prefix:
            # Разделяем ветви на префикс и суффиксы
            suffixes = []
            for branch in branches:
                if branch.startswith(common_prefix):
                    suffix = branch[len(common_prefix):]
                    suffixes.append(suffix if suffix else "")
                else:
                    suffixes.append(branch)

            # Если все ветви имеют общий префикс
            if all(b.startswith(common_prefix) for b in branches):
                # Рекурсивно объединяем суффиксы
                suffixes_merged = merge_branches_with_common_prefix(suffixes)
                if suffixes_merged and "|" in suffixes_merged:
                    return f"{common_prefix}({suffixes_merged})"
                else:
                    return f"{common_prefix}{suffixes_merged}"

    # Если нет общего префикса, объединяем через |
    if len(branches) > 1:
        # Проверяем, не являются ли все ветви простыми токенами
        all_simple = all(re.match(r'^q\d+$', b) for b in branches)
        if all_simple:
            return f"({'|'.join(branches)})"

        # Для сложных ветвей
        return f"({'|'.join(branches)})"

    return branches[0]


def find_common_token_prefix(strings):
    """Находит общий префикс по полным токенам qN"""
    if not strings:
        return ""

    # Разбиваем каждую строку на токены qN
    tokenized = []
    for s in strings:
        tokens = re.findall(r'q\d+|[^q]', s)
        tokenized.append(tokens)

    # Ищем общий префикс из токенов
    common_tokens = []
    min_len = min(len(t) for t in tokenized)

    for i in range(min_len):
        if all(t[i] == tokenized[0][i] for t in tokenized):
            common_tokens.append(tokenized[0][i])
        else:
            break

    if common_tokens:
        return ''.join(common_tokens)

    return ""


def find_common_prefix(strings):
    """Находит общий префикс для всех строк"""
    if not strings:
        return ""

    # Находим наименьшую строку для ограничения
    min_len = min(len(s) for s in strings)

    # Ищем общий префикс
    prefix = ""
    for i in range(min_len):
        char = strings[0][i]
        if all(s[i] == char for s in strings):
            prefix += char
        else:
            break

    return prefix


def extract_common_prefix(expr):
    """Извлекает общий префикс из выражения с альтернативами"""
    if not expr or '|' not in expr:
        return expr

    # Убираем внешние скобки
    while expr.startswith("(") and expr.endswith(")"):
        inner = expr[1:-1]
        if inner.count("(") == inner.count(")") and inner.count(")") > 0:
            break
        expr = inner

    parts = expr.split("|")

    # Ищем общий префикс
    common_prefix = find_common_prefix(parts)

    if common_prefix:
        suffixes = [p[len(common_prefix):] for p in parts]
        # Убираем пустые суффиксы для более компактного вида
        suffixes = [s if s else "" for s in suffixes]

        if all(s == "" for s in suffixes):
            return common_prefix

        if len(set(suffixes)) == 1 and suffixes[0]:
            return common_prefix + suffixes[0]

        # Рекурсивно обрабатываем суффиксы
        inner = merge_branches_with_common_prefix(suffixes)
        if inner and "|" in inner:
            return f"{common_prefix}({inner})"
        else:
            return f"{common_prefix}{inner}"

    # Если нет общего префикса, возвращаем как есть
    if len(parts) == 1:
        return parts[0]
    return f"({expr})" if expr.startswith("(") else f"({expr})"


def remove_extra_parentheses(expr):
    """Удаляет лишние скобки из выражения"""
    changed = True
    while changed:
        changed = False

        # Удаляем (qN) → qN
        new_expr = re.sub(r'\(q\d+\)', r'\1', expr)
        if new_expr != expr:
            changed = True
            expr = new_expr
            continue

        # Удаляем (A) → A, если A не содержит | на верхнем уровне
        if expr.startswith("(") and expr.endswith(")"):
            inner = expr[1:-1]
            if '|' not in inner or (inner.count("(") == inner.count(")") and inner.count("(") == 0):
                expr = inner
                changed = True
                continue

        # Удаляем (A|B) если это единственная альтернатива
        if expr.startswith("(") and expr.endswith(")") and "|" in expr:
            inner = expr[1:-1]
            # Проверяем, что скобки сбалансированы
            if inner.count("(") == inner.count(")"):
                expr = inner
                changed = True

    return expr


def simplify_final(expr):
    """Финальная очистка выражения"""
    # Удаляем лишние скобки вокруг одиночных блоков
    while expr.startswith("(") and expr.endswith(")"):
        inner = expr[1:-1]
        if "|" in inner:
            # Проверяем, не являются ли скобки необходимыми
            if inner.count("(") == inner.count(")"):
                expr = inner
            else:
                break
        else:
            expr = inner

    # Упрощаем (A|B) в A|B
    if expr.startswith("(") and expr.endswith(")") and "|" in expr:
        inner = expr[1:-1]
        if inner.count("(") == inner.count(")"):
            expr = inner

    return expr


def is_balanced_and_single_group(s):
    """Проверяет, является ли строка одной сбалансированной группой скобок"""
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
    """Разбивает выражение на части верхнего уровня по |"""
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