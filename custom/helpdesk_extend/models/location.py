# -*- coding: utf-8 -*-

from odoo import models, fields


class Location(models.Model):
    _name = "helpdesk.location"

    name=fields.Char(
        string="Name",
        required=True
    )
