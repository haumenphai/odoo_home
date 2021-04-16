# -*- coding: utf-8 -*-
from odoo import http


class MySchool(http.Controller):
    @http.route('/hello', auth='public')
    def index1(self, **kw):
        return "Hello, world"
    
    
    @http.route('/students', auth='public')
    def index2(self, **kw):
        return http.request.render('my_school.index', {
            'students': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })
    
    
    @http.route('/monhoc', auth='public')
    def index3(self, **kw):
        monhoc = http.request.env['myschool.monhoc']
        return http.request.render('my_school.mochoc123', {
            
            }) 
    
    
    
    
#     @http.route('/my_school/my_school/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_school.listing', {
#             'root': '/my_school/my_school',
#             'objects': http.request.env['my_school.my_school'].search([]),
#         })

#     @http.route('/my_school/my_school/objects/<model("my_school.my_school"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_school.object', {
#             'object': obj
#         })
