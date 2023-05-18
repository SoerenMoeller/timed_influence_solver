from statements.td_statement import TDStatement


class TVStatement(TDStatement):
    """
    Internal representation of statements
    Visually, this can be interpreted as an trapeze with coordidinates:
        (start, lower), (end, lower + lower_offset), (end, upper + upper_offset), (start, upper)

    namedtuple
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

    def __init__(self, start, end, lower, upper, slope_lower, slope_upper):
        super().__init__(start, end, lower, upper)
        self.slope_lower = slope_lower
        self.slope_upper = slope_upper

    def __hash__(self):
        return hash((self.start, self.end, self.lower, self.upper, self.slope_lower, self.slope_upper))

    def overlaps(self, start, end=None):
        if end is None:
            return self.overlaps(start.start, start.end)
        return start <= self.end and end >= self.start

    def get_coordinates(self):
        return [(self.start, self.lower), (self.start, self.upper),
                (self.end, self.upper + (self.end - self.start) * self.slope_upper),
                (self.end, self.lower + (self.end - self.start) * self.slope_lower)]

    def intersect(self, other):
        # lo_l = l_1 + (l_2 - l_1) * (tl-t2)/(t2-t1) = l_1' + (l_2' - l_1') * (tl-t1)/(t2-t1)
        #      = (l_1 + (l_2 - l_1) * (tl-t2)/(t2-t1) - l_1')/(l_2' - l_1') * (t2-t1) + t1 = tl
        pass

    def __repr__(self):
        return f"TVStatement({self.start}, {self.end}, {self.lower}, " +\
            f"{self.upper}, {self.slope_lower}, {self.slope_upper})"

    __str__ = __repr__
