import examples.photosynthesis_model as photosynthesis_model
from solver.csv_reader import read_csv
from solver.solver import solve

# there are hypothesis for TV, VD and TD statements available

def main():
    statements, hypothesis = photosynthesis_model.generate_model()
    solve(statements, hypothesis["TD"], k_mode=True, k=15)      # Use "TV", "VD" or "TD"
    # solve(statements, hypothesis["TV"], k_mode=False)  # do not set an upper bound k

    # CSV reader example
    model = read_csv("example_csv")
    hypo = ("a", (0, 4), (0, 4), (0, 4))
    # solve(model, hypo)


if __name__ == "__main__":
    main()
