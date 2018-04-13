# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    helpdesk_id = fields.Many2one(
        'helpdesk.ticket',
        string="Helpdesk Ticket",
    )

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    helpdesk_id = fields.Many2one(
        'helpdesk.ticket',
        string="Helpdesk Ticket",
    )
