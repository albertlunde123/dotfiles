import windows as w

win = w.create_window(1200, 400, "Rain", "Rain")
print(win)
canvas = w.create_frame(win, 1200, 400)
w.place_image(canvas, "rain_graph.png")

win.mainloop()
