class ConsoleUI:
    """
    Интерфейс пользователя через консоль.
    Отвечает за ввод команд, их парсинг и вывод результатов пользователю.
    """

    def __init__(self, command_handler):
        self.command_handler = command_handler

    def run(self):
        while True:
            try:
                command_line = input("> ").strip()
                if not command_line:
                    continue
                parts = command_line.split()
                command_name = parts[0].upper()
                args = parts[1:]

                result = self.command_handler.execute_command(command_name, args)

                if result == 'END':
                    break  # Exit application
                elif result is not None:
                    print(result)
                elif command_name == 'FIND' and result is None:
                    print("NULL")
                elif command_name == 'GET' and result == 'NULL':
                    print("NULL")

            except EOFError:
                print("\nExiting application.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue
