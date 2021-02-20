
from odoo import models, fields


class CreatePresntaion(models.TransientModel):
    _name = 'create.presntaion'
    _description = "Create User for selected Student"
    name = fields.Char(string="Name")
    mis=fields.Date(string="appointment Date")

    # def create_appointment(self):
    #     vals={'patient_id':self.patient_ids.id,
    #            'appointment_date':self.appointment_date}
    #     self.env['clinic.appointment'].create(vals)

