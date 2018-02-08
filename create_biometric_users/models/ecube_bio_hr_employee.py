# -*- coding: utf-8 -*-
import os
from zklib import zklib
from zklib import zkconst
from datetime import datetime , timedelta
import time
import xmlrpclib
import config
from openerp import models, fields, api
from openerp.exceptions import Warning


class hr_create_user_bio_machine(models.Model):
	_inherit = 'hr.employee'
	
	
	# @api.model
	# def create(self, values):
	# 	record = super(hr_create_user_bio_machine, self).create(values)
	# 	record.emp_machine_id = record.id	
	# 	return record


	@api.multi
	def createBioUsers(self):
		print "111111111111111111111111"
		for m_ip in (config.Machine_ip):
			ip= config.Machine_ip[m_ip]
			print ip
			zk = zklib.ZKLib(ip, int(config.key['port']))
			result=zk.connect()
			if result == False:
				print ip
				print "ereeeeeeeeeeeeeeeeeee"
				continue
			self._singleBioUser(ip)

	def _singleBioUser(self,ip):
		zk = zklib.ZKLib(ip, int(config.key['port']))
		res = zk.connect()
		if res == True:
			zk.enableDevice()
			zk.disableDevice()
			BioUsers = zk.getUser()
			for user in BioUsers[0]:
				if (BioUsers[0][user][0] == str(self.id)):
					raise Warning('User Already Present in Machine.')
			zk.setUser(uid=False, userid=str(self.id), name=str(self.name), password='', role=zkconst.LEVEL_USER)

			zk.enableDevice()
		zk.disconnect()
		zk.refreshData()

	# @api.multi
	# def createBioUsersall(self):
	# 	zk = zklib.ZKLib(config.key['ip'], int(config.key['port']))
	# 	res = zk.connect()
	# 	if res == True:
	# 		zk.enableDevice()
	# 		zk.disableDevice()
	# 		BioUsers = zk.getUser()
	# 		if BioUsers==({}, []):
	# 			record=self.env['hr.employee'].search([])
	# 			for r_list in record:
	# 				for user in BioUsers[0]:
	# 					if (BioUsers[0][user][0] == str(r_list.id)):
	# 						pass
	# 				zk.setUser(uid=False, userid=str(r_list.id), name=str(r_list.name), password='', role=zkconst.LEVEL_USER)

	# 				zk.enableDevice()				
	# 		else:
	# 			for user in BioUsers[0]:
	# 				if (BioUsers[0][user][0] == str(self.id)):
	# 					raise Warning('User Already Present in Machine.')
	# 			zk.setUser(uid=False, userid=str(self.id), name=str(self.name), password='', role=zkconst.LEVEL_USER)

	# 			zk.enableDevice()
				
	# 		zk.disconnect()
	# 		zk.refreshData()
			


	

	@api.multi
	def _updateAttendanceAll(self):
		for m_ip in (config.Machine_ip):
			ip= config.Machine_ip[m_ip]
			print "oooooooooooooooooooooooooo"
			print ip
			zk = zklib.ZKLib(ip, int(config.key['port']))
			result=zk.connect()
			if result == False:
				self._attendance_error(ip)
				continue
			self._updateAttendance(ip)

	def _updateAttendance(self,ip):
		zk = zklib.ZKLib(ip, int(config.key['port']))
		common =  xmlrpclib.ServerProxy('%s/xmlrpc/2/common' % config.key['odooserver'])
		common.version()
		uid = common.authenticate(config.key['db'], config.key['odooLogin'], config.key['odooPasswd'], {})
		api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % config.key['odooserver'])
		res = zk.connect()
		zk.enableDevice()
		zk.disableDevice()
		info = []
		attendance = zk.getAttendance()
		actualServerTime = str(datetime.now())
		requiredServerTime = actualServerTime.split('.')
		requiredServerDate = requiredServerTime[0].split(' ')
		if (attendance):
			for lattendance in attendance:
				time_att = str(lattendance[2].date()) + ' ' +str(lattendance[2].time())
				atten_time1 = datetime.strptime(str(time_att), '%Y-%m-%d %H:%M:%S')
				atten_time = atten_time1 - timedelta(hours=5)
				atten_time = datetime.strftime(atten_time,'%Y-%m-%d %H:%M:%S')
				attenDate = str(atten_time).split(' ')
				if (requiredServerDate[0] == attenDate[0]):
					data = {
					'user_id' :lattendance[0],
					'Date' : str(lattendance[2].date()),
					'Time' : str(lattendance[2].time()),
					'DateTime' : atten_time
						}

					info.append(data)
			allOdooAttendance = api.execute_kw(config.key['db'], uid, config.key['odooPasswd'],
			 'ecube.raw.attendance','search_read',[],
			 {'fields': ['employee_id', 'attendance_date', 'name']})
			# user_id=rec['user_id']
			# name=self.get_machine_name(user_id)
			# print name
			user_machine=zk.getUser()[1]
			for rec in info:
				user_id_name=rec['user_id']
				if (rec['DateTime'] not in [odooAtten['attendance_date'] for odooAtten in allOdooAttendance]) and rec['user_id'] not in [odooAtten['employee_id'][0] for odooAtten in allOdooAttendance]:
					self.env['ecube.raw.attendance'].create({
								'employee_id': rec['user_id'],
								'machine_id': rec['user_id'],
								'attendance_date': rec['DateTime'],
								'name': ip,					
								# 'machine_name': self._get_machine_name(user_id_name,user_machine),				
						})
					# user_id_name=""
					# api.execute_kw(config.key['db'], uid, config.key['odooPasswd'], 'ecube.raw.attendance',
					# 'create', [{
					# 			'employee_id': rec['user_id'],
					# 			'attendance_date': rec['DateTime'],
					# 			'name': ip,
					# 			'machine_id': rec['user_id'],
					# 			'machine_name': self._get_machine_name(user_id_name,user_machine),
					# 			}])


	def _get_machine_name(self,user_id_name, user_machine):
		username = None
		for user in user_machine:
			raw_user=user.split(":")
			if raw_user[0]==user_id_name:
				username=raw_user[1]
		return username

	def _attendance_error(self,ip):
		print ip
		record=self.env['ecube.attendence.error'].search([('date','=',time.strftime("%d/%m/%Y"))])
		print record
		if not record:
			record=self.env['ecube.attendence.error'].create({
				'date': time.strftime("%d/%m/%Y"),
				})
		for x in record:
			print  time.strftime("%H:%M:%S")
			print "jjjjjjjjjjjjjjjjj"
			x.product_ids.create({
				'machine_ip_error': ip,
				'time': datetime.now().strftime("%H:%M:%S"),
				'partner_id': x.id,
				})

# Steps that required for this F*****G machine
# Install https://github.com/dnaextrim/python_zklib this library
# Install Selenium
# Download Gekodriver
# Export path of Geckodriver
# Install sudo apt-get install xvfb
#install sudo pip install pyvirtualdisplay

# sudo apt-get install python-pip
# sudo pip install git+https://github.com/ehtishamfaisal/zklib.git
# sudo pip install pyvirtualdisplay
# sudo pip install selenium
# sudo apt-get install xvfb