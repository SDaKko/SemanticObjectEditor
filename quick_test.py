# Файл quick_test.py
# Быстрый тест функции build_regex

from regex import build_regex

print("=" * 80)
print("БЫСТРЫЙ ТЕСТ ФУНКЦИИ build_regex")
print("=" * 80)

# Тест 1: Простой линейный путь
print("\nТест 1: Простой путь S0 -> a -> S1 -> b -> Z")
transitions1 = {
    'S0': {'a': 'S1'},
    'S1': {'b': 'Z'},
    'Z': {}
}
result1 = build_regex('S0', transitions1)
print(f"Результат: {result1}")
print(f"✓ Тест пройден" if result1 else "❌ Тест не пройден")

# Тест 2: Множественные переходы
print("\nТест 2: Множественные переходы из S0")
transitions2 = {
    'S0': {'a': 'S1', 'b': 'S2'},
    'S1': {'c': 'Z'},
    'S2': {'d': 'Z'},
    'Z': {}
}
result2 = build_regex('S0', transitions2)
print(f"Результат: {result2}")
print(f"✓ Тест пройден" if result2 and ('a' in result2 or 'b' in result2) else "❌ Тест не пройден")

# Тест 3: Самопетля
print("\nТест 3: Самопетля (переход в себя)")
transitions3 = {
    'S0': {'a': 'S0', 'b': 'S1'},
    'S1': {'c': 'Z'},
    'Z': {}
}
result3 = build_regex('S0', transitions3)
print(f"Результат: {result3}")
print(f"✓ Тест пройден" if result3 else "❌ Тест не пройден")

# Тест 4: Несколько меток в одно состояние
print("\nТест 4: Несколько меток в одно состояние")
transitions4 = {
    'S0': {'a': 'S1', 'b': 'S1', 'c': 'S1'},
    'S1': {'d': 'Z'},
    'Z': {}
}
result4 = build_regex('S0', transitions4)
print(f"Результат: {result4}")
print(f"✓ Тест пройден" if result4 and 'a' in result4 and 'b' in result4 else "❌ Тест не пройден")

print("\n" + "=" * 80)
print("БЫСТРЫЙ ТЕСТ ЗАВЕРШЕН")
print("=" * 80)
print("\nДля более подробного тестирования запустите: python test_regex.py")
print("Для полного тестирования запустите: python run_tests.py")

