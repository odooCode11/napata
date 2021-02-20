import datetime

from odoo import models, fields, api, _


class CreateRegister(models.TransientModel):
    _name = 'create.register'
    _description = "Create User for selected Student(s)"
    managemanent_fees = fields.Many2one(
        'napata.managemanentfees', string='Managemanent Fees')
    student_ids = fields.Many2one(
        'napata.register', string='Student Name')
    other_ids = fields.Many2one(
        'na.feestype', string='Other Expenses')
    appointment_date = fields.Char(string="appointment Date")
    main_desires = fields.Char(string="Main Desires")
    discount = fields.Selection([
        ('10', '10%'),
        ('20', '20%'),
        ('30', '30%'),
        ('40', '40%'), ],
        string="Discount Percentage")
    register_fees = fields.Char(straing='Register Fees')
    the_amount  = fields.Float(straing='the amount')
    inser_amount  = fields.Float(straing='Specified amount')
    total_fees = fields.Float(string="Study Fees")
    other_fees = fields.Float(string="Other Fees")
    card_fees = fields.Float(string="Card Fees")
    firest_installment_fees = fields.Selection([
        ('1', '100%'),
        ('2', '50%'), ],string="First installment")
    certificate_type = fields.Selection([
        ('sudanese', 'Sudanese'),
        ('foreign', 'Foreign'), ],
        string="Nationality")
    syllabus=fields.Selection([('one', 'One'), ('two', 'Two')], 'Syllabus')
    discount_fees= fields.Float(string=" The Discount")
    fina_flees=fields.Float(string="Final Fees")
    total_received = fields.Char(string="Total Received Fees",compute='_get_total_fees')
    # other fees
    reset_correction = fields.Boolean(string="re-correction")
    certificate_correction = fields.Boolean(string="Re-Certificate ")
    degree_holders = fields.Boolean(string="Degree Holders ")
    card_fine = fields.Boolean(string="Card Fine ")
    #



    @api.onchange('student_ids')
    def create_appointment(self):
        filtered_b_ids = self.env['napata.register'].search([('id', '=', self.student_ids.id)])
        if filtered_b_ids:
            self.appointment_date = filtered_b_ids.accept_type
            self.main_desires = filtered_b_ids.main_desires
    @api.onchange('discount')
    def get_discount(self):
        if self.fina_flees > 0.0 :
            self.discount_fees=(self.total_fees*float(self.discount))/100
            self.fina_flees=self.total_fees-(self.total_fees*float(self.discount))/100
        else:
              self.discount_fees=0.0
    
    @api.onchange('certificate_type')
    def get_study_and_regist_fees(self):
        curr_year = datetime.datetime.now().year
        fees = self.env['napata.studyfees'].search([('year', '=', curr_year)])
        if fees:

            # if self.certificate_type:
            for rec in fees:
                if rec.program.name == self.main_desires:

                    if self.certificate_type == 'sudanese':
                        self.total_fees = rec.sudaness_study
                        self.fina_flees = rec.sudaness_study
                        self.register_fees = rec.sdn_register_fees
                        self.card_fees = rec.card_fees_sudan
                    elif self.certificate_type == 'foreign':
                        self.total_fees = rec.foreigners_study
                        self.fina_flees = rec.foreigners_study
                        self.register_fees = rec.foriegn_register_fees
                        self.card_fees = rec.card_fees_foring
                    else:
                        self.total_fees = 0.0
                        self.fina_flees = 0.0
                        self.register_fees = 0.0
    @api.depends('firest_installment_fees')
    def _get_total_fees(self):
        if self.fina_flees:
          for rec in self:
            if int(rec.firest_installment_fees) ==1:
                   self.total_received = float(self.register_fees)+float(rec.fina_flees)
            elif int(rec.firest_installment_fees) ==2:
                self.total_received =float(self.register_fees)+float(rec.fina_flees)/2
        else:
            self.total_received=0.0
    def create_registration(self):
        self.env['napata.accounting'].create({
            'name': self.student_ids.name,
            'first': self.student_ids.first_name,
            'second': self.student_ids.second_name,
            'third': self.student_ids.third_name,
            'last': self.student_ids.forth_name,
            'register_fees': self.register_fees,
            'Study_fees': self.total_fees,
            'fees':self.student_ids.ids[0],
        })