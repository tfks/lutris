"""Side panel when no game is selected"""
import json
from gi.repository import Gtk, Gdk, Gio, Pango, GObject
from lutris import api
from lutris.game import Game
from lutris.util import system
from lutris.gui.widgets.utils import (
    get_pixbuf_for_panel,
    get_pixbuf_for_game,
    get_pixbuf,
    get_main_window,
    open_uri,
    get_default_button,
    get_default_link_button,
    get_link_button,
)
from lutris.gui.config.system import SystemConfigDialog

LINKS = {
    "floss": "https://lutris.net/games/?q=&fully-libre-filter=on&sort-by-popularity=on",
    "f2p": (
        "https://lutris.net/games/?q=&all-free=on&free-filter=on&freetoplay-filter=on"
        "&pwyw-filter=on&sort-by-popularity=on"
    ),
    "donate": "https://lutris.net/donate",
    "forums": "https://forums.lutris.net/",
    "discord": "https://discord.gg/Pnt5CuY",
    "irc": "irc://irc.freenode.org:6667/lutris",
}


class GenericPanel(Gtk.Box):
    """Side panel displayed when no game is selected"""

    __gtype_name__ = "LutrisPanel"
    __gsignals__ = {
        "running-game-selected": (GObject.SIGNAL_RUN_FIRST, None, (Game, ))
    }

    def __init__(self, application=None):
        super().__init__(visible=True)
        self.application = application
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
        hbox_header = self.get_content_header()

        vbox.pack_start(hbox_header, False, False, 6)

        """Links"""
        vbox.pack_start(self.get_lutris_links(), False, False, 6)

        """Running games"""
        vbox_running_games = Gtk.VBox(spacing=0, visible=True)

        running_label = Gtk.Label(visible=True)
        running_label.set_markup("<b>Playing</b>")
        running_label.set_justify(Gtk.Justification.CENTER)
        vbox_running_games.pack_start(running_label, False, False, 6)

        application = Gio.Application.get_default()

        if application.running_games.get_n_items():
            listbox = Gtk.ListBox(visible=True)
            listbox.bind_model(self.application.running_games, self.create_list_widget)
            listbox.connect('row-selected', self.on_running_game_select)
            listbox.show()

            vbox_running_games.pack_start(listbox, False, False, 6)
        else:
            label_no_games_running = Gtk.Label(visible=True)
            label_no_games_running.set_markup("<i>No games plaging</i>")

            vbox_running_games.pack_start(label_no_games_running, False, False, 6)

        vbox.pack_start(vbox_running_games, True, True, 6)

        """Buttons"""
        vbox.pack_end(self.get_preferences_button(), False, False, 6)

        vbox.set_center_widget(vbox_running_games)

        self.pack_start(vbox, True, True, 6)

    def get_content_header(self):
        """Header"""
        hbox_header = Gtk.Box(spacing=0, visible=True)

        app_title_label = Gtk.Label(visible=True)

        app_title_label.set_markup("<span font_desc='22'>Lutris</span>")
        app_title_label.set_alignment(0, 0.5)

        hbox_header.pack_start(app_title_label, True, True, 6)
        hbox_header.pack_start(self.get_user_info_box(), False, False, 6)

        hbox_header.set_center_widget(app_title_label)

        return hbox_header

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_preferences_button(self):
        preferences_button = get_default_button("", "preferences-system-symbolic")
        #preferences_button = Gtk.Button.new_from_icon_name(
        #    "preferences-system-symbolic", Gtk.IconSize.MENU
        #)
        preferences_button.set_tooltip_text("Preferences")
        #preferences_button.set_size_request(32, 32)
        #preferences_button.props.relief = Gtk.ReliefStyle.NONE
        preferences_button.connect("clicked", self.on_preferences_clicked)
        preferences_button.show()
        return preferences_button

    def on_preferences_clicked(self, button):
        SystemConfigDialog(get_main_window(button))

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

    def get_user_info_box(self):
        user_box = Gtk.Box(spacing=6, visible=True)
        #user_box.set_size_request(254, 64)
        #user_box.set_size_request(-1, 64)
        if not system.path_exists(api.USER_INFO_FILE_PATH):
            return user_box
        if system.path_exists(api.USER_ICON_FILE_PATH):
            user_icon = Gtk.Image(visible=True)
            user_icon.set_from_pixbuf(get_pixbuf(api.USER_ICON_FILE_PATH, (56, 56)))
            icon_align = Gtk.Alignment(visible=True)
            icon_align.set(1, 0, 0, 0)
            icon_align.add(user_icon)
            user_box.pack_end(icon_align, False, False, 0)
        with open(api.USER_INFO_FILE_PATH) as user_info_file:
            user_info = json.load(user_info_file)
        user_info_box = Gtk.VBox(spacing=6, visible=True)
        user_label = Gtk.Label(visible=True)
        user_label.set_markup("<b>%s</b>" % user_info.get("username"))
        user_label.set_justify(Gtk.Justification.RIGHT)
        user_label.set_ellipsize(Pango.EllipsizeMode.END)
        user_label.set_alignment(1, 0.5)
        user_info_box.pack_start(user_label, False, False, 0)
        if user_info.get("steamid"):
            steam_button = Gtk.Button(visible=True)
            steam_button.set_image(
                Gtk.Image.new_from_icon_name("steam-symbolic", Gtk.IconSize.MENU)
            )
            steam_button.connect(
                "clicked",
                lambda *x: open_uri(
                    "https://steamcommunity.com/profiles/%s" % user_info["steamid"]
                ),
            )
            button_align = Gtk.Alignment(visible=True)
            button_align.set(1, 0, 0, 0)
            button_align.add(steam_button)
            user_info_box.pack_start(button_align, False, False, 0)

        user_box.pack_end(user_info_box, True, True, 0)
        return user_box

    def get_lutris_links(self):
        box = Gtk.VBox(spacing=6, visible=True)

        donate_button = get_link_button("Support Lutris!")
        donate_button.connect("clicked", lambda *x: open_uri(LINKS["donate"]))
        box.pack_start(donate_button, False, False, 6)

        help_label = Gtk.Label(visible=True)
        help_label.set_markup("<b>Help</b>")
        help_label.set_justify(Gtk.Justification.CENTER)
        box.pack_start(help_label, False, False, 6)

        help_box = Gtk.Box(spacing=6, visible=True)

        forums_button = get_default_link_button("Forums")
        #forums_button.set_size_request(-1, -1)
        forums_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        forums_button.connect("clicked", lambda *x: open_uri(LINKS["forums"]))
        help_box.pack_start(forums_button, False, False, 4)

        irc_button = get_default_link_button("IRC")
        #irc_button.set_size_request(-1, -1)
        irc_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        irc_button.connect("clicked", lambda *x: open_uri(LINKS["irc"]))
        help_box.pack_start(irc_button, True, True, 4)

        discord_button = get_default_link_button("Discord")
        #discord_button.set_size_request(-1, -1)
        discord_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        discord_button.connect("clicked", lambda *x: open_uri(LINKS["discord"]))
        help_box.pack_start(discord_button, False, False, 4)

        help_box.set_homogeneous(True)

        box.add(help_box)

        return box

    def on_running_game_select(self, widget, row):
        """Handler for hiding and showing the revealers in children"""
        if not row:
            game = None
        else:
            game = row.get_children()[0].game
        self.emit("running-game-selected", game)
