from gi.repository import Gtk


class WineActionsBlock(Gtk.VBox):
    """Panel containing the WINE options for the game panel"""

    def __init__(self, spacing, visible, buttons, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.buttons = buttons
        self.title = title
        self.place_content()

    def place_content(self):
        label_wine = Gtk.Label(visible=True)
        label_wine.set_markup("<b>{}</b>".format("Wine options"))
        label_wine.set_size_request(-1, 25)

        self.pack_start(label_wine, True, True, 6)

        for action_id, button in self.buttons.items():
            self.pack_start(button, False, False, 0)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()
