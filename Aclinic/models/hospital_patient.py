from odoo import fields, models, api
from odoo.exceptions import ValidationError



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(required=True, default='New', size=30)
    name = fields.Char(required=True, tracking=True)
    age = fields.Integer()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], tracking=True)
    admission_date = fields.Date(default=fields.Date.today)
    discharge_date = fields.Date()
    estimated_bill = fields.Float(digits=(6, 2), tracking=True)
    treatment_cost = fields.Float(tracking=True)
    diff = fields.Float(compute='_compute_diff', store=True, readonly=True)
    diagnosis = fields.Text()
    doctor_id = fields.Many2one('hospital.doctor', string='Assigned Doctor')
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('under_treatment', 'Under Treatment'),
        ('discharged', 'Discharged'),
        ('deceased', 'Deceased'),
    ], default='admitted', tracking=True)
    treatment_ids = fields.One2many('hospital.treatment', 'patient_id', string='Treatments')

    customer_id = fields.Many2one('res.partner', string="Billing Partner")
    invoice_id = fields.Many2one('account.move', string="Invoice")

    @api.depends('estimated_bill', 'treatment_cost')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.estimated_bill - rec.treatment_cost

    def action_create_invoice(self):
        for record in self:
            if not record.customer_id:
                raise ValidationError("Please set a billing partner before creating invoice.")

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                   'name': f"Treatment for {record.name}",
                   'quantity': 1,
                   'price_unit': record.treatment_cost,
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