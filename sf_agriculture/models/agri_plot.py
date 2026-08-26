# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AgriPlot(models.Model):
    _name = 'sf.agri.plot'
    _description = 'Agricultural Plot'
    _order = 'name'

    name = fields.Char(string='Plot', required=True, index=True)
    farm_id = fields.Many2one('sf.agri.farm', string='Farm', required=True,
                              ondelete='cascade', index=True)
    area_ha = fields.Float(string='Area (ha)', required=True)
    soil_type = fields.Selection([
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loam', 'Loam'),
        ('chalky', 'Chalky'),
        ('other', 'Other'),
    ], string='Soil type', default='loam')
    irrigation = fields.Selection([
        ('rain', 'Rain-fed'),
        ('drip', 'Drip'),
        ('sprinkler', 'Sprinkler'),
        ('none', 'None'),
    ], string='Irrigation', default='rain')
    culture_ids = fields.One2many('sf.agri.culture', 'plot_id',
                                  string='Cultures')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.agri.plot')
        return super().create(vals)