C2H5OH: str = "C2H5OH"
O2: str = "O2"
CO2: str = "CO2"
H2O: str = "H2O"
CELSIUS: str = "°C"


# This should model the reaction C2H5OH + 3 02 -> 2 CO2 + 3 H20
# t -> C2H5OH and t -> O2 show how much of them is consumed over time while
# t -> CO2 and t -> H2O show much of them is created
def generate_model() -> tuple[set, tuple]:
    statements: set[tuple] = {
        (H2O, (0, 1), (0, 15), (0, 15)),
        (CO2, (0, 1), (0, 10), (0, 10)),
        (C2H5OH, (0, 1), (0, 5), (0, 5)),
        (O2, (0, 1), (0, 15), (0, 15)),
        (CELSIUS, (0, 5), (18, 22), (18, 22)),
        (CELSIUS, (5, 10), (18, 22), (26, 30)),
        (CELSIUS, (10, 20), (26, 30), (54, 60)),
        (CELSIUS, (20, 40), (54, 60), (68, 75)),
        (CELSIUS, (40, 80), (68, 75), (95, 105)),
        (CELSIUS, (80, 140), (95, 105), (115, 130)),
        (CELSIUS, (140, 200), (115, 130), (115, 130)),
        (CELSIUS, (18, 30), (0, 10), (1, 1), C2H5OH),
        (CELSIUS, (18, 30), (1, 10), (1, 1), H2O),
        (CELSIUS, (18, 30), (1, 10), (1, 1), O2),
        (CELSIUS, (18, 30), (1, 10), (1, 1), CO2),
        (CELSIUS, (26, 60), (10, 10), (1, 1), C2H5OH),
        #(CELSIUS, (26, 30), (54, 60)),
        #(CELSIUS, (54, 60), (68, 75)),
        #(CELSIUS, (68, 75), (95, 105)),
        #(CELSIUS, (95, 105), (115, 130)),
        #(CELSIUS, (115, 130), (115, 130)),
    }
    # TODO: Continue

    hypothesis: tuple = (C2H5OH,  (16, 18), (15, 20),  (0, 10))

    return statements, hypothesis
