# -*- coding: utf-8 -*-
# from odoo import http


# class Project1(http.Controller):
#     @http.route('/project_1/project_1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_1/project_1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_1.listing', {
#             'root': '/project_1/project_1',
#             'objects': http.request.env['project_1.project_1'].search([]),
#         })

#     @http.route('/project_1/project_1/objects/<model("project_1.project_1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_1.object', {
#             'object': obj
#         })
