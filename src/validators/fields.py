class ValidatedField:
    """
    Дескриптор для проверки соответствию набору правил из rules.
    """
    def __init__(self, *rules):
        self.rules = rules

    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None: return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        for rule in self.rules:
            rule.validator(self._name, value)
        setattr(instance, self._name, value)
