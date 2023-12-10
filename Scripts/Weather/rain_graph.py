import numpy as np
import matplotlib.pyplot as plt
import requests
import os
import datetime

def get_next_weekdays(num_weekdays):
    today = datetime.date.today()
    weekdays = []
    for i in range(num_weekdays):
        # while today.weekday() in (5, 6):  # 5=Saturday, 6=Sunday
        #     today += datetime.timedelta(days=1)
        weekdays.append(today.strftime("%A")[0:2])
        today += datetime.timedelta(days=1)
    return weekdays

def set_location():
    path = os.environ["HOME"] + "/Scripts/Weather/locations.txt"
    with open(path, "r") as f:
        LOCATION = f.readlines()[0].strip()
        f.close()
    return LOCATION

# Set the API key and location
# Jeg skal vide hvad det første klokkeslet er.

def get_rain():
    API_KEY = 'a146716be5993f249f0399db75894e1c'
    LOCATION = set_location()
    print(LOCATION)
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={API_KEY}&units=metric"
    rain_list = []
    # Send an HTTP GET request to the OpenWeatherMap API
    response = requests.get(((forecast_url)))
    forecast = response.json()["list"]

    first_time = forecast[0]["dt_txt"].split(' ')[1].split(":")[0]
    first_time = int(first_time)
    for day in forecast:
        try:
            rain_list.append(day["rain"]["3h"])
        except:
            rain_list.append(0)
    return [np.array(rain_list), first_time]

def get_slope(r1, r2):
    return (r2 - r1)/3
def generate_points_between(rl):
    rl_dense = []

    for i in range(len(rl)):
        if i+1 == len(rl):
            continue
        else:
            sl = get_slope(rl[i], rl[i+1])
            for j in range(10):
                j += 1
                point = (3*j/10)*sl + rl[i]
                rl_dense.append(point)
    return rl_dense

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth*(6.29/5)

def style_plot(ax, fig):
    col_path = os.environ["HOME"] + "/.cache/wal/colors_general"
    colors = [c.split("\n")[0] for c in open(col_path, "r").readlines()]
    background = colors[0]
    foreground = colors[1]
    text_color = colors[4]
    highlight = colors[6]

    ax.set_facecolor(background)
    fig.set_facecolor(background)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()

    return [background,
            foreground,
            text_color,
            highlight]

def smooth_rain():
    return smooth(generate_points_between(get_rain()[0]), 10), get_rain()[1]


def plot_everything(rain, hours, first_time, colors, ax):
    # line.
    # ax.plot(hours,
    #         rain,
    #         colors[2],
    #         linewidth = 3)
    # area
    ax.fill_between(hours,
                    np.zeros(len(rain)),
                    rain,
                    color = colors[1])
    # day separators
    vmax = np.max(rain)
    coords = np.array([0, 78, 2*78, 3*78, 4*78]) + 78-first_time*3
    for i in coords:
        if i < len(hours) - 1:
            ax.vlines(hours[i],
                      0,
                      vmax+ 2,
                      colors = colors[3],
                      linewidth = 1,
                      linestyle = 'dashed')

    props = dict(boxstyle = 'square, pad=0.5',
                facecolor = colors[0],
                edgecolor = colors[1]
    )
    
    ax.set_ylim(0, vmax+2)
    for day, coord in zip(get_next_weekdays(5), hours[coords]):
        ax.text(coord -3, vmax+1, day,
            color = colors[1],
            bbox = props,
            fontsize = 16,
            fontweight = 'bold',
            horizontalalignment = 'right',
            fontname = 'Hack Nerd Font')
    return

rain, first_time = smooth_rain()
print(first_time)
hours = np.arange(0.3, 117.3, 0.3)

fig, ax = plt.subplots(1, 1, figsize = (12, 4))

colors = style_plot(ax, fig)
plot_everything(rain, hours, first_time, colors, ax)

fig.savefig(os.environ["HOME"] + "/Scripts/Weather/rain_graph.png")
