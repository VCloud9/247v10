# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Productproduct(models.Model):
    _inherit = 'product.product'
    
    #lst_price = fields.Float(
     #   groups="helpdesk_extend.group_sale_price_visible,account.group_account_user",
    #)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    #list_price = fields.Float(
     #   groups="helpdesk_extend.group_sale_price_visible,account.group_account_user",
    #)
