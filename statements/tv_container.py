import bisect

from statements.container_base import ContainerBase
from statements.tv_statement import TVStatement


class TVContainer(ContainerBase):
    def contains(self, index: int, statement: TVStatement):
        return index < len(self._statements) and self._statements[index] == statement

    def add(self, statement: TVStatement):
        # check where to insert
        index: int = bisect.bisect_left(self._statements, statement)
        if self.contains(index, statement):
            return

        overlap_start, overlap_end = self._get_overlap(statement, index)
        if overlap_start == overlap_end == -1:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        # get all overlapping statements (inclusive start point, exclusive end point)
        o = self._statements[overlap_start:overlap_end]
        overlapping: list[TVStatement] = [st for st in o if st.start != statement.end]
        diff = len(o) - len(overlapping)
        if not overlapping:
            self.newly_created.add(statement)
            return self._statements.insert(index, statement)

        # insert statement while normalizing the model, by pruning and intersecting statements
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
            result.append(statement.relax(last.end, statement.end))
        elif statement.end < last.end:
            result.append(last.relax(statement.end, last.end))

        result = sorted(set(result))

        self._statements = self._statements[:overlap_start] + result + self._statements[overlap_end-diff:]
        self.newly_created.update(result)

        # adapt upper and lower borders to match with predecessor and successor
        index: int = overlap_start - 1 if overlap_start > 0 else overlap_start
        while index < len(self._statements):
            current = self._statements[index]
            changed = False

            if index - 1 >= 0:
                pre = self._statements[index - 1]
                if adapt_bounds(current, pre, True):
                    changed = True
            if index + 1 < len(self._statements):
                suc = self._statements[index + 1]
                if adapt_bounds(current, suc, False):
                    changed = True

            if changed:
                self.newly_created.add(current)
                if index != 0:
                    index -= 1
            else:
                index += 1


def adapt_bounds(current, other, left: bool):
    lower_cond = other.lower_r > current.lower if left else other.lower > current.lower_r
    upper_cond = other.upper_r < current.upper if left else other.upper < current.upper_r

    if lower_cond:
        diff = abs(other.lower_r - current.lower)
        current.lower += diff
        current.lower_r += diff
    if upper_cond:
        diff = -abs(other.upper_r - current.upper)
        current.upper += diff
        current.upper_r += diff

    return lower_cond or upper_cond
