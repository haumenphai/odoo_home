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
    _rec_name='time'

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








    def _conver_list_data(self, data):
        result = data.copy()
        print('aaaaaaaaaaa', result)

        for o in result:
            o['dt'] = unix2datetime(o['dt'])

            o['temp'] = f"{round(o['temp'])} ºC"
            o['feels_like'] = f"{round(o['feels_like'])} ºC"
            o['pressure'] = f"{round(o['pressure'])} hPa"
            o['humidity'] = f"{round(o['humidity'])} %"
            o['clouds'] = f"{round(o['clouds'])} %"
            o['visibility'] = f"{round(o['visibility'])} m"
            o['wind_speed'] = f"{round(o['wind_speed'], 2)} m/s"
            o['wind_deg'] = f"{round(o['wind_deg'])} º"
            o['pop'] = f"{o['pop'] * 100} %"



        return result



    def update_hourly(self, data_hourly):
        # hourly = self.search([])


        data_hourly = self._conver_list_data(data_hourly)
        for o in data_hourly:
            self.write({
                'time': o['dt'],
                'temp': o['temp'],
                'pop': o['pop'],
                'humidity': o['humidity'],
                'clouds': o['clouds'],
                'wind_speed': o['wind_speed'],
                'weather_description': o['weather'][0]['description'],
                'weather_main': o['weather'][0]['main'],
                'weather_icon': o['weather'][0]['icon']
            })
