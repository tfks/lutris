import json
from gi.repository import Gtk, Pango
from lutris.util.strings import gtk_safe
from lutris import api
from lutris.util import system
from lutris.gui.widgets.utils import get_pixbuf, open_uri


class HeaderBlock(Gtk.Box):
    """Panel containing the header for the generic panel"""

    def __init__(self, spacing, visible, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.place_content()

    def place_content(self):
        app_title_label = Gtk.Label(visible=True)

        app_title_label.set_markup("<span font_desc='22'>%s</span>" % gtk_safe(self.title))
        app_title_label.set_alignment(0, 0.5)

        self.pack_start(app_title_label, True, True, 6)
        self.pack_start(self.get_user_info_box(), False, False, 6)

        self.set_center_widget(app_title_label)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_user_info_box(self):
        user_box = Gtk.Box(spacing=6, visible=True)

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
            steam_button.set_tooltip_text("Go to your Steam profile on the Steam website")
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
