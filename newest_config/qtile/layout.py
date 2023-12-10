from qtile import layout

borders_max = [colors[0]] * 75 + [colors[1]] + [colors[0]] * 10 + [colors[2]] + [colors[0]] * 10 + [colors[1]]


border_foc =  [colors[1]] + 10*[colors[0]] + [colors[1]]
layouts = [
    layout.Columns(border_focus = border_foc,
                   border_normal = colors[0],
                   border_width = len(border_foc),
                   margin = [10, 10, 10, 10]),
    layout.Max(border_focus = borders_max,
               border_width = len(borders_max)),
               # margin = [0, 100, 0, 100]),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]
