from gi.repository import Gtk, Gdk

from lutris.gui.widgets.utils import (
    get_default_button,
    get_main_window
)
from lutris.gui.controls.collapsible_panel import CollapsiblePanel


class OtherVersionsView(Gtk.VBox):
    def __init__(
        self,
        spacing,
        visible,
        store,
        add_click_callback,
        del_click_callback,
        play_click_callback,
        stop_click_callback,
        configure_click_callback
    ):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.shortcut_store = store

        self.selected_game = None
        self.current_path = None

        self.btn_play = None

        self.add_click_callback = add_click_callback
        self.del_click_callback = del_click_callback
        self.play_click_callback = play_click_callback
        self.stop_click_callback = stop_click_callback
        self.configure_click_callback = configure_click_callback

        self.get_style_context().add_class("other-versions-view")

        self.item_view = None

        self.place_content()

    def place_content(self):
        # Add toolbar with Add / remove buttons...
        box_tools = Gtk.Box(spacing=6, visible=True)

        btn_add = self.create_button(
            text = "",
            icon = "add",
            tooltip = "Add another version",
            visible = True,
            sensitive = True,
            clicked_callback = self.add_click_callback
        )

        box_tools.pack_start(btn_add, False, False, 6)

        btn_del = self.create_button(
            text = "",
            icon = "delete",
            tooltip = "Remove selected version",
            visible = True,
            sensitive = False,
            clicked_callback = self.del_click_callback
        )

        box_tools.pack_start(btn_del, False, False, 6)

        hsep1 = Gtk.HSeparator()

        hsep1.set_visible(True)

        box_tools.pack_start(hsep1, False, False, 6)

        self.btn_play = self.create_button(
            text = "",
            icon = "media-playback-start",
            tooltip = "Play",
            visible = True,
            sensitive = False,
            clicked_callback = self.play_click_callback
        )

        box_tools.pack_start(self.btn_play, False, False, 6)

        self.btn_stop = self.create_button(
            text = "",
            icon = "media-playback-stop",
            tooltip = "Stop",
            visible = False,
            sensitive = False,
            clicked_callback = self.stop_click_callback
        )

        box_tools.pack_start(self.btn_stop, False, False, 6)

        hsep2 = Gtk.HSeparator()

        hsep2.set_visible(True)

        box_tools.pack_start(hsep2, False, False, 6)

        self.btn_config = self.create_button(
            text = "",
            icon = "preferences-system-symbolic",
            tooltip = "Configure",
            visible = True,
            sensitive = False,
            clicked_callback = self.configure_click_callback
        )

        box_tools.pack_start(self.btn_config, False, False, 6)

        self.pack_start(box_tools, True, True, 6)

        box_item_view = Gtk.Box(spacing=6, visible=True)

        self.item_view = Gtk.IconView()
        self.item_view.get_style_context().add_class("other-versions-view-item-view")
        self.item_view.set_visible(True)
        self.item_view.set_size_request(-1, 200)

        self.item_view.connect("selection-changed", self.on_selection_changed)

        box_item_view.pack_end(self.item_view, True, True, 6)

        self.pack_end(box_item_view, True, True, 6)

    def create_button(self, text, icon, tooltip, visible, sensitive, clicked_callback):
        btn = get_default_button(text, icon)
        btn.set_tooltip_text(tooltip)
        btn.set_visible(visible)
        btn.set_sensitive(sensitive)

        btn.connect("clicked", clicked_callback)

        return btn

    def get_selected_item(self):
        """Return the currently selected game's id."""
        selection = self.get_selected_items()
        if not selection:
            return
        self.current_path = selection[0]
        return self.get_model().get_iter(self.current_path)

    def on_selection_changed(self, _view):
        selected_item = self.get_selected_item()
        if selected_item:
            self.selected_game = self.get_selected_game(selected_item)
        else:
            self.selected_game = None


class OtherVersions(Gtk.VBox):
    def __init__(
        self,
        spacing,
        visible,
        store,
        title,
        info_text,
        add_click_callback,
        del_click_callback,
        play_click_callback,
        stop_click_callback,
        configure_click_callback
    ):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)

        self.add_click_callback = add_click_callback
        self.del_click_callback = del_click_callback
        self.play_click_callback = play_click_callback
        self.stop_click_callback = stop_click_callback
        self.configure_click_callback = configure_click_callback

        self.title = title
        self.info_text = info_text

        self.get_style_context().add_class("other-versions")

        self.other_versions_store = store

        self.col_pnl = None
        self.other_versions_view = None

        self.place_content()

        self.set_styling()

    def place_content(self):
        label_info = Gtk.Label(self.info_text)
        label_info.set_line_wrap(True)
        label_info.set_visible(True)

        self.col_pnl = CollapsiblePanel(
            spacing=6,
            visible=True,
            title=self.title,
            collapsible_content=None,
            non_collapsible_content=label_info,
            expanded=True
        )

        self.add(self.col_pnl)

        self.other_versions_view = OtherVersionsView(
            spacing=6,
            visible=True,
            store=self.other_versions_store,
            add_click_callback=self.add_click_callback,
            del_click_callback=self.del_click_callback,
            play_click_callback=self.play_click_callback,
            stop_click_callback=self.stop_click_callback,
            configure_click_callback=self.configure_click_callback
        )

        self.col_pnl.add_content(self.other_versions_view)

    def set_styling(self):
        style = Gtk.StyleContext()
        style.add_class(Gtk.STYLE_CLASS_VIEW)
        bg_provider = Gtk.CssProvider()
        bg_provider.load_from_data(
            (
                ".other-versions { background-color: rgba(0, 0, 0, 0.2) }"
            ).encode("utf-8")
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            bg_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
