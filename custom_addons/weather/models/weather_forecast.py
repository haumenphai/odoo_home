
from odoo import models, fields, api

from urllib.request import urlopen
import json, time
from dateutil import tz

from datetime import datetime


def unix2datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime)

def convertime(datetime, str_tz, format):
    to_zone = tz.gettz(str_tz)
    timel = datetime.astimezone(to_zone)
    result = timel.strftime(format)
    
    return result

  
apikey1 = '3e65cba6de46a1e4074e68215ed5938a'
apikey2 = 'dfc2d4e0b00c6903afcfdfcc3b059752'

class WeatherForecast(models.Model):
    _name = 'weather.forecast'
    _description = ''
    _inherit = 'weather.api'


    name = fields.Char(string='Tỉnh/Thành phố')
    lat = fields.Float(string='Kinh độ')
    lon = fields.Float(string='Vĩ độ')     
    
    temp = fields.Char(string='Nhiệt độ')
    feels_like = fields.Char(string='Cảm nhận')
    humidity = fields.Char(string='Độ ẩm')
    pressure = fields.Char('Áp suất')
    
    clouds = fields.Char('Mây')
    
    visibility = fields.Char('Tầm nhìn')
    wind_speed = fields.Char('Tốc độ gió')
    wind_deg = fields.Char('Hướng gió')
    
    sunrise = fields.Datetime()
    sunset = fields.Datetime()
    sunrise_show = fields.Char('Bình minh')
    sunset_show = fields.Char('Hoàng hôn')
    
    
    timezone = fields.Char()
    dt = fields.Datetime(string='Cập nhật lúc')
    current_pop = fields.Char('Xác xuất mưa')
    
    weather_id = fields.Char()
    weather_main = fields.Char()
    weather_description = fields.Char()
    weather_icon = fields.Char()

    
    url_icon = fields.Char(compute='_get_url_icon')
    hourly_ids = fields.Many2many('weather.hourly')
    daily_ids = fields.Many2many('weather.daily')
    
    
    @api.depends('weather_icon')
    def _get_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'
    
    
    def update_data_weather(self):
        i = 0
        cities = self.search([])
        
        for city in cities:
            i += 1
            if i % 2 == 0:     
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, units='metric', apikey=apikey1, lang='vi')
            else:
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, units='metric', apikey=apikey2, lang='vi')
            
            data = self._convert_data(data)
                
            current = data['current']
            weather = data['current']['weather'][0]
              
            city.write({
                'temp':  current['temp'],
                'feels_like': current['feels_like'],
                'humidity': current['humidity'],
                'pressure': current['pressure'],
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
                'current_pop': data['current_pop'],
                'timezone': data['timezone'],
                'sunset_show': data['sunset_show'],
                'sunrise_show': data['sunrise_show']
                
            })

            j = 0
            hour_list = data['hourly']
            day_list = data['daily']

            # length hourly_ids = 6.
            for hour in city.hourly_ids:
                hour.update_hourly(hour_list[j], data['timezone'])
                j += 1
            
            j = 0
            for day in city.daily_ids:
                day.update_data_daily(day_list[j], data['timezone'])
                j += 1

            
            if i == 3: break
        self.set_act_window_label(f"Thời tiết hiện tại cập nhật lúc: {convertime(cities[0].dt, cities[0].timezone, '%H:%M')}")

    def _convert_data(self, data):
        result = data.copy()
        print('result: ', result)
        current = result['current']
        
        current['dt'] = unix2datetime(current['dt'])
        current['sunrise'] = unix2datetime(current['sunrise'])
        current['sunset'] = unix2datetime(current['sunset'])
        
        current['temp'] = f"{round(current['temp'])} ºC"
        current['feels_like'] = f"{round(current['feels_like'])} ºC"
        current['pressure'] = f"{round(current['pressure'])} hPa"
        
        current['humidity'] = f"{round(current['humidity'])} %"
        current['clouds'] = f"{round(current['clouds'])} %"
        current['visibility'] = f"{round(current['visibility'])} m"
        current['wind_speed'] = f"{round(current['wind_speed'], 2)} m/s"
        current['wind_deg'] = f"{round(current['wind_deg'])} º"
        
      
        pop = f"{int(result['hourly'][0]['pop'] * 100)} %"
        result['current_pop'] = pop
        
        result['sunset_show'] = convertime(current['sunset'], data['timezone'], '%H:%M')
        result['sunrise_show'] = convertime(current['sunset'], data['timezone'], '%H:%M')
        
        return result
    
    
    def set_act_window_label(self, label):
        act_window = self.env.ref('weather.weather_city_act')
        act_window.name = label
        
        
    
    @api.model 
    def set_forecast_to_tomorrow(self):
        self.set_act_window_label('Đang xem thời tiết ngày mai')
        self._update_data_tomorrow()
        
        print('set to tomorrow')
    
    
    def _update_data_tomorrow(self):
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree'
        
        
    
    @api.model
    def set_forecast_to_current(self):
        self.set_act_window_label('Thời tiết hôm nay')
        self._update_data_current()
        
        print('set to tomorow')
        
    def _update_data_current(self):
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree,form,kanban'

    
    
    
    def unlink(self):
        self.update_data_weather()
