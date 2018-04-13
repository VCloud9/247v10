# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Certificate(models.Model):
    _name = 'certificate.name'
    _description = 'Certificate Name'

    @api.multi
    @api.depends()
    def _get_cert(self):
        emp_certi_obj = self.env['employee.certificate']
        for rec in self:
            emp_certi_ids = emp_certi_obj.search([('certificate_id', '=', rec.id)])
            rec.certificate_ids = emp_certi_ids.ids
    
    name = fields.Char(
        string='Name',
        required=True
    )
    first_days_reminder = fields.Float(
        string='First Reminder (Days)'
    )
    second_days_reminder = fields.Float(
        string='Second Reminder (Days)'
    )
    certificate_ids = fields.Many2many(
        'employee.certificate',
        compute='_get_cert',
        string='Employee Certificates'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Certification Partner',
        required=True,
    )
    valid_for_years = fields.Integer(
        string='Valid for Years'
    )
    certfication_exp_date = fields.Date(
        string='Certification Expiration Date'
    )
    image = fields.Binary(
        string='Image'
    )
    desc = fields.Text(
        string='Description/Requirement',
    )
