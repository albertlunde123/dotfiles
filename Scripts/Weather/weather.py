import requests
import fontawesome as fa
import datetime


# Set the API key and location
API_KEY = 'a146716be5993f249f0399db75894e1c'
LOCATION = 'Aarhus, Denmark'
loc = LOCATION.split(",")[0]

# Send an HTTP GET request to the OpenWeatherMap API
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}')

# Parse the response
data = response.json()

# Extract the weather data
temperature = data['main']['temp']
description = data['weather'][0]['description']

# print(fa.icons)

def icon(description):
    if "clear" in description:
        icon = fa.icons["sun"]
    elif "cloud" in description:
        icon = fa.icons["cloud"]
    elif "rain" in description:
        # icon = fa.icons["cloud-rain"]
        icon = "🌦"
    elif "snow" in description:
        icon = fa.icons["snowflake"]
    else:
        icon = fa.icons["cloud"]
    return icon

# Output the temperature and icon
print(f"{icon(description)}", f"{temperature-273:.0f}°C", f"{loc}")

def get_relative_day(date):
    # Convert the date to a datetime object
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Get the current date and time
    now = datetime.datetime.now()

    # Calculate the difference between the two dates
    diff = date - now

    # Convert the difference to days
    diff_days = diff.days

    # Return the relative day and hour
    if diff_days == 0:
        return f"day 0 - {date.hour}"
    elif diff_days == 1:
        return f"day 1 - {date.hour}"
    elif diff_days == 2:
        return f"day 2 - {date.hour}"
    elif diff_days == 3:
        return f"day 3 - {date.hour}"
    elif diff_days == 4:
        return f"day 4 - {date.hour}"
    elif diff_days == 5:
        return f"day 5 - {date.hour}"
    else:
        return "invalid day"

forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={API_KEY}&units=metric"
forecast_response =  requests.get(forecast_url)
forecast_data = forecast_response.json()
# print(forecast_data)

forecast = forecast_data["list"]
for day in forecast:
    try:
        print(day["rain"])
    except:
        continue


# print(forecast[0])
i = 0
for day in forecast[::4]:
    temp = day["main"]["temp"]
    time = get_relative_day(day["dt_txt"])
    print(f"{time}h -",
            f"{temp}°C",
            icon(day["weather"][0]["description"]))
