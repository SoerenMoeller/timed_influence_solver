GLUCOSE: str = "glucose"
LIGHT: str = "light"


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (LIGHT,   (0,  6),   (0,  10),  (0, 10)),
        (LIGHT,   (6,  8),   (0,  10),  (15, 20)),
        (LIGHT,   (8,  9),   (15, 20),  (40, 45)),
        (LIGHT,   (9,  10),  (40, 45),  (65, 70)),
        (LIGHT,   (10, 11),  (65, 70),  (90, 95)),
        (LIGHT,   (11, 13),  (90, 95), (90, 95)),
        (LIGHT,   (13, 14),  (90, 95), (65, 70)),
        (LIGHT,   (14, 15),  (65, 70), (40, 45)),
        (LIGHT,   (15, 16),  (40, 45), (15, 20)),
        (LIGHT,   (16, 18),  (15, 20),  (0, 10)),
        (LIGHT,   (18, 24),  (0, 10),   (0, 10)),
        (GLUCOSE, (0, 4),    (20, 25),  (20, 25)),
        (LIGHT,   (0, 20),   (0, 2),    (-10, 0),    GLUCOSE),
        (LIGHT,   (10, 45),  (0, 1.5),  (-2.5, 2.5), GLUCOSE),
        (LIGHT,   (40, 80),  (1.5, 1),  (0, 25),     GLUCOSE),
        (LIGHT,   (60, 100), (1, 1),    (5, 30),     GLUCOSE),
        (LIGHT,   (90, 100), (0, 0.5),  (15, 40),    GLUCOSE),
    }

    hypothesis: dict[str, tuple] = {
        "VD" : (LIGHT,   (0, 20),  (0, 2),   (-10, 0), GLUCOSE),
        "TV" : (GLUCOSE, (16, 18), (2, 175), (-8, 175)),
        "TD" : (GLUCOSE, (15.5, 16), (0, 2.5))
    }

    return statements, hypothesis
