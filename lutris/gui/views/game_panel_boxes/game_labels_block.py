from datetime import datetime
from gi.repository import Gtk
from lutris.util.strings import gtk_safe


class GameLabelsBlock(Gtk.VBox):
    """Panel containing the game labels for the game panel"""

    def __init__(self, spacing, visible, game):
        """Game labels block"""
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game = game
        self.place_content()

    def place_content(self):
        if self.game.is_installed:
            self.pack_start(self.get_runner_label(), False, False, 2)
        if self.game.playtime:
            self.pack_start(self.get_playtime_label(), False, False, 2)
        if self.game.lastplayed:
            self.pack_start(self.get_last_played_label(), False, False, 2)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

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
