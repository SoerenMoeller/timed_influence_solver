from typing import Union

from statements.vd_statement import IStatement
from statements.td_statement import RStatement
from statements.tv_statement import TStatement


def transitivity_rule(st_a: RStatement, st_b: IStatement) -> Union[RStatement, None]:
    if not _envelopes((st_b.start, st_b.end), (st_a.lower, st_a.upper)):
        return None

    return RStatement(
        st_a.start + st_b.lower, st_a.end + st_b.upper, st_b.min_slope, st_b.max_slope)


def smallest_rectangle_rule(st: TStatement) -> RStatement:
    return RStatement(
        st.start, st.end,
        min(st.lower, st.lower + (st.start - st.end) * st.lower_r),
        max(st.upper, st.upper + (st.end - st.start) * st.upper))


def cdi_rule(st_a: TStatement, st_b: RStatement) -> Union[TStatement, None]:
    if not _overlaps((st_a.start, st_a.end), (st_b.start, st_b.end)):
        return None

    overlap_iv: tuple[float, float] = max(st_a.start, st_b.start), min(st_a.end, st_b.end)
    return TStatement(overlap_iv[0], overlap_iv[1], st_a.lower, st_a.upper,
                      max(st_a.lower_r, st_b.lower), min(st_a.upper_r, st_b.upper))


def cdr_rule(st_a: RStatement, st_b: RStatement) -> Union[TStatement, None]:
    if not st_b.start <= st_a.start <= st_b.end:
        return None

    return TStatement(st_b.start, st_b.end, st_a.lower, st_a.upper, st_b.lower, st_b.upper)


# helper functions
def _envelopes(fst: tuple[float, float], snd: tuple[float, float]) -> bool:
    return fst[0] <= snd[0] and fst[1] >= snd[1]


def _overlaps(fst: tuple[float, float], snd: tuple[float, float]) -> bool:
    return fst[0] <= snd[1] and fst[1] >= snd[0]
