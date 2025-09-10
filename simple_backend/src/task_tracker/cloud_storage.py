import requests


class CloudTaskStorage:
    """Класс для хранения в облаке jsonbin"""

    def __init__(self, bin_id: str, api_key: str):
        self.base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {"X-Master-Key": api_key, "Content-Type": "application/json"}

    def load_tasks(self):
        """Загрузка задач из облака"""
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()["record"]
            # Поддержка старого формата (массив задач) и нового (объект с tasks)
            return data.get("tasks", data) if isinstance(data, dict) else data
        raise Exception(f"Ошибка загрузки: {response.text}")

    def save_tasks(self, tasks):
        """Сохранение задач в облаке"""
        # Сохраняем как объект с ключом tasks для consistency
        data = {"tasks": tasks}
        response = requests.put(self.base_url, headers=self.headers, json=data)
        if response.status_code == 200:
            return True
        raise Exception(f"Ошибка сохранения: {response.text}")
