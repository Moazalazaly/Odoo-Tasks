# -*- coding: utf-8 -*-
# from odoo import http


# class InternshipApp(http.Controller):
#     @http.route('/internship_app/internship_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/internship_app/internship_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('internship_app.listing', {
#             'root': '/internship_app/internship_app',
#             'objects': http.request.env['internship_app.internship_app'].search([]),
#         })

#     @http.route('/internship_app/internship_app/objects/<model("internship_app.internship_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('internship_app.object', {
#             'object': obj
#         })

