from gi.repository import Gtk
from lutris.gui.views.store import GameStore


class OtherVersionsStore(GameStore):
    def __init__(
        self,
        games,
        icon_type,
        filter_installed,
        sort_key,
        sort_ascending,
        show_hidden_games,
        show_installed_first=False,
        bg_color_selected=None
    ):
        super(GameStore, self).__init__()
