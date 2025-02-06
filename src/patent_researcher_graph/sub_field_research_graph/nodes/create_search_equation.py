class CreateSearchEquation:
    def __init__(self, search_equation: str = "dummy search equation"):
        self.search_equation = search_equation

    def run(self, state, config=None) -> dict:
        # Simply return the dummy search equation.
        return {"search_equation": self.search_equation}
