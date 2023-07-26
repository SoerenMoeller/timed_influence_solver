WOLVES: str = "wolves"
SHEEP: str = "sheep"
SQUARE_SIZE: int = 300


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (SHEEP, (0, 1), (800, 900), (800, 900)),
        (WOLVES, (0, 1), (400, 500), (400, 500)),
        (SHEEP, (800, 900), (1, 1), (50, 50), WOLVES),
        (WOLVES, (400, 500), (1, 1), (0, 0), SHEEP),
        (WOLVES, (450, 600), (1, 1), (-30, -30), SHEEP)
    }

    hypothesis: tuple = (SHEEP, (5, 10), (450, 550), (450, 550))    # False
    # hypothesis: tuple = (SHEEP, (5, 10), (740, 810), (490, 560))    # True

    return statements, hypothesis
