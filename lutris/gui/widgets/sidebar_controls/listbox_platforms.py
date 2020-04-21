from gi.repository import Gtk

from lutris import platforms
from lutris import pga
from lutris.gui.config.runner import RunnerConfigDialog
from lutris.gui.dialogs.runner_install import RunnerInstallDialog

from lutris.gui.widgets.sidebar_controls.listbox_sidebar_base import SidebarRowBase, SidebarHeaderBase, SidebarListBoxBase


class SidebarRowPlatforms(SidebarRowBase):
    def __init__(self, id_, type_, name, icon):
        super().__init__(id, type, name, icon)
        self.type = type_
        self.id = id_

    def _create_button_box(self):
        if self.has_button_box():
            return

        self.create_button_box()

    def on_configure_runner(self, *args):
        RunnerConfigDialog(self.runner, parent=self.get_toplevel())

    def on_manage_versions(self, *args):
        dlg_title = "Manage %s versions" % self.runner.name
        RunnerInstallDialog(dlg_title, self.get_toplevel(), self.runner.name)


class SidebarHeaderPlatforms(SidebarHeaderBase):
    def __init__(self, name):
        super().__init__(name)

        self.add(Gtk.Separator())
        self.show_all()


class SidebarListBoxPlatforms(SidebarListBoxBase):
    __gtype_name__ = "SidebarListBoxPlatforms"

    lutris_window = None

    def __init__(self, lutris_window):
        super().__init__(lutris_window)
        self.active_platforms = pga.get_used_platforms()
        self.platforms = sorted(platforms.__all__)

        self.add(SidebarRowPlatforms(None, "platform", "All", None))
        for platform in self.platforms:
            icon_name = (
                platform.lower().replace(" ", "").replace("/", "_") + "-symbolic"
            )
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
            self.add(SidebarRowPlatforms(platform, "platform", platform, icon))

        self.set_filter_func(self._filter_func)
        # self.set_header_func(self._header_func)
        self.update()
        self.show_all()

    def _filter_func(self, row):
        if row is None:
            return True
        else:
            if len(self.active_platforms) <= 1:
                return False  # Hide useless filter
            elif row.id is None:  # 'All'
                return True
            return row.id in self.active_platforms

    def _header_func(self, row, before):
        if row.get_header():
            return

        if not before:
            row.set_header(SidebarHeaderPlatforms("Platforms"))

    def update(self, *args):
        self.active_platforms = pga.get_used_platforms()
        self.invalidate_filter()

        self.connect("selected-rows-changed", self.on_sidebar_changed)

    def on_sidebar_changed(self, widget):
        row = widget.get_selected_row()
        if row is None:
            self.lutris_window.set_selected_filter(None, None)
        else:
            self.lutris_window.set_selected_filter(None, row.id)
