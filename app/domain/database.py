from abc import ABC, abstractmethod


class Database(ABC):
    """
    Интерфейс для работы с базой данных.
    Определяет контракт на операции хранения, получения, удаления и подсчета данных.
    """

    @abstractmethod
    def set_value(self, key, value):
        pass

    @abstractmethod
    def get_value(self, key):
        pass

    @abstractmethod
    def unset_value(self, key):
        pass

    @abstractmethod
    def count_value(self, value):
        pass

    @abstractmethod
    def find_keys_by_value(self, value):
        pass

    @abstractmethod
    def begin_transaction(self):
        pass

    @abstractmethod
    def commit_transaction(self):
        pass

    @abstractmethod
    def rollback_transaction(self):
        pass
