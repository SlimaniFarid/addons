# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SlottingAnalysis(models.Model):
    _name = 'sf.warehouse.heatmap.slotting.analysis'
    _description = 'Slotting Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    warehouse_id = fields.stock.warehouse(string='Warehouse Id', required=True)
    analysis_date = fields.Analysis(string='Analysis Date', default=fields.Date.today)
    abc_a_pct = fields.Class(string='Abc A Pct', default=20)
    abc_b_pct = fields.Class(string='Abc B Pct', default=30)
    state = fields.draft,computed(string='State', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.warehouse.heatmap.slotting.analysis') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()
    
    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

