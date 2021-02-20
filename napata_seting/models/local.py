# -*- coding: utf-8 -*-

from odoo import models, fields, api

class  napataLocal(models.Model):
    _name = 'na.locals'
    name = fields.Char(string="Local", required=True)
    state_id= fields.Many2one('na.state',
        ondelete='cascade', string="State", required=True)
    
