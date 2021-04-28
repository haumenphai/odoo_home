# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.api import Environment
import random
from docutils.nodes import Invisible

class GiaoVien(models.Model):
    _name = 'school.giaovien'
    _description = 'giáo viên'
    _inherit = 'school.person'

    luong = fields.Float(string='Lương')
    chu_nhiem_lop = fields.Many2one('school.class', string='Chủ nhiệm lớp')
    bo_mon_day = fields.Many2many('school.monhoc', string='Bộ môn dạy')
    active = fields.Boolean(default=True)
    
    
    def test_v1(self):
        print('-----------------------------------------------------------------------')
        print(type(self.luong), type(self.bo_mon_day))
        print(self.env['school.person'], Environment.user, self.env.user.name)
        print(self.luong, self.chu_nhiem_lop)
        print('uid: ', self.env.uid)
        print('user name: ', self.env.user.name)
        s = self.env.cr.execute('SELECT * FROM school_giaovien')
        print('s: ',s)
        print(self.read(['name', 'luong']))
        print(self.name)
        print('\n=======================================\n')
        print(self.env['school.giaovien'].search([]))
        print(self.bo_mon_day.name)
        print('-----------------------------------------------------------------------')
       
    
    def test_v2(self):
        print('------------------------------------------------------------------------')
        print('self.name: ', self.name)
        print('selef.class_id',  self.chu_nhiem_lop)
        print('------------------------------------------------------------------------')
    
    
    def print_report(self): 
        return self.env.ref('my_school.report_giao_vien1').report_action(self)
    
    def test1234(self):
        user1 = self.with_context({},uid=6)
        print(user1._context)
        
    person_test_id = fields.Many2one('school.persontest', invisible=True)

class Student(models.Model):
    _name = 'school.student'
    _description = 'Học sinh'
    _inherit = 'school.person'

    hoc_sinh_lop = fields.Many2one('school.class', string='Học sinh lớp')
    tinh_trang   = fields.Selection([
        ('Da_tot_nghiep', 'Đã tốt nghiệp'),
        ('Dang_hoc', 'Đang học')
        ], default='Dang_hoc', string='Tình trạng')
    
    related_field_test = fields.Char(related='hoc_sinh_lop.name')
    


class Class(models.Model):
    _name = 'school.class'
    _description = 'Lớp học'

    name = fields.Char(required=True, string='Tên lớp', index=True)
    phong_hoc = fields.Char(string="Số phòng")
    hoc_sinh_trong_lop = fields.One2many('school.student', 'hoc_sinh_lop',
                                        string='Học sinh của lớp', copy=True)

    tham_chieu = fields.Reference(
        selection=[('school.student', 'Học Sinh'), ('school.giaovien', 'Giáo viên')], 
        string='Field Reference')
    
   

class MonHoc(models.Model):
    _name = 'school.monhoc'
    _description = 'Mon hoc'
    
    name = fields.Char(required=True, string='Môn học')
    giao_vien_ids = fields.Many2many('school.giaovien', string='Giáo viên dạy')
    image = fields.Image(max_height=200)
    
    currency_id = fields.Many2one('res.currency', string='loại tiền', )
    hoc_phi_mon = fields.Monetary(string='Học phí', currency_field='currency_id')
    
    
    
class BaoVe(models.Model):
    _name = 'school.baove'
    _inherit = 'school.person'
    _description = 'bao ve'
    _sequence = 'jj'
    
    
    
    
    
    



