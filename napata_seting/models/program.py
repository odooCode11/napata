
from odoo import models, fields, api
#

class napataDepartment(models.Model):
    _name = 'na.program'
    _description = ' department name '
    name = fields.Char(string="Programs", required=True,help="enter Name of Department")
    collage_id= fields.Many2one('na.collage',
        ondelete='cascade', string="Collage Name", required=True)
    code=fields.Integer(string="Code" ,required=True)



