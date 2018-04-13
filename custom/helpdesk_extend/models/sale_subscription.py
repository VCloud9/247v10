# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.onchange('template_id')
    def on_change_template(self):
        res = super(SaleSubscription, self).on_change_template()
        if self.template_id:
            self.term_and_condition = self.template_id.term_and_condition

    @api.multi
    def action_view_tickets(self):
        self.ensure_one()
        if self.partner_id.child_ids:
            partners.extend(self.partner_id.child_ids.ids)
        helpdesk_id = self.env['helpdesk.ticket'].search([
            ('subscription_id', '=', self.ids),
        ])
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree')
        result = action.read()[0]
        result['domain'] = [('id', 'in', helpdesk_id.ids)]
        return result

    equipment_subscription_line_ids = fields.One2many(
        'equipment.subscriptions.line',
        'subscriptions_id',
        string="Equipments"
    )
    product_ids = fields.Many2many(
        'product.product',
        string='Equipments',
        compute="_compute_products",
        store=True,
    )
    serial_number = fields.Text(
        string="Serial Numbers",
        compute="_compute_serial_number",
        store=True,
    )
    parent_id = fields.Many2one(
        related="partner_id.parent_id",
        string='Parent Customer',
        store=True,
        model='res.partner'
    )
    term_and_condition = fields.Html(
        'Term and Condition'
    )
    signature = fields.Binary(string='Signature', copy=False)
    signature_date = fields.Date(
        string="Signature Date"
    )
    signed_by = fields.Char(
        string="Signed By"
    )

    @api.multi
    @api.depends(
        'equipment_subscription_line_ids',
        'equipment_subscription_line_ids.product_id'
    )
    def _compute_products(self):
        for rec in self:
            product = []
            for line in rec.equipment_subscription_line_ids:
                product.append(line.product_id.id)
            rec.product_ids = [(6, 0, product)]

    @api.multi
    @api.depends(
        'equipment_subscription_line_ids',
        'equipment_subscription_line_ids.serial_number'
    )
    def _compute_serial_number(self):
        for rec in self:
            serial_number = []
            for line in rec.equipment_subscription_line_ids:
                if line.serial_number:
                    serial_number.append(line.serial_number)
            if serial_number:
                serial_number_str = ', '.join(serial_number)
                rec.serial_number = serial_number_str

class SaleSubscriptionTemplate(models.Model):
    _inherit = "sale.subscription.template"

    term_and_condition = fields.Html(
        'Term and Condition'
    )
