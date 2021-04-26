from odoo import api, models, fields


class Weather(models.AbstractModel):
    _name = 'weather.weather'
    _description = 'Abstract Weather'

    dt = fields.Datetime(string='Update at')
    temp = fields.Char(string='Temp')
    temp_int = fields.Integer(string='Temp int')
    temp_float = fields.Float(string='Temp Float')
    feels_like = fields.Char(string='Feels Like')
    pop = fields.Char(string='Pop')
    humidity = fields.Char(string='Humidity')
    pressure = fields.Char(string='Pressure')
    clouds = fields.Char(string='Clouds')
    wind_speed = fields.Char(string='Wind Speed')
    wind_deg = fields.Char(string='Wind Deg')
    uvi = fields.Char(string='Uvi')

    url_icon = fields.Char(compute='_compute_url_icon', string='URL weather icon')
    weather_main = fields.Char(string='Weather Main')
    weather_description = fields.Char(string='Weather Description')
    weather_icon = fields.Char(string='Weather Icon Code')


    @api.depends('weather_icon')
    def _compute_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'