
from odoo import models, fields, api

from urllib.request import urlopen
import json, time
from datetime import datetime

def unix2datetime(unixtime):
    return datetime.utcfromtimestamp(unixtime)



  
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
    
    sunrise = fields.Datetime('Bình minh')
    sunset = fields.Datetime('Hoàng hôn')
    
    dt = fields.Datetime(string='Cập nhật lúc')
    current_pop = fields.Char('Xác xuất mưa')
    
    weather_id = fields.Char()
    weather_main = fields.Char()
    weather_description = fields.Char()
    weather_icon = fields.Char()

    
    
    #==========================================================================
    @api.depends('weather_icon')
    def _get_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'
    
    url_icon = fields.Char(compute=_get_url_icon)
    hourly_ids = fields.Many2many('weather.hourly')
    
    
    def update_data_weather(self):
        # self.env['weather.hourly'].search([]).unlink()
        i = 0
        cities = self.search([])
        
        for city in cities:
            i += 1
            if i % 2 == 0:     
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, units='metric', apikey=apikey1, lang='vi')
            else:
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, units='metric', apikey=apikey2, lang='vi')
            
            data = self._conver_data(data)
                
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
                'current_pop': data['current_pop']
            })

            j = 0
            hour_list = data['hourly']
            # print('ids', self.hourly_ids)

            # length hourly_ids = 6.
            for hour in self.hourly_ids:
                hour.update_hourly(hour_list[j])

                # hour.write({
                #     'temp': hour_list[j]['temp']
                # })
                j += 1
                print(hour.temp)
                # print(hour.conver_data(hour_list[j]))

            if i == 3: break
            # self._update_hourly(data['hourly'])


    def _conver_data(self, data):
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
        
        return result
        
        
        
       
    
    
    def unlink(self):
        self.update_data_weather()
        # print(self.hourly_ids)
