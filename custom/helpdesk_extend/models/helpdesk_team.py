# -*- coding: utf-8 -*-
from odoo import models, fields

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'
    
    team_type = fields.Selection(
        [('service_team','Service Team'),
         ('non_service_team', 'Non - Service Team')],
        string='Team Type',
        default='non_service_team',
    )