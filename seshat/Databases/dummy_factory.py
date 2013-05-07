"""Pretends to be a factory, but does nothing."""

class factory:
    """A factory that produces nothing."""

    def produce(self, type):
        return Nothing()

class Nothing:
    """It really is nothing."""

    def __init__(self):
        """Nope. Nothing here."""
        pass

    def load(self, blah):
        """Sitting here doing nothing."""
        pass

    def update(self, blah):
        """Even more of nothing."""
        pass