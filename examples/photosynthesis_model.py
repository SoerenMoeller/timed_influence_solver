GLUCOSE: str = "glucose"
LIGHT: str = "light"


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (LIGHT,   (0,  6),   (0,  10),  (0, 10)),
        (LIGHT,   (6,  8),   (0,  10),  (15, 20)),
        (LIGHT,   (8,  11),  (15, 20),  (90, 100)),
        (LIGHT,   (11, 13),  (90, 100), (90, 100)),
        (LIGHT,   (13, 16),  (90, 100), (15, 20)),
        (LIGHT,   (16, 18),  (15, 20),  (0, 10)),
        (LIGHT,   (18, 24),  (0, 10),   (0, 10)),
        (LIGHT,   (0, 15),   (0, 2),    (-10, 0),    GLUCOSE),
        (LIGHT,   (15, 40),  (0, 1.5),  (-2.5, 2.5), GLUCOSE),
        (LIGHT,   (40, 80),  (0, 1),    (0, 25),     GLUCOSE),
        (LIGHT,   (80, 100), (0, 0.5),  (15, 40),    GLUCOSE),
        (GLUCOSE, (0, 2),    (20, 25),  (20, 25),    LIGHT)
    }

    hypothesis: tuple = (LIGHT,  (16, 18), (15, 20),  (0, 10))

    return statements, hypothesis
