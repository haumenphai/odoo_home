# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'schoolv3.student'
    _description = 'schoolv3.student'

    name = fields.Char(string='Name')

    def unlink(self):
        s = self.env['to.vietnamese.number2words']
        print(s.num2words(2))

