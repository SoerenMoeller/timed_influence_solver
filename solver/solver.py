from plotter.plotter import plot_statements, show_plot
from statements.influence_container import InfluenceContainer
from statements.influence_statement import InfluenceStatement
from statements.time_container import TimeContainer
from statements.time_statement import TimeStatement


class Solver:

    def __init__(self, statements=None):
        self._influences: dict[tuple[str, str], InfluenceContainer] = {}
        self._time_influences: dict[str, TimeContainer] = {}

        if statements is not None:
            self.add(statements)

    def add(self, statement):
        if type(statement) == tuple:
            statement = {statement}

        for elem in statement:
            print(elem)
            is_influence: bool = type(elem[-1]) == str
            self.add_influence(elem) if is_influence else self.add_time_influence(elem)

    def add_influence(self, statement: tuple[str, tuple, tuple, tuple, str]):
        influence: tuple[str, str] =  statement[0], statement[-1]
        if influence not in self._influences:
            self._influences[influence] = InfluenceContainer()

        self._influences[influence].add(InfluenceStatement.create_influence_statement(statement))

    def add_time_influence(self, statement: tuple[str, tuple, tuple, tuple]):
        variable: str = statement[0]
        if variable not in self._time_influences:
            self._time_influences[variable] = TimeContainer()

        self._time_influences[variable].add(TimeStatement.create_time_statement(statement))

    def solve(self, hypothesis: tuple) -> bool:
        self.plot(hypothesis)

    def plot(self, hypothesis):
        plot_statements(self._time_influences | self._influences, self._time_influences.keys() | self._influences.keys(), hypothesis)
        show_plot()

    def __str__(self) -> str:
        return f"{self._influences}\n{self._time_influences}"
