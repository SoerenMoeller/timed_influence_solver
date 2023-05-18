import bisect

from statements.vd_statement import VDStatement


class VDContainer:
    def __init__(self):
        self._statements: set[VDStatement] = set()
        self._normalized = []
        self._overlap_map: dict[float, set[VDStatement]] = {}
        self._s_points: list[float] = []

    def add(self, st: VDStatement):
        self._statements.add(st)

    def get_statements(self):
        return [st for sts in self._normalized for st in sts]

    def init(self):
        # init bounds
        self._s_points, self._overlap_map = construct_map(self._statements)

        for i in range(len(self._s_points) - 1):
            point: float = self._s_points[i]
            if not self._overlap_map[point]:
                continue

            next_point: float = self._s_points[i + 1]
            s_points, o_map = construct_map(self._overlap_map[point], x=False)

            sts = {
                VDStatement(point, next_point, s_points[j], s_points[j+1],
                           max(map(lambda st: st.min_slope, o_map[s_points[j]])),
                           min(map(lambda st: st.max_slope, o_map[s_points[j]])))
                for j in range(len(s_points) - 1)
                if o_map[s_points[j]]
            }
            self._normalized.append(sts)

    def overlap(self, start: float, end: float) -> list:
        i, j = get_overlap_index(self._s_points, start, end)
        return self._normalized[i:j]

    def envelope(self, start: float, end: float) -> list:
        e = [st for st in self.overlap(start, end) if next(iter(st)).start <= start and next(iter(st)).end >= end]
        return e[0] if e else None


def construct_map(sts, x=True):
    points = set()
    overlap_map = {}
    for st in sts:
        start = st.start if x else st.lower
        end = st.end if x else st.upper
        points.update({start, end})

        if start not in overlap_map:
            overlap_map[start] = set()
        if end not in overlap_map:
            overlap_map[end] = set()
        overlap_map[start].add(st)
        overlap_map[end].add(st)

    s_points: list[float] = sorted(points)
    collect = set()
    for bound in s_points:
        to_remove = set(filter(lambda s: (s.end if x else s.upper) == bound, collect))
        collect.difference_update(to_remove)
        overlap_map[bound].difference_update(to_remove)

        overlap_map[bound].update(collect)
        collect.update(overlap_map[bound])

    return s_points, overlap_map


def get_overlap_index(boundaries: list[float], begin, end=None) -> tuple[int, int]:
    if end is None:
        return get_overlap_index(boundaries, begin.begin, begin.end)

    left: int = bisect.bisect_left(boundaries, begin)
    if left > 0:
        left -= 1
    right: int = bisect.bisect_right(boundaries, end)
    return left, right
