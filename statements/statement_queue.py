from typing import Union

from statements.influence_statement import IStatement
from statements.rectangle_statement import RStatement
from statements.time_container import TimeContainer
from statements.trapezoid_statement import TStatement
from statements.variable_derivation_container import VariableDerivationContainer


class StatementQueue:
    def __init__(self):
        self.var_der_influence: dict[tuple[str, str], VariableDerivationContainer] = {}
        self.time_influence: dict[str, TimeContainer] = {}

    def add_extern(self, statement):
        if type(statement) == tuple:
            statement = {statement}

        for elem in statement:
            is_influence: bool = type(elem[-1]) == str
            self._add_influence(elem) if is_influence else self._add_time_influence(elem)

    def add(self, var, st):
        if var not in self.time_influence:
            self.time_influence[var] = TimeContainer()
        self.time_influence[var].add(st)

    def _add_influence(self, statement: tuple[str, tuple, tuple, tuple, str]):
        influence: tuple[str, str] = statement[0], statement[-1]
        if influence not in self.var_der_influence:
            self.var_der_influence[influence] = VariableDerivationContainer()

        self.var_der_influence[influence].add(IStatement.create(statement))

    def init(self):
        for container in self.var_der_influence.values():
            container.init()

    def _add_time_influence(self, statement):
        variable: str = statement[0]

        if len(statement) == 3:
            st = RStatement.create(statement)
        else:
            st = TStatement.create(statement)

        if variable not in self.time_influence:
            self.time_influence[variable] = TimeContainer()
        self.time_influence[variable].add(st)

    def all_statements(self):
        return self.var_der_influence | self.time_influence

    def next_st(self) -> Union[tuple[str, RStatement], None]:
        choices = set(filter(lambda x: self.time_influence[x], self.time_influence.keys()))
        if not choices:
            return None

        variable: str = min(choices, key=lambda x: self.time_influence[x].top())
        return variable, self.time_influence[variable].get()

