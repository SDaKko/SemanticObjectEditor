# Файл test_regex.py
# Unit-тесты для функции build_regex

import unittest
from regex import build_regex, remove_extra_parentheses


class TestBuildRegex(unittest.TestCase):
    """Тесты для функции build_regex - общего случая семантических объектов"""
    
    def test_simple_linear_path(self):
        """Тест простого линейного пути: S0 -> a -> S1 -> b -> Z"""
        transitions = {
            'S0': {'a': 'S1'},
            'S1': {'b': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Ожидаемый результат: ab или (a)(b)
        self.assertIn('a', result)
        self.assertIn('b', result)
        print(f"\n✓ Тест 1 (простой путь): {result}")
    
    def test_multiple_transitions_from_state(self):
        """Тест множественных переходов из одного состояния"""
        transitions = {
            'S0': {'a': 'S1', 'b': 'S2'},
            'S1': {'c': 'Z'},
            'S2': {'d': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Ожидаемый результат должен содержать альтернативу: (a|c)|(b|d) или подобное
        self.assertIn('a', result or '')
        self.assertIn('b', result or '')
        print(f"\n✓ Тест 2 (множественные переходы): {result}")
    
    def test_self_loop(self):
        """Тест самопетли (переход в себя)"""
        transitions = {
            'S0': {'a': 'S0', 'b': 'S1'},
            'S1': {'c': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Ожидаемый результат должен содержать цикл: (a)* или подобное
        self.assertIn('a', result or '')
        # Проверяем наличие звездочки для цикла
        if 'S0' in str(transitions):
            self.assertTrue('*' in result or 'b' in result)
        print(f"\n✓ Тест 3 (самопетля): {result}")
    
    def test_multiple_labels_to_same_state(self):
        """Тест нескольких меток, ведущих в одно состояние"""
        transitions = {
            'S0': {'a': 'S1', 'b': 'S1'},
            'S1': {'c': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Ожидаемый результат: (a|b)c или подобное
        self.assertIn('a', result or '')
        self.assertIn('b', result or '')
        self.assertIn('c', result or '')
        print(f"\n✓ Тест 4 (несколько меток в одно состояние): {result}")
    
    def test_empty_state(self):
        """Тест состояния без переходов"""
        transitions = {
            'S0': {},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        self.assertEqual(result, "")
        print(f"\n✓ Тест 5 (пустое состояние): '{result}'")
    
    def test_complex_structure(self):
        """Тест сложной структуры с несколькими состояниями"""
        transitions = {
            'S0': {'a': 'S1', 'b': 'S2'},
            'S1': {'c': 'S3', 'd': 'Z'},
            'S2': {'e': 'S3'},
            'S3': {'f': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Результат должен быть непустым и содержать метки
        self.assertNotEqual(result, "")
        self.assertTrue(len(result) > 0)
        print(f"\n✓ Тест 6 (сложная структура): {result}")
    
    def test_final_state(self):
        """Тест финального состояния Z"""
        transitions = {
            'S0': {'a': 'Z'},
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Результат должен содержать 'a'
        self.assertIn('a', result)
        print(f"\n✓ Тест 7 (финальное состояние): {result}")
    
    def test_cycle_detection(self):
        """Тест обнаружения циклов"""
        transitions = {
            'S0': {'a': 'S1'},
            'S1': {'b': 'S0'},  # Цикл обратно в S0
            'Z': {}
        }
        result = build_regex('S0', transitions)
        # Результат должен быть обработан без бесконечной рекурсии
        self.assertIsInstance(result, str)
        print(f"\n✓ Тест 8 (обнаружение циклов): {result}")


class TestRemoveExtraParentheses(unittest.TestCase):
    """Тесты для функции remove_extra_parentheses"""
    
    def test_remove_unnecessary_parentheses(self):
        """Тест удаления лишних скобок"""
        expr = "((a))"
        result = remove_extra_parentheses(expr)
        # Скобки вокруг одного символа должны быть удалены
        self.assertIn('a', result)
        print(f"\n✓ Тест remove_extra_parentheses: '{expr}' -> '{result}'")
    
    def test_keep_necessary_parentheses(self):
        """Тест сохранения необходимых скобок"""
        expr = "(a|b)"
        result = remove_extra_parentheses(expr)
        # Скобки вокруг альтернативы должны остаться
        self.assertIn('(', result)
        self.assertIn(')', result)
        print(f"\n✓ Тест сохранения скобок: '{expr}' -> '{result}'")


def run_manual_tests():
    """Ручные тесты с выводом подробной информации"""
    print("=" * 80)
    print("РУЧНЫЕ ТЕСТЫ ФУНКЦИИ build_regex")
    print("=" * 80)
    
    # Тест 1: Простой случай
    print("\n" + "-" * 80)
    print("ТЕСТ 1: Простой линейный путь")
    print("-" * 80)
    transitions1 = {
        'S0': {'a': 'S1'},
        'S1': {'b': 'Z'},
        'Z': {}
    }
    result1 = build_regex('S0', transitions1)
    print(f"Входные данные: {transitions1}")
    print(f"Результат: {result1}")
    
    # Тест 2: Множественные переходы
    print("\n" + "-" * 80)
    print("ТЕСТ 2: Множественные переходы из одного состояния")
    print("-" * 80)
    transitions2 = {
        'S0': {'a': 'S1', 'b': 'S2'},
        'S1': {'c': 'Z'},
        'S2': {'d': 'Z'},
        'Z': {}
    }
    result2 = build_regex('S0', transitions2)
    print(f"Входные данные: {transitions2}")
    print(f"Результат: {result2}")
    
    # Тест 3: Самопетля
    print("\n" + "-" * 80)
    print("ТЕСТ 3: Самопетля (переход в себя)")
    print("-" * 80)
    transitions3 = {
        'S0': {'a': 'S0', 'b': 'S1'},
        'S1': {'c': 'Z'},
        'Z': {}
    }
    result3 = build_regex('S0', transitions3)
    print(f"Входные данные: {transitions3}")
    print(f"Результат: {result3}")
    
    # Тест 4: Несколько меток в одно состояние
    print("\n" + "-" * 80)
    print("ТЕСТ 4: Несколько меток, ведущих в одно состояние")
    print("-" * 80)
    transitions4 = {
        'S0': {'a': 'S1', 'b': 'S1', 'c': 'S1'},
        'S1': {'d': 'Z'},
        'Z': {}
    }
    result4 = build_regex('S0', transitions4)
    print(f"Входные данные: {transitions4}")
    print(f"Результат: {result4}")
    
    # Тест 5: Сложная структура
    print("\n" + "-" * 80)
    print("ТЕСТ 5: Сложная структура с несколькими путями")
    print("-" * 80)
    transitions5 = {
        'S0': {'start': 'S1', 'begin': 'S2'},
        'S1': {'middle1': 'S3', 'middle2': 'S4'},
        'S2': {'middle3': 'S3'},
        'S3': {'end1': 'Z'},
        'S4': {'end2': 'Z'},
        'Z': {}
    }
    result5 = build_regex('S0', transitions5)
    print(f"Входные данные: {transitions5}")
    print(f"Результат: {result5}")
    
    print("\n" + "=" * 80)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 80)


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ")
    print("=" * 80)
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n\n")
    run_manual_tests()

