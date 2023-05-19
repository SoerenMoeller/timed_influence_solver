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

        index: int = overlap_start - 1 if overlap_start > 0 else overlap_start
        while index < len(self._statements):
            current = self._statements[index]
            changed = False
            print(index)
            if index - 1 >= 0:
                pre = self._statements[index-1]
                if pre.lower_r > current.lower:
                    diff = pre.lower_r - current.lower
                    current.lower += diff
                    current.lower_r += diff
                    changed = True
                if pre.upper_r < current.upper:
                    diff = pre.upper_r - current.upper
                    current.upper -= diff
                    current.upper_r -= diff
                    changed = True
            if index + 1 < len(self._statements):
                suc = self._statements[index+1]
                if suc.lower > current.lower_r:
                    diff = suc.lower - current.lower_r
                    current.lower += diff
                    current.lower_r += diff
                    changed = True
                if suc.upper < current.upper_r:
                    diff = suc.upper - current.upper_r
                    current.upper -= diff
                    current.upper_r -= diff
                    changed = True

            if changed and index != 0:
                index -= 1
            else:
                index += 1
