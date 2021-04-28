# -*- coding: utf-8 -*-
# from odoo import http


# class XemBoi(http.Controller):
#     @http.route('/xem_boi/xem_boi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xem_boi/xem_boi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xem_boi.listing', {
#             'root': '/xem_boi/xem_boi',
#             'objects': http.request.env['xem_boi.xem_boi'].search([]),
#         })

#     @http.route('/xem_boi/xem_boi/objects/<model("xem_boi.xem_boi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xem_boi.object', {
#             'object': obj
#         })
