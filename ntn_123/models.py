# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ntn(models.Model):
    _inherit = ['res.partner']

    xxntn  = fields.Char(string="NTN")
    xxpntn = fields.Char(string="PNTN")
    xxcnic = fields.Char(string="CNIC")
    xxstrn = fields.Char(string="STRN")