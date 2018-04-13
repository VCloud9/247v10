# -*- coding: utf-8 -*-

from odoo import models, fields


class Resolution(models.Model):
    _name = "helpdesk.resolution"

    name=fields.Char(
        string="Name",
        required=True
    )
