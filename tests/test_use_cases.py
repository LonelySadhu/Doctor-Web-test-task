from app.domain.use_cases.command_handler import CommandHandler
from app.infrastructure.in_memory_db import InMemoryDatabase


def test_set_command():
    db = InMemoryDatabase()
    handler = CommandHandler(db)
    handler.execute_command('SET', ['a', '10'])
    assert db.get_value('a') == '10'
