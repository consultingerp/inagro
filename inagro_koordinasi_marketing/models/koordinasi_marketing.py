# -*- coding: utf-8 -*-

from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.exceptions import UserError, AccessError
_STATES = [
    ('draft', 'Draft'),
    ('confirm', 'Confirm'),
    ('cancel', 'Cancel')
]

# class Room_marketing(models.Model):
#     _name = 'room.marketing'

#     name = fields.Char('Room Name', required=True)
#     capacity = fields.Integer('Capacity', required=True)

#     _sql_constraints = [('room_marketing_uniq', 'unique (name)', 'Name room must be unique!')]

class outdoor_activities(models.Model):
    _name = 'ourdoor.activities'

    name = fields.Char('Name')
    _sql_constraints = [('activities_uniq', 'unique (name)', 'Name must be unique!')]

class facilities(models.Model):
    _name = 'facilities'

    name = fields.Char('Name')
    _sql_constraints = [('activities_uniq', 'unique (name)', 'Name must be unique!')]

# class food_beverage(models.Model):
#     _name = 'food.beverage'

#     name = fields.Char('Name')
#     _sql_constraints = [('food_uniq', 'unique (name)', 'Name must be unique!')]



class Koordinasi_marketing(models.Model):
    _name = 'koordinasi.marketing'
    _inherit = ['mail.thread']

    name = fields.Char('Activity Number', readonly=True)
    # tanggal = fields.Date('Date Request')
    partner_id = fields.Many2one('res.partner', 'Customer',
                                 index=True,
                                 required=True)
    customer_pic = fields.Char('Customer PIC',required=True)
    customer_contact = fields.Char('Customer Contact',required=True)

    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user, oldname='creating_user_id')

    # employee_id = fields.Many2one('hr.employee', 'Emplopyee',
    #                              index=True,
    #                              track_visibility='onchange',
    #                              required=True)

    @api.one
    @api.depends('user_id')
    def _compute_department(self):
        if (self.user_id.id == False):
            self.department_id = None
            return

        employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)])
        print(employee,' emp')
        if (len(employee) > 0):
            self.department_id = employee[0].department_id.id
        else:
            self.department_id = None

    department_id = fields.Many2one('hr.department', string='Divisi', compute='_compute_department', store=True,)

    date = fields.Date('Date Request',required=True)
    qty_participant = fields.Integer('Number of participants')
    qty_teacher = fields.Integer('Quantity Teacher')
    qty_add_participant = fields.Integer('Additional participants')
    total = fields.Integer('Total')

    state = fields.Selection(selection=_STATES,
                             string='State',
                             index=True,
                             required=True,
                             copy=False,
                             default='draft')

    @api.onchange('qty_participant', 'qty_teacher', 'qty_add_participant')
    def amount_total(self):
        print('tes change')
        self.total = self.qty_participant+self.qty_teacher+self.qty_add_participant

    facilities_ids = fields.One2many('facilities.line', 'fcl_id',
                               'Facilities',
                               readonly=False,
                               copy=True,
                               track_visibility='onchange')

    activities_ids = fields.One2many('activities.line', 'act_id',
                               'Activities',
                               readonly=False,
                               copy=True,
                               track_visibility='onchange')

    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """

        print('create')
        if not vals:
            vals = {}
        vals['name'] = self.env['ir.sequence'].next_by_code('koordinasi.marketing') or 'New'
        return super(Koordinasi_marketing, self).create(vals)


    @api.one
    def _get_flag_readonly(self):
        print(self.env.user.has_group('inagro_koordinasi_marketing.ga_koordinasi_marketing'),' has group')

        if self.state == 'draft':
            if self.create_uid == self.env.user:
                self.flag_readonly = 0
            elif self.env.user.has_group('inagro_koordinasi_marketing.ga_koordinasi_marketing') == True:
                self.flag_readonly = 0
            else:
                self.flag_readonly = 1
        else:
            self.flag_readonly = 1

        # print()
    flag_readonly = fields.Integer(string='Flag Readonly', store=False, compute = "_get_flag_readonly") 

    @api.multi
    def confirm_request(self):
        for fcl in self.facilities_ids:
            fcl.state = 'confirm'

        for act in self.activities_ids:
            act.state = 'confirm'
        return self.write({'state': 'confirm'})

    @api.multi
    def draft_request(self):
        for fcl in self.facilities_ids:
            fcl.state = 'draft'

        for act in self.activities_ids:
            act.state = 'draft'
        return self.write({'state': 'draft'})

    @api.multi
    def unlink(self):
        if self.create_uid != self.env.user or self.state != 'draft':
            raise UserError(_('You cannot delete this data !!!'))
        return super(Koordinasi_marketing, self).unlink()


class facilities_line(models.Model):

    _name = "facilities.line"
    _description = "Facilities Line"

    name = fields.Many2one('facilities', string='Name',required=True)
    qty = fields.Integer('Number of participants')
    start = fields.Datetime('Start')
    end = fields.Datetime('End')
    state = fields.Selection(selection=_STATES,
                             string='State',
                             index=True,
                             required=True,
                             copy=False,
                             default='draft')
    fcl_id = fields.Many2one('koordinasi.marketing',
                                 'MK Number',
                                 ondelete='cascade', readonly=True)
    date_request = fields.Date('Date Request', readonly=True,related='fcl_id.date',store=True)
    info = fields.Char('Information')


class activities_line(models.Model):

    _name = "activities.line"
    _description = "Activities Line"

    name = fields.Many2one('ourdoor.activities', string='Name',required=True)
    qty = fields.Integer('Number of participants')
    start = fields.Datetime('Start')
    end = fields.Datetime('End')
    state = fields.Selection(selection=_STATES,
                             string='State',
                             index=True,
                             required=True,
                             copy=False,
                             default='draft')
    act_id = fields.Many2one('koordinasi.marketing',
                                 'MK Number',
                                 ondelete='cascade', readonly=True)
    date_request = fields.Date('Date Request', readonly=True,related='act_id.date',store=True)


