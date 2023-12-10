import pyperclip
import pyautogui
import requests
import tkinter as tk

# Replace YOUR_API_KEY with your own API key from OpenWeatherMap
API_KEY = "YOUR_API_KEY"

# Set the units to be used for temperature
UNITS = "metric"

# Set the default location
DEFAULT_LOCATION = "New York, US"

# Get the current location from the clipboard
current_location = pyperclip.paste()

# If the clipboard is empty, use the default location
if not current_location:
    current_location = DEFAULT_LOCATION

# Create the user interface
root = tk.Tk()
root.title("Select Location")

# Create a label to display the current location
label = tk.Label(root, text=f"Current location: {current_location}")
label.pack()

# Create an entry field for entering a new location
entry = tk.Entry(root)
entry.pack()

# Create a function to search for a location
def search():
    # Get the location from the entry field
    location = entry.get()

    # Use the OpenWeatherMap API to search for the location
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={UNITS}&appid={API_KEY}")

    # If the location was not found, display an error message
    if response.status_code != 200:
        label.config(text="Location not found")
        return

    # Extract the city ID from the JSON response
    data = response.json()
    city_id = data["id"]

    # Copy the city ID to the clipboard
    pyperclip.copy(str(city_id))

    # Close the user interface
    root.destroy()

# Create a button to search for a location
button = tk.Button(root, text="Search", command=search)
button.pack()

# Run the user interface
root.mainloop()

