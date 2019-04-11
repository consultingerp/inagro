# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime 
from datetime import datetime,timedelta
import requests
import re
import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    """ Add user id machine in employee """
    _inherit = 'hr.employee'

    x302_s_user_id = fields.Integer('Machine user ID', help="ID on fingerprint.")


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    _order = 'check_in desc'

    check_in_log = fields.Char(String="Check in Time")
    check_out_log = fields.Char(String="Check out Time")




    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        # for attendance in self:
        #     # we take the latest attendance before our check_in time and check it doesn't overlap with ours
        #     last_attendance_before_check_in = self.env['hr.attendance'].search([
        #         ('employee_id', '=', attendance.employee_id.id),
        #         ('check_in', '<=', attendance.check_in),
        #         ('id', '!=', attendance.id),
        #     ], order='check_in desc', limit=1)
        #     if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
        #         raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
        #             'empl_name': attendance.employee_id.name,
        #             'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_in))),
        #         })

        #     if not attendance.check_out:
        #         # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
        #         no_check_out_attendances = self.env['hr.attendance'].search([
        #             ('employee_id', '=', attendance.employee_id.id),
        #             ('check_out', '=', False),
        #             ('id', '!=', attendance.id),
        #         ])
        #         if no_check_out_attendances:
        #             raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
        #                 'empl_name': attendance.employee_id.name,
        #                 'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(no_check_out_attendances.check_in))),
        #             })
        #     else:
        #         # we verify that the latest attendance with check_in time before our check_out time
        #         # is the same as the one before our check_in time computed before, otherwise it overlaps
        #         last_attendance_before_check_out = self.env['hr.attendance'].search([
        #             ('employee_id', '=', attendance.employee_id.id),
        #             ('check_in', '<', attendance.check_out),
        #             ('id', '!=', attendance.id),
        #         ], order='check_in desc', limit=1)
        #         if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
        #             raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
        #                 'empl_name': attendance.employee_id.name,
        #                 'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(last_attendance_before_check_out.check_in))),
        #             })

        return True

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_in_check_out(self):
        """ verifies if check_in is earlier than check_out. """
        # for attendance in self:
        #     if attendance.check_in and attendance.check_out:
        #         if attendance.check_out < attendance.check_in:
        #             raise exceptions.ValidationError(_('"Check Out" time cannot be earlier than "Check In" time.'))



    @api.onchange('check_in')
    def _check_in(self):
        # time_check_in = datetime.strptime(str(self.date_time), '%Y-%m-%d %H:%M:%S')
        # time_check_in_gmt7 = time_check_in + timedelta(hours = 7)
        self.check_in_log = self.check_in

    @api.onchange('check_out')
    def _check_out(self):
        # time_check_in = datetime.strptime(str(self.date_time), '%Y-%m-%d %H:%M:%S')
        # time_check_in_gmt7 = time_check_in + timedelta(hours = 7)
        self.check_out_log = self.check_out


    @api.model
    def get_fingerprint_log(self):

        # tes from 04-03-2019 sd 07-03-2019
        # today = fields.date.today()
        today1 = '2019-03-04'
        today = datetime.strptime(today1, '%Y-%m-%d')
        print(today,' today2')
        next_date = today + timedelta(days=1)

        # print(next_day,' next_day')



        employee_id = self.env['hr.employee'].search([('x302_s_user_id', '!=', 0)])
        employee_id_count = self.env['hr.employee'].search_count([('x302_s_user_id', '!=', 0)])
        attendance = self.env['hr.attendance']

        # print(employee_id)
        print(employee_id_count,' count')

        no = 0
        for emp in employee_id:
            no = no+1
            finger_log_in = self.env['attendance.log'].search(['&','&',('name', '=',int(emp.id)),('date_time', '>=', str(today)),('date_time', '<=', str(next_date))], order='date_time asc', limit=1)
            finger_log_out = self.env['attendance.log'].search(['&','&',('name', '=',int(emp.id)),('date_time', '>=', str(today)),('date_time', '<=', str(next_date))], order='date_time desc', limit=1)

            print('no: ',no)
            print('nama : ',emp.name)
            # print('log in name : ',finger_log_in.name.name)
            # print('log in : ',finger_log_in.date_time)
            # print('log out : ',finger_log_out.date_time)

            log_in_time = finger_log_in.date_time
            log_out_time= finger_log_out.date_time

            if log_in_time == log_out_time:
                log_in_time = finger_log_in.date_time
                log_out_time= False

            print('log in : ',log_in_time)
            print('log out : ',log_out_time)

            if log_in_time != False: 
                respone = attendance.create({
                            'employee_id': emp.id,
                            'check_in': log_in_time,
                            'check_out': log_out_time,
                            'check_in_log': log_in_time,
                            'check_out_log': log_out_time,
                        })
                        
                _logger.info("Succeed with ID : "+ str(respone.id))


            # for fg in finger_log_in:
            #     print('log in name : ',fg.name.name)
            #     print('log in : ',fg.date_time)

            print('=====================================================================')