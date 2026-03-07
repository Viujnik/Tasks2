import pytest
import datetime
from src.tasks_models import Task, FileSource, ConsoleSource, APISource
from src.validators.errors import LenError, StatusError


@pytest.fixture
def valid_task_data():
    return {
        "task_id": 123,
        "task_type": "service",
        "description": "This is a very long description for testing",
        "priority": 3,
        "status": "created",
        "deadline": datetime.datetime.now() + datetime.timedelta(days=1),
        "payload": {"key": "value"}
    }


class TestTaskValidation:
    def test_correct_task_creation(self, valid_task_data):
        """Проверяем, что валидная задача создается без ошибок."""
        task = Task(**valid_task_data)
        assert task.task_id == 123
        assert task.status == "created"

    def test_invalid_type(self, valid_task_data):
        """Проверяем TypeRule: task_id должен быть int."""
        valid_task_data["task_id"] = "not_an_int"
        with pytest.raises(TypeError):
            Task(**valid_task_data)

    def test_invalid_status(self, valid_task_data):
        """Проверяем StatusRule: левый статус должен кидать StatusError."""
        valid_task_data["status"] = "hacking_rkn"
        with pytest.raises(StatusError):
            Task(**valid_task_data)

    def test_min_len_description(self, valid_task_data):
        """Проверяем MinLenRule: описание < 8 символов."""
        valid_task_data["description"] = "short"
        with pytest.raises(LenError):
            Task(**valid_task_data)

    def test_priority_range(self, valid_task_data):
        """Проверяем MaxValue: приоритет 1-5."""
        valid_task_data["priority"] = 10
        with pytest.raises(ValueError):
            Task(**valid_task_data)


class TestTaskProperties:
    def test_is_on_time_logic(self, valid_task_data):
        """Проверяем вычисляемое свойство успеха"""
        valid_task_data["status"] = "finished"
        valid_task_data["deadline"] = datetime.datetime.now() + datetime.timedelta(days=5)
        task = Task(**valid_task_data)
        assert task.is_on_time is True

        valid_task_data["deadline"] = datetime.datetime.now() - datetime.timedelta(days=1)
        task_late = Task(**valid_task_data)
        assert task_late.is_on_time is False

    def test_summary_content(self, valid_task_data):
        """Проверяет вычислимое свойство summary."""
        task = Task(**valid_task_data)
        res = task.summary
        assert isinstance(res, str)
        assert str(task.task_id) in res
        assert task.task_type in res
        assert "CREATED" in res


class TestSources:
    @pytest.mark.parametrize("source_class", [FileSource, ConsoleSource, APISource])
    def test_source_get_tasks(self, source_class, monkeypatch):
        """Проверяет get_tasks всех source'ов."""
        monkeypatch.setattr("builtins.input", lambda _: "test_cmd_8_chars")

        source = source_class()
        tasks = list(source.get_tasks())

        assert len(tasks) == 5
        assert all(isinstance(t, Task) for t in tasks)
