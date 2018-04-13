# -*- coding: utf-8 -*-

from odoo import models, fields


class Make(models.Model):
    _name = "helpdesk.make"

    name=fields.Char(
        string="Name",
        required=True
    )
