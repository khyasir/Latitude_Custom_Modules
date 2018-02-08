from openerp import models, fields, api

class EcubeMachineAttendenceError(models.Model):
	_name = 'ecube.attendence.error'
	date = fields.Char('Date')

	
	product_ids=fields.One2many('ecube.attendence.error.tree','partner_id')

class EcubeMachineAttendenceErrorTree(models.Model):
	_name = 'ecube.attendence.error.tree'

	machine_ip_error = fields.Char('Machine IP')
	time = fields.Char('Time')
	partner_id=fields.Many2one('ecube.attendence.error')