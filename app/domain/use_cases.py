from app.domain.database import Database


class CommandHandler:
    def __init__(self, database: Database):
        self.database = database
        self.command_strategies = {
            'SET': self.set_command,
            'GET': self.get_command,
            'UNSET': self.unset_command,
            'COUNTS': self.counts_command,
            'FIND': self.find_command,
            'BEGIN': self.begin_transaction,
            'COMMIT': self.commit_transaction,
            'ROLLBACK': self.rollback_transaction,
        }

    def execute_command(self, command_name: str, args: list[str]) -> str | None:
        strategy = self.command_strategies.get(command_name.upper())
        if strategy:
            return strategy(args)
        return f"Error: Unknown command '{command_name}'."

    def set_command(self, args):
        if len(args) == 2:
            self.database.set_value(args[0], args[1])
            return None
        return "Error: SET command requires two arguments (key and value)."

    def get_command(self, args):
        if len(args) == 1:
            value = self.database.get_value(args[0])
            return value if value is not None else 'NULL'
        return "Error: GET command requires one argument (key)."

    def unset_command(self, args):
        if len(args) == 1:
            self.database.unset_value(args[0])
            return None
        return "Error: UNSET command requires one argument (key)."

    def counts_command(self, args):
        if len(args) == 1:
            return str(self.database.count_value(args[0]))
        return "Error: COUNTS command requires one argument (value)."

    def find_command(self, args):
        if len(args) == 1:
            keys = self.database.find_keys_by_value(args[0])
            return ' '.join(keys) if keys else 'NULL'
        return "Error: FIND command requires one argument (value)."

    def begin_transaction(self, args):
        if not args:
            self.database.begin_transaction()
            return None
        return "Error: BEGIN command does not require arguments."

    def commit_transaction(self, args):
        if not args:
            self.database.commit_transaction()
            return None
        return "Error: COMMIT command does not require arguments."

    def rollback_transaction(self, args):
        if not args:
            self.database.rollback_transaction()
            return None
        return "Error: ROLLBACK command does not require arguments."
