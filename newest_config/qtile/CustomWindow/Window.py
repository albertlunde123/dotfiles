import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="My Custom Window")
        
        # Create the main vertical box layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Create a separate vbox for the label
        label_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.label = Gtk.Label(label="Can I help youwith anything?", xalign=0)
        # label_vbox.pack_start(self.label, False, False, 10)  # Added padding

        self.image = Gtk.Image()
        self.image.set_from_file("CanIHelpYou.svg")
        label_vbox.pack_start(self.image, False, False, 10)  # Added padding
        main_vbox.pack_start(label_vbox, False, False, 0)

        # Create a separate vbox for the entry
        entry_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.textview = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)  # Use Gtk.TextView
        self.textview.set_left_margin(50)
        self.textview.set_right_margin(50)
        entry_vbox.pack_start(self.textview, True, True, 10)  # Added padding
        main_vbox.pack_start(entry_vbox, True, True, 0)
        
        # Set CSS styles
        style_provider = Gtk.CssProvider()
        css = """
            * {
                background-color: #24283b;
                color: #c0caf5;
                font-family: 'Courier New';
            }
            textview {
                border: none;  /* Removed the border */
            }
            textview:focus {
                outline: none;  /* Removed focus outline */
            }
        """
        style_provider.load_from_data(bytes(css.encode()))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Add main vertical box to window
        self.add(main_vbox)
        
        # Connect the "configure-event" signal to dynamically change font size
        self.connect("configure-event", self.on_resize)

    def on_resize(self, widget, event):
        # Calculate a suitable font size based on window height
        font_size = int(event.height / 20)
        font_desc = Pango.FontDescription(f"Courier New {font_size}")
        self.label.modify_font(font_desc)
        self.textview.modify_font(font_desc)

if __name__ == "__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

