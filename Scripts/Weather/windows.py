import tkinter as tk
from PIL import Image

def create_window(w, h, title, clas):

    window = tk.Tk(className = clas)
    window.title(title)
    window.geometry(str(w) + "x" + str(h))
    
    return window

def create_frame(window, w, h):
    
    frame = tk.Frame(window,
                     width = w,
                     height = h,
                     highlightthickness = 2,
                     highlightcolor="#a9bd16")

    frame.pack(side = "top",
               fill = "both",
               expand = True)

    return frame

def create_canvas(window, w, h):
    canvas = tk.Canvas(window,
                       width = w,
                       height = h,
                       highlightthickness = 2,
                       highlightcolor="#a9bd16")
    canvas.pack()
    return canvas

def place_image(frame, img):

    img = tk.PhotoImage(file = img)
    label = tk.Label(frame, image = img)
    label.pack()
    # img = tk.PhotoImage(file = img)
    # canvas.create_image(0, 0, anchor = 'nw', image = img)
    return

def place_labels(labels, window, font):
    rely = 0.15
    relx = 0.26
    for l in labels:
        l.place(relx = relx, rely = rely)
        rely += 0.15
    return

def destroy_windows(windows):
    for w in windows:
        w.destroy()
    return

def bind_keys(windows, key, function):
    for w in windows:
        w.bind(key, function)
    return
