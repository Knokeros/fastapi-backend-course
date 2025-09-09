from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    """Модель Задачи"""

    id: int
    title: str
    status: str


# Добаляю хранение в оперативной памяти
tasks = []
current_id = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """ "Получение всвех задач"""
    return tasks


@app.post("/tasks", response_model=Task)
def create_task(task_data: dict):
    """Создание новой задачи"""
    global current_id
    task = Task(
        id=current_id,
        title=task_data.get("title"),
        status=task_data.get("status"),
    )
    tasks.append(task)
    current_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: dict):
    """Обновление задачи"""
    for task in tasks:
        if task.id == task_id:
            task.title = task_data.get("title", task.title)
            task.status = task_data.get("status", task.status)
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи"""
    global tasks
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
