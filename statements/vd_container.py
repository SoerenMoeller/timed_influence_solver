from statements.vd_statement import VDStatement


class VDContainer:
    def __init__(self):
        self._statements: set[VDStatement] = set()

    def add(self, st: VDStatement):
        self._statements.add(st)

    def get_statements(self):
        return list(self._statements)

    def envelope(self, start: float, end: float) -> set:
        return {st for st in self._statements if st.start <= start and st.end >= end}
