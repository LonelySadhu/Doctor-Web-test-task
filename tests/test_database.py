import pytest
from app.infrastructure.in_memory_db import InMemoryDatabase


def test_set_and_get():
    db = InMemoryDatabase()
    db.set_value('a', '1')
    assert db.get_value('a') == '1'


def test_unset():
    db = InMemoryDatabase()
    db.set_value('a', '1')
    db.unset_value('a')
    assert db.get_value('a') is None


def test_count_value():
    db = InMemoryDatabase()
    db.set_value('a', '1')
    db.set_value('b', '1')
    assert db.count_value('1') == 2


def test_transactions():
    db = InMemoryDatabase()
    db.set_value('a', '1')
    db.begin_transaction()
    db.set_value('a', '2')
    assert db.get_value('a') == '2'
    db.rollback_transaction()
    assert db.get_value('a') == '1'


def test_unset_in_transaction():
    db = InMemoryDatabase()

    db.set_value("A", "10")
    assert db.get_value("A") == "10"

    db.begin_transaction()
    assert db.get_value("A") == "10"

    db.set_value("A", "20")
    assert db.get_value("A") == "20"

    db.unset_value("A")
    assert db.get_value("A") is None

    db.rollback_transaction()
    assert db.get_value("A") == "10"
