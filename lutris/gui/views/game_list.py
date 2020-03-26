# pylint: disable=no-member
from gi.repository import Gtk
from lutris.gui.views.base import GameView


class GameList(Gtk.Box, GameView):

    _gsignals__ = GameView.__gsignals__

    def __init__(self, store):
        self.game_store = store
        self.model = self.game_store.modelsort
        super().__init__(self.model)
        self.set_rules_hint(True)

        """
        Build the widget
        Resizable panes
          Narrow panel at the right containing the (filtered) list of games Gtk.ListBox
          Panel on the right containing the game details.
        """
        vp = Gtk.HPaned()

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)

        self.game_list = Gtk.ListView

        vp.add1(self.game_list)

        vp.add2(sw)

        vp.set_position(100)

        self.add(vp)

        self.show_all()
