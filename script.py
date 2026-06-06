# Файл script.py
import re
from typing import List, Tuple, Any, Dict

try:
    import pymorphy3

    morph = pymorphy3.MorphAnalyzer()
    LEMMATIZATION_AVAILABLE = True
except ImportError:
    print("Предупреждение: pymorphy3 не установлен. Лемматизация отключена.")
    print("Установите: pip install pymorphy3")
    LEMMATIZATION_AVAILABLE = False
    morph = None

# Кэш для хранения уже обработанных слов
_lemma_cache: Dict[str, str] = {}


def lemmatize_word(word: str) -> str:
    """Лемматизация одного слова с кэшированием"""
    if not LEMMATIZATION_AVAILABLE or morph is None:
        return word.lower()

    if word in _lemma_cache:
        return _lemma_cache[word]

    try:
        lemma = morph.parse(word)[0].normal_form
        _lemma_cache[word] = lemma
        return lemma
    except Exception:
        _lemma_cache[word] = word.lower()
        return word.lower()


def lemmatize_text(text: str) -> str:
    """Лемматизация текста - приведение слов к нормальной форме."""
    if not LEMMATIZATION_AVAILABLE or morph is None:
        return text.lower()

    words = re.findall(r'\b\w+\b', text.lower())
    lemmatized_words = []

    for word in words:
        lemma = lemmatize_word(word)
        lemmatized_words.append(lemma)

    return ' '.join(lemmatized_words)


def remove_curator_prefix(text: str) -> str:
    """
    Удаляет префикс "Куратор:" из текста.
    Пример: "Куратор: Привет!" -> "Привет!"
    """
    # Удаляем "Куратор:" в начале строки (с возможными пробелами)
    text = re.sub(r'^Куратор:\s*', '', text, flags=re.IGNORECASE)
    # Также удаляем "Куратор:" после знаков препинания
    text = re.sub(r'[.!?]\s*Куратор:\s*', '. ', text, flags=re.IGNORECASE)
    return text.strip()

def tokenize(text):
    """Разбивает текст на предложения"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def extract_scripts(text, character, threshold=0.6, use_lemmatization=True):
    """
    Извлекает сценарий из текста.
    """
    sentences = tokenize(text)
    sequence = []
    results = []  # Для хранения деталей (используется только если verbose=True)

    # Предварительно лемматизируем шаблоны для ускорения
    lemmatized_patterns = {}
    if use_lemmatization and LEMMATIZATION_AVAILABLE:
        for key, pattern in character.items():
            lemmatized_patterns[key] = lemmatize_text(pattern)

    for sent_idx, sentence in enumerate(sentences, 1):
        best_score = 0.0
        best_key = None

        # Удаляем "Куратор:" из предложения для отображения в отчете
        clean_sentence_for_display = remove_curator_prefix(sentence)

        # Лемматизируем предложение (с удаленным "Куратор:")
        sentence_for_compare = remove_curator_prefix(sentence)
        lemma_sentence = lemmatize_text(
            sentence_for_compare) if use_lemmatization and LEMMATIZATION_AVAILABLE else sentence_for_compare.lower()

        for key, pattern in character.items():
            # Для шаблона тоже удаляем "Куратор:" на всякий случай
            pattern_for_compare = remove_curator_prefix(pattern)

            if use_lemmatization and LEMMATIZATION_AVAILABLE:
                pattern_text = lemmatized_patterns[key]
                sentence_text = lemma_sentence
            else:
                pattern_text = pattern_for_compare.lower()
                sentence_text = sentence_for_compare.lower()

            # Сравниваем
            tokens1 = set(pattern_text.split())
            tokens2 = set(sentence_text.split())

            if len(tokens1) == 0 or len(tokens2) == 0:
                curr_sem_prox = 0.0
            else:
                intersection = tokens1.intersection(tokens2)
                union = tokens1.union(tokens2)
                curr_sem_prox = round((len(intersection) / len(union)), 2)

            if curr_sem_prox > best_score:
                best_score = curr_sem_prox
                best_key = key

        if best_score >= threshold:
            sequence.append(best_key)

        results.append({
            'index': sent_idx,
            'sentence': sentence,
            'clean_sentence': clean_sentence_for_display,  # Оригинальное предложение без "Куратор:"
            'best_key': best_key,
            'best_score': best_score,
            'passed': best_score >= threshold
        })

    return sequence

def build_dict_char(scripts):
    """Построение словаря характеристик"""
    unique_elements = set()
    for script in scripts:
        unique_elements.update(script)

    sequences = {elem: [] for elem in unique_elements}

    for i in range(len(scripts)):
        for j in range(len(scripts[i]) - 1):
            primary = scripts[i][j]
            secondary = scripts[i][j + 1]
            sequences[primary].append(secondary)

    return sequences


def get_start_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    """Получение первых элементов из каждого списка"""
    start_elements = []
    for lst in input_tuple:
        if lst:
            if lst[0] not in start_elements:
                start_elements.append(lst[0])
    return start_elements


def get_finish_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    """Получение последних элементов из каждого списка"""
    finish_elements = []
    for lst in input_tuple:
        if lst:
            if lst[-1] not in finish_elements:
                finish_elements.append(lst[-1])
    return finish_elements