# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    project_type = fields.Selection(
        string = 'Project Type',
        selection = [('template','Template'),('subscription','Subscription'),('job','Job')],
    )


class AnalyticAccountLine(models.Model):
    _inherit = "account.analytic.line"

    rate = fields.Float(
        string = 'Rate',
    )


    r_total = fields.Float(
        string = 'Total',
        compute = '_calc_r_total',
    )

    @api.multi
    def _calc_r_total(self):
        for record in self:
            record.r_total = record.rate * record.unit_amount

