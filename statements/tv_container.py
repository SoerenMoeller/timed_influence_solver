import bisect

from statements.container_base import ContainerBase
from statements.tv_statement import TVStatement


class TVContainer(ContainerBase):
    def contains(self, index: int, statement: TVStatement):
        return index < len(self._statements) and self._statements[index] == statement

    def add(self, statement: TVStatement):
        if statement == TVStatement(1, 3, 1050.0, 1150.0, 950.0, 1050.0):
            print("hi")

        index: int = bisect.bisect_left(self._statements, statement)
        if self.contains(index, statement):
            return

        overlap_start, overlap_end = self._get_overlap(statement, index)
        if overlap_start == overlap_end == -1:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        o = self._statements[overlap_start:overlap_end]
        overlapping: list[TVStatement] = [st for st in o if st.start != statement.end]
        diff = len(o) - len(overlapping)
        if not overlapping:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        result: list[TVStatement] = []
        first: TVStatement = overlapping[0]
        if first.start < statement.start:
            result.append(first.relax(first.start, statement.start))
            first.start = statement.start
        elif statement.start < first.start:
            result.append(statement.relax(statement.start, first.start))

        for st in overlapping:
            trimmed: TVStatement = statement.relax(st.start, st.end)
            if trimmed.start != trimmed.end:
                result += trimmed.intersect(st)

        last: TVStatement = overlapping[-1]
        if last.end < statement.end:
            u = statement.relax(last.end, statement.end)
            if u.lower_r == u.upper_r:
                print("hi")

            result.append(statement.relax(last.end, statement.end))
        elif statement.end < last.end:
            u = last.relax(statement.end, last.end)
            if u.lower_r == u.upper_r:
                print("hi")

            result.append(last.relax(statement.end, last.end))

        self._statements = self._statements[:overlap_start] + result + self._statements[overlap_end-diff:]
        self.newly_created.update(result)

        index: int = overlap_start - 1 if overlap_start > 0 else overlap_start
        # current is fucked up here lol
        while index < len(self._statements):
            current = self._statements[index]
            changed = False
            if index - 1 >= 0:
                pre = self._statements[index-1]
                if pre.lower_r > current.lower:
                    diff = pre.lower_r - current.lower
                    current.lower += diff
                    current.lower_r += diff
                    changed = True
                if pre.upper_r < current.upper:
                    diff = pre.upper_r - current.upper
                    current.upper += diff
                    current.upper_r += diff
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
                    current.upper += diff
                    current.upper_r += diff
                    changed = True

            if changed:
                self.newly_created.add(current)
                if index != 0:
                    index -= 1
            else:
                index += 1
