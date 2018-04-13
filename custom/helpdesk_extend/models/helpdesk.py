# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class HelpDeskWorkTiming(models.Model):
    _name = 'helpdesk.work.time.line'

    ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string="Ticket",
    )
    response_time = fields.Datetime(
        string="Response Time",
    )
    status = fields.Selection(
        selection=[
            ('start', 'Started'),
            ('pause', 'Paused'),
            ('stop', 'Stopped'),
        ],
        string="Status",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    user_id = fields.Many2one(
        'res.users',
        string="Responsible User",
        default=lambda self: self.env.user,
    )
    pause_time = fields.Datetime(
        string="Pause Time",
    )
    work_time = fields.Float(
        string="Work Time",
        compute="_compute_work_time",
    )
    reason_pause = fields.Char(
        string="Pause Reason"
    )

    @api.depends('response_time', 'pause_time')
    def _compute_work_time(self):
        for rec in self:
            if rec.response_time and rec.pause_time:
                work_stop_time = datetime.strptime(rec.response_time, '%Y-%m-%d %H:%M:%S')
                work_start_time = datetime.strptime(rec.pause_time, '%Y-%m-%d %H:%M:%S')
                diff_time = work_start_time - work_stop_time
                rec.work_time = diff_time.total_seconds() / 60.0 / 60.0

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def cause_ids_str(self, cause_id):
        name_str = ', '.join([i.name for i in cause_id])
        cause_ids = str(name_str)
        return cause_ids
    
    def tag_ids_str(self, tag_id):
        name_str = ', '.join([i.name for i in tag_id])
        tag_ids = str(name_str)
        return tag_ids
    
    def reported_issues_ids_str(self, reported_issues_id):
        name_str = ', '.join([i.name for i in reported_issues_id])
        reported_issues_ids = str(name_str)
        return reported_issues_ids
    
    def resolution_ids_str(self, resolution_id):
        name_str = ', '.join([i.name for i in resolution_id])
        resolution_ids = str(name_str)
        return resolution_ids

    @api.multi
    @api.onchange('subscription_id','subscription_id.project_ids')
    def onchange_project(self):
        for rec in self:
            rec.project_id = rec.subscription_id.project_ids and rec.subscription_id.project_ids[0] or False
        return {'domain': {'project_id': [('id', 'in', rec.subscription_id.project_ids.ids)]}}

    quotations_count = fields.Integer(
        compute="_quotations_count",
    )
    invoice_count = fields.Integer(
        compute="_invoice_count",
    )
    delivery_count = fields.Integer(
        compute="_delivery_count",
    )
    order_count = fields.Integer(
        compute="_order_count",
    )
    subscriptions_count = fields.Integer(
        compute="_subscriptions_count",
    )
    timesheet_count = fields.Integer(
        compute="_timesheet_count",
    )
    account_analytic_lines = fields.One2many(
        'account.analytic.line',
        'helpdesk_id',
        string="Analytic account"
    )
    enroute_start_time = fields.Datetime(
        string="Traveling Start Time",
    )
    enroute_stop_time = fields.Datetime(
        string="Traveling Stop Time",
    )
    work_time_lines = fields.One2many(
        'helpdesk.work.time.line',
        'ticket_id',
        string="Work Time History",
        readonly=False,
    )
    enroute_time = fields.Float(
        string="Total Traveling Time",
        compute="_compute_enroute_time",
    )
    pause_reason = fields.Char(
        string="Reason for Pause",
    )
    po_ref = fields.Char(
        string="Purchase Order #",
        required=False, 
    )
    working_hours = fields.Float(
        string="Working Hour(s)",
        compute="_compute_working_hours",
    )
    reported_issues_ids = fields.Many2many(
        'helpdesk.reported.issues',
        string='Reported Issues',
        required=False, 
    )
    cause_ids = fields.Many2many(
        'helpdesk.cause',
        string='Causes', 
    )
    resolution_ids = fields.Many2many(
        'helpdesk.resolution',
        string='Resolutions', 
    )
    location_id = fields.Many2one(
        'helpdesk.location', 
        'Location', 
    )
    make_id = fields.Many2one(
        'helpdesk.make', 
        'Make', 
    )
    subscription_id = fields.Many2one(
        'sale.subscription', 
        'Contracts', 
    )
    contract_item_id = fields.Many2one(
        'equipment.subscriptions.line',
        'Contract Asset', 
    )
    description = fields.Text(
        required=False,
    )
    help_desk_team_type = fields.Selection(
        related="team_id.team_type",
        string='Help Desk Team Type',
    )
    parent_id = fields.Many2one(
        related="partner_id.parent_id",
        string='Parent Company',
        store=True,
        model='res.partner'
    )
    project_id = fields.Many2one(
        'project.project',
        'Project',
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        related='subscription_id.analytic_account_id',
        store=True,
    )
    site_id = fields.Many2one(
        'res.partner',
        string='Site',
    )
    signature = fields.Binary(string='Signature', copy=False)
    signature_date = fields.Date(
        string="Signature Date"
    )
    signed_by = fields.Char(
        string="Signed By"
    )

    @api.multi
    @api.onchange('subscription_id', 'contract_item_id')
    def subscription_id_change(self):
        partner_ids = []
        for rec in self:
            if rec.subscription_id:
                partner_ids = [s.site_id.id for s in rec.subscription_id.equipment_subscription_line_ids]
            if rec.contract_item_id:
                partner_ids = [rec.contract_item_id.site_id.id]
        return {'domain': {'site_id': [('id', 'in', partner_ids)]}}

    @api.depends('enroute_start_time', 'enroute_stop_time')
    def _compute_enroute_time(self):
        for rec in self:
            if rec.enroute_stop_time and rec.enroute_start_time:
                enroute_stop_time = datetime.strptime(rec.enroute_stop_time, '%Y-%m-%d %H:%M:%S')
                enroute_start_time = datetime.strptime(rec.enroute_start_time, '%Y-%m-%d %H:%M:%S')
                diff_time = enroute_stop_time - enroute_start_time
                rec.enroute_time = diff_time.total_seconds() / 60.0 / 60.0

    @api.depends('work_time_lines')
    def _compute_working_hours(self):
        work_time = 0.0
        for line in self.work_time_lines:
            self.working_hours = self.working_hours + line.work_time

    @api.multi
    def create_quotation(self):
        self.ensure_one()
        form_view = self.env.ref('sale.view_order_form')
        return {
            'name': _('Quotations'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'sale.order',
            'view_id': False,
            'views': [
                (form_view.id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'context': {
                'default_partner_id':self.partner_id.id,
                'default_helpdesk_id':self.id,
                'default_origin':self.name_get()[0][1] + '-' + self.name,
            }
        }

    @api.multi
    @api.depends()
    def _timesheet_count(self):
        self.ensure_one()
        self.timesheet_count = self.env['account.analytic.line'].search_count([
            ('helpdesk_id', '=', self.id),
        ])

    @api.multi
    @api.depends()
    def _quotations_count(self):
        self.ensure_one()
        self.quotations_count = self.env['sale.order'].search_count([
            ('helpdesk_id', '=', self.id),
            ('state', 'in', ['draft', 'sent']),
            ('state', 'not in', ['sale', 'done', 'cancel']),
        ])

    @api.multi
    @api.depends()
    def _subscriptions_count(self):
        self.ensure_one()
        partners = self.partner_id.ids
        if self.partner_id.child_ids:
            partners.extend(self.partner_id.child_ids.ids)
        self.subscriptions_count = self.env['sale.subscription'].search_count([
            ('company_id', '=', self.company_id.id),
            ('partner_id', 'in', partners),
            ('state', 'in', ['draft', 'open']),
        ])

    @api.multi
    @api.depends()
    def _order_count(self):
        self.ensure_one()
        self.order_count = self.env['sale.order'].search_count([
            ('helpdesk_id', '=', self.id),
            ('state', 'in', ['sale', 'done', 'cancel']),
        ])

    @api.multi
    @api.depends()
    def _invoice_count(self):
        self.ensure_one()
        self.invoice_count = self.env['account.invoice'].search_count([
            ('helpdesk_id', '=', self.id),
        ])

    @api.multi
    @api.depends()
    def _delivery_count(self):
        self.ensure_one()
        quotations_id = self.env['sale.order'].search([
            ('helpdesk_id', '=', self.id),
        ])
        self.delivery_count = self.env['stock.picking'].search_count([
            ('sale_id', 'in', quotations_id.ids),
        ])

    @api.multi
    def write(self, vals):
        WorkTimeLine = self.env['helpdesk.work.time.line']
        res = super(HelpdeskTicket, self).write(vals)
        if vals.get('stage_id'):
            stage = self.env['helpdesk.stage'].browse(vals.get('stage_id'))
            for rec in self:
                if stage.stage_type == 'en_route': # Traveling Stage
                    rec.enroute_start_time = datetime.now()
                elif stage.stage_type == 'work_started': # Work Start Stage
                    if not rec.enroute_stop_time or True:#Should go always here.
                        rec.enroute_stop_time = datetime.now()
                    line = WorkTimeLine.create({
                         'ticket_id': rec.id,
                         'response_time': datetime.now(),
                         'status': 'start',
                    })
                elif stage.stage_type == 'work_pause': # Work Pause
#                     if not rec.pause_reason:
#                         raise UserError(_('Please add pause reason!'))
                    # TODO: Maintain pause reason for multiple time pausing
                    work_time_line_id = WorkTimeLine.search([('pause_time', '=', False),('ticket_id', '=', rec.id)])
                    work_time_line_id.write({'pause_time':datetime.now()})
                elif stage.stage_type == 'work_complete': # Work Complete
                    work_time_line_id = WorkTimeLine.search([('pause_time', '=', False),('ticket_id', '=', rec.id)])
                    work_time_line_id.write({'pause_time':datetime.now()})
        return res

    @api.multi
    def action_view_quotations(self):
        self.ensure_one()
        quotations_id = self.env['sale.order'].search([
            ('helpdesk_id', '=', self.id),
            ('state', 'in', ['draft', 'sent']),
            ('state', 'not in', ['sale', 'done', 'cancel']),
        ])
        action = self.env.ref('sale.action_quotations')
        result = action.read()[0]
        result['domain'] = [('id', 'in', quotations_id.ids)]
        return result

    @api.multi
    def action_view_invoice(self):
        self.ensure_one()
        invoice_id = self.env['account.invoice'].search([
            ('helpdesk_id', '=', self.id)
        ])
        action = self.env.ref('account.action_invoice_tree1')
        result = action.read()[0]
        result['domain'] = [('id', 'in', invoice_id.ids)]
        return result

    @api.multi
    def action_view_delivery(self):
        self.ensure_one()
        quotations_id = self.env['sale.order'].search([
            ('helpdesk_id', '=', self.id)
        ])
        picking_id = self.env['stock.picking'].search([
            ('sale_id', 'in', quotations_id.ids)
        ])
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        result['domain'] = [('id', 'in', picking_id.ids)]
        return result

    @api.multi
    def action_view_order(self):
        self.ensure_one()
        order_id = self.env['sale.order'].search([
            ('helpdesk_id', '=', self.id),
            ('state', 'in', ['sale', 'done', 'cancel']),
        ])
        action = self.env.ref('sale.action_orders')
        result = action.read()[0]
        result['domain'] = [('id', 'in', order_id.ids)]
        return result

    @api.multi
    def action_view_subscriptions(self):
        self.ensure_one()
        partners = self.partner_id.ids
        if self.partner_id.child_ids:
            partners.extend(self.partner_id.child_ids.ids)
        subscriptions_id = self.env['sale.subscription'].search([
            ('company_id', '=', self.company_id.id),
            ('partner_id', 'in', partners),
        ])
        action = self.env.ref('sale_contract.sale_subscription_action')
        result = action.read()[0]
        result['domain'] = [('id', 'in', subscriptions_id.ids)]
        result['context'] = {'search_default_open':1}
        return result

    @api.multi
    def action_view_timesheet(self):
        self.ensure_one()
        partners = self.partner_id.ids
        if self.partner_id.child_ids:
            partners.extend(self.partner_id.child_ids.ids)
        timesheet_id = self.env['account.analytic.line'].search([
            ('helpdesk_id', '=', self.id)
        ])
        action = self.env.ref('hr_timesheet.act_hr_timesheet_line')
        result = action.read()[0]
        result['domain'] = [('id', 'in', timesheet_id.ids)]
        return result
