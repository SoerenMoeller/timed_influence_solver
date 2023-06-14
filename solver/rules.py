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
    if not st_b.start <= st_a.start <= st_b.end:
        return None

    st_a_cpy = st_a.copy()
    st_a_cpy.relax(st_a.start, st_b.start)

    return TVStatement(st_b.start, st_b.end,
                       st_a_cpy.lower + (st_b.end - st_b.start) * st_b.upper,
                       st_a_cpy.upper + (st_b.end - st_b.start) * st_b.lower,
                       st_a_cpy.lower, st_a_cpy.upper)


def cdr_rule(st_a: TVStatement, st_b: TDStatement) -> Union[TVStatement, None]:
    if not st_b.start <= st_a.start <= st_b.end:
        return None

    st_a_cpy = st_a.copy()
    st_a_cpy.relax(st_a.start, st_b.start)

    return TVStatement(st_b.start, st_b.end,
                       st_a_cpy.lower_r, st_a_cpy.upper_r,
                       st_a_cpy.lower_r + (st_b.end - st_b.start) * st_b.lower,
                       st_a_cpy.upper_r + (st_b.end - st_b.start) * st_b.upper)


# helper functions
def _envelopes(fst: tuple[float, float], snd: tuple[float, float]) -> bool:
    return fst[0] <= snd[0] and fst[1] >= snd[1]


def _overlaps(fst: tuple[float, float], snd: tuple[float, float]) -> bool:
    return fst[0] <= snd[1] and fst[1] >= snd[0]
