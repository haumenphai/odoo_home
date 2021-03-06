from dateutil import tz
from odoo import models, fields, api

from ..tools import time_util


class WeatherDaily(models.Model):
    _name = 'weather.daily'
    _description = 'Daily forecast'
    _inherit = ['weather.weather']
    _rec_name = 'dt'

    sunrise_show = fields.Char(string='Sunrise', readonly=True)
    sunset_show = fields.Char(string='Sunset', readonly=True)
    moonrise_show = fields.Char(string='Moonrise', readonly=True)
    moonset_show = fields.Char(string='Moonset', readonly=True)
    time_show = fields.Char(string='Day', compute='_compute_time_show')
    timezone = fields.Char(string='Timezone', readonly=True)

    temp_min = fields.Char(string='Temp Min', readonly=True)
    temp_max = fields.Char(string='Temp Max', readonly=True)
    temp_night = fields.Char(string='Temp Night', readonly=True)
    temp_eve = fields.Char(string='Temp Evening', readonly=True)
    temp_morning = fields.Char(string='Temp Morning', readonly=True)

    feels_like_day = fields.Char(string='Feels Like', readonly=True)
    feels_like_night = fields.Char(string='Feels Like Night', readonly=True)
    feels_like_eve = fields.Char(string='Feels Like Evening', readonly=True)
    feels_like_morning = fields.Char(string='Feels Like Morning', readonly=True)

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
            if r.timezone and r.dt:
                to_zone = tz.gettz(r.timezone)
                utc = fields.Datetime.to_datetime(r.dt)
                timel = utc.astimezone(to_zone)
                r.time_show = timel.strftime('%d/%m')  # %a: week
            else:
                r.time_show = 'null'


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
            'moonset_show': data['moonset_show'],
            'pop_int': data['pop_int'],
            'humidity_int': data['humidity_int'],
            'clouds_int': data['clouds_int'],
            'pressure_int': data['pressure_int']
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
        temp['min'] = f"{round(temp['min'])} ??C"
        temp['max'] = f"{round(temp['max'])} ??C"
        temp['night'] = f"{round(temp['night'])} ??C"
        temp['eve'] = f"{round(temp['eve'])} ??C"
        temp['morn'] = f"{round(temp['morn'])} ??C"

        feels_like = r['feels_like']
        feels_like['day'] = f"{round(feels_like['day'])} ??C"
        feels_like['night'] = f"{round(feels_like['night'])} ??C"
        feels_like['eve'] = f"{round(feels_like['eve'])} ??C"
        feels_like['morn'] = f"{round(feels_like['morn'])} ??C"

        r['pressure'] = f"{r['pressure']} hPa"
        r['humidity'] = f"{round(r['humidity'])} %"
        r['wind_speed'] = f"{round(r['wind_speed'], 2)} m/s"
        r['wind_deg'] = f"{r['wind_deg']} ??"
        r['clouds'] = f"{round(r['clouds'])} %"
        r['pop'] = f"{int(r['pop'] * 100)} %"

        r['pop_int'] = int(r['pop'][0:len(r['pop']) - 2])
        r['humidity_int'] = int(r['humidity'][0:len(r['humidity']) - 2])
        r['clouds_int'] = round(data_day['clouds'])
        r['pressure_int'] = round(data_day['pressure'])
        return r
