# -*- coding: utf-8 -*-

from odoo import models, fields

class EquipmentSubscriptionsLine(models.Model):
    _name = "equipment.subscriptions.line"
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product',
        string="Equipment",
        required=True,
    )
    product_uom_qty = fields.Float(
        string='Quantity',
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Unit of Measure',
    )
    serial_number = fields.Char(
        string="Serial Number"
    )
    subscriptions_id = fields.Many2one(
        'sale.subscription',
        string="Subscription",
    )
    site_id = fields.Many2one(
        'res.partner',
        string='Site',
    )
