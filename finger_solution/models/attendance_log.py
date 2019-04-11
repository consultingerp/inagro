# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime 
from datetime import datetime,timedelta
import requests
import re
import logging
_logger = logging.getLogger(__name__)


class att_log(models.Model):
    """ Add user id machine in employee """
    _name = 'attendance.log'
    _order = "date_time desc"

    name = fields.Many2one('hr.employee','Name',required=True)
    char_log = fields.Char(String="Fingerprint Time")
    date_time = fields.Datetime('Date log temp', required=False, readonly=False, select=True
                , default=lambda self: fields.datetime.now())

    @api.onchange('date_time')
    def onchange_time(self):
        time_check_in = datetime.strptime(str(self.date_time), '%Y-%m-%d %H:%M:%S')
        time_check_in_gmt7 = time_check_in + timedelta(hours = 7)
        self.char_log = self.date_time
        # self.char_log = time_check_in_gmt7


    @api.model
    def cek_fingerprint(self):
        """ sync 1 direction machine to odoo """
        def get_data_from_x302_s(self, date, x302_user_id=""):
            r = requests.session()

            print(x302_user_id,' x302_user_id')
            datas = {
                'sdate': date, 'edate': date, 
                'uid': x302_user_id}

            # datas = {
            #     'sdate': date, 'edate': date}

            print (datas, 'datas')
            block = []
            try:
                print ('konek')
                response = r.post('http://192.168.10.91/form/Download',data=datas, stream=True)
                print (response,'response')
                # response = r.post('http://192.168.10.91/form/Download', stream=True)
                block = response.text.split('\n')
                # print (block,'block')
            except:
                # Failed to connect machine 
                print ('failed konek')
                pass

            # print('============= stop =============')
            return block
        

        # tes from 04-03-2019 sd 07-03-2019
        today = fields.date.today()
        # today = '2019-03-06'
        
        emp_obj = self.env['hr.employee']
        attendance_obj = self.env['attendance.log']
        # search employee who registered on machine
        emp_ids = emp_obj.search([('x302_s_user_id', '!=', 0)])
        # print(emp_ids,'karyawan')
        today_attendance = attendance_obj.search([('date_time', '>=', str(today) + " 00:00:00")])

        # print(str(today),'today')
        # print(today_attendance,'today_attendance')
        regex = re.compile(r'[\n\r\t]') # remove 3 character
        for emp_id in emp_ids:
            print('============= start =============')
            print(emp_id.id,emp_id.name,'data karyawan')
            emp_attendance = today_attendance.filtered(lambda x: x.name.id == emp_id.id)
            # emp_attendance = today_attendance.filtered(lambda x:x)
            print(emp_attendance,'emp_attendance')
            if not emp_attendance:
                # block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                print(block,'block')
                print(len(block),'len block')
                if len(block) <= 1:
                    continue
                block.pop()
                # print(len(block),'len(block)')
                last_idx_awal = len(block) - 2
                last_idx = len(block) - 1

                print(last_idx_awal,last_idx,' idx')
                _logger.debug("Check block => "+str(block))
                while(last_idx > -1):
                    row = regex.sub(' ', block[last_idx])
                    row = row.split(' ')

                    # row_awal = regex.sub(' ', block[last_idx_awal])
                    # row_awal = row_awal.split(' ')

                    # print(row_awal,'awal')

                    # print(row)

                    print(row,'row')
                    # print(len(row),'len row')
                    _logger.debug(row)
                    print(len(row),' row 9')
                    cek_row = ""
                    check_in = ""
                    # check_out = ""
                    if len(row) <= 2:
                        cek_row = ""
                        check_in = ""
                        # check_out = ""
                        print(emp_id.id,emp_id.name,row[2],row[3],row[5],check_in,'data 1')
                    elif len(row) > 2 and len(row) <= 7:
                        cek_row = row[5]
                        check_in = row[2] + " " +row[3]
                        # check_out = row[2] + " " +row[3]

                        print(len(check_in),'prr1')
                        print(emp_id.id,emp_id.name,row[2],row[3],row[5],check_in,'data 2')
                    elif len(row) >= 9:
                        cek_row = row[7]
                        check_in = row[4] + " " +row[5]
                        # check_out = row[4] + " " +row[5]

                        print(len(check_in),'prr1')
                        print(emp_id.id,emp_id.name,row[2],row[3],row[5],check_in,'data 21')
                    else:
                        cek_row = row[6]
                        check_in = row[3] + " " +row[4]
                        # check_out = row[3] + " " +row[4]

                        print(len(check_in),'prr2')
                        print(emp_id.id,emp_id.name,row[3],row[4],row[5],check_in,'data 3')

                    print(cek_row,'cek_row')



                    # if row[5] == '0':
                    if cek_row == '0':
                        _logger.debug("Create check in for "+ emp_id.name)
                        # atten_time_check_in = datetime.strptime(check_in, '%Y-%m-%d %H:%M:%S')
                        # atten_time_check_in_gmt7 = atten_time_check_in - timedelta(hours = 7)
                        # print(atten_time_check_in,'atten_time_check_in')
                        # print(atten_time_check_in_gmt7,'atten_time_check_in_gmt7')
                        print({
                            'name': emp_id.id,
                            'date_time': check_in,
                            'char_log': check_in
                        })

                        respone = attendance_obj.create({
                            'name': emp_id.id,
                            'date_time': check_in,
                            'char_log': check_in
                        })
                        
                        # _logger.info("Succeed with ID : "+ str(respone.id))
                    last_idx -= 1
            else:
                _logger.debug("UPDATE EXISTING ATTENDANCE")
                # block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                # if len(block) == 0:
                #     continue
                # block.pop()
                # last_idx = len(block) - 1
                # while(last_idx > -1):
                #     row = regex.sub(' ', block[last_idx])
                #     row = row.split(' ')
                #     _logger.debug(row)
                #     if row[5] == '1':
                #         respone = emp_attendance[0].write({
                #             'check_out': row[2] + " " +row[3],
                #         })
                #         break
                #     last_idx -= 1
        


