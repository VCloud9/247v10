# -*- coding: utf-8 -*-

import datetime as DT
import datetime
from datetime import date
import time
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class EmployeeCertificate(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name = 'employee.certificate'
    _rec_name = 'employee_id'
    _description = 'Employee Certificate'
    
    @api.multi
    @api.onchange('certificate_id')
    def onchange_certificate(self):
        for rec in self:
            today = datetime.datetime.today()
            rec.desc = rec.certificate_id.desc
            rec.certfication_exp_date = today.replace(today.year + rec.certificate_id.valid_for_years)#Add Year in date#datetime.datetime.strptime(date.today().strftime('%Y-%m-%d'), '%Y-%m-%d') + DT.timedelta(relativedelta(years=1))
    
    @api.multi
    @api.depends('first_days_reminder','certfication_exp_date')
    def onchange_first_reminder_date(self):
        for rec in self:
            if rec.certfication_exp_date:
                certfication_exp_date = datetime.datetime.strptime(rec.certfication_exp_date, '%Y-%m-%d')
                first_reminder = certfication_exp_date - DT.timedelta(days=rec.first_days_reminder)
                first_reminder = datetime.date.strftime(first_reminder, '%Y-%m-%d')
                rec.first_reminder_date = first_reminder
            
    @api.multi
    @api.depends('second_days_reminder','certfication_exp_date')
    def onchange_second_reminder_date(self):
        for rec in self:
            if rec.certfication_exp_date:
                certfication_exp_date = datetime.datetime.strptime(rec.certfication_exp_date, '%Y-%m-%d')
                second_reminder = certfication_exp_date - DT.timedelta(days=rec.second_days_reminder)
                second_reminder = datetime.date.strftime(second_reminder, '%Y-%m-%d')
                rec.second_reminder_date = second_reminder
            
    certificate_id = fields.Many2one(
        'certificate.name',
        string='Name of Certificate',
        required=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Certification Partner',
        related='certificate_id.partner_id',
        required=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
    )
    certification_date = fields.Date(
        string='Effective Date',
    )
    desc = fields.Text(
        string='Description/Requirement',
    )
    certfication_exp_date = fields.Date(
#         related='certificate_id.certfication_exp_date',
        string='Certification Expiration Date'
    )
    first_reminder_date = fields.Date(
        string='First Reminder Date',
        compute='onchange_first_reminder_date'
    )
    first_days_reminder = fields.Float(
        string='First Reminder (Days)',
        related='certificate_id.first_days_reminder',
    )
    second_reminder_date = fields.Date(
        string='Second Reminder Date',
        compute='onchange_second_reminder_date'
    )
    second_days_reminder = fields.Float(
        string='Second Reminder (Days)',
        related='certificate_id.second_days_reminder',
    )
    company_id = fields.Many2one(
        'res.company', 
        required=True, 
        default=lambda self: self.env.user.company_id, 
        string='Company', 
        readonly=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Created by',
        default=lambda self: self.env.user,
        readonly=True
    )
    
    @api.multi
    @api.depends('first_reminder_date', 'certfication_exp_date')
    def _compute_certificate_state(self):
        today = date.today().strftime('%Y-%m-%d')
        for rec in self:
            rec.state = 'running'
            if rec.certfication_exp_date:
                certfication_exp_date = datetime.datetime.strptime(rec.certfication_exp_date, '%Y-%m-%d')
                certfication_exp_date = datetime.date.strftime(certfication_exp_date, '%Y-%m-%d') 
                
                first_reminder_date = datetime.datetime.strptime(rec.first_reminder_date, '%Y-%m-%d')
                first_reminder_date = datetime.date.strftime(first_reminder_date, '%Y-%m-%d') 
                
                if first_reminder_date <= today and certfication_exp_date > today:
                    rec.state = 'expiring_soon'
                elif certfication_exp_date <= today:
                    rec.state = 'expired'
                elif first_reminder_date < today:
                    rec.state = 'running'
        
    state = fields.Selection(
        [('running','Running'),
         ('expiring_soon','Expiring Soon'),
         ('expired','Expired')],
        string='State',
        default='running',
        store=True,
        compute='_compute_certificate_state'
    )
    
    @api.multi
    def run_first_days_reminder(self):
        ir_model_data = self.env['ir.model.data']
        template_pool = self.env['mail.template']
        mail_obj = self.env['mail.mail']
        certificates = self.search([])
        for certificate in certificates:
            certfication_exp_date = datetime.datetime.strptime(certificate.certfication_exp_date, '%Y-%m-%d')
            first_reminder = certfication_exp_date - DT.timedelta(days=certificate.first_days_reminder)
            first_reminder = datetime.date.strftime(first_reminder, '%Y-%m-%d')
            today = date.today().strftime('%Y-%m-%d')
            if today == first_reminder:
                template_id = self.env.ref('employee_certificate_manage.email_template_first_days_reminder')
                if template_id:
                    template_id.send_mail(certificate.id)
    
    @api.multi
    def run_second_days_reminder(self):
        ir_model_data = self.env['ir.model.data']
        template_pool = self.env['mail.template']
        mail_obj = self.env['mail.mail']
        certificates = self.search([])
        import time
        for certificate in certificates:
            certfication_exp_date = datetime.datetime.strptime(certificate.certfication_exp_date, '%Y-%m-%d')
            second_reminder = certfication_exp_date - DT.timedelta(days=certificate.second_days_reminder)
            second_reminder = datetime.date.strftime(second_reminder, '%Y-%m-%d')
            today = date.today().strftime('%Y-%m-%d')
            if today == second_reminder:
                template_id = self.env.ref('employee_certificate_manage.email_template_second_days_reminder')
                if template_id:
                    template_id.send_mail(certificate.id)
        
