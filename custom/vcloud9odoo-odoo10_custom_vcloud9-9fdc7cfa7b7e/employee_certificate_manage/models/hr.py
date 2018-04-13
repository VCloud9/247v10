# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = "hr.employee"
    
    certificate_ids = fields.One2many(
        'employee.certificate',
        'employee_id',
        string='Certificates'
    )