# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    @api.model
    def _get_stage_types(self):
        return [
            ('en_route', 'En Route'),
            ('work_started', 'Work Start'),
            ('work_pause', 'Work Pause'),
            ('work_complete', 'Work Complete'),
        ]

    stage_type = fields.Selection(
        selection=_get_stage_types,
        string='Stage Type',
    )

    @api.constrains('stage_type')
    def _stage_type_validation(self):
        for stage in self:
            if stage.stage_type:
                stage_ids = self.search_count([('stage_type', '=', stage.stage_type)])
                if stage_ids > 1:
                    raise ValidationError(_('You can not set multiple stage with same type!'))
