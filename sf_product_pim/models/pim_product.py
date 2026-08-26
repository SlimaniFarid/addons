# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pim_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], string='PIM Status', default='draft', required=True, index=True,
       tracking=True)
    pim_category_id = fields.Many2one('sf.pim.category', string='PIM Family',
                                      index=True)
    pim_score = fields.Float(string='Completeness (%)',
                             compute='_compute_pim_score', store=True,
                             aggregator='avg')
    pim_attributes = fields.One2many('sf.pim.product.attribute',
                                     'product_tmpl_id',
                                     string='PIM Attributes')
    pim_publication_ids = fields.One2many('sf.pim.publication',
                                          'product_tmpl_id',
                                          string='Publications')
    pim_review_ids = fields.One2many('sf.pim.review', 'product_tmpl_id',
                                     string='Review History')
    pim_channel_ids = fields.Many2many(
        'sf.pim.channel', string='Published Channels',
        compute='_compute_pim_channels', store=True)

    @api.depends('pim_category_id.attribute_ids.required',
                 'pim_category_id.attribute_ids.field_type',
                 'pim_attributes.attribute_id',
                 'pim_attributes.value',
                 'pim_attributes.value_html',
                 'pim_attributes.image',
                 'pim_attributes.document_ids',
                 'name', 'description')
    def _compute_pim_score(self):
        for template in self:
            if not template.pim_category_id:
                filled = sum(1 for f in (template.name, template.description)
                             if f)
                template.pim_score = round(filled / 2.0 * 100, 2)
                continue
            required = template.pim_category_id.attribute_ids.filtered(
                lambda a: a.required)
            total = len(required)
            if not total:
                template.pim_score = 100.0
                continue
            filled = 0
            for attr in required:
                pa = template.pim_attributes.filtered(
                    lambda x: x.attribute_id.id == attr.id)
                if not pa:
                    continue
                if attr.field_type == 'html':
                    filled += 1 if pa.value_html else 0
                elif attr.field_type == 'image':
                    filled += 1 if pa.image else 0
                elif attr.field_type == 'document':
                    filled += 1 if pa.document_ids else 0
                else:
                    filled += 1 if pa.value else 0
            template.pim_score = round(filled / float(total) * 100, 2)

    @api.depends('pim_publication_ids.state',
                 'pim_publication_ids.channel_id')
    def _compute_pim_channels(self):
        for template in self:
            template.pim_channel_ids = template.pim_publication_ids.filtered(
                lambda p: p.state == 'published').mapped('channel_id')

    @api.onchange('pim_category_id')
    def _onchange_pim_category_id(self):
        if not self.pim_category_id:
            return
        vals = []
        existing = {attr.id for attr in self.pim_attributes.mapped('attribute_id')}
        for attr in self.pim_category_id.attribute_ids:
            if attr.id not in existing:
                vals.append((0, 0, {'attribute_id': attr.id}))
        if vals:
            self.pim_attributes = vals + [(4, r.id) for r in self.pim_attributes]

    def write(self, vals):
        res = super().write(vals)
        if 'pim_attributes' in vals or 'pim_category_id' in vals:
            self._check_published_consistency()
        if vals.get('pim_state'):
            self._check_pim_state_change(vals['pim_state'])
        return res

    def _check_pim_state_change(self, new_state):
        """Only PIM managers may move a product into review/approved/published
        or out of the normal workflow; plain users may only set draft/archived
        through the dedicated actions."""
        if new_state in ('in_review', 'approved', 'published', 'archived'):
            if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
                raise AccessError(_('Only PIM managers can change the PIM '
                                    'status of a product.'))

    def _check_published_consistency(self):
        """R6: a published product losing a required attribute (score below
        the threshold) automatically returns to draft."""
        for template in self:
            if template.pim_state != 'published':
                continue
            threshold = template.company_id.sf_pim_score_threshold \
                if template.company_id else 100.0
            if template.pim_score < threshold:
                template.pim_state = 'draft'
                self.env['sf.pim.review'].create({
                    'product_tmpl_id': template.id,
                    'action': 'rejected',
                    'notes': _('Automatically moved back to draft: '
                               'completeness dropped below the threshold '
                               '(%s%%).') % threshold,
                })
                self._notify_manager(
                    _('PIM: "%s" completeness dropped below threshold')
                    % template.name)

    def action_submit(self):
        self.ensure_one()
        if self.pim_state != 'draft':
            raise UserError(_('Only draft products can be submitted '
                              'for review.'))
        self.pim_state = 'in_review'
        self.env['sf.pim.review'].create({
            'product_tmpl_id': self.id,
            'action': 'submitted',
        })
        self._notify_manager(
            _('PIM: "%s" has been submitted for review') % self.name)

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
            raise AccessError(_('Only PIM managers can approve products.'))
        if self.pim_state != 'in_review':
            raise UserError(_('Only products in review can be approved.'))
        self.pim_state = 'approved'
        self.env['sf.pim.review'].create({
            'product_tmpl_id': self.id,
            'action': 'approved',
        })

    def action_reject(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
            raise AccessError(_('Only PIM managers can reject products.'))
        if self.pim_state != 'in_review':
            raise UserError(_('Only products in review can be rejected.'))
        return {
            'name': _('Reject Product'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.pim.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_product_tmpl_id': self.id},
        }

    def action_publish(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
            raise AccessError(_('Only PIM managers can publish products.'))
        if self.pim_state not in ('approved', 'published'):
            raise UserError(_('Only approved or published products can be '
                              'published on a channel.'))
        return {
            'name': _('Publish to Channel'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.pim.publish.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_product_tmpl_id': self.id},
        }

    def action_withdraw(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
            raise AccessError(_('Only PIM managers can withdraw products.'))
        published = self.pim_publication_ids.filtered(
            lambda p: p.state == 'published')
        published.write({'state': 'withdrawn',
                         'withdrawn_on': fields.Date.context_today(self)})
        if not self.pim_publication_ids.filtered(
                lambda p: p.state == 'published'):
            self.pim_state = 'approved'

    def action_archive(self):
        self.ensure_one()
        self.pim_state = 'archived'
        self.active = False

    def action_restore(self):
        self.ensure_one()
        self.active = True
        self.pim_state = 'draft'

    def _notify_manager(self, summary):
        group = self.env.ref('sf_product_pim.group_pim_manager')
        managers = self.env['res.users'].search([
            ('groups_id', 'in', group.id),
            ('share', '=', False),
        ])
        for manager in managers:
            self.activity_schedule('mail.mail_activity_data_todo',
                                   summary=summary, user_id=manager.id)


class PimProductAttribute(models.Model):
    _name = 'sf.pim.product.attribute'
    _description = 'PIM Product Attribute Value'
    _order = 'attribute_id, id'

    product_tmpl_id = fields.Many2one('product.template', string='Product',
                                      required=True, ondelete='cascade',
                                      index=True)
    attribute_id = fields.Many2one('sf.pim.attribute', string='Attribute',
                                   required=True, ondelete='cascade')
    value = fields.Char(string='Value')
    value_html = fields.Html(string='Long Description')
    image = fields.Image(string='Image', max_width=1024, max_height=1024)
    document_ids = fields.Many2many('ir.attachment', string='Documents')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='product_tmpl_id.company_id',
                                 store=True, readonly=True)

    _sql_constraints = [
        ('tmpl_attr_uniq', 'UNIQUE(product_tmpl_id, attribute_id)',
         _('An attribute can only be set once per product.')),
    ]

    def _check_parent_consistency(self):
        for line in self:
            if line.product_tmpl_id:
                line.product_tmpl_id._check_published_consistency()

    def create(self, vals_list):
        res = super().create(vals_list)
        res._check_parent_consistency()
        return res

    def write(self, vals):
        res = super().write(vals)
        if any(f in vals for f in ('value', 'value_html', 'image',
                                   'document_ids', 'attribute_id')):
            self._check_parent_consistency()
        return res

    def unlink(self):
        parents = self.product_tmpl_id
        res = super().unlink()
        parents._check_published_consistency()
        return res


class PimPublishWizard(models.TransientModel):
    _name = 'sf.pim.publish.wizard'
    _description = 'PIM Publish to Channel'

    product_tmpl_id = fields.Many2one('product.template', string='Product',
                                      required=True)
    channel_id = fields.Many2one('sf.pim.channel', string='Channel',
                                 required=True,
                                 domain="[('active', '=', True)]")
    publish_date = fields.Date(string='Publish date',
                               default=lambda self: fields.Date.context_today(self))

    def action_publish(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_product_pim.group_pim_manager'):
            raise AccessError(_('Only PIM managers can publish products.'))
        template = self.product_tmpl_id
        if template.pim_state not in ('approved', 'published'):
            raise UserError(_('Only approved products can be published.'))
        threshold = template.company_id.sf_pim_score_threshold \
            if template.company_id else 100.0
        if template.pim_score < threshold:
            raise UserError(
                _('This product cannot be published: completeness score '
                  '(%s%%) is below the required threshold (%s%%).')
                % (template.pim_score, threshold))
        self.env['sf.pim.publication'].create({
            'product_tmpl_id': template.id,
            'channel_id': self.channel_id.id,
            'state': 'published',
            'published_on': self.publish_date,
        })
        template.pim_state = 'published'
        return {'type': 'ir.actions.act_window_close'}


class PimRejectWizard(models.TransientModel):
    _name = 'sf.pim.reject.wizard'
    _description = 'PIM Reject Product'

    product_tmpl_id = fields.Many2one('product.template', string='Product',
                                      required=True)
    reason = fields.Text(string='Rejection reason', required=True)

    def action_reject(self):
        self.ensure_one()
        template = self.product_tmpl_id
        if template.pim_state != 'in_review':
            raise UserError(_('Only products in review can be rejected.'))
        template.pim_state = 'draft'
        self.env['sf.pim.review'].create({
            'product_tmpl_id': template.id,
            'action': 'rejected',
            'notes': self.reason,
        })
        return {'type': 'ir.actions.act_window_close'}