from gi.repository import Gtk, GObject, GLib
from lutris import settings
from lutris.util.log import logger
from lutris.gui.widgets.utils import (
    get_default_button,
    get_main_window
)
from lutris.util.strings import gtk_safe
from lutris.gui.config.system import SystemConfigDialog


class LutrisSpecificBlock(Gtk.VBox):
    """Panel containing the Lutris specific actions for the generic panel"""

    def __init__(self, spacing, visible, title, game_store, actions, parent_widget):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.game_store = game_store
        self.actions = actions
        self.parent_widget = parent_widget

        self.cbox_installed_games_toggle = None
        self.cbox_hidden_games_toggle = None

        self.place_content()

    def place_content(self):
        title_label = Gtk.Label(visible=True)
        title_label.set_markup("<b>%s</b>" % gtk_safe(self.title))
        self.pack_start(title_label, False, False, 6)

        """Show installed games checkbox"""
        self.cbox_installed_games_toggle = self.create_checkbox(
            visible=True,
            label="Installed Games Only",
            active=True,
            action="show-installed-only-changed",
            callback=self.on_cbox_installed_games_toggle
        )

        self.cbox_installed_games_toggle.set_active(self.get_show_installed_games_onle_active_state())

        self.pack_start(self.cbox_installed_games_toggle, False, False, 6)

        """Show hidden games checkbox"""
        self.cbox_hidden_games_toggle = self.create_checkbox(
            visible=True,
            label="Show Hidden Games",
            active=True,
            # action="show-hidden-games-changed",
            action="show-hidden-games",
            callback=self.on_cbox_hidden_games_toggle
        )
        self.pack_start(self.cbox_hidden_games_toggle, False, False, 6)

        """Preferences"""
        preferences_button = get_default_button("", "preferences-system-symbolic")
        preferences_button.set_tooltip_text("Preferences")

        preferences_button.connect("clicked", self.on_preferences_clicked)
        preferences_button.show()

        self.pack_start(preferences_button, False, False, 6)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def create_checkbox(self, visible, label, active, action, callback):
        cbox = Gtk.CheckButton()
        cbox.set_visible(True)
        cbox.set_label(gtk_safe(label))
        # cbox.set_active(active)
        # cbox.set_action_name(action)
        cbox.set_sensitive(True)
        cbox.connect("toggled", callback)
        return cbox

    def get_show_installed_games_onle_active_state(self):
        return self.actions["show-installed-only"].get_state() is True

    def set_show_installed_games_only_controls_active(self, value):
        self.cbox_installed_games_toggle.set_active(value)

    def set_show_hidden_games_controls_active(self, value):
        self.cbox_hidden_games_toggle.set_active(value)

    def on_preferences_clicked(self, button):
        SystemConfigDialog(get_main_window(button))

    def on_cbox_installed_games_toggle(self, widget):
        # action = self.actions["show-installed-only"]
        # action.set_state(GLib.Variant("b", button.get_active()))
        self.parent_widget.do_show_installed_games_only_change(self.cbox_installed_games_toggle.get_active())

    def on_cbox_hidden_games_toggle(self, widget):
        # action = self.actions["show-hidden-games"]
        # action.set_state(GLib.Variant("b", button.get_active()))
        self.parent_widget.do_show_hidden_games_change(self.cbox_hidden_games_toggle.get_active())

    @property
    def filter_installed(self):
        return settings.read_setting("filter_installed").lower() == "true"

    @property
    def view_sorting(self):
        return settings.read_setting("view_sorting") or "name"

    @property
    def view_sorting_ascending(self):
        return settings.read_setting("view_sorting_ascending").lower() != "false"

    @property
    def show_hidden_games(self):
        return settings.read_setting("show_hidden_games").lower() == "true"
