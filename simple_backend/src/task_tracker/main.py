import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from cloud_storage import CloudTaskStorage


# Загружаем .env
load_dotenv()

app = FastAPI()

BIN_ID = os.getenv("JSONBIN_BIN_ID")
API_KEY = os.getenv("JSONBIN_API_KEY")

if not BIN_ID or not API_KEY:
    raise RuntimeError(
        "Не найдены переменные окружения JSONBIN_BIN_ID или JSONBIN_API_KEY"
    )

storage = CloudTaskStorage(BIN_ID, API_KEY)


class Task(BaseModel):
    """Модель задачи"""

    id: int
    title: str
    status: str


class TaskCreate(BaseModel):
    """Модель для создания задачи"""

    title: str
    status: str


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получение всех задач"""
    tasks = storage.load_tasks()
    return tasks


@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate):
    """Создание новой задачи"""
    tasks = storage.load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1
    task = {"id": new_id, "title": task_data.title, "status": task_data.status}
    tasks.append(task)
    storage.save_tasks(tasks)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    """Обновление задачи"""
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["status"] = task_data.status
            storage.save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи"""
    tasks = storage.load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            storage.save_tasks(tasks)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
