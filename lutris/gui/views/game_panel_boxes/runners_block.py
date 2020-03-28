from gi.repository import Gtk
from lutris.gui.widgets.utils import get_link_button


class RunnersBlock(Gtk.HButtonBox):
    """Panel containing the runner buttons for the game panel"""

    def __init__(self, visible, layout, spacing, game_actions):
        super().__init__()
        self.set_visible(visible)
        self.set_layout(layout)
        self.set_spacing(spacing)
        self.game_actions = game_actions
        self.place_content()

    def place_content(self):
        self.set_layout(Gtk.ButtonBoxStyle.EDGE)
        self.set_spacing(4)

        self.buttons_for_runner = self.get_buttons_for_runner_actions()

        for action_id, button in self.buttons_for_runner.items():
            self.add(button)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_buttons_for_runner_actions(self):
        displayed = self.game_actions.get_displayed_entries_runner_actions()
        icon_map = {
            "configure": "preferences-system-symbolic",
            "browse": "system-file-manager-symbolic",
            "show_logs": "utilities-terminal-symbolic"
        }
        buttons = {}
        for action in self.game_actions.get_runner_actions():
            action_id, label, callback = action
            if action_id in icon_map:
                button = Gtk.Button.new_from_icon_name(
                    icon_map[action_id], Gtk.IconSize.MENU
                )
                button.set_tooltip_text(label)
                button.set_size_request(-1, 32)
            else:
                button = get_link_button(label)

            if displayed.get(action_id):
                button.show()
            else:
                button.hide()
            button.connect("clicked", callback)
            buttons[action_id] = button
        return buttons
