from app.domain.database import Database


class InMemoryDatabase(Database):
    """
    Реализация базы данных в оперативной памяти.
    Поддерживает транзакции и сохранение состояний для отката.
    """

    def __init__(self):
        self._data = {}
        self._transaction_stack = []

    def set_value(self, key, value):
        if self._transaction_stack:
            self._transaction_stack[-1]['data'][key] = value
        else:
            self._data[key] = value

    def get_value(self, key):
        if self._transaction_stack:
            for transaction in reversed(self._transaction_stack):
                if key in transaction['data']:
                    return transaction['data'][key]
            return self._data.get(key, None)
        return self._data.get(key, None)

    def unset_value(self, key):
        if self._transaction_stack:
            # Вместо удаления ключа, сохраняем None
            self._transaction_stack[-1]['data'][key] = None
        elif key in self._data:
            del self._data[key]

    def count_value(self, value):
        combined_data = self._data.copy()
        for transaction in self._transaction_stack:
            combined_data.update(transaction['data'])
        return sum(1 for v in combined_data.values() if v == value)

    def find_keys_by_value(self, value):
        combined_data = self._data.copy()
        for transaction in self._transaction_stack:
            combined_data.update(transaction['data'])
        return [k for k, v in combined_data.items() if v == value]

    def begin_transaction(self):
        self._transaction_stack.append({'data': {}})

    def commit_transaction(self):
        if self._transaction_stack:
            current_transaction = self._transaction_stack.pop()
            if self._transaction_stack:
                self._transaction_stack[-1]['data'].update(current_transaction['data'])
            else:
                for key, value in current_transaction['data'].items():
                    if value is None:
                        self._data.pop(key, None)
                    else:
                        self._data[key] = value

    def rollback_transaction(self):
        if self._transaction_stack:
            self._transaction_stack.pop()
