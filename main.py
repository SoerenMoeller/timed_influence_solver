import examples.wolves_sheep_model as wolves_sheep
from solver.solver import solve


def main():
    statements, hypothesis = wolves_sheep.generate_model()

    solve(statements, hypothesis)


if __name__ == "__main__":
    main()
