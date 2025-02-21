from app.domain.use_cases.command_handler import CommandHandler
from app.infrastructure.in_memory_db import InMemoryDatabase
from app.interface.console_ui import ConsoleUI


def main():
    """
    Главная функция для запуска приложения.
    Инициализирует все компоненты и запускает UI.
    """
    database = InMemoryDatabase()
    command_handler = CommandHandler(database)
    ui = ConsoleUI(command_handler)
    ui.run()


if __name__ == "__main__":
    main()
