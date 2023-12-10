import tkinter as tk

# Create the main window
def display_forecast():
    window = tk.Tk(className = 'forecast_2')
    window_2 = tk.Tk(className = 'forecast')
    # Set the title and size of the window
    window.title("5-day Forecast")
    window.geometry("400x300")
    window_2.geometry("450x350")
    # window_2.overrideredirect(True)

    # Define the forecast data
    forecast = [
        {"day": "Day 1", "icon": "☀️", "temperature": "27°C"},
        {"day": "Day 2", "icon": "🌤", "temperature": "25°C"},
        {"day": "Day 3", "icon": "🌥", "temperature": "23°C"},
        {"day": "Day 4", "icon": "🌦", "temperature": "21°C"},
        {"day": "Day 5", "icon": "☁️", "temperature": "19°C"},
    ]

    colors = []

    # Set the font to Hack Nerd Font
    font = ("Hack Nerd Font", 18)

    frame = tk.Frame(window,
                     relief="solid",
                     # borderwidth = 10, bordercolor = "#e26d5c",
                     highlightthickness = 2,
                     highlightcolor = "#a9bd16")
    frame1 = tk.Frame(window_2,
                     relief="solid",
                     # borderwidth = 10, bordercolor = "#e26d5c",
                     highlightthickness = 2,
                     highlightcolor = "#a9bd16")
    frame.pack(side="top", fill="both", expand=True)
    frame1.pack(side="top", fill="both", expand=True)
    # Create a label for each day of the forecast

    rely = 0.15
    for day in forecast:
        label = tk.Label(window, text=f"{day['day']}: {day['icon']} {day['temperature']}", font=font)
        # label.config(anchor="center")
        # label.pack(side="center", pady=(5, 0))
        label.place(relx = 0.26, rely = rely)
        rely += 0.15

    # Set the window to close when it is clicked

    def on_click(event):
        window.destroy()
        window_2.destroy()

    # window.bind("<Button-1>", lambda event: window.destroy())
    window.bind("<Button-1>", on_click)
    window_2.bind("<Button-1>", on_click)

    return window, window_2# Run the Tkinter event loop
    # window_2.mainloop()
    # window.mainloop()
