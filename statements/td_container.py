import bisect

from statements.container_base import ContainerBase
from statements.td_statement import TDStatement


class TDContainer(ContainerBase):
    def add(self, statement: TDStatement):
        index: int = bisect.bisect_left(self._statements, statement)
        overlap_start, overlap_end = self._get_overlap(statement, index)

        if overlap_start == overlap_end == -1:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        overlapping: list[TDStatement] = self._statements[overlap_start:overlap_end]

        result: list[TDStatement] = []
        first: TDStatement = overlapping[0]
        if first.start < statement.start:
            result.append(TDStatement(first.start, statement.start, first.lower, first.upper))
        elif statement.start < first.start:
            result.append(TDStatement(statement.start, first.start, first.lower, first.upper))

        for st in overlapping:
            result.append(st.intersect(statement))

        last: TDStatement = overlapping[-1]
        if last.end < statement.end:
            result.append(TDStatement(last.end, statement.end, statement.lower, statement.upper))
        elif statement.end < last.end:
            result.append(TDStatement(statement.end, last.end, last.lower, last.upper))

        self._statements = self._statements[:overlap_start] + result + self._statements[overlap_end:]
        self.newly_created.update(result)

