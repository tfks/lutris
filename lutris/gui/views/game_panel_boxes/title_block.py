from gi.repository import Gtk, Pango
from lutris.gui.widgets.utils import get_pixbuf_for_game
from lutris.util.strings import gtk_safe


class GamePanelTitleBlock(Gtk.Box):
    """Panel containing the header for the game panel"""

    def __init__(self, spacing, visible, game, parent_widget):
        super().__init__()
        self.set_spacing(spacing)
        self.set_visible(visible)
        self.game = game
        self.parent_widget = parent_widget
        self.place_content()

    def place_content(self):
        title_label = Gtk.Label()

        self.set_title_label_styles(title_label)

        self.pack_start(self.get_icon(), False, False, 6)
        self.pack_start(title_label, True, True, 0)
        self.pack_start(self.get_close_button(), False, False, 6)

        self.set_center_widget(title_label)

        self.set_size_request(-1, 25)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    def get_close_button(self):
        """Return the close button"""
        button = Gtk.Button.new_from_icon_name(
            "window-close-symbolic", Gtk.IconSize.MENU
        )
        button.set_tooltip_text("Close")
        button.set_size_request(32, 32)
        button.connect("clicked", self.on_close)
        button.show()
        return button

    def get_icon(self):
        """Return the game icon"""
        icon = Gtk.Image.new_from_pixbuf(get_pixbuf_for_game(self.game.slug, "icon"))
        icon.show()
        return icon

    def set_title_label_styles(self, title_label):
        """Style the label with the game's title"""
        title_label.set_markup(
            "<span font_desc='16'>%s</span>" % gtk_safe(self.game.name)
        )
        title_label.set_ellipsize(Pango.EllipsizeMode.END)
        title_label.show()
        return title_label

    def on_close(self, _widget):
        """Callback for the clone panel button"""
        self.parent_widget.on_close(self.parent_widget)
