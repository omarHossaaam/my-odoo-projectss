from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Existing fields
    ref = fields.Char(required=True, default='New', size=30)
    reff = fields.Char(default='new', readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(tracking=True)
    expected_price = fields.Float(digits=(6, 2))
    selling_price = fields.Float(tracking=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    diff = fields.Float(compute='_compute_diff', store=True, readonly=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    photo_id = fields.Many2one('ir.attachment', string='Photo')
    image = fields.Binary(string='Property Image', attachment=True)

    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation")

    owner_id = fields.Many2one('owner', string='Owner')
    tag_ids = fields.Many2many('tag', string='Tags')
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')
    line_ids = fields.One2many('property.line', 'property_id', string='Lines')
    active = fields.Boolean(default=True)

    #
    customer_id = fields.Many2one('res.partner', string="Customer")
    invoice_id = fields.Many2one('account.move', string="Invoice")
    price = fields.Float(string="Price")
    product_id = fields.Many2one('product.product', string="Product")
    ref = fields.Char(string='Reference')

    def property_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/property/excel/report',
        }

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for record in self:
            record.diff = record.expected_price - record.selling_price

    @api.onchange('expected_price', 'selling_price')
    def _onchange_diff(self):
        for record in self:
            record.diff = record.expected_price - record.selling_price
            if record.diff < 0:
                record.diff = 0
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'The diff has been updated.'
                    }
                }

    _sql_constraints = [
        ('unique_ref', 'unique(ref)', 'This reference already exists')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_than_zero(self):
        for property in self:
            if property.bedrooms == 0:
                raise ValidationError('Please add number of bedrooms!')

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        res.product_id = self.env["product.product"].create({"name": res.ref})

        for vals in vals:

            if not vals.get('ref') or vals['ref'] == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('property.ref')
        records = super(Property, self).create(vals)
        for record in records:
            product = self.env["product.product"].create({
                "name": record.ref,
                "list_price": record.price or 0.0,
                "type": "service",
            })
            record.product_id = product.id
            record.product_id = self.env['product.product'].create({"name": record.ref})
        return res, records

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print('inside search method')
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        print('inside write method')
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print('inside unlink method')
        return res

    def action_sold(self):
        for record in self:
            print("inside sold method")
            record.state = 'sold'

    def action_closed(self):
        for record in self:
            print("inside closed method")
            record.state = 'closed'

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_state.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_state.owner_action')
        view_id = self.env.ref('real_state.view_owner_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    # new
    def action_create_invoice(self):
        for record in self:
            if not record.customer_id:
                raise ValidationError("Please set a customer before creating invoice.")

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'ref': record.ref,
                    'quantity': 1,
                    'price_unit': record.selling_price,
                    'product_id': record.product_id.id,
                })]
            }
            invoice = self.env['account.move'].create(invoice_vals)
            record.invoice_id = invoice.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
            }

    def action_create_sale_order(self):

        if not self:
            raise ValidationError("Please select at least one property to create a sales order.")

        # Get or create the product
        product = self.env['product.product'].search([('name', '=', 'Property Sale')], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': 'Property Sale',
                'type': 'service',
                'list_price': 0.0,
                'standard_price': 0.0,
                'detailed_type': 'service',
            })

        sale_orders = self.env['sale.order']
        for prop in self:
            if not prop.owner_id:
                raise ValidationError(f"Property {prop.name} has no owner set!")

            # Create the sale order
            sale_order = self.env['sale.order'].create({
                'partner_id': prop.owner_id.id,
                'origin': prop.name,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'name': f"Property: {prop.name or ''}",
                    'product_uom_qty': 1.0,
                    'price_unit': prop.selling_price or 0.0,
                })]
            })

            # Confirm the sale order so invoices can be generated
            sale_order.action_confirm()
            sale_orders += sale_order

        # Open the first created sale order in form view
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': sale_orders[0].id
        }


class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line'
    property_id = fields.Many2one('property', string='Property')
    area = fields.Float()
    description = fields.Char()
