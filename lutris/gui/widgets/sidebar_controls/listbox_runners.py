from gi.repository import Gtk, GObject

from lutris import runners
from lutris.gui.config.runner import RunnerConfigDialog
from lutris.gui.dialogs.runner_install import RunnerInstallDialog
from lutris.gui.dialogs.runners import RunnersDialog

from lutris.game import Game

from lutris.gui.widgets.sidebar_controls.listbox_sidebar_base import SidebarRowBase, SidebarHeaderBase, SidebarListBoxBase


class SidebarRowRunners(SidebarRowBase):
    def __init__(self, id_, type_, name, icon):
        super().__init__(id, type, name, icon)
        self.type = type_
        self.id = id_

    def _create_button_box(self):
        self.create_button_box()

        # Creation is delayed because only installed runners can be imported
        # and all visible boxes should be installed.
        self.runner = runners.import_runner(self.id)()
        entries = []
        if self.runner.multiple_versions:
            entries.append(
                (
                    "system-software-install-symbolic",
                    "Manage Versions",
                    self.on_manage_versions,
                )
            )
        if self.runner.runnable_alone:
            entries.append(("media-playback-start-symbolic", "Run", self.runner.run))
        entries.append(
            ("emblem-system-symbolic", "Configure", self.on_configure_runner)
        )

        for entry in entries:
            btn = Gtk.Button(
                tooltip_text=entry[1], relief=Gtk.ReliefStyle.NONE, visible=True
            )

            image = Gtk.Image.new_from_icon_name(entry[0], Gtk.IconSize.MENU)
            image.show()

            btn.add(image)
            btn.connect("clicked", entry[2])

            self.add_button(btn)

    def on_configure_runner(self, *args):
        RunnerConfigDialog(self.runner, parent=self.get_toplevel())

    def on_manage_versions(self, *args):
        dlg_title = "Manage %s versions" % self.runner.name
        RunnerInstallDialog(dlg_title, self.get_toplevel(), self.runner.name)

    def do_state_flags_changed(self, previous_flags):
        if self.id is not None and self.type == "runner":
            flags = self.get_state_flags()

            if flags & Gtk.StateFlags.PRELIGHT or flags & Gtk.StateFlags.SELECTED:
                if self.has_button_box() is False:
                    self._create_button_box()
                self.show_button_box()
            elif self.has_button_box() and self.button_box_is_visible():
                self.hide_button_box()

        Gtk.ListBoxRow.do_state_flags_changed(self, previous_flags)


class SidebarHeaderRunners(SidebarHeaderBase):
    def __init__(self, name):
        super().__init__(name)

        manage_runners_button = Gtk.Button.new_from_icon_name(
            "emblem-system-symbolic", Gtk.IconSize.MENU
        )

        manage_runners_button.props.action_name = "win.manage-runners"
        manage_runners_button.props.relief = Gtk.ReliefStyle.NONE
        manage_runners_button.set_margin_right(16)
        manage_runners_button.get_style_context().add_class("sidebar-button")

        self.add_control(manage_runners_button)

        self.add(Gtk.Separator())
        self.show_all()


class SidebarListBoxRunners(SidebarListBoxBase):
    __gtype_name__ = "SidebarListBoxRunners"

    lutris_window = None

    def __init__(self, lutris_window):
        super().__init__(lutris_window)
        self.lutris_window = lutris_window
        self.get_style_context().add_class("sidebar")
        self.installed_runners = []
        self.runners = sorted(runners.__all__)

        GObject.add_emission_hook(RunnersDialog, "runner-installed", self.update)
        GObject.add_emission_hook(RunnersDialog, "runner-removed", self.update)
        GObject.add_emission_hook(Game, "game-updated", self.update)
        GObject.add_emission_hook(Game, "game-removed", self.update)

        all_row = SidebarRowRunners(None, "runner", "All", None)
        self.add(all_row)
        self.select_row(all_row)
        for runner in self.runners:
            icon_name = runner.lower().replace(" ", "") + "-symbolic"
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
            name = runners.import_runner(runner).human_name
            self.add(SidebarRowRunners(runner, "runner", name, icon))

        self.set_filter_func(self._filter_func)
        self.set_header_func(self._header_func)
        self.update()
        self.show_all()

    def _filter_func(self, row):
        if row is None:
            return True
        else:
            if row.id is None:
                return True  # 'All'
            return row.id in self.installed_runners

    def _header_func(self, row, before):
        if row.get_header():
            return

        if not before:
            row.set_header(SidebarHeaderRunners("Manage Runners: "))

    def update(self, *args):
        self.installed_runners = [runner.name for runner in runners.get_installed()]

        self.invalidate_filter()

        self.connect("selected-rows-changed", self.on_sidebar_changed)

    def on_sidebar_changed(self, widget):
        row = widget.get_selected_row()
        if row is None:
            self.lutris_window.set_selected_filter(None, None)
        else:
            self.lutris_window.set_selected_filter(row.id, None)
