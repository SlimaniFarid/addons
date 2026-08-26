# -*- coding: utf-8 -*-
"""Customer onboarding models."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCobTemplate(models.Model):
    _name = 'sf.cob.template'
    _description = 'Onboarding Template'

    name = fields.Char(string='Template Name', required=True)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)
    step_ids = fields.One2many('sf.cob.template.step', 'template_id',
                               string='Steps', copy=True)


class SfCobTemplateStep(models.Model):
    _name = 'sf.cob.template.step'
    _description = 'Onboarding Template Step'
    _order = 'sequence, id'

    template_id = fields.Many2one('sf.cob.template', required=True,
                                  ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Step', required=True)
    step_type = fields.Selection([
        ('document', 'Document'), ('contract', 'Contract'),
        ('setup', 'Account Setup'), ('training', 'Training'),
        ('other', 'Other')], default='document')
    description = fields.Text(string='Instructions')


class SfCustomerOnboarding(models.Model):
    _name = 'sf.customer.onboarding'
    _description = 'Customer Onboarding'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    template_id = fields.Many2one('sf.cob.template',
                                  string='Onboarding Template', required=True)
    owner_id = fields.Many2one('res.users', string='Onboarding Owner',
                               default=lambda s: s.env.uid)
    task_ids = fields.One2many('sf.customer.onboarding.task', 'onboarding_id',
                               string='Tasks')
    task_count = fields.Integer(compute='_compute_stats')
    done_count = fields.Integer(compute='_compute_stats')
    progress = fields.Float(compute='_compute_stats')
    first_order_id = fields.Many2one('sale.order', string='First Sale Order')
    state = fields.Selection([
        ('draft', 'Draft'), ('in_progress', 'In Progress'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft', tracking=True)
    completed_date = fields.Date(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.onboarding') or 'COB-NEW'
        return super().create(vals_list)

    def _compute_stats(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)
            rec.done_count = len(rec.task_ids.filtered(lambda t: t.done))
            rec.progress = (rec.done_count / rec.task_count * 100.0
                            if rec.task_count else 0.0)

    def action_start(self):
        self.ensure_one()
        if self.task_ids:
            raise UserError(_('Tasks already generated.'))
        vals_list = [{'onboarding_id': self.id, 'sequence': s.sequence,
                      'name': s.name, 'step_type': s.step_type,
                      'description': s.description}
                     for s in self.template_id.step_ids]
        self.env['sf.customer.onboarding.task'].create(vals_list)
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.ensure_one()
        pending = self.task_ids.filtered(lambda t: not t.done)
        if pending:
            raise UserError(_('%s tasks are not done.') % len(pending))
        self.write({'state': 'completed',
                    'completed_date': fields.Date.today()})


class SfCustomerOnboardingTask(models.Model):
    _name = 'sf.customer.onboarding.task'
    _description = 'Onboarding Task'

    onboarding_id = fields.Many2one('sf.customer.onboarding', required=True,
                                    ondelete='cascade')
    company_id = fields.Many2one(related='onboarding_id.company_id',
                                 store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Task', required=True)
    step_type = fields.Selection([
        ('document', 'Document'), ('contract', 'Contract'),
        ('setup', 'Account Setup'), ('training', 'Training'),
        ('other', 'Other')], default='document')
    description = fields.Text(string='Instructions')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    done = fields.Boolean(string='Done', default=False)
    done_date = fields.Date(readonly=True)

    def action_toggle_done(self):
        for rec in self:
            rec.write({'done': not rec.done,
                       'done_date': fields.Date.today() if not rec.done
                       else False})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.cob.template'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
