from odoo import fields, models


class TodoTask(models.Model):
    _name = "todo.task"

    name = fields.Char("Task Name")
    due_date = fields.Date()
    description = fields.Text()
    assign_to_do = fields.Many2one("res.partner", string="Assigned To")
    state = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "in_progress"),
            ("completed", "Completed"),
        ]
    )
