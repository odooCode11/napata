# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, exceptions


class napataRegister(models.Model):
    _name = 'napata.register'
    _inherit = ['mail.thread']

    name = fields.Char(string="student's name", readonly=True)
    # get student name
    first_name = fields.Char(string='First Name')
    second_name = fields.Char(string='Second Name')
    third_name = fields.Char(string='Third Name')
    forth_name = fields.Char(string='Fourth Name')
    nationality=fields.Char(string="Nationality")
    type_id=fields.Char(string="Type of identification")
    number_ids=fields.Char(string="identification Number")
    phone1 = fields.Integer(string=" Phone Number")
    phone2 = fields.Integer(string="WatsApp")
    # Parent info
    provider_name = fields.Char(string="Applicant Name")
    job = fields.Char(string="job")
    parent = fields.Char(string="parent")
    phone3 = fields.Integer(string="Phone Number")
    # education info
    accept_type = fields.Char(straing='Type of acceptance')
    # study  information
    school_name = fields.Char(string="School Name")
    cource = fields.Char(straing='cource')
    siting_number= fields.Integer(string="Sitting Number" )
    ratio = fields.Float(string="The Precentage")
    main_desires =fields.Char(straing='Main Desires')
    athoer_desires =fields.Char(straing='other Desires')
    form_number = fields.Integer(string=' Form number')
    pay_date = fields.Char(string='Received  Date')
    firest_pay_date = fields.Char(string='Received  Date')
    secand_pay_date = fields.Char(string='Received  Date')

    # fees
    total_fees = fields.Float(string="Total Assessed Fees")
    register_fees = fields.Char(straing='Register Fees')
    application_fees = fields.Float(string="application  Fees")
    discount = fields.Char(string="Discount")
    firest_installment_fees = fields.Float(string="First installment")
    secand_installment_fees = fields.Float(string="Secand installment")
    year = fields.Char('Study Year',  default=lambda self: datetime.datetime.now().year)
    # Exam year
    exam_year = fields.Date(string='Exam year')
    # Exam center
    exam_center = fields.Char(string='Exam center')
    # Form number
    # The percentage obtained in the certificate
    degree = fields.Float(string='degree')
    # Type of identification
    id_type = fields.Char(string='Type of identification')
    # ID number
    id_number= fields.Integer(string="ID Number" )
    # Type of certificate
    certificate_type = fields.Char(string='Type of certificate')
    # The course
    course = fields.Char(string=' The course')
    # Submission date
    submission_date = fields.Char(string='Submission date')
    # phone number
    phone_number= fields.Integer(string="Phone Number" )
    # Signature of Applicant
    sgnature= fields.Char(string='Signature',defualt="--------------------")
    receipt_code = fields.Char(string='	Receipt Number ')
    fee_paid_id= fields.One2many(
        'napata.feepaid', 'student_id', string="Sessions")



class feesPaid(models.Model):
    _name = 'napata.feepaid'
    _inherit = ['mail.thread']
    name = fields.Float(string="installment")
    student_id = fields.Many2one('napata.register', string="Student  ID",
                                 ondelete='cascade')
    paid_date = fields.Date(string="Date")
























