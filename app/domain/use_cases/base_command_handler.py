from abc import ABC, abstractmethod


class BaseCommandHandler(ABC):
    @abstractmethod
    def execute_command(self, command_name: str, args: list[str]) -> str | None:
        """Метод для выполнения команды."""
        pass
