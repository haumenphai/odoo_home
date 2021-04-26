from odoo import models, fields, api


class CustomLocation(models.Model):
    _name = 'weather.customlocation'
    _description = 'Customize locations to get weather forecast'
    _inherit = 'weather.forecast'

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user,
                              groups='weather.group_weather_admin', readonly=True)
