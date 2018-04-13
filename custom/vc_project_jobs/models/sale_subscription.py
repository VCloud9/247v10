# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    #make sure the Analytic Account is created as a Project each time a subscription is created
    @api.model
    def create(self, vals):
        vals['use_tasks'] = True
        vals['project_type'] = 'subscription'
        return super(SaleSubscription, self).create(vals)

    @api.multi
    def action_subscription_projects(self):
        return {
                "type": "ir.actions.act_window",
                "res_model": "project.project",
                "res_id": self.project_ids.ids[0],
                "domain": [["id", "in", self.project_ids.ids]],
                "views": [[self.env.ref('project.edit_project').id, "form"]],
                "name": "Projects",
        }



