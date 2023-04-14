from solver.solver import Solver


def main():
    i_st = ("a", 1, 2, 1, 2, 0, 1, "b")
    t_st = ("a", 1, 2, 1, 2, 0, 0)

    solver: Solver = Solver()
    solver.add(i_st)
    solver.add(t_st)
    print(solver)

    solver.solve()


if __name__ == "__main__":
    main()
