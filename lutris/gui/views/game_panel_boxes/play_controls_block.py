from gi.repository import Gtk


class PlayControlsBlock(Gtk.Box):
    """Panel containing the play controls for the game panel"""

    def __init__(self, spacing, visible, game, game_actions):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game = game
        self.game_actions = game_actions
        self.game.connect("game-start", self.on_game_start)
        self.game.connect("game-started", self.on_game_started)
        self.game.connect("game-stopped", self.on_game_state_changed)

        self.place_content()

    def place_content(self):
        self.buttons = self.get_buttons_play_control_actions()

        for action_id, button in self.buttons.items():
            if action_id == "show_game_details" or action_id == "hide_game_details":
                button.set_size_request(32, 32)
                self.pack_start(button, False, False, 2)
            else:
                button.set_size_request(-1, 20)
                self.pack_start(button, True, True, 0)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_buttons_play_control_actions(self):
        displayed = self.game_actions.get_displayed_entries_play_controls()
        icon_map = {
            "show_game_details": "view-list-details",
            "hide_game_details": "arrow-right",
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

    def on_game_start(self, _widget):
        """Callback for the `game-start` signal"""
        self.buttons["play"].set_label("Launching...")
        self.buttons["play"].set_sensitive(False)

    def on_game_started(self, _widget):
        """Callback for the `game-started` signal"""
        self.buttons["stop"].show()
        self.buttons["play"].hide()
        self.buttons["play"].set_label("Play")
        self.buttons["play"].set_sensitive(True)

    def on_game_state_changed(self, _widget, _game_id=None):
        """Generic callback to trigger a refresh"""
        self.refresh()
