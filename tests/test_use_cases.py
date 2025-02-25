from app.domain.use_cases.command_handler import CommandHandler
from app.infrastructure.in_memory_db import InMemoryDatabase


def test_set_command():
    db = InMemoryDatabase()
    handler = CommandHandler(db)
    handler.execute_command('SET', ['a', '10'])
    assert db.get_value('a') == '10'


def test_end_command():
    db = InMemoryDatabase()
    handler = CommandHandler(db)

    result = handler.execute_command("END", [])
    assert result == 'END'

    result = handler.execute_command("END", ["extra_arg"])
    assert result == "Error: END command does not require arguments."
