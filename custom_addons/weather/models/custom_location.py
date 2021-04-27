from odoo import models, fields, api


class CustomLocation(models.Model):
    _name = 'weather.customlocation'
    _description = 'Customize locations to get weather forecast'
    _inherit = 'weather.forecast'

    user_id = fields.Many2one('res.users', string='Created User', default=lambda self: self.env.user,
                              groups='weather.group_weather_admin', readonly=True)

    @api.model
    def create(self, vals_list):
        rec = super(CustomLocation, self).create(vals_list)
        rec.write({
            'hourly_ids': [
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
            ],
            'daily_ids': [
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
                (0, 0, {'temp_show': 'null'}),
            ]
        })
        return rec

    def update_data_weather(self):
        super(CustomLocation, self).update_data_weather()
        return {
            'name': 'Your location',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'weather.customlocation',
            'target': 'current'
        }

