import bisect
from queue import PriorityQueue

from statements.rectangle_statement import RStatement


class TimeContainer:
    def __init__(self):
        self._queue = PriorityQueue()
        self._statements: list[RStatement] = []

    def __bool__(self):
        return not self._queue.empty()

    def add(self, st: RStatement):
        self._queue.put(st)

    def top(self):
        return self._queue.queue[0] if not self._queue.empty() else None

    def get(self):
        elem = self._queue.get()
        self._statements.append(elem)

        return elem

    def envelope(self, start: float, end: float) -> list:
        return [st for st in self.envelope(start, end) if st.start <= start and st.end >= end]

    def overlap(self, start: float, end: float) -> list:
        """
        Check which statements overlap a given area

        Parameters:
            begin, end (float): [begin, end] interval to check overlap for
        """

        start, end = self._overlapping(start, end)
        if start == end == -1:
            return []
        return self._statements[start:end]

    def _overlapping(self, start, end) -> tuple[int, int]:
        """
        check which statements in a given list overlap a given area

        Parameters:
            statements (list[Statement]): list of normalized statements
            begin, end (float): [begin, end] is the overlapping area

        Returns:
            indices of start and end pos of overlapping statements, or (-1, -1) if none found
        """

        index = bisect.bisect_left(self._statements, RStatement(start, start, 0, 0))

        lower = index
        if index > 0 and len(self._statements) > 0:
            for i in range(index - 1, -1, -1):
                if not self._statements[i].overlaps(start, end):
                    break
                lower = i

        upper = index - 1
        for i in range(index, len(self._statements)):
            if self._statements[i].start > end:
                break
            upper = i

        if upper - lower < 0:
            return -1, -1
        return lower, upper + 1

    def __repr__(self):
        return str(self._statements)

    __str__ = __repr__

    def get_statements(self):
        return self._statements
