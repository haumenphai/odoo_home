import json

from odoo import models, fields, api

from ..tools import time_util


apikey1 = '3e65cba6de46a1e4074e68215ed5938a'
apikey2 = 'dfc2d4e0b00c6903afcfdfcc3b059752'


class WeatherForecast(models.Model):
    _name = 'weather.forecast'
    _description = ''
    _inherit = ['weather.api', 'weather.weather']

    name = fields.Char('Location')
    lat = fields.Float()
    lon = fields.Float()

    dt = fields.Datetime('Updated at')
    visibility = fields.Char()
    sunrise_show = fields.Char('Sunrise')
    sunset_show = fields.Char('Sunset')
    timezone = fields.Char()
    hourly_ids = fields.Many2many('weather.hourly')
    daily_ids = fields.Many2many('weather.daily')
    current_json = fields.Text()

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    @api.depends('weather_icon')
    def _compute_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'
        print(time_util)

    @api.model
    def update_data_weather(self):
        """ Update weather for all location
            :return: None
        """
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

            if i == 3: break  # todo: delete
        self._save_current_weather(cities)
        self._set_act_window_label(f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")
        return self._reload_page(f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")

    def _convert_data(self, data):
        """ Converts the value of the dict (data) to a displayable format
            :param data: dict contains json weather forecast
            :return dict: (result) contains the converted values
        """
        result = data.copy()
        print('result: ', result)
        current = result['current']
        current['dt'] = time_util.unix2datetime(current['dt'])
        current['temp'] = f"{round(current['temp'])} ºC"
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
        return result

    def _save_current_weather(self, cities):
        """ Save current weather data so you can go back to current weather information when switching to tomorrow
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
        i = 0  # todo: delete
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree'
        cities = self.search([])

        for city in cities:
            i += 1  # todo delete
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
            if i == 3: break  # todo delete
        print('set to tomorrow')
        self._set_act_window_label("Tomorrow's weather")
        return self._reload_page("Tomorrow's weather", "tree")

    def set_forecast_to_current(self):
        """ Convert the time data currently displayed in the tree view to the current weather
        """
        cities = self.search([])
        act_window = self.env.ref('weather.weather_city_act')
        act_window.view_mode = 'tree,form,kanban'

        i = 0  # todo delete
        for city in cities:
            i += 1  # todo delete
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

            if i == 3: break  # todo delete
        print('set to Current weather')
        self._set_act_window_label(f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")
        return self._reload_page(f"Current weather updated at: {time_util.convert_datetime(cities[0].dt, cities[0].timezone).strftime('%H:%M')}")

    def _reload_page(self, name, view_mode='tree,form,kanban'):
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
        act_window = self.env.ref('weather.weather_city_act')
        act_window.name = label

    def display_temp_C(self):
        print('display temp C')
        cities = self.search([])
        for r in cities:
            if r.temp:
                if 'C' in str(r.temp): return
                tempF = f'{r.temp}'
                tempF = float(tempF[0:tempF.find(' ')])
                tempC = f'{round((tempF - 32) / 1.8)} °C'
                r.temp = tempC
        return self._reload_page(self.env.ref('weather.weather_city_act').name + ' (Temp C)')

    def display_temp_F(self):
        print('display temp F')
        cities = self.search([])
        for r in cities:
            if r.temp:
                if 'F' in str(r.temp): return
                tempC = f'{r.temp}'
                tempC = int(tempC[0:tempC.find(' ')])
                tempF = f'{(tempC * 9 / 5 + 32)} °F'
                r.temp = tempF
        return self._reload_page(self.env.ref('weather.weather_city_act').name + ' (Temp F)')
