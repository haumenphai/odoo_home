import json, time
from datetime import datetime
from dateutil import tz

from odoo import models, fields, api

def unix2datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime)

def convertime(datetime, str_tz, format):
    to_zone = tz.gettz(str_tz)
    timel = datetime.astimezone(to_zone)
    result = timel.strftime(format)
    
    return result


class WeatherDaily(models.Model):
    _name = 'weather.daily'
    _description = 'weather daily'
    _rec_name = 'time'
    
    time = fields.Datetime('dt')
    temp = fields.Char('Nhiệt độ') #temp day
    pop = fields.Char('Xác suất mưa')
    humidity = fields.Char('Độ ẩm')
    clouds = fields.Char('Mây')
    wind_speed = fields.Char('Tốc độ gió')
    wind_deg = fields.Char('Hướng gió')
    pressure = fields.Char('Áp suất')

    weather_main = fields.Char()
    weather_description = fields.Char('Miêu tả')
    weather_icon = fields.Char()
    url_icon = fields.Char(compute='_get_url_icon')
    
    sunrise = fields.Datetime()
    sunset = fields.Datetime()
    moonrise = fields.Datetime()
    moonset = fields.Datetime()
    
    sunrise_show = fields.Char('Bình minh')
    sunset_show = fields.Char('Hoàng hôn')
    moonrise_show = fields.Char('Trăng mọc')
    moonset_show = fields.Char('Trăng lặn')
    time_show = fields.Char('Ngày', compute='_compute_time_show')
    timezone = fields.Char()
    
    temp_min = fields.Char()
    temp_max = fields.Char()
    temp_night = fields.Char()
    temp_eve = fields.Char()
    temp_morning = fields.Char()
    
    feels_like_day = fields.Char('Cảm nhận')
    feels_like_night = fields.Char()
    feels_like_eve = fields.Char()
    feels_like_morning = fields.Char()
    uvi = fields.Char()
    
    
    
    def get_data_one_day(self):
        """
            self: one
        """
        r = {}
        r['temp'] = self.temp
        r['humidity'] = self.humidity
        r['clouds'] = self.clouds
        r['pop'] = self.pop
        r['visibility'] = 'Null'
        r['wind_speed'] = self.wind_speed
        r['wind_deg'] = self.wind_deg
        r['weather_description'] = self.weather_description
        r['pressure'] = self.pressure
        r['sunset_show'] = self.sunset_show
        r['sunrise_show'] = self.sunrise_show
        
        return r
    
    
    @api.depends('time')
    def _compute_time_show(self):
        for r in self:
            to_zone = tz.gettz(r.timezone)
            utc = fields.Datetime.to_datetime(r.time)
            timel = utc.astimezone(to_zone)
            r.time_show = timel.strftime('%d/%m') # %a: week 
            
    
    @api.depends('weather_icon')
    def _get_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'

    
    def update_data_daily(self, data_day, timezone):
        data = self._convert_data(data_day, timezone)
        
        weather = data['weather'][0]
        self.write({
            'time': data['dt'],
            'temp': data['temp']['day'],
            'pop': data['pop'],
            'humidity': data['humidity'],
            'clouds': data['humidity'],
            'wind_speed': data['wind_speed'],
            'wind_deg': data['wind_deg'],
            'pressure': data['pressure'],
            'weather_main': weather['main'],
            'weather_description': weather['description'],
            'weather_icon': weather['icon'],
            'sunrise': data['sunrise'],
            'sunset': data['sunset'],
            'moonrise': data['moonrise'],
            'moonset': data['moonset'],
            'temp_min': data['temp']['min'],
            'temp_max': data['temp']['max'],
            'temp_night': data['temp']['night'],
            'temp_eve': data['temp']['eve'],
            'temp_morning': data['temp']['morn'],
            'feels_like_day': data['feels_like']['day'],
            'feels_like_night': data['feels_like']['night'],
            'feels_like_eve': data['feels_like']['eve'],
            'feels_like_morning': data['feels_like']['morn'],
            'uvi': data['uvi'],
            'timezone': timezone,
            'sunrise_show': data['sunrise_show'], 
            'sunset_show': data['sunset_show'], 
            'moonrise_show': data['moonrise_show'], 
            'moonset_show': data['moonset_show']
        })

    
    def _convert_data(self, data_day, tz):
        r = data_day.copy()
        
        r['dt'] = unix2datetime(r['dt'])
        r['sunrise'] = unix2datetime(r['sunrise'])
        r['sunset'] = unix2datetime(r['sunset'])
        r['moonrise'] = unix2datetime(r['moonrise'])
        r['moonset'] = unix2datetime(r['moonset'])
        
        temp = r['temp']
        temp['day'] = f"{round(temp['day'])} ºC"
        temp['min'] = f"{round(temp['min'])} ºC"
        temp['max'] = f"{round(temp['max'])} ºC"
        temp['night'] = f"{round(temp['night'])} ºC"
        temp['eve'] = f"{round(temp['eve'])} ºC"
        temp['morn'] = f"{round(temp['morn'])} ºC"

        feels_like = r['feels_like']
        feels_like['day'] = f"{round(feels_like['day'])} ºC"
        feels_like['night'] = f"{round(feels_like['night'])} ºC"
        feels_like['eve'] = f"{round(feels_like['eve'])} ºC"
        feels_like['morn'] = f"{round(feels_like['morn'])} ºC"
        
        r['pressure'] = f"{r['pressure']} hPa"
        r['humidity'] = f"{round(r['humidity'])} %"
        r['wind_speed'] = f"{round(r['wind_speed'],2)} m/s"
        r['wind_deg'] = f"{r['wind_deg']} º"
        r['clouds'] = f"{round(r['clouds'])} %"
        r['pop'] = f"{int(r['pop'] * 100)} %"
        
        
        r['sunrise_show'] = convertime(r['sunrise'], tz, '%H:%M')
        r['sunset_show'] = convertime(r['sunset'], tz, '%H:%M')
        r['moonrise_show'] = convertime(r['moonrise'], tz, '%H:%M')
        r['moonset_show'] = convertime(r['moonset'], tz, '%H:%M')
        
        return r

    