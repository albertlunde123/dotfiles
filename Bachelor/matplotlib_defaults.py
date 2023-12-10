import os

# import colors

col_path = os.environ["HOME"] + "/.cache/wal/colors_general"
colors = [c.split("\n")[0] for c in open(col_path, "r").readlines()]
background = colors[0]
foreground = colors[1]
text_color = colors[4]
highlight = colors[6]

# style text

props = dict(boxstyle = 'square, pad=0.5',
            facecolor = highlight,
            edgecolor = text_color
)
# style axes and figure

def style_ax_fig(fig, axes, text_color=text_color, background=background):
    axes = axes.ravel()

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.set_facecolor(background)
        ax.grid(color=text_color, linestyle='-', linewidth=0.25, alpha=0.5)
        
    fig.set_facecolor(background)

    return fig, axes

    # plt.tight_layout()
