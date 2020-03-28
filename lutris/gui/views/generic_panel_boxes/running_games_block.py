from gi.repository import Gtk, Pango, Gio
from lutris.util.strings import gtk_safe


class RunningGamesBlock(Gtk.VBox):
    """Panel containing the running games for the generic panel"""

    def __init__(self, spacing, visible, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.place_content()

    def place_content(self):
        running_label = Gtk.Label(visible=True)
        running_label.set_markup("<b>%s</b>" % gtk_safe(self.title))
        running_label.set_justify(Gtk.Justification.CENTER)
        self.pack_start(running_label, False, False, 6)

        application = Gio.Application.get_default()

        if application.running_games.get_n_items():
            listbox = Gtk.ListBox(visible=True)
            listbox.bind_model(self.application.running_games, self.create_list_widget)
            listbox.connect('row-selected', self.on_running_game_select)
            listbox.show()

            self.pack_start(listbox, False, False, 6)
        else:
            label_no_games_running = Gtk.Label(visible=True)
            label_no_games_running.set_markup("<i>No games playing</i>")

            self.pack_start(label_no_games_running, False, False, 6)

    def create_list_widget(self, game):
        box = Gtk.Box(
            spacing=6, margin_top=6, margin_bottom=6, margin_right=6, margin_left=6
        )
        box.set_size_request(100, 32)

        icon = Gtk.Image.new_from_pixbuf(get_pixbuf_for_game(game.slug, "icon"))
        icon.show()
        box.pack_start(icon, False, False, 2)

        game_label = Gtk.Label(game.name, visible=True)
        game_label.set_ellipsize(Pango.EllipsizeMode.END)
        box.pack_start(game_label, False, False, 2)
        box.game = game

        return box

    def on_running_game_select(self, widget, row):
        """Handler for hiding and showing the revealers in children"""
        if not row:
            game = None
        else:
            game = row.get_children()[0].game
        self.emit("running-game-selected", game)
