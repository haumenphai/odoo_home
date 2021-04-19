# -*- coding: utf-8 -*-
from odoo import models, fields, api

from urllib.request import urlopen
import json, time
from datetime import datetime

def unix2datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime)




class WeatherHourly(models.Model):
    _name = 'weather.hourly'
    _description = ''
    # _rec_name='time'
    name = fields.Char()

    time = fields.Datetime('Lúc')
    temp = fields.Char('Nhiệt độ')
    pop = fields.Char('Xác suất mưa')
    humidity = fields.Char('Độ ẩm')
    clouds = fields.Char('Mây')
    wind_speed = fields.Char('Tốc độ gió')


    @api.depends('weather_icon')
    def _get_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'


    weather_main = fields.Char()
    weather_description = fields.Char('Miêu tả')
    weather_icon = fields.Char()

    json = fields.Text()

    def convert_data(self, data):
        result = data.copy()

        result['dt'] = unix2datetime(result['dt'])

        result['temp'] = f"{round(result['temp'])} ºC"
        result['feels_like'] = f"{round(result['feels_like'])} ºC"
        result['pressure'] = f"{round(result['pressure'])} hPa"
        result['humidity'] = f"{round(result['humidity'])} %"
        result['clouds'] = f"{round(result['clouds'])} %"
        result['visibility'] = f"{round(result['visibility'])} m"
        result['wind_speed'] = f"{round(result['wind_speed'], 2)} m/s"
        result['wind_deg'] = f"{round(result['wind_deg'])} º"
        result['pop'] = f"{result['pop'] * 100} %"


        return result



    def update_hourly(self, data):
        """
            self: single
            data: single data hourly
        """

        data1 = self.convert_data(data)

        self.write({
            'time': data1['dt'],
            'temp': data1['temp'],
            'pop': data1['pop'],
            'humidity': data1['humidity'],
            'clouds': data1['clouds'],
            'wind_speed': data1['wind_speed'],
            'weather_description': data1['weather'][0]['description'],
            'weather_main': data1['weather'][0]['main'],
            'weather_icon': data1['weather'][0]['icon']
        })
