import os
from gi.repository import Gtk, Pango
from lutris.util import datapath


class SidebarRowBase(Gtk.ListBoxRow):
    def __init__(self, id_, type_, name, icon):
        super().__init__()
        self.type = type_
        self.id = id_
        self.btn_box = None

        self.box = Gtk.Box(spacing=6, margin_start=9, margin_end=9)

        # Construct the left column icon space.
        if icon:
            self.box.add(icon)
        else:
            # Place a spacer if there is no loaded icon.
            icon = Gtk.Box(spacing=6, margin_start=9, margin_end=9)
            self.box.add(icon)

        label = Gtk.Label(
            label=name,
            halign=Gtk.Align.START,
            hexpand=True,
            margin_top=6,
            margin_bottom=6,
            ellipsize=Pango.EllipsizeMode.END,
        )
        self.box.add(label)

        self.add(self.box)

    def create_button_box(self):
        self.btn_box = Gtk.Box(
            spacing=3, no_show_all=True, valign=Gtk.Align.CENTER, homogeneous=True
        )

        self.box.add(self.btn_box)

    def has_button_box(self):
        if self.btn_box is None:
            return False
        else:
            return True

    def show_button_box(self):
        self.btn_box.show()

    def hide_button_box(self):
        self.btn_box.hide()

    def button_box_is_visible(self):
        return self.btn_box.get_visible()

    def add_button(self, button):
        self.btn_box.pack_start(button, False, False, 0)


class SidebarHeaderBase(Gtk.Box):
    def __init__(self, name):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.get_style_context().add_class("sidebar-header")
        label = Gtk.Label(
            halign=Gtk.Align.START,
            hexpand=True,
            use_markup=True,
            label="<b>{}</b>".format(name),
        )
        label.get_style_context().add_class("dim-label")
        self.box = Gtk.Box(margin_start=9, margin_top=6, margin_bottom=6, margin_right=6)
        self.box.add(label)
        self.add(self.box)

        self.show_all()

    def add_control(self, control):
        self.box.pack_start(control, False, False, 0)


class SidebarListBoxBase(Gtk.ListBox):
    __gtype_name__ = "SidebarListBoxBase"

    lutris_window = None

    def __init__(self, lutris_window):
        super().__init__()
        self.lutris_window = lutris_window
        self.get_style_context().add_class("sidebar")

        # TODO: This should be in a more logical location
        icon_theme = Gtk.IconTheme.get_default()
        local_theme_path = os.path.join(datapath.get(), "icons")
        if local_theme_path not in icon_theme.get_search_path():
            icon_theme.prepend_search_path(local_theme_path)
