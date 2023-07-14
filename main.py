import examples.wolves_sheep_model as wolves_sheep
from solver.solver import Solver


def main():
    statements, hypothesis = wolves_sheep.generate_model()

    solver: Solver = Solver(statements)
    solver.solve(hypothesis)


if __name__ == "__main__":
    main()
