from gi.repository import Gtk


class GameDetailsView(Gtk.Box):
    def __init__(self, store, game_actions):
        self.__init__()
        self.game_store = store
        self.game_actions = game_actions
        self.game = game_actions.game

        self.get_style_context().add_class("game-details")

        self.place_content()

        self.connect_signals()

    def place_content(self):
        vbox_header = Gtk.VBox(spacing=6, visible=True)

        label_game_title = Gtk.Label()

        vbox_header.pack_start(label_game_title, False, False, 12)

        self.set_label_game_title_styles(label_game_title)

        self.pack_start(vbox_header, True, True, 6)

    def connect_signals(self):
        return

    def set_label_game_title_styles(self, game_title_label):
        game_title_label.set_markup(
            "<span font-desc='22'>%s</span>" %
            self.game.name
        )
