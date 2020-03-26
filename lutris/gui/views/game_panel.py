"""Game panel"""
from datetime import datetime
from gi.repository import Gtk, Pango, GObject
from lutris import runners
from lutris.gui.widgets.utils import get_pixbuf_for_game, get_link_button
from lutris.util.strings import gtk_safe
from lutris.gui.views.generic_panel import GenericPanel


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

        """Add all controls to a vertical box"""
        hbox_top_buttons = Gtk.Box(spacing=6, visible=True)

        title_label = Gtk.Label()

        self.set_title_label_styles(title_label)

        hbox_top_buttons.pack_start(self.get_icon(), False, False, 6)
        hbox_top_buttons.pack_start(title_label, True, True, 0)
        hbox_top_buttons.pack_start(self.get_close_button(), False, False, 6)

        hbox_top_buttons.set_center_widget(title_label)

        vbox.pack_start(hbox_top_buttons, False, False, 6)

        if self.game.is_installed:
            vbox.pack_start(self.get_runner_label(), False, False, 2)
        if self.game.playtime:
            vbox.pack_start(self.get_playtime_label(), False, False, 2)
        if self.game.lastplayed:
            vbox.pack_start(self.get_last_played_label(), False, False, 2)

        self.play_control_buttons = self.get_buttons_play_control()

        for action_id, button in self.play_control_buttons.items():
            vbox.pack_start(button, False, False, 6)

        hbox_runners = Gtk.Box(spacing=0, visible=True)
        hbox_runners.set_size_request(-1, 25)

        self.buttons_for_runner = self.get_buttons_for_runner()

        for action_id, button in self.buttons_for_runner.items():
            hbox_runners.pack_start(button, True, True, 4)

        vbox.pack_start(hbox_runners, False, True, 0)

        label_game = Gtk.Label(visible=True)
        label_game.set_markup("<b>{}</b>".format("Game options"))
        label_game.set_size_request(-1, 25)

        vbox.pack_start(label_game, True, True, 6)

        self.buttons_game_actions = self.get_buttons_game()

        for action_id, button in self.buttons_game_actions.items():
            vbox.pack_start(button, False, False, 6)

        label_other = Gtk.Label(visible=True)
        label_other.set_markup("<b>{}</b>".format("Other options"))
        label_other.set_size_request(-1, 25)

        vbox.pack_start(label_other, True, True, 6)

        self.buttons_other = self.get_buttons_other_actions()

        for action_id, button in self.buttons_other.items():
            vbox.pack_start(button, False, False, 6)

        self.pack_start(vbox, True, True, 0)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    @property
    def background_id(self):
        return self.game.slug

    def get_close_button(self):
        """Return the close button"""
        button = Gtk.Button.new_from_icon_name(
            "window-close-symbolic", Gtk.IconSize.MENU
        )
        button.set_tooltip_text("Close")
        button.set_size_request(32, 32)
        button.connect("clicked", self.on_close)
        button.show()
        return button

    def get_icon(self):
        """Return the game icon"""
        icon = Gtk.Image.new_from_pixbuf(get_pixbuf_for_game(self.game.slug, "icon"))
        icon.show()
        return icon

    def set_title_label_styles(self, title_label):
        """Style the label with the game's title"""
        title_label.set_markup(
            "<span font_desc='16'>%s</span>" % gtk_safe(self.game.name)
        )
        title_label.set_ellipsize(Pango.EllipsizeMode.END)
        #title_label.set_alignment(0, 0.5)
        title_label.set_justify(Gtk.Justification.CENTER)
        title_label.show()
        return title_label

    def get_runner_label(self):
        """Return the label containing the runner info"""
        runner_icon = Gtk.Image.new_from_icon_name(
            self.game.runner.name.lower().replace(" ", "") + "-symbolic",
            Gtk.IconSize.MENU,
        )
        runner_icon.show()
        runner_icon.set_size_request(-1, 25);

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

    def get_buttons_play_control(self):
        displayed = self.game_actions.get_displayed_entries_play_controls()
        buttons = {}
        for action in self.game_actions.get_play_control_actions():
            action_id, label, callback = action
            button = Gtk.Button(label)
            button.set_size_request(100, 42)
            if displayed.get(action_id):
                button.show()
            else:
                button.hide()
            buttons[action_id] = button
        return buttons

    def get_buttons_for_runner(self):
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
            buttons[action_id] = button
        return buttons

    #def get_buttons_main(self):
    #    displayed = self.game_actions.get_displayed_entries_game()
    #    buttons = {}
    #    if self.game.runner_name and self.game.is_installed:
    #        for entry in self.get_displayed_entries_game(self.game):
    #            name, label, callback = entry
    #            button = get_link_button(label)
    #            button.show()
    #            button.connect("clicked", callback)
    #            buttons[name] = button
    #    return buttons

    def get_buttons_game(self):
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
                    "rm-menu-shortcut",
            ):
                button.connect("clicked", self.on_shortcut_edited, action_id)

            button.connect("clicked", callback)
            buttons[action_id] = button

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
            buttons[action_id] = button
        return buttons

    """Obsolete"""
    def place_buttons(self, base_height):
        """Places all appropriate buttons in the panel"""
        play_x_offset = 87
        icon_offset = 6
        icon_width = 32
        icon_start = 84
        icons_y_offset = 60
        buttons_x_offset = 28
        extra_button_start = 540  # Y position for runner actions
        extra_button_index = 0
        for action_id, button in self.buttons.items():
            position = None
            if action_id in ("play", "stop", "install"):
                position = (play_x_offset, base_height)
            if action_id == "configure":
                position = (icon_start, base_height + icons_y_offset)
            if action_id == "browse":
                position = (
                    icon_start + icon_offset + icon_width,
                    base_height + icons_y_offset,
                )
            if action_id == "show_logs":
                position = (
                    icon_start + icon_offset * 2 + icon_width * 2,
                    base_height + icons_y_offset,
                )
            if action_id == "remove":
                position = (
                    icon_start + icon_offset * 3 + icon_width * 3,
                    base_height + icons_y_offset,
                )

            current_y = base_height + 150
            if action_id == "execute-script":
                position = (buttons_x_offset, current_y)
            if action_id in ("add", "install_more"):
                position = (buttons_x_offset, current_y + 40)
            if action_id == "view":
                position = (buttons_x_offset, current_y + 80)
            if action_id in ("desktop-shortcut", "rm-desktop-shortcut"):
                position = (buttons_x_offset, current_y + 120)
            if action_id in ("menu-shortcut", "rm-menu-shortcut"):
                position = (buttons_x_offset, current_y + 160)
            if action_id in ("hide", "unhide"):
                position = (buttons_x_offset, current_y + 200)

            if not position:
                position = (
                    buttons_x_offset,
                    extra_button_start + extra_button_index * 40,
                )
                extra_button_index += 1

            self.put(button, position[0], position[1])

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
