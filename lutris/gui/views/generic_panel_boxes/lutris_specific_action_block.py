from gi.repository import Gtk
from lutris.gui.widgets.utils import (
    get_default_button,
    get_main_window
)
from lutris.util.strings import gtk_safe
from lutris.gui.config.system import SystemConfigDialog


class LutrisSpecificBlock(Gtk.VBox):
    """Panel containing the Lutris specific actions for the generic panel"""

    def __init__(self, spacing, visible, title):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.title = title
        self.place_content()

    def place_content(self):
        title_label = Gtk.Label(visible=True)
        title_label.set_markup("<b>%s</b>" % gtk_safe(self.title))
        self.pack_start(title_label, False, False, 6)

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

    def on_preferences_clicked(self, button):
        SystemConfigDialog(get_main_window(button))
