import json
from dateutil import tz

from odoo import models, fields, api

from ..tools import time_util

apikey1 = '3e65cba6de46a1e4074e68215ed5938a'
apikey2 = 'dfc2d4e0b00c6903afcfdfcc3b059752'


class WeatherForecast(models.Model):
    _name = 'weather.forecast'
    _description = 'Current Forecast'
    _inherit = ['weather.api', 'weather.weather']

    name = fields.Char(string='Location', required=True)
    lat = fields.Float(string='Latitude', required=True)
    lon = fields.Float(string='Longitude', required=True)

    dt_show = fields.Char(string='Update at', readonly=True, compute='_compute_dt_show')
    visibility = fields.Char(string='Visibility', readonly=True)
    sunrise_show = fields.Char(string='Sunrise', readonly=True)
    sunset_show = fields.Char(string='Sunset', readonly=True)
    timezone = fields.Char(string='Timezone', readonly=True)
    hourly_ids = fields.Many2many('weather.hourly', string='Hourly Forecast', readonly=True)
    daily_ids = fields.Many2many('weather.daily', string='Daily Forecast', readonly=True)
    current_json = fields.Text(string='Current Json', readonly=True)

    @api.depends('dt')
    def _compute_dt_show(self):
        for r in self:
            if r.timezone and r.dt:
                to_zone = tz.gettz(r.timezone)
                time = r.dt.astimezone(to_zone)
                r.dt_show = time.strftime(f'%m/%d/%Y %H:%M:%S - Timezone: {r.timezone}')
            else:
                r.dt_show = 'null'


    @api.model
    def update_data_weather(self):
        """ Update weather for all location
            :return: None
        """
        self = self.sudo(True)
        i = 0
        cities = self.search([])
        for city in cities:
            i += 1
            if i % 2 == 0:
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, apikey=apikey1)
            else:
                data = self.get_data_weather_onecall(lat=city.lat, lon=city.lon, apikey=apikey2)
            data = self._convert_data(data)

            current = data['current']
            weather = data['current']['weather'][0]
            city.write({
                'temp': current['temp'],
                'feels_like': current['feels_like'],
                'humidity': current['humidity'],
                'pressure': current['pressure'],
                'clouds': current['clouds'],
                'visibility': current['visibility'],
                'wind_speed': current['wind_speed'],
                'wind_deg': current['wind_deg'],
                'weather_main': weather['main'],
                'weather_description': weather['description'],
                'weather_icon': weather['icon'],
                'dt': current['dt'],
                'pop': data['pop'],
                'timezone': data['timezone'],
                'sunset_show': data['sunset_show'],
                'sunrise_show': data['sunrise_show'],
                'pop_int': data['pop_int'],
                'humidity_int': data['humidity_int'],
                'clouds_int': data['clouds_int'],
                'pressure_int': data['pressure_int']
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
        self._save_current_weather(cities)
        self._set_act_window_label(
            f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")
        return self._reload_page(
            f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")

    def _convert_data(self, data):
        """ Converts the value of the dict (data) to a displayable format
            :param data: dict contains json weather forecast
            :return dict: (result) contains the converted values
        """
        result = data.copy()
        result['humidity_int'] = round(data['current']['humidity'])
        result['clouds_int'] = round(data['current']['clouds'])
        result['pressure_int'] = round(data['current']['pressure'])

        print('result: ', result)
        current = result['current']
        current['dt'] = time_util.unix2datetime(current['dt'])
        current['feels_like'] = f"{round(current['feels_like'])} ºC"
        current['pressure'] = f"{round(current['pressure'])} hPa"
        current['humidity'] = f"{round(current['humidity'])} %"
        current['clouds'] = f"{round(current['clouds'])} %"
        current['visibility'] = f"{round(current['visibility'])} m"
        current['wind_speed'] = f"{round(current['wind_speed'], 2)} m/s"
        current['wind_deg'] = f"{round(current['wind_deg'])} º"
        result['pop'] = f"{int(result['hourly'][0]['pop'] * 100)} %"
        sunrise = time_util.unix2datetime(current['sunrise'])
        sunset = time_util.unix2datetime(current['sunset'])
        result['sunset_show'] = time_util.convert_datetime(sunrise, data['timezone']).strftime('%H:%M')
        result['sunrise_show'] = time_util.convert_datetime(sunset, data['timezone']).strftime('%H:%M')
        result['pop_int'] = int(result['pop'][0:len(result['pop'])-2])
        return result

    def _save_current_weather(self, cities):
        """ Save current weather data so you can go back to current weather information when switching to tomorrow on tree view
            :param cities: all record of weather.forecast
        """
        for city in cities:
            current_weather = {
                'temp': city.temp,
                'humidity': city.humidity,
                'clouds': city.clouds,
                'pop': city.pop,
                'visibility': city.visibility,
                'wind_speed': city.wind_speed,
                'wind_deg': city.wind_deg,
                'weather_description': city.weather_description,
                'pressure': city.pressure,
                'sunset_show': city.sunset_show,
                'sunrise_show': city.sunrise_show
            }
            city.current_json = str(current_weather).replace("'", '"')

    def set_forecast_to_tomorrow(self):
        """ Convert the weather data currently displayed in the tree view to tomorrow's weather
        """
        self = self.sudo(True)
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree'
        cities = self.search([])
        for city in cities:
            data_tomorrow = city.daily_ids[1].get_data_one_day()
            city['temp'] = data_tomorrow['temp']
            city['humidity'] = data_tomorrow['humidity']
            city['clouds'] = data_tomorrow['clouds']
            city['pop'] = data_tomorrow['pop']
            city['visibility'] = 'Null'
            city['wind_speed'] = data_tomorrow['wind_speed']
            city['wind_deg'] = data_tomorrow['wind_deg']
            city['weather_description'] = data_tomorrow['weather_description']
            city['pressure'] = data_tomorrow['pressure']
            city['sunset_show'] = data_tomorrow['sunset_show']  # co the khong can thiet
            city['sunrise_show'] = data_tomorrow['sunrise_show']  # co the khong can thiet
        print('set to tomorrow')  # todo delete
        self._set_act_window_label("Tomorrow's weather")
        return self._reload_page("Tomorrow's weather", "tree")

    def set_forecast_to_current(self):
        """ Convert the time data currently displayed in the tree view to the current weather
        """
        self = self.sudo(True)
        cities = self.search([])
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree,form,kanban'
        for city in cities:
            data = json.loads(city.current_json)
            city['temp'] = data['temp']
            city['humidity'] = data['humidity']
            city['clouds'] = data['clouds']
            city['pop'] = data['pop']
            city['visibility'] = data['visibility']
            city['wind_speed'] = data['wind_speed']
            city['wind_deg'] = data['wind_deg']
            city['weather_description'] = data['weather_description']
            city['pressure'] = data['pressure']
            city['sunset_show'] = data['sunset_show']  # co the khong can thiet vì nó không hiển thị trên tree view
            city['sunrise_show'] = data['sunrise_show']  #
        print('set to Current weather')  # todo delete
        self._set_act_window_label(
            f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")
        return self._reload_page(
            f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")

    def _reload_page(self, name, view_mode='tree,form,kanban,graph'):
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_mode': view_mode,
            'res_model': 'weather.forecast',
            'target': 'current'
        }

    def _set_act_window_label(self, label):
        """ Set name for Window Action: weather forecast
        """
        sudo = self.sudo(True)
        act_window = sudo.env.ref('weather.weather_city_act')
        act_window.name = label

    def display_temp_C(self):
        print('display temp C')
        cities = self.search([])
        for city in cities:
            if city.temp:
                city.set_temp_C()
            for hour in city.hourly_ids:
                hour.set_temp_C()
            for day in city.daily_ids:
                day.set_temp_C()
        return self._reload_page(self.env.ref('weather.weather_city_act').name + ' (Temp C)')

    def display_temp_F(self):
        print('display temp F')
        cities = self.search([])
        for city in cities:
            if city.temp:
                city.set_temp_F()
            for hour in city.hourly_ids:
                hour.set_temp_F()
            for day in city.daily_ids:
                day.set_temp_F()
        return self._reload_page(self.env.ref('weather.weather_city_act').name + ' (Temp F)')
