from solver.solver import Solver
import examples.wolves_sheep_model as wolves_sheep

def main():
    statements, hypothesis = wolves_sheep.generate_model()

    solver: Solver = Solver(statements)
    solver.solve(hypothesis)

    #statements = {
    #    ("a", (0, 2), (1, 2), (0, 1), "b'"),
    #    ("a", (1, 3), (1, 3), (1, 2), "b'"),
    #    ("a", (0, 1), (0.2, 1.1), (1, 3), "b'")
    #}
    #solver = Solver(statements)
    #solver.solve(("a", (0, 10), (-3, 5), "b'"))


if __name__ == "__main__":
    main()
