from dateutil import tz
from ..tools import time_util
from odoo import models, fields, api


class WeatherHourly(models.Model):
    _name = 'weather.hourly'
    _inherit = ['weather.weather']
    _description = 'Hourly Forecast'

    time_show = fields.Char(string='Hour', compute='_compute_time_show', readonly=True)
    timezone = fields.Char(string='Timezone', readonly=True)

    @api.depends('dt')
    def _compute_time_show(self):
        for r in self:
            if r.timezone and r.dt:
                to_zone = tz.gettz(r.timezone)
                time = r.dt.astimezone(to_zone)
                r.time_show = time.strftime('%H:%M:%S')
            else:
                r.time_show = 'null'

    def _convert_data(self, data):
        result = data.copy()
        result['dt'] = time_util.unix2datetime(result['dt'])
        result['feels_like'] = f"{round(result['feels_like'])} ºC"
        result['pressure'] = f"{round(result['pressure'])} hPa"
        result['humidity'] = f"{round(result['humidity'])} %"
        result['clouds'] = f"{round(result['clouds'])} %"
        result['visibility'] = f"{round(result['visibility'])} m"
        result['wind_speed'] = f"{round(result['wind_speed'], 2)} m/s"
        result['wind_deg'] = f"{round(result['wind_deg'])} º"
        result['pop'] = f"{round(result['pop'] * 100)} %"
        result['uvi'] = f"{result['uvi']}"
        return result

    def update_hourly(self, data, timezone):
        self.ensure_one()
        data1 = self._convert_data(data)
        self.write({
            'dt': data1['dt'],
            'temp': data1['temp'],
            'feels_like': data1['feels_like'],
            'pop': data1['pop'],
            'humidity': data1['humidity'],
            'clouds': data1['clouds'],
            'wind_speed': data1['wind_speed'],
            'wind_deg': data1['wind_deg'],
            'weather_description': data1['weather'][0]['description'],
            'weather_main': data1['weather'][0]['main'],
            'weather_icon': data1['weather'][0]['icon'],
            'timezone': timezone,
            'pressure': data1['pressure'],
            'uvi': data1['uvi']
        })
