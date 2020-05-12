from gi.repository import Gtk, Gdk, Pango


class CollapsiblePanel(Gtk.VBox):
    def __init__(
        self,
        spacing,
        visible,
        title,
        collapsible_content,
        non_collapsible_content,
        expanded=True
    ):
        super().__init__()

        self.set_spacing(spacing)
        self.set_visible(visible)

        self.title = title
        self.host = None
        self.collapsible_content = collapsible_content
        self.non_collapsible_content = non_collapsible_content

        self.place_content()

        self.bind_callbacks()

        self.expanded = expanded

    def expanded():
        def fget(self):
            return self._expanded

        def fset(self, value):
            # update internal value
            self._expanded = value

            # UI updates
            if self._expanded:
                self.header_arrow.set(
                    Gtk.ArrowType.DOWN,
                    Gtk.ShadowType.NONE
                )
                self.host.show()
            else:
                self.header_arrow.set(
                    Gtk.ArrowType.RIGHT,
                    Gtk.ShadowType.NONE
                )
                self.host.hide()

        return locals()
    expanded = property(**expanded())

    def place_content(self):
        self.setup_header(self.title)

        if self.non_collapsible_content is not None:
            self.pack_start(self.non_collapsible_content, False, False, 2)

        self.setup_content_host(self.collapsible_content)

    def setup_header(self, title):
        self.header_arrow = Gtk.Arrow(
            Gtk.ArrowType.DOWN,
            Gtk.ShadowType.NONE
        )

        self.header_arrow.set_visible(True)

        self.label = Gtk.Label(title)
        self.label.set_visible(True)
        self.label.modify_font(
            Pango.FontDescription("sans bold 13")
        )

        lbl_wrap = Gtk.Alignment.new(0.0, 0.5, 0.0, 0.0)
        lbl_wrap.set_visible(True)
        lbl_wrap.add(self.label)

        hbox = Gtk.Box()
        hbox.set_visible(True)
        hbox.set_border_width(2)

        hbox.pack_start(self.header_arrow, False, False, 2)
        hbox.pack_start(lbl_wrap, False, False, 2)

        self.header = Gtk.EventBox()
        self.header.set_visible(True)

        self.header.add(hbox)

        self.pack_start(self.header, False, False, 2)

    def setup_content_host(self, content):
        self.host = Gtk.VBox()
        self.host.set_visible(True)

        if content is not None:
            self.host.add(content)
        else:
            self.host.add(Gtk.VBox()) # dummy, otherwise we crash

        self.add(self.host)

    def bind_callbacks(self):
        # override show event, so that collapsed parts stay collapsed
        self.connect("show", self.show_all)

        self.header.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.header.connect("button_press_event", self.header_click_cb)

    # Change the title text
    def set_title(self, title):
        self.label.set_text(title)

    def add_content(self, content):
        # remove old content
        # for child in self.host.get_children():
        #    self.host.remove(child)

        self.host.add(content)

    def clear_content(self):
        for child in self.host.get_children():
            self.host.remove(child)

    def set_expanded(self, expanded):
        self.expanded = expanded

    def show_all(self, widget):
        # hack: do a 'set expanded' so that we can get auto flushing
        # print "overridden show_all, %s" % widget
        self.expanded = self.expanded

    # click anywhere in header
    def header_click_cb(self, widget, event):
        self.expanded ^= True
