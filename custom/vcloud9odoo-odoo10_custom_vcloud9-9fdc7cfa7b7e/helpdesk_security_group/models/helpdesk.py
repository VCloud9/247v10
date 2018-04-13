# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    v_helpdesk_group = fields.Many2one(
        'helpdesk.group',
        string='Helpdesk Group',
        copy=True
    )
    v_group_user_id = fields.Many2many(
        'res.users',
        string='Group Users',
        copy=True
    )

    @api.multi
    @api.onchange('v_helpdesk_group')
    def onchange_v_helpdesk_group(self):
        for rec in self:
            rec.v_group_user_id = rec.v_helpdesk_group.v_user_ids
