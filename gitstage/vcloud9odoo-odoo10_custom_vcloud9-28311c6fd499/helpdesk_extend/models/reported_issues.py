# -*- coding: utf-8 -*-

from odoo import models, fields


class ReportedIssues(models.Model):
    _name = "helpdesk.reported.issues"

    name=fields.Char(
        string="Name",
        required=True
    )
