from gi.repository import Gtk


class PlayControlsBlock(Gtk.VBox):
    """Panel containing the play controls for the game panel"""

    def __init__(self, spacing, visible, game_actions):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_actions = game_actions
        self.set_content()

    def set_content(self):
        self.play_control_buttons = self.get_buttons_play_control_actions()

        for action_id, button in self.play_control_buttons.items():
            button.set_size_request(-1, 20)
            self.pack_start(button, False, False, 6)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_buttons_play_control_actions(self):
        displayed = self.game_actions.get_displayed_entries_play_controls()
        icon_map = {
            "play": "media-playback-start",
            "stop": "media-playback-stop"
        }
        buttons = {}
        for action in self.game_actions.get_play_control_actions():
            action_id, label, callback = action
            if action_id in icon_map:
                button = Gtk.Button.new_from_icon_name(
                    icon_map[action_id], Gtk.IconSize.MENU
                )
                button.set_tooltip_text(label)
                button.set_size_request(-1, 32)
            else:
                button = Gtk.Button(label)
                button.set_tooltip_text(label)
                button.set_size_request(32, 32)

            if displayed.get(action_id):
                button.show()
            else:
                button.hide()
            button.connect("clicked", callback)
            buttons[action_id] = button
        return buttons
