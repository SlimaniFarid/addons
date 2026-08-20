# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AgriCampaign(models.Model):
    _name = 'sf.agri.campaign'
    _description = 'Agricultural Campaign'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Campaign', required=True, index=True)
    farm_id = fields.Many2one('sf.agri.farm', string='Farm', required=True,
                              ondelete='cascade', index=True)
    year = fields.Integer(string='Year', required=True)
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True)
    culture_ids = fields.One2many('sf.agri.culture', 'campaign_id',
                                  string='Cultures')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.agri.campaign')
        return super().create(vals)

    def action_open(self):
        for campaign in self:
            if campaign.state != 'draft':
                raise UserError(_('Only draft campaigns can be opened.'))
            campaign.state = 'open'

    def action_close(self):
        for campaign in self:
            if not self.env.user.has_group(
                    'sf_agriculture.group_agri_manager'):
                raise UserError(_('Only managers can close campaigns.'))
            if campaign.culture_ids.filtered(lambda c: c.state != 'closed'):
                raise UserError(_('All cultures must be closed before '
                                  'closing the campaign.'))
            campaign.state = 'closed'