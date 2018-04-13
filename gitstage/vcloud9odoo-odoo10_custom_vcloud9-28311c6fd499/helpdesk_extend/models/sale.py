# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    helpdesk_id = fields.Many2one(
        'helpdesk.ticket',
        string="Helpdesk Ticket",
    )

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if invoice_vals and self.helpdesk_id:
            invoice_vals.update({
                'helpdesk_id':self.helpdesk_id.id,
                'origin': self.helpdesk_id.name_get()[0][1],
            })
        return invoice_vals

    def create_contract(self):
        subscription = super(SaleOrder, self).create_contract()
        if subscription:
            invoice_line_ids = []
            for line in self.order_line:
                if not line.product_id.recurring_invoice:
                    invoice_line_ids.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom_id': line.product_uom.id,
                    }))
            if invoice_line_ids:
                sub_values = {'equipment_subscription_line_ids': invoice_line_ids}
                subscription.write(sub_values)
        return subscription


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #price_unit = fields.Float(
    #    groups="helpdesk_extend.group_sale_price_visible,account.group_account_user",
    #)

    @api.model
    def create(self, values):
        return super(SaleOrderLine, self.sudo()).create(values)

    @api.multi#full override.
    def _get_display_price(self, product):
        if self.order_id.pricelist_id.discount_policy == 'without_discount':
            from_currency = self.order_id.company_id.currency_id
            return from_currency.compute(product.lst_price, self.order_id.pricelist_id.currency_id)
        return product.sudo().with_context(pricelist=self.order_id.pricelist_id.id).price#add sudo by probuse

    @api.multi
    def action_set_unit_price_zero(self):
        for line in self:
            line.price_unit = 0.0


