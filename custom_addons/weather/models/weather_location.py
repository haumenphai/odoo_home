from odoo import fields, models, api


class WeatherLocation(models.Model):
    _name = 'weather.location'
    _description = 'Weather Location Forecast, user can edit'
    # _rec_name = 'location_name'

    weather_forecast_id = fields.Many2one('weather.forecast')

    temp = fields.Char(related='weather_forecast_id.temp')
    humidity = fields.Char(related='weather_forecast_id.humidity')
    clouds = fields.Char(related='weather_forecast_id.clouds')
    pop = fields.Char(related='weather_forecast_id.pop')

    field_location_seach = fields.Char()

    city_id = fields.Many2one('weather.city')
    location_name = fields.Char(related='city_id.name')

    def update_weather(self):
        print('update weather location for user')

    def search_loaction(self):
        print(self.field_location_seach)
        self.field_location_seach = ''


