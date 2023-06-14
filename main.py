from plotter.plotter import plot_statements
from solver.solver import Solver
import examples.wolves_sheep_model as wolves_sheep
from statements.tv_container import TVContainer
from statements.tv_statement import TVStatement


def main():
    statements, hypothesis = wolves_sheep.generate_model()

    solver: Solver = Solver(statements)
    solver.solve(hypothesis)
    #st_a = TVStatement(1, 3, 1, 2, 1, 3)
    #st_b = TVStatement(1, 3, 1, 3, 1, 2)
    #isect = st_a.intersect(st_b)
    #print(isect)
    #print(st_a.relax(1.5, 2))

    #statements = {
    #    ("a", (0, 2), (1, 2), (0, 1), "b'"),
    #    ("a", (1, 3), (1, 3), (1, 2), "b'"),
    #    ("a", (0, 1), (0.2, 1.1), (1, 3), "b'")
    #}
    #solver = Solver(statements)
    #solver.solve(("a", (0, 10), (-3, 5), "b'"))
    #st_a = TVStatement(1, 2, 1, 3, 0.5, 3.5)
    #st_b = TVStatement(1.5, 2.5, 1.5, 3, 1, 4)
    #st_c = TVStatement(0.5, 3, 1.5, 2.5, 0.25, 3)

    #class CN:
    #    def __init__(self):
    #        self._sts = []
    #    def add(self, st):
    #        self._sts.append(st)
    #    def get_statements(self):
    #        return self._sts

    #container = CN()
    #container.add(st_a)
    #container.add(st_b)
    #container.add(st_c)


    #plot_statements({"x": container}, {"x"})

    #print(container)
    #st_0 = ("a", (1, 2), (1, 3), (.5, 3.5))
    #st_1 = ("a", (1.5, 2.5), (1.5, 3), (1, 4))
    #st_2 = ("a", (.5, 3), (1.5, 2.5), (0.25, 3))
    #h = ("a", (1, 4), (0, 5), (0, 4))
    #solver = Solver()
    #solver.add(st_0)
    #solver._plot(h)
    #solver.add(st_1)
    #solver._plot(h)
    #solver.add(st_2)
    #solver._plot(h)


if __name__ == "__main__":
    main()
