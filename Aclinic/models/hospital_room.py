from odoo import models, fields



class HospitalRoom(models.Model):
    _name = "hospital.room"
    _description = "Hospital Room"

    name = fields.Char(string="Room Number/Name", required=True)
    room_type = fields.Selection([
        ('general', 'General Ward'),
        ('semi_private', 'Semi-Private'),
        ('private', 'Private'),
        ('icu', 'ICU'),
        ('operation', 'Operation Theatre'),
    ], string="Room Type", required=True)
    capacity = fields.Integer(string="Capacity", default=1)
    occupied_beds = fields.Integer(string="Occupied Beds", compute="_compute_occupied_beds", store=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string="Status", default="available")
    notes = fields.Text(string="Notes")

    appointment_ids = fields.One2many('hospital.appointment', 'room_id', string="Appointments")

    def _compute_occupied_beds(self):
        for record in self:
            record.occupied_beds = len(record.appointment_ids)