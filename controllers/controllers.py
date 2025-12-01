# -*- coding: utf-8 -*-
# from odoo import http


# class GestionNominas(http.Controller):
#     @http.route('/gestion_nominas/gestion_nominas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_nominas/gestion_nominas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_nominas.listing', {
#             'root': '/gestion_nominas/gestion_nominas',
#             'objects': http.request.env['gestion_nominas.gestion_nominas'].search([]),
#         })

#     @http.route('/gestion_nominas/gestion_nominas/objects/<model("gestion_nominas.gestion_nominas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_nominas.object', {
#             'object': obj
#         })

