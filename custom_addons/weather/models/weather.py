from odoo import api, models, fields


class Weather(models.AbstractModel):
    _name = 'weather.weather'
    _description = ''

    dt = fields.Datetime()
    temp = fields.Char()
    feels_like = fields.Char()
    pop = fields.Char()
    humidity = fields.Char()
    pressure = fields.Char()
    clouds = fields.Char()
    wind_speed = fields.Char()
    wind_deg = fields.Char()
    uvi = fields.Char()

    url_icon = fields.Char(compute='_compute_url_icon')
    weather_main = fields.Char()
    weather_description = fields.Char()
    weather_icon = fields.Char()


    @api.depends('weather_icon')
    def _compute_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'