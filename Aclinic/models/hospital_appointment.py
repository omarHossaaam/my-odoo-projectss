from odoo import models, fields




class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    name = fields.Char(string="Appointment Reference", required=True, copy=False, readonly=True, default="New")
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    room_id = fields.Many2one('hospital.room', string="Doctor", required=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    reason = fields.Text(string="Reason for Visit")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset_to_draft(self):
        self.state = 'draft'