from statements.td_statement import TDStatement
import sympy as sy


class TVStatement(TDStatement):
    """
    Internal representation of time-variable statements
    Visually, this can be interpreted as a trapeze with coordinates:
        (start, lower), (end, lower + lower_offset), (end, upper + upper_offset), (start, upper)

    ----------
    start (float):
        start value of range interval
    end (float):
        end value of range interval
    lower (float):
        start value of domain interval
    upper (float):
        end value of domain interval
    lower_offset (float):
        lower offset for the end value of the range
    upper_offset (float):
        upper offset for the end value of the range
    """

    @classmethod
    def create(cls, st: tuple[str, tuple, tuple, tuple]):
        return TVStatement(st[1][0], st[1][1], st[2][0], st[2][1], st[3][0], st[3][1])

    def __init__(self, start, end, lower, upper, lower_r, upper_r):
        super().__init__(start, end, lower, upper)
        self.lower_r = lower_r
        self.upper_r = upper_r

    def __hash__(self):
        return hash((self.start, self.end, self.lower, self.upper, self.lower_r, self.upper_r))

    def copy(self):
        return TVStatement(self.start, self.end, self.lower, self.upper, self.lower_r, self.upper_r)

    def overlaps(self, start, end=None):
        if end is None:
            return self.overlaps(start.start, start.end)
        return start <= self.end and end >= self.start

    def get_coordinates(self):
        return [(self.start, self.lower), (self.start, self.upper),
                (self.end, self.upper_r),
                (self.end, self.lower_r)]

    def intersect(self, other) -> list:
        cond_1 = self.lower >= other.lower and self.lower_r >= other.lower_r or \
            self.lower <= other.lower and self.lower_r <= other.lower_r
        cond_2 = self.upper >= other.upper and self.upper_r >= other.upper_r or \
            self.upper <= other.upper and self.upper_r <= other.upper_r
        cond_3 = self.upper > other.upper and self.upper_r < other.upper_r or \
            self.upper < other.upper and self.upper_r > other.upper_r
        cond_4 = self.lower > other.lower and self.lower_r < other.lower_r or \
            self.lower < other.lower and self.lower_r > other.lower_r
        if cond_4 and cond_3:  # last case
            lo_l, hi_l, tl = get_lo_hi_l(self, other)
            lo_u, hi_u, tu = get_lo_hi_u(self, other)

            if tl < tu:
                return [TVStatement(self.start, tl,
                                    max(self.lower, other.lower), min(self.upper, other.upper),
                                    lo_l, hi_l),
                        TVStatement(tl, tu,
                                    lo_l, hi_l,
                                    lo_u, hi_u),
                        TVStatement(tu, self.end,
                                    lo_u, hi_u,
                                    max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r))]
            return [TVStatement(self.start, tu,
                                max(self.lower, other.lower), min(self.upper, other.upper),
                                lo_u, hi_u),
                    TVStatement(tu, tl,
                                lo_u, hi_u,
                                lo_l, hi_l),
                    TVStatement(tl, self.end,
                                lo_l, hi_l,
                                max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r))]
        if cond_4 and cond_2:  # second last case
            lo_l, hi_l, tl = get_lo_hi_l(self, other)
            return [TVStatement(self.start, tl,
                                max(self.lower, other.lower), min(self.upper, other.upper),
                                max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r)),
                    TVStatement(tl, self.end,
                                lo_l, hi_l,
                                max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r))]
        if cond_1 and cond_3:  # second case
            lo_u, hi_u, tu = get_lo_hi_u(self, other)
            return [TVStatement(self.start, tu,
                                max(self.lower, other.lower), min(self.upper, other.upper),
                                lo_u, hi_u),
                    TVStatement(tu, self.end,
                                lo_u, hi_u,
                                max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r))]
        if cond_1 and cond_2:  # first case
            return [TVStatement(self.start, self.end,
                                max(self.lower, other.lower), min(self.upper, other.upper),
                                max(self.lower_r, other.lower_r), min(self.upper_r, other.upper_r))]
        return []

    def relax(self, start: float, end: float):
        assert start >= self.start and end <= self.end, "Relaxation not possible"

        f_u = create_lin_function(self.start, self.upper, self.end, self.upper_r)
        f_l = create_lin_function(self.start, self.lower, self.end, self.lower_r)

        return TVStatement(start, end, f_l(start), f_u(start), f_l(end), f_u(end))

    def __repr__(self):
        return f"TVStatement({self.start}, {self.end}, {self.lower}, " + \
            f"{self.upper}, {self.lower_r}, {self.upper_r})"

    __str__ = __repr__


def create_lin_function(x1, y1, x2, y2):
    return lambda x: ((y2 - y1) / (x2 - x1)) * x + y2 - x2 * ((y2 - y1) / (x2 - x1))


def get_lo_hi_l(st_a: TVStatement, st_b: TVStatement) -> tuple[float, float, float]:
    tl = sy.S("tl")
    equation = sy.Eq(st_a.lower + (st_a.lower_r - st_a.lower) * ((tl - st_a.start) / (st_a.end - st_a.start)),
                     st_b.lower + (st_b.lower_r - st_b.lower) * ((tl - st_a.start) / (st_a.end - st_a.start)))
    result = next(filter(lambda x: st_a.start < x < st_a.end, sy.solve(equation)))

    return (
        st_a.lower + (st_a.lower_r - st_a.lower) * ((result - st_a.start) / (st_a.end - st_a.start)),
        min(st_a.upper + (st_a.upper_r - st_a.upper) * ((result - st_a.start) / (st_a.end - st_a.start)),
            st_b.upper + (st_b.upper_r - st_b.upper) * ((result - st_a.start) / (st_a.end - st_a.start))),
        result
    )


def get_lo_hi_u(st_a: TVStatement, st_b: TVStatement) -> tuple[float, float, float]:
    tu = sy.S("tu")
    equation = sy.Eq(st_a.upper + (st_a.upper_r - st_a.upper) * ((tu - st_a.start) / (st_a.end - st_a.start)),
                     st_b.upper + (st_b.upper_r - st_b.upper) * ((tu - st_a.start) / (st_a.end - st_a.start)))
    result = next(filter(lambda x: st_a.start < x < st_a.end, sy.solve(equation)))

    return (
        st_a.upper + (st_a.upper_r - st_a.upper) * ((result - st_a.start) / (st_a.end - st_a.start)),
        max(st_a.lower + (st_a.lower_r - st_a.lower) * ((result - st_a.start) / (st_a.end - st_a.start)),
            st_b.lower + (st_b.lower_r - st_b.lower) * ((result - st_a.start) / (st_a.end - st_a.start))),
        result
    )
