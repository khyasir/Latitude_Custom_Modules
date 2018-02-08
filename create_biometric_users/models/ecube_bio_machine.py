from openerp import models, fields, api

class EcubeMachine(models.Model):
	_name = 'ecube.machine'
	_description = 'EcubeMachine'
	name = fields.Char('Machine Name')
	machine_ip = fields.Char('Machine IP')
	machine_status = fields.Boolean('Machine Status')