import bisect

from statements.tv_statement import TVStatement


class TVContainer:
    def __init__(self):
        self._statements: list[TVStatement] = []

    def add(self, statement: TVStatement):
        index: int = bisect.bisect(self._statements, statement)
        overlap_start, overlap_end = self._get_overlap(statement, index)

    def _get_overlap(self, statement: TVStatement, index: int) -> tuple[int, int]:
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
