from gi.repository import Gtk


def get_treeview_bg_color(gtk_state_flag):
    win = Gtk.Window()
    vb = Gtk.VBox()
    tv = Gtk.TreeView()
    vb.add(tv)
    # win.show_all()
    style = tv.get_style_context()
    bgcolor = style.get_background_color(gtk_state_flag)

    return bgcolor

