class Item:
    def __init__(self, attributes):
        self._attributes = attributes

    @property
    def attributes(self):
        return self._attributes

    def draw(self, canvas):
        # Drawing logic goes here
        pass
