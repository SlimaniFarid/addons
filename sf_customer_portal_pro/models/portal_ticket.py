from datetime import timedelta

from odoo import api, fields, models


class PortalTicket(models.Model):
    _name = 'portal.ticket'
    _description = 'Portal Support Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, create_date desc'

    config_id = fields.Many2one('portal.config', string='Portal Config', required=True, ondelete='cascade')
    name = fields.Char(string='Subject', required=True)
    description = fields.Html(string='Description')

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    # Category & Priority
    category = fields.Selection([
        ('technical', 'Technical Support'),
        ('billing', 'Billing/Invoice'),
        ('order', 'Order Issue'),
        ('return', 'Return/RMA'),
        ('account', 'Account Access'),
        ('general', 'General Inquiry'),
    ], string='Category', required=True)

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='1')

    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='new', tracking=True)

    # Assignment
    user_id = fields.Many2one('res.users', string='Assigned To', tracking=True)
    team_name = fields.Char(string='Support Team')

    # SLA
    sla_deadline = fields.Datetime(string='SLA Deadline')
    sla_status = fields.Selection([
        ('ok', 'On Track'),
        ('warning', 'Warning'),
        ('breached', 'Breached'),
    ], string='SLA Status', compute='_compute_sla_status')

    # Resolution
    resolution = fields.Html(string='Resolution')
    resolved_date = fields.Datetime(string='Resolved Date')
    closed_date = fields.Datetime(string='Closed Date')

    # Customer satisfaction
    satisfaction = fields.Selection([
        ('0', 'Very Dissatisfied'),
        ('1', 'Dissatisfied'),
        ('2', 'Neutral'),
        ('3', 'Satisfied'),
        ('4', 'Very Satisfied'),
    ], string='Satisfaction')

    @api.depends('sla_deadline', 'state')
    def _compute_sla_status(self):
        for ticket in self:
            if ticket.state in ('resolved', 'closed') or not ticket.sla_deadline:
                ticket.sla_status = 'ok'
            elif ticket.sla_deadline < fields.Datetime.now():
                ticket.sla_status = 'breached'
            elif ticket.sla_deadline < fields.Datetime.now() + timedelta(hours=2):
                ticket.sla_status = 'warning'
            else:
                ticket.sla_status = 'ok'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'portal.config'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

