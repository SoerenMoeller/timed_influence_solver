import examples.wolves_sheep_model as wolves_sheep
from solver.solver import solve


def main():
    statements, hypothesis = wolves_sheep.generate_model()

    solve(statements, hypothesis, k_mode=True, k=15) # tv hypothesis
    # solve(statements, hypothesis, k_mode=False)
    # solve(statements, ("wolves", (10, 200), (0.5, 1.5), (-40, -40), "sheep")) # vd hypothesis
    # solve(statements, ("wolves", (0, 5), (50, 50))) # td hypothesis


if __name__ == "__main__":
    main()
