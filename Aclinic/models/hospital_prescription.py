from odoo import models, fields


class HospitalPrescription(models.Model):
    _name = "hospital.prescription"
    _description = "Hospital Prescription"

    name = fields.Char(string="Prescription Reference", required=True, copy=False, default="New")
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    treatment_id = fields.Many2one("hospital.treatment", string="Treatment")
    date = fields.Date(string="Prescription Date", default=fields.Date.context_today)
    notes = fields.Text(string="Notes")
    medicine_line_ids = fields.One2many("hospital.prescription.line", "prescription_id", string="Medicines")
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("done", "Done"),
    ], default="draft", string="Status")

    def action_confirm(self):
        self.state = "confirmed"

    def action_done(self):
        self.state = "done"

    def action_reset_to_draft(self):
        self.state = "draft"


class HospitalPrescriptionLine(models.Model):
    _name = "hospital.prescription.line"
    _description = "Hospital Prescription Line"

    prescription_id = fields.Many2one("hospital.prescription", string="Prescription", required=True, ondelete="cascade")
    medicine_name = fields.Char(string="Medicine", required=True)
    dosage = fields.Char(string="Dosage")
    duration = fields.Char(string="Duration")
    instructions = fields.Text(string="Instructions")
