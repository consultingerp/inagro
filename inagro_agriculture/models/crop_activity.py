# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class inagro_crop_activity(models.Model):
    _name = 'crop.activity'
    _inherit = ['mail.thread']
    _order = "date desc"

    farmer_id = fields.Many2one(
        'res.partner',
        string='Farmer',
        domain="[('is_farmer','=',True)]",
        required=True
    )

    # name = fields.Many2one('farmer.location.crops',string='Crop Code',domain="[('active','=',True)]",required=True)
    # category_id = fields.Many2one('crop.category',string='Category',related="name.category_id",store=True)
    # varieties_id = fields.Many2one('crop.varieties',string='Varieties',related="name.varieties_id",store=True)
    # area_location_id = fields.Many2one('res.partner',string='Location Area',related="name.area_location_id",store=True)

    date = fields.Date(string='Date',required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,default=lambda *a: 'draft')

    line_ids = fields.One2many('crop.activity.line', 'line_id','Activity detail',readonly=False,copy=True,track_visibility='onchange')

    @api.multi
    def button_confirm(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def button_validate(self):
        return self.write({'state': 'done'})

    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def button_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def unlink(self):
        """
        Overrides orm unlink method.
        @param self: The object pointer
        @return: True/False.
        """
        for activity in self:
            if activity.state != 'draft':
                raise ValidationError(_('You cannot delete activity'))
        return super(inagro_crop_activity, self).unlink()


class inagro_crop_activity_line(models.Model):

    _name = 'crop.activity.line'
    _description = "Detail activity"

    area_location_id = fields.Many2one('res.partner',string='Location Area',domain="[('is_location','=',True)]",required=True)
    category_id = fields.Many2one(
        'crop.category',
        string='Commodity',
        required=True
    )

    varieties_id = fields.Many2one(
        'crop.varieties',
        string='Varieties',
        required=True
    )

    crop_id = fields.Many2many('farmer.location.crops','crop_activity_line_crop_rel','activity_line',string='Crop Code',domain="[('active','=',True)]")
    name = fields.Many2one('crop.masteractivity','Activity', required=True)
    description = fields.Text(string='Description')
    line_id = fields.Many2one('crop.activity','Activity',ondelete='cascade', readonly=True)

    # farmer_id = fields.Many2one(
    #     'res.partner',
    #     string='Farmer',
    #     domain="[('is_farmer','=',True)]",
    #     required=True
    # )

    @api.onchange('category_id')
    def on_change_category(self):
        domain = [('category', '=',self.category_id.id )]
        return {'domain': {'varieties_id': domain}}

    @api.onchange('area_location_id','category_id','varieties_id')
    def on_change_area(self):
        '''
        When you change categ_id it check checkin and checkout are
        filled or not if not then raise warning
        -----------------------------------------------------------
        @param self: object pointer
        '''
        domain = {}
        if len(self.area_location_id) < 1 and len(self.category_id) < 1 and len(self.varieties_id) < 1:
            domain = {}
        elif len(self.area_location_id) >= 1 and len(self.category_id) < 1 and len(self.varieties_id) < 1:
            crop = self.env['farmer.location.crops'].search([('area_location_id', '=',self.area_location_id.id)])
            domain = {'crop_id': '''[('id', 'in', %s)]'''%str(crop.ids)}
        elif len(self.area_location_id) >= 1 and len(self.category_id) >= 1 and len(self.varieties_id) < 1:
            crop = self.env['farmer.location.crops'].search([('area_location_id', '=',self.area_location_id.id),('category_id', '=',self.category_id.id)])
            domain = {'crop_id': '''[('id', 'in', %s)]'''%str(crop.ids)}
        elif len(self.area_location_id) >= 1 and len(self.category_id) >= 1 and len(self.varieties_id) >= 1:
            crop = self.env['farmer.location.crops'].search([('area_location_id', '=',self.area_location_id.id),('category_id', '=',self.category_id.id),('varieties_id', '=',self.varieties_id.id)])
            domain = {'crop_id': '''[('id', 'in', %s)]'''%str(crop.ids)}
        else:
            domain = {}



        
        
        return {'domain': domain}