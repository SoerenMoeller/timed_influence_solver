from collections import namedtuple


class TDStatement:
    """
    Internal representation of time-derivative statements.
    Visually, this can be interpreted as a rectangle with coordinates:
        (start, lower), (end, lower ), (end, upper), (start, upper)

    ----------
    start (float):
        start value of range interval
    end (float):
        end value of range interval
    lower (float):
        start value of domain interval
    upper (float):
        end value of domain interval
    """

    @classmethod
    def create(cls, st: tuple[str, tuple, tuple, str]):
        return TDStatement(st[1][0], st[1][1], st[2][0], st[2][1])

    def __init__(self, start, end, lower, upper):
        self.start = start
        self.end = end
        self.lower = lower
        self.upper = upper

    def overlaps(self, start, end=None):
        if end is None:
            return self.overlaps(start.start, start.end)
        return start <= self.end and end >= self.start

    def intersect(self, other):
        return TDStatement(
            max(self.start, other.start), min(self.end, other.end),
            max(self.lower, other.lower), min(self.upper, other.upper))

    def copy(self):
        return TDStatement(self.start, self.end, self.lower, self.upper)

    def relax(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"TDStatement({self.start}, {self.end}, {self.lower}, {self.upper})"

    def __eq__(self, other):
        return all(getattr(self, fld) == getattr(other, fld) for fld in ["start", "end", "lower", "upper"])

    def __hash__(self):
        return hash((self.start, self.end, self.lower, self.upper))

    def __cmp__(self, other):
        if self.start != other.start:
            return -1 if self.start < other.start else 1
        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    __str__ = __repr__
