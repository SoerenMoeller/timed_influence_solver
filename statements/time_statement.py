from collections import namedtuple

# TODO: should time alwasys be positive? / begin at zero


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
    def create_time_statement(self, st: tuple[str, tuple, tuple, tuple]):
        return TimeStatement(st[1][0], st[1][1], st[2][0], st[2][1], st[3][0], st[3][1])

    def __new__(cls, start, end, lower, upper, lower_offset, upper_offset):
        return super(TimeStatement, cls).__new__(cls, start, end, lower, upper, lower_offset, upper_offset)

    def __repr__(self):
        return f"TimeStatement({self.start}, {self.end}, {self.lower}, "  +\
            f"{self.upper}, {self.lower_offset}, {self.upper_offset})"

    __str__ = __repr__
