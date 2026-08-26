# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AgriHarvest(models.Model):
    _name = 'sf.agri.harvest'
    _description = 'Agricultural Harvest'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Harvest', required=True, index=True)
    culture_id = fields.Many2one('sf.agri.culture', string='Culture',
                                 required=True, ondelete='cascade',
                                 index=True)
    plot_id = fields.Many2one('sf.agri.plot', string='Plot', required=True,
                              ondelete='restrict', index=True)
    harvest_date = fields.Date(string='Harvest date')
    quantity = fields.Float(string='Quantity', default=0.0)
    unit = fields.Selection([
        ('kg', 'kg'),
        ('t', 'tonnes'),
    ], string='Unit', default=lambda self:
    self.env.company.sf_agri_default_unit or 'kg')
    quality = fields.Char(string='Quality')
    yield_t_ha = fields.Float(string='Yield (t/ha)',
                              compute='_compute_yield_t_ha', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('recorded', 'Recorded'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.agri.harvest')
        return super().create(vals)

    @api.depends('quantity', 'unit', 'plot_id.area_ha')
    def _compute_yield_t_ha(self):
        for harvest in self:
            if not harvest.plot_id or not harvest.plot_id.area_ha:
                harvest.yield_t_ha = 0.0
                continue
            tonnes = harvest.quantity
            if harvest.unit == 'kg':
                tonnes = (harvest.quantity or 0.0) / 1000.0
            harvest.yield_t_ha = tonnes / harvest.plot_id.area_ha

    def action_record(self):
        for harvest in self:
            if not self.env.user.has_group(
                    'sf_agriculture.group_agri_manager'):
                raise UserError(_('Only managers can record harvests.'))
            if harvest.state != 'draft':
                raise UserError(_('Only draft harvests can be recorded.'))
            harvest.state = 'recorded'

    def action_close(self):
        for harvest in self:
            if not self.env.user.has_group(
                    'sf_agriculture.group_agri_manager'):
                raise UserError(_('Only managers can close harvests.'))
            if harvest.state != 'recorded':
                raise UserError(_('Only recorded harvests can be closed.'))
            harvest.state = 'closed'