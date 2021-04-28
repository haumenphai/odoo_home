from odoo import models, fields, api


class PlayerPosition(models.Model):
    _name = 'football.playerposition'
    _description = 'Player Position'

    name = fields.Char('Position')