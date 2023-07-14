from statements.vd_statement import VDStatement

# Maybe order to access more efficiently and memorize more


class VDContainer:
    def __init__(self):
        self._statements: set[VDStatement] = set()
        self._normalized = []
        self._overlap_map: dict[float, set[VDStatement]] = {}
        self._s_points: list[float] = []

    def add(self, st: VDStatement):
        self._statements.add(st)

    def get_statements(self):
        return list(self._statements)

    def envelope(self, start: float, end: float) -> set:
        return {st for st in self._statements if st.start <= start and st.end >= end}

    # TODO: create map for overlapping bounds, for faster overlapping (bisect of overlap bounds, union of all found)
