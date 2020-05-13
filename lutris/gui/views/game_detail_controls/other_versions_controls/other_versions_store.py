from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf

from lutris.gui.views.store import GameStore
from lutris.gui.views.game_detail_controls.other_versions_controls import other_versions_pga

from lutris.gui.views import (
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


class OtherVersionsStore(GObject.Object):
    __gsignals__ = {
        "media-loaded": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "icon-loaded": (GObject.SIGNAL_RUN_FIRST, None, (str, str)),
        "icons-changed": (GObject.SIGNAL_RUN_FIRST, None, (str, )),
        "sorting-changed": (GObject.SIGNAL_RUN_FIRST, None, (str, bool)),
    }

    def __init__(
        self,
        games,
        game,
        icon_type,
        filter_installed,
        sort_key,
        sort_ascending,
        show_hidden_games,
        show_installed_first=False,
        bg_color_selected=None
    ):
        super(OtherVersionsStore, self).__init__()
        self.games = games or other_versions_pga.get_other_versions(game)

        self.game = game

        self.store = Gtk.ListStore(
            int,
            str,
            str,
            Pixbuf,
            str,
            str,
            str,
            str,
            int,
            str,
            bool,
            int,
            str,
            float,
            str
        )

        sort_col = COL_NAME

        self.modelfilter = self.store.filter_new()

        try:
            self.modelsort = Gtk.TreeModelSort.new_with_model(self.modelfilter)
        except AttributeError:
            self.modelsort = Gtk.TreeModelSort.sort_new_with_model(self.modelfilter)


