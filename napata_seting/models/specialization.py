
from odoo import models, fields, api

class napataSpecialization(models.Model):
    _name = 'na.specialization'
    _description = ' Specialization name '
    name = fields.Char(string="Specialization", required=True,help="enter Name of Specialization")
    collage_id= fields.Many2one('na.collage',
        ondelete='cascade', string="Collage ", required=True)
    departmen_id= fields.Many2one('na.depaerment',
        ondelete='cascade', string="Programs", required=True )
    
  


