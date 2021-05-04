# -*- coding: utf-8 -*-
# from odoo import http


# class Schoolv3(http.Controller):
#     @http.route('/schoolv3/schoolv3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/schoolv3/schoolv3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('schoolv3.listing', {
#             'root': '/schoolv3/schoolv3',
#             'objects': http.request.env['schoolv3.schoolv3'].search([]),
#         })

#     @http.route('/schoolv3/schoolv3/objects/<model("schoolv3.schoolv3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('schoolv3.object', {
#             'object': obj
#         })
