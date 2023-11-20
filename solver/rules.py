from typing import Union

from statements.vd_statement import VDStatement
from statements.td_statement import TDStatement
from statements.tv_statement import TVStatement


def transitivity_rule(st_a: TDStatement, st_b: VDStatement) -> Union[TDStatement, None]:
    if not _envelopes((st_b.start, st_b.end), (st_a.lower, st_a.upper)):
        return None

    return TDStatement(
        st_a.start + st_b.lower, st_a.end + st_b.upper, st_b.min_slope, st_b.max_slope)


def smallest_rectangle_rule(st: TVStatement) -> TDStatement:
    return TDStatement(
        st.start, st.end,
        min(st.lower, st.lower + (st.start - st.end) * st.lower_r),
        max(st.upper, st.upper + (st.end - st.start) * st.upper))


def cdl_rule(st_a: TVStatement, st_b: TDStatement) -> Union[TVStatement, None]:
    if not st_a.start <= st_b.end <= st_a.end or st_b.start == st_a.start:
        return None

    st_b_cpy = st_b.copy()
    st_b_cpy.relax(st_b.start, st_a.start)
    if st_b_cpy is None:
        return None

    return TVStatement(st_b_cpy.start, st_b_cpy.end,
                       st_a.lower - (st_b_cpy.end - st_b_cpy.start) * st_b_cpy.upper,
                       st_a.upper - (st_b_cpy.end - st_b_cpy.start) * st_b_cpy.lower,
                       st_a.lower, st_a.upper)


def cdr_rule(st_a: TVStatement, st_b: TDStatement) -> Union[TVStatement, None]:
    if not st_a.start <= st_b.end <= st_a.end or st_a.end == st_b.end:
        return None

    st_b_cpy = st_b.copy()
    st_b_cpy.relax(st_a.end, st_b.end)
    if st_b_cpy is None:
        return None

    return TVStatement(st_b_cpy.start, st_b_cpy.end,
                       st_a.lower_r, st_a.upper_r,
                       st_a.lower_r + (st_b_cpy.end - st_b_cpy.start) * st_b_cpy.lower,
                       st_a.upper_r + (st_b_cpy.end - st_b_cpy.start) * st_b_cpy.upper)


def join_tvs(st_a: TVStatement, st_b: TVStatement) -> Union[None, TVStatement]:
    if st_a is None:
        return st_b

    if st_a.end != st_b.start:
        return None

    l: float = st_a.lower + (st_b.lower_r - st_a.lower) * (st_a.end-st_a.start)/(st_b.end-st_a.start)
    u: float = st_a.upper + (st_b.upper_r - st_a.upper) * (st_a.end-st_a.start)/(st_b.end-st_a.start)

    if not (u >= st_a.upper_r and u >= st_b.upper and l <= st_a.lower_r and l <= st_b.lower):
        return None

    return TVStatement(st_a.start, st_b.end, st_a.lower, st_a.upper, st_b.lower_r, st_b.upper_r)


def join_tds(st_a: TDStatement, st_b: TDStatement) -> Union[None, TDStatement]:
    if st_a is None:
        return st_b

    if st_a.end != st_b.start:
        return None

    return TDStatement(min(st_a.start, st_b.start), max(st_a.end, st_b.end),
                       min(st_a.lower, st_b.lower), max(st_a.upper, st_b.upper))


# helper functions
def _envelopes(fst: tuple[float, float], snd: tuple[float, float]) -> bool:
    return fst[0] <= snd[0] and fst[1] >= snd[1]
