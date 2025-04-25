from libqtile import bar, layout, widget
from libqtile import qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
import CustomWidgets
import custom_functions as cf
from Scripts.audio import toggle_mute, change_volume_down, change_volume_up
import subprocess
import Scripts.screenshot as screenshot
from qtile_extras import widget
import Scripts.color_getter as cg
import time
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration
# import subprocess
import os


colors = ["#f3dfa2",
          "#231d20",
          "#ea3546",
          "878472",
          "#494331",
          "#de541e"]

def change_background(qtile):
    subprocess.run(["wal", "--theme", "random"])
    subprocess.run(["python3", os.path.expanduser("~/.config/qtile/Scripts/generate_background_image.py")])
    subprocess.run(["feh", "--bg-fill", os.path.expanduser("~/.config/qtile/background.png")])

change_background(qtile)

def load_colors(colors, path):
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            colors[i] = line.strip()
    return colors

colors = load_colors(colors, os.path.expanduser("~/.cache/wal/qtile_colors"))

# subprocess.run(["python3", .config/qtile/Scripts/generate_background_image.py"])
# subprocess.run(["feh", "--bg-fill", "../qtile/background.png"])


home = os.path.expanduser('~')

mod = "mod4"
terminal = "kitty"

# screenshot.main()

# toggle_keyboard_layout()

keys = [
    # cf.tap_or_hocgcld_key(key = "o", tap_func = lazy.spawn("redshift -O 2000"), hold_func = lazy.spawn("redshift -x")),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "p", lazy.function(cf.toggle_keyboard_layout), desc="c"),
    Key([mod], "f", lazy.function(change_background), desc="c"),
    # Key([mod], "a", lazy.function(screenshot.main), desc="take screenshot"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    # sound controls

    Key([], "XF86AudioRaiseVolume", lazy.function(change_volume_up)),
    Key([], "XF86AudioLowerVolume", lazy.function(change_volume_down)),
    Key([], "XF86AudioMute", lazy.function(toggle_mute)),

    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "a", lazy.spawn("gnome-screenshot -a"), desc="Toggle floating"),

    # headphone volume
    # Key([mod], "XF86AudioRaiseVolume", lazy.spawn(os.path.expanduser("~/Scripts/Sound/sound_up.sh"))),
    # Key([mod], "XF86AudioLowerVolume", lazy.spawn(os.path.expanduser("~/Scripts/Sound/sound_down.sh"))),
    # Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute alsa_input.pci-0000_00_1f.3.analog-stereo toggle")),

    # brightness controls

    Key([], "XF86MonBrightnessUp", lazy.spawn("sh " + os.path.expanduser("~/.config/qtile/Scripts/light_up.sh"))),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
    # Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([mod], "XF86MonBrightnessDown", lazy.spawn("sh " + os.path.expanduser("~/.config/qtile/Scripts/redshift_on.sh"))),
    Key([mod], "XF86MonBrightnessUp", lazy.spawn("sh " + os.path.expanduser("~/.config/qtile/Scripts/redshift_off.sh"))),
    Key([mod, "shift"], "s", lazy.spawn("gnome-screenshot")),

    # redshift
    # Key([mod], "a", lazy.spawn("python3 " + os.path.expanduser("~/Scripts/colorGetter.py"))),
    Key([mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "z"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Key([mod, "shift"], "p",
    #     lazy.spawn(os.path.expanduser("~/Projects/Voice_Recognition/RecordTranscribe/record.sh")),
    #     desc="Spawn a command using a prompt widget"),
    
    # My custom keybindings.
    # filelauncher, shutdown, open confing

    Key([mod, "shift"], "e", 
        lazy.spawn(os.path.expanduser("~/.config/rofi/bin/powermenu")), 
        desc="Shutdown, Reboot, Logout"),
    Key([mod, "shift"], "a",
        lazy.spawn("python3 " + os.path.expanduser("~/.config/qtile/Scripts/color_getter.py")),
        desc="Get color from screen"),
    Key([mod], "d", 
        lazy.spawn(os.path.expanduser("~/.config/rofi/bin/launcher_text")), 
        desc="Shutdown, Reboot, Logout"),
    Key([mod, "shift"], "i", 
        lazy.spawn("kitty -e nvim " + os.path.expanduser("~/.config/qtile/config.py")))
]

# lazy.reload_config()

group_names = ["a","b","c","d","e","f","g","h","i"]
group_labels = [ "", "", "", "", "", "", "", "", ""]
groups = []
for g in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[g],
            label=group_labels[g],
        )
    )


for i, j in zip(groups, range(len(groups))):
    j = j + 1
    keys.extend(
        [
            Key(
                [mod],
                str(j),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                str(j),
                lazy.window.togroup(i.name),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# fun that converts rgb to hex
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# col1 and col2 should be specified in rgb
def gradient(col1, col2, width):
    colors = []

    diffs = [int((j - i)/width) for j,i in zip(col1, col2)]
    for i in range(width):
        col = [k + j*i for k,j in zip(col2, diffs)]
        colors.append(rgb_to_hex(tuple(col)))

    return colors

# col1 and col2 should be specified in hex
col1 = hex_to_rgb(colors[3])
col2 = hex_to_rgb(colors[5])
col3 = hex_to_rgb(colors[1])

gradient_border = gradient(col2, col1, 10) + [colors[0]]*5 + [colors[1]] + [colors[0]]*5 + gradient(col1, col2, 10)

print(gradient_border)

borders_max = gradient(col1, col3, 3) + [colors[0]]*7 + [colors[2]] +[colors[0]]*7 + gradient(col1, col3, 3)

layouts = [
    layout.Columns(border_focus = borders_max,
                   border_normal = (len(borders_max)-1)*[colors[0]] + [colors[1]],
                   border_width = len(borders_max),
                   margin = [0, 0, 0, 0],
                   no_titlebar = True),
    layout.Max(border_focus = borders_max,
               border_width = len(borders_max),
               margin = [75, 200, 75, 200]),
    layout.Floating(border = borders_max,
                    border_width = len(borders_max),
                    margin = [0, 0, 0, 0]),
    ]

widget_defaults = dict(
    font="Hack Nerd Font",
    fontsize=22,
    foreground = colors[1],
    padding=0,
)
extension_defaults = widget_defaults.copy()

Rect = {
    "decorations": [
        RectDecoration(colour=colors[0],
                       radius=4,
                       linewidth = 0,
                       filled=True,
                       padding=1),
        RectDecoration(colour=colors[0],
                       radius=4,
                       linewidth = 0,
                       filled=True,
                       padding=2)
    ],
    "padding": 5,
}

Border = {
    "decorations": [
        BorderDecoration(colour=colors[0],
               borderwidth = 10,
               padding_x=0,
               padding_y=0)
    ],
    "padding": 5,
}

bluetooth_status_script = os.path.expanduser("~/.config/qtile/Scripts/bluetooth_status.sh")
bluetooth_connect_script = os.path.expanduser("~/.config/qtile/Scripts/bluetooth_connect_powerbeats.sh")


# PDF launcher button
pdf_launcher = CustomWidgets.CustomGenPollText(
    click_python_func=cf.launch_pdf_selector,
    icon="  ",  # Book icon from Nerd Font
    foreground=colors[2],
    **Rect
)
bluetooth_widget = CustomWidgets.CustomGenPollText(update_script = bluetooth_status_script,
                                                   click_script = bluetooth_connect_script,
                                                   texts1 = cf.get_connected_bluetooth_device_name,
                                                   texts2 = "  - Chill.",
                                                   colors = [colors[2], colors[5]])

# bluetooth_widget.run_click_script()
print(bluetooth_widget.poll())
# subprocess.run(["/home/albert/.config/qtile/Scripts/bluetooth_connect_powerbeats.sh"], capture_output=True, text=True, shell=True)
screens = [
    Screen(
        # wallpaper=home + "/Pictures/brown.jpg",
        # wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                             # foreground = color[0]),
                # CustomWidgets.CustomIconWidget(),
                bluetooth_widget,
                pdf_launcher,
                widget.Spacer(),
                widget.GroupBox(active=colors[2],
                                inactive=colors[1],
                                highlight_method="text",
                                margin_x=0,
                                spacing=1,
                                this_current_screen_border=colors[2],
                                **Rect),
                widget.Spacer(),
                # widget.BatteryIcon(scale = 1.5,
                #                    update_interval = 10,
                #                    paddin),
                widget.PulseVolume(fmt = "  - {}",
                                   update_interval = 0.1),
                widget.Sep(linewidth=20,
                           foreground = colors[0]),
                widget.Sep(linewidth=3,
                           foreground = colors[0]),
                widget.Sep(linewidth=20,
                           foreground = colors[0]),
                widget.Battery(format = "Juice - {percent:2.0%}"),
            ],
            50,
            background=[colors[0]],
            border_width=[10, 30,20, 30],  # Draw top and bottom borders
            border_color=[colors[0],
                colors[0],
                colors[0],
                colors[0]]
        ),
        left=bar.Gap(50),
        right=bar.Gap(50),
        bottom=bar.Gap(50),
    ),
]


##################
# MOUSE BINDINGS #
##################

# functions
def close_window(qtile):
    window = qtile.current_window
    print(window.window.get_wm_class())
    if window and 'feh' in window.window.get_wm_class():
        window.kill()
    else:
        subprocess.run(['xdotool', 'click', '1'])


keys.extend(
        [
            Key(
                [mod],
                "x",
                lazy.function(close_window),
                desc="Switch to group {}".format(i.name),
            ),
        ]
    )


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    # Click([], "Button1", lazy.function(close_window))
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    border_width = len(borders_max),
    border_focus = borders_max,
    border_normal = (len(borders_max)-1)*[colors[0]] + [colors[1]],
    # border_normal = [colors[1]] + (len(borders_max)-1)*[colors[0]] + [colors[1]],
    # border_width = len(borders_max),
    # margin = [0, 0, 0, 0],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),
        Match(title="Custom Window"),
        Match(title="EAR"),# GPG key password entry
        Match(title="InputWindow"),
        Match(title="PDF Launcher"),
        Match(title="pdf_preview"),
        Match(title="LaTeX Editor (PyQtDraw)")


        # Match(title="InputWindow"),
    ]
)

@hook.subscribe.client_new
def window_open(window):
    # if window.floating:
    #     window.cmd_disable_focus()
    if window.name == "EAR":
        window.cmd_toggle_floating()
        # window.cmd_set_position_floating(0, 0, 100, 100)
    
    if window.window.get_wm_class() == "Unity":
        window.toggle_fullscreen()

auto_fullscreen = True
focus_on_window_activation = "smart"
# reconfigure_screens = True

# groups[1].label = "a"
@hook.subscribe.setgroup
def setgroup():
    for i in range(0, 9):
        qtile.groups[i].label = ""
    qtile.current_group.label = ""

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

#startup
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

lazy.reload_config()


# lazy.spawn(os.path.expanduser("~/Projects/Voice_Recognition/record.sh"))
