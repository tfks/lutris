"""Side panel when no game is selected"""
from gi.repository import Gtk, Gdk, Gio, Pango, GObject
# Third Party Libraries
from gi.repository import Gdk, Gio, GObject, Gtk, Pango

# Lutris Modules
from lutris.game import Game
from lutris.util import system
from lutris.gui.views.generic_panel_boxes.header_block import HeaderBlock
from lutris.gui.views.generic_panel_boxes.links_block import LinksBlock
from lutris.gui.views.generic_panel_boxes.running_games_block import RunningGamesBlock
from lutris.gui.views.generic_panel_boxes.lutris_specific_action_block import LutrisSpecificBlock
from lutris.util.log import logger
from lutris.gui.config.system import SystemConfigDialog

LINKS = {
    "floss":
    "https://lutris.net/games/?q=&fully-libre-filter=on&sort-by-popularity=on",
    "f2p": (
        "https://lutris.net/games/?q=&all-free=on&free-filter=on&freetoplay-filter=on"
        "&pwyw-filter=on&sort-by-popularity=on"
    )
    "donate":
    "https://lutris.net/donate",
    "forums":
    "https://forums.lutris.net/",
    "discord":
    "https://discord.gg/Pnt5CuY",
    "irc":
    "irc://irc.freenode.org:6667/lutris",
}


class GenericPanel(Gtk.Box):

    """Side panel displayed when no game is selected"""

    __gtype_name__ = "LutrisPanel"
    __gsignals__ = {"running-game-selected": (GObject.SIGNAL_RUN_FIRST, None, (Game, ))}
        "running-game-selected-from-generic-panel": (GObject.SIGNAL_RUN_FIRST, None, (Game, )),
        "show-installed-only-changed-from-generic-panel": (GObject.SIGNAL_RUN_FIRST, None, (bool, )),
        "show-hidden-games-changed-from-generic-panel": (GObject.SIGNAL_RUN_FIRST, None, (bool, ))

    def __init__(self, game_store, actions, application=None):
        super().__init__(visible=True)
        self.game_store = game_store
        self.actions = actions
        self.application = application

        self.lutris_specific_action_block = None

        self.get_style_context().add_class("game-panel")
        self.set_background()
        self.place_content()
        self.timer_id = None

    @property
    def background_id(self):
        return None

    def set_background(self):
        """Return the background image for the panel"""
        bg_path = get_pixbuf_for_panel(self.background_id)
        if not bg_path:
            return

        style = Gtk.StyleContext()
        style.add_class(Gtk.STYLE_CLASS_VIEW)
        bg_provider = Gtk.CssProvider()
        bg_provider.load_from_data(
            ('.game-scrolled { background-image: url("%s"); '
             "background-repeat: no-repeat; }" % bg_path).encode("utf-8")
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            bg_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def place_content(self):
        """Places widgets in the side panel"""
        vbox = Gtk.VBox(spacing=0, visible=True)

        """Header"""
        header_block = HeaderBlock(spacing=0, visible=True, title="Lutris")

        vbox.pack_start(header_block, False, False, 6)

        """Links"""
        links_block = LinksBlock(spacing=6, visible=True, title="Help")
        vbox.pack_start(links_block, False, False, 6)

        """Running games"""
        running_games_block = RunningGamesBlock(
            spacing=0,
            visible=True,
            title="Playing",
            parent_widget=self

        vbox.pack_start(running_games_block, True, True, 6)

        """Lutris specific actions"""
        self.lutris_specific_action_block = LutrisSpecificBlock(
            spacing=6,
            visible=True,
            title="Lutris",
            game_store=self.game_store,
            actions=self.actions,
            parent_widget=self
        vbox.pack_end(self.lutris_specific_action_block, False, False, 6)

        self.pack_start(vbox, True, True, 6)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def running_game_selected(self, widget, game):
        """Handler for hiding and showing the revealers in children"""
        self.emit("running-game-selected-from-generic-panel", game)

    def set_show_installed_games_only_controls_active(self, value):
        self.lutris_specific_action_block.set_show_installed_games_only_controls_active(value)

    def do_show_installed_games_only_change(self, value):
        self.emit("show-installed-only-changed-from-generic-panel", GLib.Variant.new_boolean(value))

    def set_show_hidden_games_controls_active(self, value):
        self.lutris_specific_action_block.set_show_hidden_games_controls_active(value)

    def do_show_hidden_games_change(self, value):
        self.emit("show-hidden-games-changed-from-generic-panel", GLib.Variant.new_boolean(value))

