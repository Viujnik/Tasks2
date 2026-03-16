from src.sources import FileSource, ConsoleSource, APISource

def give_engine():
    """
    Выводит информацию о таске с помощью метода printf_task.
    """
    sources = [FileSource(), ConsoleSource(), APISource()]
    for source in sources:
        print(f"\n{'=' * 20} SOURCE: {source.__class__.__name__} {'=' * 20}")
        try:
            tasks = source.get_tasks()
            for task in tasks:
                print(source.printf_task(task))
        except (TypeError, ValueError) as e:
            print(f"🛑 Ошибка валидации в источнике {source.__class__.__name__}: {e}")
        except Exception as e:
            print(f"🛑 Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    give_engine()
