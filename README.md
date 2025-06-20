# GUI

# 🌦️ WeatherApp – Your 4-Day Forecast Companion

**WeatherApp** is a sleek and user-friendly desktop application built with Python and PyQt5 that fetches real-time 4-day weather forecasts using the OpenWeatherMap API. Simply enter a city name or coordinates and get detailed weather data with intuitive icons and clean visuals.

*A simple and stylish weather app UI built with PyQt5*

## 🔑 Features

* 🔍 **Search by City Name or Coordinates**
  Enter a city like `London` or coordinates like `51.5074,-0.1278`.

* 📅 **4-Day Forecast**
  Automatically fetches weather for the next 4 days (in 24-hour intervals).

* 🌤️ **Emoji-Based Weather Icons**
  Clear and expressive icons for rain, snow, clouds, and more.

* 📡 **Live Data from OpenWeatherMap**
  Reliable and regularly updated data from a popular weather API.

* ❌ **Comprehensive Error Handling**
  Handles incorrect inputs, network issues, and API errors gracefully.

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure Python 3 is installed. Then install the required libraries:

```bash
pip install PyQt5 requests
```

### 🔧 Setup

1. Add your OpenWeatherMap API key:
   Replace the placeholder in `api_key = "your_api_key_here"` with your actual API key from [OpenWeatherMap](https://openweathermap.org/api).

2. Run the app:

   ```bash
   python app.py
   ```

---

## ⚙️ How It Works

* When the user enters a city or lat/long coordinates and clicks **Get Weather**, the app:

  * Uses OpenWeatherMap’s forecast API to fetch weather data.
  * Parses data in 3-hour intervals and selects one data point per day.
  * Displays the weather with temperatures in °C and matching emojis.

---

## 💻 Tech Stack

* **Language**: Python 3
* **GUI Framework**: PyQt5
* **API**: OpenWeatherMap

---

## 🎨 UI Highlights

* Fully responsive layout using `QVBoxLayout`
* Styled with `QSS` (Qt Style Sheets) for modern look
* Input, buttons, and labels styled for clarity and usability

---

## 🛠️ Future Enhancements

* [ ] Add hourly forecasts
* [ ] Enable unit switching (°C ↔ °F)
* [ ] Include weather icons or maps
* [ ] Cache or save forecast data locally


