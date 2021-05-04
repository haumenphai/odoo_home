# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolV2(http.Controller):
#     @http.route('/school_v2/school_v2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_v2/school_v2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_v2.listing', {
#             'root': '/school_v2/school_v2',
#             'objects': http.request.env['school_v2.school_v2'].search([]),
#         })

#     @http.route('/school_v2/school_v2/objects/<model("school_v2.school_v2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_v2.object', {
#             'object': obj
#         })
