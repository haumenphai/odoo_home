# -*- coding: utf-8 -*-

from odoo import models, fields, api

from urllib.request import urlopen
import json, time
from docutils.languages import da
from stdnum import ro
from datetime import datetime


  
apikey = '3e65cba6de46a1e4074e68215ed5938a'

class WeatherApi(models.AbstractModel):
    _name = 'weather.api'
    _description = 'weather api'
    
    def get_data_weather_current(self, lat, lon, units, apikey):
        """
            document: https://openweathermap.org/current
            :param lat:
            :param lon:
            :param units:
            :param apikey:
        """
        response = urlopen(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units={units}')
        data = json.load(response)
        return data
    
    def get_data_weather_onecall(self, lat, lon, units, apikey):
        response = urlopen(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apikey}&units={units}')
        data = json.load(response)
        return data
        

    

class WeatherForecast(models.Model):
    _name = 'weather.forecast'
    _description = ''
    _inherit = 'weather.api'
    

    name = fields.Char(string='Thành phố')
    lat = fields.Float(string='Kinh độ')
    lon = fields.Float(string='Vĩ độ')     
    
    temp = fields.Integer(string='Nhiệt độ')
    feels_like = fields.Integer(string='Cảm nhận')
    humidity = fields.Integer(string='Độ ẩm')
    pressure = fields.Integer('Áp suất')
    
    clouds = fields.Integer('Mây')
    
    visibility = fields.Integer('Tầm nhìn')
    wind_speed = fields.Float('Tốc độ gió')
    wind_deg = fields.Integer('Hướng gió')
    
    sunrise = fields.Datetime('Bình minh')
    sunset = fields.Datetime('Hoàng hôn')
    
    weather_id = fields.Char()
    weather_main = fields.Char()
    weather_description = fields.Char()
    weather_icon = fields.Char()
    
    dt = fields.Datetime(string='Cập nhật lúc')
    
    #==========================================================================
    
    @api.onchane
    def get_temp_show(self):
        return f'{self.temp} ºC'
    
    def get_humidity_show(self):
        return f'{self.humidity} %'
    
    def get_clouds_show(self):
        return f'{self.coulds} %'
    
    def get_visibility_show(self):
        r = self.visibility / 1000
        r = round(r, 2)
        return f'{r} km'
    
    def get_wind_speed_show(self):
        return f'{self.wind_speed} %'
    
    def get_wind_deg_show(self):
        return f'self.wind_deg º'
     
    # temp_show = fields.Char(string='Nhiệt độ', compute=get_temp_show, )
    # humidity_show = fields.Char(string='Độ ẩm', compute=get_humidity_show)
    # clouds_show = fields.Char(string='Mây', compute=get_clouds_show)
    # visibility_show = fields.Char('Tầm nhìn', compute=get_visibility_show)
    # wind_speed_show = fields.Char('Tốc độ gió', compute=get_wind_speed_show)
    # wind_deg_show = fields.Char('Gió', compute=get_wind_deg_show)
    
    temp_show = fields.Char(string='Nhiệt độ')
    humidity_show = fields.Char(string='Độ ẩm')
    clouds_show = fields.Char(string='Mây')
    visibility_show = fields.Char('Tầm nhìn')
    wind_speed_show = fields.Char('Tốc độ gió')
    wind_deg_show = fields.Char('Gió')
   
    
   
    
    
    
    
    
    def update_data_weather(self):
        cities = self.search([])
        
        for city in cities:    
            data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, units='metric', apikey=apikey)
            data = self.conver_data(data)
            
            current = data['current']
            weather = data['current']['weather'][0]
              
            city.write({
                'temp':  current['temp'],
                'feels_like': current['feels_like'],
                'humidity': current['humidity'],
                'pressure': current['pressure'],
                'humidity': current['humidity'],
                'clouds':   current['clouds'],
                'visibility': current['visibility'],
                'wind_speed': current['wind_speed'],
                'wind_deg': current['wind_deg'],
                'sunrise': current['sunrise'],
                'sunset': current['sunset'],
                'weather_id': weather['id'],
                'weather_main': weather['main'],
                'weather_description': weather['description'],
                'weather_icon': weather['icon'],
                'dt': current['dt'],
                
            })     
           
    
    
   
    
    
    def conver_data(self, data):
        result = data.copy()
        print('result: ', result)
        current = result['current']
        
        current['dt'] = self.unix2datetime(current['dt'])
        current['sunrise'] = self.unix2datetime(current['sunrise'])
        current['sunset'] = self.unix2datetime(current['sunset'])
        
        current['temp'] = round(current['temp'])
        current['feels_like'] = round(current['feels_like'])
        current['pressure'] = round(current['pressure'])
        current['humidity'] = round(current['humidity'])
        current['clouds'] = round(current['clouds'])
        current['visibility'] = round(current['visibility'])
        current['wind_speed'] = round(current['wind_speed'], 2)
        current['wind_deg'] = round(current['wind_deg'])
        
        return result
        
        
        
    def unix2datetime(self, unixtime):
        return datetime.utcfromtimestamp(unixtime)    
    
    
    def unlink(self):
        # self.update_data_weather_city()
        # self.test1()
        # print('unlink', self.env.context)
        self.update_data_weather()





