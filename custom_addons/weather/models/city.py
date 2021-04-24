from odoo import fields, models, api


class City(models.Model):
    _name = 'weather.city'
    _description = ''

    name = fields.Char('Location', required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)


