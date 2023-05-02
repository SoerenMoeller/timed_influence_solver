from statements.rectangle_statement import RStatement


class TimeDerivationContainer:
    def __init__(self):
        self._statements = set()

    def add(self, st: RStatement):
        self._statements.add(st)

    def get_statements(self):
        return self._statements
