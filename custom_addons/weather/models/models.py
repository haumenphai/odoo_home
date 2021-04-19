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
    
    
   
    
    
    
    
    
    # def _conver_data(self, data):
        # result = data.copy()
        #
        #
        # data['dt'] = unix2datetime(data['dt'])
        #
        # data['temp'] = f"{round(data['temp'])} ºC"
        # data['feels_like'] = f"{round(data['feels_like'])} ºC"
        # data['pressure'] = f"{round(data['pressure'])} hPa"
        # data['humidity'] = f"{round(data['humidity'])} %"
        # data['clouds'] = f"{round(data['clouds'])} %"
        # data['visibility'] = f"{round(data['visibility'])} m"
        # data['wind_speed'] = f"{round(data['wind_speed'], 2)} m/s"
        # data['wind_deg'] = f"{round(data['wind_deg'])} º"
        # data['pop'] = f"{data['pop'] * 100} %"
        #
        # return result
        #
        #
    # def update_hourly(self, data_hourly):
        # hourly = self.search([])
        #
        # for r in hourly:
            # try:
                # data = self._conver_data(data_hourly)
                # for o in data:
                    # r.write({
                    # 'time': o['dt'],
                    # 'temp': o['temp'],
                    # 'pop': o['pop'],
                    # 'humidity': o['humidity'],
                    # 'clouds': o['clouds'],
                    # 'wind_speed': o['wind_speed'],
                    # 'weather_description': o['weather'][0]['description'],
                    # 'weather_main': o['weather'][0]['main'],
                    # 'weather_icon': o['weather'][0]['icon']
                    # })
            # except Exception as e:
                # print(e)
            
        
    
    





