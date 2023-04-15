from statements.influence_statement import InfluenceStatement


class InfluenceContainer:
    def __init__(self):
        self._statements = set()

    def add(self, statement: InfluenceStatement):
        self._statements.add(statement)

    def get_statements(self):
        return self._statements
