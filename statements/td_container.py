import bisect

from statements.container_base import ContainerBase
from statements.td_statement import TDStatement


class TDContainer(ContainerBase):
    def contains(self, index: int, statement: TDStatement):
        return index < len(self._statements) and self._statements[index] == statement

    def add(self, statement: TDStatement):
        # check where to insert
        index: int = bisect.bisect_left(self._statements, statement)
        if self.contains(index, statement):
            return

        overlap_start, overlap_end = self._get_overlap(statement, index)

        # no overlapping ones found
        if overlap_start == overlap_end == -1:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        overlapping: list[TDStatement] = [st for st in self._statements[overlap_start:overlap_end] if st.start != statement.end and st.end != statement.start]
        if not overlapping:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        # insert statement and normalize, by pruning statements and intersecting them to prevent overlaps
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

        self._statements = sorted(set(self._statements) - set(overlapping) | set(result))
        self.newly_created.update(result)
