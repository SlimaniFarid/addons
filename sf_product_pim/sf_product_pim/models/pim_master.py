# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PimCategory(models.Model):
    _name = 'sf.pim.category'
    _description = 'PIM Family'
    _order = 'code, name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    parent_id = fields.Many2one('sf.pim.category', string='Parent family',
                                ondelete='restrict')
    child_ids = fields.One2many('sf.pim.category', 'parent_id',
                                string='Sub-families')
    attribute_ids = fields.One2many('sf.pim.attribute', 'category_id',
                                    string='Attributes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('A family with this name already exists.')),
    ]


class PimAttribute(models.Model):
    _name = 'sf.pim.attribute'
    _description = 'PIM Attribute'
    _order = 'category_id, sequence, name'

    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('sf.pim.category', string='Family',
                                  ondelete='cascade')
    field_type = fields.Selection([
        ('text', 'Text'),
        ('html', 'HTML'),
        ('selection', 'Selection'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('numeric', 'Numeric'),
        ('date', 'Date'),
    ], string='Type', required=True, default='text')
    required = fields.Boolean(string='Required for score')
    translated = fields.Boolean(string='Translatable')
    sequence = fields.Integer(string='Sequence', default=10)
    unit = fields.Char(string='Unit')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('cat_name_uniq', 'UNIQUE(category_id, name)',
         _('This attribute already exists in this family.')),
    ]


class PimChannel(models.Model):
    _name = 'sf.pim.channel'
    _description = 'PIM Publication Channel'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('A channel with this name already exists.')),
    ]


class PimPublication(models.Model):
    _name = 'sf.pim.publication'
    _description = 'PIM Product Publication'
    _order = 'published_on desc, id desc'

    product_tmpl_id = fields.Many2one('product.template', string='Product',
                                      required=True, ondelete='cascade')
    channel_id = fields.Many2one('sf.pim.channel', string='Channel',
                                 required=True, ondelete='restrict')
    state = fields.Selection([
        ('published', 'Published'),
        ('withdrawn', 'Withdrawn'),
    ], string='Status', default='published', required=True)
    published_on = fields.Date(string='Published on')
    withdrawn_on = fields.Date(string='Withdrawn on')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='product_tmpl_id.company_id',
                                 store=True, readonly=True)

    _sql_constraints = [
        ('tmpl_channel_uniq', 'UNIQUE(product_tmpl_id, channel_id)',
         _('This product is already published on this channel.')),
    ]


class PimReview(models.Model):
    _name = 'sf.pim.review'
    _description = 'PIM Review History'
    _order = 'date desc, id desc'

    product_tmpl_id = fields.Many2one('product.template', string='Product',
                                      required=True, ondelete='cascade')
    action = fields.Selection([
        ('submitted', 'Submitted for review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Action', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now,
                           required=True)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.user)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='product_tmpl_id.company_id',
                                 store=True, readonly=True)