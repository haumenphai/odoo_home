from dateutil import tz
from ..tools import time_util

from odoo import models, fields, api

# ToDo: refactor
class WeatherDaily(models.Model):
    _name = 'weather.daily'
    _description = 'weather daily'
    _rec_name = 'time'

    time = fields.Datetime('dt')
    temp = fields.Char()  # temp day
    pop = fields.Char()
    humidity = fields.Char()
    clouds = fields.Char()
    wind_speed = fields.Char()
    wind_deg = fields.Char()
    pressure = fields.Char()

    weather_main = fields.Char()
    weather_description = fields.Char()
    weather_icon = fields.Char()
    url_icon = fields.Char(compute='_get_url_icon')

    sunrise = fields.Datetime()
    sunset = fields.Datetime()
    moonrise = fields.Datetime()
    moonset = fields.Datetime()

    sunrise_show = fields.Char('Sunrise')
    sunset_show = fields.Char('Sunset')
    moonrise_show = fields.Char('Moonrise')
    moonset_show = fields.Char('Moonset')
    time_show = fields.Char('Day', compute='_compute_time_show')
    timezone = fields.Char()

    temp_min = fields.Char()
    temp_max = fields.Char()
    temp_night = fields.Char()
    temp_eve = fields.Char()
    temp_morning = fields.Char()

    feels_like_day = fields.Char('Feels Like')
    feels_like_night = fields.Char()
    feels_like_eve = fields.Char()
    feels_like_morning = fields.Char()
    uvi = fields.Char()

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

    @api.depends('time')
    def _compute_time_show(self):
        for r in self:
            to_zone = tz.gettz(r.timezone)
            utc = fields.Datetime.to_datetime(r.time)
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

        r['dt'] = time_util.unix2datetime(r['dt'])
        r['sunrise'] = time_util.unix2datetime(r['sunrise'])
        r['sunset'] = time_util.unix2datetime(r['sunset'])
        r['moonrise'] = time_util.unix2datetime(r['moonrise'])
        r['moonset'] = time_util.unix2datetime(r['moonset'])

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

        r['sunrise_show'] = time_util.convert_datetime(r['sunrise'], tz).strftime('%H:%M')
        r['sunset_show'] = time_util.convert_datetime(r['sunset'], tz).strftime('%H:%M')
        r['moonrise_show'] = time_util.convert_datetime(r['moonrise'], tz).strftime('%H:%M')
        r['moonset_show'] = time_util.convert_datetime(r['moonset'], tz).strftime('%H:%M')

        return r
