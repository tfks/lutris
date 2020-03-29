"""Game panel"""
from gi.repository import Gtk, GObject
from lutris import runners
from lutris.gui.widgets.utils import get_link_button
from lutris.gui.views.generic_panel import GenericPanel
from lutris.gui.views.game_panel_boxes.title_block import GamePanelTitleBlock
from lutris.gui.views.game_panel_boxes.game_labels_block import GameLabelsBlock
from lutris.gui.views.game_panel_boxes.play_controls_block import PlayControlsBlock
from lutris.gui.views.game_panel_boxes.runners_block import RunnersBlock
from lutris.gui.views.game_panel_boxes.game_options_block import GameOptionsBlock
from lutris.gui.views.game_panel_boxes.wine_actions_block import WineActionsBlock
from lutris.gui.views.game_panel_boxes.other_actions_block import OtherActionsBlock


class GamePanel(GenericPanel):
    """Panel allowing users to interact with a game"""

    __gsignals__ = {
        "panel-closed": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self, game_actions, game_store):
        self.game_actions = game_actions
        self.game_store = game_store
        self.game = game_actions.game
        super().__init__(game_store=self.game_store)
        self.set_margin_left(10)
        self.set_margin_right(10)
        self.game.connect("game-start", self.on_game_start)
        self.game.connect("game-started", self.on_game_started)
        self.game.connect("game-stopped", self.on_game_stop)

    def place_content(self):
        vbox = Gtk.VBox(spacing=0, visible=True)

        """Game panel title block"""
        game_panel_title_block = GamePanelTitleBlock(spacing=6, visible=True, game=self.game, parent_widget=self)
        vbox.pack_start(game_panel_title_block, False, False, 12)

        """Game labels block"""
        game_labels_block = GameLabelsBlock(spacing=0, visible=True, game=self.game)
        vbox.pack_start(game_labels_block, False, False, 12)

        """Play controls block"""
        play_controls_block = PlayControlsBlock(spacing=0, visible=True, game_actions=self.game_actions)

        vbox.pack_start(play_controls_block, False, False, 12)

        """Runners block"""
        runners_block = RunnersBlock(visible=True, layout=Gtk.ButtonBoxStyle.EDGE, spacing=4, game_actions=self.game_actions)

        vbox.pack_start(runners_block, False, False, 12)

        """Game options"""
        game_options_block = GameOptionsBlock(spacing=4, visible=True, game_actions=self.game_actions, title="Game options", parent_widget=self)

        vbox.pack_start(game_options_block, False, False, 12)

        # vbox.set_center_widget(game_options_block)

        """WINE actions"""
        self.buttons_wine_actions = self.get_buttons_for_wine_actions()

        if self.buttons_wine_actions.items():
            wine_actions_block = WineActionsBlock(spacing=0, visible=True, buttons=self.buttons_wine_actions, title="Wine options")

            vbox.pack_start(wine_actions_block, False, False, 12)

        """Other actions"""
        other_actions_block = OtherActionsBlock(spacing=0, visible=True, game_actions=self.game_actions, title="Other options")

        vbox.pack_start(other_actions_block, True, True, 12)

        self.pack_start(vbox, True, True, 0)

    def refresh(self):
        """Redraw the panel"""
        for child in self.get_children():
            child.destroy()
        self.place_content()

    @property
    def background_id(self):
        return self.game.slug

    @staticmethod
    def get_runner_entries(game):
        """Return runner specific contextual actions"""
        try:
            runner = runners.import_runner(game.runner_name)(game.config)
        except runners.InvalidRunner:
            return None
        return runner.context_menu_entries

    def get_buttons_for_wine_actions(self):
        buttons = {}
        if self.game.runner_name and self.game.is_installed:
            for entry in self.get_runner_entries(self.game):
                name, label, callback = entry
                button = get_link_button(label)
                button.show()
                button.connect("clicked", callback)
                buttons[name] = button
        return buttons

    def on_game_start(self, _widget):
        """Callback for the `game-start` signal"""
        self.buttons["play"].set_label("Launching...")
        self.buttons["play"].set_sensitive(False)

    def on_game_started(self, _widget):
        """Callback for the `game-started` signal"""
        self.buttons["stop"].show()
        self.buttons["play"].hide()
        self.buttons["play"].set_label("Play")
        self.buttons["play"].set_sensitive(True)

    def on_game_stop(self, _widget, _game_id=None):
        """Called when a game is stopped (`game-stopped` signal)"""
        self.refresh()

    def on_shortcut_edited(self, _widget, action_id):
        """Callback for shortcut buttons"""
        self.buttons[action_id].hide()
        if action_id[0:2] == "rm":
            self.buttons[action_id[3:]].show()
        else:
            self.buttons["rm-" + action_id].show()

    def on_close(self, _widget):
        """Callback for the clone panel button"""
        self.emit("panel-closed")
