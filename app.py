import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name or coordinates:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.forecast_label = QLabel(self)  # Label to display 4-day forecast
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.forecast_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.forecast_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.forecast_label.setObjectName("forecast_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel, QPushButton {
                font-family: Calibri;
                color: #333333;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
                color: #555555;
            }
            QLineEdit#city_input {
                font-size: 40px;
                padding: 10px;
                border: 2px solid #cccccc;
                border-radius: 10px;
                background-color: #ffffff;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #45a049;
            }
            QPushButton#get_weather_button:pressed {
                background-color: #3d8b40;
            }
            QLabel#forecast_label {
                font-size: 25px;
                color: #2c3e50;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        api_key = "658a4ad59ac88a9ab31cd607e28f8773"  # Replace with your OpenWeatherMap API key
        city_input = self.city_input.text()

        # Check if the input is coordinates
        if ',' in city_input:
            lat, lon = city_input.split(',')
            lat, lon = float(lat), float(lon)
            city_name = self.get_city_name_from_coordinates(lat, lon, api_key)
            if city_name:
                self.city_input.setText(city_name)  # Automatically fill the city name
            else:
                self.display_error("Invalid coordinates or location not found")
                return
        else:
            city_name = city_input

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)

            if data["cod"] == "200":
                self.display_forecast(data)
            else:
                self.display_error("City not found or invalid response.")
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is Denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\nServer is Down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def get_city_name_from_coordinates(self, lat, lon, api_key):
        # Reverse geocoding to get city name from coordinates
        reverse_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        try:
            response = requests.get(reverse_url)
            response.raise_for_status()
            data = response.json()
            if data.get('cod') == 200:
                return data['name']  # Return city name
            else:
                return None
        except requests.exceptions.RequestException as e:
            self.display_error(f"Error fetching city from coordinates: {e}")
            return None

    def display_forecast(self, data):
        forecast = data["list"]
        result_text = ""

        # Display weather for the next 4 days (every 24 hours)
        for i in range(0, len(forecast), 8):  # Each day has 8 data points (3-hour intervals)
            day_data = forecast[i]
            date = day_data["dt_txt"].split()[0]  # Extract date only
            temperature_k = day_data["main"]["temp"]
            temperature_c = temperature_k - 273.15
            weather_id = day_data["weather"][0]["id"]
            description = day_data["weather"][0]["description"]

            result_text += (
                f"{date}: {temperature_c:.1f}°C, "
                f"{self.get_weather_emoji(weather_id)} {description}\n"
            )

        self.forecast_label.setText(result_text)

    def display_error(self, message):
        self.forecast_label.setStyleSheet("font-size: 25px; color: #e74c3c;")
        self.forecast_label.setText(message)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌧️"  # Drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️"  # Rain
        elif 600 <= weather_id <= 622:
            return "❄️"  # Snow
        elif 701 <= weather_id <= 781:
            return "🌫️"  # Atmosphere (fog, haze, etc.)
        elif weather_id == 800:
            return "☀️"  # Clear
        elif 801 <= weather_id <= 804:
            return "☁️"  # Clouds
        else:
            return "❓"  # Unknown


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
