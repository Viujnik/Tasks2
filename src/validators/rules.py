from typing import Protocol, runtime_checkable, Any

from src.validators.errors import LenError, StatusError


@runtime_checkable
class Rule(Protocol):
    """
    Контракт для правил. Их суть - в методе validator выкинуть исключение, если значение не подходит.
    """

    def validator(self, field: str, value: Any) -> None:
        ...


class TypeRule:
    def __init__(self, expected_type: type) -> None:
        self.expected_type = expected_type

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if not isinstance(value, self.expected_type):
                raise TypeError(f"{field} должен быть {self.expected_type}")


class MinLenRule:
    def __init__(self, min_len: int) -> None:
        self.min_len = min_len

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if len(value) < self.min_len:
                raise LenError(f"Длина поля {field} должна быть не меньше {self.min_len}")


class MaxLenRule:
    def __init__(self, max_len: int) -> None:
        self.max_len = max_len

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if len(value) > self.max_len:
                raise LenError(f"Длина поля {field} должна быть не больше {self.max_len}")


class MinValueRule:
    def __init__(self, min_val: int) -> None:
        self.min_val = min_val

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if value < self.min_val:
                raise ValueError(f"Значение поля {field} должно быть не меньше {self.min_val}")


class MaxValueRule:
    def __init__(self, max_val: int) -> None:
        self.max_val = max_val

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if value > self.max_val:
                raise ValueError(f"Значение поля {field} должно быть не больше {self.max_val}")


class StatusRule:
    def __init__(self, statuses: set[str]) -> None:
        self.statuses = statuses

    def validator(self, field: str, value: Any) -> None:
        if value is not None:
            if value not in self.statuses:
                raise StatusError(f"Значение поля {field} должно быть одним из {self.statuses}")
