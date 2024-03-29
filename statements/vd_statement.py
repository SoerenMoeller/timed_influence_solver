from statements.td_statement import TDStatement


class VDStatement(TDStatement):
    """
    Internal representation of variable-derivative statements
    Visually, this can be interpreted as a rectangle with coordinates:
        (start, lower), (end, lower), (end, upper), (start, upper)

    ----------
    start (float):
        start value of range interval
    end (float):
        end value of range interval
    lower (float):
        start value of domain interval
    upper (float):
        end value of domain interval
    min_slope (float):
        min slope in that area
    max_slope (float):
        max slope in that area
    """
    def __init__(self, start, end, lower, upper, min_slope: float, max_slope: float):
        super().__init__(start, end, lower, upper)
        self.min_slope: float = min_slope
        self.max_slope: float = max_slope

    def __str__(self):
        return f"VDStatement({self.start}, {self.end}, {self.lower}, {self.upper}, {self.min_slope}, {self.max_slope})"

    def __hash__(self):
        return hash((self.start, self.end, self.lower, self.upper, self.min_slope, self.max_slope))

    @classmethod
    def create(cls, st: tuple[str, tuple, tuple, tuple, str]):
        return VDStatement(st[1][0], st[1][1], st[2][0], st[2][1], st[3][0], st[3][1])

    def to_tuple(self, a, b) -> tuple:
        return a, (self.start, self.end), (self.lower, self.upper), (self.min_slope, self.max_slope), b
