from collections import namedtuple


class InfluenceStatement(namedtuple('InfluenceStatement', ['start', 'end', 'lower', 'upper', 'min_pitch', 'max_pitch'])):
    """
    Internal representation of influence-statements. Those represent the influence of a variable
    (in interval [start, end]) on the derivation of another variable [min_pitch, max_pitch]. This influence
    is valid for the relative time period [lower, upper].
    Visually, this can be interpreted as an rectangle with coordinates:
        (start, lower), (end, lower ), (end, upper), (start, upper)

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
    min_pitch (float):
        min value of the derivation
    max_pitch (float):
        max value of the derivation
    """
    __slots__ = ()

    @classmethod
    def create_influence_statement(self, st: tuple[str, tuple, tuple, tuple, str]):
        return InfluenceStatement(st[1][0], st[1][1], st[2][0], st[2][1], st[3][0], st[3][1])

    def __new__(cls, start, end, lower, upper, min_pitch, max_pitch):
        return super(InfluenceStatement, cls).__new__(cls, start, end, lower, upper, min_pitch, max_pitch)

    def __repr__(self):
        return f"InfluenceStatement({self.start}, {self.end}, {self.lower}, "  +\
            f"{self.upper}, {self.min_pitch}, {self.max_pitch})"

    def __eq__(self, other):
        return all(getattr(self, fld) == getattr(other, fld) for fld in self._fields)

    def __hash__(self):
        return hash(getattr(self, fld) for fld in self._fields)

    def __cmp__(self, other):
        if self.start != other.start:
            return -1 if self.start < other.start else 1
        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    __str__ = __repr__
