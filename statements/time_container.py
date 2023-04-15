from statements.time_statement import TimeStatement


class TimeContainer:
    def __init__(self):
        self._statements = set()

    def add(self, statement: TimeStatement):
        self._statements.add(statement)

    def get_statements(self):
        return self._statements
