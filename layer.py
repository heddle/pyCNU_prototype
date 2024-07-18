from items.item import Item

class Layer:
    def __init__(self, view, name):
        self.view = view
        self.name = name
        self.items = []

    def add_item(self, attributes):
        item = Item(attributes=attributes)
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)
