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

_dependency_graph: dict[str, set[str]] = {}
_td_statements: defaultdict[str, TDContainer] = defaultdict(TDContainer)
_tv_statements: defaultdict[str, TVContainer] = defaultdict(TVContainer)
_vd_statements: defaultdict[tuple[str, str], VDContainer] = defaultdict(VDContainer)
_k_mode: bool = True


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


def _add(statements):
    if statements is None:
        return
    if type(statements) == tuple:
        statements = {statements}
    for st in statements:
        _add_st(st)


#   tuple[str, tuple[float, float], tuple[float, float], tuple[float, float], str]  VD-Statements
#   tuple[str, tuple[float, float], tuple[float, float], tuple[float, float]]       TV-Statements
#   tuple[str, tuple[float, float], tuple[float, float]]                            TD-Statements
def _add_st(st: tuple):
    if len(st) == 5:
        statement = VDStatement.create(st)
        container = _vd_statements
        var = (st[0], st[-1])
    elif len(st) == 4:
        statement = TVStatement.create(st)
        container = _tv_statements
        var = st[0]
    else:
        statement = TDStatement.create(st)
        container = _td_statements
        var = st[0]

    container[var].add(statement)


def solve(sts, hypothesis: tuple) -> bool:
    _add(sts)

    variable: str = hypothesis[0]
    hypothesis_st: TVStatement = TVStatement.create(hypothesis)

    while _greatest_end(variable) < hypothesis_st.end and _running():
        tv_todos = {var: _tv_statements[var].newly_created.copy() for var in _tv_statements.keys()}
        for var in tv_todos.keys():
            _tv_statements[var].clear_new()
            _apply_transitive(var, tv_todos[var])

        for var in sorted(tv_todos.keys()):
            td_todo = _td_statements[var].newly_created.copy()
            _td_statements[var].clear_new()
            _apply_cd(var, tv_todos[var], td_todo)

    overlapping = filter(lambda x: x.end != hypothesis_st.start, _tv_statements[variable].overlap(hypothesis_st))
    final_st = functools.reduce(lambda a, b: join_tvs(a, b), overlapping)
    final_st = final_st.relax(hypothesis_st.start, hypothesis_st.end)

    result: bool = final_st.lower >= hypothesis_st.lower and final_st.upper <= hypothesis_st.upper \
        and final_st.lower_r >= hypothesis_st.lower_r and final_st.upper_r <= hypothesis_st.upper_r

    print(f"The hypothesis is {result}!")

    _plot(hypothesis)
    return result


def _running():
    return any(map(lambda x: x.newly_created, set(_tv_statements.values()) | set(_td_statements.values())))


def _greatest_end(variable: str):
    return max(map(lambda x: x.end, _tv_statements[variable].get_statements()))


def _apply_transitive(variable: str, tv_todo):
    for st_a in tv_todo:
        influences = filter(lambda k: k[0] == variable, _vd_statements.keys())

        for k in influences:
            vd_container = _vd_statements[k]
            enveloped_sts = vd_container.envelope(st_a.lower, st_a.upper)

            for st_b in enveloped_sts:
                new_st = transitivity_rule(st_a, st_b)

                if new_st is not None:
                    _td_statements[k[1]].add(new_st)


def _apply_cd(variable: str, tv_todo, td_todo):
    tv_container = _tv_statements[variable]
    td_container = _td_statements[variable]

    for st_a in [st.relax(st.start, st.start) for st in tv_todo] + [st.relax(st.end, st.end) for st in tv_todo]:
        _combine_overlapping(td_container.overlap(st_a), st_a, tv_container, True)

    for st_b in td_todo:
        _combine_overlapping(tv_container.overlap(st_b), st_b, tv_container, False)


def _plot(hypothesis):
    plot_statements(_tv_statements, _td_statements, _vd_statements,
                    _tv_statements.keys(), _td_statements.keys(),  _vd_statements.keys(), hypothesis)
    show_plot()
