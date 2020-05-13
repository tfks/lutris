from gi.repository import Gtk, Gdk
from lutris import settings
from lutris.gui.widgets.utils import get_pixbuf_for_game
from lutris.gui.widgets.utils import convert_to_background_generic
from lutris.gui.views.game_detail_controls.other_versions import OtherVersions
from lutris.gui.views.game_detail_controls.other_versions_controls import (
    other_versions_pga
)
from lutris.gui.views.game_detail_controls.other_versions_controls.other_versions_store import (
    OtherVersionsStore
)
from lutris.util.log import logger
from lutris.services.steam import SteamGame
from lutris.services.gog import GOGGame
from lutris.util.gtkutils import get_treeview_bg_color

from . import (
    COL_ICON,
    COL_ID,
    COL_INSTALLED,
    COL_INSTALLED_AT,
    COL_INSTALLED_AT_TEXT,
    COL_LASTPLAYED,
    COL_LASTPLAYED_TEXT,
    COL_NAME,
    COL_PLATFORM,
    COL_PLAYTIME,
    COL_PLAYTIME_TEXT,
    COL_RUNNER,
    COL_RUNNER_HUMAN_NAME,
    COL_SLUG, COL_YEAR
)


class GameDetailsView(Gtk.VBox):
    def __init__(self, spacing, visible, store, game_actions, main_window):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_store = store
        self.game_actions = game_actions
        self.game = game_actions.game
        self.main_window = main_window

        self.allocation_values = None

        self.window_size = (0, 0)

        self.bg_info = None

        self.icon_type = None

        self.bg_color_selected = get_treeview_bg_color(Gtk.StateFlags.SELECTED)

        self.other_versions_store = self.get_other_versions_store()

        self.get_style_context().add_class("game-details")

        self.place_content()

        bg_is_set = self.set_background()

        if not bg_is_set:
            self.vbox_header.set_visible(False)

    def set_background(self):
        bg_width = self.main_window.current_window_size[0]
        bg_height = self.main_window.current_window_size[1]

        background_url = self.get_background_url()

        if background_url == "":
            return False

        self.bg_info = convert_to_background_generic(
            background_url,
            (bg_width, bg_height),
            True,
            False
        )

        if self.bg_info is None:
            logger.debug("GameDetails: No image")
            return False

        bg_image = self.bg_info[0]
        bg_path = self.bg_info[1]

        stylesheet = (
            ".game-details {{ background-color: rgba(0, 0, 0, 0.6) }}"
            '.game-details-header {{ background-image: url("{0}"); '
            "background-repeat: no-repeat; "
            "background-position: 0 0; "
            "background-size: 100% 100%;"
            "background-color: rgba(0, 0, 0, 1); }}").format(bg_path,
                                                             bg_image.height)

        logger.debug(stylesheet)

        style = Gtk.StyleContext()
        style.add_class(Gtk.STYLE_CLASS_VIEW)
        bg_provider = Gtk.CssProvider()
        bg_provider.load_from_data(
            (stylesheet).encode("utf-8")
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            bg_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.vbox_header.set_size_request(-1, 400)

        return True

    def get_background_url(self):
        if self.game.steamid != "":
            logger.debug("steamid=%s" % self.game.steamid)
            return SteamGame.get_game_header_image(self.game)
        elif self.game.gogid != "":
            logger.debug("gogid=%s" % self.game.gogid)
            return GOGGame.get_banner_large(self.game)
        else:
            return ""

    def place_content(self):
        self.add_header_image()

        box_header = Gtk.Box(spacing=6, visible=True)
        box_header.set_size_request(-1, 32)

        box_header.pack_start(self.get_icon(), False, False, 6)

        label_game_title = Gtk.Label()

        self.set_label_game_title_styles(label_game_title)

        box_header.pack_start(label_game_title, True, True, 6)

        self.pack_start(box_header, False, False, 6)

        other_versions = OtherVersions(
            spacing=6,
            visible=True,
            store=self.game_store,
            title="Other versions",
            info_text="Use this section to install different version of the same game. This can come in handy when trying out different settings but without having to uninstall the original version. In case the application needs Wine to run: The wizard will ask for the location where the new Wine-prefix is to be created.",
            add_click_callback=self.on_add_other_version_clicked,
            del_click_callback=self.on_del_other_version_clicked,
            play_click_callback=self.on_play_other_version_clicked,
            stop_click_callback=self.on_stop_other_version_clicked,
            configure_click_callback=self.on_configure_other_version_clicked
        )

        self.pack_start(other_versions, False, False, 6)

        related_apps = OtherVersions(
            spacing=6,
            visible=True,
            store=self.game_store,
            title="Related applications",
            info_text="Use this section to install extra applications which are specific to the main application. Examples are applications used for modding a game. In case the application needs Wine to run: if an application needs a specific Wine-prefix to run correctly, the Wizard has the option to create one.",
            add_click_callback=self.on_add_related_app_clicked,
            del_click_callback=self.on_del_related_app_clicked,
            play_click_callback=self.on_play_related_app_clicked,
            stop_click_callback=self.on_stop_related_app_clicked,
            configure_click_callback=self.on_configure_related_app_clicked
        )

        self.pack_start(related_apps, False, False, 6)

        box_content_dummy = Gtk.Box(spacing=6, visible=True)

        self.pack_end(box_content_dummy, True, True, 6)

    def add_header_image(self):
        self.vbox_header = Gtk.VBox(spacing=0, visible=True)
        self.vbox_header.get_style_context().add_class("game-details-header")
        self.pack_start(self.vbox_header, True, True, 0)

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

    def get_other_versions_store(self, other_versions=None):
        other_versions = other_versions or other_versions_pga.get_other_versions(self.game)

        game_store = OtherVersionsStore(
            other_versions,
            self.icon_type,
            False,
            self.view_sorting,
            self.view_sorting_ascending,
            True,
            False,
            self.bg_color_selected
        )
        game_store.connect("sorting-changed", self.on_other_versions_sorting_changed)

        return game_store

    def on_add_other_version_clicked(self, button):
        return

    def on_del_other_version_clicked(self, button):
        return

    def on_play_other_version_clicked(self, button):
        return

    def on_stop_other_version_clicked(self, button):
        return

    def on_configure_other_version_clicked(self, button):
        return

    def on_add_related_app_clicked(self, button):
        return

    def on_del_related_app_clicked(self, button):
        return

    def on_play_related_app_clicked(self, button):
        return

    def on_stop_related_app_clicked(self, button):
        return

    def on_configure_related_app_clicked(self, button):
        return

    def on_other_versions_sorting_changed(self, _game_store, key, ascending):
        self.actions["view-sorting-other-versions"].set_state(GLib.Variant.new_string(key))
        settings.write_setting("view_sorting_other_versions", key)

        self.actions["view-sorting-other-versions-ascending"].set_state(GLib.Variant.new_boolean(ascending))
        settings.write_setting("view_sorting_other_versions_ascending", bool(ascending))

    @property
    def view_sorting(self):
        return settings.read_setting("view_sorting_other_versions") or "name"

    @property
    def view_sorting_ascending(self):
        return settings.read_setting("view_sorting_other_versions_ascending").lower() != "false"
