import requests


class CloudflareAIClient:
    """Клиент для работы с Cloudflare AI API"""

    def __init__(self, account_id: str, api_key: str):
        self.base_url = (
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        )
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get_task_solutions(self, task_title: str) -> str:
        """Получить способы решения задачи от LLM"""
        prompt = f"""
        Задача: {task_title}

        Проанализируй эту задачу и предложи 3-5 конкретных способов её решения.
        Ответ должен быть кратким, практичным и на русском языке.
        Формат: маркированный список.
        """

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Ты помощник по решению задач. Давай практичные советы.",
                },
                {"role": "user", "content": prompt},
            ],
            "model": "@cf/meta/llama-3-8b-instruct",  # Или другая модель
            "max_tokens": 500,
        }

        try:
            response = requests.post(
                f"{self.base_url}/@cf/meta/llama-3-8b-instruct",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()
            return result["result"]["response"]

        except requests.exceptions.RequestException as e:
            print(f"Ошибка Cloudflare AI: {e}")
            return "Не удалось получить рекомендации"
