from gi.repository import Gtk
from lutris.gui.widgets.utils import (
    get_link_button,
    get_default_link_button,
    open_uri
)
from lutris.util.strings import gtk_safe

LINKS = {
    "donate": "https://lutris.net/donate",
    "forums": "https://forums.lutris.net/",
    "discord": "https://discord.gg/Pnt5CuY",
    "irc": "irc://irc.freenode.org:6667/lutris"
}


class LinksBlock(Gtk.VBox):
    """Panel containing the links for the generic panel"""

    def __init__(self, spacing, visible, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.place_content()

    def place_content(self):
        donate_button = get_link_button("Support Lutris!")
        donate_button.connect("clicked", lambda *x: open_uri(LINKS["donate"]))
        self.pack_start(donate_button, False, False, 6)

        help_label = Gtk.Label(visible=True)
        help_label.set_markup("<b>%s</b>" % gtk_safe(self.title))
        help_label.set_justify(Gtk.Justification.CENTER)
        self.pack_start(help_label, False, False, 6)

        help_box = Gtk.Box(spacing=6, visible=True)

        forums_button = get_default_link_button("Forums")
        forums_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        forums_button.connect("clicked", lambda *x: open_uri(LINKS["forums"]))
        help_box.pack_start(forums_button, False, False, 4)

        irc_button = get_default_link_button("IRC")
        irc_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        irc_button.connect("clicked", lambda *x: open_uri(LINKS["irc"]))
        help_box.pack_start(irc_button, True, True, 4)

        discord_button = get_default_link_button("Discord")
        discord_button.get_children()[0].set_justify(Gtk.Justification.CENTER)
        discord_button.connect("clicked", lambda *x: open_uri(LINKS["discord"]))
        help_box.pack_start(discord_button, False, False, 4)

        help_box.set_homogeneous(True)

        self.add(help_box)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()
