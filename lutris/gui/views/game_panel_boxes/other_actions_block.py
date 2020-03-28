from gi.repository import Gtk
from lutris.gui.widgets.utils import get_link_button


class OtherActionsBlock(Gtk.VBox):
    """Panel containing the other options for the game panel"""

    def __init__(self, spacing, visible, game_actions, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_actions = game_actions
        self.title = title
        self.place_content()

    def place_content(self):
        label_other = Gtk.Label(visible=True)
        label_other.set_markup("<b>{}</b>".format(self.title))
        label_other.set_size_request(-1, 25)

        self.pack_start(label_other, False, False, 12)

        self.buttons_other = self.get_buttons_other_actions()

        for action_id, button in self.buttons_other.items():
            self.pack_end(button, False, False, 6)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_buttons_other_actions(self):
        displayed = self.game_actions.get_displayed_entries_other_actions()
        icon_map = {
            "remove": "user-trash-symbolic"
        }
        buttons = {}
        for action in self.game_actions.get_other_actions():
            action_id, label, callback = action
            if action_id in icon_map:
                button = Gtk.Button.new_from_icon_name(
                    icon_map[action_id], Gtk.IconSize.MENU
                )
                button.set_tooltip_text(label)
                button.set_size_request(32, 32)
            else:
                button = get_link_button(label)

            if displayed.get(action_id):
                button.show()
            else:
                button.hide()
            button.connect("clicked", callback)
            buttons[action_id] = button
        return buttons

