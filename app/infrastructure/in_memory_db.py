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
            if key in self._data:
                return self._data[key]
        elif key in self._data:
            return self._data[key]
        return None

    def unset_value(self, key):
        if self._transaction_stack:
            if key in self._transaction_stack[-1]['data']:
                del self._transaction_stack[-1]['data'][key]
            elif key in self._data and key not in self.get_transaction_data():
                if not any(key in trans['data'] for trans in self._transaction_stack):
                    del self._data[key]
        elif key in self._data:
            del self._data[key]

    def count_value(self, value):
        count = 0
        combined_data = self._data.copy()
        for transaction in self._transaction_stack:
            combined_data.update(transaction['data'])

        for key in combined_data:
            if combined_data[key] == value:
                count += 1
        return count

    def find_keys_by_value(self, value):
        keys = []
        combined_data = self._data.copy()
        for transaction in self._transaction_stack:
            combined_data.update(transaction['data'])
        for key, val in combined_data.items():
            if val == value:
                keys.append(key)
        return keys

    def begin_transaction(self):
        self._transaction_stack.append({'data': {}})

    def commit_transaction(self):
        if self._transaction_stack:
            current_transaction = self._transaction_stack.pop()
            if self._transaction_stack: # если есть родительская транзакция, сливаем изменения в нее
                self._transaction_stack[-1]['data'].update(current_transaction['data'])
            else: # иначе, сливаем изменения в основную базу данных
                self._data.update(current_transaction['data'])

    def rollback_transaction(self):
        if self._transaction_stack:
            self._transaction_stack.pop()

    def get_transaction_data(self):
        transaction_data = {}
        for transaction in self._transaction_stack:
            transaction_data.update(transaction['data'])
        return transaction_data
