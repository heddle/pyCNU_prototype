from items.item import Item


class Layer:
    def __init__(self, view, name):
        """
        Initialize the layer.
        :param view: The view the layer belongs to.
        :param name: The name of the layer.
        """
        self.view = view
        self.name = name
        self.items = []
        self._visible = True

    @property
    def visible(self):
        """Return the visibility of the layer."""
        return self._visible

    @visible.setter
    def visible(self, value):
        """Set the visibility of the layer."""
        self._visible = value
        self.view.update()

    def add_item(self, item, update=True):
        """
        Add an item to the layer.
        :param item: The item to add.
        :param update: If True, update the view after adding the item.
        :return: None
        """
        self.items.append(item)
        if update:
            self.view.update()

    def remove_item(self, item, update=True):
        """ Remove an item from the layer.
        :param item: The item to remove.
        :param update: If True, update the view after removing the item.
        :return: None
        """
        self.items.remove(item)
        if update:
            self.view.update()
