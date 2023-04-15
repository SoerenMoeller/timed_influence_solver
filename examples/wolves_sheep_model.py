WOLVES: str = "wolves"
SHEEP: str = "sheep"
SQUARE_SIZE: int = 50

def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (SHEEP, (0, 1), (950, 1050), (0, 0)),
        (WOLVES, (0, 1), (50, 150), (0, 0))
    }

    statements |= {(SHEEP, (i, i + SQUARE_SIZE), (0, 2), (1, 1), WOLVES) for i in range(0, 2000, SQUARE_SIZE)}
    statements |= {(WOLVES, (i, i + SQUARE_SIZE), (0, 2), (-1, -1), SHEEP) for i in range(0, 2000, SQUARE_SIZE)}

    hyptothesis: tuple = (SHEEP, (95, 100), (450, 550), (0, 0))

    return statements, hyptothesis
