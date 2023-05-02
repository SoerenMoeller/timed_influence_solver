from plotter.plotter import show_plot, plot_statements
from statements.variable_derivation_container import VariableDerivationContainer
from statements.influence_statement import IStatement
from statements.rectangle_statement import RStatement
from statements.time_derivation_container import TimeDerivationContainer
from statements.time_variable_container import TimeVariableContainer
from statements.trapezoid_statement import TStatement


class Solver:

    def __init__(self, statements=None):
        self._var_der_influence: dict[tuple[str, str], VariableDerivationContainer] = {}
        self._time_var_influence: dict[str, TimeVariableContainer] = {}
        self._time_der_influence: dict[str, TimeDerivationContainer] = {}

        if statements is not None:
            self.add(statements)

    def add(self, statement):
        if type(statement) == tuple:
            statement = {statement}

        for elem in statement:
            is_influence: bool = type(elem[-1]) == str
            self._add_influence(elem) if is_influence else self._add_time_influence(elem)

    def _add_influence(self, statement: tuple[str, tuple, tuple, tuple, str]):
        influence: tuple[str, str] = statement[0], statement[-1]
        if influence not in self._var_der_influence:
            self._var_der_influence[influence] = VariableDerivationContainer()

        self._var_der_influence[influence].add(IStatement.create(statement))

    def _add_time_influence(self, statement):
        variable: str = statement[0]
        container = self._time_der_influence if variable.endswith("'") else self._time_var_influence

        if len(statement) == 3:
            if variable not in container:
                container[variable] = TimeDerivationContainer()
            container[variable].add(RStatement.create(statement))
            return

        if variable not in container:
            container[variable] = TimeVariableContainer()
        container[variable].add(TStatement.create(statement))

    def solve(self, hypothesis: tuple) -> bool:
        self.plot(hypothesis)
        return False

    def plot(self, hypothesis):
        plot_statements(self._var_der_influence | self._time_der_influence | self._time_var_influence,
                        self._var_der_influence.keys() | self._time_var_influence.keys() |
                        self._time_der_influence.keys(), hypothesis)
        show_plot()
        pass

    def __str__(self) -> str:
        return ""
