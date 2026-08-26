# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AgriCulture(models.Model):
    _name = 'sf.agri.culture'
    _description = 'Agricultural Culture'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Culture', required=True, index=True)
    campaign_id = fields.Many2one('sf.agri.campaign', string='Campaign',
                                  required=True, ondelete='cascade',
                                  index=True)
    plot_id = fields.Many2one('sf.agri.plot', string='Plot', required=True,
                              ondelete='restrict', index=True)
    crop = fields.Selection([
        ('wheat', 'Wheat'),
        ('maize', 'Maize'),
        ('barley', 'Barley'),
        ('rapeseed', 'Rapeseed'),
        ('sunflower', 'Sunflower'),
        ('potato', 'Potato'),
        ('vineyard', 'Vineyard'),
        ('vegetable', 'Vegetable'),
        ('orchard', 'Orchard'),
        ('other', 'Other'),
    ], string='Crop', required=True)
    variety = fields.Char(string='Variety')
    planted_date = fields.Date(string='Planted date')
    harvest_date = fields.Date(string='Harvest date')
    expected_yield = fields.Float(string='Expected yield')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True)
    operation_ids = fields.One2many('sf.agri.operation', 'culture_id',
                                    string='Operations')
    treatment_ids = fields.One2many('sf.agri.treatment', 'culture_id',
                                    string='Treatments')
    harvest_ids = fields.One2many('sf.agri.harvest', 'culture_id',
                                  string='Harvests')
    yield_t_ha = fields.Float(string='Yield (t/ha)',
                              compute='_compute_yield_t_ha', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.agri.culture')
        return super().create(vals)

    @api.depends('harvest_ids', 'harvest_ids.yield_t_ha')
    def _compute_yield_t_ha(self):
        for culture in self:
            culture.yield_t_ha = sum(
                culture.harvest_ids.mapped('yield_t_ha'))

    def action_start_growing(self):
        for culture in self:
            if culture.state != 'draft':
                raise UserError(_('Only draft cultures can be started.'))
            culture.state = 'growing'

    def action_set_harvested(self):
        for culture in self:
            if culture.state != 'growing':
                raise UserError(_('Only growing cultures can be marked '
                                  'as harvested.'))
            culture.state = 'harvested'

    def action_close(self):
        for culture in self:
            if culture.state != 'harvested':
                raise UserError(_('Only harvested cultures can be closed.'))
            culture.state = 'closed'