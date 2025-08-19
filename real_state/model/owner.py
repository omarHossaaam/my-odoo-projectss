from odoo import fields, models


class Owner(models.Model):
    _name = 'owner'
    _description = 'owner'

    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    address = fields.Char()
    city = fields.Char()
    state = fields.Char()
    country = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique'),
        ('email_uniq', 'unique(email)', 'Email must be unique'),
        ('phone_uniq', 'unique(phone)', 'Phone must be unique'),
    ]
