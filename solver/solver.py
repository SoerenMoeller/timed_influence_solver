from collections import defaultdict

from plotter.plotter import show_plot, plot_statements
from statements.td_statement import TDStatement
from statements.td_container import TDContainer
from statements.tv_container import TVContainer
from statements.tv_statement import TVStatement
from statements.vd_container import VDContainer
from statements.vd_statement import VDStatement


class Solver:

    def __init__(self, statements=None):
        self._dependency_graph: dict[str, set[str]] = {}
        self._td_statements: defaultdict[str, TDContainer] = defaultdict(TDContainer)
        self._tv_statements: defaultdict[str, TVContainer] = defaultdict(TVContainer)
        self._vd_statements: defaultdict[tuple[str, str], VDContainer] = defaultdict(VDContainer)

        self.add(statements)

    def add(self, statements):
        if statements is None:
            return

        if type(statements) == tuple:
            statements = {statements}

        for st in statements:
            self._add_st(st)

#   tuple[str, tuple[float, float], tuple[float, float], tuple[float, float], str]  VD-Statements
#   tuple[str, tuple[float, float], tuple[float, float], tuple[float, float]]       TV-Statements
#   tuple[str, tuple[float, float], tuple[float, float]]                            TD-Statements
    def _add_st(self, st: tuple):
        if len(st) == 5:
            statement = VDStatement.create(st)
            container = self._td_statements
            var = (st[0], st[-1])
        elif len(st) == 4:
            statement = TVStatement.create(st)
            container = self._tv_statements
            var = st[0]
        else:
            statement = TDStatement.create(st)
            container = self._td_statements
            var = st[0]

        container[var].add(statement)

    def solve(self, hypothesis: tuple) -> bool:
        #self._create_dependency_graph()

        # if variable is a sink, that's not part of the hypothesis, remove it
        variable: str = hypothesis[0]
        hypothesis_st = TDStatement.create(hypothesis)
        #self._remove_sink(variable)
        #self._remove_influences_without_time()

        # TODO: check if hypothesis true already?

        # need initial value
        #if variable not in self._st_queue.time_influence:
        #    return False
#
        #if min(self._st_queue.time_influence[variable].get_statements()).start > hypothesis_st.start:
        #    return False

        #print(self._st_queue.next_st())
        #while next_st := self._st_queue.next_st():
        #    print("hi")
        #    var, st = next_st#

        #    if var.endswith("'"):
        #        self._apply_cdr(var, st)
        #    else:
        #        self._apply_transitive(var, st)

        #print(self._st_queue.time_influence)
        self._plot(hypothesis)
        return False

    #def _apply_cdr(self, variable: str, statement):
    #    influence = variable[:-1]
    #    time_var_model = self._st_queue.time_influence[influence]
    #    #time_var_model.envelope()

    #def _apply_transitive(self, variable: str, statement):
    #    influences = filter(lambda k: k[0] == variable, self._st_queue.var_der_influence.keys())

    #    for k in influences:
    #        var_der_model = self._st_queue.var_der_influence[k]
    #        enveloped = var_der_model.envelope(statement.lower, statement.upper)
    #        if enveloped is None:
    #            continue

    #        for st in enveloped:
    #            new_st = transitivity_rule(statement, st)
    #            if new_st is None:
    #                continue
    #            self._st_queue.add(f"{variable}'", new_st)

    #def _remove_influences_without_time(self):
    #    self._dependency_graph = {a: self._dependency_graph[a] for a in self._dependency_graph
    #                              if a in self._st_queue.time_influence}

    #def _remove_sink(self, variable: str):
    #    variable += "'"
    #    values = functools.reduce(lambda a, b: a.union(b), self._dependency_graph.values(), set())
    #    values.difference(self._dependency_graph.keys())#

    #    self._dependency_graph = {a: self._dependency_graph[a].difference(values) for a in self._dependency_graph}

    #def _create_dependency_graph(self):
    #    for a, b in self._st_queue.var_der_influence.keys():
    #        if a not in self._dependency_graph:
    #            self._dependency_graph[a] = set()
    #        self._dependency_graph[a].add(b)

    def _plot(self, hypothesis):
        plot_statements(self._td_statements | self._tv_statements | self._vd_statements,
                        self._td_statements.keys() | self._tv_statements.keys() | self._vd_statements.keys(), hypothesis)
        show_plot()

    def __str__(self) -> str:
        return ""
