# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TraceabilityRecall(models.Model):
    _name = 'sf.traceability.recall'
    _description = 'Batch Recall Event'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, readonly=True)
    lot_id = fields.Many2one('stock.lot', string='Batch / Serial',
                             required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 related='lot_id.product_id', store=True,
                                 readonly=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', default='medium', required=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ], string='Status', default='open', tracking=True)
    reason = fields.Text(string='Reason')
    affected_customers = fields.Char(
        string='Affected Customers', readonly=True,
        help="Computed list of customers who received this batch.")
    date_recall = fields.Date(string='Recall Date',
                              default=fields.Date.context_today)
    partner_count = fields.Integer(string='Affected Partners',
                                   compute='_compute_affected')
    move_count = fields.Integer(string='Movements', compute='_compute_affected')

    @api.depends('lot_id')
    def _compute_affected(self):
        for rec in self:
            moves = self.env['stock.move.line'].search([
                ('lot_id', '=', rec.lot_id.id),
                ('state', '=', 'done'),
            ])
            rec.move_count = len(moves)
            partners = set()
            for move in moves:
                if move.move_id.picking_id and move.move_id.picking_id.partner_id:
                    partners.add(move.move_id.picking_id.partner_id.display_name)
            rec.partner_count = len(partners)
            rec.affected_customers = ', '.join(sorted(partners))

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('sf.traceability.recall')
        vals['name'] = vals.get('name') or seq or 'RECALL/'
        rec = super().create(vals)
        rec.message_post(
            body=_('Recall %s opened for batch %s (severity: %s).')
                 % (rec.name, rec.lot_id.name, rec.severity))
        return rec

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_close(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.traceability.recall'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
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

