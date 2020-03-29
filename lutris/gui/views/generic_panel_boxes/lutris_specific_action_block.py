from gi.repository import Gtk, GLib
from lutris import settings, pga
from lutris.gui.widgets.utils import (
    get_default_button,
    get_main_window
)
from lutris.util.strings import gtk_safe
from lutris.gui.config.system import SystemConfigDialog


class LutrisSpecificBlock(Gtk.VBox):
    """Panel containing the Lutris specific actions for the generic panel"""

    def __init__(self, spacing, visible, title, game_store, actions):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.game_store = game_store
        self.actions = actions
        self.place_content()

    def place_content(self):
        title_label = Gtk.Label(visible=True)
        title_label.set_markup("<b>%s</b>" % gtk_safe(self.title))
        self.pack_start(title_label, False, False, 6)

        """Show installed games checkbox"""
        cbox_installed_games = self.create_checkbox(visible=True, label="Installed Games Only", active=self.filter_installed, callback=self.on_cbox_installed_games_toggle)
        self.pack_start(cbox_installed_games, False, False, 6)

        """Show hidden games checkbox"""
        cbox_hidden_games_toggle = self.create_checkbox(visible=True, label="Show Hidden Games", active=self.show_hidden_games, callback=self.on_cbox_hidden_games_toggle)
        self.pack_start(cbox_hidden_games_toggle, False, False, 6)

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

    def create_checkbox(self, visible, label, active, callback):
        cbox = Gtk.CheckButton()
        cbox.set_visible(True)
        cbox.set_label(gtk_safe(label))
        cbox.set_active(active)
        cbox.set_action_name
        cbox.connect("toggled", callback)
        return cbox

    def on_preferences_clicked(self, button):
        SystemConfigDialog(get_main_window(button))

    def on_cbox_installed_games_toggle(self, button):
        settings.write_setting("filter_installed", bool(button.get_active()))
        self.actions["show-installed-only"].set_state(GLib.Variant('b', 
button.get_active()))
        self.game_store.filter_installed = self.filter_installed
        self.invalidate_game_filter()

    def invalidate_game_filter(self):
        """Refilter the game view based on current filters"""
        self.game_store.modelfilter.refilter()
        self.game_store.modelsort.clear_cache()
        self.game_store.sort_view(self.view_sorting, self.view_sorting_ascending)

    def show_hidden_games_changed(self, active):
        do_show_hidden_games_change(active)
        
    def do_show_hidden_games_change(self, active):
        settings.write_setting("show_hidden_games", bool(active), section="lutris")
        
        self.actions["show-hidden-games"].set_active(GLib.Variant('b', 
show_hidden_games))

        ignores = pga.get_hidden_ids()

        if active:
            self.game_store.add_games_by_ids(ignores)
        else:
            for game_id in ignores:
                self.game_store.remove_game(game_id)

    def on_cbox_hidden_games_toggle(self, button):
        do_show_hidden_games_change(button.get_active())

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
