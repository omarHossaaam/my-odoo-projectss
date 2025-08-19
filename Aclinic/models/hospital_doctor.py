from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Doctor Name', required=True, tracking=True)
    ref = fields.Char(string='Doctor Reference', readonly=True, default='New')
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    user_id = fields.Many2one('res.users', string='Related User')
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    image = fields.Binary(string='Photo', attachment=True)
    note = fields.Text(string='Notes')
    active = fields.Boolean(default=True)
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals.get('ref') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor.ref') or 'DR/0000'
        doctors = super(HospitalDoctor, self).create(vals_list)
        return doctors

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError("Please provide a valid email address for the doctor.")

    def action_open_patients(self):
        self.ensure_one()
        return {
            'name': 'Patients',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'view_mode': 'tree,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
        }