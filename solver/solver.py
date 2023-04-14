from statements.influence_container import InfluenceContainer
from statements.time_container import TimeContainer


class Solver:

    def __init__(self):
        self._influences: dict[tuple[str, str], InfluenceContainer] = {}
        self._time_influences: dict[str, TimeContainer] = {}

    def add(self, statement: tuple):
        is_influence: bool = type(statement[-1]) == str
        return self.add_influence(statement) if is_influence else self.add_time_influence(statement)

    def add_influence(self, statement: tuple[str, float, float, float, float, float, float, str]):
        influence: tuple[str, str] =  statement[0], statement[-1]
        if influence not in self._influences:
            self._influences[influence] = InfluenceContainer()


        self._influences[influence].add(statement)

    def add_time_influence(self, statement: tuple[str, float, float, float, float, float, float]):
        variable: str = statement[0]
        if variable not in self._time_influences:
            self._time_influences[variable] = TimeContainer()


        self._time_influences[variable].add(statement)

    def solve(self) -> bool:
        pass

    def __str__(self) -> str:
        return f"{self._influences}\n{self._time_influences}"
