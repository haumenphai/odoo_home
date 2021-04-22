from odoo import models, fields, api

from urllib.request import urlopen
import json


class WeatherApi(models.AbstractModel):
    _name = 'weather.api'
    _description = 'weather api'

    def get_data_weather_current(self, lat, lon, apikey, units='metric', lang="en"):
        """
            document: https://openweathermap.org/current
        """
        response = urlopen(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units={units}&lang={lang}')
        data = json.load(response)
        return data

    def get_data_weather_onecall(self, lat, lon, apikey, units='metric', lang="en"):
        """
            document: https://openweathermap.org/api/one-call-api
        """
        response = urlopen(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apikey}&units={units}&lang={lang}')
        data = json.load(response)
        return data