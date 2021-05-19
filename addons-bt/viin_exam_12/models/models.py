# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class viin_exam_12(models.Model):
#     _name = 'viin_exam_12.viin_exam_12'
#     _description = 'viin_exam_12.viin_exam_12'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
