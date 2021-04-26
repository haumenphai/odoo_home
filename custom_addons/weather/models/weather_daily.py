from dateutil import tz
from odoo import models, fields, api

from ..tools import time_util


class WeatherDaily(models.Model):
    _name = 'weather.daily'
    _description = 'Daily forecast'
    _inherit = ['weather.weather']
    _rec_name = 'dt'

    sunrise_show = fields.Char(string='Sunrise')
    sunset_show = fields.Char(string='Sunset')
    moonrise_show = fields.Char(string='Moonrise')
    moonset_show = fields.Char(string='Moonset')
    time_show = fields.Char(string='Day', compute='_compute_time_show')
    timezone = fields.Char(string='Timezone')

    temp_min = fields.Char(string='Temp Min')
    temp_max = fields.Char(string='Temp Max')
    temp_night = fields.Char(string='Temp Night')
    temp_eve = fields.Char(string='Temp Evening')
    temp_morning = fields.Char(string='Temp Morning')

    feels_like_day = fields.Char(string='Feels Like')
    feels_like_night = fields.Char(string='Feels Like Night')
    feels_like_eve = fields.Char(string='Feels Like Evening')
    feels_like_morning = fields.Char(string='Feels Like Morning')
    uvi = fields.Char(string='Uvi')

    def get_data_one_day(self):
        return {
            'temp': self.temp,
            'humidity': self.humidity,
            'clouds': self.clouds,
            'pop': self.pop,
            'visibility': 'Null',
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'weather_description': self.weather_description,
            'pressure': self.pressure,
            'sunset_show': self.sunset_show,
            'sunrise_show': self.sunrise_show
        }

    @api.depends('dt')
    def _compute_time_show(self):
        for r in self:
            to_zone = tz.gettz(r.timezone)
            utc = fields.Datetime.to_datetime(r.dt)
            timel = utc.astimezone(to_zone)
            r.time_show = timel.strftime('%d/%m')  # %a: week

    @api.depends('weather_icon')
    def _get_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'

    def update_data_daily(self, data_day, timezone):
        data = self._convert_data(data_day, timezone)
        weather = data['weather'][0]
        self.write({
            'dt': data['dt'],
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

        r['dt'] = time_util.unix2datetime(r['dt'])
        sunrise = time_util.unix2datetime(r['sunrise'])
        sunset = time_util.unix2datetime(r['sunset'])
        moonrise = time_util.unix2datetime(r['moonrise'])
        moonset = time_util.unix2datetime(r['moonset'])

        r['sunrise_show'] = time_util.convert_datetime(sunrise, tz).strftime('%H:%M')
        r['sunset_show'] = time_util.convert_datetime(sunset, tz).strftime('%H:%M')
        r['moonrise_show'] = time_util.convert_datetime(moonrise, tz).strftime('%H:%M')
        r['moonset_show'] = time_util.convert_datetime(moonset, tz).strftime('%H:%M')

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
        r['wind_speed'] = f"{round(r['wind_speed'], 2)} m/s"
        r['wind_deg'] = f"{r['wind_deg']} º"
        r['clouds'] = f"{round(r['clouds'])} %"
        r['pop'] = f"{int(r['pop'] * 100)} %"
        return r
