import datetime
import random
from typing import Protocol, runtime_checkable, Any, Generator, List

from src.validators.fields import ValidatedField
from src.validators.rules import TypeRule, MinLenRule, MaxLenRule, MinValueRule, MaxValueRule, StatusRule


class Task:
    """Модель задачи с валидацией полей через дескрипторы."""
    task_id = ValidatedField(TypeRule(int))
    task_type = ValidatedField(TypeRule(str), MinLenRule(3), MaxLenRule(16))
    description = ValidatedField(TypeRule(str), MinLenRule(8), MaxLenRule(128))
    priority = ValidatedField(TypeRule(int), MinValueRule(1), MaxValueRule(5))
    status = ValidatedField(TypeRule(str), StatusRule({"created", "in_progress", "in_review", "finished"}))
    created_at = ValidatedField(TypeRule(datetime.datetime))
    deadline = ValidatedField(TypeRule(datetime.datetime))
    payload = ValidatedField(TypeRule(dict))

    def __init__(self, task_id: int, task_type: str, description: str,
                 priority: int, status: str, deadline: datetime.datetime, payload: dict) -> None:
        """Инициализирует задачу и устанавливает дату создания."""
        self.task_id = task_id
        self.task_type = task_type
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = datetime.datetime.now()
        self.deadline = deadline
        self.payload = payload

    @property
    def is_on_time(self) -> bool:
        """Проверяет, завершена ли задача в течение 3 дней с момента создания."""
        return self.status == "finished" and self.created_at + datetime.timedelta(days=3) <= self.deadline

    @property
    def summary(self) -> str:
        """Возвращает краткую сводку о состоянии задачи с иконкой успеха."""
        success_icon = "✅" if self.is_on_time else "⏳"
        return f"Task #{self.task_id} ({self.task_type})\t{self.status.upper()} {success_icon}"

    def __repr__(self) -> str:
        """Строковое представление объекта задачи."""
        return f"Task(id={self.task_id}, type='{self.task_type}', status='{self.status}')"
