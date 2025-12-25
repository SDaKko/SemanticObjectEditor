# Файл run_tests.py
# Скрипт для запуска всех тестов

import sys
import os

def main():
    """Запускает все тесты"""
    print("=" * 80)
    print("ЗАПУСК ВСЕХ ТЕСТОВ РЕДАКТОРА СЕМАНТИЧЕСКИХ ОБЪЕКТОВ")
    print("=" * 80)
    
    # Проверка наличия необходимых файлов
    required_files = ['test_regex.py', 'test_integration.py', 'regex.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"\n❌ ОШИБКА: Отсутствуют необходимые файлы: {', '.join(missing_files)}")
        return 1
    
    print("\n✓ Все необходимые файлы найдены")
    
    # Запуск unit-тестов
    print("\n" + "=" * 80)
    print("1. ЗАПУСК UNIT-ТЕСТОВ")
    print("=" * 80)
    try:
        import test_regex
        print("\nЗапуск автоматических тестов...")
        import unittest
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_regex)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\n✓ Все unit-тесты пройдены успешно!")
        else:
            print(f"\n❌ Некоторые тесты не пройдены: {len(result.failures)} ошибок, {len(result.errors)} исключений")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске unit-тестов: {e}")
        return 1
    
    # Запуск интеграционных тестов
    print("\n" + "=" * 80)
    print("2. ЗАПУСК ИНТЕГРАЦИОННЫХ ТЕСТОВ")
    print("=" * 80)
    try:
        import test_integration
        test_integration.test_full_workflow()
        test_integration.test_with_sample_data()
        print("\n✓ Интеграционные тесты выполнены!")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске интеграционных тестов: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 80)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

