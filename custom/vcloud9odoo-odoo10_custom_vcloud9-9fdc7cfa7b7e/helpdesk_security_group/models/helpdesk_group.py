# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpDeskGroup(models.Model):
    _name = 'helpdesk.group'
    _rec_name = "v_name"

    v_helpdesk_team = fields.Many2one(
        'helpdesk.team',
        string='Helpdesk Team'
    )
    v_user_ids = fields.Many2many(
        'res.users',
        string='User', 
        required=True
    )
    v_name = fields.Char(
        string='Name',
        required=True
    )

    @api.multi
    @api.onchange('v_helpdesk_team')
    def onchange_v_helpdesk_team(self):
        for rec in self:
            rec.v_user_ids = rec.v_helpdesk_team.member_ids
