# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'schoolv3.student'
    _description = 'schoolv3.student'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age', default=20)
    address = fields.Char(string='Address', default='default address')

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

    def test_copy(self):
        # single, return new record.
        r = self.copy({'age': self.age + 1})

    def test_default_get(self):
        l = self.search([])
        r = l.default_get(['age', 'address'])
        print(f'result: {r}')