from collections import defaultdict

from plotter.plotter import show_plot, plot_statements
from solver.rules import transitivity_rule, cdr_rule, cdl_rule, join_tvs, join_tds
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


def _extract_hypothesis(hypothesis: tuple):
    if len(hypothesis) == 5:
        statement = VDStatement.create(hypothesis)
        kind = "VD"
    elif len(hypothesis) == 4:
        statement = TVStatement.create(hypothesis)
        kind = "TV"
    else:
        statement = TDStatement.create(hypothesis)
        kind = "TD"

    return statement, kind


def _check_vd(hypothesis: VDStatement, a: str, b: str) -> bool:
    def is_valid(st: VDStatement) -> bool:
        return st.min_slope <= hypothesis.min_slope and st.max_slope >= hypothesis.max_slope \
            and st.start <= hypothesis.start and st.end >= hypothesis.end \
            and st.lower <= hypothesis.lower and st.upper >= hypothesis.upper

    result = bool(set(filter(is_valid, _vd_statements[(a, b)].get_statements())))
    return _feedback(result, hypothesis.to_tuple(a, b))


def _feedback(result: bool, hypothesis) -> bool:
    print(f"The hypothesis is {result}!")
    _plot(hypothesis)

    return result


def solve(sts, hypothesis: tuple, k_mode: bool = True, k: int = 15) -> bool:
    _add(sts)

    tv = _tv_statements

    variable: str = hypothesis[0]
    hypothesis_st, hypothesis_kind = _extract_hypothesis(hypothesis)

    if hypothesis_kind == "VD":
        return _check_vd(hypothesis_st, hypothesis[0], hypothesis[4])

    j: int = 0
    while _running() and (j <= k if k_mode else _greatest_end(variable) < hypothesis_st.end):
        tv_todos = {var: _tv_statements[var].newly_created.copy() for var in _tv_statements.keys()}
        for var in tv_todos.keys():
            _tv_statements[var].clear_new()
            _apply_transitive(var, tv_todos[var])

        for var in sorted(tv_todos.keys()):
            td_todo = _td_statements[var].newly_created.copy()
            _td_statements[var].clear_new()
            _apply_cd(var, tv_todos[var], td_todo)

        j += 1
        
    if hypothesis_kind == "TV":
        return _check_tv(variable, hypothesis_st)
    return _check_td(variable, hypothesis_st)


def _check_tv(var: str, hypothesis: TVStatement) -> bool:
    overlapping = list(filter(lambda x: x.end != hypothesis.start, _tv_statements[var].overlap(hypothesis)))
    final_st = None
    if overlapping:
        final_st = functools.reduce(lambda a, b: join_tvs(a, b), overlapping)
        if final_st is not None:
            final_st = final_st.relax(hypothesis.start, hypothesis.end)

    result: bool = final_st is not None and final_st.lower >= hypothesis.lower and \
        final_st.upper <= hypothesis.upper and final_st.lower_r >= hypothesis.lower_r and \
        final_st.upper_r <= hypothesis.upper_r

    return _feedback(result, hypothesis.to_tuple(var))


def _check_td(var: str, hypothesis: TVStatement) -> bool:
    overlapping = list(filter(lambda x: x.start != hypothesis.end, _td_statements[var].overlap(hypothesis)))
    final_st = None
    if overlapping:
        final_st = functools.reduce(lambda a, b: join_tds(a, b), overlapping)
        final_st.relax(hypothesis.start, hypothesis.end)

    result: bool = final_st is not None and final_st.lower >= hypothesis.lower and final_st.upper <= hypothesis.upper

    return _feedback(result, hypothesis.to_tuple(var))


def _running():
    return any(map(lambda x: x.newly_created, set(_tv_statements.values()) | set(_td_statements.values())))


def _greatest_end(variable: str):
    return max(map(lambda x: x.end, _tv_statements[variable].get_statements()))


def _apply_transitive(variable: str, tv_todo):
    for st_a in tv_todo | set([st.relax(st.start, st.start) for st in tv_todo] + [st.relax(st.end, st.end) for st in tv_todo]) :
        influences = filter(lambda k: k[0] == variable, _vd_statements.keys())

        for k in influences:
            vd_container = _vd_statements[k]
            enveloped_sts = vd_container.envelope(min(st_a.lower, st_a.lower_r), max(st_a.upper, st_a.upper_r))

            for st_b in enveloped_sts:
                new_st = transitivity_rule(st_a, st_b)

                if new_st is not None:
                    _td_statements[k[1]].add(new_st)


def _apply_cd(variable: str, tv_todo, td_todo):
    tv_container = _tv_statements[variable]
    td_container = _td_statements[variable]

    for st_a in set([st.relax(st.start, st.start) for st in tv_todo] + [st.relax(st.end, st.end) for st in tv_todo]):
        if st_a is None:
            continue
        _combine_overlapping(td_container.overlap(st_a), st_a, tv_container, True)

    for st_b in set(td_todo):
        _combine_overlapping(tv_container.overlap(st_b), st_b, tv_container, False)


def _plot(hypothesis):
    plot_statements(_tv_statements, _td_statements, _vd_statements,
                    _tv_statements.keys(), _td_statements.keys(), _vd_statements.keys(), hypothesis)
    show_plot()
