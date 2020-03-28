from gi.repository import Gtk
from lutris.gui.widgets.utils import get_link_button


class GameOptionsBlock(Gtk.VBox):
    """Panel containing the game option buttons for the game panel"""

    def __init__(self, spacing, visible, game_actions, title, parent_widget):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_actions = game_actions
        self.title = title
        self.parent_widget = parent_widget
        self.place_content()

    def place_content(self):
        label_game = Gtk.Label(visible=True)
        label_game.set_markup("<b>{}</b>".format(self.title))
        label_game.set_size_request(-1, 25)

        self.pack_start(label_game, False, False, 6)

        self.buttons_game_actions = self.get_buttons_game_actions()

        for action_id, button in self.buttons_game_actions.items():
            self.pack_start(button, False, False, 6)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_buttons_game_actions(self):
        """Return a dictionary of buttons to use in the panel"""
        displayed = self.game_actions.get_displayed_entries_game()
        buttons = {}
        for action in self.game_actions.get_game_actions():
            action_id, label, callback = action
            button = get_link_button(label)

            if displayed.get(action_id):
                button.show()
            else:
                button.hide()

            if action_id in (
                    "desktop-shortcut",
                    "rm-desktop-shortcut",
                    "menu-shortcut",
                    "rm-menu-shortcut"
            ):
                button.connect("clicked", self.parent_widget.on_shortcut_edited, action_id)

            button.connect("clicked", callback)
            buttons[action_id] = button

        return buttons
