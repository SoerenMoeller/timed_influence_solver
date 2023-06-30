WOLVES: str = "wolves"
SHEEP: str = "sheep"
SQUARE_SIZE: int = 300


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (SHEEP, (0, 1), (950, 1050), (950, 1050)),
        (WOLVES, (0, 1), (50, 150), (50, 150))
    }

    statements |= {(SHEEP, (i, i + SQUARE_SIZE), (0, 2), (50, 50), WOLVES) for i in range(0, 2000, SQUARE_SIZE)}
    statements |= {(SHEEP, (i, i + SQUARE_SIZE), (0, 2), (50, 50), WOLVES) for i in range(SQUARE_SIZE//3, 2000, SQUARE_SIZE)}
    statements |= {(WOLVES, (i, i + SQUARE_SIZE), (0, 2), (-50, -50), SHEEP) for i in range(0, 2000, SQUARE_SIZE)}

    hypothesis: tuple = (SHEEP, (5, 10), (450, 550), (450, 550))    # False
    #hypothesis: tuple = (SHEEP, (5, 10), (740, 810), (490, 560))    # True

    return statements, hypothesis