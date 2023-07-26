WOLVES: str = "wolves"
SHEEP: str = "sheep"
SQUARE_SIZE: int = 300


def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (SHEEP, (0, 1), (825, 875), (825, 875)),
        (WOLVES, (0, 1), (400, 450), (430, 480)),
        (WOLVES, (0, 100), (1, 3), (40, 40), SHEEP),
        (WOLVES, (100, 200), (1, 3), (30, 30), SHEEP),
        (WOLVES, (200, 300), (1, 3), (20, 20), SHEEP),
        (WOLVES, (300, 400), (1, 3), (10, 10), SHEEP),
        (WOLVES, (400, 500), (1, 3), (0, 0), SHEEP),
        (WOLVES, (500, 600), (1, 3), (0, 0), SHEEP),
        (WOLVES, (600, 700), (1, 3), (-10, -10), SHEEP),
        (WOLVES, (700, 800), (1, 3), (-20, -20), SHEEP),
        (WOLVES, (800, 900), (1, 3), (-30, -30), SHEEP),
        (WOLVES, (900, 1000), (1, 3), (-40, -40), SHEEP),
        (SHEEP, (0, 100), (1, 3), (-40, -40), WOLVES),
        (SHEEP, (100, 200), (1, 3), (-30, -30), WOLVES),
        (SHEEP, (200, 300), (1, 3), (-20, -20), WOLVES),
        (SHEEP, (300, 400), (1, 3), (-10, -10), WOLVES),
        (SHEEP, (400, 500), (1, 3), (0, 0), WOLVES),
        (SHEEP, (500, 600), (1, 3), (0, 0), WOLVES),
        (SHEEP, (600, 700), (1, 3), (10, 10), WOLVES),
        (SHEEP, (700, 800), (1, 3), (20, 20), WOLVES),
        (SHEEP, (800, 900), (1, 3), (30, 30), WOLVES),
        (SHEEP, (900, 1000), (1, 3), (40, 40), WOLVES)
    }

    hypothesis: tuple = (SHEEP, (5, 10), (450, 550), (450, 550))    # False
    #hypothesis: tuple = (SHEEP, (5, 10), (740, 810), (490, 560))    # True

    return statements, hypothesis
