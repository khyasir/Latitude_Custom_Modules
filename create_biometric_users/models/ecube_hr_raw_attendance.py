from openerp import models, fields, api

class EcubeRawAttendance(models.Model):
	_name = 'ecube.raw.attendance'
	_description = 'EcubeRawAttendance'
	name = fields.Char('ERP Name')
	machine_name = fields.Char('Machine Name')
	machine_id = fields.Float('Machine id')
	employee_id = fields.Many2one('hr.employee',string="Employee Name")
	attendance_date = fields.Datetime('Attendance Date')