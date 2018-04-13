# -*- coding: utf-8 -*-

from odoo import models, fields


class Cause(models.Model):
    _name = "helpdesk.cause"

    name=fields.Char(
        string="Name",
        required=True
    )
