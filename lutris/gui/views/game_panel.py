"""Game panel"""
from datetime import datetime
from gi.repository import Gtk, GObject
from lutris import runners
from lutris.gui.widgets.utils import get_link_button
from lutris.util.strings import gtk_safe
from lutris.gui.views.generic_panel import GenericPanel
from lutris.gui.views.game_panel_boxes.title_block import GamePanelTitleBlock


class GamePanel(GenericPanel):
    """Panel allowing users to interact with a game"""

    __gsignals__ = {
        "panel-closed": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self, game_actions):
        self.game_actions = game_actions
        self.game = game_actions.game
        super().__init__()
        self.set_margin_left(10)
        self.set_margin_right(10)
        self.game.connect("game-start", self.on_game_start)
        self.game.connect("game-started", self.on_game_started)
        self.game.connect("game-stopped", self.on_game_stop)

    def place_content(self):
        vbox = Gtk.VBox(spacing=0, visible=True)

        game_panel_title_block = GamePanelTitleBlock(spacing=6, visible=True, game=self.game, parent_widget=self)
        vbox.pack_start(game_panel_title_block, False, False, 12)

        """Game labels block"""
        vbox_game_labels = Gtk.VBox(spacing=0, visible=True)

        if self.game.is_installed:
            vbox_game_labels.pack_start(self.get_runner_label(), False, False, 2)
        if self.game.playtime:
            vbox_game_labels.pack_start(self.get_playtime_label(), False, False, 2)
        if self.game.lastplayed:
            vbox_game_labels.pack_start(self.get_last_played_label(), False, False, 2)

        vbox.pack_start(vbox_game_labels, False, False, 12)

        """Play controls"""
        vbox_play_control_buttons = Gtk.VBox(spacing=0, visible=True)

        self.play_control_buttons = self.get_buttons_play_control_actions()

        for action_id, button in self.play_control_buttons.items():
            button.set_size_request(-1, 20)
            vbox_play_control_buttons.pack_start(button, False, False, 6)

        vbox.pack_start(vbox_play_control_buttons, False, False, 12)

        """Runners"""
        hbbox_runners = Gtk.HButtonBox(visible=True)

        hbbox_runners.set_layout(Gtk.ButtonBoxStyle.EDGE)
        hbbox_runners.set_spacing(4)

        self.buttons_for_runner = self.get_buttons_for_runner_actions()

        for action_id, button in self.buttons_for_runner.items():
            hbbox_runners.add(button)

        vbox.pack_start(hbbox_runners, False, False, 12)

        """Game options"""
        vbox_game_options = Gtk.VBox(spacing=4, visible=True)

        label_game = Gtk.Label(visible=True)
        label_game.set_markup("<b>{}</b>".format("Game options"))
        label_game.set_size_request(-1, 25)

        vbox_game_options.pack_start(label_game, False, False, 6)

        self.buttons_game_actions = self.get_buttons_game_actions()

        for action_id, button in self.buttons_game_actions.items():
            vbox_game_options.pack_start(button, False, False, 6)

        vbox.pack_start(vbox_game_options, False, False, 12)

        vbox.set_center_widget(vbox_game_options)

        """WINE actions"""
        self.buttons_wine_actions = self.get_buttons_for_wine_actions()

        if self.buttons_wine_actions.items():
            vbox_wine = Gtk.VBox(spacing=0, visible=True)

            label_wine = Gtk.Label(visible=True)
            label_wine.set_markup("<b>{}</b>".format("Wine options"))
            label_wine.set_size_request(-1, 25)

            vbox_wine.pack_start(label_wine, True, True, 6)

            for action_id, button in self.buttons_wine_actions.items():
                vbox_wine.pack_start(button, False, False, 0)

            vbox.pack_start(vbox_wine, False, False, 12)

        """Other actions"""
        vbox_other = Gtk.VBox(spacing=0, visible=True)

        label_other = Gtk.Label(visible=True)
        label_other.set_markup("<b>{}</b>".format("Other options"))
        label_other.set_size_request(-1, 25)

        vbox_other.pack_start(label_other, False, False, 12)

        self.buttons_other = self.get_buttons_other_actions()

        for action_id, button in self.buttons_other.items():
            vbox_other.pack_end(button, False, False, 6)

        vbox.pack_start(vbox_other, True, True, 12)

        self.pack_start(vbox, True, True, 0)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    @property
    def background_id(self):
        return self.game.slug

    def get_runner_label(self):
        """Return the label containing the runner info"""
        runner_icon = Gtk.Image.new_from_icon_name(
            self.game.runner.name.lower().replace(" ", "") + "-symbolic",
            Gtk.IconSize.MENU,
        )
        runner_icon.show()
        runner_icon.set_size_request(-1, 25)

        runner_label = Gtk.Label()
        runner_label.show()
        runner_label.set_markup("<b>%s</b>" % gtk_safe(self.game.platform))
        runner_label.set_size_request(-1, 25)

        runner_box = Gtk.Box(spacing=6)
        runner_box.pack_start(runner_icon, False, False, 0)
        runner_box.pack_start(runner_label, False, False, 0)
        runner_box.set_size_request(-1, 25)
        runner_box.show()

        return runner_box

    def get_playtime_label(self):
        """Return the label containing the playtime info"""
        playtime_label = Gtk.Label()
        playtime_label.show()
        playtime_label.set_markup(
            "Time played: <b>%s</b>" % self.game.formatted_playtime
        )
        playtime_label.set_size_request(-1, 25)
        return playtime_label

    def get_last_played_label(self):
        """Return the label containing the last played info"""
        last_played_label = Gtk.Label()
        last_played_label.set_size_request(-1, 25)
        last_played_label.show()
        lastplayed = datetime.fromtimestamp(self.game.lastplayed)
        last_played_label.set_markup(
            "Last played: <b>%s</b>" % lastplayed.strftime("%x")
        )
        return last_played_label

    @staticmethod
    def get_runner_entries(game):
        """Return runner specific contextual actions"""
        try:
            runner = runners.import_runner(game.runner_name)(game.config)
        except runners.InvalidRunner:
            return None
        return runner.context_menu_entries

    def get_buttons_play_control_actions(self):
        displayed = self.game_actions.get_displayed_entries_play_controls()
        buttons = {}
        for action in self.game_actions.get_play_control_actions():
            action_id, label, callback = action
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
                button.connect("clicked", self.on_shortcut_edited, action_id)

            button.connect("clicked", callback)
            buttons[action_id] = button

        return buttons

    def get_buttons_for_wine_actions(self):
        buttons = {}
        if self.game.runner_name and self.game.is_installed:
            for entry in self.get_runner_entries(self.game):
                name, label, callback = entry
                button = get_link_button(label)
                button.show()
                button.connect("clicked", callback)
                buttons[name] = button
        return buttons

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

    def on_shortcut_edited(self, _widget, action_id):
        """Callback for shortcut buttons"""
        self.buttons[action_id].hide()
        if action_id[0:2] == "rm":
            self.buttons[action_id[3:]].show()
        else:
            self.buttons["rm-" + action_id].show()

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

    def on_game_stop(self, _widget, _game_id=None):
        """Called when a game is stopped (`game-stopped` signal)"""
        self.refresh()

    def on_close(self, _widget):
        """Callback for the clone panel button"""
        self.emit("panel-closed")
