from statements.influence_statement import IStatement


class VariableDerivationContainer:
    def __init__(self):
        self._statements = set()

    def add(self, st: IStatement):
        self._statements.add(st)

    def get_statements(self):
        return self._statements
