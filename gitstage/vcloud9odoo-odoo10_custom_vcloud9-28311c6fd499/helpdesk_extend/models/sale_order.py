# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.multi
    @api.depends('order_line','order_line.is_po_created')
    def _check_is_po_created(self):
        for rec in self:
            for line in rec.order_line:
                if not line.is_po_created:
                    rec.so_created = True
    
    need_external_service = fields.Boolean(
        string='Is Need External Service?',
        default=True,
    )
    so_created = fields.Boolean(
        string='IS Sales Order Created?',
        compute='_check_is_po_created',
    )
    purchase_order_ids = fields.One2many(
        'purchase.order',
        'sale_order_id',
        string='Purchase Order'
    )
    
    @api.multi
    def get_purchase_order(self):
        for rec in self:
            purchase_orders = self.env['purchase.order'].search([('sale_order_id', '=', rec.id)])
            action = self.env.ref('purchase.purchase_form_action')
            result = action.read()[0]
            result.update({'domain': [('id', 'in', purchase_orders.ids)]})
        return result
        
    
    @api.model
    def _get_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'),
                                ('warehouse_id.company_id', '=', company_id),])
        return types[0].id if types else False

    @api.multi
    def _prepare_purchase_order(self, sale_orders, partner):
        sale_order_id = sale_orders 
        fpos = self.env['account.fiscal.position'].with_context(\
                company_id=sale_order_id.company_id.id).get_fiscal_position(partner.id)
        if not partner:
            raise Warning('Please select vendor on Sales order line')
        res = {
            'partner_id': partner.id,
            'picking_type_id': self._get_picking_type(),
            'company_id': sale_order_id.company_id.id,
            'currency_id': partner.property_purchase_currency_id.id \
                            or self.env.user.company_id.currency_id.id,
            'origin': sale_order_id.name,
            'payment_term_id': partner.property_supplier_payment_term_id.id,
            'date_order': sale_order_id.date_order,
            'fiscal_position_id': fpos,
            'order_id': sale_order_id.id,
            'sale_order_id':sale_order_id.id
        }
        return res
    
    @api.multi
    def _prepare_purchase_order_line(self, po, line):
        taxes = line.product_id.supplier_taxes_id
        fpos = po.fiscal_position_id
        taxes_id = fpos.map_tax(taxes) if fpos else taxes
        if taxes_id:
            taxes_id = taxes_id.filtered(lambda x: x.company_id.id == line.company_id.id)
        date_planned = datetime.today()
        seller = line.product_id._select_seller(
            partner_id=po.partner_id,
            quantity=line.product_uom_qty,
            date=po.date_order,
            uom_id=line.product_id.uom_po_id)
        return {
            'product_qty': line.product_uom_qty,
            'product_id': line.product_id.id,
            'product_uom': line.product_id.uom_po_id.id,
            'price_unit':  seller.price or 0.0,
            'date_planned': date_planned,
            'taxes_id': [(6, 0, taxes_id.ids)],
            'order_id': po.id,
            'name': line.name,
#             'account_analytic_id': line.order_id.compute_project_id.id,
        }
    
    @api.multi
    def create_purchase_order_based_vendor(self, order_line=None):
        vendor_dict = {}
        if order_line:
            order_line = [order_line]
        else:
            order_line = []
        for rec in self:
            sale_order = rec
            for line in order_line:
                if line.vendor_id not in vendor_dict:
                    vendor_dict[line.vendor_id] = [line]
                else:
                    vendor_dict[line.vendor_id].append(line)
        order_ids = []
        po_all_ids = []
        for vendor in vendor_dict:
            if sale_order.so_created:
                po_dict = rec._prepare_purchase_order(sale_order, vendor)
                po_id = self.env['purchase.order'].create(po_dict)
                po_all_ids.append(po_id.id)
                for order_line in vendor_dict[vendor]:
                    if not order_line.is_po_created:
                        if not order_line.product_id.type == 'service' and not order_line.product_id.type == 'consu':
                            raise Warning('Product selected on the sales order line is not types of Service/Consumable so the purchase order can not be created.')
                        elif order_line.product_id.type == 'service' and not order_line.product_id.track_service == 'task':
                            raise Warning('Service Products are not set as track service with create purchase order option.')
                        else:
                            po_line_dict = self._prepare_purchase_order_line(po_id, order_line)
                            po_line_id = self.env['purchase.order.line'].create(po_line_dict)
                            order_ids.append(po_id.id)
                            order_line.is_po_created = True
        result = self.env.ref('purchase.purchase_form_action')
        result = result.read()[0]
        result.update({'domain': [('id', 'in', order_ids)]})
        return result
        
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    is_po_created = fields.Boolean(
        string='Is PO Created',
        copy=False,
    )
    vendor_id = fields.Many2one(
        'res.partner', 
        string="Vendor",
    )
    product_type = fields.Selection(
        related='product_id.type',
        string='Product Type'
    )
    
    @api.multi
    def create_purchase_order_based_vendor(self):
        if self.is_po_created:
            raise Warning('Purchase order has been created already.')
        return self.order_id.create_purchase_order_based_vendor(order_line=self)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
