WOLVES: str = "wolves"
SHEEP: str = "sheep"
SQUARE_SIZE: int = 300


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (SHEEP,  (0,   1),   (800, 900), (800, 900)),
        (WOLVES, (0,   1),   (500, 600), (500, 600)),
        (SHEEP,  (350, 450), (0,   1),   (-200, -200), WOLVES),
        (SHEEP,  (550, 650), (0,   1),   (-100, -100), WOLVES),
        (SHEEP,  (700, 800), (0,   1),   (100,  100),  WOLVES),
        (SHEEP,  (800, 900), (1,   1),   (100,  100),  WOLVES),
        (WOLVES, (500, 600), (1,   1),   (0,    0),    SHEEP),
        (WOLVES, (600, 700), (0,   1),   (-100, -100), SHEEP),
        (WOLVES, (700, 800), (0,   1),   (-150, -150), SHEEP),
        (WOLVES, (800, 900), (0,   1),   (-200, -200), SHEEP),
    }

    hypothesis: tuple = (SHEEP, (5, 10), (450, 550), (450, 550))    # False
    # hypothesis: tuple = (SHEEP, (5, 10), (740, 810), (490, 560))    # True

    return statements, hypothesis
