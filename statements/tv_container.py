import bisect

from statements.container_base import ContainerBase
from statements.tv_statement import TVStatement


class TVContainer(ContainerBase):
    def add(self, statement: TVStatement):
        index: int = bisect.bisect(self._statements, statement)
        overlap_start, overlap_end = self._get_overlap(statement, index)

        if overlap_start == overlap_end == -1:
            return self._statements.insert(index, statement)

        overlapping: list[TVStatement] = self._statements[overlap_start:overlap_end]

        result: list[TVStatement] = []
        first: TVStatement = overlapping[0]
        if first.start < statement.start:
            result.append(first.relax(first.start, statement.start))
            first.start = statement.start
        elif statement.start < first.start:
            result.append(statement.relax(statement.start, first.start))

        for st in overlapping:
            trimmed: TVStatement = statement.relax(st.start, st.end)
            result += trimmed.intersect(st)

        last: TVStatement = overlapping[-1]
        if last.end < statement.end:
            result.append(statement.relax(last.end, statement.end))
        elif statement.end < last.end:
            result.append(last.relax(statement.end, last.end))

        self._statements = self._statements[:overlap_start] + result + self._statements[overlap_end:]

        # TODO: normalize

