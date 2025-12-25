# Файл regex.py

import re

def build_regex(state, transitions_dict, visited=None, memo=None):
    """
    Строит регулярное выражение для общего случая семантических объектов.
    Использует общий алгоритм преобразования конечного автомата в регулярное выражение.
    
    Args:
        state: Текущее состояние автомата
        transitions_dict: Словарь переходов {состояние: {метка: следующее_состояние}}
        visited: Множество посещенных состояний в текущем пути для обнаружения циклов
        memo: Словарь для мемоизации результатов (предотвращает повторные вычисления)
    
    Returns:
        Регулярное выражение в стандартном формате
    """
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}
    
    # Проверяем, есть ли переходы из этого состояния
    if state not in transitions_dict or not transitions_dict[state]:
        print(f"Нет переходов из состояния '{state}', возвращаем пустую строку.")
        return ""
    
    # Проверяем мемоизацию (но не используем для состояний в цикле)
    if state not in visited and state in memo:
        print(f"Используем мемоизированный результат для состояния '{state}'")
        return memo[state]
    
    # Предотвращаем бесконечную рекурсию при циклах
    # Если состояние уже в пути, это означает цикл
    if state in visited:
        print(f"Обнаружен цикл в состоянии '{state}', возвращаем пустую строку для предотвращения рекурсии.")
        # Для циклов возвращаем пустую строку, цикл будет обработан на уровне выше
        return ""
    
    # Добавляем текущее состояние в посещенные
    visited.add(state)
    
    transitions = transitions_dict[state]
    # Словарь для группировки переходов по следующему состоянию
    # {следующее_состояние: [список_меток]}
    next_states = {}
    
    # Группируем переходы по следующему состоянию
    for label, next_state in transitions.items():
        if next_state not in next_states:
            next_states[next_state] = []
        next_states[next_state].append(label)
    
    # Список для хранения подвыражений для каждого следующего состояния
    sub_expressions = []
    
    # Обрабатываем все следующие состояния
    for next_state, labels in next_states.items():
        print(f"Обрабатываем переходы в состояние '{next_state}' с метками {labels}")
        
        # Убираем дубликаты меток
        unique_labels = list(set(labels))
        
        # Формируем выражение для меток перехода
        if len(unique_labels) == 1:
            label_expr = unique_labels[0]
        else:
            # Объединяем несколько меток через |
            label_expr = f"({'|'.join(unique_labels)})"
        
        # Проверка на переход в себя (самопетля)
        if next_state == state:
            # Для самопетли используем стандартный синтаксис регулярных выражений
            # (a|b)* означает повторение a или b ноль или более раз
            loop_expr = f"({label_expr})*"
            print(f"Переход в само себя, добавляем цикл: {loop_expr}")
            sub_expressions.append(loop_expr)
        else:
            # Рекурсивно строим регулярное выражение для следующего состояния
            sub_expr = build_regex(next_state, transitions_dict, visited.copy(), memo)
            
            # Объединяем метку перехода с выражением следующего состояния
            if sub_expr:
                combined_expr = f"{label_expr}{sub_expr}"
            else:
                # Если следующее состояние не имеет переходов или это цикл, просто метка
                combined_expr = label_expr
            
            print(f"Собранное выражение для перехода в состояние '{next_state}': '{combined_expr}'")
            sub_expressions.append(combined_expr)
    
    # Удаляем текущее состояние из посещенных перед возвратом
    visited.remove(state)
    
    # Объединяем все подвыражения через альтернативу |
    if len(sub_expressions) == 0:
        final_expr = ""
    elif len(sub_expressions) == 1:
        final_expr = sub_expressions[0]
    else:
        # Объединяем все альтернативы через |
        # Используем скобки для группировки
        final_expr = f"({'|'.join(sub_expressions)})"
    
    # Сохраняем результат в мемоизацию
    memo[state] = final_expr
    
    print(f"Возвращаем выражение для состояния '{state}': '{final_expr}'")
    cleaned_expression = remove_extra_parentheses(final_expr)
    return cleaned_expression

def find_inner_expressions(expr):
    """ Находит все подвыражения с вертикальной чертой, включая вложенные. """
    stack = []
    inner_expressions = []
    for i, char in enumerate(expr):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                if '|' in expr[start:i]:  # Проверяем наличие вертикальной черты
                    inner_expressions.append(expr[start + 1:i])  # Добавляем содержимое без скобок
    return inner_expressions

def longest_common_suffix(str1, str2):
    """Находит общую подстроку максимальной длины, расположенную в конце двух строк."""
    print(str1, str2)
    # Длина двух строк
    len1, len2 = len(str1), len(str2)

    # Устанавливаем начальную длину общей подстроки
    common_length = 0

    # Сравниваем строки с конца до начала
    while common_length < len1 and common_length < len2 and str1[len1 - 1 - common_length] == str2[len2 - 1 - common_length]:
        common_length += 1

    common_suffix = str1[len1 - common_length:] if common_length > 0 else ""

    # Условие, чтобы суффикс не совпадал с одной из строк
    if common_suffix == str1 or common_suffix == str2:
        common_length = max(0, common_length - 2)  # Убираем 2 символа, если это возможно
        common_suffix = str1[len1 - common_length:] if common_length > 0 else ""

    print(common_suffix)
    return common_suffix

def remove_duplicate_inner_expressions(inner_expressions):
    seen = set()  # Множество для отслеживания уникальных подвыражений
    unique_expressions = []  # Список для хранения уникальных выражений
    for exp in inner_expressions:
        if exp not in seen:
            seen.add(exp)
            unique_expressions.append(exp)
    return unique_expressions

def remove_unpaired_parentheses(s):
    result = []
    last_close_index = -1  # Индекс последней закрывающей скобки

    for index, char in enumerate(s):
        if char == '(':
            # Если встречаем открывающую скобку, добавляем её в результат
            result.append(char)
        elif char == ')':
            # Если встречаем закрывающую скобку, закрываем
            if result:
                result.append(char)  # Добавляем закрывающую скобку, только если есть открывающая
                last_close_index = index  # Запоминаем индекс закрывающей скобки
            else:
                continue  # Пропускаем, если нет соответствующей открывающей скобки
        else:
            # Добавляем другие символы в результат
            result.append(char)

    # Удаляем все символы до последней закрывающей скобки и её саму:
    if last_close_index != -1:
        final_result = ''.join(result).rstrip()[:last_close_index]  # Создаем строку вплоть до закрывающей скобки
        return final_result

    return ''.join(result)  # Если не было ни одной закрывающей скобки, просто возвращаем результат.

def normalize_expression(expr):
    """ Нормализует регулярное выражение, вынося дублирующиеся завершающие части. """
    while True:
        print("НОВАЯ ИТТЕРАЦИЯ")

        inner = remove_duplicate_inner_expressions(find_inner_expressions(expr))

        if not inner:
            break  # Если нет подвыражений, выходим из цикла

        changed = False

        for i in range(len(inner)):
            print("Подвыражение", inner[i], expr)
            parts = inner[i].split('|')
            print("parts", parts[0], parts[1])

            common_suffix = longest_common_suffix(parts[0], parts[1])
            common_suffix = remove_unpaired_parentheses(common_suffix)
            print("Общая завершающая", common_suffix)

            if common_suffix:  # Если есть общие завершающие части
                new_parts = []
                for part in parts:
                    print("part:", part)
                    # Убираем общую завершающую часть из каждого подвыражения
                    new_part = part.removesuffix(common_suffix)
                    new_parts.append(new_part)
                print("new_parts:", new_parts)
                # Создаём новое подвыражение с общей частью
                new_inner = f"({'I'.join(new_parts)}){common_suffix}"
                print(new_inner)

                if i != len(inner):
                    j = i + 1
                    for j in range(len(inner)):
                        old_string = "(" + inner[i] + ")"
                        inner[j] = inner[j].replace(old_string, new_inner)

                # Обновляем основное выражение, заменяем только найденное
                expr = expr.replace(f"({inner[i]})", new_inner)
                print("expr", expr)
                # changed = True

            print("\n")

        if not changed:
            break

        print("\n\n\n")

    return expr.replace("I", "|")

def remove_extra_parentheses(expression):
    stack = []
    result = []
    skip_indices = set()  # Для хранения индексов, которые нужно пропустить

    for i, char in enumerate(expression):
        if char == '(':
            stack.append(len(result))  # Сохраняем текущую позицию в результат
            result.append(char)
        elif char == ')':
            if stack:
                start_index = stack.pop()  # Получаем позицию открывающей скобки
                # Проверяем содержимое между скобками
                content = ''.join(result[start_index + 1:])  # Содержимое между скобками
                if '|' in content:  # Если есть '|' в содержимом
                    result.append(char)  # Оставляем скобки
                else:
                    skip_indices.add(start_index)  # Запоминаем, что нужно пропустить
                    result.append('')  # Вместо закрывающей скобки добавляем пустую строку
            else:
                result.append(char)  # Закрывающая скобка без соответствующей открывающей
        else:
            result.append(char)  # Добавляем другие символы

    # Удаляем элементы по индексам, которые были отмечены для пропуска
    final_result = []
    for i in range(len(result)):
        if i not in skip_indices:
            if result[i]:  # Добавляем только непустые элементы
                final_result.append(result[i])

    return ''.join(final_result)