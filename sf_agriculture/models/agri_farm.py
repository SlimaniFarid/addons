# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AgriFarm(models.Model):
    _name = 'sf.agri.farm'
    _description = 'Agricultural Farm'
    _order = 'name'

    name = fields.Char(string='Farm', required=True, index=True)
    address = fields.Char(string='Address')
    manager_id = fields.Many2one('res.users', string='Manager',
                                 ondelete='restrict')
    phone = fields.Char(string='Phone')
    plot_ids = fields.One2many('sf.agri.plot', 'farm_id', string='Plots')
    campaign_ids = fields.One2many('sf.agri.campaign', 'farm_id',
                                   string='Campaigns')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.agri.farm')
        return super().create(vals)