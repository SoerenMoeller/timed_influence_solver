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
    def create_influence_statement(st: tuple[str, float, float, float, float, float, float, str]):
        return InfluenceStatement(st[1], st[2], st[3], st[4], st[5], st[6])

    def __new__(cls, start, end, lower, upper, min_pitch, max_pitch):
        return super(InfluenceStatement, cls).__new__(cls, start, end, lower, upper, min_pitch, max_pitch)

    def __repr__(self):
        return f"InfluenceStatement({self.start}, {self.end}, {self.lower}, "  +\
            f"{self.upper}, {self.min_pitch}, {self.max_pitch})"

    __str__ = __repr__
