# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'schoolv3.student'
    _description = 'schoolv3.student'

    name = fields.Char(string='Name')
    state_visibility = fields.Boolean(string='State Visibility')
    state = fields.Selection(selection=[
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('level3', 'Level 3'),
        ('level 4', 'Level 4'),
    ], string='Status', required=True, copy=False, tracking=True, default='level1')
    fields_level1 = fields.Char(string='Level', defaut="This is Level mess",
                                states={
                                    'level1': [('readonly', True), ('invisible', False), ('required', False)],
                                    'level2': [('invisible', True)],
                                    'level3': [('invisible', False)],
                                    'level 4': [('invisible', True)],
                                }
    )

    def print_name(self):
        print(self.name)


    def unlink(self):
        s = self.env['to.vietnamese.number2words']
        print(s.num2words(2))
        cre = self.mapped('create_uid')
        cre.print_name()
