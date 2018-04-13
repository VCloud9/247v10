# -*- coding: utf-8 -*-

from odoo import models, fields, api

class State(models.Model):
    _inherit = 'res.country.state'


    min_wage = fields.Float(
        string = 'Minimum Wage',
        required = False,
    )

