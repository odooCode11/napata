

from odoo import models, fields, api 


class napataUniversity(models.Model):
    _name = 'na.semester'
    _description = 'Semester name '
    name = fields.Char(string="Semester", required=True)
    academic_id = fields.Many2one('na.acdemic', string='Academic level')



