from collections import defaultdict

from plotter.plotter import show_plot, plot_statements
from solver.rules import transitivity_rule, cdr_rule, cdl_rule, join_tvs
import functools
from statements.td_statement import TDStatement
from statements.td_container import TDContainer
from statements.tv_container import TVContainer
from statements.tv_statement import TVStatement
from statements.vd_container import VDContainer
from statements.vd_statement import VDStatement


def _combine_overlapping(overlapping, current, tv_container: TVContainer, from_tv: bool):
    for o in overlapping:
        st_a = current if from_tv else o
        st_b = o if from_tv else current

        new_st = cdr_rule(st_a, st_b)

        if new_st is not None:
            tv_container.add(new_st)

        new_st = cdl_rule(st_a, st_b)

        if new_st is not None:
            tv_container.add(new_st)


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
            container = self._vd_statements
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
        # if variable is a sink, that's not part of the hypothesis, remove it
        variable: str = hypothesis[0]
        hypothesis_st = TVStatement.create(hypothesis)

        while self._greatest_end(variable) < hypothesis_st.end and self._running():
            tv_todos = {var: self._tv_statements[var].newly_created.copy() for var in self._tv_statements.keys()}
            for var in tv_todos.keys():
                self._tv_statements[var].clear_new()
                self._apply_transitive(var, tv_todos[var])

            for var in sorted(tv_todos.keys()):
                td_todo = self._td_statements[var].newly_created.copy()
                self._td_statements[var].clear_new()
                self._apply_cd(var, tv_todos[var], td_todo)

        overlapping = filter(lambda x: x.end != hypothesis_st.start, self._tv_statements[variable].overlap(hypothesis_st))
        final_st = functools.reduce(lambda a, b: join_tvs(a, b), overlapping)
        final_st = final_st.relax(hypothesis_st.start, hypothesis_st.end)

        result: bool = final_st.lower >= hypothesis_st.lower and final_st.upper <= hypothesis_st.upper \
            and final_st.lower_r >= hypothesis_st.lower_r and final_st.upper_r <= hypothesis_st.upper_r

        print(f"The hypothesis is {result}!")

        self._plot(hypothesis)
        return result

    def _running(self):
        return any(map(lambda x: x.newly_created, set(self._tv_statements.values()) | set(self._td_statements.values())))

    def _greatest_end(self, variable: str):
        return max(map(lambda x: x.end, self._tv_statements[variable].get_statements()))

    def _apply_transitive(self, variable: str, tv_todo):
        for st_a in tv_todo:
            influences = filter(lambda k: k[0] == variable, self._vd_statements.keys())

            for k in influences:
                vd_container = self._vd_statements[k]
                enveloped_sts = vd_container.envelope(st_a.lower, st_a.upper)

                for st_b in enveloped_sts:
                    new_st = transitivity_rule(st_a, st_b)

                    if new_st is not None:
                        self._td_statements[k[1]].add(new_st)

    def _apply_cd(self, variable: str, tv_todo, td_todo):
        tv_container = self._tv_statements[variable]
        td_container = self._td_statements[variable]

        for st_a in [st.relax(st.start, st.start) for st in tv_todo] + [st.relax(st.end, st.end) for st in tv_todo]:
            _combine_overlapping(td_container.overlap(st_a), st_a, tv_container, True)

        for st_b in td_todo:
            _combine_overlapping(tv_container.overlap(st_b), st_b, tv_container, False)

    def _plot(self, hypothesis):
        plot_statements(self._tv_statements, self._td_statements, self._vd_statements,
                        self._tv_statements.keys(), self._td_statements.keys(),  self._vd_statements.keys(), hypothesis)
        show_plot()

    def __str__(self) -> str:
        return ""
