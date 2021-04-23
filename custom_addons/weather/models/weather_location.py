from odoo import fields, models, api


class WeatherLocation(models.Model):
    _name = 'weather.location'
    _description = 'Weather Location Forecast, user can edit'

    name = fields.Char('Location')
    lat = fields.Float()
    lon = fields.Float()

    weather_forecast_id = fields.Many2one('weather.forecast')
    temp = fields.Char(related='weather_forecast_id.temp')
    humidity = fields.Char(related='weather_forecast_id.humidity')
    clouds = fields.Char(related='weather_forecast_id.clouds')
    pop = fields.Char(related='weather_forecast_id.pop')

    field_location_seach = fields.Char()

    def update_weather(self):
        print('update weather location for user')

    def search_loaction(self):
        print(self.field_location_seach)
        self.field_location_seach = ''


