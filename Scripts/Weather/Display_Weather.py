import os
import tkinter as tk

def display_weather():
    window = tk.Tk(className = 'Rain')
    window.geometry('1200x400')

    with open('locations.txt', 'r') as f:
        locations = f.readlines()[0].strip().split(',')[0]
        f.close()

    window.title('Rain' + ' - ' + locations)

    # display a png image in the window
    img = tk.PhotoImage(file = 'rain_graph.png')

    # create a canvas to display the image
    canvas = tk.Canvas(window,
                       width = 1200,
                       height = 400,
                       highlightthickness = 2,
                       highlightcolor = "#a9bd16")
    canvas.pack()

    # display the image on the canvas
    canvas.create_image(0, 0, anchor = 'nw', image = img)

    # Lav billedet bagved som giver illusion om doubler border
    window_2 = tk.Tk(className = 'Rain2')
    window_2.geometry('1300x500')
    canvas1 = tk.Canvas(window_2,
                       width = 1300,
                       height = 500,
                       highlightthickness = 2,
                       highlightcolor = "#a9bd16")
    canvas1.pack()

    def on_click(e):
        window.destroy()
        window_2.destroy()

    window.bind("<Button-1>", on_click)
    window_2.bind("<Button-1>", on_click)
    window_2.mainloop()
    # window.mainloop()
    return
display_weather()
