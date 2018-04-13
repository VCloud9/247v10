# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):

    _inherit = 'project.project'

    # for top level projects
    subscription_project_id = fields.Many2one('project.project', string='Subscription Project', index=True)
    job_project_ids = fields.One2many('project.project', 'subscription_project_id', string='Job Projects', domain=[('active', '=', True)])
    daily_report_ids = fields.One2many('job.daily.report','job_id', string='Daily Reports')

    @api.onchange('subscription_project_id')
    def _onchange_subscription_id(self):
        for record in self:
            if record.subscription_project_id:
                parent_project = record.search([('id','=',record.subscription_project_id.id)])
                record.partner_id = parent_project[0].partner_id.id

    # for job projects
    date_from = fields.Date('Scheduled Start')

    date_to = fields.Date('Scheduled Finish')

    hotel_name = fields.Many2one(
        string = 'Hotel Name',
        comodel_name = 'res.partner',
        domain = [('supplier','=',True)]
    )

    foreman_id = fields.Many2one(
        string = 'Foreman',
        comodel_name = 'hr.employee',
    )

    crew_id = fields.Many2one(
        comodel_name = 'job.crew',
        string = 'Job Crew',
    )

    crew_employees = fields.Many2many(
        comodel_name = 'hr.employee',
        string = 'Crew Members',
        related = 'crew_id.employee_ids',
    )

    job_instructions = fields.Text(
        string = 'Instructions',
    )

    site_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Site',
        domain = "[('type','=','job')]"
    )

    job_count = fields.Integer(compute='_get_job_count', string="Jobs")

    @api.depends('job_project_ids')
    def _get_job_count(self):
        for project in self:
            project.job_count = len(project.job_project_ids.ids)

    daily_report_count = fields.Integer(compute='_get_daily_report_count', string="Daily Reports")

    @api.depends('daily_report_ids')
    def _get_daily_report_count(self):
        for project in self:
            project.daily_report_count = len(project.daily_report_ids.ids)



