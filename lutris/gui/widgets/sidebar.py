"""Sidebar for the main window"""
from gi.repository import Gtk

from lutris.gui.widgets.sidebar_controls.listbox_runners import SidebarListBoxRunners
from lutris.gui.widgets.sidebar_controls.listbox_platforms import SidebarListBoxPlatforms

TYPE = 0
SLUG = 1
ICON = 2
LABEL = 3
GAMECOUNT = 4


class SidebarContainer(Gtk.VBox):
    __gtype_name__ = "LutrisSidebarContainer"

    lutris_window = None

    def __init__(self, spacing, visible, lutris_window):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.lutris_window = lutris_window
        self.place_content()

    def place_content(self):
        box = box = Gtk.VBox(spacing=12, visible=True)

        label_header_runners = Gtk.Label(visible=True)
        label_header_runners.set_markup("<b>%s</b>" % "Filter by runner")

        box.pack_start(label_header_runners, False, False, 0)

        sidebarControlRunners = SidebarListBoxRunners(self.lutris_window)
        sidebarControlRunners.set_visible(True)
        box.pack_start(sidebarControlRunners, False, False, 0)

        label_header_platforms = Gtk.Label(visible=True)
        label_header_platforms.set_markup("<b>%s</b>" % "Filter by platform")

        box.pack_start(label_header_platforms, False, False, 0)

        sidebarControlPlatforms = SidebarListBoxPlatforms(self.lutris_window)
        sidebarControlPlatforms.set_visible(True)
        box.pack_start(sidebarControlPlatforms, False, False, 0)

        self.pack_start(box, True, True, 0)
