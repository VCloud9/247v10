# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    helpdesk_id = fields.Many2one(
        'helpdesk.ticket',
        string="Helpdesk Ticket",
    )
