from odoo import models,fields,api
class napataJob(models.Model):
    _name='na.job'
    _description=" the table containt job name " 
    name=fields.Char(string="job",required=True)
    