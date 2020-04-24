from gi.repository import Gtk
from lutris.gui.controls.collapsible_panel import CollapsiblePanel


class ShortCutStore:
    def __init__(self):
        self.dummy = 1


class ShortCutsView(Gtk.VBox):
    def __init__(self, spacing, visible, shortcut_store):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.shortcut_store = shortcut_store


class RelatedApplications(Gtk.VBox):
    def __init__(self, spacing, visible, store):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_store = store

        self.shortcut_store = ShortCutStore()

        self.col_pnl = None
        self.shortcut_view = None

        self.place_content()

    def place_content(self):
        label_info = Gtk.Label("Use this section to install extra applications which are specific to the main application. Examples are applications used for modding a game. In case the application needs Wine to run: if an application needs a specific Wine-prefix to run correctly, the Wizard has the option to create one.")
        label_info.set_line_wrap(True)
        label_info.set_visible(True)

        self.col_pnl = CollapsiblePanel(
            spacing=6,
            visible=True,
            title="Related Applications",
            collapsible_content=None,
            non_collapsible_content=label_info,
            expanded=True)

        self.add(self.col_pnl)

        self.add_content_to_panel()

        b2 = Gtk.Button("Replaced Content")
        b2.set_visible(True)

        b2.connect("clicked", self.on_button_clicked)

        self.col_pnl.add_content(b2)

        self.shortcut_view = ShortCutsView(6, True, self.shortcut_store)

        self.col_pnl.add_content(self.shortcut_view)

    def add_content_to_panel(self):
        return

    def on_button_clicked(self, widget):
        self.col_pnl.set_title("Hacked")
        self.col_pnl.set_expanded(False)
