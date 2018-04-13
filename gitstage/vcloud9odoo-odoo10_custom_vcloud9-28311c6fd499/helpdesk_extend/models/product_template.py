# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    track_service = fields.Selection(selection_add=[
#         ('create_purchase_order_line', 'Create a Purchase Order (by SO Lines)'),
        ('task', 'Create a task, track hours and Create a Purchase Order (by SO Lines)'),
        ])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
