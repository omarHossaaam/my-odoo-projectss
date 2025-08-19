from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HospitalTreatment(models.Model):
        _name = 'hospital.treatment'
        _description = 'Hospital Treatment'

        name = fields.Char(string="Treatment Name", required=True)
        description = fields.Text(string="Description")

        patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
        doctor_id = fields.Many2one('hospital.doctor', string="Doctor")

        treatment_date = fields.Date(string="Treatment Date")
        cost = fields.Float(string="Cost")

        state = fields.Selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
        ], string="Status", default='draft')


        def action_confirm(self):
            for rec in self:
                rec.state = 'confirmed'

        def action_done(self):
            for rec in self:
                rec.state = 'done'
