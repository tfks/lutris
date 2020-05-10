from gi.repository import Gtk


def get_background_color(widget, gtk_state_flag):
    if gtk_state_flag is not Gtk.StateFlags:
        return ""

    context = widget.get_style_context()
    # bgcolor = context.get_background_color(gtk_state_flag)

    # window = Gtk.Window()
    # context = window.get_style_context()
    # this one is buggy
    bgcolor = context.get_property("background-color", gtk_state_flag)

    return bgcolor

