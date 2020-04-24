from gi.repository import Gtk
from lutris.gui.controls.collapsible_panel import CollapsiblePanel


class OtherVersionsStore:
    def __init__(self):
        self.dummy = 1


class OtherVersionsView(Gtk.VBox):
    def __init__(self, spacing, visible, shortcut_store):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.shortcut_store = shortcut_store


class OtherVersions(Gtk.VBox):
    def __init__(self, spacing, visible, store):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game_store = store

        self.other_versions_store = OtherVersionsStore()

        self.col_pnl = None
        self.other_versions_view = None

        self.place_content()

    def place_content(self):
        label_info = Gtk.Label("Use this section to install different version of the same game. This can come in handy when trying out different settings but without having to uninstall the original version. In case the application needs Wine to run: The wizard will ask for the location where the new Wine-prefix is to be created.")
        label_info.set_line_wrap(True)
        label_info.set_visible(True)

        self.col_pnl = CollapsiblePanel(
            spacing=6,
            visible=True,
            title="Other versions",
            collapsible_content=None,
            non_collapsible_content=label_info,
            expanded=True)

        self.add(self.col_pnl)

        self.add_content_to_panel()

        b2 = Gtk.Button("Replaced Content")
        b2.set_visible(True)

        b2.connect("clicked", self.on_button_clicked)

        self.col_pnl.add_content(b2)

        self.other_versions_view = OtherVersionsView(
            6,
            True,
            self.other_versions_store
        )

        self.col_pnl.add_content(self.other_versions_view)

    def add_content_to_panel(self):
        return

    def on_button_clicked(self, widget):
        self.col_pnl.set_title("Hacked")
        self.col_pnl.set_expanded(False)
