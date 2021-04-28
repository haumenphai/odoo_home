from odoo import models, fields, api

from datetime import datetime
import random

class Person(models.Model):
    _name = 'school.person'
    _description = 'person'

    name = fields.Char(required=True, string='Họ tên', help="This param 'help' of field. [field: name]")
    birth_day = fields.Date(required=True, string="Ngày sinh", default = '1900-02-20')
    address = fields.Char(required=True, string="Địa chỉ")
    gioi_tinh = fields.Selection([
        ('Nam_', 'Nam'),
        ('Nu_', 'Nữ')
    ],required=True, string='Giới tính', default='Nam_')
    
    age = fields.Integer(readonly=True, string='Tuổi', compute='_get_age')
    
    @api.depends('birth_day')
    def _get_age(self):
        try:
            print(self)

            now_year = datetime.now().year
            for o in self:
                o.age = now_year - o.birth_day.year
        except Exception as e:
            print('exception:', e)
            
    
    













            