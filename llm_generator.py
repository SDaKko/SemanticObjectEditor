# llm_generator.py
import uuid

import requests
import base64
import os
from dotenv import load_dotenv
from typing import Literal

# Загружаем переменные окружения
load_dotenv()


class LLMGenerator:
    def __init__(self):
        """
        Инициализация без токена — он будет получен автоматически.
        """
        self.token = None
        self.client_id = os.getenv("GIGACHAT_CLIENT_ID")
        self.client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Не найдены GIGACHAT_CLIENT_ID или GIGACHAT_CLIENT_SECRET в .env")

        self.get_token()  # Автоматически получаем токен при создании объекта

    def get_token(self) -> bool:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        auth_str = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),  # ✅ ФИКС: генерируем уникальный UUID
            "Authorization": f"Basic {encoded_auth}"
        }

        payload = {
            "scope": "GIGACHAT_API_PERS"
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                data=payload,
                verify=False,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                print("✅ Токен успешно получен!")
                return True
            else:
                print(f"[Ошибка получения токена] {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"[Ошибка подключения]: {e}")
            return False

    def generate(self, prompt: str, temperature=0.8, max_tokens=600) -> str:
        """
        Генерация текста через GigaChat API.
        """
        url = "https://gigachat.devices.sberbank.ru:443/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "RqUID": str(uuid.uuid4())
        }

        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                verify=False  # ⚠️ Только для теста!
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"[Ошибка {response.status_code}]: {response.text}"
        except Exception as e:
            return f"[Ошибка подключения]: {e}"

    def generate_by_style(self, style: str, length: str = "средний") -> str:
        """
        Генерирует текст по заданному стилю.
        """
        styles = {
            "манипулятивный": (
                "Один из собеседников — проводник в психологической игре. "
                "Он говорит коротко, жёстко, с элементами давления и одобрения. "
                "Он использует фразы: 'Слабые здесь не задерживаются', 'Ты двигаешься в правильном направлении', 'Подумай, зачем ты вообще живёшь'."
            ),
            "терапевтический": (
                "Один из собеседников — терапевт. Он говорит мягко, поддерживающе, он задаёт вопросы. "
                "Фокус на осознании: 'Что тебя тревожит?', 'Хочешь изменить свою жизнь?', 'Ты нужен мне, чтобы пройти это'."
            ),
            "загадочный": (
                "Один из собеседников — лидер закрытого сообщества. Он говорит с ощущением тайны, контроля, избранности. "
                "Фразы: 'Я знаю, где ты, и слежу за тобой', 'Назад пути нет', 'Ты почти у цели'."
            ),
            "провокационный": (
                "Один из собеседников провоцирует на действия. Он говорит дерзко, вызывающе. "
                "Пример: 'Если не сделаешь — я найду тебя', 'Сделай что-то необычное', 'Страшно? Это часть пути'."
            )
        }

        base_prompt = styles.get(style, styles["манипулятивный"])
        length_hint = {
            "короткий": "3–4 пар реплик",
            "средний": "5–7 пар реплик",
            "длинный": "8–10 пар реплик"
        }.get(length, "5–7 пар")

        full_prompt = f"""
        {base_prompt}
        
        Напиши диалоговый фрагмент длиной {length_hint}.
        Участвуют два человека: "Куратор" и "Игрок"
        Пиши перед репликами, от кого они (от "Куратора" или от "Игрока", после атора реплик ставь двоеточие)
        Напиши фрагмент текста, представляющий собой мой диалог с загадочным незнакомцем в заданном стиле. 
        Действие происходит в социальной сети.
        Стиль оформления (строго):
        1. Пиши текст единым сплошным абзацем без переносов строк, списков и тире.
        2. Используй формат коротких, обрывистых фраз, где мои реплики и ответы собеседника чередуются.
        3. Не используй кавычки, двоеточия и жирный шрифт. Предложения должны просто следовать друг за другом.
        4. Повествование должно идти от первого лица.
        
        Запрещено писать незаконченные фразы.
        
        Пример темпа: Привет, у тебя есть данные? Да, но это опасно. Я готов рискнуть.
        Тогда иди к заброшенному дому. Понял, уже выхожу.
"""

        return self.generate(full_prompt)

    def generate_by_example(self, example_text: str, length: str = "средний") -> str:
        """
        Генерирует новый текст в стиле примера, строго в формате диалога.
        """
        length_hint = {
            "короткий": "3–4 пары реплик",
            "средний": "5–7 пар реплик",
            "длинный": "8–10 пар реплик"
        }.get(length, "5–7 пар")

        full_prompt = f"""
        Ты — мастер генерации диалогов. Проанализируй стиль следующего диалога:
    
        "{example_text.strip()}"
    
        Напиши диалоговый фрагмент длиной {length_hint}.
        Участвуют два человека: "Куратор" и "Игрок"
        Пиши перед репликами, от кого они (от "Куратора" или от "Игрока", после атора реплик ставь двоеточие)
        Напиши фрагмент текста, представляющий собой мой диалог с загадочным незнакомцем в заданном стиле.
        Действие происходит в социальной сети.
        Стиль оформления (строго):
        1. Пиши текст единым сплошным абзацем без переносов строк, списков и тире.
        2. Используй формат коротких, обрывистых фраз, где мои реплики и ответы собеседника чередуются.
        3. Не используй кавычки, двоеточия и жирный шрифт. Предложения должны просто следовать друг за другом.
        4. Повествование должно идти от первого лица.
        
        Запрещено писать незаконченные фразы.
    
        Пример темпа: Привет, у тебя есть данные? Да, но это опасно. Я готов рискнуть.
        Тогда иди к заброшенному дому. Понял, уже выхожу.
        Выведи только сам диалог.
    """

        return self.generate(full_prompt)
