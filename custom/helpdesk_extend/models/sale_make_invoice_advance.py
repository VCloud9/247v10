# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        self.ensure_one()
        invoice_id = super(SaleAdvancePaymentInv, self)._create_invoice(
            order=order, so_line=so_line, amount=amount)
        if order.helpdesk_id:
            invoice_id.write({'helpdesk_id':order.helpdesk_id.id})
        return invoice_id
