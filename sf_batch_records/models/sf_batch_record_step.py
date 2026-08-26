# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class SfBatchRecordStep(models.Model):
    _name = 'sf.batch.record.step'
    _description = 'Batch Record Step'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.batch.record.activity.mixin']
    _order = 'sequence asc, id asc'

    batch_record_id = fields.Many2one('sf.batch.record', string='Batch Record',
                                      required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    step_name = fields.Char(string='Step Name', required=True)
    instruction = fields.Text(string='Instruction')
    operator_id = fields.Many2one('res.users', string='Operator', required=True,
                                  default=lambda self: self.env.user)
    started_at = fields.Datetime(string='Started At')
    ended_at = fields.Datetime(string='Ended At')
    completed = fields.Boolean(string='Completed', default=False)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('started_at', 'ended_at')
    def _check_end_after_start(self):
        for step in self:
            if (step.started_at and step.ended_at and step.ended_at < step.started_at):
                raise ValidationError(_('The end datetime cannot be before the start datetime.'))

    def _check_editable(self):
        self.ensure_one()
        if self.batch_record_id.state in ('released', 'rejected', 'cancelled'):
            raise UserError(_('A finished batch record cannot be modified.'))

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('batch_record_id'):
                parent = self.env['sf.batch.record'].browse(vals['batch_record_id'])
                if parent.state in ('released', 'rejected', 'cancelled'):
                    raise UserError(_('A finished batch record cannot be modified.'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._check_editable()
        return super().write(vals)

    def unlink(self):
        for record in self:
            record._check_editable()
        return super().unlink()

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.batch.record'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.batch.record'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
