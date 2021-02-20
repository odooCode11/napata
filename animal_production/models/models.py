# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class States(models.Model):
    _name = 'states'
    _inherit = 'mail.thread'

    name = fields.Char(string='State Name')
    seq1 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    locality_ids = fields.One2many('localities', 'state_id', string='Localities')
    locality_count = fields.Integer('Localities', compute='_get_locality_count')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {}  ".format(rec.name)))
        return result

    @api.depends('locality_ids')
    def _get_locality_count(self):
        self.locality_count = self.env['localities'].search_count([('state_id', '=', self.id)])

    @api.model
    def create(self, vals):
        if vals.get('seq1', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq1'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'state.request') or _('New')
            else:
                vals['seq1'] = self.env['ir.sequence'].next_by_code('state.request') or _('New')

        result = super(States, self).create(vals)
        return result


class Localities(models.Model):
    _name = 'localities'
    _inherit = 'mail.thread'

    state_id = fields.Many2one('states', string='State Name')
    name = fields.Char(string='Locality Name')
    seq2 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {} / {} ".format(rec.state_id.name, rec.name)))
        return result

    @api.model
    def create(self, vals):
        if vals.get('seq2', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq2'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'localities.request') or _('New')
            else:
                vals['seq2'] = self.env['ir.sequence'].next_by_code('localities.request') or _('New')

        result = super(Localities, self).create(vals)
        return result


class Areas(models.Model):
    _name = 'areas'
    _inherit = 'mail.thread'

    locality_id = fields.Many2one('localities', string='Locality Name')
    state_id = fields.Many2one('states', related='locality_id.state_id', string='State Name', store=True)
    seq3 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    name = fields.Char(string='Area Name')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {} / {} / {} ".format(rec.state_id.name, rec.locality_id.name, rec.name)))

        return result

    @api.model
    def create(self, vals):
        if vals.get('seq3', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq3'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'area.request') or _('New')
            else:
                vals['seq3'] = self.env['ir.sequence'].next_by_code('area.request') or _('New')

        result = super(Areas, self).create(vals)
        return result


class Window(models.Model):
    _name = 'window'
    _inherit = 'mail.thread'

    area_id = fields.Many2one('areas', string='Area Name')
    seq4 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    locality_id = fields.Many2one('localities', related='area_id.locality_id', string='Locality Name', store=True)
    state_id = fields.Many2one('states', related='area_id.state_id', string='State Name', store=True)
    name = fields.Char(string='Window Name')
    employee_ids = fields.One2many('employees', 'window_id', string='employees')

    @api.model
    def create(self, vals):
        if vals.get('seq4', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq4'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'window.request') or _('New')
            else:
                vals['seq4'] = self.env['ir.sequence'].next_by_code('window.request') or _('New')

        result = super(Window, self).create(vals)
        return result

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,
                           " {} / {} / {} / {}".format(rec.state_id.name, rec.locality_id.name, rec.area_id.name,
                                                       rec.name)))

        return result


class Departments(models.Model):
    _name = 'departments'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    seq5 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    area_id = fields.Many2one('areas', string='Area Name')
    locality_id = fields.Many2one('localities', related='area_id.locality_id', string='Locality Name', store=True)
    state_id = fields.Many2one('states', related='area_id.state_id', string='State Name', store=True)
    name = fields.Char(string='Departments Name')
    policy_ids = fields.One2many('policies', 'department_id', string='policies')
    condition_ids = fields.One2many('conditions', 'department_id', string='Conditions')
    employee_ids = fields.One2many('employees', 'department_id', string='employees')
    type = fields.Selection([('cuttle_farms', 'Cuttle_Farms'),
                             ('slaughterhouse', 'Slaughterhouse'),
                             ('fodder_factory', 'Fodder_factory'),
                             ('agency', 'Agency'),
                             ('poultry_farms', 'Poultry_Farms'),
                             ('hydromagnetic_center', 'Hydromagnetic_Center')],
                            string='Type', default='cuttle_farms')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id," {} / {} / {} / {}".format(rec.state_id.name, rec.locality_id.name, rec.area_id.name,
                                                       rec.name)))


        return result

    @api.model
    def create(self, vals):
        if vals.get('seq5', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq5'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'department.request') or _('New')
            else:
                vals['seq5'] = self.env['ir.sequence'].next_by_code('department.request') or _('New')

        result = super(Departments, self).create(vals)
        return result


class Policies(models.Model):
    _name = 'policies'
    _inherit = 'mail.thread'

    seq6 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    policy_type = fields.Char(string='Policy Type')
    Policy_Description = fields.Text(string='Policy Description')
    f_date = fields.Date("Stare Date")
    l_date = fields.Date("End Date")
    department_id = fields.Many2one('departments', string='Departments Name')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq6', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq6'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'policies.request') or _('New')
            else:
                vals['seq6'] = self.env['ir.sequence'].next_by_code('policies.request') or _('New')

        result = super(Policies, self).create(vals)
        return result


class Conditions(models.Model):
    _name = 'conditions'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    seq7 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    Condition_Type = fields.Char(string='Condition Type')
    Condition_Description = fields.Text(string='Condition Description')
    f_date = fields.Date(" Condition Stare Date")
    l_date = fields.Date(" Condition End Date")
    department_id = fields.Many2one('departments', string='Departments Name')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq7', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq7'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'policies.request') or _('New')
            else:
                vals['seq7'] = self.env['ir.sequence'].next_by_code('conditions.request') or _('New')

        result = super(Conditions, self).create(vals)
        return result


class Career(models.Model):
    _name = 'career'
    _inherit = 'mail.thread'

    name = fields.Char(string='Career Name')
    seq8 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_ids = fields.One2many('employees', 'career_id', string='employees')

    @api.model
    def create(self, vals):
        if vals.get('seq8', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq8'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'career.request') or _('New')
            else:
                vals['seq8'] = self.env['ir.sequence'].next_by_code('career.request') or _('New')

        result = super(Career, self).create(vals)
        return result


class Employees(models.Model):
    _name = 'employees'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], track_visibility=True, string="State", default='draft')
    name = fields.Char(string='Employees Name', track_visibility=True)
    seq9 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    user_id = fields.Many2one('res.users', string='Related User', track_visibility=True)
    image = fields.Binary(string='Image', track_visibility=True)
    _Phone_number = fields.Char(string='Phone number', track_visibility=True, size=10)
    _gender = fields.Selection([('male', 'Male'),
                                ('female', 'Female')],
                               string='Gander', default='m')
    _address = fields.Char(string='Address', track_visibility=True)
    _Birth_date = fields.Date(string='Birth date', default=fields.Date.today())
    _email = fields.Char(string='Email', track_visibility=True)
    _Personal_prove_type = fields.Selection([('N', 'National Identification'),
                                             ('C', 'National Card'),
                                             ('P', 'Pass Port'),
                                             ('O', 'Other')],
                                            string='Personal Prove Type', default='N')
    _personal_prove_number = fields.Char(string='Personal Prove Number', track_visibility=True, placeholder='123456789')
    _social_state = fields.Selection([
        ('m', 'Married'),
        ('S', 'Single'),
        ('O', 'Other')], track_visibility=True,
        string='Social State', default='m')
    _hire_date = fields.Date(string='Hire date', track_visibility=True)
    department_id = fields.Many2one('departments', track_visibility=True, string='Department Name')
    window_id = fields.Many2one('window', string='Window Name')
    career_id = fields.Many2one('career', track_visibility=True, string='Career Name')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq9', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq9'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'employees.request') or _('New')
            else:
                vals['seq9'] = self.env['ir.sequence'].next_by_code('employees.request') or _('New')

        result = super(Employees, self).create(vals)
        return result


class Applicant(models.Model):
    _name = 'applicant'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    name = fields.Char(string='Applicant Name')
    seq10 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    _Phone_number = fields.Char(string='Phone number', size=10)
    image = fields.Binary(string='Image')
    _gender = fields.Selection([('m', 'Male'),
                                ('f', 'Female')],
                               string='Gander', default='m')
    _address = fields.Char(string='Address')
    _Birth_date = fields.Date(default=fields.Date.today(), string='Birth date')
    _email = fields.Char(string='Email')
    _Personal_prove_type = fields.Selection([('N', 'National Identification'),
                                             ('C', 'National Card'),
                                             ('P', 'Pass Port'),
                                             ('O', 'Other')],
                                            string='Personal Prove Type', default='N')
    _personal_prove_number = fields.Char(string='Personal Prove Number')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq10', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq10'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'applicant.request') or _('New')
            else:
                vals['seq10'] = self.env['ir.sequence'].next_by_code('applicant.request') or _('New')

        result = super(Applicant, self).create(vals)
        return result

    def action_order(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'orders',
            'target': 'new',
            'context': {
                'default_Applicant_id': self.id,
                'create': False,
            }
        }


class Orders(models.Model):
    _name = 'orders'
    _inherit = 'mail.thread'
    _rec_name = 'Order_date'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('reject', 'Rejected')], string="State",
                             default='draft')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    visit_id = fields.Many2one('visits', string='Visits')

    order_type = fields.Selection([('I', 'Initial Order Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re Permission')],
                                  string='Order Type', default='I')
    Order_date = fields.Date(string='Order date', default=date.today(), store=True)
    recommend_date = fields.Date(string='Recommendation Date', )
    Applicant_id = fields.Many2one('applicant', string='Applicant Name')
    department_id = fields.Many2one('departments', string='Department Name')
    window_id = fields.Many2one('window', string='Window Name')

    state_id = fields.Many2one('states', compute='_get_location', store=True)
    locality_id = fields.Many2one('localities', compute='_get_location', store=True)
    area_id = fields.Many2one('areas', compute='_get_location', store=True)

    @api.depends('window_id')
    def _get_location(self):
        for rec in self:
            rec.state_id = False
            rec.locality_id = False
            rec.area_id = False
            rec.state_id = rec.window_id.state_id
            rec.locality_id = rec.window_id.locality_id
            rec.area_id = rec.window_id.area_id

    # def action_confirm(self):
    #     self.state = 'confirm'
    #
    # def action_draft(self):
    #     self.state = 'draft'

    def name_get(self):
        result = []
        order = ''
        for rec in self:
            if rec.order_type == 'I':
                order = 'طلب زيارة مبدئية'
            elif rec.order_type == 'p':
                order = 'طلب تصديق'
            else:
                order = 'طلب تجديد تصديق'
            result.append((rec.id, " {} / {} / {}".format(rec.name, rec.Applicant_id.name, order)))
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'order.request') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('order.request') or _('New')

        result = super(Orders, self).create(vals)
        return result

    def action_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'visits',
            'target': 'new',
            'context': {
                'default_Order_id': self.id,
                'default_order_type': self.order_type,
                'department_id': self.department_id,
                'create': False,
            }
        }


class Visits(models.Model):
    _name = 'visits'
    _inherit = 'mail.thread'
    _rec_name = 'visit_date'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    seq11 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    visit_type = fields.Selection([('I', 'Initial Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re Permission')],
                                  string='Visit Type', related="Order_id.order_type", store=True)
    visit_date = fields.Date(string='Visit date', default=fields.Date.today(), store=True)
    Order_id = fields.Many2one('orders', string="Order")
    order_type = fields.Selection([('I', 'Initial Order Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re_Permission')],
                                  string='Order Type', related="Order_id.order_type")
    Order_date = fields.Date(string='Date', related='Order_id.Order_date')
    employee_id = fields.Many2one('employees', string='Employee Name', store=True)
    land_id = fields.Many2one('lands', string="Certificate Number")
    department_id = fields.Many2one('departments', related='Order_id.department_id', string='Department Name')
    type = fields.Selection(related='department_id.type', string='Type', readonly=False, store=True)
    recommend_id = fields.Many2one('recommendation', string='Recommendations')
    water_source = fields.Selection([('G', 'General Water Source'),
                                     ('W', 'Well'),
                                     ('N', 'Non')],
                                    string='Water Source', default='G')
    water_amount = fields.Selection([('E', 'Enough'),
                                     ('N', 'UnSufficient')],
                                    string='Water Amount', default='E')
    power_source = fields.Selection([('GE', 'General Electricity'),
                                     ('G', 'Generator'),
                                     ('O', 'Other')],
                                    string='Power Source', default='GE')
    inner_distribution_of_light = fields.Selection([('E', 'Enough'),
                                                    ('N', 'UnSufficient')],
                                                   string='Inner Lighting', default='E')
    ventilation_state = fields.Selection([('G', 'Good'),
                                          ('N', 'Not_Good')],
                                         string='ventilation State', default='G')
    temp_degree = fields.Selection([('H', 'High'),
                                    ('M', 'Medium'),
                                    ('L', 'Low')],
                                   string='Temperature', default='H')
    room_coll = fields.Selection([('E', 'Existed'),
                                  ('NE', 'Non_Existent')],
                                 string='Room Colling', default='E')
    conditioners = fields.Selection([('E', 'Existed'),
                                     ('NE', 'Non Existent')],
                                    string='Conditioners', default='E')
    sufficient_Colling = fields.Selection([('G', 'Good'),
                                           ('NE', 'Non Good')],
                                          string='Sufficient Colling', default='G')
    sew_state = fields.Selection([('G', 'Good'),
                                  ('N', 'Not Good')],
                                 string='Sewerage State', default='G')
    sew_used_water = fields.Selection([('G', 'Good'),
                                       ('N', 'Not Good')],
                                      string='Water Drainage used', default='G')
    outer_Clearing = fields.Selection([('G', 'Good'),
                                       ('NE', 'Non Good')],
                                      string='Outer Clearing', default='G')
    inner_Clearing = fields.Selection([('G', 'Good'),
                                       ('NE', 'Non Good')],
                                      string='Inner Clearing', default='G')
    mop_up_Dry_Offal = fields.Selection([('G', 'Good'),
                                         ('NE', 'Non Good')],
                                        string='Mop up  Dry Offal', default='G')
    mop_up_Used_Offal = fields.Selection([('G', 'Good'),
                                          ('NE', 'Non Good')],
                                         string='Mop up  used Offal', default='G')
    medical_Detect = fields.Selection([('D', 'Done For All'),
                                       ('DF', 'Done For Some'),
                                       ('N', 'Did Not')],
                                      string='Medical Detection', default='D')
    general_Shape = fields.Selection([('G', 'Acceptable'),
                                      ('NE', 'Need Improvement')],
                                     string='General Shape', default='G')
    building_state = fields.Selection([('G', 'Good'),
                                       ('N', 'Not Good')],
                                      string='Building State', default='G')
    building_space = fields.Selection([('S', 'Suitable'),
                                       ('N', 'Non Suitable')],
                                      string='Building Space', default='S')
    silos = fields.Selection([('S', 'Existent'),
                              ('N', 'Non Existed')],
                             string='Silos', default='S')
    worker_residence = fields.Selection([('S', 'Existent'),
                                         ('N', 'Non Existed')],
                                        string='Worker Residence', default='S')
    feed_stock = fields.Selection([('S', 'Existent'),
                                   ('N', 'Non Existed')],
                                  string='Feed Stock', default='S')
    sanitation_building = fields.Selection([('S', 'Existent'),
                                            ('N', 'Non Existed')],
                                           string='Sanitation Building', default='S')
    lap = fields.Selection([('S', 'Existent'),
                            ('N', 'Non Existed')],
                           string='Lap', default='S')
    mills = fields.Selection([('S', 'Existent'),
                              ('N', 'Non Existed')],
                             string='Mills', default='S')
    mixers = fields.Selection([('S', 'Existent'),
                               ('N', 'Non Existed')],
                              string='Mixers', default='S')
    forage_analyzers = fields.Selection([('S', 'Existent'),
                                         ('N', 'Non Existed')],
                                        string='Forage Analyzers', default='S')
    feed_presses = fields.Selection([('S', 'Existent'),
                                     ('N', 'Non Existed')],
                                    string='Feed Presses', default='S')
    build_state = fields.Selection([('G', 'Good'),
                                    ('N', 'Not Good')],
                                   string='Building State', default='G')
    external_fence = fields.Selection([('E', 'Existent'),
                                       ('N', 'Not Existed')],
                                      string='External Fence', default='E')
    hanger = fields.Selection([('E', 'Existent'),
                               ('NE', 'Not Existed')],
                              string='Hanger', default='E')
    worker_residences = fields.Selection([('E', 'Existent'),
                                          ('N', 'Not Existed')],
                                         string='Worker Residence', default='E')
    feed_stocks = fields.Selection([('E', 'Existent'),
                                    ('N', 'Not Existent')],
                                   string='Feed Stocks', default='E')
    product_stock = fields.Selection([('E', 'Existent'),
                                      ('N', 'Not Existed')],
                                     string='Products Stock', default='E')
    feed_source = fields.Selection([('I', 'Internal'),
                                    ('E', 'External')],
                                   string='Feed Source', default='E')
    stock_Space = fields.Selection([('E', 'Enough'),
                                    ('NE', 'Not Enough')],
                                   string='Stocks Space', default='E')
    sanitation = fields.Selection([('G', 'General'),
                                   ('N', 'Private')],
                                  string='Sanitation', default='G')
    mop_up_Offal = fields.Selection([('G', 'Conformity'),
                                     ('N', 'UnConformity')],
                                    string='Mop Up Offal', default='G')
    basin_purge = fields.Selection([('E', 'Existent'),
                                    ('NE', 'Not Existed')],
                                   string='Basin Purge', default='E')
    basin_number = fields.Selection([('E', 'Enough'),
                                     ('U', 'UnSufficient')],
                                    string='Basin Number', default='E')
    basin_dimension = fields.Selection([('S', 'Suitable'),
                                        ('U', 'UnSuitable')],
                                       string='Basin Dimension', default='S')
    slaughter_house = fields.Selection([('E', 'Existent'),
                                        ('N', 'Not Existent')],
                                       string='Slaughtering House', default='E')
    mop_up_liquid_substances = fields.Selection([('C', 'Conformity'),
                                                 ('U', 'UnConformity')],
                                                string='mop up Liquid Substances', default='C')
    holocaust = fields.Selection([('M', 'Modern'),
                                  ('T', 'Traditional'),
                                  ('M', 'Movable'),
                                  ('P', 'Pit')],
                                 string='Holocaust', default='M')
    water_Circulation = fields.Selection([('M', 'Modern'),
                                          ('T', 'Traditional')],
                                         string='Holocaust', default='M')
    Hanger_Number = fields.Selection((('S', 'Sufficient'),
                                      ('N', 'Not Sufficient')),
                                     string='Hanger Number', default='S')
    Hanger_Space = fields.Selection((('S', 'Suitable'),
                                     ('N', 'Not Suitable')),
                                    string='Hanger Space', default='S')
    Floor = fields.Selection((('S', 'Suitable'),
                              ('NE', 'Not Suitable')),
                             string='Grown', default='S')
    Hanger_Capacity = fields.Selection((('E', 'Enough'),
                                        ('N', 'UnSufficient')),
                                       string='Hanger Space', default='E')
    shadow_Roof = fields.Selection((('G', 'Good'),
                                    ('N', 'Not Good')),
                                   string='Shadow And Roof', default='G')
    build_states = fields.Selection([('G', 'Good'),
                                     ('N', 'Not Good')],
                                    string='Building State', default='G')
    external_Fence = fields.Selection([('E', 'Existent'),
                                       ('NE', 'Not Existed')],
                                      string='External Fence', default='E')
    hanger_wait = fields.Selection([('E', 'Existent'),
                                    ('NE', 'Not Existed')],
                                   string='Hanger', default='E')
    viscera_offal_room = fields.Selection([('G', 'Good'),
                                           ('N', 'Not Good')],
                                          string='Viscera Offal Room', default='G')
    wall_grown = fields.Selection([('G', 'Good'),
                                   ('N', 'Not Good')],
                                  string='Walls And grown Sacrifice hull', default='G')
    check_lap = fields.Selection([('E', 'Existent'),
                                  ('NE', 'Not Existed')],
                                 string='Check Lap', default='E')
    water_circulation = fields.Selection([('E', 'Existent'),
                                          ('NE', 'Not Existed')],
                                         string='Water Circulation', default='E')
    general_State = fields.Selection([('C', 'Clean'),
                                      ('N', 'Not Clean')],
                                     string='General State For Machine', default='C')
    Special_knife = fields.Selection([('C', 'Conformable'),
                                      ('N', 'Not Conformable')],
                                     string='Knife', default='C')
    hanger_waiting_Space = fields.Selection((('S', 'Suitable'),
                                             ('N', 'Not Suitable')),
                                            string='Hanger Waiting Space', default='S')
    offal_cleaning = fields.Selection((('A', 'Acceptable'),
                                       ('N', 'Not Acceptable')),
                                      string='Innards Cleaning', default='A')
    offal_treatment = fields.Selection((('E', 'Acceptable'),
                                        ('N', 'Not Acceptable')),
                                       string='Offal Treatment', default='E')
    dispose_death = fields.Selection((('B', 'Burn'),
                                      ('BB', 'Burn And Bury')),
                                     string='Dispose Death', default='B')
    record_stamp = fields.Selection((('E', 'Existent'),
                                     ('N', 'Not Existent')),
                                    string='Records And Stamp', default='E')
    skin_room = fields.Selection((('A', 'Acceptable'),
                                  ('N', 'Not Acceptable')),
                                 string='Skin Rooms', default='A')
    strip = fields.Selection((('E', 'Existent'),
                              ('N', 'Not Existent')),
                             string='Strip', default='E')
    strip_number = fields.Selection((('T', 'Trainer'),
                                     ('N', 'Not Trainer')),
                                    string='Strip Number', default='T')
    skins_keeping = fields.Selection((('E', 'Enough'),
                                      ('N', 'Not Enough')),
                                     string='Skin Keeping', default='E')
    inflection = fields.Selection([('G', 'Good'),
                                   ('N', 'Not Good')],
                                  string='Hanger Waiting Space', default='G')
    wash_dash = fields.Selection([('E', 'Exist'),
                                  ('N', 'Not Exist')],
                                 string='Wash Dash', default='E')
    area_space = fields.Selection([('E', 'Enough'),
                                   ('N', 'Not Enough')],
                                  string='Area Space', default='E')
    stores = fields.Selection([('E', 'Exist'),
                               ('N', 'Not Exist')],
                              string='Stores', default='E')
    stores_space = fields.Selection([('E', 'Enough'),
                                     ('N', 'Not Enough')],
                                    string='Stores Space', default='E')
    halls = fields.Selection([('E', 'Exist'),
                              ('N', 'Not Exist')],
                             string='Halls', default='E')
    halls_space = fields.Selection([('E', 'Enough'),
                                    ('N', 'Not Enough')],
                                   string='Halls Space', default='E')
    grown = fields.Selection([('S', 'Suitable'),
                              ('N', 'Not Suitable')],
                             string='Grown', default='S')
    building_State = fields.Selection([('G', 'Good'),
                                       ('N', 'Not Good')],
                                      string='Building', default='G')
    batch_machine = fields.Selection([('S', 'Exist'),
                                      ('N', 'Not Exist')],
                                     string='Batch Machine', default='S')
    skin_weigher = fields.Selection([('S', 'Exist'),
                                     ('N', 'Non Exist')],
                                    string='Skin Weigher', default='S')
    dryer_tables = fields.Selection([('S', 'Exist'),
                                     ('N', 'Non Exist')],
                                    string='Dryer Tables', default='S')
    big_barrels = fields.Selection([('S', 'Exist'),
                                    ('N', 'Non Exist')],
                                   string='Big Barrels', default='S')
    waiter_dashes = fields.Selection([('S', 'Exist'),
                                      ('N', 'Non Exist')],
                                     string='Waiter Dashes', default='S')

    state_id = fields.Many2one('states', compute='_get_location', store=True)
    locality_id = fields.Many2one('localities', compute='_get_location', store=True)
    area_id = fields.Many2one('areas', compute='_get_location', store=True)

    @api.depends('Order_id')
    def _get_location(self):
        for rec in self:
            rec.state_id = False
            rec.locality_id = False
            rec.area_id = False
            rec.state_id = rec.Order_id.window_id.state_id
            rec.locality_id = rec.Order_id.window_id.locality_id
            rec.area_id = rec.Order_id.window_id.area_id

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.onchange('Order_id')
    def _get_orders(self):
        order = []

        res = self.env['orders'].search([('visit_id', '=', False)])
        if res:
            for rec in res:
                order.append(rec.id)

        return {'domain': {'Order_id': [('id', 'in', order)]}}



    @api.onchange('Order_id')
    def _get_land(self):
        lands = []
        res = ()
        self.land_id = False
        if self.order_type == 'I':
            res = self.env['lands'].search([('state', '=', 'draft')])
        elif self.order_type == 'p':
            res = self.env['lands'].search([('state', '=', 'register')])
        elif self.order_type == 'O':
            res = self.env['lands'].search([('state', '=', 'confirm')])
        if res:
            for rec in res:
                lands.append(rec.id)

        return {'domain': {'land_id': [('id', 'in', lands)]}}

    
    @api.constrains('visit_date')
    def _check_date(self):
        if self.visit_date:
            if self.visit_date < self.Order_date:
                raise ValidationError(_("visit date must be grater than or equal to order date."))

    @api.model
    def create(self, vals):
        if vals.get('seq11', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq11'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'visit.request') or _('New')
            else:
                vals['seq11'] = self.env['ir.sequence'].next_by_code('visit.request') or _('New')

        result = super(Visits, self).create(vals)
        result.Order_id.visit_id = result.id
        return result

    def name_get(self):
        result = []
        visit = ''
        for rec in self:
            if rec.visit_type == 'I':
                visit = 'زيارة مبدئية'
            elif rec.visit_type == 'p':
                visit = 'زيارة تصديق'
            else:
                visit = 'زيارة تجديد تصديق'
            result.append((rec.id, " {} / {} ".format(rec.seq11, visit)))
        return result

    def action_recommend(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'recommendation',
            'target': 'new',
            'context': {
                'default_visit_id': self.id,
                'default_order_type': self.order_type,
                'default_employee_id': self.employee_id.id,
                'default_land_id': self.land_id.id,
                'create': False,
            }
        }


class Lands(models.Model):
    _name = 'lands'
    _inherit = 'mail.thread'

    state = fields.Selection(
        [('draft', 'Draft'), ('register', 'Registered'), ('confirm', 'مصدقة'), ('cancel', 'Canceled')],
        default='draft', string='State')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    ownership_type = fields.Selection([('Private', 'Private'),
                                       ('governmental', 'Governmental'),
                                       ('Others', 'Others')],
                                      string='Ownership Type', default='Private')
    search_certificate_id = fields.Char(string='Certificate Number')
    search_certificate_date = fields.Date(string='Certificate Date', default=date.today(), store=True)
    land_type = fields.Selection([('S', 'Sand Bank'),
                                  ('P', 'Petrographic'),
                                  ('M', 'Muddy')],
                                 string='Land Type', default='S')
    lands_space = fields.Char(string='Space')
    e_direction = fields.Char(string='Direction E')
    n_direction = fields.Char(string='Direction N')
    distance = fields.Char(string='Distance From Building')
    visit_id = fields.Many2one('visits', string='Visit')

    def name_get(self):
        result = []
        name = ''
        for rec in self:
            if rec.ownership_type == 'Private':
                name = 'خاص'
            elif rec.ownership_type == 'governmental':
                name = 'حكومي'
            else:
                name = 'أخرى'
            result.append((rec.id, " {} / {} ".format(name, rec.search_certificate_id)))
        return result

    def action_register(self):
        self.state = 'register'

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'lands.request') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('lands.request') or _('New')

        result = super(Lands, self).create(vals)
        return result


class Recommendation(models.Model):
    _name = 'recommendation'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('reject', 'Rejected')], string="State",
                             default='draft')
    seq12 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    visit_id = fields.Many2one('visits', string='visit')
    per_id = fields.Many2one('permission', string='permission')
    recommend_type = fields.Selection([('initial_recommendation', 'Initial Recommendation'),
                                       ('permission_recommendation', 'Permission Recommendation'),
                                       ('re_permission recommendation', 'Re_Permission Recommendation')],
                                      compute='_get_recommend_type', string='Recommendation Type',  store=True)
    recommend_date = fields.Date(string='Recommendation Date', default=date.today(), store=True)
    recommendation_text = fields.Text(string='Recommendation Text')
    land_id = fields.Many2one('lands', related="visit_id.land_id", store=True)
    order_type = fields.Selection([('I', 'Initial Order Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re_Permission')],
                                  string='Order Type', related="visit_id.order_type")
    employee_id = fields.Many2one('employees', related="visit_id.employee_id", store=True)
    emp_id = fields.Many2one('employees', string='Accredited')

    @api.depends('visit_id')
    def _get_recommend_type(self):
        if self.visit_id.visit_type == 'I':
            self.recommend_type = 'initial_recommendation'
        elif self.visit_id.visit_type == 'p':
            self.recommend_type = 'permission_recommendation'
        else:
            self.recommend_type = 're_permission recommendation'

    def action_confirm(self):
        self.state = 'confirm'
        self.visit_id.Order_id.state = 'confirm'
        self.visit_id.land_id.state = 'register'
        self.emp_id = self.env['employees'].search([('user_id', '=', self.env.user.id)], limit=1)

    def action_reject(self):
        self.emp_id = self.env['employees'].search([('user_id', '=', self.env.user.id)], limit=1)
        self.state = 'reject'
        self.visit_id.Order_id.state = 'reject'
        self.visit_id.land_id.state = 'cancel'

    def action_draft(self):
        self.emp_id = False
        self.state = 'draft'
        self.visit_id.Order_id.state = 'draft'
        self.visit_id.land_id.state = 'draft'

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {} / {} ".format(rec.seq12, rec.recommend_type)))
        return result

    @api.model
    def create(self, vals):
        if vals.get('seq12', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq12'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'recommendation.request') or _('New')
            else:
                vals['seq12'] = self.env['ir.sequence'].next_by_code('recommendation.request') or _('New')

        result = super(Recommendation, self).create(vals)
        result.visit_id.recommend_id = result.id
        return result

    @api.onchange('visit_id')
    def _get_visit(self):
        visits = []

        res = self.env['visits'].search([('recommend_id', '=', False)])
        if res:
            for rec in res:
                visits.append(rec.id)

        return {'domain': {'visit_id': [('id', 'in', visits)]}}

    def action_permission(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'permission',
            'target': 'new',
            'context': {
                'default_recommend_id': self.id,
                'default_order_type': self.order_type,
                'default_recommend_date': self.recommend_date,
                'default_employee_id': self.employee_id.id,
                'create': False,
            }
        }

    def name_get(self):
        result = []
        recommend = ''
        for rec in self:
            if rec.order_type == 'I':
                recommend = 'Initial Recommendation'
            elif rec.order_type == 'p':
                recommend = 'Permission Recommendation'
            else:
                recommend = 'Re Permission Recommendation'
            result.append((rec.id, " {} / {} ".format(rec.seq12, recommend)))
        return result


#
class Permission(models.Model):
    _name = 'permission'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    recommend_id = fields.Many2one('recommendation', string='Recommendations')
    seq13 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    permission_Type = fields.Selection([('N', 'New Permission'),
                                        ('R', 'Renew Permission')],
                                       string='Permission Type')
    Start_date = fields.Date(string='Stare Date', default=date.today(), store=True)
    end_date = fields.Date(string='End Date')
    employee_id = fields.Many2one('employees', related="recommend_id.employee_id", store=True)
    fess = fields.Integer("Fess")
    order_type = fields.Selection([('I', 'Initial Order Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re_Permission')],
                                  string='Order Type', related="recommend_id.order_type")
    recommend_date = fields.Date(string='Date', related='recommend_id.recommend_date')
    pro_id = fields.Many2one('projects', string='project')
    state_id = fields.Many2one('states', compute='_get_location', store=True)
    locality_id = fields.Many2one('localities', compute='_get_location', store=True)
    area_id = fields.Many2one('areas', compute='_get_location', store=True)
    department_id = fields.Many2one('departments', compute='_get_location', store=True)

    @api.onchange('recommend_id')
    def _get_recommendation(self):
        recommendations = []

        res = self.env['recommendation'].search([('state', '=', 'confirm')])
        if res:
            for rec in res:
                recommendations.append(rec.id)

        return {'domain': {'recommend_id': [('id', 'in', recommendations)]}}

    @api.depends('recommend_id')
    def _get_location(self):
        for rec in self:
            rec.state_id = False
            rec.locality_id = False
            rec.area_id = False
            rec.department_id = False
            rec.state_id = rec.recommend_id.visit_id.Order_id.window_id.state_id
            rec.locality_id = rec.recommend_id.visit_id.Order_id.window_id.locality_id
            rec.area_id = rec.recommend_id.visit_id.Order_id.window_id.area_id
            rec.department_id = rec.recommend_id.visit_id.department_id

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq13', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq13'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'permission.request') or _('New')
            else:
                vals['seq13'] = self.env['ir.sequence'].next_by_code('permission.request') or _('New')

        result = super(Permission, self).create(vals)
        result.recommend_id.per_id = result.id
        return result

    def action_project(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'projects',
            'target': 'new',
            'context': {
                'default_per_id': self.id,
                'create': False,
            }
        }

    def name_get(self):
        result = []
        permission = ''
        for rec in self:
            if rec.permission_Type == 'N':
                permission = 'New Permission'

            else:
                permission = 'Renew Permission'
            result.append((rec.id, " {} / {} ".format(rec.seq13, permission)))
        return result


class ProjectType(models.Model):
    _name = 'project_type'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    seq14 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    TYPE = [('poultry farm', 'Poultry Farm'),
            ('domestic farm', 'Domestic Farm'),
            ('fodder factory', 'Fodder Factory'),
            ('slaughterhouse', 'Slaughterhouse'),
            ('agency', 'Agency'),
            ('hydromagnetic center', 'Hydromagnetic Center')]

    project_type = fields.Selection(TYPE, string='Project Type')
    project_ids = fields.One2many('projects', 'project_type_id', string='projects')

    @api.model
    def create(self, vals):
        if vals.get('seq14', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq14'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'projectType.request') or _('New')
            else:
                vals['seq14'] = self.env['ir.sequence'].next_by_code('projectType.request') or _('New')

        result = super(ProjectType, self).create(vals)
        return result

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

   
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {} ".format(rec.project_type)))
        return result


class Projects(models.Model):
    _name = 'projects'
    _inherit = 'mail.thread'

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    seq15 = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    per_id = fields.Many2one('permission', string='Permission')
    project_name = fields.Char(string='Project Name')
    project_type_id = fields.Many2one('project_type', string='Project Type')

    state_id = fields.Many2one('states', compute='_get_location', store=True)
    locality_id = fields.Many2one('localities', compute='_get_location', store=True)
    area_id = fields.Many2one('areas', compute='_get_location', store=True)
    department_id = fields.Many2one('departments', compute='_get_location', store=True)
    Start_date = fields.Date(string='Start Date', related='per_id.Start_date')
    end_date = fields.Date(string='End Date', related='per_id.end_date')

    @api.depends('per_id')
    def _get_location(self):
        for rec in self:
            rec.state_id = False
            rec.locality_id = False
            rec.area_id = False
            rec.department_id = False
            rec.state_id = rec.per_id.recommend_id.visit_id.Order_id.window_id.state_id
            rec.locality_id = rec.per_id.recommend_id.visit_id.Order_id.window_id.locality_id
            rec.area_id = rec.per_id.recommend_id.visit_id.Order_id.window_id.area_id
            rec.department_id = rec.per_id.recommend_id.visit_id.department_id

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('seq15', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['seq15'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'projects.request') or _('New')
            else:
                vals['seq15'] = self.env['ir.sequence'].next_by_code('projects.request') or _('New')

        result = super(Projects, self).create(vals)
        result.per_id.pro_id = result.id
        return result

    @api.onchange('per_id')
    def _get_permission(self):
        permissions = []

        res = self.env['permission'].search([('pro_id', '=', False)])
        if res:
            for rec in res:
                permissions.append(rec.id)

        return {'domain': {'per_id': [('id', 'in', permissions)]}}

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, " {} ".format(rec.seq15)))
        return result
