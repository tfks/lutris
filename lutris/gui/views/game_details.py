from gi.repository import Gtk, Gdk
from lutris.gui.widgets.utils import get_pixbuf_for_game
from lutris.gui.widgets.utils import convert_to_background_generic
from lutris.gui.views.game_detail_controls.related_apps import RelatedApplications
from lutris.gui.views.game_detail_controls.other_versions import OtherVersions


class GameDetailsView(Gtk.VBox):
    def __init__(self, spacing, visible, store, game_actions):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_store = store
        self.game_actions = game_actions
        self.game = game_actions.game

        self.allocation_values = None

        self.get_style_context().add_class("game-details")

        self.connect_signals()

        self.set_background()

        self.place_content()

    def set_background(self):
        bg_width = 1920
        bg_height = 1080

        bg_path = convert_to_background_generic(
            "/home/tfk/.local/share/lutris/covers/star-trek-starfleet-command-iii.jpg", (bg_width, bg_height),
            True
        )

        if not bg_path:
            return

        style = Gtk.StyleContext()
        style.add_class(Gtk.STYLE_CLASS_VIEW)
        bg_provider = Gtk.CssProvider()
        bg_provider.load_from_data(
            ('.game-details { background-image: url("%s"); '
             "background-repeat: no-repeat; "
             "background-position: center center; "
             "background-size: cover; "
             "background-color: rgba(0, 0, 0, 0.5)}" % bg_path).encode("utf-8")
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            bg_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def place_content(self):
        box_header = Gtk.Box(spacing=6, visible=True)
        box_header.set_size_request(-1, 32)

        box_header.pack_start(self.get_icon(), False, False, 6)

        label_game_title = Gtk.Label()

        self.set_label_game_title_styles(label_game_title)

        box_header.pack_start(label_game_title, True, True, 6)

        self.pack_start(box_header, False, False, 6)

        other_versions = OtherVersions(6, True, self.game_store)

        self.pack_start(other_versions, False, False, 6)

        related_apps = RelatedApplications(6, True, self.game_store)

        self.pack_start(related_apps, False, False, 6)

        box_content_dummy = Gtk.Box(spacing=6, visible=True)

        self.pack_end(box_content_dummy, True, True, 6)

        # self.set_center_widget(box_content_dummy)

    def connect_signals(self):
        return

    def get_icon(self):
        """Return the game icon"""
        icon = Gtk.Image.new_from_pixbuf(get_pixbuf_for_game(self.game.slug, "icon"))
        icon.show()
        icon.set_size_request(32, 32)
        return icon

    def set_label_game_title_styles(self, game_title_label):
        game_title_label.set_visible(True)
        game_title_label.set_markup(
            "<span font-desc='22'>%s</span>" %
            self.game.name
        )
        game_title_label.set_alignment(0.0, -1)

