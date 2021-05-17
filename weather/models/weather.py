from odoo import api, models, fields


class Weather(models.AbstractModel):
    _name = 'weather.weather'
    _description = 'Abstract Weather'

    dt = fields.Datetime(string='Update at', readonly=True)
    temp = fields.Float(string='Temp Float', readonly=True)
    temp_F = fields.Integer(string='Temp F', compute='_compute_temp', store=True)
    temp_C = fields.Integer(string='Temp C', compute='_compute_temp', store=True)
    temp_show = fields.Char(string='Temp', compute='_compute_temp', store=True)

    feels_like = fields.Char(string='Feels Like', readonly=True)
    pop = fields.Char(string='Pop', readonly=True)
    humidity = fields.Char(string='Humidity', readonly=True)
    pressure = fields.Char(string='Pressure', readonly=True)
    clouds = fields.Char(string='Clouds', readonly=True)
    wind_speed = fields.Char(string='Wind Speed', readonly=True)
    wind_deg = fields.Char(string='Wind Deg', readonly=True)
    uvi = fields.Char(string='Uvi', readonly=True)

    url_icon = fields.Char(compute='_compute_url_icon', string='URL weather icon', readonly=True)
    weather_main = fields.Char(string='Weather Main', readonly=True)
    weather_description = fields.Char(string='Weather Description', readonly=True)
    weather_icon = fields.Char(string='Weather Icon Code', readonly=True)

    pop_int = fields.Integer(string='Pop', readonly=True)
    humidity_int = fields.Integer(string='Humidity', readonly=True)
    clouds_int = fields.Integer(string='Clouds', readonly=True)
    pressure_int = fields.Integer(string='Pressure', readonly=True)



    @api.depends('weather_icon')
    def _compute_url_icon(self):
        for r in self:
            r.url_icon = f'http://openweathermap.org/img/wn/{r.weather_icon}@2x.png'
        print('compute url icon')

    @api.depends('temp')
    def _compute_temp(self):
        for r in self:
            r.temp_C = round(r.temp)
            r.temp_F = round(r.temp * 1.8 + 32)
            r.temp_show = f'{r.temp_C} °C'
        print('compute temp')

    def set_temp_C(self):
        self.ensure_one()
        self.temp_show = f'{self.temp_C} °C'

    def set_temp_F(self):
        self.ensure_one()
        self.temp_show = f'{self.temp_F} °F'









