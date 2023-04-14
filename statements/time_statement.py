from collections import namedtuple


class TimeStatement(namedtuple('TimeStatement', ['start', 'end', 'lower', 'upper', 'lower_offset', 'upper_offset'])):
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
    __slots__ = ()

    @classmethod
    def create_time_statement(st: tuple[str, float, float, float, float, float, float]):
        return TimeStatement(st[1], st[2], st[3], st[4], st[5], st[6])

    def __new__(cls, start, end, lower, upper, lower_offset, upper_offset):
        return super(TimeStatement, cls).__new__(cls, start, end, lower, upper, lower_offset, upper_offset)

    def __repr__(self):
        return f"TimeStatement({self.start}, {self.end}, {self.lower}, "  +\
            f"{self.upper}, {self.lower_offset}, {self.upper_offset})"

    __str__ = __repr__
