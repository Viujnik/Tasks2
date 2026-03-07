from src.main import give_engine

class TestSimulation:
    """
    Проверят, что print вызвался 18 раз - 3 для красоты и 15 - информация task'ов
    """
    def test_simulator_engine(self, mocker):
        mocker.patch("builtins.input", return_value="test_command")
        mock_print = mocker.patch("builtins.print")

        give_engine()

        assert mock_print.call_count == 18
