from libqtile import bar, widget, layout
from libqtile.config import Key, Group, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
from libqtile.command import lazy as lz
import random

mod = "mod4"

keys = [
    Key([mod], "Return", lazy.spawn("xterm")),
    Key([mod], "r", lazy.restart()),
]

groups = [Group("a")]

layouts = [
    layout.Stack()
]

class CustomGenPollText(widget.GenPollText):
    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(CustomGenPollText.defaults)

    defaults = [
        ("update_interval", 1, "Update interval in seconds."),
    ]

    def poll(self):
        if self.foreground == "#ff0000":
            self.foreground = "#0000ff"
        else:
            self.foreground = "#ff0000"
        self.bar.draw()
        return "I update color"

# Instantiate it like this
custom_widget = CustomGenPollText()

# color_toggling_widget = widget.GenPollText(
#     name = "color_toggling_widget",
#     func=simple_poll_text,
#     update_interval=10,
#     foreground="ff0000",
#     mouse_callbacks={"Button1": lambda: update_color(color_toggling_widget)},
# )

screens = [
    Screen(
        top=bar.Bar(
            [
                custom_widget,
            ],
            24,
        ),
    ),
]

@hook.subscribe.startup_once
def startup():
    pass

main = None

@hook.subscribe.client_new
def _(window):
    if (window.window.get_wm_class()[0] == "XTerm"):
        window.togroup("a")

if __name__ in ["config", "__main__"]:
    from libqtile import layout

    main = None

