import bisect


class ContainerBase:
    def __init__(self):
        self._statements = []
        self.newly_created = set()

    def clear_new(self):
        self.newly_created.clear()

    def overlap(self, statement):
        index: int = bisect.bisect_left(self._statements, statement)
        s, e = self._get_overlap(statement, index)

        if s == -1 and e == -1:
            return []
        return self._statements[s:e]

    def _get_overlap(self, statement, index: int) -> tuple[int, int]:
        lower = index
        if index > 0 and len(self._statements) > 0:
            for i in range(index - 1, -1, -1):
                if not self._statements[i].overlaps(statement):
                    break
                lower = i

        upper = index - 1
        for i in range(index, len(self._statements)):
            if self._statements[i].start > statement.end:
                break
            upper = i

        if upper - lower < 0:
            return -1, -1
        return lower, upper + 1

    def get_statements(self):
        return self._statements

    def __repr__(self):
        return str(self._statements)

    __str__ = __repr__
