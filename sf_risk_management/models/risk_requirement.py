# -*- coding: utf-8 -*-
from odoo import _, fields, models, api


class RiskRequirement(models.Model):
    _name = 'sf.risk.requirement'
    _description = 'Regulatory Requirement'
    _order = 'code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    regulation = fields.Selection([
        ('nis2', 'NIS2'),
        ('dora', 'DORA'),
        ('iso27001', 'ISO 27001'),
        ('gdpr', 'GDPR'),
        ('iso9001', 'ISO 9001'),
        ('other', 'Other'),
    ], string='Regulation', default='nis2', required=True)
    description = fields.Text(string='Description')
    risk_ids = fields.Many2many(
        'sf.risk',
        'sf_risk_requirement_m2m', 'requirement_id', 'risk_id',
        string='Risks')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)


class RiskRequirementLink(models.Model):
    _name = 'sf.risk.requirement.link'
    _description = 'Risk Requirement Link'

    requirement_id = fields.Many2one('sf.risk.requirement',
                                     string='Requirement',
                                     ondelete='cascade', required=True)
    risk_id = fields.Many2one('sf.risk', string='Risk',
                              ondelete='cascade', required=True)
    coverage = fields.Selection([
        ('full', 'Full'),
        ('partial', 'Partial'),
        ('none', 'None'),
    ], string='Coverage', default='partial')

    _sql_constraints = [
        ('req_risk_uniq', 'UNIQUE (requirement_id, risk_id)',
         'A requirement can only be linked to a risk once.'),
    ]

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.risk'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.risk'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
