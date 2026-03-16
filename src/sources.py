import datetime
import random
from typing import Generator, Any

from src.tasks_models import Task


class FileSource:
    """Источник задач, имитирующий чтение файловой системы."""

    def get_tasks(self) -> list[Task]:
        """Генерирует список задач, связанных с передачей файлов."""
        tasks_list = []
        for i in range(5):
            tasks_list.append(
                Task(task_id=random.randint(1000, 9999), task_type="file", description="Send very important file",
                     priority=1, status=random.choice(["created", "in_progress", "in_review", "finished"]),
                     deadline=datetime.datetime.now() + datetime.timedelta(days=4),
                     payload={"sender_id": random.randint(100000, 999999),
                              "receiver_id": random.randint(100000, 999999),
                              "filename": f"pron_{random.randint(100, 999)}_{random.randint(10, 99)}.mp4",
                              "file_size": random.randint(1000, 9999)}))
        return tasks_list

    def printf_task(self, task: Task) -> str:
        """Форматирует данные о файле и дедлайне."""
        header = task.summary
        p = task.payload
        timing = f"\t🕒 Deadline: {task.deadline.strftime('%d.%m %H:%M')}"
        details = f"\t🎥 File: {p['filename']} ({p['file_size']} MB) | Sender ID: {p['sender_id']}"
        return f"{header}\n{timing}\n{details}\n"


class ConsoleSource:
    """Источник задач через ввод команд в консоли."""

    def get_tasks(self) -> Generator[Task, Any, None]:
        """Запрашивает команды у пользователя и генерирует задачи."""
        now = datetime.datetime.now()
        for i in range(5):
            yield Task(
                task_id=random.randint(1000, 9999), task_type="console", description="System command execution",
                priority=random.randint(1, 5), status=random.choice(["created", "in_progress", "finished"]),
                deadline=now + datetime.timedelta(days=2),
                payload={
                    "sender_id": random.randint(100000, 999999),
                    "command": input("Введите команду системы: "),
                    "status": random.choice(["OK", "ERROR", "WARNING", "CRITICAL"])})

    def printf_task(self, task: Task) -> str:
        """Форматирует вывод системной команды и результата."""
        p = task.payload
        return (f"{task.summary}\n"
                f"   💻 User({p['sender_id']}) executed: {p['command']}\n"
                f"   ⚡ Result: {p['status']}\n")


class APISource:
    """Источник задач, имитирующий получение данных из REST API."""

    def get_tasks(self) -> list[Task]:
        """Генерирует список задач на основе HTTP-запросов."""
        tasks_list = []
        now = datetime.datetime.now()
        for i in range(5):
            tasks_list.append(Task(
                task_id=random.randint(1000, 9999), task_type="api", description="REST API Request",
                priority=random.randint(1, 5),
                status="finished" if i == 0 else "in_review", deadline=now + datetime.timedelta(hours=12),
                payload={
                    "client_id": random.randint(100000, 999999),
                    "HTTP_METHOD": random.choice(["GET", "POST", "PUT", "PATCH"]),
                    "url": "https://rkn.gov.ru",
                    "status_code": "ERROR"}))
        return tasks_list

    def printf_task(self, task: Task) -> str:
        """Форматирует информацию об URL и методе запроса."""
        p = task.payload
        return (f"{task.summary}\n"
                f"   🌐 Client({p['client_id']}) {p['HTTP_METHOD']} -> {p['url']}\n"
                f"   🚫 Response: {p['status_code']}\n")
