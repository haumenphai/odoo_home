# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'schoolv2.student'
    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='Created User', default=lambda self: self.env.user)